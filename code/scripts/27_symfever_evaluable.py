#!/usr/bin/env python3
"""Evaluable sets for the Symmetric-FEVER extension (zero model calls).

The main-experiment leakage rule (no-context answer must be wrong) does not suit
a binary verdict: a no-context guess is right half of the time. Instead, from the
screening rows (full-context and no-context answers, T=0.01):

  full_correct  : the full-context answer equals the gold verdict (yes/no).
  evidence_dep  : full_correct AND the claim twin -- same claim, the family's other
                  evidence sentence, opposite label -- is also full_correct.
                  Both twins right means the verdict follows the evidence, not the
                  claim alone. PRIMARY evaluable set.

Methods are run on full_correct (a superset); analyses report evidence_dep as
primary, full_correct as secondary, and no-context outcomes as a stratifier.

  python scripts/27_symfever_evaluable.py --model gpt-6-luna [--pool symfever.all]
writes results/closed/screen/symfever/<model>/<pool>.evaluable.json
"""
from __future__ import annotations

import argparse
import collections
import gzip
import json
import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
from src.utils.parsing import normalize_answer  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--pool", default="symfever.all")
    ap.add_argument("--instances", default=os.path.join(ROOT, "data", "constructed", "symfever", "symfever.all.jsonl.gz"))
    args = ap.parse_args()
    meta = {}
    with gzip.open(args.instances, "rt", encoding="utf-8") as f:
        for l in f:
            d = json.loads(l)
            meta[d["qid"]] = d["meta"]
    d = os.path.join(ROOT, "results", "closed", "screen", "symfever", args.model)
    rows = {}
    for l in open(os.path.join(d, f"{args.pool}.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        rows[r["qid"]] = r
    ok = {q: normalize_answer(r.get("full_answer") or "") == normalize_answer(r["gold_answer"]) for q, r in rows.items()}
    twin = {}
    by_fc = collections.defaultdict(list)
    for q, m in meta.items():
        by_fc[(m["family"], m["orig_claim"])].append(q)
    for qs in by_fc.values():
        if len(qs) == 2:
            twin[qs[0]], twin[qs[1]] = qs[1], qs[0]
    full = sorted(q for q in rows if ok[q])
    dep = sorted(q for q in full if twin.get(q) in ok and ok[twin[q]])
    missing = sorted(set(meta) - set(rows))
    out = {"model": args.model, "pool": args.pool, "n_screened": len(rows), "n_missing": len(missing),
           "complete": not missing, "full_correct": full, "evidence_dep": dep,
           "counts": {"full_correct": len(full), "evidence_dep": len(dep)}}
    with open(os.path.join(d, f"{args.pool}.evaluable.json"), "w") as f:
        json.dump(out, f)
    with open(os.path.join(d, f"{args.pool}.full_correct.json"), "w") as f:
        json.dump(full, f)
    with open(os.path.join(d, f"{args.pool}.evidence_dep.json"), "w") as f:
        json.dump(dep, f)
    print(json.dumps({k: v for k, v in out.items() if k not in ("full_correct", "evidence_dep")}))


if __name__ == "__main__":
    main()
