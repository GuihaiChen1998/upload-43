#!/usr/bin/env python3
"""Empty-context leakage diagnostic -- can the model answer without the context?

Across three model sizes, ablating a GOLD source changed the answer only ~40% of
the time. If the model can already answer from parametric knowledge, ablation
has nothing to detect, and every metric downstream is measured on instances
where the causal signal does not exist.

This script measures that directly by asking the question with NO sources at
all, and comparing against the full-context answer:

  leaked        empty-context answer matches the gold answer
                -> parametric knowledge; ablation cannot reveal dependence
  context_dep   empty-context answer is wrong but full-context is right
                -> the instance genuinely requires the context (what we want)
  both_wrong    wrong either way -> the instance is uninformative for attribution

Two confounds are handled explicitly:
  * yes/no questions can be guessed at 50%, so they are reported separately;
  * "I don't know"-style refusals are counted as abstentions, not as wrong
    answers, since a refusal is evidence of NON-leakage rather than of failure.

Output includes a qid list of leaked instances, so 02/03 runs can exclude them.

  python scripts/01c_leakage_check.py \
      --model /path/to/Qwen3-8B --dataset hotpotqa --n-instances 100
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.backends.base import GenConfig
from src.data.loaders import load_dataset_by_name
from src.stages.prompting import _SCHEMA_ANSWER_ONLY, build_answer_prompt
from src.utils.parsing import normalize_answer, parse_observation

def _no_context_prompt(question: str) -> str:
    """Build the no-context prompt.

    Deliberately concatenated rather than .format()-ed: the schema string
    contains literal JSON braces, which str.format would try to interpret as
    replacement fields.
    """
    return (
        "Answer the question from your own knowledge.\n\n"
        f"Question: {question}\n\n"
        'If you do not know the answer, respond with {"short_answer": "unknown"}.\n'
        + _SCHEMA_ANSWER_ONLY
    )

_ABSTAIN = {"unknown", "i don t know", "i dont know", "not known",
            "no answer", "unanswerable", "n a", "none", "unclear", "cannot"}

_YESNO = {"yes", "no"}


def is_abstention(ans: str | None) -> bool:
    if not ans:
        return True
    return ans in _ABSTAIN or any(a in ans for a in ("don t know", "unknown"))


def matches_gold(pred: str | None, inst) -> bool:
    """Lenient match: exact, or gold contained in prediction (or vice versa).

    Deliberately generous -- we are trying NOT to under-count leakage, since an
    undetected leaked instance silently corrupts the attribution evaluation.
    """
    if not pred:
        return False
    golds = [inst.answer] + list(inst.answer_aliases or [])
    p = normalize_answer(pred)
    for g in golds:
        g = normalize_answer(g)
        if not g:
            continue
        if p == g or (len(g) > 3 and g in p) or (len(p) > 3 and p in g):
            return True
    return False


def ask(backend, content, cfg):
    text = backend.generate([{"role": "user", "content": content}], cfg)
    obs = parse_observation(text, strict_thinking=False)
    return normalize_answer(obs.answer) if obs.ok and obs.answer else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--base-url", default="http://localhost:8000/v1")
    ap.add_argument("--backend", default="openai", choices=["openai", "anthropic"])
    ap.add_argument("--dataset", default="hotpotqa", choices=["hotpotqa", "musique"])
    ap.add_argument("--n-instances", type=int, default=100)
    ap.add_argument("--no-balance-hops", action="store_true",
                    help="MuSiQue: take instances in file order instead of "
                         "balancing across hop counts. The first N rows are "
                         "almost all 2-hop, so balancing is on by default.")
    ap.add_argument("--temperature", type=float, default=0.01)
    ap.add_argument("--out", default="results/raw/leakage.json")
    args = ap.parse_args()

    if args.backend == "openai":
        from src.backends.openai_backend import OpenAIBackend
        backend = OpenAIBackend(args.model, base_url=args.base_url)
    else:
        from src.backends.anthropic_backend import AnthropicBackend
        backend = AnthropicBackend(args.model)

    ld_kw = {"limit": args.n_instances}
    if args.dataset == "musique" and not args.no_balance_hops:
        # Without this the first N rows are overwhelmingly 2-hop, and the
        # per-hop breakdown below would be vacuous.
        ld_kw["balance_hops"] = True
    instances = load_dataset_by_name(args.dataset, **ld_kw)
    cfg = GenConfig(temperature=args.temperature, max_tokens=128)

    print(f"{args.model} | {args.dataset} | {len(instances)} instances\n")

    buckets = {"leaked": [], "context_dep": [], "both_wrong": [],
               "abstained_correct": [], "abstained_wrong": [], "unparsable": []}
    yesno_leaked = 0
    yesno_total = 0
    # Per-hop tallies (MuSiQue). The evaluable set is conditioned on the model
    # answering correctly, and accuracy falls with hop count, so the subset
    # skews toward shallower instances. That skew has to be visible before any
    # hop-stratified analysis is attempted -- and reported in the dataset
    # description either way.
    hop_total: dict[int, int] = {}
    hop_evaluable: dict[int, int] = {}

    for inst in instances:
        empty = ask(backend, _no_context_prompt(inst.question), cfg)
        full = ask(backend, build_answer_prompt(inst, structured=True, cot=False), cfg)

        h = inst.n_hop
        if h is not None:
            hop_total[h] = hop_total.get(h, 0) + 1

        if empty is None and full is None:
            buckets["unparsable"].append(inst.qid)
            continue

        gold_is_yesno = normalize_answer(inst.answer) in _YESNO
        if gold_is_yesno:
            yesno_total += 1

        empty_right = matches_gold(empty, inst)
        full_right = matches_gold(full, inst)

        if is_abstention(empty):
            # Refusing without context is the ideal profile -- no parametric
            # knowledge. Whether the instance is USABLE then depends on whether
            # the model gets it right once the context is supplied, so split
            # this bucket rather than lumping it together.
            if full_right:
                buckets["abstained_correct"].append(inst.qid)
                is_evaluable = True
            else:
                buckets["abstained_wrong"].append(inst.qid)
                is_evaluable = False
        elif empty_right:
            buckets["leaked"].append(inst.qid)
            is_evaluable = False
            if gold_is_yesno:
                yesno_leaked += 1
        elif full_right:
            buckets["context_dep"].append(inst.qid)
            is_evaluable = True
        else:
            buckets["both_wrong"].append(inst.qid)
            is_evaluable = False

        if h is not None and is_evaluable:
            hop_evaluable[h] = hop_evaluable.get(h, 0) + 1

    n = sum(len(v) for v in buckets.values())

    def pct(k):
        return f"{len(buckets[k]):4d}  ({len(buckets[k])/n:.1%})"

    print(f"  {'leaked':20s} {pct('leaked')}  correct with NO context")
    print(f"  {'context_dep':20s} {pct('context_dep')}  wrong w/o context, right with")
    print(f"  {'abstained_correct':20s} {pct('abstained_correct')}  refused w/o context, "
          f"right with  <- ideal")
    print(f"  {'abstained_wrong':20s} {pct('abstained_wrong')}  refused w/o context, "
          f"still wrong with")
    print(f"  {'both_wrong':20s} {pct('both_wrong')}  wrong either way")
    print(f"  {'unparsable':20s} {pct('unparsable')}")

    # EVALUABLE = no parametric shortcut AND the model actually produces the
    # right answer. Only here do gold supporting facts serve as a valid
    # attribution target: if the model answers wrongly, the evidence it used is
    # under no obligation to match the human-annotated gold evidence.
    evaluable = buckets["context_dep"] + buckets["abstained_correct"]
    leak_rate = len(buckets["leaked"]) / n if n else 0

    print("\n--- interpretation")
    print(f"  leakage rate: {leak_rate:.1%}")
    if yesno_total:
        print(f"  of which yes/no questions: {yesno_leaked}/{yesno_total} "
              f"(guessable at ~50%, discount accordingly)")
    print(f"  EVALUABLE (no leak + model correct): {len(evaluable)}/{n} "
          f"= {len(evaluable)/n:.1%}")
    print(f"    -> to obtain K evaluable instances, sample about "
          f"{int(round(1/(len(evaluable)/n)))}K raw instances"
          if evaluable else "    -> no evaluable instances found")

    if leak_rate > 0.3:
        print("  HIGH leakage: ablation cannot reveal dependence on instances the "
              "model already knows.")
    elif leak_rate > 0.15:
        print("  MODERATE leakage: report the full set and the evaluable subset; "
              "the gap is itself a finding.")
    else:
        print("  LOW leakage: parametric knowledge is not the limiting factor "
              "here -- attrition comes from the model failing the task.")

    if len(buckets["both_wrong"]) + len(buckets["abstained_wrong"]) > 0.3 * n:
        print("  ! A large share of instances are answered incorrectly even with "
              "full context. Gold supporting facts are not a valid attribution "
              "target there -- the model's evidence need not match the annotation.")

    if hop_total:
        print("\n--- evaluable set by hop count")
        for h in sorted(hop_total):
            tot = hop_total[h]
            ev = hop_evaluable.get(h, 0)
            print(f"  {h}-hop: {ev:4d}/{tot:4d} evaluable ({ev/tot:.1%})")
        counts = [hop_evaluable.get(h, 0) for h in sorted(hop_total)]
        smallest = min(counts) if counts else 0
        if len(hop_total) < 2:
            print(f"  ! only {len(hop_total)} hop level present -- the sample is "
                  f"not hop-diverse, so no stratified analysis is possible. "
                  f"Re-run without --no-balance-hops.")
        elif smallest < 30:
            print(f"  ! smallest hop bucket has {smallest} evaluable instances. "
                  f"A hop-stratified analysis would lack statistical power; "
                  f"prefer reporting the aggregate rate plus a note that the "
                  f"evaluable set skews toward shallower instances.")
        elif smallest < 50:
            print(f"  smallest hop bucket: {smallest}. Stratification is "
                  f"borderline; report exact n per stratum if you use it.")
        else:
            print(f"  smallest hop bucket: {smallest}. Adequate for a "
                  f"hop-stratified analysis.")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump({"model": args.model, "dataset": args.dataset,
                   "n": n, "leak_rate": leak_rate,
                   "evaluable_rate": len(evaluable) / n if n else 0,
                   "yesno_leaked": yesno_leaked, "yesno_total": yesno_total,
                   "hop_total": hop_total, "hop_evaluable": hop_evaluable,
                   "buckets": buckets, "evaluable": evaluable}, f, indent=2)
    print(f"\nwrote {args.out}")
    print("  buckets['leaked'] -> qids to exclude")
    print("  ['evaluable']     -> qids to evaluate on (pass to 02 via --only-qids)")


if __name__ == "__main__":
    main()
