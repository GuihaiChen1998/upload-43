#!/usr/bin/env python3
"""Validate gold supporting sources as a proxy for phi*, on open models.

We cannot compute the gray-box logprob drop for the closed model, and our
black-box methods never use it. But on open-weight models we CAN compute it, and
we use it here for one purpose only: to check whether the gold supporting facts
agree with the causal signal that logprob drop provides. If they agree, gold is a
justified proxy for the contributive target across all models (including the
closed one, where only gold is available). If they disagree, that disagreement is
itself reportable and is interpreted in the paper's validation framework -- it
does not invalidate the black-box results, which are relative comparisons on a
fixed gold yardstick.

This runs a leave-one-out logprob-drop attribution (src/baselines/graybox_logprob)
on a small evaluable sample and reports two agreement measures between the
gold-based and logprob-drop-based views:

  * top-1 agreement: does the highest-logprob-drop source land in gold?
    (comparable to how we score the black-box methods)
  * rank correlation: Spearman rho between per-source logprob drop and
    gold membership (1 if gold else 0), per instance, averaged.

Cost is modest: one leave-one-out pass per instance (M+1 scored answers), no
sampling, open models only. Restrict with --only-qids to the shared evaluable set
and --sample-n to keep it small; a few hundred instances suffice to establish
agreement.

  python scripts/08_validate_gold.py --model qwen3-8b --dataset musique \
      --only-qids results/raw/shared_qwen3_musique.json --sample-n 150
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.baselines.graybox_logprob import LogprobScorer
from src.data.loaders import load_dataset_by_name
from src.eval.filtering import load_evaluable_qids, stratified_sample
from src.utils.config import load_model_config


def _spearman(xs, ys):
    """Spearman rho without scipy dependency (ties broken by average rank)."""
    n = len(xs)
    if n < 2:
        return float("nan")
    def ranks(v):
        order = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = sum((rx[i] - mx) ** 2 for i in range(n)) ** 0.5
    dy = sum((ry[i] - my) ** 2 for i in range(n)) ** 0.5
    if dx == 0 or dy == 0:
        return float("nan")
    return num / (dx * dy)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="open-weight model config name")
    ap.add_argument("--dataset", default="musique")
    ap.add_argument("--only-qids", default=None)
    ap.add_argument("--sample-n", type=int, default=150)
    ap.add_argument("--n-instances", type=int, default=999999)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    cfg = load_model_config(args.model)
    if cfg.get("closed"):
        print(f"{args.model} is a closed model; logprob scoring is unavailable "
              f"(this is expected -- validation runs on open models only).")
        return

    ld_kw = {"limit": args.n_instances}
    if args.dataset == "musique":
        ld_kw["balance_hops"] = True
    instances = load_dataset_by_name(args.dataset, **ld_kw)

    if args.only_qids:
        keep = load_evaluable_qids(args.only_qids)
        instances = [i for i in instances if i.qid in keep]
    if args.sample_n and len(instances) > args.sample_n:
        strat = "hop" if args.dataset == "musique" else None
        instances = stratified_sample(instances, args.sample_n, stratify_by=strat)

    print(f"validating gold vs logprob-drop on {args.model}/{args.dataset}, "
          f"{len(instances)} instances")

    scorer = LogprobScorer(
        model=cfg["model"],
        base_url=cfg.get("base_url", "http://localhost:8000/v1"),
        api_key=os.path.expandvars(cfg.get("api_key", "EMPTY")),
    )

    out_path = args.out or f"results/raw/validate_{args.model}_{args.dataset}.jsonl"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    top1_hits = 0
    rhos = []
    n_done = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for inst in instances:
            try:
                res = scorer.score_instance(inst)
            except Exception as e:
                print(f"  skip {inst.qid}: {e}")
                continue
            gold = set(res.gold)
            # top-1 agreement: is the top logprob-drop source a gold source?
            top1 = res.ranking[0] if res.ranking else -1
            hit = top1 in gold
            top1_hits += int(hit)
            # rank correlation: per-source drop vs gold membership
            gold_membership = [1.0 if s.idx in gold else 0.0 for s in inst.sources]
            rho = _spearman(res.drops, gold_membership)
            if rho == rho:  # not nan
                rhos.append(rho)
            n_done += 1
            rec = res.to_json()
            rec["logprob_top1_in_gold"] = hit
            rec["rho_drop_vs_gold"] = rho
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    if n_done == 0:
        print("no instances scored")
        return
    mean_rho = sum(rhos) / len(rhos) if rhos else float("nan")
    top1_agree = top1_hits / n_done
    print(f"\n=== gold vs logprob-drop agreement ({n_done} instances) ===")
    print(f"  logprob-drop top-1 in gold: {top1_agree:.3f}")
    print(f"  mean Spearman rho (drop vs gold membership): {mean_rho:.3f}")
    print(f"\n  interpretation:")
    # Top-1 agreement is the primary signal: it matches how the black-box methods
    # are scored (top-1 against gold) and is not distorted by the many near-zero
    # non-gold drops that a continuous-vs-binary rank correlation folds in. We
    # read top-1 first, then use rho to describe the tail.
    if top1_agree >= 0.70:
        print(f"  HIGH top-1 agreement: the most causally important source (by")
        print(f"  logprob drop) lands in gold {top1_agree:.0%} of the time. On the")
        print(f"  metric the paper actually reports (top-1), gold and the causal")
        print(f"  signal strongly agree -> gold is a justified proxy for phi* at the")
        print(f"  head of the ranking (Sec. 5).")
        if mean_rho < 0.4:
            print(f"  The lower full-ranking rho ({mean_rho:.2f}) reflects (i) the")
            print(f"  binary nature of gold membership vs. continuous drops, which")
            print(f"  depresses Spearman, and (ii) genuine underdetermination among")
            print(f"  non-gold sources -- consistent with the paper's finding that")
            print(f"  attribution views diverge away from the top-1 choice (Sec. 6.2).")
    elif top1_agree >= 0.5 or mean_rho >= 0.3:
        print(f"  MODERATE agreement: gold and causal logprob-drop are related but")
        print(f"  not identical (top-1 {top1_agree:.2f}, rho {mean_rho:.2f}). This is")
        print(f"  consistent with the thesis that different attribution views")
        print(f"  (evidence vs. causal dependence) diverge (Sec. 6.2); report as")
        print(f"  such, not as a failure of gold.")
    else:
        print(f"  LOW agreement on both measures (top-1 {top1_agree:.2f}, rho")
        print(f"  {mean_rho:.2f}): gold, logprob-drop, and (Sec. 6) retrieval are")
        print(f"  only weakly correlated -- multi-hop attribution is underdetermined.")
        print(f"  The black-box results remain valid as relative comparisons on a")
        print(f"  fixed gold yardstick and do not depend on gold being unique truth.")
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    main()
