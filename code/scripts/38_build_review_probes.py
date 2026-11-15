#!/usr/bin/env python3
"""Instances for the two follow-up probes approved in issue #3 (zero model calls here).

B. Symmetric FEVER evidence relocation (CMU 2): does the self-report follow the evidence or
   the slot / a plausible-looking sentence?
   * swap: an evidence-dependent row with its gold sentence moved to another slot; the slot it
     left receives a sentence from the gold sentence's own page when one exists (the most
     plausible non-evidence sentence), otherwise a random distractor. Same claim, same label.
   * conflict: a claim with BOTH of its evidence sentences (E supporting one verdict, E' the
     opposite) in two slots; which one is at the family's usual slot is balanced by a seeded
     coin. The verdict the model gives reveals which sentence controlled it; a faithful
     self-report must cite that one, and leave-one-out / leave-one-in give a causal check.
     The second evidence sentence replaces a cross-family distractor, so M stays 10.
     Only claims whose two rows are both in the model's evidence-dependent set are used.

C. Unscreened QA candidates (Explore C1): instances the screening excluded for a model, i.e.
   leaked (correct without context) or answered wrongly with context, sampled per dataset.

  python scripts/38_build_review_probes.py [--n-leaked 150 --n-wrong 100]
  -> data/constructed/review_probes/{symfever.<model>.swap,symfever.<model>.conflict,
     <ds>.<model>.unscreened}.jsonl.gz
"""
from __future__ import annotations

import argparse
import copy
import gzip
import json
import os
import random
import sys
import zlib

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
from src.data.schema import read_jsonl  # noqa: E402

MAIN = ["claude-haiku-5-5", "gpt-6-luna", "gemini-2.5-flash-lite"]
OUT = os.path.join(ROOT, "data", "constructed", "review_probes")


def rng_for(key):
    return random.Random(zlib.crc32(key.encode()))


def renumber(srcs):
    for i, s in enumerate(srcs):
        s["idx"] = i
    return srcs


def gold_slot(row):
    return next(i for i, s in enumerate(row["sources"]) if s.get("is_gold"))


def build_swap(row):
    r = copy.deepcopy(row)
    g = gold_slot(r)
    page = r["sources"][g]["title"]
    rng = rng_for(r["qid"] + "::swap")
    same = [i for i, s in enumerate(r["sources"]) if i != g and s["title"] == page]
    j = rng.choice(same) if same else rng.choice([i for i in range(len(r["sources"])) if i != g])
    r["sources"][g], r["sources"][j] = r["sources"][j], r["sources"][g]
    renumber(r["sources"])
    r["qid"] = row["qid"] + "::swap"
    r["meta"] = {**r["meta"], "probe": "swap", "orig_slot": g, "new_slot": j,
                 "moved_in_same_page": bool(same), "base_qid": row["qid"]}
    return r


def build_conflict(a, b):
    """a, b: the two rows of one claim (same question, evidence E vs E', opposite labels)."""
    ga, gb = gold_slot(a), gold_slot(b)
    assert ga == gb, "family rows share the slot layout"
    rng = rng_for(a["meta"]["family"] + a["question"])
    first, second = (a, b) if rng.random() < 0.5 else (b, a)  # which evidence keeps the usual slot
    r = copy.deepcopy(first)
    g = ga
    page = r["sources"][g]["title"]
    cand = [i for i, s in enumerate(r["sources"]) if i != g and s["title"] != page]
    j = rng.choice(cand)
    ev2 = copy.deepcopy(second["sources"][g])
    r["sources"][j] = ev2
    renumber(r["sources"])
    for i, s in enumerate(r["sources"]):
        s["is_gold"] = i in (g, j)
    r["qid"] = first["qid"] + "::conflict"
    r["answer"] = ""  # no single correct verdict: the controlling sentence is read off the answer
    r["meta"] = {**r["meta"], "probe": "conflict", "base_qids": [first["qid"], second["qid"]],
                 "slot_first": g, "label_first": first["answer"], "slot_second": j,
                 "label_second": second["answer"], "first_is_orig_evidence": bool(first["meta"]["orig_evidence"])}
    return r


def write(path, rows):
    os.makedirs(OUT, exist_ok=True)
    with gzip.open(path, "wt", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{len(rows):5d}  {os.path.relpath(path, ROOT)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-leaked", type=int, default=150)
    ap.add_argument("--n-wrong", type=int, default=100)
    a = ap.parse_args()
    fever = [json.loads(l) for l in gzip.open(os.path.join(ROOT, "data", "constructed", "symfever", "symfever.all.jsonl.gz"), "rt")]
    by_q = {r["qid"]: r for r in fever}
    for m in MAIN:
        ev = set(json.load(open(os.path.join(ROOT, "results", "closed", "screen", "symfever", m,
                                             "symfever.all.evaluable.json")))["evidence_dep"])
        write(os.path.join(OUT, f"symfever.{m}.swap.jsonl.gz"), [build_swap(by_q[q]) for q in sorted(ev)])
        # claims: rows of one family with the same question text
        claims = {}
        for q in ev:
            r = by_q[q]
            claims.setdefault((r["meta"]["family"], r["question"]), []).append(r)
        pairs = [sorted(v, key=lambda r: r["qid"]) for v in claims.values() if len(v) == 2]
        write(os.path.join(OUT, f"symfever.{m}.conflict.jsonl.gz"),
              sorted((build_conflict(x, y) for x, y in pairs), key=lambda r: r["qid"]))
    for ds in ("hotpotqa", "musique"):
        insts = {i.qid: i for i in read_jsonl(os.path.join(ROOT, "data", "processed", f"{ds}_validation.jsonl"))}
        for m in MAIN:
            d = os.path.join(ROOT, "results", "closed", "screen", ds, m)
            rows = {}
            for f in ("union.jsonl", "union.retrunc.jsonl"):  # re-asked truncated rows override
                p = os.path.join(d, f)
                if os.path.exists(p):
                    for l in open(p):
                        r = json.loads(l)
                        rows[r["qid"]] = r
            leaked = sorted(q for q, r in rows.items() if r["bucket"] == "leaked")
            wrong = sorted(q for q, r in rows.items() if r["bucket"] in ("both_wrong", "abstained_wrong"))
            rng = rng_for(f"{ds}::{m}::unscreened")
            pick = [(q, "leaked") for q in rng.sample(leaked, min(a.n_leaked, len(leaked)))] + \
                   [(q, "wrong") for q in rng.sample(wrong, min(a.n_wrong, len(wrong)))]
            out = []
            for q, b in sorted(pick):
                j = insts[q].to_json()
                j["meta"] = {**(j.get("meta") or {}), "screen_bucket": b}
                out.append(j)
            write(os.path.join(OUT, f"{ds}.{m}.unscreened.jsonl.gz"), out)


if __name__ == "__main__":
    main()
