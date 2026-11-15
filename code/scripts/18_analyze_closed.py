#!/usr/bin/env python3
"""Analyse phase-2 runs on closed models (results/closed/raw/<ds>/<model>/<tag>/).

Per method (tie-aware, as in phase 0):
  top1     expected top-1 hit when the max-score tie group is broken uniformly
  rec@g    expected recall of gold within the top-|gold| (ties at the cut split)
  signal   all_zero / unique_max / reaches_tau rates
Derived rows (no extra calls):
  MEXGEN_LOO           MExGen-inspired token-F1 LOO adaptation: P1 ablated answers re-scored
                       with 1 - token-F1 (not a full reproduction of MExGen / C-LIME)
  RM<K>:<est>_<value>  random-masking estimators (banzhaf | linear) x (exact | f1)
  RM@k                 the first k masks of the K-mask run (k-convergence for tuning K)
Stability (repeat 1 vs repeat 0): top-1 agreement, tie-preserving Spearman, identical phi.
Cost: issued-call cost per instance per method (cache hits free; methods run in
the order of the run, so P1's reference answer is paid once).

  python scripts/18_analyze_closed.py --tag pilot
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from collections import defaultdict

import numpy as np
from scipy.stats import spearmanr

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)

from src.pipelines.subset import SCALARIZERS, banzhaf, mexgen_loo_from_p1, ridge  # noqa: E402

RAW = os.path.join(ROOT, "results", "closed", "raw")
OUT = os.path.join(ROOT, "results", "closed", "analysis")


def tie_top1(phi, gold):
    phi = np.asarray(phi, float)
    T = np.flatnonzero(phi == phi.max())
    return sum(int(i) in set(gold) for i in T) / len(T)


def topk_inclusion(phi, k):
    phi = np.asarray(phi, float)
    inc, slots = np.zeros_like(phi), k
    for v in np.sort(np.unique(phi))[::-1]:
        if slots <= 0:
            break
        grp = np.flatnonzero(phi == v)
        take = min(slots, len(grp))
        inc[grp] = take / len(grp)
        slots -= take
    return inc


def rec_gold(phi, gold):
    if not gold:
        return np.nan
    return float(topk_inclusion(phi, len(gold))[list(gold)].sum() / len(gold))


def row_stats(rows):
    if not rows:
        return {}
    phis = [np.asarray(r["phi"], float) for r in rows]
    return {
        "n": len(rows),
        "top1": float(np.mean([tie_top1(p, r["gold"]) for p, r in zip(phis, rows)])),
        "rec@g": float(np.nanmean([rec_gold(p, r["gold"]) for p, r in zip(phis, rows)])),
        "random_top1": float(np.mean([len(r["gold"]) / len(r["phi"]) for r in rows])),
        "all_zero": float(np.mean([not p.any() for p in phis])),
        "unique_max": float(np.mean([np.sum(p == p.max()) == 1 for p in phis])),
        "reaches_tau": float(np.mean([(p >= 0.5).any() for p in phis])),
        "calls/inst": float(np.mean([r.get("n_calls", 0) for r in rows])),
    }


def load(path):
    return [json.loads(l) for l in open(path, encoding="utf-8")] if os.path.exists(path) else []


def rm_variants(rows):
    """Extra estimator rows and prefix-k rows from stored RM answers."""
    out = defaultdict(list)
    for r in rows:
        meta = r["meta"]
        a0 = r.get("baseline_answer")
        masks = np.array(meta["masks"], dtype=bool)
        K = len(masks)
        for key, phi in (meta.get("scores") or {}).items():
            out[f"RM{K}:{key}"].append({**r, "phi": phi})
        if a0 is None:
            continue
        y = np.array([SCALARIZERS["exact"](a, a0) for a in meta["mask_answers"]], float)
        for k in (8, 16, 32):
            if k < K:
                out[f"RM@{k}"].append({**r, "phi": banzhaf(masks[:k], y[:k]).tolist(), "n_calls": k + 1})
    return out


def stability(a_rows, b_rows):
    A = {r["qid"]: r for r in a_rows}
    B = {r["qid"]: r for r in b_rows}
    qs = sorted(set(A) & set(B))
    if not qs:
        return {}
    agree, rho, same, per_src, per_src_same_a0 = [], [], [], [], []
    for q in qs:
        pa, pb = np.asarray(A[q]["phi"], float), np.asarray(B[q]["phi"], float)
        same.append(bool(np.array_equal(pa, pb)))
        # per-source agreement: a 20-dim vector differs if ONE entry differs, so the
        # whole-vector rate alone overstates instability. Separately on items whose
        # two reference answers a0 coincide (estimator stability given a0) vs all
        # items (end-to-end: a0 regenerated, then the whole procedure).
        ps = float(np.mean(np.isclose(pa, pb)))
        per_src.append(ps)
        a0a, a0b = A[q].get("baseline_answer"), B[q].get("baseline_answer")
        if a0a is not None and a0a == a0b:
            per_src_same_a0.append(ps)
        ta, tb = set(np.flatnonzero(pa == pa.max())), set(np.flatnonzero(pb == pb.max()))
        agree.append(len(ta & tb) / len(ta | tb))  # Jaccard of top-tie groups
        if pa.std() > 0 and pb.std() > 0:
            rho.append(spearmanr(pa, pb)[0])
    return {"n": len(qs), "identical_phi": float(np.mean(same)), "per_source_agree": float(np.mean(per_src)),
            "n_same_a0": len(per_src_same_a0),
            "per_source_agree_same_a0": float(np.mean(per_src_same_a0)) if per_src_same_a0 else np.nan,
            "top_group_jaccard": float(np.mean(agree)),
            "spearman_tie_preserving": float(np.mean(rho)) if rho else np.nan, "n_rho_defined": len(rho)}


def _tie_jacc(a, b):
    ta, tb = set(np.flatnonzero(a == a.max())), set(np.flatnonzero(b == b.max()))
    return len(ta & tb) / len(ta | tb)


def k_convergence(rm_rows, ks=(8, 16, 32)):
    """Prefix-k vs K_max (NOT independent: the prefix is part of K_max) and, as the
    honest check, the two disjoint halves (masks 1..K/2 vs K/2+1..K). Top groups
    are compared tie-aware (Jaccard of top-tie sets), never by argmax index.
    This shows sensitivity to K, not convergence to the true value."""
    out = {}
    half_rho, half_j, uniq = [], [], []
    for r in rm_rows:
        a0 = r.get("baseline_answer")
        if a0 is None:
            continue
        masks = np.array(r["meta"]["masks"], dtype=bool)
        y = np.array([SCALARIZERS["exact"](a, a0) for a in r["meta"]["mask_answers"]], float)
        uniq.append(len({tuple(m) for m in masks.tolist()}))
        h = len(masks) // 2
        a, b = banzhaf(masks[:h], y[:h]), banzhaf(masks[h:], y[h:])
        if a.std() > 0 and b.std() > 0:
            half_rho.append(spearmanr(a, b)[0])
        half_j.append(_tie_jacc(a, b))
    out["halves"] = {"spearman_vs_Kmax": float(np.mean(half_rho)) if half_rho else np.nan,
                     "argmax_agree": float(np.mean(half_j)) if half_j else np.nan,
                     "unique_masks_min": int(min(uniq)) if uniq else None,
                     "unique_masks_mean": float(np.mean(uniq)) if uniq else np.nan}
    for k in ks:
        rho, agree = [], []
        for r in rm_rows:
            a0 = r.get("baseline_answer")
            if a0 is None:
                continue
            masks = np.array(r["meta"]["masks"], dtype=bool)
            if k >= len(masks):
                continue
            y = np.array([SCALARIZERS["exact"](a, a0) for a in r["meta"]["mask_answers"]], float)
            full, pre = banzhaf(masks, y), banzhaf(masks[:k], y[:k])
            if full.std() > 0 and pre.std() > 0:
                rho.append(spearmanr(full, pre)[0])
            agree.append(_tie_jacc(full, pre))
        out[k] = {"spearman_vs_Kmax": float(np.mean(rho)) if rho else np.nan,
                  "argmax_agree": float(np.mean(agree)) if agree else np.nan}
    return out


M_AVG = {"hotpotqa": 10, "musique": 20}


def formula_calls(method: str, M: int, rm_k: int, full_repeats: int = 3) -> int:
    """Calls per instance without cache sharing (an upper bound)."""
    from src.pipelines.registry import METHODS
    base = method.split(".")[0]
    if base in METHODS:
        m = METHODS[base]
        N = 1 if m.sampling == "single_pass" else (5 if m.is_verbalize else 3)
        kappa = 2 if m.prompting == "self_probing" else 1
        extra = 0 if m.is_verbalize else full_repeats * kappa
        return m.query_cost(M, N) + extra
    if base.startswith("RM"):
        return rm_k + 1
    if base == "LOI":
        return M + 1
    return 0


def projection(cost_rows, kconv, rm_k_main: int = 32):
    summ = json.load(open(os.path.join(ROOT, "results", "closed", "screen", "summary.json")))
    n_eval = {}
    for r in summ["screening"]:
        if r["pool"] != "audit":
            n_eval[(r["model"], r["dataset"])] = r["evaluable"]
    out = []
    for c in cost_rows:
        if not c["calls_issued"]:
            continue
        per_call = c["cost_cny"] / c["calls_issued"]
        m = c["method"]
        k = rm_k_main if m.startswith("RM") else 0
        calls = formula_calls(m, M_AVG[c["dataset"]], k)
        n = n_eval.get((c["model"], c["dataset"]), 0)
        out.append({"dataset": c["dataset"], "model": c["model"], "method": (f"RM{k}" if k else m),
                    "cny_per_call": round(per_call, 7), "calls_per_inst": calls,
                    "cny_per_inst": round(per_call * calls, 5), "n_eval": n,
                    "cny_total": round(per_call * calls * n, 3)})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="pilot")
    ap.add_argument("--split", default="all", choices=["all", "test", "dev"],
                    help="dev = the pilot qids of that model x dataset (pilot/qids.json); "
                         "test = all other qids (main tables)")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    out_name = args.tag if args.split == "all" else f"{args.tag}.{args.split}"
    table, stab, cost, kconv = [], [], [], []
    for d in sorted(glob.glob(os.path.join(RAW, "*", "*", args.tag))):
        ds, model = d.split(os.sep)[-3], d.split(os.sep)[-2]
        files = {os.path.basename(p)[:-6]: p for p in glob.glob(os.path.join(d, "*.jsonl"))}
        R = {k: load(p) for k, p in files.items()}
        if args.split != "all":
            qp = os.path.join(RAW, ds, model, "pilot", "qids.json")
            dev = set(json.load(open(qp))) if os.path.exists(qp) else set()
            keep = (lambda q: q in dev) if args.split == "dev" else (lambda q: q not in dev)
            R = {k: [r for r in rows if keep(r["qid"])] for k, rows in R.items()}
        derived = {}
        if R.get("P1"):
            derived["MEXGEN_LOO"] = [mexgen_loo_from_p1(r, r["gold"]) for r in R["P1"]
                                     if r["meta"].get("ablated_answers") is not None]
        for k, rows in list(R.items()):
            if k.startswith("RM") and "." not in k:
                derived.update(rm_variants(rows))
                for kk, v in k_convergence(rows).items():
                    kconv.append({"dataset": ds, "model": model, "k": kk, **v})
        for k in sorted(set(R) | set(derived)):
            rows = R.get(k) or derived.get(k)
            st = row_stats(rows)
            if st:
                if k == "P1" or (k.startswith("P") and "." not in k):
                    fc = [r["meta"].get("full_context_change_rate") for r in rows
                          if r["meta"].get("full_context_change_rate") is not None]
                    st["full_ctx_change"] = float(np.mean(fc)) if fc else np.nan
                table.append({"dataset": ds, "model": model, "method": k, **st})
        for m in ("V1", "P1"):
            if R.get(m) and R.get(f"{m}.r1"):
                stab.append({"dataset": ds, "model": model, "method": m, **stability(R[m], R[f"{m}.r1"])})
        for p in glob.glob(os.path.join(d, "*.cost.json")):
            c = json.load(open(p))
            tot = sum(x["est_cost_cny"] for x in c["runs"])
            n = sum(x["n_instances_run"] for x in c["runs"])
            calls = sum(x["calls"] for x in c["runs"])
            trunc = sum(x.get("finish_length", 0) for x in c["runs"])
            cost.append({"dataset": ds, "model": model, "method": os.path.basename(p)[:-10],
                         "n": n, "cost_cny": round(tot, 5), "cny_per_inst": round(tot / n, 6) if n else None,
                         "calls_issued": calls, "truncated": trunc})
    proj = projection(cost, kconv)
    res = {"methods": table, "stability": stab, "cost": cost, "k_convergence": kconv, "projection": proj}
    with open(os.path.join(OUT, f"{out_name}.json"), "w") as f:
        json.dump(res, f, indent=1, default=float)

    def md(rows, cols):
        if not rows:
            return ""
        s = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
        for r in rows:
            s += "| " + " | ".join(f"{r.get(c):.3f}" if isinstance(r.get(c), float) else str(r.get(c)) for c in cols) + " |\n"
        return s
    text = (f"# Phase-2 {out_name} analysis\n\n## Methods\n"
            + md(table, ["dataset", "model", "method", "n", "top1", "rec@g", "random_top1", "all_zero",
                         "unique_max", "reaches_tau", "calls/inst", "full_ctx_change"])
            + "\n## Stability (repeat 1 vs 0)\n"
            + md(stab, ["dataset", "model", "method", "n", "identical_phi", "per_source_agree", "n_same_a0",
                        "per_source_agree_same_a0", "top_group_jaccard",
                        "spearman_tie_preserving", "n_rho_defined"])
            + "\n## RM K-sensitivity (banzhaf, exact). k = prefix vs K_max (overlapping); "
            "halves = disjoint first vs second K/2 masks. 'argmax_agree' = tie-aware top-group Jaccard\n"
            + md(kconv, ["dataset", "model", "k", "spearman_vs_Kmax", "argmax_agree", "unique_masks_min",
                         "unique_masks_mean"])
            + "\n## Projected cost of the main run (per-call cost from the pilot x formula calls x evaluable set)\n"
            + md(proj, ["dataset", "model", "method", "cny_per_call", "calls_per_inst", "cny_per_inst", "n_eval", "cny_total"])
            + "\n## Cost\n" + md(cost, ["dataset", "model", "method", "n", "cost_cny", "cny_per_inst",
                                        "calls_issued", "truncated"]))
    with open(os.path.join(OUT, f"{out_name}.md"), "w") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
