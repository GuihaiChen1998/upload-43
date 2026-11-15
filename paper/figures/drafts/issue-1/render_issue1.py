"""Render the two issue #1 figure drafts as vector PDF and SVG."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle


HERE = Path(__file__).resolve().parent
INK = "#182735"
MUTED = "#485866"
EDGE = "#c4cfd7"
BLUE = "#2a78d6"
ORANGE = "#c85023"
GOLD = "#a57914"
PALETTE = [BLUE, "#13805d", "#ce9011", "#eb6834"]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
})


def canvas(width, height):
    fig = plt.figure(figsize=(width, height), facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1], xlim=(0, width), ylim=(height, 0))
    ax.set_axis_off()
    return fig, ax


def text(ax, x, y, value, size=6.5, color=INK, weight="normal", ha="left"):
    return ax.text(
        x, y, value, fontsize=size, color=color, weight=weight,
        ha=ha, va="center", linespacing=1.24,
    )


def box(ax, x, y, w, h, fill="white", edge=EDGE, lw=0.6):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0,rounding_size=0.045",
        facecolor=fill, edgecolor=edge, linewidth=lw,
    ))


def arrow(ax, x1, y1, x2, y2, color=MUTED):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=6,
        linewidth=0.7, color=color, shrinkA=0, shrinkB=0,
    ))


def record(ax, x, y, label, *, deleted=False, w=0.17, h=0.16):
    box(ax, x, y, w, h, "#f1f3f5" if deleted else "white")
    text(ax, x + w / 2, y + h / 2, label, 5.7, MUTED if deleted else INK, ha="center")
    if deleted:
        ax.plot([x + 0.027, x + w - 0.027], [y + h - 0.02, y + 0.02],
                color=ORANGE, lw=0.9, zorder=4)


def export(fig, stem, title):
    fig.savefig(HERE / (stem + ".pdf"), metadata={"Title": title, "CreationDate": None})
    fig.savefig(HERE / (stem + ".svg"), metadata={"Title": title, "Date": None})
    plt.close(fig)


def motivation():
    fig, ax = canvas(3.50, 2.24)
    text(ax, 1.75, 0.135, "Which records did the model use?", 8.4, weight="bold", ha="center")
    box(ax, 0.09, 0.31, 0.43, 0.31, "#f5f7f9")
    text(ax, 0.305, 0.465, "Query", 7, ha="center")
    arrow(ax, 0.55, 0.465, 0.69, 0.465)
    for n in range(4):
        record(ax, 0.73 + n * 0.19, 0.385, f"[{n + 1}]")
    arrow(ax, 1.51, 0.465, 1.67, 0.465)
    box(ax, 1.70, 0.31, 1.03, 0.31, "#e8edf1")
    text(ax, 2.215, 0.465, "LLM API · text only", 6.7, weight="bold", ha="center")
    arrow(ax, 2.76, 0.465, 2.91, 0.465)
    box(ax, 2.94, 0.31, 0.47, 0.31, "#f5f7f9")
    text(ax, 3.175, 0.465, "Answer", 6.8, ha="center")

    box(ax, 0.09, 0.76, 1.17, 0.86, "#edf5ff", "#9ebfe6")
    text(ax, 0.19, 0.90, "Saying", 8.5, BLUE, "bold")
    text(ax, 0.19, 1.045, "Ask the model", 7.1)
    box(ax, 0.19, 1.15, 0.84, 0.22, "white", "#b8cde4")
    text(ax, 0.61, 1.26, "“I used [2].”", 7.7, BLUE, ha="center")
    text(ax, 0.19, 1.49, "V1 · 1 call", 6.7, BLUE, "bold")

    box(ax, 1.35, 0.76, 2.06, 0.86, "#fff5ed", "#e3b69f")
    text(ax, 1.46, 0.90, "Doing", 8.5, ORANGE, "bold")
    text(ax, 1.92, 0.90, "Intervene on the context", 6.9)
    for row, deleted in enumerate((1, 2, 3)):
        y = 0.99 + row * 0.155
        for n in range(1, 5):
            record(ax, 1.48 + (n - 1) * 0.195, y, f"[{n}]", deleted=n == deleted,
                   h=0.135)
        arrow(ax, 2.28, y + 0.068, 2.46, y + 0.068)
        changed = deleted == 2
        ax.add_patch(Circle((2.55, y + 0.068), 0.026, edgecolor=ORANGE,
                            facecolor=ORANGE if changed else "white", linewidth=0.75))
        text(ax, 2.62, y + 0.068, "changed" if changed else "unchanged", 6.6)
    text(ax, 1.46, 1.51, "LOO  M+1  ·  RM@k  ≤k+1 calls", 6.75, ORANGE, "bold")

    for x, head, lines in [
        (0.09, "Redundancy", "A copy remains after deletion.\nThe answer can stay the same."),
        (1.80, "Answer variation", "A distractor is removed.\nRephrasing can count as change."),
    ]:
        box(ax, x, 1.72, 1.61, 0.45, "#f6f8fa")
        text(ax, x + 0.085, 1.83, head, 7.0, weight="bold")
        text(ax, x + 0.085, 2.015, lines, 5.85, color=MUTED)

    export(fig, "fig_motivation", "Text-only API provenance probes")


def worked_examples():
    data = json.loads((HERE / "worked_examples.json").read_text())
    fig, ax = canvas(7.15, 2.78)
    for i, example in enumerate(data["examples"]):
        x = 0.04 + i * 2.385
        box(ax, x, 0.04, 2.30, 2.44, "#f8fafb", EDGE)
        text(ax, x + 0.11, 0.185, f"({example['letter']}) {example['title']}",
             7.75, weight="bold")
        text(ax, x + 0.11, 0.34, f"{example['tag']}  ·  {example['model']}", 6.35, MUTED)
        questions = {
            "a": "Who animated the TV anime\nadaptation of Dies irae?",
            "b": "Claim: Exercise temporarily\nincreases the heart rate.",
            "c": "Which dataset is used for\nheadline generation?",
        }
        text(ax, x + 0.11, 0.565, questions[example["letter"]], 7.1)
        text(ax, x + 0.11, 0.785, f"Reference  {example['baseline']}", 6.75, weight="bold")

        for j, source in enumerate(example["sources"]):
            cy = (1.07 + j * 0.425) if len(example["sources"]) == 3 else (1.165 + j * 0.555)
            box(ax, x + 0.10, cy - 0.186, 1.00, 0.373, "white")
            if source["gold"]:
                ax.plot([x + 0.106, x + 0.106], [cy - 0.123, cy + 0.123],
                        color=GOLD, lw=2.2, solid_capstyle="round")
            key = f"[{source['id']}]" + (" ★" if source["gold"] else "")
            text(ax, x + 0.16, cy - 0.115, key, 6.6, GOLD if source["gold"] else INK, "bold")
            text(ax, x + 0.16, cy + 0.047, source["label"], 5.55)
            zero = x + 1.51
            scale = 0.52
            ax.plot([zero, zero], [cy - 0.153, cy + 0.153], color="#7a8895", lw=0.55)
            for k, method in enumerate(data["methods"]):
                val = example["scores"][k][j]
                y = cy + (k - 1.5) * 0.077
                text(ax, x + 1.17, y, method, 5.3, MUTED)
                if val:
                    ax.add_patch(Rectangle(
                        (zero + min(0, val) * scale, y - 0.018), abs(val) * scale,
                        0.036, linewidth=0, facecolor=PALETTE[k], zorder=3,
                    ))
                else:
                    ax.add_patch(Circle((zero, y), 0.016, facecolor=PALETTE[k],
                                        edgecolor="none", zorder=3))
                shown = f"{val:.2f}" if method == "RM64" else f"{val:.0f}"
                text(ax, x + 2.22, y, shown.replace("-", "−"), 5.8, ha="right")

        ax.plot([x + 0.11, x + 2.19], [2.17, 2.17], color=EDGE, lw=0.6)
        text(ax, x + 0.11, 2.315, "\n".join(example["footer"]), 6.75, MUTED)

    text(ax, 0.15, 2.632, "★ Annotated support", 6.65, GOLD, "bold")
    for k, (method, color) in enumerate(zip(data["methods"], PALETTE)):
        x = 1.65 + k * 0.67
        ax.add_patch(Rectangle((x, 2.608), 0.14, 0.048, color=color, linewidth=0))
        text(ax, x + 0.20, 2.632, method, 6.65, MUTED)
    text(ax, 6.98, 2.632, "Selected records · shared score scale", 6.65, MUTED, ha="right")
    export(fig, "fig_worked_examples", "Three worked source attribution examples")


if __name__ == "__main__":
    motivation()
    worked_examples()
