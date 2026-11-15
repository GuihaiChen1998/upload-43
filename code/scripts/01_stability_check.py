#!/usr/bin/env python3
"""Measure baseline stability epsilon-hat -- Assumption 1 (paper Sec. 3.4).

RUN THIS FIRST, before any full method sweep. It answers three questions that
the rest of the paper depends on:

  1. Is the output channel deterministic enough for ablation to mean anything?
     If epsilon is large even on unablated input, "the answer changed" is noise
     and the whole interventional paradigm is unsound for that model.
  2. Does the structured-output constraint actually suppress surface variation?
     Compare `structured` against `freeform`.
  3. Does CoT inflate substantive variation?
     Compare `structured` against `structured_cot`. This is the empirical
     backing for excluding CoT x perturbation (Sec. 4.5).

Cheap to run, and it can invalidate the design -- so it goes first.

Example:
  python scripts/01_stability_check.py --model Qwen/Qwen3-8B \
      --dataset hotpotqa --n-instances 50 --n-repeats 5
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.backends.base import GenConfig
from src.data.loaders import load_dataset_by_name
from src.stages.prompting import build_answer_prompt
from src.utils.parsing import (
    ThinkingLeakError, normalize_answer, parse_observation,
)


def build_prompt(inst, condition: str) -> str:
    if condition == "structured":
        return build_answer_prompt(inst, structured=True, cot=False)
    if condition == "freeform":
        return build_answer_prompt(inst, structured=False, cot=False)
    if condition == "structured_cot":
        return build_answer_prompt(inst, structured=True, cot=True)
    raise KeyError(condition)


def extract_answer(text: str, condition: str) -> str | None:
    if condition == "freeform":
        # No schema to lean on: the raw string IS the answer. That is exactly
        # the situation the structured constraint exists to avoid, and the
        # resulting epsilon is the cost of not having it.
        return normalize_answer(text)
    obs = parse_observation(text, strict_thinking=False)
    return normalize_answer(obs.answer) if obs.ok and obs.answer else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--base-url", default="http://localhost:8000/v1")
    ap.add_argument("--backend", default="openai", choices=["openai", "anthropic"])
    ap.add_argument("--dataset", default="hotpotqa", choices=["hotpotqa", "musique"])
    ap.add_argument("--n-instances", type=int, default=50)
    ap.add_argument("--n-repeats", type=int, default=5)
    ap.add_argument("--temperature", type=float, default=0.01)
    ap.add_argument("--conditions", nargs="+",
                    default=["structured", "freeform", "structured_cot"])
    ap.add_argument("--out", default="results/raw/stability.json")
    args = ap.parse_args()

    if args.backend == "openai":
        from src.backends.openai_backend import OpenAIBackend
        backend = OpenAIBackend(args.model, base_url=args.base_url)
    else:
        from src.backends.anthropic_backend import AnthropicBackend
        backend = AnthropicBackend(args.model)

    instances = load_dataset_by_name(args.dataset, limit=args.n_instances)
    cfg = GenConfig(temperature=args.temperature, max_tokens=1024)
    print(f"{args.model} | {args.dataset} | {len(instances)} instances "
          f"x {args.n_repeats} repeats | T={args.temperature}\n")

    report = {"model": args.model, "dataset": args.dataset,
              "n_instances": len(instances), "n_repeats": args.n_repeats,
              "temperature": args.temperature, "conditions": {}}

    for cond in args.conditions:
        unstable = 0
        unparsable = 0
        leaked = 0
        per_instance = []

        for inst in instances:
            msgs = [{"role": "user", "content": build_prompt(inst, cond)}]
            answers = []
            for i in range(args.n_repeats):
                try:
                    text = backend.generate(msgs, cfg, seed=i)
                except Exception as e:
                    print(f"  ! generation error: {e}")
                    continue
                if "<think>" in (text or "").lower():
                    leaked += 1
                answers.append(extract_answer(text, cond))

            valid = [a for a in answers if a]
            if not valid:
                unparsable += 1
                continue
            mode_count = Counter(valid).most_common(1)[0][1]
            stability = mode_count / len(valid)
            per_instance.append(stability)
            if stability < 1.0:
                unstable += 1

        eps = 1.0 - (sum(per_instance) / len(per_instance)) if per_instance else 1.0
        report["conditions"][cond] = {
            "epsilon_hat": round(eps, 4),
            "unstable_instance_rate": round(unstable / max(1, len(per_instance)), 4),
            "unparsable_instances": unparsable,
            "thinking_leaks": leaked,
            "n_scored": len(per_instance),
        }
        print(f"  {cond:18s} eps_hat={eps:.4f}  "
              f"unstable={unstable}/{len(per_instance)}  "
              f"unparsable={unparsable}  leaks={leaked}")

    c = report["conditions"]
    print("\n--- interpretation")
    if "structured" in c and "freeform" in c:
        d = c["freeform"]["epsilon_hat"] - c["structured"]["epsilon_hat"]
        print(f"  structured constraint suppresses surface variation by {d:+.4f}")
    if "structured" in c and "structured_cot" in c:
        d = c["structured_cot"]["epsilon_hat"] - c["structured"]["epsilon_hat"]
        print(f"  CoT inflates substantive variation by {d:+.4f}"
              f"{'  <- supports excluding CoT x perturbation' if d > 0.05 else ''}")
    if c.get("structured", {}).get("thinking_leaks"):
        print("  WARNING: <think> blocks leaked -- thinking mode is NOT disabled. "
              "Fix this before running anything else.")
    if c.get("structured", {}).get("epsilon_hat", 0) > 0.2:
        print("  WARNING: epsilon_hat is high even under constraint; Assumption 1 "
              "is shaky for this model and perturbation results will be noisy.")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
