# Black-box Context Attribution

Contributive context attribution for LLMs accessible only through text-only
APIs, where token-level likelihoods are unavailable.

## Layout

`src/stages/` mirrors the three stages of the paper's framework:
`prompting.py` (pi), `sampling.py` (sigma), `aggregation.py` (alpha).
`src/pipelines/registry.py` defines the 12 viable methods and refuses the
infeasible combinations.

## Order of operations

1. `scripts/01_stability_check.py` -- **run this first**. It measures
   epsilon-hat (Assumption 1). If thinking mode leaks, or epsilon is high even
   under the structured-output constraint, the interventional pipeline is
   unsound for that model and nothing downstream is worth running.
2. Small-scale sweep (~200 instances) across the full method matrix.
3. Baselines and gray-box upper bounds.
4. Full run and figures.

## Serving open models

```bash
vllm serve Qwen/Qwen3-8B --port 8000        # do NOT pass --enable-reasoning
vllm serve google/gemma-3-12b-it --port 8000
```

Thinking is disabled per-request via `chat_template_kwargs.enable_thinking`.
`utils/parsing.py` raises `ThinkingLeakError` if a `<think>` block appears
anyway -- an inflated epsilon from leaked reasoning would look like a property
of the model rather than a configuration error.

## Cost

Interventional methods cost `(M*N + 1) * kappa` calls per instance.
M is ~10 on HotpotQA and ~20 on MuSiQue, so MuSiQue is roughly twice as
expensive. The SQLite cache stores raw responses keyed on generation
parameters only, so re-sweeping lambda / beta / tau costs nothing.

## Not implemented

- ARC-JSD: adapter interface only (`src/baselines/arc_jsd.py`).
- Diffusion LMs: future work.
