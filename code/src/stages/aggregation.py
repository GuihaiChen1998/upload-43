"""Aggregation stage (alpha) -- paper Sec. 4.4.

Two formulas, one per paradigm. The three named aggregation strategies
(direct / consistency / uncertainty-aware) are parameter settings of these
same formulas, not separate methods -- see the table in Sec. 4.4.
"""
from __future__ import annotations

import numpy as np

from ..utils.parsing import ParsedObservation, normalize_answer

# Confidence map c(.) used for the auxiliary signal.
_C = {"yes": 1.0, "unsure": 0.5, "no": 0.0}


def _w(likely: str | None, lam: float) -> float:
    """Vote weight w(u): yes->1, unsure->lambda, no->0.

    A missing `likely` (vanilla prompting) carries no information, so it gets
    full weight -- otherwise vanilla would be silently penalised relative to
    self-probing.
    """
    if likely is None:
        return 1.0
    return {"yes": 1.0, "unsure": lam, "no": 0.0}[likely]


def aggregate_verbalize(
    observations: list[ParsedObservation],
    M: int,
    surviving: list[int],
    lam: float = 0.5,
) -> np.ndarray:
    """phi^V_i = sum_n w(u_n) * 1[i in r_n].

    Votes are marginalised over the source field only. An earlier design keyed
    votes on the (answer, source) pair, which fragments the count: a sample
    agreeing on the source but differing on the answer still carries
    attribution evidence and should not be discarded.

    `surviving` maps 1-based displayed numbers to 0-based original indices.
    """
    phi = np.zeros(M, dtype=float)
    for obs in observations:
        if not obs.ok or not obs.sources:
            continue
        weight = _w(obs.likely, lam)
        if weight == 0.0:
            continue
        for disp in set(obs.sources):  # dedupe within one response
            k = disp - 1
            if 0 <= k < len(surviving):
                phi[surviving[k]] += weight
    return phi


def aggregate_perturbation(
    baseline: ParsedObservation,
    ablated: dict[int, list[ParsedObservation]],
    M: int,
    beta: float = 0.0,
) -> np.ndarray:
    """phi^P_i = (1/N) sum_n ( 1[a_i^n != a_0] + beta * delta_u_i^n ).

    Primary signal: the answer changed. Auxiliary signal: self-reported
    confidence dropped RELATIVE TO BASELINE. The two are additive in the same
    direction -- removing a critical source leaves the model without grounds,
    so rising uncertainty reinforces the importance judgment rather than
    weakening it. Using a relative rather than absolute confidence avoids
    misreading instances whose baseline was already unsure.

    Counts are kept as a continuous score rather than thresholded here, so the
    same object supports both a ranking (top-k) and a set (threshold).
    """
    phi = np.zeros(M, dtype=float)
    if not baseline.ok or baseline.answer is None:
        return phi  # unusable baseline; caller should have filtered these

    a0 = normalize_answer(baseline.answer)
    c0 = _C.get(baseline.likely, 1.0) if baseline.likely else None

    for i, obs_list in ablated.items():
        usable = [o for o in obs_list if o.ok and o.answer is not None]
        if not usable:
            continue
        total = 0.0
        for o in usable:
            changed = 1.0 if normalize_answer(o.answer) != a0 else 0.0
            aux = 0.0
            if beta > 0.0 and c0 is not None and o.likely is not None:
                aux = max(0.0, c0 - _C[o.likely])
            total += changed + beta * aux
        phi[i] = total / len(usable)
    return phi


def to_set(phi: np.ndarray, tau: float = 0.5) -> list[int]:
    """Thresholded set prediction, with argmax fallback on the empty set.

    The fallback keeps top-1 accuracy defined everywhere; the empty-set rate is
    reported separately as a diagnostic (Sec. 6.5) precisely because the
    fallback hides it.
    """
    idx = [int(i) for i in np.nonzero(phi >= tau)[0]]
    if idx:
        return idx
    return [int(np.argmax(phi))] if phi.size else []


def is_empty_prediction(phi: np.ndarray, tau: float = 0.5) -> bool:
    """True iff NO score reaches tau (note: >= tau, matching `to_set`).

    This is NOT "the score vector is all zero": with N > 1 or a confidence term,
    a vector can be non-zero and informative yet stay below tau. Use
    `pipelines.runner.signal_fields` for the explicit breakdown.
    """
    return bool(phi.size) and not bool(np.any(phi >= tau))


def to_ranking(phi: np.ndarray) -> list[int]:
    """Descending order of importance; ties broken by index for determinism."""
    return [int(i) for i in np.lexsort((np.arange(phi.size), -phi))]
