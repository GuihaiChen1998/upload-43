#!/usr/bin/env python3
"""Intersect evaluable sets across models -- shared evaluation set selection.

Gold supporting facts are a valid attribution target only where the model
answers correctly, so each model has its own evaluable set (01c). That creates a
tension: per-model sets keep the target valid, but a shared set is what makes
cross-model comparison clean. Intersecting resolves it -- every model is scored
on instances it answers correctly, and all models are scored on the same
instances.

The price is size, bounded by the weakest model. Intersecting within a family
(rather than globally) is usually the better trade: Sec. 6.3 asks whether the
scale trend holds within each family, which needs clean comparison inside a
family, not across families -- and a global intersection is squeezed by the
weakest model of every family at once.

  # global and per-family intersections, with hop composition
  python scripts/01d_intersect_evaluable.py \\
      --reports results/raw/eval_*_musique.json --dataset musique

  # write the chosen set for 02/03 to consume via --only-qids
  python scripts/01d_intersect_evaluable.py \\
      --reports results/raw/eval_*_musique.json --dataset musique \\
      --family qwen3 --out results/raw/shared_qwen3_musique.json
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.data.loaders import load_dataset_by_name

# Model-name substrings -> family. Matched against the report's model field,
# which is typically a path, so substring matching is the robust choice.
FAMILY_PATTERNS = {
    "qwen": "qwen3",
    "gemma": "gemma3",
    "claude": "closed",
    "gpt": "closed",
}


def family_of(model: str) -> str:
    low = str(model).lower()
    for pat, fam in FAMILY_PATTERNS.items():
        if pat in low:
            return fam
    return "other"


def short_name(model: str) -> str:
    return os.path.basename(str(model).rstrip("/"))


def load_reports(patterns: list[str]) -> list[dict]:
    paths = []
    for p in patterns:
        paths.extend(sorted(glob.glob(p)))
    reports = []
    for path in paths:
        with open(path, encoding="utf-8") as f:
            r = json.load(f)
        r["_path"] = path
        ev = r.get("evaluable")
        if ev is None:  # older format
            b = r.get("buckets", {})
            ev = b.get("context_dep", []) + b.get("abstained_correct", [])
        r["_evaluable"] = set(ev)
        r["_family"] = family_of(r.get("model", path))
        r["_short"] = short_name(r.get("model", path))
        reports.append(r)
    return reports


def hop_breakdown(qids: set[str], hop_by_qid: dict[str, int]) -> dict:
    c = Counter(hop_by_qid.get(q) for q in qids if hop_by_qid.get(q) is not None)
    return dict(sorted(c.items()))


def describe(label: str, qids: set[str], hop_by_qid: dict, indent: str = "  ") -> None:
    hops = hop_breakdown(qids, hop_by_qid)
    hop_str = f" hops={hops}" if hops else ""
    print(f"{indent}{label:28s} {len(qids):5d}{hop_str}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reports", nargs="+", required=True,
                    help="01c report paths or globs")
    ap.add_argument("--dataset", required=True, choices=["hotpotqa", "musique"])
    ap.add_argument("--family", default=None,
                    help="write the intersection for this family only "
                         "(e.g. qwen3); omit to write the global intersection")
    ap.add_argument("--models", nargs="+", default=None,
                    help="restrict to these models (substring match)")
    ap.add_argument("--out", default=None,
                    help="write the chosen qid set as a 01c-compatible report")
    args = ap.parse_args()

    reports = load_reports(args.reports)
    if args.models:
        reports = [r for r in reports
                   if any(m.lower() in r["_short"].lower() for m in args.models)]
    if not reports:
        print("no reports matched")
        return

    # hop lookup, for composition reporting
    insts = load_dataset_by_name(args.dataset, limit=None)
    hop_by_qid = {i.qid: i.n_hop for i in insts}

    print(f"{args.dataset}: {len(reports)} report(s)\n")
    print("per-model evaluable sets:")
    for r in sorted(reports, key=lambda x: (x["_family"], x["_short"])):
        describe(f"{r['_short']} [{r['_family']}]", r["_evaluable"], hop_by_qid)

    # global intersection
    glob_int = set.intersection(*[r["_evaluable"] for r in reports])
    print("\nintersections:")
    describe("GLOBAL (all models)", glob_int, hop_by_qid)

    # per-family intersections
    fams: dict[str, list[dict]] = {}
    for r in reports:
        fams.setdefault(r["_family"], []).append(r)
    fam_ints = {}
    for fam, rs in sorted(fams.items()):
        inter = set.intersection(*[r["_evaluable"] for r in rs])
        fam_ints[fam] = inter
        describe(f"{fam} ({len(rs)} models)", inter, hop_by_qid)

    # What is the binding constraint?
    print("\n--- notes")
    smallest = min(reports, key=lambda r: len(r["_evaluable"]))
    print(f"  the global intersection is bounded by {smallest['_short']} "
          f"({len(smallest['_evaluable'])} evaluable)")
    if glob_int:
        retention = len(glob_int) / len(smallest["_evaluable"])
        print(f"  it retains {retention:.0%} of that model's set; the rest are "
              f"instances the other models get wrong")
    for fam, inter in fam_ints.items():
        hops = hop_breakdown(inter, hop_by_qid)
        thin = [h for h, c in hops.items() if c < 20]
        if thin:
            print(f"  ! {fam}: hop level(s) {thin} have <20 instances; report "
                  f"exact n per stratum, or pool strata for that family")

    if args.out:
        chosen = fam_ints.get(args.family) if args.family else glob_int
        if chosen is None:
            print(f"\nfamily {args.family!r} not found; nothing written")
            return
        payload = {
            "model": f"INTERSECTION[{args.family or 'global'}]",
            "dataset": args.dataset,
            "n": len(chosen),
            "evaluable": sorted(chosen),
            "source_reports": [r["_path"] for r in reports
                               if not args.family or r["_family"] == args.family],
            "hop_breakdown": hop_breakdown(chosen, hop_by_qid),
        }
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"\nwrote {args.out} ({len(chosen)} qids)")
        print("  pass it to 02/03 via --only-qids")
        print("  note: the model field is a marker, so the per-model mismatch "
              "warning will fire -- that is expected for a shared set")


if __name__ == "__main__":
    main()
