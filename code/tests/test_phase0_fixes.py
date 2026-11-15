"""Tests for the ICDE-revision fixes (audit items E1, E3, E4).

E1: explicit signal fields instead of the overloaded `empty_prediction`.
E3: temperature-matched full-context noise measurement for perturbation.
E4: cache keys include the endpoint/decoding fingerprint and a repeat index.
"""
import json
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.backends.base import GenConfig
from src.pipelines.registry import METHODS
from src.pipelines.runner import run_method, signal_fields
from src.utils.cache import QueryCache, _key

from test_pipelines import MockBackend, make_instance


# ---------------------------------------------------------------- E1
def test_signal_fields_distinguish_all_zero_from_below_tau():
    assert signal_fields(np.zeros(4)) == {
        "all_zero": True, "reaches_tau": False, "below_tau_nonzero": False, "unique_max": False}
    f = signal_fields(np.array([0.0, 0.33, 0.0, 0.0]))
    assert f["below_tau_nonzero"] and not f["all_zero"] and not f["reaches_tau"] and f["unique_max"]
    f = signal_fields(np.array([0.0, 1.0, 1.0, 0.0]))
    assert f["reaches_tau"] and not f["unique_max"]


def test_results_carry_signal_fields():
    inst = make_instance(M=5, gold=(1, 3))
    for mid in ("V1", "P1"):
        res = run_method(inst, METHODS[mid], MockBackend(inst), cfg=GenConfig(), n_samples=3)
        for k in ("all_zero", "reaches_tau", "below_tau_nonzero", "unique_max"):
            assert k in res.meta
    assert res.meta["answer_change_signal"] is True


# ---------------------------------------------------------------- E4
def test_cache_key_separates_endpoints_configs_and_repeats():
    msgs = [{"role": "user", "content": "q"}]
    fp_a = {"base_url": "https://a/v1", "max_tokens": 64}
    fp_b = {"base_url": "https://b/v1", "max_tokens": 64}
    fp_c = {"base_url": "https://a/v1", "max_tokens": 256}
    k = lambda fp, rep=0: _key("m", msgs, 0.7, 0, fp, rep)
    assert k(fp_a) != k(fp_b)          # different endpoint
    assert k(fp_a) != k(fp_c)          # different decoding setting
    assert k(fp_a, 0) != k(fp_a, 1)    # independent repeat
    # legacy key ignores fingerprint and repeat (replays AAAI-27 cache only)
    assert _key("m", msgs, 0.7, 0, fp_a, 0, legacy=True) == _key("m", msgs, 0.7, 0, fp_b, 3, legacy=True)


def test_cache_roundtrip_stores_meta(tmp_path):
    c = QueryCache(path=str(tmp_path / "q.sqlite"))
    msgs = [{"role": "user", "content": "q"}]
    fp = {"base_url": "https://a/v1"}
    assert c.get("m", msgs, 0.01, 0, fp) is None
    c.put("m", msgs, 0.01, 0, "resp", fp, 0, {"prompt_tokens": 10, "completion_tokens": 2, "latency_s": 0.5})
    assert c.get("m", msgs, 0.01, 0, fp) == "resp"
    assert c.get("m", msgs, 0.01, 0, {"base_url": "https://b/v1"}) is None
    u = c.usage_summary()["m"]
    assert u["calls"] == 1 and u["prompt_tokens"] == 10 and u["completion_tokens"] == 2


# ---------------------------------------------------------------- E3
class NoisyBackend(MockBackend):
    """Like MockBackend, but at T > 0.3 the full-context answer flips with prob p."""

    def __init__(self, inst, p=0.4):
        super().__init__(inst)
        self.p = p
        self.rng = random.Random(0)

    def generate(self, messages, cfg, seed=None):
        out = json.loads(super().generate(messages, cfg, seed))
        if "short_answer" in out and cfg.temperature > 0.3 and self.rng.random() < self.p:
            out["short_answer"] = "Noise"
        return json.dumps(out)


def test_full_context_noise_is_measured_at_ablation_temperature():
    inst = make_instance(M=5, gold=(1, 3))
    be = NoisyBackend(inst, p=0.4)
    res = run_method(inst, METHODS["P2"], be, cfg=GenConfig(), n_samples=25, measure_full_noise=True)
    r = res.meta["full_context_change_rate"]
    assert r is not None and 0.15 < r < 0.65
    assert res.meta["ablation_temperature"] > 0.3
    # without the flag nothing extra is drawn or recorded
    res2 = run_method(inst, METHODS["P2"], NoisyBackend(inst, p=0.4), cfg=GenConfig(), n_samples=25)
    assert res2.meta["full_context_change_rate"] is None
    assert res.n_calls == res2.n_calls + 25


# ---------------------------------------------------------------- phase 0.1 regressions
class SeedRecordingBackend(MockBackend):
    supports_seed = True

    def __init__(self, inst):
        super().__init__(inst)
        self.seeds = []

    def generate(self, messages, cfg, seed=None):
        self.seeds.append(seed)
        return super().generate(messages, cfg, seed)


def test_public_entry_repeat_issues_fresh_requests(tmp_path):
    inst = make_instance(M=5, gold=(1, 3))
    cache = QueryCache(path=str(tmp_path / "q.sqlite"))
    be = SeedRecordingBackend(inst)
    r0 = run_method(inst, METHODS["V1"], be, cfg=GenConfig(), n_samples=3, cache=cache, repeat=0)
    r0b = run_method(inst, METHODS["V1"], be, cfg=GenConfig(), n_samples=3, cache=cache, repeat=0)
    r3 = run_method(inst, METHODS["V1"], be, cfg=GenConfig(), n_samples=3, cache=cache, repeat=3)
    assert r0.n_calls == 1 and r0b.n_calls == 0   # same repeat -> cache replay
    assert r3.n_calls == 1                        # new repeat -> fresh request
    assert r3.meta["repeat"] == 3


def test_independent_repeats_use_different_seeds(tmp_path):
    inst = make_instance(M=5, gold=(1, 3))
    be = SeedRecordingBackend(inst)
    run_method(inst, METHODS["V2"], be, cfg=GenConfig(), n_samples=3, repeat=0)
    s0 = list(be.seeds); be.seeds.clear()
    run_method(inst, METHODS["V2"], be, cfg=GenConfig(), n_samples=3, repeat=1)
    s1 = list(be.seeds)
    assert len(s0) == len(s1) == 3 and not set(s0) & set(s1)


def test_full_repeats_work_for_single_pass_p1():
    inst = make_instance(M=5, gold=(1, 3))
    res = run_method(inst, METHODS["P1"], MockBackend(inst), cfg=GenConfig(), n_samples=3, n_full_repeats=4)
    assert res.meta["full_context_change_rate"] == 0.0     # deterministic mock never changes
    assert res.meta["n_full_repeats"] == 4
    assert res.meta["ablation_temperature"] < 0.1
    assert len(res.meta["answer_phi"]) == inst.M


def test_unknown_argument_is_rejected():
    inst = make_instance(M=5, gold=(1, 3))
    import pytest
    with pytest.raises(TypeError):
        run_method(inst, METHODS["V1"], MockBackend(inst), cfg=GenConfig(), n_samples=1, repaet=2)


def test_resume_refuses_changed_configuration(tmp_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "run_method_script", os.path.join(os.path.dirname(__file__), "..", "scripts", "02_run_method.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = tmp_path / "V1.jsonl"
    m1 = {"method": "V1", "fingerprint": {"base_url": "https://a/v1", "max_tokens": 64}}
    mod.check_or_write_manifest(str(out), m1, allow_unmanifested=False)   # writes manifest
    out.write_text('{"qid": "x"}\n')
    mod.check_or_write_manifest(str(out), dict(m1), allow_unmanifested=False)  # same config: ok
    m2 = {"method": "V1", "fingerprint": {"base_url": "https://a/v1", "max_tokens": 256}}
    import pytest
    with pytest.raises(SystemExit):
        mod.check_or_write_manifest(str(out), m2, allow_unmanifested=False)
    legacy = tmp_path / "P1.jsonl"; legacy.write_text('{"qid": "y"}\n')
    with pytest.raises(SystemExit):   # rows but no manifest
        mod.check_or_write_manifest(str(legacy), m1, allow_unmanifested=False)
