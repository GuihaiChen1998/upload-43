"""Tests for the phase-2 subset attributors (RM, LOI, MExGen-LOO)."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.backends.base import GenConfig
from src.pipelines.registry import METHODS
from src.pipelines.runner import run_method
from src.pipelines.subset import (
    draw_masks, mexgen_loo_from_p1, run_leave_one_in, run_random_mask, subset_prompt, token_f1,
)
from src.stages.prompting import Vanilla

from test_pipelines import MockBackend, make_instance


class RedundantBackend(MockBackend):
    """Correct iff source 1 OR source 3 is visible (a duplicated fact)."""

    def generate(self, messages, cfg, seed=None):
        c = messages[-1]["content"]
        ok = "] T1\n" in c or "] T3\n" in c
        return json.dumps({"short_answer": "Miquette Giraudy" if ok else "Unknown"})


def test_masks_are_prefix_nested_and_never_full():
    a, b = draw_masks(10, 16, seed=7), draw_masks(10, 64, seed=7)
    assert (a == b[:16]).all()
    assert not b.all(axis=1).any()


def test_random_mask_recovers_conjunctive_gold():
    inst = make_instance(M=6, gold=(1, 3))
    res = run_random_mask(inst, MockBackend(inst), GenConfig(), K=64)
    assert set(res.ranking[:2]) == {1, 3}
    n_unique = len({tuple(m) for m in res.meta['masks']})
    assert res.n_calls == 1 + n_unique  # duplicate masks are sent once


def test_random_mask_credits_redundant_sources_where_loo_cannot():
    inst = make_instance(M=6, gold=(1, 3))
    p1 = run_method(inst, METHODS["P1"], RedundantBackend(inst), cfg=GenConfig(), n_samples=1)
    assert p1.meta["all_zero"]                       # removing either copy changes nothing
    rm = run_random_mask(inst, RedundantBackend(inst), GenConfig(), K=64)
    assert set(rm.ranking[:2]) == {1, 3} and rm.phi[1] > 0.1 and rm.phi[3] > 0.1


def test_leave_one_in_is_a_sufficiency_probe():
    inst = make_instance(M=5, gold=(1, 3))
    assert run_leave_one_in(inst, MockBackend(inst), GenConfig()).meta["all_zero"]
    res = run_leave_one_in(inst, RedundantBackend(inst), GenConfig())
    assert sorted(np.flatnonzero(res.phi)) == [1, 3]


def test_single_exclusion_mask_prompt_equals_loo_prompt():
    inst = make_instance(M=5, gold=(1, 3))
    keep = [0, 1, 3, 4]
    assert subset_prompt(inst, keep).messages == Vanilla().build(inst, exclude=2, verbalize=False).messages
    assert subset_prompt(inst, list(range(5))).messages == Vanilla().build(inst, None, False).messages


def test_mexgen_loo_rescoring_from_p1_row():
    inst = make_instance(M=5, gold=(1, 3))
    row = run_method(inst, METHODS["P1"], MockBackend(inst), cfg=GenConfig(), n_samples=1).to_json()
    out = mexgen_loo_from_p1(json.loads(json.dumps(row)), inst.gold_indices)
    assert set(out["pred_set"]) == {1, 3}
    assert token_f1("the Eiffel Tower", "Eiffel tower") == 1.0
    assert 0 < token_f1("1 522 miles", "1522 miles") < 1


def test_concurrent_samples_match_serial_draws(tmp_path):
    import src.stages.sampling as S
    from src.utils.cache import QueryCache
    from test_phase0_fixes import NoisyBackend
    inst = make_instance(M=5, gold=(1, 3))
    outs = []
    for w in (1, 5):
        S.SAMPLE_WORKERS = w
        try:
            r = run_method(inst, METHODS["V4"], NoisyBackend(inst), cfg=GenConfig(), n_samples=5,
                           cache=QueryCache(path=str(tmp_path / f"c{w}.sqlite")))
        finally:
            S.SAMPLE_WORKERS = 1
        outs.append((r.n_calls, r.n_observations))
    assert outs[0] == outs[1] == (10, 5)


def test_identical_prompts_are_sent_once():
    from src.pipelines.subset import _answers_for

    class Counting(MockBackend):
        n = 0

        def generate(self, messages, cfg, seed=None):
            Counting.n += 1
            return super().generate(messages, cfg, seed)

    inst = make_instance(M=5, gold=(1, 3))
    ps = [subset_prompt(inst, [0, 1, 3]), subset_prompt(inst, [0, 1, 3]), subset_prompt(inst, [1, 3])]
    obs, calls = _answers_for(ps, Counting(inst), GenConfig(), None, 0, 4)
    assert len(obs) == 3 and calls == 2 and Counting.n == 2 and obs[0].answer == obs[1].answer


def test_full_product_masks_make_banzhaf_unbiased_for_and():
    # AND of two sources: true Banzhaf value is [0.5, 0.5]. With all-kept masks
    # rejected the estimate collapses to [0, 0]; the product design recovers it.
    import numpy as np
    from src.pipelines.subset import banzhaf, draw_masks
    m = draw_masks(2, 4000, seed=1)
    y = m.all(1).astype(float)
    assert np.allclose(banzhaf(m, y), [0.5, 0.5], atol=0.05)
    mr = draw_masks(2, 400, seed=1, reject_full=True)
    assert np.allclose(banzhaf(mr, mr.all(1).astype(float)), [0, 0])
