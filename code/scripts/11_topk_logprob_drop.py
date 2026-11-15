#!/usr/bin/env python3
"""Top-k log-probability drop evaluation of attribution methods (open models).

This is a ContextCite-style intrinsic evaluation of attribution QUALITY, distinct
from the gold-based top-1 metric used in the main paper. For a given attribution
ranking, we ablate the top-k ranked sources and measure how far the
log-probability of the model's own original answer falls:

    drop@k = log P(a0 | full context) - log P(a0 | context minus top-k sources)

A larger drop means the method's top-k sources were more load-bearing for the
answer, i.e. better attribution. We report drop@1..4 for every method, so methods
can be compared on a signal that does not use gold at all.

Two things to keep in mind when reading the output (and when deciding how to write
it up):
  * This metric requires token log-probabilities, so it is gray-box: it runs on
    the open models only, never on the closed model.
  * It rewards methods that agree with the logprob signal. Perturbation methods
    are themselves built on answer-change under ablation, so this metric may
    structurally favour them; verbalize, which never consults likelihoods, is
    judged here on a criterion it does not optimize. Whether the gold-based and
    logprob-drop rankings of the methods agree is exactly the empirical question
    -- read the numbers before deciding the narrative.

Inputs: the per-method run outputs (jsonl with a `ranking` and `baseline_answer`
per qid) produced by the main pipeline, and a LogprobScorer pointed at the open
model's vLLM endpoint.

  python scripts/11_topk_logprob_drop.py --model qwen3-8b --dataset musique \
      --runs-dir results/raw/musique/qwen3-8b --kmax 4 --sample-n 150
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.baselines.graybox_logprob import LogprobScorer
from src.data.loaders import load_dataset_by_name
from src.utils.config import load_model_config


def load_rankings(runs_dir: str) -> dict:
    """method -> {qid -> ranking list}. Reads every V*/P* jsonl in the dir."""
    out = {}
    for path in sorted(glob.glob(os.path.join(runs_dir, "*.jsonl"))):
        method = os.path.splitext(os.path.basename(path))[0]
        if not (method.startswith("V") or method.startswith("P")):
            continue
        per_qid = {}
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                if r.get("ranking"):
                    per_qid[r["qid"]] = {
                        "ranking": r["ranking"],
                        "answer": r.get("baseline_answer"),
                    }
        if per_qid:
            out[method] = per_qid
    return out


class TopKDropScorer(LogprobScorer):
    """Adds top-k ablation scoring on top of the single-source LogprobScorer."""

    def score_answer_under_exclusion(self, inst, answer, exclude_set) -> float:
        """log P(answer | context with exclude_set ablated), teacher-forced."""
        ctx = inst.render_context_excluding(exclude_set)
        prompt = (
            f"Context:\n{ctx}\n\nQuestion: {inst.question}\nAnswer: "
        )
        return self._score_answer_logprob(prompt, answer)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--dataset", default="musique")
    ap.add_argument("--runs-dir", required=True,
                    help="dir with per-method V*/P*.jsonl run outputs")
    ap.add_argument("--kmax", type=int, default=4)
    ap.add_argument("--cap-by-gold", action="store_true",
                    help="cap k per-instance at its gold count, so drop@k is not "
                         "reported past the number of gold sources (recommended "
                         "for HotpotQA, where every instance has exactly 2 gold: "
                         "only drop@1 and drop@2 are semantically meaningful, since "
                         "drop@3+ necessarily ablates distractors).")
    ap.add_argument("--sample-n", type=int, default=150)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    cfg = load_model_config(args.model)
    if cfg.get("closed"):
        print(f"{args.model} is closed; top-k logprob drop is gray-box and cannot "
              f"run here (expected -- open models only).")
        return

    rankings = load_rankings(args.runs_dir)
    if not rankings:
        print(f"no V*/P*.jsonl rankings found in {args.runs_dir}")
        return
    methods = sorted(rankings.keys())
    print(f"methods found: {methods}")

    # instances, keyed by qid
    instances = {i.qid: i for i in load_dataset_by_name(args.dataset, limit=100000)}

    scorer = TopKDropScorer(
        model=cfg["model"],
        base_url=cfg.get("base_url", "http://localhost:8000/v1"),
        api_key=os.path.expandvars(cfg.get("api_key", "EMPTY")),
    )

    # qids common to all methods (so every method is scored on the same set)
    common = set.intersection(*[set(rankings[m]) for m in methods])
    common = sorted(common)
    if args.sample_n and len(common) > args.sample_n:
        common = common[: args.sample_n]
    print(f"scoring {len(common)} common instances, k=1..{args.kmax}")

    # baseline logprob per qid is answer-specific; each method shares the same a0
    # (the pipeline's baseline_answer). We take a0 from the first method that has
    # it, and cache the full-context logprob per qid.
    base_lp_cache = {}
    results = {m: {k: [] for k in range(1, args.kmax + 1)} for m in methods}

    for qi, qid in enumerate(common):
        inst = instances.get(qid)
        if inst is None:
            continue
        # answer a0: prefer a method's stored baseline_answer
        a0 = None
        for m in methods:
            a0 = rankings[m][qid].get("answer")
            if a0:
                break
        if not a0:
            continue
        # full-context logprob of a0
        if qid not in base_lp_cache:
            base_lp_cache[qid] = scorer.score_answer_under_exclusion(inst, a0, set())
        base_lp = base_lp_cache[qid]

        for m in methods:
            ranking = rankings[m][qid]["ranking"]
            # cap k at this instance's gold count if requested
            inst_kmax = args.kmax
            if args.cap_by_gold:
                inst_kmax = min(args.kmax, len(inst.gold_indices))
            for k in range(1, inst_kmax + 1):
                topk = set(ranking[:k])
                lp_k = scorer.score_answer_under_exclusion(inst, a0, topk)
                drop = base_lp - lp_k
                results[m][k].append(drop)

        if (qi + 1) % 20 == 0:
            print(f"  [{qi+1}/{len(common)}]")

    # aggregate: mean drop@k per method, noting how many instances contributed
    # (under --cap-by-gold, k beyond an instance's gold count is skipped, so on a
    # 2-gold dataset like HotpotQA drop@3/@4 will have zero samples).
    print(f"\n=== mean top-k logprob drop (higher = better attribution) ===")
    # which k's actually have data
    ks_with_data = [k for k in range(1, args.kmax + 1)
                    if any(results[m][k] for m in methods)]
    n_per_k = {k: (len(results[methods[0]][k]) if methods else 0)
               for k in ks_with_data}
    print("  instances per k: " +
          ", ".join(f"drop@{k}: n={n_per_k[k]}" for k in ks_with_data))
    header = "method  " + "  ".join(f"drop@{k}" for k in ks_with_data)
    print(header)
    summary = {}
    for m in methods:
        row = []
        summary[m] = {}
        for k in ks_with_data:
            vals = results[m][k]
            mean = sum(vals) / len(vals) if vals else float("nan")
            summary[m][k] = mean
            row.append(f"{mean:6.3f}")
        print(f"{m:6s}  " + "  ".join(row))

    # verbalize vs perturbation aggregate at k=1
    vs = [summary[m][1] for m in methods if m.startswith("V")]
    ps = [summary[m][1] for m in methods if m.startswith("P")]
    if vs and ps:
        vm = sum(vs) / len(vs)
        pm = sum(ps) / len(ps)
        print(f"\n  mean drop@1: verbalize {vm:.3f} vs perturbation {pm:.3f} "
              f"(diff {vm - pm:+.3f})")
        print("  NOTE: interpret with care -- this metric may structurally favour")
        print("  perturbation (built on answer-change). Compare against the")
        print("  gold-based top-1 ranking of the methods before writing a narrative.")

    out = args.out or f"results/tables/topk_drop_{args.model}_{args.dataset}.json"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump({"model": args.model, "dataset": args.dataset,
                   "n": len(common), "summary": summary}, f, indent=2)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
