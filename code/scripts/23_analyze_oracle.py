#!/usr/bin/env python3
"""Analyse the drop-all-gold oracle (22_drop_gold_oracle.py).

Per model x dataset:
  survive_maj   answer still correct in >=2/3 repeats with every gold passage removed
  survive_all   ... in 3/3 repeats
  split by: answer-bearing non-gold passage present (ABD) or not; screening bucket
  (context_dep = wrong without context, abstained_correct = abstains without context).
If P1 rows (tag main, else pilot) exist, cross with P1 all-zero: among P1 all-zero
questions, how many survive gold removal (=> all-zero is explained by something
outside the gold set, not by redundancy among gold passages)?

  python scripts/23_analyze_oracle.py  -> results/closed/analysis/oracle_drop_gold.{md,json}
"""
from __future__ import annotations

import ast
import glob
import json
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
MODELS = ["claude-haiku-5-5", "gpt-6-luna", "gemini-2.5-flash-lite", "gemini-2.5-flash", "gpt-6.1-terra"]


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def bucket_map(ds, model):
    out = {}
    for pool in ("union", "intersection", "audit"):
        for suf in (".jsonl", ".retrunc.jsonl"):
            p = os.path.join(ROOT, "results", "closed", "screen", ds, model, pool + suf)
            if os.path.exists(p):
                for r in jl(p):
                    out[r["qid"]] = r["bucket"]
    return out


def p1_all_zero(ds, model):
    for tag in ("main", "pilot"):
        p = os.path.join(ROOT, "results", "closed", "raw", ds, model, tag, "P1.jsonl")
        if os.path.exists(p):
            out = {}
            for r in jl(p):
                m = r.get("meta")
                m = ast.literal_eval(m) if isinstance(m, str) else (m or {})
                if not m.get("baseline_ok", True):
                    continue
                out[r["qid"]] = not any(abs(x) > 0 for x in r["phi"])
            return tag, out
    return None, {}


def rate(rows, f):
    return (round(sum(f(r) for r in rows) / len(rows), 3), len(rows)) if rows else (None, 0)


def main():
    res, lines = [], ["# Drop-all-gold oracle (original presentation, repeats 0-2)", "",
                      "survive = answer still correct with every gold passage removed (>=2/3 repeats; 3/3 in brackets). "
                      "ABD = some non-gold passage contains a gold answer string.", "",
                      "| dataset | model | n | survive | ABD share | survive ABD | survive no-ABD | survive context_dep | survive abstained_correct | P1 rows | P1 all-zero | survive among P1 all-zero | survive among P1 non-zero |",
                      "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for ds in ("hotpotqa", "musique"):
        for m in MODELS:
            p = os.path.join(ROOT, "results", "closed", "oracle", ds, m, "drop_gold.jsonl")
            if not os.path.exists(p):
                continue
            rows = jl(p)
            bm = bucket_map(ds, m)
            for r in rows:
                r["maj"] = sum(r["correct"]) >= 2
                r["all3"] = all(r["correct"])
                r["abd"] = bool(r["answer_bearing_distractors"])
                r["bucket"] = bm.get(r["qid"])
            tag, az = p1_all_zero(ds, m)
            joined = [r for r in rows if r["qid"] in az]
            z = [r for r in joined if az[r["qid"]]]
            nz = [r for r in joined if not az[r["qid"]]]
            rec = {"dataset": ds, "model": m, "n": len(rows),
                   "survive_maj": rate(rows, lambda r: r["maj"]), "survive_all3": rate(rows, lambda r: r["all3"]),
                   "abd_share": rate(rows, lambda r: r["abd"]),
                   "survive_abd": rate([r for r in rows if r["abd"]], lambda r: r["maj"]),
                   "survive_no_abd": rate([r for r in rows if not r["abd"]], lambda r: r["maj"]),
                   "survive_context_dep": rate([r for r in rows if r["bucket"] == "context_dep"], lambda r: r["maj"]),
                   "survive_abstained_correct": rate([r for r in rows if r["bucket"] == "abstained_correct"], lambda r: r["maj"]),
                   "p1_tag": tag, "p1_n": len(joined), "p1_all_zero": rate(joined, lambda r: az[r["qid"]]),
                   "survive_given_p1_zero": rate(z, lambda r: r["maj"]),
                   "survive_given_p1_nonzero": rate(nz, lambda r: r["maj"])}
            res.append(rec)
            f = lambda t: "–" if t[0] is None else f"{t[0]:.3f} (n={t[1]})"
            lines.append(f"| {ds} | {m} | {len(rows)} | {rec['survive_maj'][0]:.3f} [{rec['survive_all3'][0]:.3f}] | "
                         f"{rec['abd_share'][0]:.3f} | {f(rec['survive_abd'])} | {f(rec['survive_no_abd'])} | "
                         f"{f(rec['survive_context_dep'])} | {f(rec['survive_abstained_correct'])} | "
                         f"{len(joined)} ({tag}) | {f(rec['p1_all_zero'])} | {f(rec['survive_given_p1_zero'])} | {f(rec['survive_given_p1_nonzero'])} |")
    cost = 0.0
    for c in glob.glob(os.path.join(ROOT, "results", "closed", "oracle", "*", "*", "drop_gold.cost.json")):
        cost += sum(r["est_cost_cny"] for r in json.load(open(c))["runs"])
    lines += ["", f"Total cost ≈ ¥{cost:.2f}"]
    out = os.path.join(ROOT, "results", "closed", "analysis", "oracle_drop_gold")
    open(out + ".md", "w").write("\n".join(lines) + "\n")
    json.dump(res, open(out + ".json", "w"), indent=1)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
