# Editable ICDE figure drafts

Source snapshot: [`dda344f`](https://github.com/GuihaiChen1998/probing-context-attribution-in-strict-blackbox-llm/tree/dda344f662409b48cf26f47d41df3725882d2c7a). The tracked paper and existing figures are the reference for these drafts.

## Overview

Open [fig_overview.drawio](fig_overview.drawio) in diagrams.net. It contains three editable pages with separate shapes, labels and arrows. The SVGs use the same source geometry.

| Style | SVG | Design |
| --- | --- | --- |
| Illustrated Modular | [Preview](fig_overview_editorial.svg) | Muted semantic modules, open line icons and darker contours. |
| Pastel Airy UI | [Preview](fig_overview_airy.svg) | Light dashed scope boundaries, floating cards and a dark ranking anchor. |
| Dual-Fidelity Loop | [Preview](fig_overview_dual.svg) | Blue cheap probe, coral escalation and an explicit unique-top gate. |

All three follow [§IV](https://github.com/GuihaiChen1998/probing-context-attribution-in-strict-blackbox-llm/blob/dda344f662409b48cf26f47d41df3725882d2c7a/paper/sections/04_methods.tex). A asks for source IDs. B removes or isolates one record and compares answers with the reference. C queries Bernoulli masks and contrasts the means with and without each record. B and C reuse one full-context reference. The optional route starts with LOI or P1 and adds RM@k when the probe has no unique maximum. Gold labels enter the offline evaluation box. The dual-fidelity design uses the visual language of two query budgets while retaining the one-step route in Algorithm 2.

**Suggested caption:** Estimator space for context attribution with text-only access. Self-report, single-source intervention and random-subset intervention all produce source scores. The optional query plan reuses the full-context reference and escalates from LOI or P1 to RM@k when the top score is tied.

## Performance and statistical figures

| Figure | Preview / editable | Inputs and interpretation |
| --- | --- | --- |
| Cost frontier | [SVG](fig_frontier_editable.svg) · [draw.io](fig_frontier_editable.drawio) | `29_paper_figures.py` loads `28_paper_tables.py` analysis JSON. This version uses each point's exact nominal cost on the log axis, including coincident costs for the single-source estimators. Points show tie-aware gold top-1 on the common valid set. The two Symmetric FEVER cells without RM are labelled. |
| Attribution score maps | [SVG](fig_maps_editable.svg) · [draw.io](fig_maps_editable.drawio) | `34_feature_figures.py` uses the shared Haiku V1/P1/LOI/RM64 rows, CPython seed 0, and 40 rows per dataset. All four estimator panels use the same rows and signed scale. Each gold source moves to the first column. Row group labels include group counts. |
| Answer changes, top sets and score distributions | [SVG](fig_dist_editable.svg) · [draw.io](fig_dist_editable.drawio) | `34_feature_figures.py` reads P1 full-context repeats, P1 score vectors and RM64 source scores. The stacked fractions and medians were independently matched to `feature_dist.json` at its published precision. The last panel replaces kernel-smoothed violins with empirical percentile intervals. The line spans the 5th–95th percentiles, the box spans the 25th–75th percentiles, and the marker is the median. Update the paper caption if substituting this panel. |
| End-to-end performance heatmap | [SVG](fig_heatmap_editable.svg) · [draw.io](fig_heatmap_editable.drawio) | `29_paper_figures.py` combines `paper.main.*.json` end-to-end metrics with `grid.test.json` for the grid variants. This is the diagnostic heatmap. A dash indicates a missing run. |

The statistical plots use the numeric chart design recommendations in [TingxiYu/academic-figure-skill](https://github.com/TingxiYu/academic-figure-skill). Markers and line styles accompany method colors. [figure_inputs.json](figure_inputs.json) records the exact plotted values, including maps row IDs and the distribution denominators. From this folder, run `node render_figures.cjs` to rebuild all SVG and draw.io outputs. The uncompressed draw.io XML uses the format documented by [bruce-drawio](https://github.com/bruc3van/bruce-drawio).

The draft XML was checked for balanced tags, valid entities, known connector endpoints and in-bounds geometry. Open the files in diagrams.net to check the final font rendering and export PDF for LaTeX.

## Upstream tools

The requested tools were identified at pinned upstream snapshots. Installation was blocked by the unavailable execution environment. The draft renderer uses the checked figure specifications and raw repository outputs directly.

| Repository | Upstream version or commit | Package form |
| --- | --- | --- |
| [c-narcissus/paper-framework-figure-studio-pro](https://github.com/c-narcissus/paper-framework-figure-studio-pro) | `7755741` | v3.2.15f skill ZIP for ChatGPT Web |
| [deermiya/visio-skill](https://github.com/deermiya/visio-skill) | `04c6d49` | Visio skill, Windows/Visio required for native export |
| [bruc3van/bruce-drawio](https://github.com/bruc3van/bruce-drawio) | `ac561a0` | Draw.io skill and XML/export helpers |
| [Haojae/scipilot-figure-skill](https://github.com/Haojae/scipilot-figure-skill) | `43098dd` | Scientific figure skill |
| [TingxiYu/academic-figure-skill](https://github.com/TingxiYu/academic-figure-skill) | `1df9940` | Scientific figure skill and Codex adapter |
| [Azhi-ss/academic-figure-skills](https://github.com/Azhi-ss/academic-figure-skills) | `73545d2` | fig-analyze, fig-draw, fig-pptx skills |
| [Galaxy-Dawn/pubfig](https://github.com/Galaxy-Dawn/pubfig) | `4eec116` | Python package |

The [original installation script](https://github.com/GuihaiChen1998/probing-context-attribution-in-strict-blackbox-llm/blob/dda344f662409b48cf26f47d41df3725882d2c7a/code/scripts/install_figure_skills.sh) targets the Claude executor paths. A persistent installation in this workspace needs the corresponding personal skill installation flow and a working executor.
