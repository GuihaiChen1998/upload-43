#!/usr/bin/env python3
"""Paper tables for the closed-model experiments (zero model calls).

Per (dataset, model) cell of one tag (default `main`, test split = pilot qids removed):

  * invalid_reference: the perturbation reference draw a0 failed (baseline_answer is
    None in a P*/RM/LOI file). Counted per method as a PIPELINE FAILURE, separate from
    a valid all-zero attribution (issue #1, round 25).
  * common valid set: qids present for every compared method and valid for all of
    them. PRIMARY comparison: tie-aware top-1 on this set, paired bootstrap CI of
    (method - V1). End-to-end top-1 (failures keep their all-zero tie = chance floor,
    same rule for all methods) is reported as secondary.
  * coverage / fidelity of P1: coverage = share with any non-zero score;
    fidelity = top-1 on the covered rows, next to V1 on the same rows.
  * routing frontier: start with a cheap estimator (P1 or LOI) and escalate to RM@k
    when its scores are all zero (or have no unique max).
  * cost: nominal distinct prompts per instance incl. the shared reference a0
    (V1 = 1, P1 = LOI = M+1, RM@k = 1 + distinct non-full masks among the first k);
    `calls` = issued cache misses, kept for the budget audit only.

  python scripts/28_paper_tables.py [--tag main] [--split test]
  python scripts/28_paper_tables.py --tag main --split all --dataset symfever \
      --keep evidence_dep            # FEVER: primary evaluable set from 27_symfever_evaluable.py
"""
from __future__ import annotations

import argparse
import glob
import importlib.util
import json
import os
import sys
from collections import defaultdict

import numpy as np

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
_spec = importlib.util.spec_from_file_location("a18", os.path.join(ROOT, "scripts", "18_analyze_closed.py"))
a18 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(a18)
from src.pipelines.subset import mexgen_loo_from_p1  # noqa: E402

RAW, OUT = a18.RAW, a18.OUT
REF_METHODS = ("P", "RM", "LOI")  # files whose rows carry a perturbation reference a0
COMPARE = ["V1", "P1", "MEXGEN_LOO", "LOI", "RM@8", "RM@10", "RM@16", "RM@20", "RM@32", "RM64"]
B = 2000


def needs_ref(name):
    return name.startswith(REF_METHODS) or name == "MEXGEN_LOO"


def invalid(r):
    m = r.get("meta") or {}
    return bool(m.get("invalid_reference")) or (r.get("baseline_answer") is None and m.get("baseline_ok") is not True)


def nominal_calls(m, r, rm_base=None):
    """Estimator cost in distinct prompts per instance, INCLUDING the shared full-context
    reference a0 and EXCLUDING P1's noise-diagnostic full-context repeats. `calls`
    (issued cache misses) depends on which method happened to draw a0 first."""
    M = len(r["phi"])
    if m.startswith("V"):
        return float(r.get("n_calls", 1))
    if m in ("P1", "MEXGEN_LOO", "LOI"):
        return float(M + 1)
    if m.startswith("RM"):
        k = int(m[3:]) if m.startswith("RM@") else int(m[2:])
        masks = (rm_base or r)["meta"].get("masks")
        if masks is None:
            return float(k + 1)
        distinct = {tuple(x) for x in masks[:k] if not all(x)}
        return float(1 + len(distinct))
    return float(r.get("n_calls", 0))


def top1_vec(rows):
    return np.array([a18.tie_top1(r["phi"], r["gold"]) for r in rows], float)


def paired_ci(x, y, seed=0, clusters=None):
    """Paired bootstrap of mean(x - y). With `clusters` (one id per row), resample whole
    clusters (Symmetric FEVER claim families, Qasper papers) and keep their rows together."""
    d = np.asarray(x) - np.asarray(y)
    if len(d) == 0:
        return (np.nan, np.nan, np.nan)
    rng = np.random.default_rng(seed)
    if clusters is None:
        bs = d[rng.integers(0, len(d), size=(B, len(d)))].mean(1)
    else:
        ids = sorted(set(clusters))
        idx = {c: np.flatnonzero(np.asarray(clusters) == c) for c in ids}
        sums = np.array([d[idx[c]].sum() for c in ids]); cnts = np.array([len(idx[c]) for c in ids])
        pick = rng.integers(0, len(ids), size=(B, len(ids)))
        bs = sums[pick].sum(1) / cnts[pick].sum(1)
    return (float(d.mean()), float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975)))


_CLUSTER = {}


def cluster_of(ds):
    """qid -> cluster id for datasets whose instances are not independent: Symmetric FEVER rows
    of one claim family share distractors and slots; Qasper questions may share a paper."""
    if ds in _CLUSTER:
        return _CLUSTER[ds]
    import gzip
    f = {"symfever": ("symfever/symfever.all.jsonl.gz", "family"), "qasper": ("qasper/qasper.all.jsonl.gz", "paper_id")}.get(ds)
    m = None
    if f:
        m = {}
        with gzip.open(os.path.join(ROOT, "data", "constructed", f[0]), "rt", encoding="utf-8") as fh:
            for l in fh:
                r = json.loads(l)
                m[r["qid"]] = r["meta"][f[1]]
    _CLUSTER[ds] = m
    return m


def load_cell(d, split, keep=None):
    ds, model = d.split(os.sep)[-3], d.split(os.sep)[-2]
    R = {os.path.basename(p)[:-6]: a18.load(p) for p in glob.glob(os.path.join(d, "*.jsonl"))}
    if split != "all":
        qp = os.path.join(RAW, ds, model, "pilot", "qids.json")
        dev = set(json.load(open(qp))) if os.path.exists(qp) else set()
        f = (lambda q: q in dev) if split == "dev" else (lambda q: q not in dev)
        R = {k: [r for r in v if f(r["qid"])] for k, v in R.items()}
    if keep is not None:
        R = {k: [r for r in v if r["qid"] in keep] for k, v in R.items()}
    if R.get("P1"):
        # derived from P1's stored answers: inherits P1's reference validity and calls (0 new calls)
        R["MEXGEN_LOO"] = [{**(mexgen_loo_from_p1(r, r["gold"]) if r["meta"].get("ablated_answers") is not None
                               else {**r, "phi": [0.0] * len(r["phi"])}),
                            "baseline_answer": r.get("baseline_answer"), "n_calls": r.get("n_calls", 0),
                            "meta": {**r["meta"], "derived_from": "P1"}} for r in R["P1"]]
    for k in list(R):
        if k.startswith("RM") and "." not in k and ":" not in k:
            R.update({kk: v for kk, v in a18.rm_variants(R[k]).items() if kk.startswith("RM@")})
    # equal-budget prefixes: RM@M has nominal cost M+1 = P1's (k = 10 on M = 10, k = 20 on M = 20)
    from src.pipelines.subset import SCALARIZERS, banzhaf
    for k in list(R):
        if k.startswith("RM") and "@" not in k and ":" not in k and "." not in k:
            for kk in (10, 20):
                rows = []
                for r in R[k]:
                    a0 = r.get("baseline_answer")
                    if a0 is None or len(r["phi"]) > 2 * kk or len(r["phi"]) < kk:
                        continue
                    masks = np.array(r["meta"]["masks"], dtype=bool)[:kk]
                    y = np.array([SCALARIZERS["exact"](a, a0) for a in r["meta"]["mask_answers"][:kk]], float)
                    rows.append({**r, "phi": banzhaf(masks, y).tolist(), "n_calls": kk + 1})
                if rows:
                    R[f"RM@{kk}"] = rows
    # invalid rows of a method keep their stored all-zero phi (prefix variants drop them: restore)
    for k in list(R):
        if k.startswith("RM@"):
            base = next((b for b in R if b.startswith("RM") and "@" not in b and ":" not in b and "." not in b), None)
            if base:
                have = {r["qid"] for r in R[k]}
                R[k] += [{**r, "n_calls": r.get("n_calls", 1)} for r in R[base] if r["qid"] not in have]
    return ds, model, R


def cell_tables(ds, model, R):
    by = {k: {r["qid"]: r for r in v} for k, v in R.items()}
    rmb = next((by[b] for b in by if b.startswith("RM") and "@" not in b and ":" not in b and "." not in b), {})
    cost = lambda m, q: nominal_calls(m, by[m][q], rmb.get(q))  # noqa: E731
    methods = [m for m in COMPARE if m in by] + sorted(m for m in by if m not in COMPARE and "." not in m and ":" not in m)
    present = [m for m in COMPARE if m in by]
    bad = set()
    for m in present:
        if needs_ref(m):
            bad |= {q for q, r in by[m].items() if invalid(r)}
    common = set.intersection(*(set(by[m]) for m in present)) - bad if present else set()
    common = sorted(common)
    out = []
    v1 = top1_vec([by["V1"][q] for q in common]) if "V1" in by and common else None
    for m in methods:
        rows = list(by[m].values())
        n_inv = sum(invalid(r) for r in rows) if needs_ref(m) else 0
        valid = [r for r in rows if not (needs_ref(m) and invalid(r))]
        st = {"dataset": ds, "model": model, "method": m, "n": len(rows), "n_invalid_ref": n_inv,
              "top1_e2e": float(top1_vec(rows).mean()) if rows else np.nan,
              "all_zero_valid": float(np.mean([not np.asarray(r["phi"]).any() for r in valid])) if valid else np.nan,
              "calls": float(np.mean([r.get("n_calls", 0) for r in rows])) if rows else np.nan,
              "cost": float(np.mean([cost(m, r["qid"]) for r in rows])) if rows else np.nan}
        if m in present and common:
            x = top1_vec([by[m][q] for q in common])
            st.update({"n_common": len(common), "top1_common": float(x.mean()),
                       "random_top1": float(np.mean([len(by[m][q]["gold"]) / len(by[m][q]["phi"]) for q in common]))})
            if v1 is not None and m != "V1":
                cm = cluster_of(ds)
                st["diff_vs_V1"], st["ci_lo"], st["ci_hi"] = paired_ci(x, v1, clusters=[cm[q] for q in common] if cm else None)
                if cm:
                    st["ci_unit"] = "cluster"
        out.append(st)
    # coverage / fidelity for single-source ablation estimators
    covfid = []
    for m in ("P1", "LOI", "MEXGEN_LOO"):
        if m in by and "V1" in by and common:
            cov = [q for q in common if np.asarray(by[m][q]["phi"]).any()]
            uq = [q for q in cov if np.sum(np.isclose(by[m][q]["phi"], max(by[m][q]["phi"]))) == 1]
            tie = [q for q in cov if q not in set(uq)]
            spont = [by[m][q]["meta"].get("full_context_change_rate") for q in common]
            spont = [x for x in spont if x is not None]
            unc = [q for q in common if q not in set(cov)]
            gap_tot = float(np.mean(top1_vec([by["V1"][q] for q in common]) - top1_vec([by[m][q] for q in common])))
            gap_unc = (float(np.sum(top1_vec([by["V1"][q] for q in unc]) - top1_vec([by[m][q] for q in unc]))) / len(common)) if unc else 0.0
            covfid.append({"dataset": ds, "model": model, "method": m, "n_common": len(common),
                           "gap_vs_V1": gap_tot, "gap_from_all_zero": gap_unc,
                           "share_gap_all_zero": gap_unc / gap_tot if gap_tot else np.nan,
                           "unique_max_share": len(uq) / len(cov) if cov else np.nan,
                           "top1_unique": float(top1_vec([by[m][q] for q in uq]).mean()) if uq else np.nan,
                           "top1_tied": float(top1_vec([by[m][q] for q in tie]).mean()) if tie else np.nan,
                           "spontaneous_change": float(np.mean(spont)) if spont else np.nan,
                           "coverage": len(cov) / len(common),
                           "fidelity": float(top1_vec([by[m][q] for q in cov]).mean()) if cov else np.nan,
                           "V1_on_covered": float(top1_vec([by["V1"][q] for q in cov]).mean()) if cov else np.nan,
                           "V1_on_uncovered": float(top1_vec([by["V1"][q] for q in common if q not in set(cov)]).mean())
                           if len(cov) < len(common) else np.nan})
    # routing: cheap -> RM@k when the cheap scores are all zero / have no unique max
    routes = []
    for cheap in ("P1", "LOI"):
        for rm in ("RM@16", "RM@32", "RM64"):
            if cheap in by and rm in by and common:
                for rule in ("all_zero", "no_unique_max"):
                    acc, calls, esc = [], [], 0
                    ncost = []
                    for q in common:
                        c, e = by[cheap][q], by[rm][q]
                        p = np.asarray(c["phi"], float)
                        go = (not p.any()) if rule == "all_zero" else (np.sum(p == p.max()) != 1)
                        # RM's reference draw is P1's (cache hit): escalation adds only the mask calls
                        extra = e.get("n_calls", 0) - 1  # P1, LOI and RM share the reference draw
                        acc.append(a18.tie_top1((e if go else c)["phi"], c["gold"]))
                        calls.append(c.get("n_calls", 0) + (extra if go else 0))
                        ncost.append(cost(cheap, q) + ((cost(rm, q) - 1) if go else 0))
                        esc += go
                    routes.append({"dataset": ds, "model": model, "route": f"{cheap}->{rm}", "rule": rule,
                                   "top1": float(np.mean(acc)), "calls": float(np.mean(calls)), "cost": float(np.mean(ncost)),
                                   "escalated": esc / len(common), "n_common": len(common)})
    return out, covfid, routes


def md(rows, cols, fmt=3):
    h = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    for r in rows:
        h += "| " + " | ".join((f"{r[c]:.{fmt}f}" if isinstance(r.get(c), float) else str(r.get(c, ""))) for c in cols) + " |\n"
    return h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="main")
    ap.add_argument("--split", default="test", choices=["all", "test", "dev"])
    ap.add_argument("--dataset", default=None, help="restrict to one dataset dir")
    ap.add_argument("--keep", default=None, choices=[None, "evidence_dep", "full_correct"],
                    help="symfever: restrict to an evaluable set from 27_symfever_evaluable.py")
    args = ap.parse_args()
    T, C, Rt = [], [], []
    for d in sorted(glob.glob(os.path.join(RAW, args.dataset or "*", "*", args.tag))):
        if not args.dataset and d.split(os.sep)[-3] == "symfever":
            continue  # FEVER has its own evaluable rule: run with --dataset symfever --keep ...
        keep = None
        if args.keep:
            m = d.split(os.sep)[-2]
            ev = json.load(open(os.path.join(ROOT, "results", "closed", "screen", "symfever", m,
                                             "symfever.all.evaluable.json")))
            keep = set(ev[args.keep])
        ds, model, R = load_cell(d, args.split, keep)
        if "V1" not in R:
            continue
        t, c, r = cell_tables(ds, model, R)
        T += t; C += c; Rt += r
    name = f"paper.{args.tag}.{args.split}" + (f".{args.dataset}" if args.dataset else "") + (f".{args.keep}" if args.keep else "")
    with open(os.path.join(OUT, name + ".json"), "w") as f:
        json.dump({"methods": T, "coverage_fidelity": C, "routing": Rt}, f, indent=1, default=float)
    with open(os.path.join(OUT, name + ".md"), "w") as f:
        f.write(f"# {name}\n\nPrimary = tie-aware top-1 on the common valid set of each cell (methods V1, P1, "
                f"MEXGEN_LOO, LOI, RM@k); diff/CI = paired bootstrap ({B}) of method − V1. "
                f"top1_e2e keeps invalid-reference rows as all-zero ties (chance floor).\n\n## Methods\n\n")
        f.write(md([t for t in T if t["method"] in COMPARE],
                   ["dataset", "model", "method", "n", "n_invalid_ref", "n_common", "top1_common", "diff_vs_V1",
                    "ci_lo", "ci_hi", "top1_e2e", "all_zero_valid", "calls", "cost", "random_top1"]))
        f.write("\n## Coverage / fidelity (common valid set)\n\n")
        f.write(md(C, ["dataset", "model", "method", "n_common", "coverage", "fidelity", "V1_on_covered", "V1_on_uncovered",
                       "unique_max_share", "top1_unique", "top1_tied", "spontaneous_change", "gap_vs_V1", "share_gap_all_zero"]))
        f.write("\n## Routing: cheap estimator, escalate to RM when uninformative\n\n")
        f.write(md(Rt, ["dataset", "model", "route", "rule", "top1", "calls", "cost", "escalated", "n_common"]))
    print("wrote", os.path.join(OUT, name + ".{json,md}"))


if __name__ == "__main__":
    main()
