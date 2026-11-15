"""The two pipelines -- paper Sec. 4.1.

verbalize:    one input configuration, ask the model what it used.  O(N)
perturbation: baseline + M ablations, compare answers.                O(M*N)

Both traverse all three stages; they differ only in how many input
configurations they query and how the observations become scores.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ..backends.base import Backend, GenConfig
from ..data.schema import Instance
from ..stages.aggregation import (
    aggregate_perturbation, aggregate_verbalize, is_empty_prediction,
    to_ranking, to_set,
)
from ..stages.prompting import get_strategy
from ..stages.sampling import SamplingSpec, collect_observations
from ..utils.cache import QueryCache
from ..utils.parsing import ParsedObservation
from .registry import MethodSpec


@dataclass
class AttributionResult:
    qid: str
    method: str
    phi: np.ndarray
    ranking: list[int]
    pred_set: list[int]
    gold: list[int]
    n_calls: int
    empty_prediction: bool
    parse_failures: int
    n_observations: int
    baseline_answer: str | None = None
    meta: dict = field(default_factory=dict)

    @property
    def top1_correct(self) -> bool:
        return bool(self.ranking) and self.ranking[0] in self.gold

    def to_json(self) -> dict:
        d = self.__dict__.copy()
        d["phi"] = [float(x) for x in self.phi]
        return d


FULL_NOISE_REPEAT_OFFSET = 100_000


def signal_fields(phi: np.ndarray, tau: float = 0.5) -> dict:
    """Explicit signal status of a score vector (replaces the overloaded
    `empty_prediction`, which only means "no score >= tau")."""
    phi = np.asarray(phi, dtype=float)
    if phi.size == 0:
        return {"all_zero": True, "reaches_tau": False, "below_tau_nonzero": False, "unique_max": False}
    reaches = bool(np.any(phi >= tau))
    nonzero = bool(np.any(phi))
    return {
        "all_zero": not nonzero,
        "reaches_tau": reaches,
        "below_tau_nonzero": nonzero and not reaches,
        "unique_max": int(np.sum(phi == phi.max())) == 1,
    }


def _count_failures(obs_list: list[ParsedObservation]) -> int:
    return sum(1 for o in obs_list if not o.ok)


def _w_of(obs: ParsedObservation, lam: float) -> float:
    """Vote weight of one observation; mirrors aggregation._w."""
    if obs.likely is None:
        return 1.0
    return {"yes": 1.0, "unsure": lam, "no": 0.0}[obs.likely]


def run_verbalize(
    inst: Instance,
    method: MethodSpec,
    backend: Backend,
    cfg: GenConfig,
    n_samples: int = 5,
    lam: float = 0.5,
    tau: float = 0.5,
    cache: QueryCache | None = None,
    repeat: int = 0,
) -> AttributionResult:
    strategy = get_strategy(method.prompting)
    sampling = SamplingSpec.build(method.sampling, n_samples)
    prompt = strategy.build(inst, exclude=None, verbalize=True)

    obs, calls = collect_observations(
        backend, prompt, strategy, sampling, cfg, cache, repeat=repeat
    )

    # direct aggregation is the N=1 special case; lambda only bites when the
    # `likely` field exists at all.
    effective_lam = lam if method.aggregation == "uncertainty" else 1.0
    raw = aggregate_verbalize(
        obs, M=inst.M, surviving=inst.surviving_indices(), lam=effective_lam
    )
    # Normalise votes to a rate in [0,1] so that tau means the same thing in
    # both pipelines: "selected in at least tau of the usable samples".
    denom = sum(_w_of(o, effective_lam) for o in obs if o.ok and o.sources)
    phi = raw / denom if denom > 0 else raw

    return AttributionResult(
        qid=inst.qid,
        method=method.mid,
        phi=phi,
        ranking=to_ranking(phi),
        pred_set=to_set(phi, tau=tau),
        gold=inst.gold_indices,
        n_calls=calls,
        empty_prediction=is_empty_prediction(phi, tau=tau),
        parse_failures=_count_failures(obs),
        n_observations=len(obs),
        meta={"n_hop": inst.n_hop, "M": inst.M, "repeat": repeat, **signal_fields(phi, tau),
              # keep what the model actually answered alongside its attribution
              "answers": [o.answer for o in obs]},
    )


def run_perturbation(
    inst: Instance,
    method: MethodSpec,
    backend: Backend,
    cfg: GenConfig,
    n_samples: int = 5,
    beta: float = 0.0,
    tau: float = 0.5,
    cache: QueryCache | None = None,
    inner_workers: int = 1,
    n_full_repeats: int = 0,
    repeat: int = 0,
    measure_full_noise: bool = False,
) -> AttributionResult:
    """Leave-one-out perturbation.

    The reference answer a0 is a single T=0.01 draw on the full context. For
    multi-sample methods the ablations are drawn at T=0.7, so part of the
    observed change rate is ordinary sampling variation. With
    `n_full_repeats=K > 0` we also draw K full-context samples at the SAME
    temperature as the ablations (also for single-pass P1) and record
    r_full = Pr_T(answer_full != a0). Note r_full is constant across sources of
    one instance: subtracting it does not change the ranking; it calibrates the
    signal and supports accept / abstain rules.
    `measure_full_noise=True` is kept as an alias for K = N (N > 1).
    `repeat` selects an independent measurement (fresh cache namespace and seeds).
    """
    strategy = get_strategy(method.prompting)
    sampling = SamplingSpec.build(method.sampling, n_samples)

    # Baseline: full context. Always a single deterministic draw -- it is the
    # reference every ablation is compared against, so it must not itself vary.
    base_prompt = strategy.build(inst, exclude=None, verbalize=False)
    base_sampling = SamplingSpec.build("single_pass")
    base_obs, calls = collect_observations(
        backend, base_prompt, strategy, base_sampling, cfg, cache, repeat=repeat
    )
    baseline = base_obs[0]

    failures = _count_failures(base_obs)
    n_obs = len(base_obs)

    ablated: dict[int, list[ParsedObservation]] = {}
    if baseline.ok:
        def _ablate(s):
            prompt = strategy.build(inst, exclude=s.idx, verbalize=False)
            return s.idx, collect_observations(
                backend, prompt, strategy, sampling, cfg, cache, repeat=repeat
            )

        # The M ablations are independent, so they parallelize cleanly. This is
        # where the O(M*N) cost lives, so it is the loop worth fanning out when
        # the server has multiple replicas (vLLM data_parallel_size>1). The
        # baseline above stays sequential -- every ablation compares against it.
        if inner_workers and inner_workers > 1 and len(inst.sources) > 1:
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=inner_workers) as ex:
                for idx, (obs, c) in ex.map(_ablate, inst.sources):
                    ablated[idx] = obs
                    calls += c
                    failures += _count_failures(obs)
                    n_obs += len(obs)
        else:
            for s in inst.sources:
                _, (obs, c) = _ablate(s)
                ablated[s.idx] = obs
                calls += c
                failures += _count_failures(obs)
                n_obs += len(obs)

    full_change_rate = None
    if measure_full_noise and not n_full_repeats and sampling.n > 1:
        n_full_repeats = sampling.n
    if n_full_repeats and baseline.ok:
        from ..utils.parsing import normalize_answer
        noise_sampling = SamplingSpec(f"full_repeats@{sampling.name}", int(n_full_repeats),
                                      sampling.temperature)
        # separate namespace from the method's own draws of this repeat
        full_obs, c = collect_observations(
            backend, base_prompt, strategy, noise_sampling, cfg, cache,
            repeat=FULL_NOISE_REPEAT_OFFSET + repeat,
        )
        calls += c
        n_obs += len(full_obs)
        failures += _count_failures(full_obs)
        usable = [o for o in full_obs if o.ok and o.answer is not None]
        if usable:
            a0 = normalize_answer(baseline.answer)
            full_change_rate = sum(normalize_answer(o.answer) != a0 for o in usable) / len(usable)

    effective_beta = beta if method.aggregation == "uncertainty" else 0.0
    phi = aggregate_perturbation(
        baseline, ablated, M=inst.M, beta=effective_beta
    )
    answer_phi = (
        aggregate_perturbation(baseline, ablated, M=inst.M, beta=0.0)
        if effective_beta else phi
    )

    return AttributionResult(
        qid=inst.qid,
        method=method.mid,
        phi=phi,
        ranking=to_ranking(phi),
        pred_set=to_set(phi, tau=tau),
        gold=inst.gold_indices,
        n_calls=calls,
        empty_prediction=is_empty_prediction(phi, tau=tau),
        parse_failures=failures,
        n_observations=n_obs,
        baseline_answer=baseline.answer,
        meta={
            "n_hop": inst.n_hop, "M": inst.M, "baseline_ok": baseline.ok,
            "invalid_reference": not baseline.ok,
            **signal_fields(phi, tau),
            # answer-change evidence alone (P5 also adds a confidence-drop term)
            "answer_change_signal": bool(np.any(answer_phi > 0)),
            "answer_phi": [float(x) for x in answer_phi],
            # raw ablated answers, so text-similarity scorers (MExGen-LOO) can
            # re-score without new calls
            "ablated_answers": {int(i): [o.answer if o.ok else None for o in obs]
                                for i, obs in ablated.items()},
            "full_context_change_rate": full_change_rate,
            "n_full_repeats": int(n_full_repeats or 0),
            "ablation_temperature": sampling.temperature,
            "repeat": repeat,
        },
    )


def run_method(inst: Instance, method: MethodSpec, backend: Backend, **kw):
    fn = run_verbalize if method.is_verbalize else run_perturbation
    # Route only the kwargs each pipeline accepts.
    allowed = {"cfg", "n_samples", "tau", "cache", "repeat"}
    allowed |= {"lam"} if method.is_verbalize else {
        "beta", "inner_workers", "measure_full_noise", "n_full_repeats"}
    unknown = set(kw) - allowed - {"lam", "beta", "inner_workers", "measure_full_noise", "n_full_repeats"}
    if unknown:
        raise TypeError(f"run_method: unknown arguments {sorted(unknown)}")
    return fn(inst, method, backend, **{k: v for k, v in kw.items() if k in allowed})
