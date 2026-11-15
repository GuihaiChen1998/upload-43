#!/usr/bin/env python3
"""How well does black-box perturbation approximate the gray-box causal signal?

The validation in 08_validate_gold compared gold against gray-box logprob-drop.
This script asks the complementary, and for our motivation more pointed,
question: our black-box perturbation methods read source removal only from
whether the *answer text* changes, whereas the gray-box logprob-drop reads it
from the change in answer *probability*. If the two agree, then giving up
likelihood access -- the whole premise of the strictly black-box setting -- costs
little for attribution, which justifies studying the black-box setting at all.

We compare, on the same instances, the ranking produced by a black-box
perturbation cell (e.g. P5) against the gray-box logprob-drop ranking from
08_validate_gold, and also line both up against gold. Reports:

  * top-1 agreement (perturbation vs logprob-drop): same top source?
  * both-in-gold rate: how often each independently lands top-1 in gold
  * Spearman rho between the two full rankings

  python scripts/09_perturbation_vs_logprob.py \
      --perturbation results/raw/musique/qwen3-8b/P5.jsonl \
      --logprob results/raw/validate_qwen3-8b_musique.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def load_jsonl(path):
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            out[r["qid"]] = r
    return out


def spearman(xs, ys):
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
    return num / (dx * dy) if dx and dy else float("nan")


def rank_to_scores(ranking, M):
    """Convert a ranking (list of source indices, best first) to per-index
    scores (higher = more important) so two rankings can be rank-correlated even
    when one is a permutation and the other has ties broken differently."""
    score = [0.0] * M
    for pos, idx in enumerate(ranking):
        if 0 <= idx < M:
            score[idx] = M - pos
    return score


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--perturbation", required=True,
                    help="a black-box perturbation cell jsonl, e.g. P5.jsonl")
    ap.add_argument("--logprob", required=True,
                    help="the 08_validate_gold output jsonl")
    args = ap.parse_args()

    pert = load_jsonl(args.perturbation)
    lp = load_jsonl(args.logprob)
    shared = sorted(set(pert) & set(lp))
    if not shared:
        print("no shared qids between the two files")
        return
    print(f"comparing on {len(shared)} shared instances "
          f"(perturbation {os.path.basename(args.perturbation)} vs gray-box logprob-drop)")

    top1_match = 0          # perturbation top-1 == logprob top-1
    pert_top1_gold = 0
    lp_top1_gold = 0
    both_top1_gold = 0
    rhos = []
    for qid in shared:
        p, l = pert[qid], lp[qid]
        pr, lr = p.get("ranking", []), l.get("ranking", [])
        if not pr or not lr:
            continue
        gold = set(p.get("gold", []))
        M = max(max(pr), max(lr)) + 1
        pt, lt = pr[0], lr[0]
        top1_match += int(pt == lt)
        pg, lg = pt in gold, lt in gold
        pert_top1_gold += int(pg)
        lp_top1_gold += int(lg)
        both_top1_gold += int(pg and lg)
        rhos.append(spearman(rank_to_scores(pr, M), rank_to_scores(lr, M)))

    n = len(shared)
    rhos = [r for r in rhos if r == r]
    mean_rho = sum(rhos) / len(rhos) if rhos else float("nan")
    print(f"\n=== black-box perturbation vs gray-box logprob-drop ===")
    print(f"  top-1 agreement (same top source):     {top1_match/n:.3f}")
    print(f"  full-ranking Spearman rho (mean):      {mean_rho:.3f}")
    print(f"\n  each independently, top-1 in gold:")
    print(f"    black-box perturbation:  {pert_top1_gold/n:.3f}")
    print(f"    gray-box logprob-drop:   {lp_top1_gold/n:.3f}")
    print(f"    both agree AND in gold:  {both_top1_gold/n:.3f}")
    print(f"\n  interpretation:")
    gap = abs(pert_top1_gold - lp_top1_gold) / n
    if gap < 0.05:
        print(f"  Black-box perturbation matches the gray-box causal signal's")
        print(f"  gold top-1 rate to within {gap:.3f}. Reading source removal from")
        print(f"  answer text rather than answer probability costs almost nothing")
        print(f"  for top-1 attribution -- direct support for the black-box setting")
        print(f"  being a viable place to do contributive attribution (Sec. 5).")
    else:
        print(f"  Black-box and gray-box causal signals differ by {gap:.3f} in gold")
        print(f"  top-1 rate; report the gap honestly and discuss which regime")
        print(f"  loses signal.")
    if mean_rho < 0.5:
        print(f"  The modest full-ranking rho ({mean_rho:.2f}) indicates the two")
        print(f"  agree mainly at the top of the ranking, not across all sources")
        print(f"  -- the same head-vs-tail pattern seen against gold.")


if __name__ == "__main__":
    main()
