#!/usr/bin/env python3
"""tab_open.tex: the open-weight models of our earlier study, which supply the multi-hop candidate
pools (Sec. V-A) and the gray-box check of the gold proxy (Sec. VI-B). Zero model calls.

Sources (all in this repository unless noted):
  results/raw/eval_<model>_<dataset>.json   screening of each open model (evaluable = context-dependent
                                            and correct; 13_build_pools.py builds the pools from these)
  results/closed/pools/<dataset>.json       union / intersection sizes
  results/reanalysis/methods.csv            tie-aware top-1 of V1 and P1 (12_reanalysis.py), on the
                                            instances evaluable for every model of a family
  results/raw/musique/_graybox/validate_<model>_musique.jsonl
                                            gray-box leave-one-out log-probability check (MuSiQue),
                                            per instance, from the earlier study's 08_validate_gold.py
                                            (copied from the authors' server, sha256-checked)

  python scripts/40_open_models_table.py  -> paper/tables/tab_open.tex
"""
import csv
import json
import math
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "..", "paper", "tables", "tab_open.tex")
MODELS = [("qwen3-1.7b", "qwen3-1.7b", "Qwen3-1.7B"), ("qwen3-4b", "qwen3-4b", "Qwen3-4B"),
          ("qwen3-8b", "qwen3-8b", "Qwen3-8B"), ("gemma-3-1b-it", "gemma3-1b", "Gemma-3-1B$^\\dagger$"),
          ("gemma-3-4b-it", "gemma3-4b", "Gemma-3-4B"), ("gemma-3-12b-it", "gemma3-12b", "Gemma-3-12B")]
# gray-box check on MuSiQue: top-ranked source by log-prob drop is gold (k of n), Spearman rho of the
# drop with gold membership over all sources
def _graybox(m):
    p = os.path.join(ROOT, "results", "raw", "musique", "_graybox", f"validate_{m}_musique.jsonl")
    rows = [json.loads(l) for l in open(p) if l.strip()]
    rho = [r["rho_drop_vs_gold"] for r in rows if r["rho_drop_vs_gold"] == r["rho_drop_vs_gold"]]
    return sum(bool(r["logprob_top1_in_gold"]) for r in rows), len(rows), sum(rho) / len(rho)


GRAYBOX = {m: _graybox(m) for m in ("qwen3-8b", "gemma3-12b")}


def wilson(k, n, z=1.96):
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


def f2(x):
    return f"{x:.2f}".lstrip("0") if x < 1 else f"{x:.2f}"


def main():
    meth = {(r["dataset"], r["model"], r["method"]): r for r in csv.DictReader(
        open(os.path.join(ROOT, "results", "reanalysis", "methods.csv")))}
    pools = {ds: json.load(open(os.path.join(ROOT, "results", "closed", "pools", f"{ds}.json"))) for ds in ("hotpotqa", "musique")}
    n_shared = {}
    L = [r"\begin{table}[t]", r"\centering\small",
         r"\caption{Open-weight models of our earlier study, served locally with vLLM. Eval.: evaluable "
         r"instances out of %s HotpotQA and %s MuSiQue candidates (context-dependent and correct; "
         r"the union over the five unmarked models is the candidate pool, %s / %s, and %s / %s are "
         r"evaluable for all five). Top-1: tie-aware, on the instances evaluable for all "
         r"models of a family (HotpotQA %s Qwen / %s Gemma, MuSiQue %s / %s). Gray: top-1 of the gray-box "
         r"log-probability drop on MuSiQue, with Wilson 95\%% interval. $^\dagger$Not in the pool.}"
         % ("{:,}".format(pools["hotpotqa"]["n_all"]).replace(",", "{,}"),
            "{:,}".format(pools["musique"]["n_all"]).replace(",", "{,}"),
            pools["hotpotqa"]["n_union"], "{:,}".format(pools["musique"]["n_union"]).replace(",", "{,}"),
            pools["hotpotqa"]["n_intersection"], pools["musique"]["n_intersection"],
            meth[("hotpotqa", "qwen3-8b", "V1")]["n"], meth[("hotpotqa", "gemma3-12b", "V1")]["n"],
            meth[("musique", "qwen3-8b", "V1")]["n"], meth[("musique", "gemma3-12b", "V1")]["n"]),
         r"\label{tab:open}", r"\setlength{\tabcolsep}{2.6pt}",
         r"\begin{tabular}{@{}l rr cc cc c@{}}", r"\toprule",
         r" & \multicolumn{2}{c}{Eval.} & \multicolumn{2}{c}{HotpotQA} & \multicolumn{2}{c}{MuSiQue} & \\",
         r"\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}",
         r"Model & HQA & MSQ & \Vb{1} & \Pb{1} & \Vb{1} & \Pb{1} & Gray \\", r"\midrule"]
    for ev, m, label in MODELS:
        e = {ds: json.load(open(os.path.join(ROOT, "results", "raw", f"eval_{ev}_{ds}.json"))) for ds in ("hotpotqa", "musique")}
        t = lambda ds, k: f2(float(meth[(ds, m, k)]["top1_tieavg"]))  # noqa: E731
        g = "--"
        if m in GRAYBOX:
            k, n, rho = GRAYBOX[m]
            lo, hi = wilson(k, n)
            g = f"{f2(k / n)} [{f2(lo)}, {f2(hi)}]"
        L.append(" & ".join([label, str(len(e["hotpotqa"]["evaluable"])), str(len(e["musique"]["evaluable"])),
                             t("hotpotqa", "V1"), t("hotpotqa", "P1"), t("musique", "V1"), t("musique", "P1"), g]) + r" \\")
        if m == "qwen3-8b":
            L.append(r"\addlinespace[2pt]")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    open(OUT, "w").write("\n".join(L) + "\n")
    print("wrote", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
