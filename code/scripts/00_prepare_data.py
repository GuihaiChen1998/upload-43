#!/usr/bin/env python3
"""Prepare datasets for offline use.

Run this ONCE on a networked machine, then copy data/processed/ to the offline
server. The loaders read the processed JSONL directly, so no HF access is
needed at experiment time.

  # on a networked machine:
  python scripts/00_prepare_data.py --dataset hotpotqa --limit 500
  python scripts/00_prepare_data.py --dataset musique  --limit 500

  # copy data/processed/*.jsonl to the offline server, then loaders find them
  # automatically (no --dataset-path needed if the layout is preserved).

You may also point --hf-name at a mirror (e.g. bdsaglam/musique) if the default
repo is unavailable in your region.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.data.loaders import load_dataset_by_name
from src.data.schema import write_jsonl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=["hotpotqa", "musique"])
    ap.add_argument("--split", default="validation")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--hf-name", default=None,
                    help="override the HF repo id, e.g. a regional mirror or "
                         "yapeichang/hotpotqa-filtered")
    ap.add_argument("--config", default=None,
                    help="HF config name; leave unset for filtered mirrors, "
                         "use 'distractor' for the canonical hotpotqa repo")
    ap.add_argument("--only-type", default=None,
                    choices=["bridge", "comparison"],
                    help="HotpotQA: keep only this question type")
    ap.add_argument("--min-gold", type=int, default=None,
                    help="keep only instances with at least this many gold "
                         "sources present in the context")
    ap.add_argument("--out-dir", default="data/processed")
    args = ap.parse_args()

    kw = {"split": args.split, "limit": args.limit}
    if args.hf_name:
        kw["hf_name"] = args.hf_name
    if args.config is not None:
        kw["config"] = args.config
    if args.only_type:
        kw["only_type"] = args.only_type
    if args.min_gold:
        kw["min_gold"] = args.min_gold

    print(f"loading {args.dataset} ({args.split}) ...")
    instances = load_dataset_by_name(args.dataset, **kw)
    print(f"  {len(instances)} instances, M range "
          f"{min(i.M for i in instances)}-{max(i.M for i in instances)}")

    os.makedirs(args.out_dir, exist_ok=True)
    out = os.path.join(args.out_dir, f"{args.dataset}_{args.split}.jsonl")
    write_jsonl(instances, out)
    print(f"wrote {out}")
    print("\nCopy data/processed/ to the offline server; loaders read it directly.")


if __name__ == "__main__":
    main()
