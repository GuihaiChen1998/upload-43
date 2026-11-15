#!/usr/bin/env python3
"""Instance-level figures (zero model calls; round 30).

fig_maps.pdf  : attribution maps. For single-gold datasets (Qasper, Symmetric FEVER) and
                one model, 40 seeded evaluable instances (rows) x 10 sources (columns:
                the gold source first, then the other sources in context order). One panel
                per estimator (V1, P1, LOI, RM64); cell = score, rows grouped by P1's outcome
                (unique max / tie / all zero) so the failure modes are visible at a glance.
fig_dist.pdf  : distributions behind the failure modes, per dataset (models pooled):
                (a) spontaneous changes of the unablated answer (0-3 of 3 repeats),
                (b) structure of P1's top set (all zero / unique / 2-way tie / 3+ tie),
                (c) RM64 scores of gold vs. non-gold sources.

  python scripts/34_feature_figures.py [--out ../paper/figures]
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import random

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW = os.path.join(ROOT, "results", "closed", "raw")
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
MODELS = ["claude-haiku-5-5", "gpt-6-luna", "gemini-2.5-flash-lite", "gemini-2.5-flash", "gpt-6.1-terra"]
DATASETS = [("hotpotqa", "HotpotQA"), ("musique", "MuSiQue"), ("qasper", "Qasper"), ("symfever", "Sym. FEVER")]


def style():
    plt.rcParams.update({"font.family": "serif", "font.size": 7, "axes.titlesize": 7.5, "axes.labelsize": 7,
                         "xtick.labelsize": 6, "ytick.labelsize": 6, "legend.fontsize": 6,
                         "axes.edgecolor": MUTED, "axes.linewidth": 0.5, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.labelcolor": INK2, "pdf.fonttype": 42})


def load(ds, model, method):
    """Rows of the main run, restricted as in the paper tables: QA/Qasper drop the pilot qids;
    Symmetric FEVER keeps the evidence-dependent set; invalid reference draws are dropped."""
    d = os.path.join(RAW, ds, model, "main")
    p = os.path.join(d, f"{method}.jsonl")
    if not os.path.exists(p):
        return {}
    rows = {}
    for l in open(p):
        r = json.loads(l)
        rows[r["qid"]] = r
    if ds == "symfever":
        keep = set(json.load(open(os.path.join(ROOT, "results", "closed", "screen", "symfever", model,
                                                 "symfever.all.evidence_dep.json"))))
        rows = {q: r for q, r in rows.items() if q in keep}
    else:
        pq = os.path.join(RAW, ds, model, "pilot", "qids.json")
        dev = set(json.load(open(pq))) if os.path.exists(pq) else set()
        rows = {q: r for q, r in rows.items() if q not in dev}
    if method != "V1":
        rows = {q: r for q, r in rows.items() if r.get("baseline_answer") is not None}
    return rows


def p1_class(phi):
    p = np.asarray(phi, float)
    if not p.any():
        return "all zero"
    n = int(np.sum(np.isclose(p, p.max())))
    return "unique" if n == 1 else ("2-way tie" if n == 2 else "3+ tie")


def maps(out, model="claude-haiku-5-5", n=40, seed=0):
    cmap = LinearSegmentedColormap.from_list("div", [ORANGE, "#f6d2c2", "#f2f2f0", "#bcd5f3", BLUE])
    meths = [("V1", "V1"), ("P1", "P1"), ("LOI", "LOI"), ("RM64", "RM64")]
    sets = [("qasper", "Qasper"), ("symfever", "Sym. FEVER")]
    fig, axes = plt.subplots(len(sets), len(meths), figsize=(7.16, 4.3), sharey="row")
    for si, (ds, dlab) in enumerate(sets):
        R = {k: load(ds, model, k) for k, _ in meths}
        qs = sorted(set.intersection(*(set(v) for v in R.values())))
        random.Random(seed).shuffle(qs)
        qs = qs[:n]
        order = {"unique": 0, "2-way tie": 1, "3+ tie": 2, "all zero": 3}
        qs.sort(key=lambda q: (order[p1_class(R["P1"][q]["phi"])], q))
        for mi, (k, lab) in enumerate(meths):
            A = []
            for q in qs:
                r = R[k][q]
                g = r["gold"][0]
                phi = np.asarray(r["phi"], float)
                rest = [i for i in range(len(phi)) if i != g]
                A.append([phi[g]] + [phi[i] for i in rest])
            A = np.array(A)
            ax = axes[si][mi]
            ax.imshow(A, cmap=cmap, vmin=-1, vmax=1, aspect="auto", interpolation="nearest")
            ax.axvline(0.5, color=INK, linewidth=0.6)
            ax.set_xticks([0] + list(range(1, A.shape[1])))
            ax.set_xticklabels(["gold"] + [""] * (A.shape[1] - 1), fontsize=5.5)
            ax.tick_params(length=0)
            if si == 0:
                ax.set_title(lab, color=INK)
            if mi == 0:
                cls = [p1_class(R["P1"][q]["phi"]) for q in qs]
                bounds = [i for i in range(1, len(cls)) if cls[i] != cls[i - 1]]
                ticks, labels = [], []
                start = 0
                for b in bounds + [len(cls)]:
                    ticks.append((start + b - 1) / 2)
                    labels.append(f"P1 {cls[start]}")
                    start = b
                ax.set_yticks(ticks)
                ax.set_yticklabels(labels, fontsize=5.5)
                ax.set_ylabel(dlab, color=INK)
            for mi2 in range(len(meths)):
                cls = [p1_class(R["P1"][q]["phi"]) for q in qs]
                for i in range(1, len(cls)):
                    if cls[i] != cls[i - 1]:
                        axes[si][mi2].axhline(i - 0.5, color="white", linewidth=1.2)
            for sp in ax.spines.values():
                sp.set_visible(False)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(-1, 1))
    cb = fig.colorbar(sm, ax=axes, fraction=0.015, pad=0.01)
    cb.set_label("attribution score", fontsize=6)
    cb.ax.tick_params(labelsize=5.5)
    cb.outline.set_visible(False)
    fig.text(0.45, 0.005, "sources: gold first, then the other nine in context order", ha="center", fontsize=6, color=INK2)
    path = os.path.join(out, "fig_maps.pdf")
    fig.savefig(path, bbox_inches="tight")
    if os.environ.get("FIG_PREVIEW"):
        fig.savefig(os.path.join(os.environ["FIG_PREVIEW"], "fig_maps.png"), dpi=200, bbox_inches="tight")
    print("wrote", path, "model", model)


def dist(out):
    stats = {}
    fig, axes = plt.subplots(1, 3, figsize=(7.16, 1.9), gridspec_kw={"width_ratios": [1, 1, 1.25]})
    # (a) spontaneous changes of the unablated answer (P1's 3 extra full-context draws)
    seq = ["#dbe8f8", "#9ec3ec", "#4f93df", "#1d5bab"]
    cls_col = {"unique": BLUE, "2-way tie": "#f5b48f", "3+ tie": ORANGE, "all zero": "#c8c7c2"}
    labs = []
    A, Bc, G, NG = [], [], [], []
    for ds, lab in DATASETS:
        labs.append(lab)
        cnt = np.zeros(4)
        cc = {k: 0 for k in cls_col}
        g, ng = [], []
        for m in MODELS:
            P = load(ds, m, "P1")
            for r in P.values():
                fr = r["meta"].get("full_context_change_rate")
                if fr is not None:
                    cnt[int(round(fr * 3))] += 1
                cc[p1_class(r["phi"])] += 1
            Rm = load(ds, m, "RM64")
            for r in Rm.values():
                phi = np.asarray(r["phi"], float)
                for i, v in enumerate(phi):
                    (g if i in r["gold"] else ng).append(v)
        A.append(cnt / cnt.sum())
        Bc.append({k: v / sum(cc.values()) for k, v in cc.items()})
        G.append(g)
        NG.append(ng)
        stats[ds] = {"spont_dist": (cnt / cnt.sum()).round(3).tolist(), "p1_structure": {k: round(v, 3) for k, v in Bc[-1].items()},
                     "rm_gold_median": float(np.median(g)) if g else None, "rm_nongold_median": float(np.median(ng)) if ng else None}
    y = np.arange(len(labs))[::-1]
    ax = axes[0]
    left = np.zeros(len(labs))
    for k in range(4):
        v = np.array([a[k] for a in A])
        ax.barh(y, v, left=left, color=seq[k], edgecolor="white", linewidth=0.8, height=0.62,
                label=f"{k} of 3")
        left += v
    ax.set_yticks(y)
    ax.set_yticklabels(labs)
    ax.set_xlim(0, 1)
    ax.set_title("(a) unablated answer changes on re-ask", color=INK)
    ax.set_xlabel("share of instances")
    ax.legend(ncol=4, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.32), handlelength=1, columnspacing=0.6)
    ax = axes[1]
    left = np.zeros(len(labs))
    for k, col in cls_col.items():
        v = np.array([b[k] for b in Bc])
        ax.barh(y, v, left=left, color=col, edgecolor="white", linewidth=0.8, height=0.62, label=k)
        left += v
    ax.set_yticks(y)
    ax.set_yticklabels([])
    ax.set_xlim(0, 1)
    ax.set_title("(b) structure of P1's top set", color=INK)
    ax.set_xlabel("share of instances")
    ax.legend(ncol=4, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.32), handlelength=1, columnspacing=0.6)
    ax = axes[2]
    pos = np.arange(len(labs))
    vg = ax.violinplot([G[i] for i in range(len(labs))], positions=pos - 0.18, widths=0.32, showextrema=False, showmedians=True)
    vn = ax.violinplot([NG[i] for i in range(len(labs))], positions=pos + 0.18, widths=0.32, showextrema=False, showmedians=True)
    for body in vg["bodies"]:
        body.set_facecolor(BLUE); body.set_edgecolor(BLUE); body.set_alpha(0.55)
    for body in vn["bodies"]:
        body.set_facecolor("#c8c7c2"); body.set_edgecolor(MUTED); body.set_alpha(0.8)
    vg["cmedians"].set_color(INK); vn["cmedians"].set_color(INK)
    vg["cmedians"].set_linewidth(0.8); vn["cmedians"].set_linewidth(0.8)
    ax.axhline(0, color=MUTED, linewidth=0.5)
    ax.set_xticks(pos)
    ax.set_xticklabels(labs)
    ax.set_ylim(-1.05, 1.05)
    ax.set_title("(c) RM64 scores by source type", color=INK)
    ax.set_ylabel("Banzhaf score")
    ax.grid(axis="y", color=GRID, linewidth=0.5)
    ax.set_axisbelow(True)
    ax.legend(handles=[Patch(color=BLUE, alpha=0.55, label="gold"), Patch(color="#c8c7c2", label="non-gold")],
              ncol=2, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.32))
    for a in axes:
        for sp in ("top", "right"):
            a.spines[sp].set_visible(False)
    fig.tight_layout(w_pad=1.0)
    path = os.path.join(out, "fig_dist.pdf")
    fig.savefig(path, bbox_inches="tight")
    if os.environ.get("FIG_PREVIEW"):
        fig.savefig(os.path.join(os.environ["FIG_PREVIEW"], "fig_dist.png"), dpi=200, bbox_inches="tight")
    json.dump(stats, open(os.path.join(ROOT, "results", "closed", "analysis", "feature_dist.json"), "w"), indent=1)
    print("wrote", path)
    print(json.dumps(stats, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "..", "paper", "figures"))
    a = ap.parse_args()
    style()
    maps(a.out)
    dist(a.out)


if __name__ == "__main__":
    main()
