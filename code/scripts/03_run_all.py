#!/usr/bin/env python3
"""Orchestrate the full method x model x dataset grid.

Wraps 02_run_method.py so a single command runs the whole matrix, with an
upfront cost estimate and a --dry-run that prints the plan and query budget
without touching a model. Given the O(M*N) cost of the interventional methods,
ALWAYS dry-run first.

  python scripts/03_run_all.py --dry-run
  python scripts/03_run_all.py --models qwen3-8b --datasets hotpotqa \
      --methods V1 V2 P1 P2 --n-instances 200
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.data.loaders import load_dataset_by_name
from src.pipelines.registry import METHODS, get_method
from src.utils.config import load_base

ALL_MODELS = ["qwen3-1.7b", "qwen3-4b", "qwen3-8b",
              "gemma3-1b", "gemma3-4b", "gemma3-12b"]
ALL_DATASETS = ["hotpotqa", "musique"]
ALL_METHODS = list(METHODS.keys())


def estimate_queries(methods, datasets, n_instances, base) -> dict:
    """Per (dataset, method) query totals, using real M from a sample."""
    n_v = base["sampling"]["n_samples_verbalize"]
    n_p = base["sampling"]["n_samples_perturbation"]
    est = {}
    for ds in datasets:
        insts = load_dataset_by_name(ds, limit=n_instances)
        for mid in methods:
            m = get_method(mid)
            n = n_v if m.is_verbalize else n_p
            est[(ds, mid)] = sum(m.query_cost(i.M, n) for i in insts)
    return est


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=ALL_MODELS)
    ap.add_argument("--datasets", nargs="+", default=ALL_DATASETS)
    ap.add_argument("--methods", nargs="+", default=ALL_METHODS)
    ap.add_argument("--n-instances", type=int, default=200)
    ap.add_argument("--only-qids-pattern", default=None,
                    help="path template for per-model 01c reports, e.g. "
                         "'results/raw/eval_{model}_{dataset}.json'. Each cell "
                         "gets its own evaluable set, since leakage and "
                         "correctness are model-specific.")
    ap.add_argument("--sample-n", type=int, default=None,
                    help="cap instances per cell after filtering")
    ap.add_argument("--outer-workers", type=int, default=1,
                    help="instances in parallel per cell")
    ap.add_argument("--inner-workers", type=int, default=1,
                    help="parallel ablations per instance (perturbation)")
    ap.add_argument("--stratify-by", default="hop", choices=["hop", "none"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--continue-on-error", action="store_true",
                    help="keep going if one cell fails (e.g. a model is down)")
    args = ap.parse_args()

    base = load_base()

    print(f"grid: {len(args.models)} models x {len(args.datasets)} datasets "
          f"x {len(args.methods)} methods = "
          f"{len(args.models) * len(args.datasets) * len(args.methods)} cells\n")

    est = estimate_queries(args.methods, args.datasets,
                           args.sample_n or args.n_instances, base)
    if args.sample_n:
        print(f"(estimate uses --sample-n={args.sample_n}; actual counts depend "
              f"on how many instances survive filtering)\n")
    per_model_total = sum(est.values())
    grand = per_model_total * len(args.models)

    print("estimated queries per model:")
    for ds in args.datasets:
        sub = sum(v for (d, _), v in est.items() if d == ds)
        print(f"  {ds}: {sub:,}")
    print(f"  per-model subtotal: {per_model_total:,}")
    print(f"  GRAND TOTAL (all models): {grand:,}")
    print("  (cache hits reduce this; interventional methods dominate)\n")

    if args.dry_run:
        print("dry run -- no models contacted. Plan:")
        for model in args.models:
            for ds in args.datasets:
                for mid in args.methods:
                    print(f"  {model:14s} {ds:10s} {mid}")
        return

    plan = [(model, ds, mid)
            for model in args.models
            for ds in args.datasets
            for mid in args.methods]

    failures = []
    for model, ds, mid in plan:
        cmd = [
            sys.executable, os.path.join(os.path.dirname(__file__), "02_run_method.py"),
            "--method", mid, "--model", model,
            "--dataset", ds, "--n-instances", str(args.n_instances),
        ]
        if args.no_cache:
            cmd.append("--no-cache")
        if args.only_qids_pattern:
            cmd += ["--only-qids",
                    args.only_qids_pattern.format(model=model, dataset=ds)]
        if args.sample_n:
            cmd += ["--sample-n", str(args.sample_n),
                    "--stratify-by", args.stratify_by]
        if args.outer_workers > 1:
            cmd += ["--outer-workers", str(args.outer_workers)]
        if args.inner_workers > 1:
            cmd += ["--inner-workers", str(args.inner_workers)]
        print(f"\n=== {model} / {ds} / {mid} ===")
        rc = subprocess.call(cmd)
        if rc != 0:
            failures.append((model, ds, mid))
            if not args.continue_on_error:
                print(f"aborting: cell failed with code {rc}")
                break

    if failures:
        print(f"\n{len(failures)} cells failed:")
        for f in failures:
            print("  ", f)


if __name__ == "__main__":
    main()
