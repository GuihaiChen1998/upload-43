#!/usr/bin/env python3
"""fig3: gap (verbalize - perturbation top-1) vs model scale.

All four family x dataset lines on one axis. The gap tends to shrink with scale
but not universally: three trends decrease monotonically, Qwen3/HotpotQA is
non-monotonic (peaks at 4B). Plotting all four makes "a trend with a stated
exception" legible. See Sec. 6.3.

Gemma-3-1B is drawn as a hollow grey marker and NOT connected into the trend:
its verbalize channel collapses to chance (Sec. 6.6), so its gap is an artifact
of a broken self-report channel, not a comparable point.

  python scripts/06b_fig_gap_vs_scale.py
"""
import csv, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

COL = {"qwen3": "#127475", "gemma3": "#c1452d"}
DS_STYLE = {
    "musique":  dict(ls="-",  marker="o", ds_label="MuSiQue"),
    "hotpotqa": dict(ls="--", marker="s", ds_label="HotpotQA-bridge"),
}
FAM_LABEL = {"qwen3": "Qwen3", "gemma3": "Gemma-3"}
COLLAPSE = {("gemma3", 1.0)}


def load_rows(path):
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            if not r.get("params_b") or r["model"] == "_baselines":
                continue
            try:
                rows.append(dict(
                    dataset=r["dataset"], family=r["family"],
                    params=float(r["params_b"]),
                    gap=float(r["best_v_top1"]) - float(r["best_p_top1"])))
            except ValueError:
                continue
    return rows


def main():
    rows = load_rows("results/tables/scale.csv")
    if not rows:
        print("no scale.csv rows; run 05 first"); return

    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    for family in ("qwen3", "gemma3"):
        for dataset, st in DS_STYLE.items():
            pts = sorted([r for r in rows if r["family"] == family
                          and r["dataset"] == dataset], key=lambda r: r["params"])
            trend = [r for r in pts if (r["family"], r["params"]) not in COLLAPSE]
            boundary = [r for r in pts if (r["family"], r["params"]) in COLLAPSE]
            if trend:
                ax.plot([r["params"] for r in trend], [r["gap"] for r in trend],
                        color=COL[family], ls=st["ls"], marker=st["marker"],
                        markersize=7, linewidth=2, zorder=3)
                for r in trend:
                    dy = 8 if family == "qwen3" else -12
                    ax.annotate(f"{r['gap']:+.3f}", (r["params"], r["gap"]),
                                fontsize=6.5, xytext=(0, dy),
                                textcoords="offset points", ha="center",
                                color=COL[family])
            # Gemma-3-1B gap is about -0.54 (verbalize collapsed); plotting it
            # to scale would squash the four trend lines. Mark its position at
            # the axis floor with an arrow and a note instead.
            for r in boundary:
                ax.annotate("Gemma-3-1B: verbalize collapses to chance,\n"
                            "gap $\\approx -0.54$, excluded from trend (Sec. 6.6)",
                            xy=(r["params"], 0.0), xytext=(1.15, 0.04),
                            fontsize=6, color="grey", va="bottom", ha="left",
                            arrowprops=dict(arrowstyle="->", color="grey", lw=0.8))

    ax.axhline(0, color="#999999", lw=0.8, ls=":", zorder=1)
    ax.set_xscale("log")
    ax.set_xticks([1, 1.7, 4, 8, 12])
    ax.set_xticklabels(["1B", "1.7B", "4B", "8B", "12B"])
    ax.set_xlabel("model size (log scale)")
    ax.set_ylabel(r"gap  (verbalize $-$ perturbation top-1)")
    ax.set_title("Gap vs scale: shrinks in 3 of 4 trends;\n"
                 "Qwen3/HotpotQA is the exception (peaks at 4B)", fontsize=10)
    ax.set_ylim(0.0, 0.30)
    ax.grid(True, ls=":", alpha=0.35, zorder=0)

    fam_handles = [Line2D([0], [0], color=COL[f], lw=2.5, label=FAM_LABEL[f])
                   for f in ("qwen3", "gemma3")]
    ds_handles = [Line2D([0], [0], color="#555555", lw=2, ls=DS_STYLE[d]["ls"],
                         marker=DS_STYLE[d]["marker"], label=DS_STYLE[d]["ds_label"])
                  for d in DS_STYLE]
    leg1 = ax.legend(handles=fam_handles, title="family", loc="upper left",
                     bbox_to_anchor=(1.02, 1.0), fontsize=8, title_fontsize=8,
                     frameon=False)
    ax.add_artist(leg1)
    ax.legend(handles=ds_handles, title="dataset", loc="upper left",
              bbox_to_anchor=(1.02, 0.58), fontsize=8, title_fontsize=8,
              frameon=False)

    fig.tight_layout()
    os.makedirs("results/figures", exist_ok=True)
    out = "results/figures/fig3_gap_vs_scale.pdf"
    fig.savefig(out, bbox_inches="tight")
    print(f"wrote {out}")
    for family in ("qwen3", "gemma3"):
        for dataset in DS_STYLE:
            g = [r["gap"] for r in sorted(
                [r for r in rows if r["family"] == family and r["dataset"] == dataset
                 and (r["family"], r["params"]) not in COLLAPSE],
                key=lambda r: r["params"])]
            if g:
                mono = "shrinks" if all(a > b for a, b in zip(g, g[1:])) else "NON-monotonic"
                print(f"  {family:8s} {dataset:16s} {[f'{x:+.3f}' for x in g]} {mono}")


if __name__ == "__main__":
    main()
