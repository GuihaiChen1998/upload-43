"""Anthropic Messages API backend -- the closed-model column.

This is the setting the paper is actually about: text in, text out, no
likelihoods of any kind. It exists to show the methods run where no gray-box
alternative is available, so it participates in black-box metrics only.
"""
from __future__ import annotations

import os
import time

from .base import Backend, GenConfig


class AnthropicBackend(Backend):
    def __init__(
        self,
        model: str = "claude-haiku-4-5-20251001",
        api_key: str | None = None,
        max_retries: int = 4,
        timeout: float = 180.0,
    ):
        import anthropic

        self.name = model
        self.model = model
        self.max_retries = max_retries
        self.client = anthropic.Anthropic(
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"), timeout=timeout
        )
        self.supports_seed = False  # no seed parameter; N samples give the spread

    def generate(self, messages, cfg: GenConfig, seed: int | None = None) -> str:
        # The Messages API takes system separately; our prompts are user-only.
        msgs = [m for m in messages if m["role"] != "system"]
        system = "\n".join(m["content"] for m in messages if m["role"] == "system")

        last = None
        for attempt in range(self.max_retries):
            try:
                kw = dict(
                    model=self.model,
                    messages=msgs,
                    max_tokens=cfg.max_tokens,
                    temperature=min(cfg.temperature, 1.0),
                )
                if system:
                    kw["system"] = system
                if cfg.top_p < 1.0:
                    kw["top_p"] = cfg.top_p
                resp = self.client.messages.create(**kw)
                return "".join(b.text for b in resp.content if b.type == "text")
            except Exception as e:
                last = e
                time.sleep(min(2 ** attempt, 16))
        raise RuntimeError(f"{self.model}: generation failed after retries: {last}")
