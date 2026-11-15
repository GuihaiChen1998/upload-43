"""Regression tests built from the worked examples in the design notes."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np

from src.stages.aggregation import (
    aggregate_perturbation, aggregate_verbalize, is_empty_prediction,
    to_ranking, to_set,
)
from src.pipelines.registry import InfeasibleMethod, METHODS, validate
from src.utils.parsing import ParsedObservation as PO


def obs(answer=None, sources=None, likely=None, ok=True):
    return PO(answer=answer, sources=sources, likely=likely, ok=ok)


def test_verbalize_marginalises_over_source():
    """6 samples: {Obama,5},{James,3},{Alvin,4}x3,{James,4}.

    Keying votes on the (answer, source) pair gives source 4 three votes.
    Marginalising over the source field gives it four -- the {James,4} sample
    still supports source 4 even though its answer differs.
    """
    samples = [
        obs("Obama", [5]), obs("James", [3]), obs("Alvin", [4]),
        obs("Alvin", [4]), obs("Alvin", [4]), obs("James", [4]),
    ]
    phi = aggregate_verbalize(samples, M=6, surviving=list(range(6)), lam=1.0)
    assert phi[3] == 4.0, phi          # source 4 -> index 3
    assert to_ranking(phi)[0] == 3


def test_verbalize_lambda_downweights_unsure():
    samples = [obs("X", [2], "yes"), obs("X", [2], "unsure"), obs("X", [3], "no")]
    surv = list(range(5))
    hard = aggregate_verbalize(samples, 5, surv, lam=0.0)   # only `yes` counts
    soft = aggregate_verbalize(samples, 5, surv, lam=0.5)
    assert hard[1] == 1.0 and soft[1] == 1.5
    assert hard[2] == 0.0 and soft[2] == 0.0                # `no` always zero


def test_perturbation_majority_counts():
    """Baseline Tim. Source 0 changes 2/3 times, source 1 changes 3/3."""
    base = obs("Tim")
    ablated = {
        0: [obs("Peter"), obs("Tim"), obs("James")],
        1: [obs("Rose"), obs("Bob"), obs("Peter")],
    }
    phi = aggregate_perturbation(base, ablated, M=2, beta=0.0)
    assert abs(phi[0] - 2 / 3) < 1e-9
    assert phi[1] == 1.0
    assert sorted(to_set(phi, tau=0.5)) == [0, 1]


def test_perturbation_self_probing_example():
    """Baseline (Tim, unsure). Source 0 marked important 1/4, source 1 3/4."""
    base = obs("Tim", likely="unsure")
    ablated = {
        0: [obs("Peter", likely="unsure"), obs("Tim", likely="yes"),
            obs("Tim", likely="unsure"), obs("Tim", likely="yes")],
        1: [obs("Sam", likely="unsure"), obs("Tim", likely="yes"),
            obs("Bob", likely="unsure"), obs("Andy", likely="no")],
    }
    phi = aggregate_perturbation(base, ablated, M=2, beta=0.0)
    assert phi[0] == 0.25 and phi[1] == 0.75
    assert to_set(phi, tau=0.5) == [1]


def test_confidence_drop_adds_in_same_direction():
    """A confident baseline that becomes unsure after ablation gains score.

    Direction matters: `unsure` after ablation is evidence the source was
    load-bearing, so it must add rather than discount.
    """
    base = obs("Tim", likely="yes")
    ablated = {0: [obs("Tim", likely="unsure")]}   # answer unchanged
    plain = aggregate_perturbation(base, ablated, M=1, beta=0.0)
    withaux = aggregate_perturbation(base, ablated, M=1, beta=0.3)
    assert plain[0] == 0.0
    assert withaux[0] > 0.0        # picked up an otherwise invisible signal


def test_answer_normalisation_is_conservative():
    base = obs("The Beatles")
    ablated = {0: [obs("beatles")], 1: [obs("Rolling Stones")]}
    phi = aggregate_perturbation(base, ablated, M=2)
    assert phi[0] == 0.0           # casing/article only -> unchanged
    assert phi[1] == 1.0


def test_empty_prediction_detected_but_top1_still_defined():
    phi = np.array([0.0, 0.33, 0.0])
    assert is_empty_prediction(phi, tau=0.5)
    assert to_set(phi, tau=0.5) == [1]     # argmax fallback


def test_registry_rejects_the_three_na_classes():
    for bad, why in [
        (("verbalize", "vanilla", "multi_sample", "direct"), "STRUCTURAL"),
        (("verbalize", "vanilla", "multi_sample", "uncertainty"), "FIELD"),
        (("perturbation", "cot", "single_pass", "direct"), "PRINCIPLED"),
    ]:
        try:
            validate(*bad)
        except InfeasibleMethod as e:
            assert why in str(e)
        else:
            raise AssertionError(f"{bad} should have been rejected")


def test_method_space_is_asymmetric():
    v = [m for m in METHODS.values() if m.is_verbalize]
    p = [m for m in METHODS.values() if not m.is_verbalize]
    assert len(v) == 7 and len(p) == 5     # the asymmetry of Sec. 4.5
    assert len(METHODS) == 12


def test_query_cost_formula():
    v2, p4 = METHODS["V2"], METHODS["P4"]
    assert v2.query_cost(M=10, N=5) == 5              # N * 1
    assert p4.query_cost(M=10, N=5) == (10 * 5 + 1) * 2   # (MN+1) * 2





def _res(qid, ranking, pred, gold):
    import numpy as np
    from src.pipelines.runner import AttributionResult
    return AttributionResult(qid=qid, method="X", phi=np.zeros(len(ranking)),
        ranking=ranking, pred_set=pred, gold=gold, n_calls=0,
        empty_prediction=False, parse_failures=0, n_observations=0)


def test_overlap_with_baseline():
    from src.eval.metrics import overlap_with_baseline
    # method and baseline agree perfectly on qid a, disagree on qid b
    method = [_res("a", [0,1,2,3], [0], [0]), _res("b", [3,2,1,0], [3], [0])]
    base   = [_res("a", [0,1,2,3], [0], [0]), _res("b", [0,1,2,3], [0], [0])]
    ov = overlap_with_baseline(method, base)
    assert ov["n"] == 2
    assert ov["top1_agreement"] == 0.5          # a agrees, b does not
    assert ov["rank_correlation"] is not None
    assert -1.0 <= ov["rank_correlation"] <= 1.0


def test_spearman_extremes():
    from src.eval.metrics import _spearman
    assert abs(_spearman([0,1,2,3], [0,1,2,3]) - 1.0) < 1e-9   # identical
    assert abs(_spearman([0,1,2,3], [3,2,1,0]) + 1.0) < 1e-9   # reversed


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")
