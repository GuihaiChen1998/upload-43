#!/usr/bin/env python3
"""Rebuild every table, analysis file and data figure of the paper from the released per-instance
results, with ZERO model calls (no API keys needed). Run from the repository root or code/:

    pip install -r code/requirements-reproduce.txt
    python code/scripts/reproduce_all.py            # analyses + LaTeX tables
    python code/scripts/reproduce_all.py --figures  # also re-render Figs. 2, 4, 5, 7 (needs node, rsvg-convert)
    python code/scripts/reproduce_all.py --tokens   # also token/character cost (needs the response cache:
                                                    #   python code/scripts/restore_cache.py)

Outputs: code/results/closed/analysis/*.{json,md} and paper/tables/*.tex. Afterwards
`git status` shows whether anything differs from the committed versions.
"""
import argparse
import os
import subprocess
import sys
import time

CODE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO = os.path.dirname(CODE)
PY = sys.executable

STEPS = [
    # per-cell tables (Table IV, coverage, routing) -- 28 is the source for most numbers in Sec. VI
    [PY, "scripts/28_paper_tables.py", "--tag", "main", "--split", "test"],
    [PY, "scripts/28_paper_tables.py", "--tag", "main", "--split", "test", "--dataset", "qasper"],
    [PY, "scripts/28_paper_tables.py", "--tag", "main", "--split", "all", "--dataset", "symfever", "--keep", "evidence_dep"],
    [PY, "scripts/28_paper_tables.py", "--tag", "main", "--split", "all", "--dataset", "symfever", "--keep", "full_correct"],
    # method grid (Sec. VI-E), exact-copy control (Table V), hop depth (Sec. VI-F), answer-string baseline
    [PY, "scripts/18_analyze_closed.py", "--tag", "grid", "--split", "test"],
    [PY, "scripts/18_analyze_closed.py", "--tag", "grid_sub"],
    [PY, "scripts/21_analyze_k3.py", "--model", "gpt-6-luna", "--tag", "k3pilot_v2"],
    [PY, "scripts/21_analyze_k3.py", "--model", "gemini-2.5-flash-lite", "--tag", "k3pilot_v2"],
    [PY, "scripts/31_hop_depth.py"],
    [PY, "scripts/32_string_baseline.py"],
    # review audits (Table VI; alignment, mask variability, equivalence, routing, failures) and probes
    [PY, "scripts/36_review_audit.py"],
    [PY, "scripts/39_analyze_probes.py"],
    # figure inputs (feature_dist.json); the matplotlib drafts go to a scratch folder, not the paper
    [PY, "scripts/34_feature_figures.py", "--out", os.path.join(CODE, "results", "figures", "matplotlib")],
    # LaTeX tables (tab_main, tab_k3, tab_review)
    [PY, "scripts/29_paper_figures.py", "--only", "main,k3,review"],
    # open-weight models of the earlier study (Table V): pools, V1/P1 top-1, gray-box check
    [PY, "scripts/40_open_models_table.py"],
]


def run(cmd, cwd=CODE):
    t = time.time()
    print("$", " ".join(os.path.relpath(c, CODE) if os.path.isabs(c) and c.startswith(CODE) else c for c in cmd), flush=True)
    r = subprocess.run(cmd, cwd=cwd)
    if r.returncode:
        sys.exit(f"step failed ({r.returncode}): {' '.join(cmd)}")
    print(f"  ok ({time.time() - t:.0f}s)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--figures", action="store_true")
    ap.add_argument("--tokens", action="store_true")
    a = ap.parse_args()
    os.makedirs(os.path.join(CODE, "results", "figures", "matplotlib"), exist_ok=True)
    steps = list(STEPS)
    if a.tokens:
        steps.insert(-1, [PY, "scripts/37_token_cost.py"])
    for s in steps:
        run(s)
    if a.figures:
        gen = os.path.join(REPO, "paper", "figures", "drafts", "editable-20261106")
        run(["node", "render_figures_paper.cjs"], cwd=gen)
        run(["sh", "crop_to_pdf.sh"], cwd=os.path.join(REPO, "paper", "figures", "gpt"))
    print("\nDone. `git status` lists any file that differs from the committed version.")


if __name__ == "__main__":
    main()
