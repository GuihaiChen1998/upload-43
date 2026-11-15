"""End-to-end pipeline tests against a scripted mock backend.

The mock imitates a model that genuinely depends on its gold sources: remove
one and the answer degrades. This lets us check that the perturbation pipeline
recovers the gold set, and that query counts match the Q(A) formula.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json

from src.backends.base import Backend, GenConfig
from src.data.schema import Instance, Source
from src.pipelines.registry import METHODS
from src.pipelines.runner import run_method
from src.stages.prompting import get_strategy


def make_instance(M=5, gold=(1, 3)):
    return Instance(
        qid="t1",
        question="Who is the spouse of the Green performer?",
        answer="Miquette Giraudy",
        sources=[
            Source(idx=i, title=f"T{i}", text=f"Body of source {i}.", is_gold=(i in gold))
            for i in range(M)
        ],
        dataset="mock",
        n_hop=2,
    )


class MockBackend(Backend):
    """Answers correctly iff every gold source is visible."""

    name = "mock"
    supports_seed = True

    def __init__(self, inst, verbalize_picks=None):
        self.inst = inst
        self.calls = 0
        self.verbalize_picks = verbalize_picks or [2, 4]  # 1-based, deliberately wrong

    def generate(self, messages, cfg: GenConfig, seed=None):
        self.calls += 1
        content = messages[-1]["content"]
        if '"likely"' in content:
            return json.dumps({"likely": "yes"})
        gold_titles = [f"T{i}" for i in self.inst.gold_indices]
        visible = all(f"] {t}\n" in content for t in gold_titles)
        ans = "Miquette Giraudy" if visible else "Unknown"
        if "attribute_source_numbers" in content:
            return json.dumps(
                {"short_answer": ans, "attribute_source_numbers": self.verbalize_picks}
            )
        return json.dumps({"short_answer": ans})


def test_perturbation_recovers_gold():
    inst = make_instance(M=5, gold=(1, 3))
    be = MockBackend(inst)
    res = run_method(
        inst, METHODS["P1"], be, cfg=GenConfig(), n_samples=1, tau=0.5, cache=None
    )
    assert sorted(res.pred_set) == [1, 3], res.pred_set
    assert res.top1_correct
    assert not res.empty_prediction
    assert res.parse_failures == 0


def test_perturbation_query_count_matches_formula():
    inst = make_instance(M=5)
    be = MockBackend(inst)
    res = run_method(inst, METHODS["P2"], be, cfg=GenConfig(), n_samples=3, cache=None)
    assert res.n_calls == 5 * 3 + 1 == be.calls        # (M*N + 1), kappa=1
    assert res.n_calls == METHODS["P2"].query_cost(M=5, N=3)


def test_self_probing_doubles_calls():
    inst = make_instance(M=4)
    be = MockBackend(inst)
    res = run_method(inst, METHODS["P3"], be, cfg=GenConfig(), n_samples=1, cache=None)
    assert res.n_calls == (4 * 1 + 1) * 2              # kappa=2


def test_verbalize_reports_its_own_pick():
    """The mock always claims sources 2 and 4 (1-based) -> indices 1 and 3."""
    inst = make_instance(M=5, gold=(1, 3))
    be = MockBackend(inst, verbalize_picks=[2, 4])
    res = run_method(inst, METHODS["V1"], be, cfg=GenConfig(), n_samples=1, cache=None)
    assert sorted(res.pred_set) == [1, 3]
    assert res.n_calls == 1


def test_verbalize_and_perturbation_can_disagree():
    """The central empirical question of the paper, in miniature."""
    inst = make_instance(M=5, gold=(1, 3))
    be_v = MockBackend(inst, verbalize_picks=[1, 5])   # claims 0 and 4
    v = run_method(inst, METHODS["V1"], be_v, cfg=GenConfig(), n_samples=1, cache=None)
    p = run_method(inst, METHODS["P1"], MockBackend(inst), cfg=GenConfig(),
                   n_samples=1, cache=None)
    assert sorted(v.pred_set) == [0, 4]
    assert sorted(p.pred_set) == [1, 3]
    assert set(v.pred_set) != set(p.pred_set)


def test_empty_prediction_when_nothing_matters():
    """A model ignoring its context yields no ablation effect at all."""
    inst = make_instance(M=4, gold=(0,))

    class Constant(MockBackend):
        def generate(self, messages, cfg, seed=None):
            self.calls += 1
            if '"likely"' in messages[-1]["content"]:
                return json.dumps({"likely": "yes"})
            return json.dumps({"short_answer": "Always The Same"})

    res = run_method(inst, METHODS["P1"], Constant(inst), cfg=GenConfig(),
                     n_samples=1, cache=None)
    assert res.empty_prediction
    assert len(res.pred_set) == 1        # argmax fallback keeps top-1 defined


def test_cot_perturbation_is_unbuildable():
    inst = make_instance()
    try:
        get_strategy("cot").build(inst, exclude=None, verbalize=False)
    except ValueError as e:
        assert "excluded by design" in str(e)
    else:
        raise AssertionError("CoT x perturbation should raise")


def test_ablation_renumbers_without_gaps():
    inst = make_instance(M=4)
    ctx = inst.render_context(exclude=1)
    assert "[1]" in ctx and "[2]" in ctx and "[3]" in ctx and "[4]" not in ctx
    assert inst.surviving_indices(exclude=1) == [0, 2, 3]


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")
