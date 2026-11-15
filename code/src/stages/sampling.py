"""Sampling stage (sigma) -- paper Sec. 4.3.

single_pass: one sample at T=0.01.
multi_sample: N samples at a fixed temperature, N odd.

Temperature is deliberately NOT a distinguishing dimension between the two
strategies. Varying count and temperature together would confound their
contributions, and pooling samples drawn at different temperatures lets the
low-temperature ones dominate the mode -- the resulting "consistency" would
just be low-temperature behaviour. Temperature is swept separately as a
sensitivity analysis.
"""
from __future__ import annotations

from dataclasses import dataclass

from ..backends.base import Backend, GenConfig
from ..stages.prompting import PromptSpec, PromptingStrategy
from ..utils.cache import QueryCache
from ..utils.parsing import ParsedObservation, parse_observation

# Non-thinking defaults from the Qwen3 model card; Gemma has no thinking mode.
SINGLE_PASS_T = 0.01
MULTI_SAMPLE_T = 0.7
# seed = SEED_STRIDE * repeat + sample_idx, so repeats never share seeds as long
# as N < SEED_STRIDE.
SEED_STRIDE = 1000
# Concurrent draws per observation set (API backends). Set by the run script.
SAMPLE_WORKERS = 1


@dataclass
class SamplingSpec:
    name: str
    n: int
    temperature: float

    @staticmethod
    def build(strategy: str, n: int = 5) -> "SamplingSpec":
        if strategy == "single_pass":
            return SamplingSpec("single_pass", 1, SINGLE_PASS_T)
        if strategy == "multi_sample":
            if n % 2 == 0:
                raise ValueError(
                    f"multi_sample needs odd N to avoid ties in the "
                    f"perturbation majority rule; got N={n}"
                )
            return SamplingSpec("multi_sample", n, MULTI_SAMPLE_T)
        raise KeyError(f"unknown sampling strategy {strategy!r}")


def collect_observations(
    backend: Backend,
    prompt: PromptSpec,
    strategy: PromptingStrategy,
    sampling: SamplingSpec,
    cfg: GenConfig,
    cache: QueryCache | None = None,
    strict_thinking: bool = True,
    repeat: int = 0,
) -> tuple[list[ParsedObservation], int]:
    """Draw `sampling.n` observations. Returns (observations, n_api_calls).

    Handles the second turn of self-probing inline, since the follow-up
    question depends on what the first turn said.
    """
    cfg = GenConfig(**{**cfg.__dict__, "temperature": sampling.temperature})
    out: list[ParsedObservation] = []
    calls = 0
    # The fingerprint (endpoint + decoding settings) and `repeat` index enter the
    # cache key, so different endpoints / configs never share responses and an
    # independent repeated measurement is never served from cache.
    fp = backend.fingerprint(cfg)
    # Independent repeats must also differ in the seed sent to seed-honouring
    # backends; otherwise a new cache namespace would replay the same draw.
    seed_base = SEED_STRIDE * int(repeat)

    def _gen(msgs, i):
        text = cache.get(backend.name, msgs, cfg.temperature, i, fp, repeat) if cache else None
        if text is not None:
            return text, 0
        text, meta = backend.generate_with_meta(
            msgs, cfg, seed=(seed_base + i) if backend.supports_seed else None
        )
        meta = {**(meta or {}), "seed": (seed_base + i) if backend.supports_seed else None,
                "repeat": int(repeat), "sample_idx": i}
        if cache:
            cache.put(backend.name, msgs, cfg.temperature, i, text, fp, repeat, meta)
        return text, 1

    def _one(i):
        calls = 0
        msgs = list(prompt.messages)

        text, c = _gen(msgs, i)
        calls += c

        obs = parse_observation(
            text,
            expect_sources=prompt.expect_sources,
            expect_likely=False,  # first turn never carries `likely`
            strict_thinking=strict_thinking,
        )

        if prompt.expect_likely and strategy.n_turns == 2:
            followup = strategy.followup_for(obs.sources)
            msgs2 = msgs + [
                {"role": "assistant", "content": text},
                {"role": "user", "content": followup},
            ]
            text2, c = _gen(msgs2, i)
            calls += c

            probe = parse_observation(
                text2, expect_sources=False, expect_likely=True,
                strict_thinking=strict_thinking,
            )
            obs.likely = probe.likely
            # A parsed answer with an unparsable probe is still usable; the
            # weight function treats a missing `likely` as neutral.
            obs.raw = text + "\n<<<PROBE>>>\n" + text2

        return obs, calls

    # Samples are independent draws (distinct sample_idx / seed / cache key), so
    # they can be issued concurrently; order and cache keys are unchanged.
    if SAMPLE_WORKERS > 1 and sampling.n > 1:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=min(SAMPLE_WORKERS, sampling.n)) as ex:
            res = list(ex.map(_one, range(sampling.n)))
    else:
        res = [_one(i) for i in range(sampling.n)]
    out = [r[0] for r in res]
    calls = sum(r[1] for r in res)
    return out, calls
