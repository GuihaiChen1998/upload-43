"""Trivial baselines -- paper Sec. 5.3, lower bounds.

random:     uniform pick over sources. On HotpotQA (M=10, 2 gold) top-1 is
            ~20%; on MuSiQue it rises with hop count. Must be reported next to
            absolute scores or the numbers get misread.
positional: always the first source. Detects position bias in the dataset --
            if "always pick paragraph 1" scores well, the benchmark leaks
            positional signal.

These produce AttributionResult objects so they flow through the same metrics
and tables as the real methods. They cost zero queries.
"""
from __future__ import annotations

import random as _random

import numpy as np

from ..data.schema import Instance
from ..pipelines.runner import AttributionResult


def _result(inst: Instance, phi: np.ndarray, method: str) -> AttributionResult:
    from ..stages.aggregation import to_ranking, to_set
    return AttributionResult(
        qid=inst.qid,
        method=method,
        phi=phi,
        ranking=to_ranking(phi),
        pred_set=to_set(phi, tau=0.5),
        gold=inst.gold_indices,
        n_calls=0,
        empty_prediction=False,
        parse_failures=0,
        n_observations=0,
        meta={"n_hop": inst.n_hop, "M": inst.M},
    )


def run_random(inst: Instance, seed: int = 0) -> AttributionResult:
    rng = _random.Random(f"{inst.qid}-{seed}")
    phi = np.array([rng.random() for _ in range(inst.M)])
    return _result(inst, phi, "random")


def run_positional(inst: Instance) -> AttributionResult:
    phi = np.linspace(1.0, 0.0, inst.M)  # first source ranks highest
    return _result(inst, phi, "positional")
