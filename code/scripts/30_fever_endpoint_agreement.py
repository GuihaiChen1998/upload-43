#!/usr/bin/env python3
"""Cross-endpoint agreement on Symmetric FEVER (zero model calls; round 28).

Compares P1 rows of a stand-in endpoint (tag agree_<ep>, fresh reference draw) with the
S3AI rows of the same qids (tag main):
  * reference verdict agreement across endpoints, next to S3AI's own spontaneous
    change rate (3 extra full-context draws per qid, meta.full_context_change_rate);
  * per-source agreement of the ablated verdicts;
  * P1 tie-aware top-1 on each endpoint.

  python scripts/30_fever_endpoint_agreement.py --ep zhihui
"""
import argparse
import json
import os
import sys

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from src.utils.parsing import normalize_answer  # noqa: E402

D = os.path.join(ROOT, "results", "closed", "raw", "symfever", "gpt-6-luna")


def tie_top1(phi, gold):
    p = np.asarray(phi, float)
    t = np.flatnonzero(np.isclose(p, p.max()))
    return len(set(t) & set(gold)) / len(t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True)
    a = ap.parse_args()
    ref = {json.loads(l)["qid"]: json.loads(l) for l in open(os.path.join(D, "main", "P1.jsonl"))}
    alt = {json.loads(l)["qid"]: json.loads(l) for l in open(os.path.join(D, f"agree_{a.ep}", "P1.jsonl"))}
    qs = sorted(q for q in alt if q in ref and alt[q].get("baseline_answer") is not None)
    n = lambda x: normalize_answer(x or "")  # noqa: E731
    base = [n(alt[q]["baseline_answer"]) == n(ref[q]["baseline_answer"]) for q in qs]
    src = [n(x) == n(y) for q in qs for x, y in zip(alt[q]["meta"]["ablated_answers"] or [],
                                                     ref[q]["meta"]["ablated_answers"] or [])]
    spont = [ref[q]["meta"].get("full_context_change_rate") for q in qs]
    spont_alt = [alt[q]["meta"].get("full_context_change_rate") for q in qs]
    out = {"endpoint": a.ep, "n": len(qs), "n_alt_invalid": sum(alt[q].get("baseline_answer") is None for q in alt),
           "reference_agree": float(np.mean(base)),
           "s3ai_self_change": float(np.mean([x for x in spont if x is not None])),
           "alt_self_change": float(np.mean([x for x in spont_alt if x is not None])),
           "ablated_agree": float(np.mean(src)),
           "p1_top1_s3ai": float(np.mean([tie_top1(ref[q]["phi"], ref[q]["gold"]) for q in qs])),
           "p1_top1_alt": float(np.mean([tie_top1(alt[q]["phi"], alt[q]["gold"]) for q in qs])),
           "phi_identical": float(np.mean([np.allclose(alt[q]["phi"], ref[q]["phi"]) for q in qs]))}
    os.makedirs(os.path.join(ROOT, "results", "closed", "analysis", "endpoint_agreement"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "closed", "analysis", "endpoint_agreement",
                           f"gpt-6-luna.symfever.{a.ep}_vs_s3ai.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
