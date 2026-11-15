#!/usr/bin/env python3
"""fig1/main: cost-accuracy scatter, one panel per dataset, all five valid
models and all twelve methods.

Replaces the large numeric main-results table in the body (the full table moves
to the appendix). Carries the same information the table did -- every method x
model top-1, plus query cost and the retrieval baselines -- but arranges it so the
three structural facts are visible at a glance rather than read out of 60 cells:
(1) verbalize (circles) sits high and cheap-left, perturbation (squares) low and
expensive-right -- the paradigm gap and the order-of-magnitude cost gap; (2)
colour tracks model, so within-paradigm method spread (small) vs. between-paradigm
spread (large) is immediate; (3) BM25/embedding baselines are horizontal
references.

  python scripts/06c_fig_main_results.py
"""
import csv, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

MODELS = ["qwen3-1.7b","qwen3-4b","qwen3-8b","gemma3-4b","gemma3-12b"]
MDISP  = {"qwen3-1.7b":"Qwen3-1.7B","qwen3-4b":"Qwen3-4B","qwen3-8b":"Qwen3-8B",
          "gemma3-4b":"Gemma-3-4B","gemma3-12b":"Gemma-3-12B"}
# colourblind-safe qualitative palette
MCOL = {"qwen3-1.7b":"#0072B2","qwen3-4b":"#009E73","qwen3-8b":"#56B4E9",
        "gemma3-4b":"#E69F00","gemma3-12b":"#D55E00"}
DATASETS=[("musique","MuSiQue ($M\\approx20$)"),("hotpotqa","HotpotQA ($M\\approx10$)")]

def ff(x):
    try: return float(x)
    except: return None

def theo_cost(method, M):
    sp = method in ("V3","V4","V5","P3","P4","P5")
    k = 2 if sp else 1
    if method.startswith("V"):
        N = 5 if method in ("V2","V4","V5","V7") else 1
        return N*k
    N = 3 if method in ("P2","P4","P5") else 1
    return (M*N+1)*k

def load():
    return [r for r in csv.DictReader(open("results/tables/main_results.csv"))]

def get(rows, ds, model, method, col="top1_accuracy"):
    for r in rows:
        if r["dataset"]==ds and r["model"]==model and r["method"]==method:
            return ff(r[col])
    return None

def baseline(rows, ds, name):
    for r in rows:
        if r["dataset"]==ds and r["model"]=="_baselines" and r["method"]==name:
            return ff(r["top1_accuracy"])
    return None

def main():
    rows=load()
    methods=[f"V{i}" for i in range(1,8)]+[f"P{i}" for i in range(1,6)]
    fig,axes=plt.subplots(1,2,figsize=(9.6,4.2),sharey=True)

    for ax,(ds,dtitle) in zip(axes,DATASETS):
        M = 20 if ds=="musique" else 10
        # jitter cost slightly per model so overlapping method-points separate
        for mi,model in enumerate(MODELS):
            for meth in methods:
                v=get(rows,ds,model,meth)
                if v is None: continue
                c=theo_cost(meth,M)
                jit=1.0+0.045*(mi-2)  # spread models around the shared cost
                is_v=meth.startswith("V")
                ax.scatter(c*jit, v, s=46,
                           color=MCOL[model],
                           marker="o" if is_v else "s",
                           edgecolors="white", linewidths=0.5,
                           alpha=0.9, zorder=3)
        # baselines
        for name,ls,lab in [("bm25",":","BM25"),("embedding","--","Embed.")]:
            b=baseline(rows,ds,name)
            if b is not None:
                ax.axhline(b, color="#888888", ls=ls, lw=1.0, zorder=1)
                ax.text(ax.get_xlim()[1]*0.62, b+0.008, lab, fontsize=6.5,
                        color="#666666", va="bottom")
        rb = 0.118 if ds=="musique" else 0.204
        ax.axhline(rb, color="#cccccc", ls="-", lw=0.8, zorder=1)
        ax.text(1.0, rb+0.006, "random", fontsize=6.5, color="#999999", va="bottom")

        ax.set_xscale("log")
        ax.set_xlabel("queries per instance (log scale)")
        ax.set_title(dtitle, fontsize=10)
        ax.grid(True, which="both", ls=":", alpha=0.3, zorder=0)
        ax.set_ylim(0.05, 1.0)
    axes[0].set_ylabel("top-1 attribution accuracy")

    # shared legends outside on the right: models (colour) and paradigm (shape)
    model_handles=[Line2D([],[],marker="o",ls="",color=MCOL[m],markeredgecolor="white",
                          markersize=7,label=MDISP[m]) for m in MODELS]
    para_handles=[Line2D([],[],marker="o",ls="",color="#444444",markersize=7,label="verbalize"),
                  Line2D([],[],marker="s",ls="",color="#444444",markersize=7,label="perturbation")]
    leg1=fig.legend(handles=model_handles, title="model", loc="center left",
                    bbox_to_anchor=(0.99,0.62), fontsize=7.5, title_fontsize=8, frameon=False)
    fig.add_artist(leg1)
    fig.legend(handles=para_handles, title="paradigm", loc="center left",
               bbox_to_anchor=(0.99,0.30), fontsize=7.5, title_fontsize=8, frameon=False)

    fig.tight_layout(rect=[0,0,0.88,1])
    os.makedirs("results/figures",exist_ok=True)
    out="results/figures/fig_main_results.pdf"
    fig.savefig(out,bbox_inches="tight"); 
    print(f"wrote {out}")

if __name__=="__main__":
    main()
