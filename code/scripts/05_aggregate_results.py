#!/usr/bin/env python3
"""Aggregate raw per-instance results into tables -- paper Sec. 6.

Reads results/raw/<dataset>/<model>/<method>.jsonl and emits:
  results/tables/main_results.csv        Table 1  (per model/dataset/method)
  results/tables/scale.csv               Figure 3 data
  results/tables/agreement.csv           Figure 4(a) data
  results/tables/failure_by_hop.csv      Figure 4(b) data (MuSiQue)
  results/tables/selection_bias.csv      Sec. 6.2 directionality

No model access here; pure post-processing, so it is safe to iterate on
formatting without re-running anything expensive.

  python scripts/05_aggregate_results.py
  python scripts/05_aggregate_results.py --raw-root results/raw
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.data.loaders import load_dataset_by_name
from src.eval.metrics import (
    agreement, empty_prediction_rate, mean_query_cost, overlap_with_baseline,
    parse_failure_rate, selection_bias, set_f1, summarize, top1_accuracy,
)


def _rehydrate(d: dict) -> SimpleNamespace:
    """Turn a serialized result row back into something the metrics accept.

    metrics.py reads .ranking / .gold / .pred_set / .top1_correct / .meta etc.
    top1_correct is a property on the dataclass, so recompute it here.
    """
    ns = SimpleNamespace(**d)
    ns.top1_correct = bool(ns.ranking) and ns.ranking[0] in set(ns.gold)
    ns.meta = d.get("meta", {})
    return ns


def load_cell(path: str) -> list:
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(_rehydrate(json.loads(line)))
    return rows


def discover(raw_root: str):
    """Yield (dataset, model, method, path) for every result file present."""
    for path in glob.glob(os.path.join(raw_root, "*", "*", "*.jsonl")):
        parts = path.split(os.sep)
        dataset, model, fname = parts[-3], parts[-2], parts[-1]
        method = fname.replace(".jsonl", "")
        yield dataset, model, method, path


# --- Params for family/size, kept here so the aggregator needs no model configs.
FAMILY = {
    "qwen3-1.7b": ("qwen3", 1.7), "qwen3-4b": ("qwen3", 4.0),
    "qwen3-8b": ("qwen3", 8.0),
    "gemma3-1b": ("gemma3", 1.0), "gemma3-4b": ("gemma3", 4.0),
    "gemma3-12b": ("gemma3", 12.0),
    "claude-haiku-4-5": ("closed", None),
}


def write_csv(path: str, rows: list[dict], fields: list[str]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"wrote {path} ({len(rows)} rows)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-root", default="results/raw")
    ap.add_argument("--out-dir", default="results/tables")
    ap.add_argument("--n-instances", type=int, default=200,
                    help="for the random-baseline column, load this many golds")
    args = ap.parse_args()

    cells = {}  # (dataset, model, method) -> results
    for dataset, model, method, path in discover(args.raw_root):
        cells[(dataset, model, method)] = load_cell(path)

    if not cells:
        print(f"no result files under {args.raw_root}. Run 02/03 first.")
        return

    # Integrity check: within one (dataset, model), all methods should cover the
    # same instance set. A divergent count usually means a cell was resumed
    # against a different --only-qids set and now mixes two populations, which
    # would silently bias its metrics.
    from collections import defaultdict as _dd
    _sizes = _dd(dict)
    for (dataset, model, method), res in cells.items():
        if model != "_baselines":
            _sizes[(dataset, model)][method] = len({r.qid for r in res})
    for (dataset, model), per_method in _sizes.items():
        counts = set(per_method.values())
        if len(counts) > 1:
            from statistics import mode
            common = mode(list(per_method.values()))
            odd = {m: n for m, n in per_method.items() if n != common}
            print(f"  ! {dataset}/{model}: methods disagree on instance count "
                  f"(most have {common}); off: {odd}. A resumed cell may mix two "
                  f"--only-qids sets. Delete and rerun those, or filter to the "
                  f"shared qids before trusting their numbers.")

    datasets = sorted({d for d, _, _ in cells})
    inst_cache = {d: load_dataset_by_name(d, limit=args.n_instances) for d in datasets}
    rand = {
        d: (sum(len(i.gold_indices) / i.M for i in insts) / len(insts)) if insts else 0.0
        for d, insts in inst_cache.items()
    }

    # --- Table 1: main results ---------------------------------------------
    # Reported twice: on the full set, and on the context-dependent subset
    # (leaked instances removed). Leaked instances have no dependence for
    # ablation to detect, so the subset is where the methods are actually
    # tested; the gap between the two views is itself reportable (Sec. 6).
    main_rows = []
    for (dataset, model, method), res in sorted(cells.items()):
        fam, size = FAMILY.get(model, ("?", None))
        clean = [r for r in res if not r.meta.get("leaked", False)]
        has_tags = any("leaked" in r.meta for r in res)
        for subset, rs in (("full", res), ("context_dep", clean)):
            if subset == "context_dep" and (not has_tags or len(rs) == len(res)):
                continue  # nothing tagged; the subset view adds nothing
            if not rs:
                continue
            s = summarize(rs)
            main_rows.append({
                "dataset": dataset, "model": model, "family": fam,
                "params_b": size, "method": method, "subset": subset,
                "n": s["n"],
                "top1_accuracy": round(s["top1_accuracy"], 4),
                "set_f1": round(s["set_f1"], 4),
                "mean_query_cost": round(s["mean_query_cost"], 2),
                "parse_failure_rate": round(s["parse_failure_rate"], 4),
                "empty_prediction_rate": round(s["empty_prediction_rate"], 4),
                "random_baseline_top1": round(rand.get(dataset, 0.0), 4),
            })
    write_csv(os.path.join(args.out_dir, "main_results.csv"), main_rows,
              list(main_rows[0].keys()))

    # --- Scale (Figure 3): best V and best P per model, with parse fail -----
    scale_rows = []
    for dataset in datasets:
        models = sorted({m for (d, m, _) in cells if d == dataset})
        for model in models:
            fam, size = FAMILY.get(model, ("?", None))
            v = [(mid, cells[(dataset, model, mid)]) for (d, m, mid) in cells
                 if d == dataset and m == model and mid.startswith("V")]
            p = [(mid, cells[(dataset, model, mid)]) for (d, m, mid) in cells
                 if d == dataset and m == model and mid.startswith("P")]
            best_v = max((top1_accuracy(r) for _, r in v), default=None)
            best_p = max((top1_accuracy(r) for _, r in p), default=None)
            # Prefer the context-dependent subset when tags are present.
            allres = [x for _, r in (v + p) for x in r
                      if not x.meta.get("leaked", False)]
            if not allres:
                allres = [x for _, r in (v + p) for x in r]
            scale_rows.append({
                "dataset": dataset, "model": model, "family": fam,
                "params_b": size,
                "best_v_top1": round(best_v, 4) if best_v is not None else "",
                "best_p_top1": round(best_p, 4) if best_p is not None else "",
                "parse_failure_rate": round(parse_failure_rate(allres), 4) if allres else "",
            })
    write_csv(os.path.join(args.out_dir, "scale.csv"), scale_rows,
              list(scale_rows[0].keys()))

    # --- Agreement (Figure 4a): best V vs best P per model ------------------
    agr_rows = []
    for dataset in datasets:
        models = sorted({m for (d, m, _) in cells if d == dataset})
        for model in models:
            fam, size = FAMILY.get(model, ("?", None))
            vlist = [(mid, cells[(dataset, model, mid)]) for (d, m, mid) in cells
                     if d == dataset and m == model and mid.startswith("V")]
            plist = [(mid, cells[(dataset, model, mid)]) for (d, m, mid) in cells
                     if d == dataset and m == model and mid.startswith("P")]
            if not vlist or not plist:
                continue
            bv = max(vlist, key=lambda kv: top1_accuracy(kv[1]))[1]
            bp = max(plist, key=lambda kv: top1_accuracy(kv[1]))[1]
            a = agreement(bv, bp)
            a.update({"dataset": dataset, "model": model, "family": fam,
                      "params_b": size})
            agr_rows.append(a)
    if agr_rows:
        keys = ["dataset", "model", "family", "params_b", "n", "agreement_rate",
                "both_correct", "only_v", "only_p", "both_wrong_same",
                "both_wrong_diff", "same_top1"]
        write_csv(os.path.join(args.out_dir, "agreement.csv"), agr_rows, keys)

    # --- Failure by hop (Figure 4b): MuSiQue, best P method ----------------
    if "musique" in datasets:
        hop_rows = []
        models = sorted({m for (d, m, _) in cells if d == "musique"})
        for model in models:
            plist = [(mid, cells[("musique", model, mid)]) for (d, m, mid) in cells
                     if d == "musique" and m == model and mid.startswith("P")]
            if not plist:
                continue
            bp = max(plist, key=lambda kv: top1_accuracy(kv[1]))[1]
            by_hop = {}
            for r in bp:
                h = r.meta.get("n_hop")
                by_hop.setdefault(h, []).append(r)
            insts_by_hop = {}
            for i in inst_cache["musique"]:
                insts_by_hop.setdefault(i.n_hop, []).append(i)
            for h in sorted(k for k in by_hop if k is not None):
                rs = by_hop[h]
                gi = insts_by_hop.get(h, [])
                rb = (sum(len(i.gold_indices) / i.M for i in gi) / len(gi)) if gi else 0.0
                hop_rows.append({
                    "model": model, "n_hop": h, "n": len(rs),
                    "empty_prediction_rate": round(empty_prediction_rate(rs), 4),
                    "top1_accuracy": round(top1_accuracy(rs), 4),
                    "random_baseline_top1": round(rb, 4),
                })
        if hop_rows:
            write_csv(os.path.join(args.out_dir, "failure_by_hop.csv"), hop_rows,
                      list(hop_rows[0].keys()))

    # --- Selection bias (Sec. 6.2 directionality) --------------------------
    bias_rows = []
    for dataset in datasets:
        models = sorted({m for (d, m, _) in cells if d == dataset})
        for model in models:
            vlist = [(mid, cells[(dataset, model, mid)]) for (d, m, mid) in cells
                     if d == dataset and m == model and mid.startswith("V")]
            if not vlist:
                continue
            bv = max(vlist, key=lambda kv: top1_accuracy(kv[1]))[1]
            b = selection_bias(bv, inst_cache[dataset])
            b.update({"dataset": dataset, "model": model})
            bias_rows.append(b)
    if bias_rows:
        keys = ["dataset", "model", "n", "mean_selected_relpos",
                "mean_gold_relpos", "mean_M"]
        write_csv(os.path.join(args.out_dir, "selection_bias.csv"), bias_rows, keys)

    # --- Overlap with shallow baselines (Sec. 6.2 diagnostic) --------------
    # Reported for the best VERBALIZE method and the best PERTURBATION method
    # separately, not just the single best overall: the whole point of Sec. 6.2
    # is to compare the two paradigms, and if verbalize wins outright the old
    # "best overall" logic would only ever show a verbalize row. Both paradigms
    # estimate the same contributive target; low overlap with BM25/embedding for
    # both means neither reduces to shallow retrieval.
    overlap_rows = []
    for dataset in datasets:
        base_cells = {mid: res for (d, m, mid), res in cells.items()
                      if d == dataset and m == "_baselines"}
        if not base_cells:
            continue
        models = sorted({m for (d, m, _) in cells if d == dataset and m != "_baselines"})
        for model in models:
            v_cells = [(mid, cells[(dataset, model, mid)]) for (d, m, mid) in cells
                       if d == dataset and m == model and mid.startswith("V")]
            p_cells = [(mid, cells[(dataset, model, mid)]) for (d, m, mid) in cells
                       if d == dataset and m == model and mid.startswith("P")]
            reps = []
            if v_cells:
                reps.append(("verbalize",
                             max(v_cells, key=lambda kv: top1_accuracy(kv[1]))))
            if p_cells:
                reps.append(("perturbation",
                             max(p_cells, key=lambda kv: top1_accuracy(kv[1]))))
            for paradigm, (best_mid, best_res) in reps:
                for bname, bres in base_cells.items():
                    if bname not in ("bm25", "embedding"):
                        continue
                    ov = overlap_with_baseline(best_res, bres)
                    ov.update({"dataset": dataset, "model": model,
                               "paradigm": paradigm, "method": best_mid,
                               "baseline": bname})
                    overlap_rows.append(ov)
    if overlap_rows:
        keys = ["dataset", "model", "paradigm", "method", "baseline", "n",
                "top1_agreement", "set_f1", "rank_correlation"]
        write_csv(os.path.join(args.out_dir, "baseline_overlap.csv"),
                  [{k: r.get(k) for k in keys} for r in overlap_rows], keys)

    # --- Verbalize vs perturbation overlap (the core Sec. 6.2 comparison) ---
    # How much do the two paradigms' own predictions coincide? This is the
    # direct measurement of the gap, independent of the baselines: both estimate
    # the same contributive target, so where they DISAGREE is where the choice
    # of paradigm (self-report vs intervention) actually matters.
    vp_rows = []
    for dataset in datasets:
        models = sorted({m for (d, m, _) in cells if d == dataset and m != "_baselines"})
        for model in models:
            v_cells = [(mid, cells[(dataset, model, mid)]) for (d, m, mid) in cells
                       if d == dataset and m == model and mid.startswith("V")]
            p_cells = [(mid, cells[(dataset, model, mid)]) for (d, m, mid) in cells
                       if d == dataset and m == model and mid.startswith("P")]
            if not v_cells or not p_cells:
                continue
            v_mid, v_res = max(v_cells, key=lambda kv: top1_accuracy(kv[1]))
            p_mid, p_res = max(p_cells, key=lambda kv: top1_accuracy(kv[1]))
            ov = overlap_with_baseline(v_res, p_res)  # reuse the same machinery
            ov.update({"dataset": dataset, "model": model,
                       "verbalize_method": v_mid, "perturbation_method": p_mid,
                       "v_top1": round(top1_accuracy(v_res), 4),
                       "p_top1": round(top1_accuracy(p_res), 4)})
            vp_rows.append(ov)
    if vp_rows:
        keys = ["dataset", "model", "verbalize_method", "perturbation_method",
                "v_top1", "p_top1", "n", "top1_agreement", "set_f1",
                "rank_correlation"]
        write_csv(os.path.join(args.out_dir, "verbalize_vs_perturbation.csv"),
                  [{k: r.get(k) for k in keys} for r in vp_rows], keys)

    print("\ndone. Feed results/tables/*.csv to 06_make_figures.py.")


if __name__ == "__main__":
    main()
