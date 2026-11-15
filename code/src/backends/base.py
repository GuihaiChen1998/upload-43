"""Backend abstraction.

Every black-box method goes through `generate(messages, temperature, seed)`
and receives text. No backend in this module exposes logits -- that is the
point. Gray-box baselines live in src/baselines and use HF directly.

`generate_with_meta` additionally returns per-call bookkeeping (token usage,
latency) so that query cost can be reported from logs rather than estimated.
`fingerprint` describes everything about the endpoint and decoding setup that
can change the generated text; it is folded into the cache key so that two
endpoints or two decoding configurations never share cached responses.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class GenConfig:
    """Sampling knobs. Defaults follow the non-thinking recommendations of the
    Qwen3 card; Gemma has no thinking mode so the same values apply."""

    temperature: float = 0.01
    top_p: float = 0.8
    top_k: int = 20
    max_tokens: int = 256
    presence_penalty: float = 0.0
    extra: dict = field(default_factory=dict)


class Backend:
    name: str
    base_url: str = ""
    supports_seed: bool = False

    def generate(self, messages: list[dict], cfg: GenConfig, seed: int | None = None) -> str:
        raise NotImplementedError

    def generate_with_meta(
        self, messages: list[dict], cfg: GenConfig, seed: int | None = None
    ) -> tuple[str, dict]:
        """Default: wrap `generate` and record latency only."""
        t0 = time.time()
        text = self.generate(messages, cfg, seed=seed)
        return text, {"latency_s": round(time.time() - t0, 3)}

    def fingerprint(self, cfg: GenConfig) -> dict:
        """Everything except messages / temperature / sample index that can
        change the generated text. Subclasses add backend-specific switches."""
        return {
            "backend": type(self).__name__,
            "base_url": self.base_url,
            "top_p": cfg.top_p,
            "top_k": cfg.top_k,
            "max_tokens": cfg.max_tokens,
            "presence_penalty": cfg.presence_penalty,
            "extra": cfg.extra,
        }

    def close(self) -> None:
        pass
