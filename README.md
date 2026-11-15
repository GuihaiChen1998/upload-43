# Saying versus Doing: Context Attribution in Strictly Black-Box LLMs

Artifact for the ICDE 2027 Experiment, Analysis & Benchmark paper. It benchmarks estimators of
*which retrieved sources an LLM answer came from* when the model is reachable only through a
text-only chat API: self-report (asking the model) against interventions (leave-one-out,
leave-one-in, random-subset masks scored by the Banzhaf value), on five commercial models and four
datasets (HotpotQA, MuSiQue, Symmetric FEVER, Qasper).

The repository has two branches:

| Branch | Content |
|---|---|
| `main` | code, constructed datasets, per-instance results with run manifests, analysis outputs, generated LaTeX tables and figures |
| `cache-snapshots` | the response cache behind every reported run (1,503,800 responses, zstd-compressed, ~215 MB) |

## 1. Setup

Python 3.10 or newer (tested with 3.13). Clone `main` only; the cache branch is fetched on demand.

```bash
git clone --single-branch --branch main https://github.com/GuihaiChen1998/upload-43
cd upload-43
python -m venv .venv && source .venv/bin/activate
pip install -r code/requirements-reproduce.txt     # numpy, scipy, pyyaml, matplotlib, zstandard
```

`code/requirements-reproduce.txt` is enough for everything that makes no model calls (Sections 2
and 3). To issue new calls (Section 4) also install `openai tqdm` (`pip install openai tqdm`).
`code/requirements.txt` is the full set of the earlier open-model study (vLLM, gray-box baselines).

Optional sanity check of the estimators and aggregation code (no network, under a second):

```bash
pip install pytest tqdm
python -m pytest -q code/tests        # 39 passed
```

## 2. Reproduce the paper (no API calls, no keys)

```bash
python code/scripts/reproduce_all.py              # every analysis file and LaTeX table (~10 min on 1 CPU)
python code/scripts/reproduce_all.py --figures    # + re-render the data figures (needs node >= 18, rsvg-convert)
git status                                        # nothing should differ from the committed outputs
```

Every number in the paper comes from the per-instance result files under
`code/results/closed/raw/<dataset>/<model>/<tag>/<method>.jsonl`, which store, per instance, the
score vector, the gold sources, the reference answer and every answer the estimator observed
(ablated, single-source and mask answers). Analyses read only these files, so this step needs
neither the cache nor any key. `reproduce_all.py` runs, in order:

| Step | Writes | Paper |
|---|---|---|
| `28_paper_tables.py` (four calls, one per dataset slice) | `analysis/paper.main.*.{json,md}` | main results, coverage, routing (Sec. VI) |
| `18_analyze_closed.py --tag grid / grid_sub` | `analysis/grid*.{json,md}` | method grid |
| `21_analyze_k3.py` (luna, flash-lite) | `analysis/k3pilot_v2.*.{json,md}` | exact-copy control |
| `31_hop_depth.py`, `32_string_baseline.py` | `analysis/hop_depth.*`, `analysis/string_baseline.*` | hop depth, answer-string baseline |
| `36_review_audit.py`, `39_analyze_probes.py` | `analysis/review_audit.*`, `analysis/review_probes.json` | alignment, mask variability, equivalence, routing triggers, failure probes |
| `34_feature_figures.py` | `analysis/feature_dist.json` | input of the distribution figure |
| `29_paper_figures.py --only main,k3,review` | `paper/tables/tab_main.tex`, `tab_k3.tex`, `tab_review.tex` | LaTeX tables |
| `40_open_models_table.py` | `paper/tables/tab_open.tex` | open-weight models of the earlier study, gray-box check |

(`analysis/` stands for `code/results/closed/analysis/`.) Each script can also be run on its own
from `code/`, e.g. `cd code && python scripts/28_paper_tables.py --tag main --split test`. Scripts
that read the HotpotQA / MuSiQue instances expect the decompressed files, which `reproduce_all.py`
creates on its way; when running a script on its own first do
`gunzip -k code/data/processed/*.jsonl.gz`.

## 3. Response cache

All model responses behind the reported runs are kept in a content-addressed SQLite cache, each
with its decoding fingerprint, token usage and latency. It is stored zstd-compressed on the
`cache-snapshots` branch:

```bash
python code/scripts/restore_cache.py              # -> code/results/cache/closed.sqlite (~1.3 GB, sha256-checked)
python code/scripts/reproduce_all.py --tokens     # adds token / prompt-size accounting, which replays the cache
```

`restore_cache.py` fetches the branch into a temporary worktree, checks the hash, decompresses and
removes the worktree; `--snapshot <date>` picks a specific snapshot. The table is
`cache(k, response, model, temperature, fingerprint, meta, created_at, key_version)`, where `meta`
is JSON with token usage, latency, finish reason, response id and served model. For example:

```bash
sqlite3 code/results/cache/closed.sqlite "select model, count(*) from cache group by model"
```

Cache keys hash the model name, the messages, the decoding settings, the sample index and the
fingerprint of the endpoint each response was drawn from (recorded per row), so a lookup with the
original model name and fingerprint returns the stored draw without a new call. The gateway
configs of Section 4 use different model ids and endpoints, so their calls are new draws.

## 4. Running new experiments

This issues billable calls. Start with a small subset (`--sample-n`) and check the cost file
written next to each output before a full run.

**Keys and endpoints.** Each closed model has two configs in `code/configs/models/closed/`:
`<model>.yaml` uses OpenRouter and `<model>@omnigate.yaml` uses OminiGate. Both are
OpenAI-compatible; keys are read from the environment and never stored in a file.

```bash
export OPENROUTER_API_KEY=...      # <model>.yaml           -> https://openrouter.ai/api/v1
export OMNIGATE_API_KEY=...        # <model>@omnigate.yaml  -> https://api.ominigate.ai/v1
```

Models: `claude-haiku-5-5`, `gpt-6-luna`, `gemini-2.5-flash-lite` (main), `gemini-2.5-flash`,
`gpt-6.1-terra` (tier), plus `gpt-5.6-luna`. Model ids follow each gateway's `provider/model` naming
(e.g. `openai/gpt-6-luna`); check them against the gateway's model list before a run. Decoding
settings shared by all models are in `code/configs/base.yaml`.

**Pipeline.** Run from `code/`. Always pass a new `--tag`: outputs go to
`results/closed/raw/<dataset>/<model>/<tag>/`, and a run manifest refuses to resume a directory
written with a different configuration, so reusing a released tag (`main`, `grid`, ...) stops
with an error instead of overwriting.

```bash
gunzip -k code/data/processed/*.jsonl.gz
cd code

# (a) screening: ask each candidate instance once without and once with context;
#     evaluable = context-dependent and correct. Released outcomes are in results/closed/screen/.
python scripts/14_screen_closed.py --model configs/models/closed/gpt-6-luna.yaml \
    --dataset hotpotqa --pool union --workers 8 --limit 20
python scripts/16_summarize_screening.py          # -> results/closed/screen/summary.{json,md}

# (b) estimators on the evaluable set: V1 (self-report), P1 (leave-one-out) with 3 matched-T
#     full-context repeats, LOI (leave-one-in), RM (random masks, K=64, Banzhaf)
python -u scripts/17_run_closed.py --model configs/models/closed/gpt-6-luna.yaml \
    --dataset hotpotqa --methods V1,P1,LOI,RM --rm-k 64 --full-repeats 3 \
    --sample-n 12 --tag mytrial --outer-workers 4 --inner-workers 4

# (c) analysis of the new tag (same scripts as Section 2)
python scripts/18_analyze_closed.py --tag mytrial
python scripts/28_paper_tables.py --tag mytrial --split all
```

Useful options of `17_run_closed.py`: `--dataset hotpotqa|musique|symfever|qasper`;
`--methods` takes `V1..V7`, `P1..P5`, `RM`, `LOI` (MExGen-LOO needs no calls; it is re-scored from
P1 by `18_analyze_closed.py`); `--pool union|intersection` (default: union for main models,
intersection for tier models); `--instances <file>` runs a constructed set such as
`data/constructed/k3/...`; `--repeat 1` draws an independent repeat; `--cache-only` never calls the
API and fails on a cache miss.

Each output `<method>.jsonl` comes with `<method>.manifest.json` (configuration, endpoint
fingerprint) and `<method>.cost.json` (tokens and cost of the calls actually issued; cache hits are
free). New responses are added to `results/cache/closed.sqlite`, so an interrupted run resumes
without repeating calls.

**Drivers.** `scripts/run_*.sh` are the drivers used for the reported runs (e.g.
`run_phase2_main.sh` for the main grid, `run_symfever.sh`, `run_qasper.sh`, `run_k3_pilot.sh`,
`run_review_probes.sh`). They contain the exact arguments per model and dataset. Each starts with
a line that loads our local key file (`. /home/claude/.mht_api.env`); delete that line and export
the variables above instead.

**Datasets.** The constructed sets are already in `code/data/constructed/` and the processed
HotpotQA / MuSiQue dev sets in `code/data/processed/` (run `gunzip -k code/data/processed/*.jsonl.gz`
once), so no download is needed. To rebuild them from the public releases: `19_build_k3.py` (exact copy),
`26_build_symfever.py`, `33_build_qasper.py`, `38_build_review_probes.py` (these need the
`datasets` package and network access).

## Layout

| Path | Content |
|---|---|
| `code/src/` | query client with cache (`utils/cache.py`), estimators (`pipelines/runner.py`, `pipelines/subset.py`), prompts and parsing |
| `code/scripts/` | numbered pipeline: data construction (`19`, `26`, `33`, `38`), screening (`14`, `16`, `27`), runs (`17`, `run_*.sh`), analyses (`18`, `21`, `28`, `31`, `32`, `36`, `37`, `39`), tables (`29`, `40`) |
| `code/configs/` | decoding settings (`base.yaml`); `models/closed/<model>.yaml` (OpenRouter) and `<model>@omnigate.yaml` (OminiGate) per model; `models/*.yaml` for the open models of the earlier study |
| `code/data/constructed/` | Symmetric FEVER, Qasper, exact-copy (`k3/`) and probe instances built from the public releases |
| `code/results/closed/` | screening outcomes, per-instance results with run manifests, analysis outputs |
| `code/results/raw/`, `code/results/reanalysis/` | open-model screening and re-analysis of the earlier study (inputs of `40_open_models_table.py`) |
| `paper/` | generated LaTeX tables and the figures; `paper/figures/drafts/` holds the editable figure sources and their renderers |

`code/RUNNING.md` documents the earlier open-model study (vLLM serving, scripts `00`-`13`), whose
screening supplies the multi-hop candidate pools.

## Datasets and licences

Licences follow the original releases (HotpotQA CC BY-SA 4.0, MuSiQue CC BY 4.0, Qasper
CC BY 4.0, FEVER and Symmetric FEVER: Wikipedia text under CC BY-SA 3.0). Constructed files keep
the original identifiers; see `code/data/raw/<dataset>/PROVENANCE.md` and the `build_info.json` / `*.report.json` files next to the constructed sets.

## Models

claude-haiku-5-5, gpt-6-luna, gemini-2.5-flash-lite (main), gemini-2.5-flash, gpt-6.1-terra (tier),
queried through OpenAI-compatible chat endpoints. Model identity is as declared by the serving
endpoint; each cached response records the served model name.
