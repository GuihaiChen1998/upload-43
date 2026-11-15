#!/usr/bin/env python3
"""Cross-endpoint agreement from P1 rows (round 24: gpt-6.1-terra on xiaojingai vs Zhihui).

For a model without K3 premise data, compare a second endpoint's P1 run (tag `--other-tag`)
with the reference endpoint's plan-A P1 rows (tag main, repeat 0) on the same questions:
  - full-context (baseline) answer agreement, and per-source ablated-answer agreement;
  - the same two numbers within the reference endpoint (main P1 repeat 0 vs P1.r1 repeat 1),
    which is the run-to-run floor;
  - P1 phi all-zero rate and top-1 on each side.
If cross-endpoint agreement is close to within-endpoint agreement, treat the endpoints as the
same model (as with BootToken vs S3AI for luna on HotpotQA).
  python scripts/25_endpoint_agreement_p1.py --model gpt-6.1-terra --other-tag agree_zhihui
"""
import argparse
import json
import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
from src.utils.parsing import normalize_answer  # noqa: E402


def load(path):
    return {r["qid"]: r for r in map(json.loads, open(path))} if os.path.exists(path) else {}


def first(ans):
    return normalize_answer(ans[0]) if isinstance(ans, list) and ans else normalize_answer(ans or "")


def compare(a, b):
    base = [normalize_answer(a[q]["baseline_answer"] or "") == normalize_answer(b[q]["baseline_answer"] or "")
            for q in a]
    abl = []
    for q in a:
        xa, xb = a[q]["meta"].get("ablated_answers", {}), b[q]["meta"].get("ablated_answers", {})
        for k in xa:
            if k in xb:
                abl.append(first(xa[k]) == first(xb[k]))
    return sum(base) / len(base), (sum(abl) / len(abl) if abl else float("nan")), len(base), len(abl)


def top1(rows):
    hit = 0.0
    for r in rows.values():
        phi, gold = r["phi"], set(r["gold"])
        m = max(phi)
        top = [i for i, v in enumerate(phi) if v == m]
        hit += sum(i in gold for i in top) / len(top)
    return hit / len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--other-tag", required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    out = {}
    for ds in ["hotpotqa", "musique"]:
        base = os.path.join(ROOT, "results", "closed", "raw", ds, a.model)
        other = load(os.path.join(base, a.other_tag, "P1.jsonl"))
        r0 = load(os.path.join(base, "main", "P1.jsonl"))
        r1 = load(os.path.join(base, "main", "P1.r1.jsonl"))
        qs = [q for q in other if q in r0 and q in r1]
        if not qs:
            continue
        O, R0, R1 = ({q: d[q] for q in qs} for d in (other, r0, r1))
        cb, ca, n, na = compare(R0, O)
        wb, wa, _, _ = compare(R0, R1)
        out[ds] = {
            "n": n, "n_ablations": na,
            "cross_baseline_agree": cb, "within_baseline_agree": wb,
            "cross_ablated_agree": ca, "within_ablated_agree": wa,
            "all_zero_ref": sum(r["meta"]["all_zero"] for r in R0.values()) / n,
            "all_zero_other": sum(r["meta"]["all_zero"] for r in O.values()) / n,
            "top1_ref": top1(R0), "top1_other": top1(O),
        }
    print(json.dumps(out, indent=1))
    path = a.out or os.path.join(ROOT, "results", "closed", "analysis", "endpoint_agreement",
                                 f"{a.model}.{a.other_tag}_vs_main.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(out, open(path, "w"), indent=1)


if __name__ == "__main__":
    main()
