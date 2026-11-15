#!/usr/bin/env python3
"""Run baselines -- paper Sec. 5.3.

Writes to the same results/raw/<dataset>/<baseline>.jsonl tree the methods use,
so 05_aggregate_results.py picks them up with no special casing. (Baselines go
one level shallower than methods since most are model-independent.)

  # trivial + retrieval (no GPU):
  python scripts/04_run_baselines.py --dataset hotpotqa \
      --baselines random positional bm25 embedding --n-instances 200

  # gray-box upper bound (needs a GPU + open-weight model):
  python scripts/04_run_baselines.py --dataset hotpotqa \
      --baselines contextcite --model Qwen/Qwen3-8B --n-instances 200
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tqdm import tqdm

from src.data.loaders import load_dataset_by_name
from src.eval.metrics import summarize

MODEL_FREE = {"random", "positional", "bm25", "embedding"}
GRAYBOX = {"contextcite", "arc_jsd"}


def build_runner(name, args):
    if name == "random":
        from src.baselines.trivial import run_random
        return lambda inst: run_random(inst, seed=args.seed)
    if name == "positional":
        from src.baselines.trivial import run_positional
        return run_positional
    if name == "bm25":
        from src.baselines.retrieval import run_bm25
        return run_bm25
    if name == "embedding":
        from src.baselines.retrieval import EmbeddingScorer
        return EmbeddingScorer(args.embed_model, device=args.embed_device).run
    if name == "contextcite":
        from src.baselines.contextcite import ContextCiteBaseline
        return ContextCiteBaseline(args.model, args.device, args.num_ablations).run
    if name == "arc_jsd":
        from src.baselines.arc_jsd import ARCJSDBaseline
        return ARCJSDBaseline(args.model, args.device).run
    raise KeyError(name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=["hotpotqa", "musique"])
    ap.add_argument("--baselines", nargs="+", required=True)
    ap.add_argument("--n-instances", type=int, default=200)
    ap.add_argument("--split", default="validation")
    ap.add_argument("--model", default=None, help="open-weight model for gray-box")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--num-ablations", type=int, default=64)
    ap.add_argument("--embed-model", default="mixedbread-ai/mxbai-embed-xsmall-v1")
    ap.add_argument("--embed-device", default="auto",
                    help="auto picks cuda if available, else cpu")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--only-qids", default=None,
                    help="path to a 01c/intersection report; evaluate only its "
                         "qids, matching the set the methods were run on")
    ap.add_argument("--out-root", default="results/raw")
    args = ap.parse_args()

    ld_kw = {"split": args.split, "limit": args.n_instances}
    if args.dataset == "musique":
        ld_kw["balance_hops"] = True
    instances = load_dataset_by_name(args.dataset, **ld_kw)

    # Restrict baselines to the same evaluable/shared set as the methods, so
    # the diagnostic comparison (does a method reduce to BM25?) is like-for-like
    # on identical instances rather than two different pools.
    if args.only_qids:
        from src.eval.filtering import load_evaluable_qids
        keep = load_evaluable_qids(args.only_qids)
        n0 = len(instances)
        instances = [i for i in instances if i.qid in keep]
        print(f"  restricted to {len(instances)} shared instances (from {n0})")
        if not instances:
            print("  ! nothing left; check the --only-qids report and --n-instances")
            return

    for name in args.baselines:
        if name in GRAYBOX and not args.model:
            print(f"skip {name}: gray-box baseline needs --model")
            continue
        runner = build_runner(name, args)

        # Gray-box baselines are model-specific; nest them under the model name.
        if name in GRAYBOX:
            model_tag = os.path.basename(args.model)
            out_dir = os.path.join(args.out_root, args.dataset, model_tag)
        else:
            out_dir = os.path.join(args.out_root, args.dataset, "_baselines")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{name}.jsonl")

        results = []
        with open(out_path, "w", encoding="utf-8") as f:
            for inst in tqdm(instances, desc=name):
                res = runner(inst)
                f.write(json.dumps(res.to_json(), ensure_ascii=False) + "\n")
                results.append(res)

        s = summarize(results, instances=instances)
        print(f"{name}: top1={s['top1_accuracy']:.4f} "
              f"set_f1={s['set_f1']:.4f} -> {out_path}")


if __name__ == "__main__":
    main()
