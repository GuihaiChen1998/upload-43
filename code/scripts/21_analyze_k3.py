#!/usr/bin/env python3
"""Analyse the K3 redundancy-group runs (design v2, K3 metrics).

Inputs
  results/closed/k3/<pool>/<model>/premise.jsonl          repeats 0-2 (construct premise)
  results/closed/raw/<ds>/<model>/<tag>/<METHOD>.r3.jsonl  repeat 3  (method evaluation)
  data/constructed/k3/<pool>.jsonl.gz                      group labels (evaluation only)

Per condition F / C / FF / CF / CC (redundancy 0/1/0/1/2), on the FIXED set of
base qids (attrition reported, not hidden):
  premise   full-context correct (3/3, >=2/3), spontaneous full-answer change,
            parse-failure / empty-answer rate, and for drop_ap / drop_group:
              *_still_correct    correct after the deletion
              *_answer_change    answer differs from the same-repeat full answer
              *_acc_drop         paired full-correct minus deleted-correct
  methods   on premise-evaluable variants (full correct 3/3):
            group_top1 / ap_top1 / gold_top1   tie-aware top-1 hit
            group_floor        |group| / M (uniform-random top-1 hit)
            group_top1_cc      chance-corrected (hit - floor) / (1 - floor)
            group_evid         evidence that the group matters:
                                 P1 / LOI / MEXGEN / V*: some member scores > 0
                                 (these scores are non-negative frequencies /
                                 similarities / verbal ranks);
                                 RM: the group's max score exceeds the 95th
                                 percentile of a permutation null (y permuted
                                 across masks, 500 draws). Non-zero is NOT
                                 evidence for signed estimators: under y
                                 independent of the masks they are ~always non-zero.
            nonzero_any        raw diagnostic (some source score != 0)
            all_zero           raw diagnostic
            pos_mass_copies    share of the group's POSITIVE score mass on the
                               copies (allocation of positive scores, not a
                               usage probability)
Paired contrasts use base qids evaluable in both conditions; the FF/CF/CC curve
uses bases evaluable in all three (one population for the whole curve).
Base-qid cluster-bootstrap 95% CIs.

  python scripts/21_analyze_k3.py --model gpt-6-luna --tag k3pilot
"""
from __future__ import annotations

import argparse
import glob
import gzip
import json
import os
import sys
from collections import defaultdict

import numpy as np

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)

from src.pipelines.subset import SCALARIZERS, banzhaf, mexgen_loo_from_p1, ridge  # noqa: E402

CONDS = ["F", "C", "FF", "CF", "CC"]


def tie_frac(phi, members):
    phi = np.asarray(phi, float)
    T = np.flatnonzero(phi == phi.max())
    return float(np.mean([int(i) in members for i in T]))


def rm_null_evidence(row, key, group, B=500, seed=0):
    """Permutation null for 'the group matters' under an RM estimator."""
    meta = row["meta"]
    a0 = row.get("baseline_answer")
    if a0 is None or not meta.get("masks"):
        return 0.0
    est, val = key.split("_")
    masks = np.asarray(meta["masks"], bool)
    y = np.array([SCALARIZERS[val](a, a0) for a in meta["mask_answers"]], float)
    f = banzhaf if est == "banzhaf" else ridge
    g = sorted(group)
    obs = f(masks, y)[g].max()
    rng = np.random.default_rng(seed)
    null = [f(masks, rng.permutation(y))[g].max() for _ in range(B)]
    return float(obs > np.percentile(null, 95))


def load(p):
    return [json.loads(l) for l in open(p, encoding="utf-8")] if os.path.exists(p) else []


def boot(vals_by_base, n=2000, seed=0):
    keys = sorted(vals_by_base)
    if not keys:
        return (np.nan, np.nan, np.nan)
    rng = np.random.default_rng(seed)
    arr = [np.asarray(vals_by_base[k], float) for k in keys]
    est = float(np.mean(np.concatenate(arr)))
    bs = []
    for _ in range(n):
        pick = rng.integers(0, len(arr), len(arr))
        bs.append(np.mean(np.concatenate([arr[i] for i in pick])))
    return est, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gpt-6-luna")
    ap.add_argument("--tag", default="k3pilot")
    ap.add_argument("--n-base", type=int, default=50)
    ap.add_argument("--version", default="v2", help="K3 construction version suffix ('' for v1)")
    args = ap.parse_args()
    out = {"premise": [], "methods": [], "curve": [], "paired": [], "cost": []}
    for ds in ("hotpotqa", "musique"):
        pool = f"{ds}.{args.model}.n{args.n_base}" + (f".{args.version}" if args.version else "")
        ipath = os.path.join(ROOT, "data", "constructed", "k3", pool + ".jsonl.gz")
        if not os.path.exists(ipath):
            continue
        inst = {}
        with gzip.open(ipath, "rt", encoding="utf-8") as fh:
            for l in fh:
                d = json.loads(l)
                inst[d["qid"]] = d
        prem = {r["qid"]: r for r in load(os.path.join(ROOT, "results", "closed", "k3", pool, args.model, "premise.jsonl"))}
        n_bases = len({d["meta"]["base_qid"] for d in inst.values()})
        # ---- premise
        for c in CONDS:
            rows = [r for r in prem.values() if r["condition"] == c]
            if not rows:
                continue
            out["premise"].append({
                "dataset": ds, "cond": c, "redundancy": rows[0]["redundancy"], "n": len(rows),
                "full_3of3": float(np.mean([all(r["full_correct"]) for r in rows])),
                "full_2of3": float(np.mean([sum(r["full_correct"]) >= 2 for r in rows])),
                "full_spont_change": float(np.mean([len(set(r["full_answer"])) > 1 for r in rows])),
                "n_bases": n_bases, "n_eval_3of3": int(sum(all(r["full_correct"]) for r in rows)),
                "parse_fail": float(np.mean([np.mean([a is None for a in r["full_answer"] + r["drop_ap_answer"]
                                                      + r["drop_group_answer"]]) for r in rows])),
                **{f"{pr}_{k}": v for pr in ("drop_ap", "drop_group") for k, v in {
                    "still_correct": float(np.mean([np.mean(r[f"{pr}_correct"]) for r in rows])),
                    "answer_change": float(np.mean([np.mean([x != y for x, y in zip(r["full_answer"], r[f"{pr}_answer"])])
                                                    for r in rows])),
                    "acc_drop": float(np.mean([np.mean(r["full_correct"]) - np.mean(r[f"{pr}_correct"])
                                               for r in rows])),
                }.items()},
            })
        evaluable = {q for q, r in prem.items() if all(r["full_correct"])}
        # ---- methods
        d = os.path.join(ROOT, "results", "closed", "raw", ds, args.model, args.tag)
        evaluable &= set(inst)
        R = {os.path.basename(p)[:-6]: load(p) for p in glob.glob(os.path.join(d, "*.jsonl"))}
        meth = {}
        for k, rows in R.items():
            base = k.split(".")[0]
            if base.startswith("RM"):
                for key in ("banzhaf_exact", "banzhaf_f1", "linear_exact"):
                    meth[f"{base}:{key}"] = [{**r, "phi": r["meta"]["scores"][key]} for r in rows
                                             if r["meta"].get("scores")]
            else:
                meth[base] = rows
            if base == "P1":
                meth["MEXGEN_LOO"] = [mexgen_loo_from_p1(r, r["gold"]) for r in rows
                                      if r["meta"].get("ablated_answers") is not None]
        per = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))  # m -> cond -> metric -> [(base, v)]
        for m, rows in meth.items():
            for r in rows:
                q = r["qid"]
                if q not in evaluable or q not in inst:
                    continue
                meta = inst[q]["meta"]
                c, b = meta["condition"], meta["base_qid"]
                grp = set(meta["redundancy_group"])
                apx = meta["answer_passage"]
                gold = set(meta["orig_gold_new_idx"]) | grp
                phi = np.asarray(r["phi"], float)
                floor = len(grp) / len(phi)
                hit = tie_frac(phi, grp)
                if m.startswith("RM"):
                    evid = rm_null_evidence(r, m.split(":")[1], grp)
                else:
                    evid = float(any(phi[i] > 0 for i in grp))
                vals = {"group_top1": hit, "group_floor": floor, "group_top1_cc": (hit - floor) / (1 - floor),
                        "ap_top1": tie_frac(phi, {apx}), "gold_top1": tie_frac(phi, gold),
                        "group_evid": evid, "nonzero_any": float(phi.any()), "all_zero": float(not phi.any())}
                if len(grp) > 1:
                    gm = np.clip(phi[sorted(grp)], 0, None)
                    if gm.sum() > 0:
                        vals["pos_mass_copies"] = float(gm[[i != apx for i in sorted(grp)]].sum() / gm.sum())
                if m == "P1" and r["meta"].get("full_context_change_rate") is not None:
                    vals["full_ctx_change_r3"] = float(r["meta"]["full_context_change_rate"])
                for k, v in vals.items():
                    per[m][c][k].append((b, v))
        for m in sorted(per):
            for c in CONDS:
                if c not in per[m]:
                    continue
                row = {"dataset": ds, "method": m, "cond": c, "n": len(per[m][c]["group_top1"])}
                for k, lst in per[m][c].items():
                    row[k] = float(np.mean([v for _, v in lst]))
                out["methods"].append(row)
            # paired redundancy effect in the 2-slot set, same base qid in both conditions
            curve = (set(dict(per[m]["FF"].get("group_top1", []))) & set(dict(per[m]["CF"].get("group_top1", [])))
                     & set(dict(per[m]["CC"].get("group_top1", []))))
            for c in ("FF", "CF", "CC"):
                if curve:
                    row = {"dataset": ds, "method": m, "cond": c, "n": len(curve)}
                    for k, lst in per[m][c].items():
                        v = [x for b, x in lst if b in curve]
                        if v:
                            row[k] = float(np.mean(v))
                    out["curve"].append(row)
            for lo, hi in (("FF", "CF"), ("CF", "CC"), ("FF", "CC"), ("F", "C")):
                for metric in ("group_evid", "all_zero", "group_top1", "group_top1_cc", "ap_top1"):
                    A = dict(per[m][lo].get(metric, []))
                    B = dict(per[m][hi].get(metric, []))
                    common = sorted(set(A) & set(B))
                    if not common:
                        continue
                    est, l95, h95 = boot({b: [B[b] - A[b]] for b in common})
                    out["paired"].append({"dataset": ds, "method": m, "contrast": f"{hi}-{lo}", "metric": metric,
                                          "n_base": len(common), "diff": est, "ci_lo": l95, "ci_hi": h95})
        # ---- cost
        costs = glob.glob(os.path.join(d, "*.cost.json")) + glob.glob(
            os.path.join(ROOT, "results", "closed", "k3", pool, args.model, "*.cost.json"))
        for p in costs:
            runs = json.load(open(p))["runs"]
            out["cost"].append({"dataset": ds, "file": os.path.basename(p),
                                "calls": sum(x["calls"] for x in runs),
                                "cost_cny": round(sum(x["est_cost_cny"] for x in runs), 4)})
    os.makedirs(os.path.join(ROOT, "results", "closed", "analysis"), exist_ok=True)
    base = os.path.join(ROOT, "results", "closed", "analysis", f"{args.tag}.{args.model}")
    json.dump(out, open(base + ".json", "w"), indent=1, default=float)

    def md(rows, cols):
        if not rows:
            return "(none)\n"
        s = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
        for r in rows:
            s += "| " + " | ".join(f"{r.get(c):.3f}" if isinstance(r.get(c), float) else str(r.get(c, "")) for c in cols) + " |\n"
        return s
    text = (f"# K3 {args.tag} · {args.model}\n\n## Premise (repeats 0-2)\n"
            + md(out["premise"], ["dataset", "cond", "redundancy", "n_bases", "n_eval_3of3", "full_3of3", "full_2of3",
                                  "full_spont_change", "parse_fail", "drop_ap_still_correct", "drop_ap_answer_change",
                                  "drop_ap_acc_drop", "drop_group_still_correct", "drop_group_answer_change",
                                  "drop_group_acc_drop"])
            + "\n## Methods (repeat 3, premise-evaluable variants of each condition)\n"
            + md(out["methods"], ["dataset", "method", "cond", "n", "group_top1", "group_floor", "group_top1_cc",
                                  "ap_top1", "gold_top1", "group_evid", "nonzero_any", "all_zero", "pos_mass_copies",
                                  "full_ctx_change_r3"])
            + "\n## FF / CF / CC curve on one population (bases evaluable in all three)\n"
            + md(out["curve"], ["dataset", "method", "cond", "n", "group_top1", "group_floor", "group_top1_cc",
                                "group_evid", "all_zero", "pos_mass_copies"])
            + "\n## Paired redundancy effects (base-qid bootstrap 95% CI)\n"
            + md(out["paired"], ["dataset", "method", "contrast", "metric", "n_base", "diff", "ci_lo", "ci_hi"])
            + "\n## Cost\n" + md(out["cost"], ["dataset", "file", "calls", "cost_cny"]))
    open(base + ".md", "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
