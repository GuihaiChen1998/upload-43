#!/usr/bin/env python3
"""Paper figures from the analysis JSON written by 28_paper_tables.py (zero model calls).

  fig_frontier.pdf : accuracy-query-cost frontier per (dataset, model) cell -- V1, the
                     single-source probes (P1, MExGen-LOO, LOI), the RM@k curve
                     (k = 8, 16, 32, 64 from one nested RM64 run) and the LOI -> RM@k
                     routes (escalate when LOI has no unique max). Rows: HotpotQA,
                     MuSiQue, Qasper and Symmetric FEVER (each once its analysis file exists).

  python scripts/29_paper_figures.py [--out ../paper/figures]
"""
from __future__ import annotations

import argparse
import json
import os

import matplotlib
import matplotlib.ticker

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
AN = os.path.join(ROOT, "results", "closed", "analysis")

# reference categorical palette, first three slots (all-pairs safe); identity is also
# carried by marker shape and the legend, never by color alone
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1"

MODELS = [("claude-haiku-5-5", "haiku"), ("gpt-6-luna", "luna"), ("gemini-2.5-flash-lite", "flash-lite"),
          ("gemini-2.5-flash", "flash"), ("gpt-6.1-terra", "terra")]
ROWS = [("hotpotqa", "HotpotQA", "paper.main.test.json"),
        ("musique", "MuSiQue", "paper.main.test.json"),
        ("qasper", "Qasper", "paper.main.test.qasper.json"),
        ("symfever", "Sym. FEVER", "paper.main.all.symfever.evidence_dep.json")]
# all three cost M+1; spread horizontally (x factor, log axis) so they do not overprint
SINGLE = [("P1", "o", "P1 (leave-one-out)", 0.86), ("MEXGEN_LOO", "D", "MExGen-LOO", 1.0),
          ("LOI", "s", "LOI (leave-one-in)", 1.16)]
RM = ["RM@8", "RM@16", "RM@32", "RM64"]
ROUTE = ["LOI->RM@16", "LOI->RM@32", "LOI->RM64"]


def style():
    plt.rcParams.update({
        "font.family": "serif", "font.size": 7, "axes.labelsize": 7, "axes.titlesize": 7.5,
        "xtick.labelsize": 6, "ytick.labelsize": 6, "legend.fontsize": 6.5,
        "axes.edgecolor": MUTED, "axes.linewidth": 0.5, "xtick.color": INK2, "ytick.color": INK2,
        "xtick.major.width": 0.5, "ytick.major.width": 0.5, "axes.labelcolor": INK2,
        "pdf.fonttype": 42, "ps.fonttype": 42})


def frontier(out):
    rows = []
    for ds, label, fn in ROWS:
        p = os.path.join(AN, fn)
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        M = {(r["model"], r["method"]): r for r in d["methods"] if r["dataset"] == ds}
        R = {(r["model"], r["route"]): r for r in d["routing"] if r["dataset"] == ds and r["rule"] == "no_unique_max"}
        if M:
            rows.append((label, M, R))
    fig, axes = plt.subplots(len(rows), len(MODELS), figsize=(7.16, 1.45 * len(rows) + 0.35),
                             sharex=True, squeeze=False)
    for ri, (label, M, R) in enumerate(rows):
        for ci, (m, short) in enumerate(MODELS):
            ax = axes[ri][ci]
            ax.set_xscale("log")
            ax.grid(True, color=GRID, linewidth=0.5)
            ax.set_axisbelow(True)
            v1 = M.get((m, "V1"))
            if v1 is None:
                ax.set_visible(False)
                continue
            ax.axhline(v1["top1_common"], color=BLUE, linewidth=0.8, linestyle=(0, (2, 2)), zorder=1)
            ax.plot([v1["cost"]], [v1["top1_common"]], "*", color=BLUE, markersize=8,
                    markeredgecolor="white", markeredgewidth=0.5, zorder=4)
            rm = [M[(m, k)] for k in RM if (m, k) in M]
            ax.plot([r["cost"] for r in rm], [r["top1_common"] for r in rm], "-o", color=ORANGE,
                    linewidth=1.2, markersize=3.2, markeredgecolor="white", markeredgewidth=0.5, zorder=3)
            for k, mk, _, dx in SINGLE:
                r = M.get((m, k))
                if r:
                    ax.plot([r["cost"] * dx], [r["top1_common"]], mk, color=AQUA, markersize=4.2,
                            markeredgecolor="white", markeredgewidth=0.5, zorder=4)
            rt = [R[(m, k)] for k in ROUTE if (m, k) in R]
            if rt:
                ax.plot([r["cost"] for r in rt], [r["top1"] for r in rt], "--^", color=INK2, linewidth=0.7,
                        markersize=3.6, markerfacecolor="white", markeredgecolor=INK2, markeredgewidth=0.7,
                        zorder=5)
            n = v1.get("n_common", v1["n"])
            ax.text(0.97, 0.05, f"n={n}", transform=ax.transAxes, ha="right", va="bottom", fontsize=5.5,
                    color=INK2)
            ax.set_ylim(0.35, 1.03)
            ax.set_yticks([0.4, 0.6, 0.8, 1.0])
            if ri == 0:
                ax.set_title(short, color=INK)
            if ci == 0:
                ax.set_ylabel(f"{label}\ntop-1 (tie-aware)")
            else:
                ax.set_yticklabels([])
            if ri == len(rows) - 1:
                ax.set_xlabel("calls / instance")
            ax.set_xticks([1, 10, 64])
            ax.set_xticklabels(["1", "10", "64"])
            ax.set_xlim(0.7, 110)
            ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    handles = [Line2D([], [], marker="*", color=BLUE, linestyle=(0, (2, 2)), markersize=7, label="V1 (self-report)"),
               *[Line2D([], [], marker=mk, color=AQUA, linestyle="", markersize=4.2, label=lab) for _, mk, lab, _ in SINGLE],
               Line2D([], [], marker="o", color=ORANGE, markersize=3.2, label="RM@8/16/32/64"),
               Line2D([], [], marker="^", color=INK2, linestyle="--", markerfacecolor="white", markersize=3.6,
                      label="LOI→RM@k (no unique max)"),
               ]
    fig.legend(handles=handles, loc="upper center", ncol=6, frameon=False, bbox_to_anchor=(0.5, 1.0),
               handlelength=2.2, columnspacing=1.0)
    fig.tight_layout(rect=(0, 0, 1, 1 - 0.3 / fig.get_figheight()), h_pad=0.4, w_pad=0.3)
    path = os.path.join(out, "fig_frontier.pdf")
    fig.savefig(path, bbox_inches="tight")
    if os.environ.get("FIG_PREVIEW"):  # PNG preview outside the paper folder
        fig.savefig(os.path.join(os.environ["FIG_PREVIEW"], "fig_frontier.png"), dpi=200, bbox_inches="tight")
    print("wrote", path, "rows:", [r[0] for r in rows])


def _f(x, d=3):
    s = f"{x:.{d}f}"
    return s[1:] if s.startswith("0.") else ("$-$" + s[2:] if s.startswith("-0.") else s)


def _sd(x):
    s = f"{x:+.3f}".replace("0.", ".")
    return s.replace("-", "$-$")


def _cells(ds):
    """(methods, coverage) dicts for one dataset from its paper-table JSON."""
    f = {"hotpotqa": "paper.main.test.json", "musique": "paper.main.test.json",
         "qasper": "paper.main.test.qasper.json", "symfever": "paper.main.all.symfever.evidence_dep.json"}[ds]
    d = json.load(open(os.path.join(AN, f)))
    M = {(r["dataset"], r["model"], r["method"]): r for r in d["methods"]}
    C = {(r["dataset"], r["model"], r["method"]): r for r in d["coverage_fidelity"]}
    return M, C


DS4 = (("hotpotqa", "HotpotQA"), ("musique", "MuSiQue"), ("qasper", "Qasper"), ("symfever", "Sym.~FEVER"))


def table_main(out):
    """tab_main.tex: one row per cell. Tie-aware gold top-1 on the common valid set, RM64 - V1 with its
    interval and equivalence class, answer alignment (36_review_audit.py) and routing LOI -> RM64."""
    A = {(r["dataset"], r["model"]): r for r in json.load(open(os.path.join(AN, "review_audit.json")))}
    cols = ["V1", "P1", "MEXGEN_LOO", "LOI", "RM64"]
    pct = lambda x: str(int(round(100 * x)))  # noqa: E731

    def eq(t):
        lo, hi = t["ci90"]
        return r"\checkmark" if t["equiv_0.05"] else (r"$\uparrow$" if lo > 0 else (r"$\downarrow$" if hi < 0 else "?"))
    L = [r"\begin{table*}[t]", r"\centering\footnotesize",
         r"\caption{Results per cell on its common valid set ($n$: instances with records for all compared "
         r"estimators and a valid reference wherever one is required; QA: test split, Symmetric FEVER: "
         r"evidence-dependent set). Top-1: tie-aware gold top-1. $\Delta$RM64: RM64 $-$ \Vb{1} with 95\% "
         r"paired bootstrap interval (FEVER: claim families, Qasper: papers resampled). Eq.: its 90\% interval "
         r"lies within $\pm$0.05 (\checkmark), above ($\uparrow$) or below ($\downarrow$) zero, or none of "
         r"these (?). Agree: share of instances on which \Vb{1}'s own answer equals the reference $a_0$; "
         r"$\Delta$\Pb{1}$|$agree: \Pb{1} $-$ \Vb{1} on those instances. Routing: LOI escalated to RM64 when "
         r"its maximum is not unique; esc.: share escalated; calls: routed / RM64 nominal calls; save: fewer "
         r"calls; $\Delta$: routed $-$ RM64 top-1. On FEVER, flash and terra were run without RM.}",
         r"\label{tab:main}", r"\setlength{\tabcolsep}{2.9pt}",
         r"\begin{tabular}{@{}llr ccccc cc cc cccc@{}}", r"\toprule",
         r" & & & \multicolumn{5}{c}{top-1} & & & \multicolumn{2}{c}{alignment} & \multicolumn{4}{c}{routing LOI $\to$ RM64} \\",
         r"\cmidrule(lr){4-8}\cmidrule(lr){11-12}\cmidrule(l){13-16}",
         r"Data & Model & $n$ & \Vb{1} & \Pb{1} & MExGen & LOI & RM64 & $\Delta$RM64 [95\% CI] & Eq. "
         r"& agree & $\Delta$\Pb{1}$|$agr. & esc. & calls & save & $\Delta$ \\", r"\midrule"]
    for k, (ds, dl) in enumerate(DS4):
        M, C = _cells(ds)
        first = True
        for m, short in MODELS:
            if (ds, m, "V1") not in M:
                continue
            v = M[(ds, m, "V1")]
            rm = M.get((ds, m, "RM64"))
            a = A[(ds, m)]
            cells = [_f(M[(ds, m, kk)]["top1_common"]) if (ds, m, kk) in M else "--" for kk in cols]
            ci = f"{_sd(rm['diff_vs_V1'])} [{_sd(rm['ci_lo'])}, {_sd(rm['ci_hi'])}]" if rm else "--"
            row = [dl if first else "", short, str(v["n_common"]), *cells, ci, eq(a["tost"]) if a.get("tost") else "--",
                   _f(a["align"]["agree"], 2), _sd(a["align"]["P1-V1_agree"][0])]
            if a.get("tost"):
                rt = next(x for x in a["routing"] if x["route"] == "LOI->RM64")
                row += [pct(rt["escalated"]) + r"\%", f"{rt['cost_routed']:.0f}/{rt['cost_rm']:.0f}",
                        pct(rt["saving"]) + r"\%", _sd(rt["diff"][0])]
            else:
                row += ["--"] * 4
            L.append(" & ".join(row) + r" \\")
            first = False
            if m == "gemini-2.5-flash-lite":
                L.append(r"\addlinespace[2pt]")
        if k < len(DS4) - 1:
            L.append(r"\midrule")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    os.makedirs(os.path.join(out, "..", "tables"), exist_ok=True)
    path = os.path.join(out, "..", "tables", "tab_main.tex")
    open(path, "w").write("\n".join(L) + "\n")
    print("wrote", os.path.abspath(path))


def table_review(out):
    """tab_review.tex: answer alignment, equivalence and routing per cell, from 36_review_audit.py and
    37_token_cost.py (issue #3)."""
    A = {(r["dataset"], r["model"]): r for r in json.load(open(os.path.join(AN, "review_audit.json")))}
    T = {(r["dataset"], r["model"]): r for r in json.load(open(os.path.join(AN, "token_cost.json")))}
    pct = lambda x: str(int(round(100 * x)))  # noqa: E731

    def eq(t):
        lo, hi = t["ci90"]
        return r"\checkmark" if t["equiv_0.05"] else (r"$\uparrow$" if lo > 0 else (r"$\downarrow$" if hi < 0 else "?"))
    L = [r"\begin{table*}[t]", r"\centering\small",
         r"\caption{Answer alignment, equivalence and routing, per cell (common valid set of Table~\ref{tab:main}). "
         r"Agree: share of instances on which \Vb{1}'s own answer equals the interventional reference $a_0$ "
         r"after normalisation; $\Delta$\Pb{1}, $\Delta$RM64: difference to \Vb{1} on those instances. "
         r"Equiv.\ (all instances): the 90\% paired interval of RM64 $-$ \Vb{1} lies within $\pm$0.05 "
         r"(\checkmark), entirely above ($\uparrow$) or below ($\downarrow$) zero, or neither (?). Routing: LOI, "
         r"escalated to RM64 when its maximum is not unique; esc.: share escalated; calls: routed / RM64 "
         r"nominal calls; saving in calls and in prompt characters; $\Delta$: routed $-$ RM64 top-1 with 95\% "
         r"paired interval.}",
         r"\label{tab:review}", r"\setlength{\tabcolsep}{3.6pt}",
         r"\begin{tabular}{@{}ll ccc c c ccc c@{}}", r"\toprule",
         r" & & \multicolumn{3}{c}{answer alignment} & & \multicolumn{5}{c}{routing LOI $\to$ RM64} \\",
         r"\cmidrule(lr){3-5}\cmidrule(l){7-11}",
         r"Data & Model & agree & $\Delta$\Pb{1} & $\Delta$RM64 & equiv. & esc.\ \% & calls & save \% & chars \% "
         r"& $\Delta$ [95\% CI] \\", r"\midrule"]
    for k, (ds, dl) in enumerate(DS4):
        first = True
        for m, short in MODELS:
            a = A.get((ds, m))
            if a is None:
                continue
            al = a["align"]
            row = [dl if first else "", short, _f(al["agree"], 2), _sd(al["P1-V1_agree"][0])]
            if a.get("tost"):
                rt = next(x for x in a["routing"] if x["route"] == "LOI->RM64")
                t = T.get((ds, m), {}).get("route_LOI_RM64", {})
                d = rt["diff"]
                row += [_sd(al["RM64-V1_agree"][0]), eq(a["tost"]),
                        pct(rt["escalated"]), f"{rt['cost_routed']:.0f}/{rt['cost_rm']:.0f}", pct(rt["saving"]),
                        pct(t["saving_chars"]) if t else "--", f"{_sd(d[0])} [{_sd(d[1])}, {_sd(d[2])}]"]
            else:
                row += ["--"] * 7
            L.append(" & ".join(row) + r" \\")
            first = False
            if m == "gemini-2.5-flash-lite":
                L.append(r"\addlinespace[2pt]")
        if k < len(DS4) - 1:
            L.append(r"\midrule")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    path = os.path.join(out, "..", "tables", "tab_review.tex")
    open(path, "w").write("\n".join(L) + "\n")
    print("wrote", os.path.abspath(path))


def table_k3(out):
    """tab_k3.tex: answer-group top-1 without (F) and with (C) an exact copy of the answer passage."""
    K = [("gpt-6-luna", "luna"), ("gemini-2.5-flash-lite", "flash-lite")]
    D = [("hotpotqa", "Hot"), ("musique", "MuS")]
    meth = [("V1", "\\Vb{1}"), ("P1", "\\Pb{1}"), ("MEXGEN_LOO", "MExGen"), ("LOI", "LOI"),
            ("RM64:banzhaf_exact", "RM64")]
    T = {}
    for m, _ in K:
        for r in json.load(open(os.path.join(AN, f"k3pilot_v2.{m}.json")))["methods"]:
            T[(m, r["dataset"], r["method"], r["cond"])] = r
    cells = [(m, ds, c) for m, _ in K for ds, _ in D for c in ("F", "C")]
    L = [r"\begin{table}[t]", r"\centering\small",
         r"\caption{Redundancy (exact copies). Top-1 hit on the answer passage or its copy, "
         r"without (F: neutral filler) and with (C: exact copy) a duplicate of the answer "
         r"passage in a reserved slot; $\approx$45 base questions per cell. All-zero: share of "
         r"\Pb{1} score vectors with no signal.}", r"\label{tab:k3}", r"\setlength{\tabcolsep}{3.2pt}",
         r"\begin{tabular}{@{}l" + "cc" * len(K) * len(D) + "@{}}", r"\toprule",
         " & " + " & ".join(rf"\multicolumn{{4}}{{c}}{{{short}}}" for _, short in K) + r" \\",
         "".join(rf"\cmidrule(lr){{{2 + 4 * i}-{5 + 4 * i}}}" for i in range(len(K))),
         " & " + " & ".join(rf"\multicolumn{{2}}{{c}}{{{dl}}}" for _ in K for _, dl in D) + r" \\",
         " & " + " & ".join("F & C" for _ in K for _ in D) + r" \\", r"\midrule"]
    for k, lab in meth:
        L.append(lab + " & " + " & ".join(_f(T[(m, ds, k, c)]["group_top1"], 2) for m, ds, c in cells) + r" \\")
    L.append(r"\midrule")
    L.append(r"chance & " + " & ".join(_f(T[(m, ds, "P1", c)]["group_floor"], 2) for m, ds, c in cells) + r" \\")
    L.append(r"\Pb{1} all-zero & " + " & ".join(_f(T[(m, ds, "P1", c)]["all_zero"], 2) for m, ds, c in cells) + r" \\")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    path = os.path.join(out, "..", "tables", "tab_k3.tex")
    open(path, "w").write("\n".join(L) + "\n")
    print("wrote", os.path.abspath(path))


def heatmap(out):
    """fig_heatmap.pdf: end-to-end tie-aware top-1 of every estimator (rows) in every
    dataset x model cell (columns). V2-V7 / P2 / P5 were run on the multi-hop cells only;
    flash and terra have no RM on Symmetric FEVER. Missing cells are left blank."""
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap
    rows = ["V1", "V2", "V3", "V4", "V5", "V6", "V7", "P1", "P2", "P5", "MEXGEN_LOO", "LOI", "RM@16", "RM@32", "RM64"]
    rlab = {"MEXGEN_LOO": "MExGen-LOO"}
    T = {}
    for fn, key in (("paper.main.test.json", "top1_e2e"), ("paper.main.test.qasper.json", "top1_e2e"),
                    ("paper.main.all.symfever.evidence_dep.json", "top1_e2e")):
        for r in json.load(open(os.path.join(AN, fn)))["methods"]:
            T[(r["dataset"], r["model"], r["method"])] = r[key]
    for r in json.load(open(os.path.join(AN, "grid.test.json")))["methods"]:
        if r["method"] in rows and (r["dataset"], r["model"], r["method"]) not in T:
            T[(r["dataset"], r["model"], r["method"])] = r["top1"]
    groups = [("hotpotqa", "HotpotQA"), ("musique", "MuSiQue"), ("qasper", "Qasper"), ("symfever", "Sym. FEVER")]
    cols = [(ds, m) for ds, _ in groups for m, _ in MODELS]
    A = np.full((len(rows), len(cols)), np.nan)
    for j, (ds, m) in enumerate(cols):
        for i, k in enumerate(rows):
            if (ds, m, k) in T:
                A[i, j] = T[(ds, m, k)]
    cmap = LinearSegmentedColormap.from_list("seq", ["#f4f7fb", "#9ec3ec", "#2a78d6", "#123f7a"])
    cmap.set_bad("#ffffff")
    fig, ax = plt.subplots(figsize=(7.16, 3.55))
    im = ax.imshow(np.ma.masked_invalid(A), cmap=cmap, vmin=0.3, vmax=1.0, aspect="auto")
    for i in range(len(rows)):
        for j in range(len(cols)):
            v = A[i, j]
            if np.isnan(v):
                ax.text(j, i, "–", ha="center", va="center", fontsize=5, color=MUTED)
            else:
                t = f"{v:.2f}"
                ax.text(j, i, "1.0" if t == "1.00" else t[1:], ha="center", va="center", fontsize=4.6,
                        color="white" if v > 0.78 else INK)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([rlab.get(r, r) for r in rows])
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels([short for _ in groups for _, short in MODELS], rotation=60, ha="right", fontsize=5.5)
    for b in (7, 10, 12):  # family separators: self-report | single-source LOO | LOO-derived / LOI | subset
        ax.axhline(b - 0.5, color="white", linewidth=1.6)
    for g in range(1, len(groups)):
        ax.axvline(g * len(MODELS) - 0.5, color="white", linewidth=1.6)
    for g, (_, lab) in enumerate(groups):
        ax.text(g * len(MODELS) + (len(MODELS) - 1) / 2, -0.9, lab, ha="center", va="bottom", fontsize=6.5, color=INK)
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01)
    cb.set_label("top-1 (tie-aware, end-to-end)", fontsize=6)
    cb.ax.tick_params(labelsize=5.5)
    cb.outline.set_visible(False)
    fig.tight_layout()
    path = os.path.join(out, "fig_heatmap.pdf")
    fig.savefig(path, bbox_inches="tight")
    if os.environ.get("FIG_PREVIEW"):
        fig.savefig(os.path.join(os.environ["FIG_PREVIEW"], "fig_heatmap.png"), dpi=220, bbox_inches="tight")
    print("wrote", path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "..", "paper", "figures"))
    ap.add_argument("--only", default=None, help="comma list of: frontier,main,k3,heatmap,review. The paper's "
                    "figures are now GPT's redraws (paper/figures/gpt/), so the default writes TABLES only")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    style()
    todo = set((a.only or "main,k3").split(","))
    if "frontier" in todo:
        frontier(a.out)
    if "main" in todo:
        table_main(a.out)
    if "k3" in todo:
        table_k3(a.out)
    if "heatmap" in todo:
        heatmap(a.out)
    if "review" in todo:
        table_review(a.out)


if __name__ == "__main__":
    main()
