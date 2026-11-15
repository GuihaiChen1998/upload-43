#!/usr/bin/env python3
"""Was the requested temperature effective? (zero model calls; round 30)

All requests carried T=0.01 (single pass) or T=0.7 (multi-sample). Per provider docs,
claude-haiku-5-5 does not accept temperature, and gpt-6-luna / gpt-6.1-terra accept it only
with reasoning effort 'none'. This script reports, per (dataset, model):
  * reasoning tokens per call (from the run cost logs) -> was a reasoning mode active?
  * answer diversity of repeated full-context draws at requested T=0.7 (V2: 5 draws) vs
    T=0.01 (P1 reference + 3 noise-control repeats: 4 draws), and the per-draw change rate
    of the unablated answer at T=0.01 (P1) vs T=0.7 (P2), on the same questions.
  python scripts/35_temperature_check.py -> results/closed/analysis/temperature_check.md
"""
import collections
import glob
import json
import os
import sys

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from src.utils.parsing import normalize_answer as n  # noqa: E402

RAW = os.path.join(ROOT, "results", "closed", "raw")
MODELS = ["claude-haiku-5-5", "gpt-6-luna", "gpt-6.1-terra", "gemini-2.5-flash-lite", "gemini-2.5-flash"]


def rows(p):
    return {json.loads(l)["qid"]: json.loads(l) for l in open(p)} if os.path.exists(p) else {}


def main():
    agg = collections.defaultdict(collections.Counter)
    for f in glob.glob(os.path.join(RAW, "*", "*", "*", "*.cost.json")):
        m = f.split(os.sep)[-3]
        for r in json.load(open(f))["runs"]:
            for k in ("calls", "completion_tokens", "reasoning_tokens"):
                agg[m][k] += r.get(k, 0) or 0
    L = ["# Requested temperature vs observed behaviour\n", "## Reasoning tokens per issued call (all runs)\n",
         "| model | calls | reasoning tokens / call | completion tokens / call |", "|---|---|---|---|"]
    for m in MODELS:
        c = agg[m]
        L.append(f"| {m} | {c['calls']} | {c['reasoning_tokens'] / max(c['calls'], 1):.1f} | {c['completion_tokens'] / max(c['calls'], 1):.1f} |")
    L += ["", "## Draw diversity of the full-context prompt (same questions)\n",
          "| dataset | model | n | any answer disagreement: 5 draws @0.7 (V2) | 4 draws @0.01 (P1) | per-draw change @0.01 (P1) | per-draw change @0.7 (P2) |",
          "|---|---|---|---|---|---|---|"]
    for ds in ("hotpotqa", "musique"):
        for m in MODELS:
            b = os.path.join(RAW, ds, m)
            V2, P1, P2 = rows(f"{b}/grid/V2.jsonl"), rows(f"{b}/main/P1.jsonl"), rows(f"{b}/grid/P2.jsonl")
            qs = [q for q in V2 if q in P1 and q in P2 and P1[q]["meta"].get("full_context_change_rate") is not None
                  and P2[q]["meta"].get("full_context_change_rate") is not None]
            if not qs:
                continue
            v2 = np.mean([len({n(a or "") for a in V2[q]["meta"]["answers"]}) > 1 for q in qs])
            p1 = np.mean([P1[q]["meta"]["full_context_change_rate"] > 0 for q in qs])
            r1 = np.mean([P1[q]["meta"]["full_context_change_rate"] for q in qs])
            r2 = np.mean([P2[q]["meta"]["full_context_change_rate"] for q in qs])
            L.append(f"| {ds} | {m} | {len(qs)} | {v2:.3f} | {p1:.3f} | {r1:.3f} | {r2:.3f} |")
    out = os.path.join(ROOT, "results", "closed", "analysis", "temperature_check.md")
    open(out, "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
