#!/usr/bin/env python3
"""Render the paper's figures from results/tables/*.csv -- paper Sec. 6.

  Figure 2  accuracy vs query cost (the core cost-accuracy tradeoff)
  Figure 3  scale trend, two families, parse-fail on a twin axis
  Figure 4  (a) verbalize/perturbation disagreement  (b) empty-pred by hop

Reads only CSVs, so it is decoupled from any model run. Colours follow the
paper convention: teal = verbalize, coral = perturbation, grey = reference.

  python scripts/06_make_figures.py --dataset hotpotqa
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TEAL = "#127475"
CORAL = "#e8604c"
GREY = "#8a8a8a"
LIGHT_TEAL = "#7fb3b3"
MIDGREY = "#c4c4c4"


def read_csv(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def fig2_cost_accuracy(tables, out_dir, dataset, subset="full"):
    """Accuracy vs query cost. Log-x. Verbalize clusters cheap-left,
    perturbation pays ~an order of magnitude more; upper-left is better.

    Methods within a paradigm share a colour family and are distinguished by
    shade (light->dark with method index), so the seven verbalize and five
    perturbation points stay readable without per-point text labels that would
    collide where costs coincide (V1/V3/V6 all cost 1 query). A small horizontal
    jitter separates exactly-overlapping points; the legend carries the method
    identities.
    """
    import numpy as np
    from matplotlib.lines import Line2D
    import matplotlib.colors as mcolors

    rows = [r for r in read_csv(os.path.join(tables, "main_results.csv"))
            if r["dataset"] == dataset
            and r.get("subset", "full") == subset]
    if not rows:
        return
    models = sorted({r["model"] for r in rows}, key=lambda m: _f(
        next((x["params_b"] for x in rows if x["model"] == m), 0) or 0))
    model = models[-1]
    sub = [r for r in rows if r["model"] == model]

    def shades(base_hex, n):
        # n shades from light to full-strength of the base colour
        base = np.array(mcolors.to_rgb(base_hex))
        white = np.array([1, 1, 1])
        return [tuple(white + (base - white) * f)
                for f in np.linspace(0.45, 1.0, n)]

    v_methods = [f"V{i}" for i in range(1, 8)]
    p_methods = [f"P{i}" for i in range(1, 6)]
    v_sh = dict(zip(v_methods, shades(TEAL, len(v_methods))))
    p_sh = dict(zip(p_methods, shades(CORAL, len(p_methods))))

    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    # group points by rounded (cost, acc) to apply jitter only where they collide
    seen = {}
    for r in sub:
        c = _f(r["mean_query_cost"]); acc = _f(r["top1_accuracy"])
        if c is None or acc is None or c <= 0:
            continue
        is_v = r["method"].startswith("V")
        key = (round(c, 2), round(acc, 3))
        k = seen.get(key, 0); seen[key] = k + 1
        jitter = 1.0 + 0.06 * k  # multiplicative on log-x
        col = v_sh.get(r["method"], TEAL) if is_v else p_sh.get(r["method"], CORAL)
        ax.scatter(c * jitter, acc, s=85,
                   color=col, marker="o" if is_v else "s",
                   edgecolors="#333333", linewidths=0.6, zorder=3)

    rb = _f(sub[0]["random_baseline_top1"])
    if rb:
        ax.axhline(rb, ls="--", c=GREY, lw=1, zorder=1)
        ax.text(0.02, rb + 0.01, "random", va="bottom", ha="left",
                fontsize=7, c=GREY, transform=ax.get_yaxis_transform())

    ax.set_xscale("log")
    ax.set_xlabel("queries per instance (log scale)")
    ax.set_ylabel("top-1 accuracy")
    tag = "" if subset == "full" else f" ({subset})"
    ax.set_title(f"Cost vs accuracy — {model} / {dataset}{tag}", fontsize=10)

    # Legend: method identities by shade, two columns (verbalize / perturbation),
    # placed OUTSIDE the axes on the right so no point is obscured.
    v_handles = [Line2D([], [], marker="o", ls="", color=v_sh[m],
                        markeredgecolor="#333333", markersize=7, label=m)
                 for m in v_methods]
    p_handles = [Line2D([], [], marker="s", ls="", color=p_sh[m],
                        markeredgecolor="#333333", markersize=7, label=m)
                 for m in p_methods]
    leg1 = ax.legend(handles=v_handles, title="verbalize", loc="upper left",
                     bbox_to_anchor=(1.02, 1.0), fontsize=7, title_fontsize=8,
                     frameon=False, handletextpad=0.3)
    ax.add_artist(leg1)
    ax.legend(handles=p_handles, title="perturbation", loc="upper left",
              bbox_to_anchor=(1.02, 0.42), fontsize=7, title_fontsize=8,
              frameon=False, handletextpad=0.3)
    ax.grid(True, which="both", ls=":", alpha=0.4)
    fig.tight_layout()
    suffix = "" if subset == "full" else f"_{subset}"
    p = os.path.join(out_dir, f"fig2_cost_accuracy_{dataset}{suffix}.pdf")
    fig.savefig(p, bbox_inches="tight"); plt.close(fig)
    print(f"wrote {p}")


def fig3_scale(tables, out_dir, dataset):
    """Two family trend lines (solid, top-1) with parse-fail on a twin axis
    (dashed). A high dashed line at the small end explains a low solid one:
    the failure is format-following, not attribution."""
    rows = [r for r in read_csv(os.path.join(tables, "scale.csv"))
            if r["dataset"] == dataset]
    if not rows:
        return
    fams = defaultdict(list)
    for r in rows:
        if _f(r["params_b"]) is not None:
            fams[r["family"]].append(r)

    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    ax2 = ax.twinx()
    colors = {"qwen3": TEAL, "gemma3": CORAL}
    for fam, frows in fams.items():
        frows.sort(key=lambda r: _f(r["params_b"]))
        xs = [_f(r["params_b"]) for r in frows]
        acc = [_f(r["best_p_top1"]) if r["best_p_top1"] else None for r in frows]
        pf = [_f(r["parse_failure_rate"]) for r in frows]
        col = colors.get(fam, GREY)
        ax.plot(xs, acc, "-o", color=col, label=f"{fam} top-1", zorder=3)
        ax2.plot(xs, pf, "--^", color=col, alpha=0.5, markersize=4,
                 label=f"{fam} parse-fail", zorder=2)

    ax.set_xscale("log")
    ax.set_xlabel("parameters (B, log scale)")
    ax.set_ylabel("top-1 accuracy (solid)")
    ax2.set_ylabel("parse failure rate (dashed)")
    ax.set_title(f"Effect of scale — {dataset}", fontsize=10)
    ax.grid(True, which="both", ls=":", alpha=0.4)
    lines = ax.get_legend_handles_labels()[0] + ax2.get_legend_handles_labels()[0]
    labels = ax.get_legend_handles_labels()[1] + ax2.get_legend_handles_labels()[1]
    ax.legend(lines, labels, fontsize=7, loc="best")
    fig.tight_layout()
    p = os.path.join(out_dir, f"fig3_scale_{dataset}.pdf")
    fig.savefig(p, bbox_inches="tight"); plt.close(fig)
    print(f"wrote {p}")


def fig4_combined(tables, out_dir, dataset):
    """Two unrelated panels combined for space (state this in the caption):
    (a) verbalize/perturbation disagreement, (b) empty-pred vs hop (MuSiQue)."""
    agr = [r for r in read_csv(os.path.join(tables, "agreement.csv"))
           if r["dataset"] == dataset]
    hop = read_csv(os.path.join(tables, "failure_by_hop.csv"))
    if not agr and not hop:
        return

    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.6))

    # (a) stacked horizontal bars per model
    axa = axes[0]
    if agr:
        agr.sort(key=lambda r: (_f(r["params_b"]) or 0))
        labels = [r["model"] for r in agr]
        segs = ["both_correct", "only_p", "only_v",
                "both_wrong_same", "both_wrong_diff"]
        seg_c = [TEAL, CORAL, LIGHT_TEAL, MIDGREY, "#e6e6e6"]
        seg_lab = ["both correct", "only perturb.", "only verbalize",
                   "both wrong, same", "both wrong, diff"]
        y = range(len(agr))
        left = [0.0] * len(agr)
        for seg, c, lab in zip(segs, seg_c, seg_lab):
            vals = []
            for r in agr:
                n = float(r["n"]) or 1
                vals.append(float(r.get(seg, 0)) / n)
            axa.barh(list(y), vals, left=left, color=c, label=lab, height=0.7)
            left = [l + v for l, v in zip(left, vals)]
        axa.set_yticks(list(y)); axa.set_yticklabels(labels, fontsize=8)
        axa.set_xlabel("fraction of instances")
        axa.set_xlim(0, 1)
        axa.set_title("(a) verbalize vs perturbation", fontsize=10)
        # Legend below the panel, anchored low enough to clear the x-axis label;
        # extra bottom margin is reserved via subplots_adjust after plotting so
        # it never overlaps the title or the neighbouring panel.
        axa.legend(fontsize=6.5, loc="upper center", bbox_to_anchor=(0.5, -0.22),
                   ncol=3, frameon=False, columnspacing=1.0, handletextpad=0.4)

    # (b) empty-pred by hop, with random baseline overlaid
    axb = axes[1]
    if hop:
        by_model = defaultdict(list)
        for r in hop:
            by_model[r["model"]].append(r)
        for model, rs in by_model.items():
            rs.sort(key=lambda r: int(r["n_hop"]))
            xs = [int(r["n_hop"]) for r in rs]
            ep = [_f(r["empty_prediction_rate"]) for r in rs]
            axb.plot(xs, ep, "-o", color=CORAL, label=f"{model} empty-pred")
        # one representative random baseline line
        rs0 = sorted(next(iter(by_model.values())), key=lambda r: int(r["n_hop"]))
        axb.plot([int(r["n_hop"]) for r in rs0],
                 [_f(r["random_baseline_top1"]) for r in rs0],
                 "--", color=GREY, label="random top-1")
        axb.set_xlabel("hop count")
        axb.set_ylabel("rate")
        axb.set_xticks(sorted({int(r["n_hop"]) for r in hop}))
        axb.set_title("(b) empty prediction vs hops", fontsize=10)
        axb.legend(fontsize=7, loc="best")
        axb.grid(True, ls=":", alpha=0.4)
    else:
        axb.text(0.5, 0.5, "MuSiQue only", ha="center", va="center")
        axb.axis("off")

    fig.tight_layout()
    # Reserve space at the bottom for panel (a)'s legend placed below its axis.
    fig.subplots_adjust(bottom=0.24)
    p = os.path.join(out_dir, f"fig4_combined_{dataset}.pdf")
    fig.savefig(p, bbox_inches="tight"); plt.close(fig)
    print(f"wrote {p}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tables", default="results/tables")
    ap.add_argument("--out-dir", default="results/figures")
    ap.add_argument("--dataset", default="hotpotqa")
    ap.add_argument("--subsets", nargs="+", default=["full", "context_dep"],
                    help="which evaluation subsets to plot, if present")
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    for sub in args.subsets:
        fig2_cost_accuracy(args.tables, args.out_dir, args.dataset, subset=sub)
    fig3_scale(args.tables, args.out_dir, args.dataset)
    fig4_combined(args.tables, args.out_dir, args.dataset)
    print("\ndone.")


if __name__ == "__main__":
    main()
