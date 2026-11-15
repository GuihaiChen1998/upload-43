#!/usr/bin/env python3
"""Output-conditioned string baseline on the closed-model QA cells (zero model calls).

phi_i = 1 if the model's own full-context answer a0 (P1's reference draw), normalised,
occurs as a whole-word substring of source i (normalised), else 0; tie-aware top-1 on
each cell's common valid set (as in 28_paper_tables.py). It uses the model's answer, so
it is not model-free; it shows how far an answer-string cue alone gets on the gold
yardstick (reviewer item B2 / stage-0 report section 4).

  python scripts/32_string_baseline.py -> results/closed/analysis/string_baseline.{json,md}
"""
import glob
import gzip
import importlib.util
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
from src.data.schema import read_jsonl  # noqa: E402
from src.utils.parsing import normalize_answer  # noqa: E402

_s = importlib.util.spec_from_file_location("t", os.path.join(ROOT, "scripts", "28_paper_tables.py"))
t = importlib.util.module_from_spec(_s)
_s.loader.exec_module(t)


def load(ds):
    if ds == "qasper":
        from src.data.schema import Instance
        with gzip.open(os.path.join(ROOT, "data", "constructed", "qasper", "qasper.all.jsonl.gz"), "rt", encoding="utf-8") as f:
            return {i.qid: i for i in (Instance.from_json(json.loads(l)) for l in f if l.strip())}
    p = os.path.join(ROOT, "data", "processed", f"{ds}_validation.jsonl")
    if not os.path.exists(p) and os.path.exists(p + ".gz"):
        with gzip.open(p + ".gz", "rt", encoding="utf-8") as f, open(p, "w", encoding="utf-8") as g:
            g.write(f.read())
    return {i.qid: i for i in read_jsonl(p)}


def main():
    rows = []
    for ds in ("hotpotqa", "musique", "qasper"):
        I = load(ds)
        for dd in sorted(glob.glob(os.path.join(t.RAW, ds, "*", "main"))):
            _, model, R = t.load_cell(dd, "test")
            by = {k: {r["qid"]: r for r in v} for k, v in R.items()}
            present = [m for m in t.COMPARE if m in by]
            bad = {q for m in present if t.needs_ref(m) for q, r in by[m].items() if t.invalid(r)}
            common = sorted(set.intersection(*(set(by[m]) for m in present)) - bad)
            hit, v1 = [], []
            for q in common:
                a0 = normalize_answer(by["P1"][q]["baseline_answer"])
                pat = re.compile(r"(^| )" + re.escape(a0) + r"( |$)") if a0 else None
                phi = [1.0 if pat and pat.search(normalize_answer((s.title or "") + " " + s.text)) else 0.0
                       for s in I[q].sources]
                hit.append(t.a18.tie_top1(phi, by["P1"][q]["gold"]))
                v1.append(t.a18.tie_top1(by["V1"][q]["phi"], by["V1"][q]["gold"]))
            rows.append({"dataset": ds, "model": model, "n_common": len(common),
                         "string_top1": float(np.mean(hit)), "V1_top1": float(np.mean(v1))})
    out = os.path.join(ROOT, "results", "closed", "analysis", "string_baseline")
    json.dump(rows, open(out + ".json", "w"), indent=1)
    with open(out + ".md", "w") as f:
        f.write("# Output-conditioned string baseline (tie-aware top-1, common valid set)\n\n")
        f.write(t.md(rows, ["dataset", "model", "n_common", "string_top1", "V1_top1"]))
    print(open(out + ".md").read())


if __name__ == "__main__":
    main()
