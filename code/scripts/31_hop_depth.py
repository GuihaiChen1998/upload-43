#!/usr/bin/env python3
"""Reasoning depth on MuSiQue, chance-corrected (zero model calls; reviewer item A8).

Hop count equals the number of gold paragraphs, so raw top-1 rises with hops by chance
(|G|/M = h/20). We use kappa_h = (acc_h - chance_h) / (1 - chance_h) per model and hop,
and report the 4-hop minus 2-hop difference pooled over the three main models
(equal model weights), with a stratified bootstrap CI (resampling within model x hop).
Same common valid set as 28_paper_tables.py (test split).

  python scripts/31_hop_depth.py  -> results/closed/analysis/hop_depth.{json,md}
"""
import glob
import importlib.util
import json
import os

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_s = importlib.util.spec_from_file_location("t", os.path.join(ROOT, "scripts", "28_paper_tables.py"))
t = importlib.util.module_from_spec(_s)
_s.loader.exec_module(t)
MAIN = ["claude-haiku-5-5", "gpt-6-luna", "gemini-2.5-flash-lite"]
METHODS = ["V1", "P1", "LOI", "RM64"]
B = 2000


def main():
    cells = {}
    for dd in sorted(glob.glob(os.path.join(t.RAW, "musique", "*", "main"))):
        ds, model, R = t.load_cell(dd, "test")
        by = {k: {r["qid"]: r for r in v} for k, v in R.items()}
        qs = [q for q in by["V1"] if all(q in by[m] and not (t.needs_ref(m) and t.invalid(by[m][q])) for m in METHODS)]
        for m in METHODS:
            for h in (2, 3, 4):
                Q = [q for q in qs if len(by[m][q]["gold"]) == h]
                cells[(model, m, h)] = (np.array([t.a18.tie_top1(by[m][q]["phi"], by[m][q]["gold"]) for q in Q]),
                                        float(np.mean([h / len(by[m][q]["phi"]) for q in Q])))
    kap = lambda x, ch: (x.mean() - ch) / (1 - ch)  # noqa: E731
    rng = np.random.default_rng(0)
    rows = []
    for m in METHODS:
        per = {h: [kap(*cells[(mo, m, h)]) for mo in MAIN] for h in (2, 3, 4)}
        d = np.mean(per[4]) - np.mean(per[2])
        bs = []
        for _ in range(B):
            k = {}
            for h in (2, 4):
                k[h] = np.mean([kap(cells[(mo, m, h)][0][rng.integers(0, len(cells[(mo, m, h)][0]), len(cells[(mo, m, h)][0]))],
                                    cells[(mo, m, h)][1]) for mo in MAIN])
            bs.append(k[4] - k[2])
        rows.append({"method": m, **{f"kappa_h{h}": float(np.mean(per[h])) for h in (2, 3, 4)},
                     "n": {h: int(sum(len(cells[(mo, m, h)][0]) for mo in MAIN)) for h in (2, 3, 4)},
                     "diff_4_minus_2": float(d), "ci_lo": float(np.quantile(bs, 0.025)), "ci_hi": float(np.quantile(bs, 0.975)),
                     "per_model": {mo: {h: float(kap(*cells[(mo, m, h)])) for h in (2, 3, 4)} for mo in MAIN}})
    out = os.path.join(ROOT, "results", "closed", "analysis", "hop_depth")
    json.dump(rows, open(out + ".json", "w"), indent=1)
    with open(out + ".md", "w") as f:
        f.write("# Chance-corrected top-1 by hop, MuSiQue, 3 main models (equal weights)\n\n"
                "| method | kappa 2-hop | 3-hop | 4-hop | 4-hop − 2-hop [95% CI] |\n|---|---|---|---|---|\n")
        for r in rows:
            f.write(f"| {r['method']} | {r['kappa_h2']:.3f} | {r['kappa_h3']:.3f} | {r['kappa_h4']:.3f} | "
                    f"{r['diff_4_minus_2']:+.3f} [{r['ci_lo']:+.3f}, {r['ci_hi']:+.3f}] |\n")
    print(open(out + ".md").read())


if __name__ == "__main__":
    main()
