"""Subset-intervention attributors for strictly black-box models (phase 2).

All three only look at the generated answer text, like P1. They differ in
which context subsets are queried and how answers become scores.

RM   random masking: K random subsets (each source kept with prob. p_keep,
     masks drawn once per instance from a fixed seed, so the first k masks of a
     K-mask run are exactly a k-mask run). The value of a subset S is
     v(S) = 1[answer(S) == a0] (exact, after normalisation) or the token-F1
     between answer(S) and a0. Two estimators over the same draws:
       * banzhaf: mean v(S | i in S) - mean v(S | i not in S); with p_keep=0.5
         this is an unbiased estimate of the Banzhaf value of i;
       * linear:  ridge-regularised linear surrogate v(S) ~ b + sum_i w_i 1[i in S]
         (the answer-only analogue of ContextCite's surrogate; with the
         token-F1 value it is our text-output adaptation of MExGen's C-LIME).
     Redundancy-aware: a source whose content is duplicated elsewhere is
     credited only through subsets that miss the duplicate.

LOI  leave-one-in: the model sees ONE source; score_i = v({i}). A sufficiency
     probe (does this source alone reproduce a0?), complementary to the
     necessity probe of leave-one-out (P1).

MExGen-LOO
     MExGen (Monteiro Paes et al., 2024) attributes generated TEXT with
     text-similarity "scalarizers" instead of logits. Its leave-one-out mode
     needs no extra calls here: score_i = 1 - F1(a_{-i}, a0) on P1's ablated
     answers (`answers_from_p1`).

a0 is P1's reference answer (full context, T=0.01, sample 0): the same prompt,
decoding settings and cache key, so it is served from the cache and RM / LOI /
P1 compare against the same a0.
"""
from __future__ import annotations

import random
import re
import zlib
from collections import Counter

import numpy as np

from ..backends.base import Backend, GenConfig
from ..data.schema import Instance
from ..stages.aggregation import is_empty_prediction, to_ranking, to_set
from ..stages.prompting import PromptSpec, Vanilla, _BASE, _SCHEMA_ANSWER_ONLY
from ..stages.sampling import SamplingSpec, collect_observations
from ..utils.cache import QueryCache
from ..utils.parsing import normalize_answer
from .runner import AttributionResult, signal_fields


# ---------------------------------------------------------------- scalarizers

def _tokens(s: str | None) -> list[str]:
    if not s:
        return []
    return re.findall(r"\w+", normalize_answer(s))


def token_f1(a: str | None, b: str | None) -> float:
    """SQuAD-style token F1 between two short answers (normalised)."""
    ta, tb = _tokens(a), _tokens(b)
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    common = sum((Counter(ta) & Counter(tb)).values())
    if common == 0:
        return 0.0
    p, r = common / len(ta), common / len(tb)
    return 2 * p * r / (p + r)


def exact(a: str | None, b: str | None) -> float:
    if a is None or b is None:
        return 0.0
    return float(normalize_answer(a) == normalize_answer(b))


SCALARIZERS = {"exact": exact, "f1": token_f1}


# ---------------------------------------------------------------- estimators

def draw_masks(M: int, K: int, p_keep: float = 0.5, seed: int = 0,
               reject_full: bool = False) -> np.ndarray:
    """K x M boolean keep-masks, i.i.d. Bernoulli(p_keep) per source. Fixed per
    instance seed; prefix-nested in K.

    Default (since 2026-11-02): the full product distribution, so the Banzhaf
    difference of means is unbiased for the Banzhaf value. An all-kept mask is
    the reference prompt itself; its answer is the cached reference draw a0
    (v = 1 by construction), i.e. the full-context sample is the REUSED
    reference generation, not an independent draw. `reject_full=True`
    reproduces the earlier conditional design (all-kept masks redrawn), under
    which the estimator is NOT the unbiased Banzhaf value (e.g. AND of two
    sources gives [0, 0] instead of [0.5, 0.5])."""
    rng = random.Random(seed)
    out = []
    while len(out) < K:
        m = [rng.random() < p_keep for _ in range(M)]
        if reject_full and all(m):
            continue
        out.append(m)
    return np.array(out, dtype=bool)


def banzhaf(masks: np.ndarray, y: np.ndarray) -> np.ndarray:
    M = masks.shape[1]
    phi = np.zeros(M)
    for i in range(M):
        inn, out = y[masks[:, i]], y[~masks[:, i]]
        if len(inn) and len(out):
            phi[i] = inn.mean() - out.mean()
    return phi


def ridge(masks: np.ndarray, y: np.ndarray, alpha: float = 1.0) -> np.ndarray:
    X = masks.astype(float)
    Xc = X - X.mean(0)
    yc = y - y.mean()
    A = Xc.T @ Xc + alpha * np.eye(X.shape[1])
    return np.linalg.solve(A, Xc.T @ yc)


# ---------------------------------------------------------------- prompts

def subset_prompt(inst: Instance, keep: list[int]) -> PromptSpec:
    """Answer-only vanilla prompt over the kept sources, renumbered 1..|S|
    in original order (no gaps, as in leave-one-out)."""
    drop = {s.idx for s in inst.sources} - set(keep)
    content = _BASE.format(context=inst.render_context_excluding(drop),
                           question=inst.question) + _SCHEMA_ANSWER_ONLY
    return PromptSpec(messages=[{"role": "user", "content": content}], expect_sources=False)


def reference_answer(inst, backend, cfg, cache, repeat):
    """P1's reference draw (same prompt / cfg / sample 0 / repeat -> cache hit)."""
    strat = Vanilla()
    obs, calls = collect_observations(backend, strat.build(inst, exclude=None, verbalize=False),
                                      strat, SamplingSpec.build("single_pass"), cfg, cache,
                                      repeat=repeat)
    return obs[0], calls


def _answers_for(prompts, backend, cfg, cache, repeat, workers):
    strat = Vanilla()
    sp = SamplingSpec.build("single_pass")

    def one(p):
        o, c = collect_observations(backend, p, strat, sp, cfg, cache, repeat=repeat)
        return o[0], c

    # Identical prompts (e.g. two equal random masks) are sent once: dispatched
    # concurrently they would both miss the cache, draw two different answers at
    # T>0, and the later cache write would make a replay disagree with the run.
    import json as _json
    keys = [_json.dumps(p.messages, sort_keys=True, ensure_ascii=False) for p in prompts]
    first = {}
    for j, k in enumerate(keys):
        first.setdefault(k, j)
    uniq = [prompts[j] for j in first.values()]
    if workers and workers > 1 and len(uniq) > 1:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=workers) as ex:
            res = list(ex.map(one, uniq))
    else:
        res = [one(p) for p in uniq]
    by_key = dict(zip(first, res))
    return [by_key[k][0] for k in keys], sum(r[1] for r in res)


def _result(inst, mid, phi, calls, n_obs, failures, a0, meta, tau):
    return AttributionResult(
        qid=inst.qid, method=mid, phi=phi, ranking=to_ranking(phi),
        pred_set=to_set(phi, tau=tau), gold=inst.gold_indices, n_calls=calls,
        empty_prediction=is_empty_prediction(phi, tau=tau), parse_failures=failures,
        n_observations=n_obs, baseline_answer=a0,
        meta={"n_hop": inst.n_hop, "M": inst.M, **signal_fields(phi, tau), **meta},
    )


def _invalid_reference(inst, mid, calls, tau, meta):
    """Reference draw failed (unparsable / empty): record it as such instead of an
    all-zero attribution, and issue no ablation / mask calls (issue #1, round 25).
    Analysis counts these as pipeline failures, separate from valid all-zero rows."""
    return _result(inst, mid, np.zeros(inst.M), calls, 1, 1, None,
                   {**meta, "baseline_ok": False, "invalid_reference": True}, tau)


# ---------------------------------------------------------------- methods

def run_random_mask(inst: Instance, backend: Backend, cfg: GenConfig, K: int = 32,
                    p_keep: float = 0.5, cache: QueryCache | None = None, repeat: int = 0,
                    inner_workers: int = 1, tau: float = 0.5, mask_seed: int = 0,
                    estimator: str = "banzhaf", value: str = "exact") -> AttributionResult:
    """Primary score = `estimator` x `value`; all four estimator x value
    combinations are stored in meta['scores'] (they share the same K calls).
    meta['mask_answers'] keeps the raw answers so any prefix k <= K can be
    re-scored offline (K is tuned on a dev set by convergence to the K_max run)."""
    base, calls = reference_answer(inst, backend, cfg, cache, repeat)
    a0 = base.answer if base.ok else None
    if a0 is None:  # invalid reference: nothing to compare masks against -> stop early
        return _invalid_reference(inst, f"RM{K}", calls, tau, {"repeat": repeat, "K": K})
    # stable across processes (str hash is salted). Constructed variants may set
    # meta['mask_key'] (e.g. K3: base qid + slot count) so paired conditions with
    # the same M share masks (common random masks -> lower paired MC variance).
    key = (inst.meta or {}).get("mask_key") or inst.qid
    seed = zlib.crc32(key.encode()) ^ mask_seed
    masks = draw_masks(inst.M, K, p_keep, seed)
    obs, c = _answers_for([subset_prompt(inst, [i for i in range(inst.M) if m[i]]) for m in masks],
                          backend, cfg, cache, repeat, inner_workers)
    calls += c
    answers = [o.answer if o.ok else None for o in obs]
    scores = {}
    if a0 is not None:
        for vn, vf in SCALARIZERS.items():
            y = np.array([vf(a, a0) for a in answers], dtype=float)
            scores[f"banzhaf_{vn}"] = banzhaf(masks, y).tolist()
            scores[f"linear_{vn}"] = ridge(masks, y).tolist()
    phi = np.array(scores.get(f"{estimator}_{value}", np.zeros(inst.M)), dtype=float)
    return _result(inst, f"RM{K}", phi, calls, len(obs) + 1,
                   sum(not o.ok for o in obs) + int(not base.ok), a0,
                   {"repeat": repeat, "K": K, "p_keep": p_keep, "mask_seed": seed,
                    "n_unique_masks": int(len({tuple(m) for m in masks.tolist()})),
                    "n_full_masks": int(masks.all(1).sum()), "mask_design": "bernoulli_product",
                    "estimator": f"{estimator}_{value}", "scores": scores,
                    "masks": masks.astype(int).tolist(), "mask_answers": answers,
                    "baseline_ok": base.ok}, tau)


def run_leave_one_in(inst: Instance, backend: Backend, cfg: GenConfig,
                     cache: QueryCache | None = None, repeat: int = 0,
                     inner_workers: int = 1, tau: float = 0.5,
                     value: str = "exact") -> AttributionResult:
    base, calls = reference_answer(inst, backend, cfg, cache, repeat)
    a0 = base.answer if base.ok else None
    if a0 is None:
        return _invalid_reference(inst, "LOI", calls, tau, {"repeat": repeat})
    obs, c = _answers_for([subset_prompt(inst, [s.idx]) for s in inst.sources],
                          backend, cfg, cache, repeat, inner_workers)
    calls += c
    answers = [o.answer if o.ok else None for o in obs]
    scores = {vn: [vf(a, a0) if a0 is not None else 0.0 for a in answers]
              for vn, vf in SCALARIZERS.items()}
    phi = np.array(scores[value], dtype=float)
    return _result(inst, "LOI", phi, calls, len(obs) + 1,
                   sum(not o.ok for o in obs) + int(not base.ok), a0,
                   {"repeat": repeat, "scores": scores, "single_answers": answers,
                    "baseline_ok": base.ok}, tau)


def mexgen_loo_from_p1(p1_row: dict, gold: list[int], tau: float = 0.5) -> dict:
    """Re-score a stored P1 row with MExGen's text-similarity scalarizer:
    phi_i = mean_n (1 - F1(a_{-i}^n, a0)). No additional calls."""
    a0 = p1_row.get("baseline_answer")
    abl = p1_row["meta"].get("ablated_answers") or {}
    M = p1_row["meta"]["M"]
    phi = np.zeros(M)
    for i, ans in abl.items():
        ans = [a for a in ans if a is not None]
        if ans and a0 is not None:
            phi[int(i)] = float(np.mean([1 - token_f1(a, a0) for a in ans]))
    return {"qid": p1_row["qid"], "method": "MEXGEN_LOO", "phi": phi.tolist(),
            "ranking": to_ranking(phi), "pred_set": to_set(phi, tau=tau), "gold": gold,
            "n_calls": 0, "meta": {"M": M, "n_hop": p1_row["meta"].get("n_hop"),
                                   **signal_fields(phi, tau), "derived_from": "P1"}}
