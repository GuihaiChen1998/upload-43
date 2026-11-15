#!/usr/bin/env python3
"""Candidate pools for the closed-model evaluable screening (phase 1).

  union         union of the evaluable sets of the 5 open models (Gemma-3-1B excluded)
  intersection  their intersection (anchor set for cross-model comparison)
  audit         a random sample OUTSIDE the union, used to estimate how many
                closed-model-evaluable instances the union misses. MuSiQue is
                stratified by hop with proportional allocation (self-weighting);
                per-stratum population sizes are stored so estimates can be
                re-weighted to the outside-union population.

  python scripts/13_build_pools.py            # writes results/closed/pools/<dataset>.json
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import random
import sys
from collections import Counter

ROOT = os.path.join(os.path.dirname(__file__), "..")
OPEN_MODELS = ["qwen3-1.7b", "qwen3-4b", "qwen3-8b", "gemma-3-4b-it", "gemma-3-12b-it"]


def hop_of(qid: str, ds: str):
    return int(qid[0]) if ds == "musique" and qid[0].isdigit() else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit-n", type=int, default=50)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out-dir", default=os.path.join(ROOT, "results", "closed", "pools"))
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    for ds in ["hotpotqa", "musique"]:
        evs = {}
        for m in OPEN_MODELS:
            with open(os.path.join(ROOT, "results", "raw", f"eval_{m}_{ds}.json")) as f:
                evs[m] = set(json.load(f)["evaluable"])
        union = sorted(set().union(*evs.values()))
        inter = sorted(set.intersection(*evs.values()))
        with open(os.path.join(ROOT, "data", "processed", f"{ds}_validation.jsonl")) as f:
            all_q = [json.loads(l)["qid"] for l in f]
        outside = sorted(set(all_q) - set(union))

        rng = random.Random(args.seed)
        strata = Counter(hop_of(q, ds) for q in outside)
        audit, alloc = [], {}
        if ds == "musique":
            # proportional allocation with largest-remainder rounding
            raw = {h: args.audit_n * c / len(outside) for h, c in strata.items()}
            alloc = {h: int(v) for h, v in raw.items()}
            for h in sorted(raw, key=lambda h: raw[h] - alloc[h], reverse=True)[: args.audit_n - sum(alloc.values())]:
                alloc[h] += 1
            for h, k in sorted(alloc.items()):
                pool_h = [q for q in outside if hop_of(q, ds) == h]
                audit += rng.sample(pool_h, k)
        else:
            audit = rng.sample(outside, args.audit_n)
            alloc = {None: args.audit_n}

        out = {
            "dataset": ds, "open_models": OPEN_MODELS, "seed": args.seed,
            "n_all": len(all_q), "n_union": len(union), "n_intersection": len(inter),
            "n_outside_union": len(outside),
            "outside_union_strata": {str(k): v for k, v in strata.items()},
            "audit_allocation": {str(k): v for k, v in alloc.items()},
            "union": union, "intersection": inter, "audit": sorted(audit),
        }
        path = os.path.join(args.out_dir, f"{ds}.json")
        with open(path, "w") as f:
            json.dump(out, f, indent=1)
        print(f"{ds}: all {len(all_q)} | union {len(union)} | intersection {len(inter)} | "
              f"outside {len(outside)} {dict(strata)} | audit {len(audit)} {alloc} -> {path}")


if __name__ == "__main__":
    main()
