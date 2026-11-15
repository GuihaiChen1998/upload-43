#!/usr/bin/env python3
"""Build the Qasper single-hop extension (zero model calls; round 28).

Source: Qasper v0.3 (Dasigi et al., NAACL 2021; CC BY 4.0), dev + test JSON from the
official release (see data/raw/qasper/PROVENANCE.md).

Single-evidence, short-extractive pool -- a question is kept only if
  * no annotator marked it unanswerable;
  * at least one annotation is "qualifying": extractive with exactly ONE span of
    1..MAX_SPAN_WORDS words (no BIBREF/TABREF/... placeholders) and exactly ONE evidence
    paragraph; all qualifying annotations cite the SAME paragraph, which occurs verbatim
    in the paper's full text (not a figure/table caption). Evidence cited by any other
    annotation is kept out of the distractors;
  * the paper has >= M-1 other eligible paragraphs (>= MIN_WORDS words, not cited as
    evidence by any annotation of this question).

Instance: M = 10 paragraphs of the same paper in document order -- the evidence paragraph
(the single gold source) plus M-1 others sampled with a seed per question; each rendered
with its section name as the title. The question names the paper:
  'About the paper "<title>": <question>'
Gold answer = first qualifying annotation's span; the other annotations' short spans are aliases. Distractors
are NOT filtered on the answer string: another paragraph may mention the answer without
being annotated evidence. That count is recorded (meta.n_answer_mentions_other) so
results can be stratified by it.

  python scripts/33_build_qasper.py  -> data/constructed/qasper/qasper.all.jsonl.gz (+ build_info.json)
"""
from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import json
import os
import random
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from src.data.schema import Instance, Source  # noqa: E402
from src.utils.parsing import normalize_answer  # noqa: E402

M = 10
MIN_WORDS = 20
MAX_SPAN_WORDS = 8
PLACEHOLDER = re.compile(r"\b(BIBREF|TABREF|FIGREF|SECREF|INLINEFORM|DISPLAYFORM)\d*")
QUESTION = 'About the paper "{title}": {question}'


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def mentions(answer, text):
    a = normalize_answer(answer)
    return bool(a) and re.search(r"(^| )" + re.escape(a) + r"( |$)", normalize_answer(text)) is not None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=os.path.join(ROOT, "data", "raw", "qasper"))
    ap.add_argument("--out-dir", default=os.path.join(ROOT, "data", "constructed", "qasper"))
    ap.add_argument("--seed", type=int, default=20261104)
    a = ap.parse_args()
    stats = collections.Counter()
    out = []
    files = {"dev": "qasper-dev-v0.3.json", "test": "qasper-test-v0.3.json"}
    for split, fn in files.items():
        papers = json.load(open(os.path.join(a.raw, fn), encoding="utf-8"))
        for pid, p in sorted(papers.items()):
            paras = [(sec["section_name"] or "", t.strip()) for sec in p["full_text"] for t in sec["paragraphs"] if t.strip()]
            for qa in p["qas"]:
                stats["questions"] += 1
                anns = [x["answer"] for x in qa["answers"]]
                if not anns:
                    stats["drop_no_annotation"] += 1
                    continue
                if any(x["unanswerable"] for x in anns):
                    stats["drop_some_annotator_unanswerable"] += 1
                    continue
                qual = [x for x in anns if x["yes_no"] is None and len(x["extractive_spans"]) == 1
                        and 1 <= len(x["extractive_spans"][0].split()) <= MAX_SPAN_WORDS
                        and not PLACEHOLDER.search(x["extractive_spans"][0]) and len(x["evidence"]) == 1]
                if not qual:
                    stats["drop_no_short_single_span_single_evidence_annotation"] += 1
                    continue
                evs = {x["evidence"][0].strip() for x in qual}
                if len(evs) != 1:
                    stats["drop_qualifying_annotations_disagree_on_paragraph"] += 1
                    continue
                ev = next(iter(evs))
                gi = [i for i, (_, t) in enumerate(paras) if t == ev]
                if len(gi) != 1:
                    stats["drop_evidence_not_in_text"] += 1
                    continue
                gi = gi[0]
                cited = {e.strip() for x in anns for e in x["evidence"]}
                others = [i for i, (_, t) in enumerate(paras)
                          if i != gi and t not in cited and len(t.split()) >= MIN_WORDS and not PLACEHOLDER.fullmatch(t)]
                if len(others) < M - 1:
                    stats["drop_short_paper"] += 1
                    continue
                rng = random.Random(f"{a.seed}:{qa['question_id']}")
                pick = sorted(rng.sample(others, M - 1) + [gi])
                spans = [x["extractive_spans"][0].strip() for x in qual] + \
                        [sp.strip() for x in anns if x not in qual for sp in x["extractive_spans"]
                         if 1 <= len(sp.split()) <= MAX_SPAN_WORDS and not PLACEHOLDER.search(sp)]
                answer, aliases = spans[0], sorted({s for s in spans[1:] if normalize_answer(s) != normalize_answer(spans[0])})
                srcs = []
                for k, i in enumerate(pick):
                    sec, t = paras[i]
                    srcs.append(Source(idx=k, title=sec.split(":::")[-1].strip() or "Text", text=t, is_gold=(i == gi)))
                n_mention = sum(mentions(s, x.text) for x in srcs if not x.is_gold for s in [answer])
                inst = Instance(qid=f"qasper_{qa['question_id']}",
                                question=QUESTION.format(title=p["title"].strip(), question=qa["question"].strip()),
                                answer=answer, sources=srcs, dataset="qasper", n_hop=None, answer_aliases=aliases,
                                meta={"paper_id": pid, "split": split, "n_annotations": len(anns), "n_qualifying": len(qual),
                                      "gold_slot": pick.index(gi), "gold_mentions_answer": mentions(answer, ev),
                                      "n_answer_mentions_other": n_mention, "n_paragraphs_paper": len(paras)})
                out.append(inst)
                stats[f"kept_{split}"] += 1
                stats[f"answer_mentions_other>0"] += int(n_mention > 0)
    os.makedirs(a.out_dir, exist_ok=True)
    path = os.path.join(a.out_dir, "qasper.all.jsonl.gz")
    with gzip.open(path, "wt", encoding="utf-8") as f:
        for i in sorted(out, key=lambda i: i.qid):
            f.write(json.dumps(i.to_json(), ensure_ascii=False) + "\n")
    info = {"seed": a.seed, "M": M, "min_words": MIN_WORDS, "max_span_words": MAX_SPAN_WORDS,
            "question_template": QUESTION, "stats": dict(sorted(stats.items())),
            "n_papers": len({i.meta["paper_id"] for i in out}),
            "inputs_sha256": {fn: sha256(os.path.join(a.raw, fn)) for fn in files.values()}}
    json.dump(info, open(os.path.join(a.out_dir, "build_info.json"), "w"), indent=1)
    print(json.dumps(info, indent=1))


if __name__ == "__main__":
    main()
