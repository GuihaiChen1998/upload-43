#!/usr/bin/env python3
"""Ablation-robustness diagnostic -- the real test behind the CoT exclusion.

01_stability_check measures epsilon on the UNABLATED input: does the same input
give the same answer twice. But Sec. 4.5 excludes CoT x perturbation for a
different reason -- that removing an IRRELEVANT source perturbs the CoT
reasoning path and flips the final answer. That is a property of ablation, not
of resampling, so 01 cannot see it.

This script measures it directly. For each instance, ablate one NON-GOLD source
(which should not change the answer) and record how often the final answer
changes, under CoT vs non-CoT prompting. The quantity of interest is:

    spurious_change_rate = P(answer changes | a non-gold source is removed)

If CoT inflates this rate, the Sec. 4.5 exclusion holds -- just re-grounded on
this measurement rather than on resampling epsilon. If both rates are ~0, the
exclusion has no empirical basis and the method space should be reconsidered
(CoT x perturbation becomes viable, i.e. P6/P7).

  python scripts/01b_ablation_robustness.py \
      --model /path/to/Qwen3-1.7B --dataset hotpotqa \
      --n-instances 50 --ablations-per-instance 3
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from statistics import mean

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.backends.base import GenConfig
from src.data.loaders import load_dataset_by_name
from src.stages.prompting import _BASE, _SCHEMA_ANSWER_ONLY, _COT_PREFIX, _COT_SUFFIX
from src.utils.parsing import normalize_answer, parse_observation


def answer_only_prompt(inst, exclude, cot: bool) -> str:
    body = _BASE.format(
        context=inst.render_context(exclude=exclude), question=inst.question
    )
    if cot:
        return _COT_PREFIX + body + _SCHEMA_ANSWER_ONLY + _COT_SUFFIX
    return body + _SCHEMA_ANSWER_ONLY


def get_answer(backend, inst, exclude, cot, cfg):
    text = backend.generate(
        [{"role": "user", "content": answer_only_prompt(inst, exclude, cot)}], cfg
    )
    obs = parse_observation(text, strict_thinking=False)
    return normalize_answer(obs.answer) if obs.ok and obs.answer else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--base-url", default="http://localhost:8000/v1")
    ap.add_argument("--backend", default="openai", choices=["openai", "anthropic"])
    ap.add_argument("--dataset", default="hotpotqa", choices=["hotpotqa", "musique"])
    ap.add_argument("--n-instances", type=int, default=50)
    ap.add_argument("--ablations-per-instance", type=int, default=3)
    ap.add_argument("--temperature", type=float, default=0.01)
    ap.add_argument("--conditions", nargs="+", default=["structured", "structured_cot"])
    ap.add_argument("--out", default="results/raw/ablation_robustness.json")
    args = ap.parse_args()

    if args.backend == "openai":
        from src.backends.openai_backend import OpenAIBackend
        backend = OpenAIBackend(args.model, base_url=args.base_url,
                                send_thinking_kwarg=(args.backend == "openai"))
    else:
        from src.backends.anthropic_backend import AnthropicBackend
        backend = AnthropicBackend(args.model)

    instances = load_dataset_by_name(args.dataset, limit=args.n_instances)
    cfg = GenConfig(temperature=args.temperature, max_tokens=1024)
    rng = random.Random(0)

    print(f"{args.model} | {args.dataset} | {len(instances)} instances | "
          f"ablate {args.ablations_per_instance} non-gold each\n")

    report = {"model": args.model, "dataset": args.dataset,
              "n_instances": len(instances), "conditions": {}}

    for cond in args.conditions:
        cot = cond.endswith("cot")
        spurious = 0          # answer changed when a NON-GOLD source was removed
        trials = 0
        baseline_unparsable = 0
        gold_changes = 0      # sanity: removing a GOLD source SHOULD change it
        gold_trials = 0

        for inst in instances:
            a0 = get_answer(backend, inst, None, cot, cfg)
            if a0 is None:
                baseline_unparsable += 1
                continue

            non_gold = [s.idx for s in inst.sources if not s.is_gold]
            gold = [s.idx for s in inst.sources if s.is_gold]
            rng.shuffle(non_gold)

            # spurious: ablate irrelevant sources, answer should be stable
            for idx in non_gold[: args.ablations_per_instance]:
                a = get_answer(backend, inst, idx, cot, cfg)
                if a is None:
                    continue
                trials += 1
                if a != a0:
                    spurious += 1

            # sanity check: ablating a gold source, answer should often change
            for idx in gold[:1]:
                a = get_answer(backend, inst, idx, cot, cfg)
                if a is None:
                    continue
                gold_trials += 1
                if a != a0:
                    gold_changes += 1

        rate = spurious / trials if trials else None
        gold_rate = gold_changes / gold_trials if gold_trials else None
        report["conditions"][cond] = {
            "spurious_change_rate": round(rate, 4) if rate is not None else None,
            "gold_change_rate": round(gold_rate, 4) if gold_rate is not None else None,
            "trials": trials,
            "baseline_unparsable": baseline_unparsable,
        }
        print(f"  {cond:16s} spurious_change={rate:.4f} "
              f"(gold_change={gold_rate:.4f}, n={trials})"
              if rate is not None else f"  {cond}: no valid trials")

    c = report["conditions"]
    print("\n--- interpretation")
    if "structured" in c and "structured_cot" in c:
        s = c["structured"]["spurious_change_rate"] or 0
        sc = c["structured_cot"]["spurious_change_rate"] or 0
        delta = sc - s
        print(f"  CoT changes the spurious-change rate by {delta:+.4f}")
        if delta > 0.05:
            print("  -> CoT inflates spurious answer changes: the Sec. 4.5 "
                  "exclusion HOLDS (re-ground it on this metric, not resampling).")
        elif abs(delta) <= 0.05:
            print("  -> CoT does NOT inflate spurious changes: the exclusion "
                  "lacks empirical support. Reconsider adding P6/P7, or justify "
                  "the exclusion on cost/complexity instead of identification.")
    # sanity note
    for cond, v in c.items():
        if v["gold_change_rate"] is not None and v["gold_change_rate"] < 0.3:
            print(f"  ! {cond}: gold-source removal rarely changes the answer "
                  f"({v['gold_change_rate']:.2f}). The model may be ignoring "
                  f"context, or answers are inferable without the gold source. "
                  f"Interpret spurious rates with this in mind.")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
