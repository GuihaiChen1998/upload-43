#!/usr/bin/env python3
"""Fixed-budget claude-3-haiku experiment: a verbalize-vs-perturbation gap
demonstration on a true closed API, with configurable methods and dataset.

The default is the cheapest testable point---V1 (vanilla/single/direct verbalize)
vs P1 (vanilla/single/direct perturbation) on HotpotQA---because on a $5 budget
that is what buys enough instances for a paired McNemar test. But the method
choice is configurable: with a larger budget you can run stronger methods
(e.g. V7 vs P5) or several at once, and the dry-run estimator prices the exact
methods you select so you can size --n to the budget before spending anything.

Cost scales sharply with method: on HotpotQA V1 is 1 query/instance but P5 is 62,
so V7-vs-P5 costs ~5x more per instance than V1-vs-P1. Always --dry-run first.

Safety for the hard budget:
  * --dry-run prices the exact --verbalize/--perturbation/--dataset choice with
    NO API calls.
  * --smoke-test runs 5 instances (spends a few cents) to verify API + parsing.
  * The backend tracks real token usage and raises BudgetExceeded before any call
    that would cross the ceiling; partial results are saved incrementally.

The endpoint is OpenAI-compatible (e.g. OmniGate): set OMNIGATE_BASE_URL and
OMNIGATE_API_KEY, or pass --base-url / --api-key. The model id is passed straight
through (default "anthropic/claude-3-haiku").

Usage:
  export OMNIGATE_BASE_URL="https://api.ominigate.ai/v1"
  export OMNIGATE_API_KEY="sk-omg-..."
  # cheapest point, price 200 instances (no API calls):
  python scripts/10_haiku_mini.py --dry-run --n 200
  # stronger methods, price them:
  python scripts/10_haiku_mini.py --dry-run --verbalize V7 --perturbation P5 --n 50
  # smoke test (a few cents) then run for real:
  python scripts/10_haiku_mini.py --smoke-test
  python scripts/10_haiku_mini.py --verbalize V1 --perturbation P1 --n 200 --budget 4.70
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.backends.base import GenConfig
from src.data.loaders import load_hotpotqa, load_musique
from src.pipelines.registry import get_method
from src.pipelines.runner import run_method

TOK_PER_PARA = 130
PROMPT_OVERHEAD = 150
OUT_AVG = 45
PRICE_IN = 1.0 / 1_000_000
PRICE_OUT = 5.0 / 1_000_000


def method_queries(mid: str, M: int) -> int:
    """Exact query count for a method id, given context size M."""
    sp = mid in ("V3", "V4", "V5", "P3", "P4", "P5")
    k = 2 if sp else 1
    if mid.startswith("V"):
        N = 5 if mid in ("V2", "V4", "V5", "V7") else 1
        return N * k
    N = 3 if mid in ("P2", "P4", "P5") else 1
    return (M * N + 1) * k


def estimate_cost(methods: list[str], n_instances: int, M: int,
                  survive_rate: float = 0.34) -> dict:
    """n_instances is the target EVALUABLE count. Filtering costs 2 queries per
    screened candidate, and only ~survive_rate of candidates are evaluable, so we
    screen ~n/survive_rate candidates. Method queries run only on survivors."""
    in_tok = M * TOK_PER_PARA + PROMPT_OVERHEAD
    n_screened = int(n_instances / survive_rate)
    # filtering: 2 queries (full + no-context) per screened candidate
    filter_q = n_screened * 2
    # method queries: only on the n_instances evaluable survivors
    method_q = n_instances * sum(method_queries(m, M) for m in methods)
    total_q = filter_q + method_q
    in_total = total_q * in_tok
    out_total = total_q * OUT_AVG
    cost = in_total * PRICE_IN + out_total * PRICE_OUT
    return {
        "methods": methods,
        "context_M": M,
        "target_evaluable": n_instances,
        "est_screened_candidates": n_screened,
        "filter_queries": filter_q,
        "method_queries": method_q,
        "total_queries": total_q,
        "est_input_tokens": in_total,
        "est_output_tokens": out_total,
        "est_cost_usd": round(cost, 3),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbalize", nargs="*", default=["V1"],
                    help="verbalize method ids to run (e.g. V1 V7)")
    ap.add_argument("--perturbation", nargs="*", default=["P1"],
                    help="perturbation method ids to run (e.g. P1 P5)")
    ap.add_argument("--dataset", choices=["hotpotqa", "musique"], default="hotpotqa")
    ap.add_argument("--n", type=int, default=200, help="max instances")
    ap.add_argument("--budget", type=float, default=4.70, help="hard $ ceiling")
    ap.add_argument("--model", default="anthropic/claude-3-haiku")
    ap.add_argument("--base-url", default=None,
                    help="OpenAI-compatible endpoint (or set OMNIGATE_BASE_URL)")
    ap.add_argument("--api-key", default=None,
                    help="API key (or set OMNIGATE_API_KEY / OPENAI_API_KEY)")
    ap.add_argument("--dry-run", action="store_true", help="estimate only, no API calls")
    ap.add_argument("--smoke-test", action="store_true", help="run 5 instances only")
    ap.add_argument("--out", default=None)
    ap.add_argument("--min-gold", type=int, default=2)
    ap.add_argument("--inner-workers", type=int, default=1,
                    help="parallel ablations within a perturbation call")
    ap.add_argument("--outer-workers", type=int, default=1,
                    help="parallel instances (keep modest under a hard budget)")
    args = ap.parse_args()

    if args.smoke_test:
        args.n = 5

    methods = list(args.verbalize) + list(args.perturbation)
    M = 10 if args.dataset == "hotpotqa" else 20
    if args.out is None:
        tag = "_".join(methods)
        args.out = f"results/raw/haiku_{args.dataset}_{tag}.jsonl"

    if args.dry_run:
        est = estimate_cost(methods, args.n, M)
        print("=== DRY RUN (no API calls) ===")
        for k, v in est.items():
            print(f"  {k}: {v}")
        if est["est_cost_usd"] > args.budget:
            safe_n = int(args.n * args.budget / est["est_cost_usd"])
            print(f"\n  WARNING: ${est['est_cost_usd']} exceeds budget "
                  f"${args.budget}. Reduce --n to ~{safe_n}.")
        else:
            print(f"\n  ${est['est_cost_usd']} within budget ${args.budget}.")
        return

    from src.backends.haiku_budget_backend import CostTrackedHaikuBackend, BudgetExceeded
    # reuse the main experiment's evaluable-filtering helpers so haiku's evaluable
    # set is constructed identically (model-specific, per Sec. 5.2)
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    from importlib import import_module
    _lk = import_module("01c_leakage_check")
    from src.stages.prompting import build_answer_prompt
    _no_context_prompt = _lk._no_context_prompt
    matches_gold = _lk.matches_gold
    is_abstention = _lk.is_abstention
    ask = _lk.ask

    backend = CostTrackedHaikuBackend(model=args.model, budget_usd=args.budget,
                                     base_url=args.base_url, api_key=args.api_key)
    vmethods = [get_method(m) for m in args.verbalize]
    pmethods = [get_method(m) for m in args.perturbation]
    cfg = GenConfig(temperature=0.01, max_tokens=64)

    loader = load_hotpotqa if args.dataset == "hotpotqa" else load_musique
    lkw = {"limit": args.n * 4, "min_gold": args.min_gold}  # 4x: ~1/3 survive evaluable
    if args.dataset == "hotpotqa":
        lkw["only_type"] = "bridge"
    instances = loader(**lkw)
    print(f"loaded {len(instances)} {args.dataset} candidates; target {args.n} "
          f"EVALUABLE instances, methods {methods}, budget ${args.budget}")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    n_done = 0
    n_screened = 0
    n_leaked = n_wrong = 0
    # per-method hit counters
    hits = {m: 0 for m in methods}
    # pairwise discordant counts for the first verbalize vs first perturbation
    v0, p0 = args.verbalize[0], args.perturbation[0]
    disc_v = disc_p = 0

    try:
        with open(args.out, "w", encoding="utf-8") as f:
            for inst in instances:
                if n_done >= args.n:
                    break
                # --- evaluable filtering (model-specific, Sec. 5.2) ---
                # full-context answer and no-context answer, both from haiku itself
                full_ans = ask(backend, build_answer_prompt(inst, structured=True, cot=False), cfg)
                empty_ans = ask(backend, _no_context_prompt(inst.question), cfg)
                n_screened += 1
                full_right = matches_gold(full_ans, inst)
                empty_right = matches_gold(empty_ans, inst)
                if empty_right:
                    n_leaked += 1  # answerable without context -> not evaluable
                    continue
                if not full_right and not is_abstention(empty_ans):
                    n_wrong += 1  # wrong even with context, and didn't abstain -> skip
                    continue
                # evaluable: context-dependent, or abstained-without / correct-with
                gold = set(inst.gold_indices)
                rec = {"qid": inst.qid, "gold": list(gold),
                       "n_hop": inst.n_hop, "M": inst.M}
                tops = {}
                for mid, spec in list(zip(args.verbalize, vmethods)) + \
                                 list(zip(args.perturbation, pmethods)):
                    r = run_method(inst, spec, backend, cfg=cfg,
                                   inner_workers=args.inner_workers)
                    top1 = r.ranking[0] if r.ranking else -1
                    hit = top1 in gold
                    hits[mid] += int(hit)
                    tops[mid] = top1
                    rec[f"{mid}_top1"] = top1
                    rec[f"{mid}_hit"] = hit
                # discordance for the headline pair
                vh, ph = tops[v0] in gold, tops[p0] in gold
                if vh and not ph:
                    disc_v += 1
                elif ph and not vh:
                    disc_p += 1
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                n_done += 1
                if n_done % 10 == 0:
                    s = backend.summary()
                    prog = " ".join(f"{m} {hits[m]}/{n_done}" for m in methods)
                    print(f"  [{n_done} eval / {n_screened} screened] "
                          f"${s['spent_usd']:.3f}/{args.budget} | {prog}")
    except BudgetExceeded as e:
        print(f"\n  STOPPED on budget: {e}")
    except KeyboardInterrupt:
        print("\n  interrupted; partial results saved")

    s = backend.summary()
    print(f"\n=== DONE: {n_done} instances, spent ${s['spent_usd']} of ${args.budget} ===")
    if n_done == 0:
        return
    for m in methods:
        print(f"  {m} top-1 in gold: {hits[m]/n_done:.3f}")
    va, pa = hits[v0] / n_done, hits[p0] / n_done
    print(f"  headline gap ({v0} - {p0}): {va - pa:+.3f}")
    print(f"  discordant: {v0}-only {disc_v}, {p0}-only {disc_p}")
    n_disc = disc_v + disc_p
    if n_disc > 0:
        k = min(disc_v, disc_p)
        p_exact = min(1.0, 2 * sum(math.comb(n_disc, i) * 0.5 ** n_disc
                                   for i in range(0, k + 1)))
        print(f"  McNemar exact two-sided p = {p_exact:.4g} (n_disc={n_disc})")
        if va > pa and p_exact < 0.05:
            print(f"  -> {v0} gap replicates on claude-3-haiku, significant.")
        else:
            print("  -> report descriptively; may be underpowered at this n.")
    print(f"\n  usage: {s}")
    with open(args.out.replace(".jsonl", "_summary.json"), "w") as f:
        json.dump({"summary": s, "hits": hits, "n": n_done,
                   "headline_pair": [v0, p0], "gap": va - pa,
                   "disc_v": disc_v, "disc_p": disc_p}, f, indent=2)


if __name__ == "__main__":
    main()
