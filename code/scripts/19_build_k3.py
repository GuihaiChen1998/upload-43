#!/usr/bin/env python3
"""Build the K3 redundancy-group construction (design v2, section 3 / K3).

No model calls: exact copies need no type pipeline.

For each base instance (a model's evaluable set, hop-stratified sample):
  * answer passage  = the unique gold passage whose text contains the gold
                      answer (or an alias); instances with none / several are
                      skipped and counted;
  * reserved slots  = inserted at random positions (same positions across a
                      base qid's conditions); no original passage is removed;
  * conditions      1 slot : F  (neutral filler)          redundancy 0
                             C  (exact copy of answer passage)       1
                    2 slots: FF                                       0
                             CF (copy in a random one of the 2 slots) 1
                             CC                                       2
  * neutral filler  = a passage from ANOTHER instance of the same dataset that
                      contains neither the answer / aliases, nor any gold title
                      of this instance, nor a capitalised question term, with
                      length closest to the answer passage (length gap reported).

Group labels (answer passage + its copies) are written to meta for evaluation
only; methods never see them.

  python scripts/19_build_k3.py --dataset musique --model gpt-6-luna --n-base 50
  -> data/constructed/k3/<ds>.<model>.n<N>.v2.jsonl  (+ .report.json with content hash)
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from collections import Counter

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)

from src.data.schema import Instance, Source, read_jsonl  # noqa: E402
from src.eval.filtering import stratified_sample  # noqa: E402

import importlib.util  # noqa: E402

_s = importlib.util.spec_from_file_location("re12", os.path.join(ROOT, "scripts", "12_reanalysis.py"))
re12 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(re12)
contains = re12.contains

CONDITIONS = {"F": ["F"], "C": ["C"], "FF": ["F", "F"], "CF": ["C", "F"], "CC": ["C", "C"]}
K3_VERSION = "v2"   # v1 (7404eae and earlier): filler re-indexed after a copy -> CF changed the other slot
REDUNDANCY = {"F": 0, "C": 1, "FF": 0, "CF": 1, "CC": 2}
_STOP = {"The", "A", "An", "In", "Of", "What", "Which", "Who", "Whom", "Whose", "When", "Where", "How",
         "Why", "Is", "Are", "Was", "Were", "Did", "Does", "Do", "That", "This"}


def question_terms(q: str) -> list[str]:
    return [t for t in re.findall(r"\b[A-Z][\w'’-]+(?:\s+[A-Z][\w'’-]+)*", q) if t not in _STOP and len(t) > 2]


def answer_passages(inst: Instance) -> list[int]:
    answers = [inst.answer] + list(inst.answer_aliases or [])
    return [s.idx for s in inst.sources if s.is_gold and any(contains(s.text, a) for a in answers if a)]


def pick_filler(inst, target_len, pool, rng, used):
    answers = [inst.answer] + list(inst.answer_aliases or [])
    gold_titles = [s.title for s in inst.sources if s.is_gold and s.title]
    titles_here = {s.title for s in inst.sources}
    qterms = question_terms(inst.question)
    banned = [a for a in answers if a] + gold_titles + qterms
    best = None
    cand = rng.sample(pool, min(len(pool), 4000))
    for qid, src in cand:
        if qid == inst.qid or src.title in titles_here or (qid, src.title) in used:
            continue
        txt = f"{src.title}\n{src.text}"
        if any(contains(txt, b) for b in banned):
            continue
        gap = abs(len(src.text) - target_len) / max(target_len, 1)
        if best is None or gap < best[0]:
            best = (gap, qid, src)
            if gap < 0.05:
                break
    return best


def build(inst: Instance, pool, rng: random.Random):
    ap = answer_passages(inst)
    if len(ap) != 1:
        return None, ("no_answer_passage" if not ap else "several_answer_passages")
    a = inst.sources[ap[0]]
    used = set()
    fillers = []
    for _ in range(2):
        f = pick_filler(inst, len(a.text), pool, rng, used)
        if f is None:
            return None, "no_filler"
        used.add((f[1], f[2].title))
        fillers.append(f)
    M0 = inst.M
    # slot positions in the final list (sorted), shared across conditions of this base qid
    pos1 = rng.randrange(M0 + 1)
    pos2 = sorted(rng.sample(range(M0 + 2), 2))
    copy_first = rng.random() < 0.5
    out = []
    for cond, slots in CONDITIONS.items():
        if cond == "CF" and not copy_first:
            slots = ["F", "C"]
        positions = [pos1] if len(slots) == 1 else pos2
        orig = [Source(idx=-1, title=s.title, text=s.text, is_gold=s.is_gold) for s in inst.sources]
        roles = ["orig"] * M0
        seq, rseq = list(orig), list(roles)
        used_fillers = []
        # v2: filler j is bound to slot j (slots ordered by position), so turning one
        # slot into a copy never changes the other slot (FF -> CF changes one slot only).
        for j, (p, kind) in enumerate(sorted(zip(positions, slots))):
            if kind == "C":
                src, role = Source(idx=-1, title=a.title, text=a.text, is_gold=True), "copy"
            else:
                f = fillers[j]
                used_fillers.append(f)
                src, role = Source(idx=-1, title=f[2].title, text=f[2].text, is_gold=False), "filler"
            seq.insert(p, src)
            rseq.insert(p, role)
        orig_pos = [i for i, r in enumerate(rseq) if r == "orig"]
        for i, s in enumerate(seq):
            s.idx = i
        ans_new = orig_pos[ap[0]]
        group = [ans_new] + [i for i, r in enumerate(rseq) if r == "copy"]
        out.append(Instance(
            qid=f"{inst.qid}::K3::{cond}", question=inst.question, answer=inst.answer, sources=seq,
            dataset=inst.dataset, n_hop=inst.n_hop, answer_aliases=list(inst.answer_aliases or []),
            meta={"construction": "K3", "base_qid": inst.qid, "condition": cond,
                  "redundancy": REDUNDANCY[cond], "n_slots": len(slots), "roles": rseq,
                  "slot_positions": [i for i, r in enumerate(rseq) if r != "orig"],
                  "answer_passage": ans_new, "redundancy_group": sorted(group),
                  "orig_gold_new_idx": [orig_pos[g] for g in inst.gold_indices],
                  "filler_len_gap": [round(f[0], 3) for f in used_fillers],
                  "k3_version": K3_VERSION,
                  # RM masks keyed by base qid: the 2-slot conditions share M and slot
                  # positions, so FF / CF / CC see the same masks (common random masks)
                  "mask_key": f"{inst.qid}::K3::{len(slots)}slot"}))
    return out, "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=["hotpotqa", "musique"])
    ap.add_argument("--model", required=True, help="whose evaluable (union/intersection) set is the base pool")
    ap.add_argument("--pool", default="union")
    ap.add_argument("--n-base", type=int, default=50)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    insts = read_jsonl(os.path.join(ROOT, "data", "processed", f"{args.dataset}_validation.jsonl"))
    by_qid = {i.qid: i for i in insts}
    summ = json.load(open(os.path.join(ROOT, "results", "closed", "screen", "summary.json")))
    ev = next(r["evaluable_qids"] for r in summ["screening"]
              if r["model"] == args.model and r["dataset"] == args.dataset and r["pool"] == args.pool)
    pool = [(i.qid, s) for i in insts for s in i.sources if not s.is_gold]
    rng = random.Random(args.seed)
    base = sorted((by_qid[q] for q in ev), key=lambda i: i.qid)
    eligible, reasons = [], Counter()
    for inst in base:
        n_ap = len(answer_passages(inst))
        reasons["eligible" if n_ap == 1 else ("no_answer_passage" if n_ap == 0 else "several_answer_passages")] += 1
        if n_ap == 1:
            eligible.append(inst)
    picked = stratified_sample(eligible, args.n_base, "hop" if args.dataset == "musique" else "none",
                               args.seed, verbose=False)
    rows, built_reasons = [], Counter()
    for inst in picked:
        out, why = build(inst, pool, rng)
        built_reasons[why] += 1
        if out:
            rows += out
    out_dir = os.path.join(ROOT, "data", "constructed", "k3")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{args.dataset}.{args.model}.n{args.n_base}.{K3_VERSION}.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r.to_json(), ensure_ascii=False) + "\n")
    gaps = [g for r in rows for g in r.meta["filler_len_gap"]]
    report = {"dataset": args.dataset, "model": args.model, "pool": args.pool, "n_evaluable": len(base),
              "eligibility": dict(reasons), "n_base_built": built_reasons["ok"], "build": dict(built_reasons),
              "n_variants": len(rows), "conditions": list(CONDITIONS),
              "hop_counts": dict(Counter(i.n_hop for i in picked)),
              "filler_len_gap_mean": round(sum(gaps) / len(gaps), 3) if gaps else None,
              "filler_len_gap_max": max(gaps) if gaps else None}
    import hashlib
    report["k3_version"] = K3_VERSION
    report["content_sha256"] = hashlib.sha256(open(path, "rb").read()).hexdigest()
    json.dump(report, open(path.replace(".jsonl", ".report.json"), "w"), indent=1)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
