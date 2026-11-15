# Running Guide — Black-box Context Attribution

End-to-end instructions, from a fresh machine to figures. Read §0 first;
the single most important rule is **run the stability check before anything
expensive**.

---

## 0. The one thing that matters most

Run `scripts/01_stability_check.py` **before** any full method sweep. It
measures baseline stability (epsilon-hat, Assumption 1 in the paper). If it
reports:

- **thinking leaks** (`<think>` blocks present) → thinking mode is not actually
  off; the perturbation pipeline is invalid until you fix the serving flags.
- **epsilon-hat > 0.2 under the `structured` condition** → the model's output is
  too nondeterministic for ablation to mean anything; perturbation results will
  be noise for that model.

Both are cheap to check and can invalidate the whole design. Do not skip.

---

## 1. Environment

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Two capability groups; install only what you use:

- **Black-box methods (the paper's contribution):** `openai`, `datasets`,
  `numpy`, `pyyaml`, `tqdm`. Talks to models over an OpenAI-compatible endpoint.
- **Gray-box baselines (upper bound):** `torch`, `transformers`, `context_cite`.
  Needs a GPU and open-weight model access.
- **Retrieval baselines:** `rank-bm25`, `sentence-transformers`. CPU is fine.

Run the tests to confirm the install:

```bash
python tests/test_aggregation.py    # 12 passed
python tests/test_pipelines.py      # 8 passed
```

---

## 2. Data (offline-friendly)

On a **networked** machine, cache the datasets to disk:

```bash
python scripts/00_prepare_data.py --dataset hotpotqa --limit 500
python scripts/00_prepare_data.py --dataset musique  --limit 500
```

Copy `data/processed/*.jsonl` to the offline server. The loaders read these
directly; no HF access happens at experiment time. To forbid network access
entirely, `export HF_DATASETS_OFFLINE=1`. To use a mirror instead, pass
`--hf-name bdsaglam/musique`.

Two loader behaviours worth knowing:

- **Answer filtering** (`max_answer_words=4`, on by default): drops the ~10% of
  answers longer than 4 words. Long compound answers break the exact-match
  change detector. Pass `--max-answer-words 0` semantics via config only if you
  deliberately want them back.
- **Hop balancing** (MuSiQue): the runner sets `balance_hops=True` automatically.
  Without it the first N rows are almost all 2-hop, which silently ruins the
  hop-stratified analysis (Sec. 6.5).

---

## 3. Serving models

### Open-weight models (vLLM)

```bash
# Qwen3: do NOT pass --enable-reasoning; thinking is disabled per-request
vllm serve Qwen/Qwen3-8B         --port 8000
vllm serve google/gemma-3-12b-it --port 8000
```

Point the model config's `base_url` at the server. Thinking is disabled via
`chat_template_kwargs.enable_thinking=False` in each request; the parser raises
`ThinkingLeakError` if a `<think>` block appears anyway.

### Closed model via a third-party OpenAI-compatible gateway

`configs/models/claude-haiku.yaml` is already set up for this. Set the key in
the environment (never commit it):

```bash
export OMNIGATE_API_KEY=sk-omg-...
```

The config uses `send_thinking_kwarg: false` so no vLLM-specific fields are
sent to the gateway. Adjust `model`, `base_url`, and the env var name to your
provider.

---

## 4. Run one cell (debugging)

```bash
python scripts/02_run_method.py --method P4 --model qwen3-8b \
    --dataset hotpotqa --n-instances 200
```

Results stream to `results/raw/<dataset>/<model>/<method>.jsonl`. A crash loses
at most one instance; rerunning skips finished qids. The SQLite cache stores raw
responses, so re-running with different `lambda`/`beta`/`tau` (set in
`configs/base.yaml`) costs **zero** queries.

Method IDs: `V1–V7` (verbalize), `P1–P5` (perturbation). See the registry for
the (prompting, sampling, aggregation) each maps to.

---

## 5. Run the full grid

**Always dry-run first** — the interventional methods are O(M·N) and MuSiQue has
M≈20, so costs are large.

```bash
python scripts/03_run_all.py --dry-run                    # prints query budget
python scripts/03_run_all.py \
    --models qwen3-1.7b qwen3-4b qwen3-8b \
             gemma3-1b gemma3-4b gemma3-12b \
    --datasets hotpotqa musique \
    --methods V1 V2 V3 V4 V5 V6 V7 P1 P2 P3 P4 P5 \
    --n-instances 200
```

Add `--continue-on-error` to keep going if one model is down. Model configs for
the 1.7b/4b sizes and gemma variants follow the pattern in
`configs/models/qwen3-8b.yaml` — copy and edit `model`, `params_b`, `family`,
and the gen params.

---

## 6. Baselines

```bash
# lower bounds + retrieval (no GPU)
python scripts/04_run_baselines.py --dataset hotpotqa \
    --baselines random positional bm25 embedding --n-instances 200
python scripts/04_run_baselines.py --dataset musique \
    --baselines random positional bm25 embedding --n-instances 200

# gray-box upper bound (GPU + open model)
python scripts/04_run_baselines.py --dataset hotpotqa \
    --baselines contextcite --model Qwen/Qwen3-8B --n-instances 200
```

`embedding` defaults to `mixedbread-ai/mxbai-embed-xsmall-v1` on `--embed-device
auto` (CUDA if present, else CPU). BM25 and embedding are **diagnostic
references, not competitors**: their overlap with a method (reported in
`baseline_overlap.csv`) tells you whether the black-box signal reduces to
lexical or semantic retrieval.

ARC-JSD is a stub — see `src/baselines/arc_jsd.py`. Clone the official repo,
confirm its paragraph-level interface, and implement `run()`.

---

## 7. Aggregate and plot

```bash
python scripts/05_aggregate_results.py --n-instances 200
python scripts/06_make_figures.py --dataset hotpotqa
python scripts/06_make_figures.py --dataset musique
```

Aggregation reads `results/raw/**` and writes CSVs to `results/tables/`:

| CSV | Paper element |
|---|---|
| `main_results.csv` | Table 1 (methods + baselines + gray-box, per model/dataset) |
| `scale.csv` | Figure 3 (best-V / best-P top-1, parse-fail, by size) |
| `agreement.csv` | Figure 4a (verbalize vs perturbation contingency) |
| `failure_by_hop.csv` | Figure 4b (empty-prediction vs hop, MuSiQue) |
| `selection_bias.csv` | Sec. 6.2 directionality (selected vs gold position) |
| `baseline_overlap.csv` | Sec. 6.2 overlap with BM25 / embedding |

Figures land in `results/figures/`. Both scripts are pure post-processing — safe
to re-run and restyle without touching a model.

---

## 8. Recommended order

```
1. 01_stability_check.py         # gate: Assumption 1 holds?
1b. 01b_ablation_robustness.py   # does CoT actually break perturbation? (Sec. 4.5)
1c. 01c_leakage_check.py         # can the model answer without context at all?
2. 02_run_method.py (one cell)   # sanity: one method end-to-end
3. 03_run_all.py --dry-run       # budget check
4. 03_run_all.py (small: 200)    # full matrix, modest N
5. 04_run_baselines.py           # bounds
6. 05_aggregate + 06_figures     # tables and plots
```

---

## Evaluation subset selection (important)

`01c_leakage_check.py` partitions instances by two questions: can the model
answer **without** the context, and does it answer correctly **with** it.

| bucket | no-context | with-context | usable? |
|---|---|---|---|
| `leaked` | correct | — | no: parametric shortcut, nothing for ablation to find |
| `context_dep` | wrong | correct | **yes** |
| `abstained_correct` | refused | correct | **yes** (ideal profile) |
| `abstained_wrong` | refused | wrong | no |
| `both_wrong` | wrong | wrong | no |

The report writes an `evaluable` list = `context_dep` + `abstained_correct`.
Gold supporting facts are a valid attribution target **only** on that subset:
when the model answers wrongly, the evidence it actually used has no reason to
match the human annotation, so scoring against gold facts measures a mismatch
rather than a method failure.

Run per model (both leakage and correctness are model-specific), then restrict
the run to the evaluable set:

```bash
python scripts/01c_leakage_check.py --model <model> --dataset musique \
    --n-instances 500 --out results/raw/eval_qwen3-8b_musique.json

python scripts/02_run_method.py --method P4 --model qwen3-8b \
    --dataset musique --n-instances 500 \
    --only-qids results/raw/eval_qwen3-8b_musique.json
```

**Sample enough raw instances.** The evaluable rate can be low (on MuSiQue with
Qwen3-8B, `context_dep` alone was 11%), so to obtain K evaluable instances,
sample roughly `K / evaluable_rate` raw ones. 01c prints this multiplier.

Two softer alternatives, if you would rather keep the full set:
`--exclude-leaked` tags leaked instances so `05_aggregate_results.py` emits both
`full` and `context_dep` rows in a `subset` column; `--drop-leaked` skips them
to save queries; `--drop-yesno` removes binary-answer questions, whose ~50%
flip prior gives poor signal-to-noise.

Observed contrast worth reporting: leakage was 26% on HotpotQA versus 1% on
MuSiQue for the same model — the synthetic multi-hop construction resists
memorisation, which makes MuSiQue the sounder primary benchmark.

## Shared evaluation sets across models

Each model has its own evaluable set, since correctness is model-specific. That
keeps gold facts a valid target but makes cross-model comparison murky: two
models scored on different instance sets differ partly because the sets differ.

`01d_intersect_evaluable.py` computes intersections so every model is scored on
instances it answers correctly AND all models are scored on the same instances:

```bash
# run 01c for every model first, then:
python scripts/01d_intersect_evaluable.py \
    --reports 'results/raw/eval_*_musique.json' --dataset musique

# write a family-level shared set
python scripts/01d_intersect_evaluable.py \
    --reports 'results/raw/eval_*_musique.json' --dataset musique \
    --family qwen3 --out results/raw/shared_qwen3_musique.json

python scripts/03_run_all.py --datasets musique \
    --models qwen3-1.7b qwen3-4b qwen3-8b \
    --only-qids-pattern 'results/raw/shared_qwen3_{dataset}.json'
```

**Prefer per-family intersections.** Sec. 6.3 asks whether the scale trend holds
within each family, which needs clean comparison inside a family, not across
them -- and a global intersection is squeezed by the weakest model of every
family simultaneously, often down to very few instances.

The tool prints the hop composition of each intersection and flags strata with
fewer than 20 instances. A small intersection is still usable; just report the
exact n per stratum rather than percentages alone.

## Sampling the evaluation set

The evaluable set can be large (MuSiQue full validation is ~2100 instances, of
which roughly a third are evaluable), while the interventional methods cost
`(M*N+1)*kappa` queries each. Cap the sample rather than the raw pool:

```bash
# 1. profile the FULL set once per model (2 queries per instance)
python scripts/01c_leakage_check.py --model <model> --dataset musique \
    --n-instances 999999 --out results/raw/eval_qwen3-8b_musique.json

# 2. run the grid on a stratified sample of the evaluable set
python scripts/03_run_all.py --datasets musique --sample-n 300 \
    --only-qids-pattern 'results/raw/eval_{model}_{dataset}.json'
```

`--stratify-by hop` (the default) balances the draw across hop counts. This
matters because the evaluable set is conditioned on the model answering
correctly, and accuracy falls with hop depth, so an unstratified draw starves
the deep strata: from a 200/120/40 pool, an unstratified n=150 yields 82/51/17,
whereas the stratified draw yields 55/55/40. Strata smaller than the quota are
taken whole and the surplus is redistributed, so the total is never silently
reduced.

Use `--sample-seed` to reproduce a draw exactly.

## Concurrency (saturating vLLM replicas)

The client is serial by default. If you serve with `data_parallel_size>1`, a
serial client leaves all but one replica idle, so the DP flag buys almost
nothing until requests are issued concurrently.

Two levels of parallelism, multiplicative:

- `--outer-workers N` runs N instances at once.
- `--inner-workers K` fans each instance's M ablations over K threads
  (perturbation only; verbalize has nothing to fan out).

In-flight requests are roughly `outer * inner`. Size that to keep every replica
busy -- as a starting point, `outer * inner ~= 8-16 x data_parallel_size`.

```bash
# vLLM with 3 replicas:
vllm serve Qwen/Qwen3-8B --data-parallel-size 3 --port 8000

python scripts/03_run_all.py --datasets musique --sample-n 186 \
    --only-qids-pattern 'results/raw/shared_qwen3_{dataset}.json' \
    --outer-workers 12 --inner-workers 4      # ~48 in flight
```

Correctness is unaffected: concurrent ablation produces byte-identical results
to serial (the M ablations are independent), the cache is mutex-guarded and
reused across threads, and output rows are written under a lock. A `<think>`
leak in any worker still aborts the cell.

Rough guide with DP=3 and ~48 in-flight, short answers (max_tokens=256): the
~1.1M-call full grid, minus cache reuse (P4/P5 and V4/V5 share queries), lands
around 3-5 hours rather than the 26-40 hours a serial client would take.

## Cost control

- Interventional cost is `(M·N + 1)·kappa` per instance; `kappa=2` for
  self-probing. MuSiQue (M≈20) is ~2× HotpotQA (M≈10).
- The cache means parameter sweeps (lambda/beta/tau) are free after the first run.
- Perturbation defaults to a smaller `N` than verbalize (binary decisions
  converge faster); tune in `configs/base.yaml`.
- If the full grid is too large, cut MuSiQue's method count or `n_instances`
  first; keep the two ends of each size ladder to preserve the scale trend.

## Known limitations in the code

- ARC-JSD: interface only.
- Diffusion LMs: not implemented (future work).
- Long answers (>4 words): filtered out by default; the method targets
  short-answer extractive QA.
