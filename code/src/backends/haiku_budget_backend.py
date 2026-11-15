"""Cost-tracking, budget-capped backend for the claude-3-haiku experiment,
using an OpenAI-compatible endpoint (e.g. OmniGate).

The endpoint is OpenAI-format: an OpenAI client pointed at a custom base_url,
calling chat.completions.create with a model like "anthropic/claude-3-haiku".
Usage is reported in OpenAI fields (prompt_tokens / completion_tokens), which we
convert to dollars at the haiku rate (input $1/M, output $5/M).

The hard budget ceiling is the whole point: every call reads real token usage,
accumulates spend, and raises BudgetExceeded the instant a call would cross the
ceiling, so a runaway script stops itself rather than draining the account.

Configure via arguments or environment:
  base_url : OMNIGATE_BASE_URL or passed in (default https://api.ominigate.ai/v1)
  api_key  : OMNIGATE_API_KEY / OPENAI_API_KEY or passed in
  model    : default "anthropic/claude-3-haiku"
"""
from __future__ import annotations

import os
import threading
import time

from .base import Backend, GenConfig


class BudgetExceeded(RuntimeError):
    """Raised when a call would exceed the configured dollar budget."""


class CostTrackedHaikuBackend(Backend):
    # claude-3-haiku pricing (USD per token)
    PRICE_IN = 1.0 / 1_000_000
    PRICE_OUT = 5.0 / 1_000_000

    def __init__(
        self,
        model: str = "anthropic/claude-3-haiku",
        budget_usd: float = 5.0,
        base_url: str | None = None,
        api_key: str | None = None,
        max_retries: int = 4,
        timeout: float = 180.0,
        stop_margin: float = 0.05,
        price_in: float | None = None,
        price_out: float | None = None,
    ):
        from openai import OpenAI

        self.name = model
        self.model = model
        self.budget = budget_usd
        self.stop_margin = stop_margin
        self.spent = 0.0
        self._lock = threading.Lock()
        self.n_calls = 0
        self.tokens_in = 0
        self.tokens_out = 0
        self.max_retries = max_retries
        self.supports_seed = False
        if price_in is not None:
            self.PRICE_IN = price_in
        if price_out is not None:
            self.PRICE_OUT = price_out
        self.client = OpenAI(
            base_url=base_url
            or os.environ.get("OMNIGATE_BASE_URL", "https://api.ominigate.ai/v1"),
            api_key=api_key
            or os.environ.get("OMNIGATE_API_KEY")
            or os.environ.get("OPENAI_API_KEY"),
            timeout=timeout,
        )

    def _cost(self, tin: int, tout: int) -> float:
        return tin * self.PRICE_IN + tout * self.PRICE_OUT

    def remaining(self) -> float:
        return self.budget - self.spent

    def generate(self, messages, cfg: GenConfig, seed: int | None = None) -> str:
        # Refuse to start a call once we are at the ceiling (atomic check).
        with self._lock:
            if self.spent >= self.budget - self.stop_margin:
                raise BudgetExceeded(
                    f"budget ceiling reached: spent ${self.spent:.4f} of ${self.budget:.2f}"
                )

        # OpenAI chat format: system stays inline as a message with role=system.
        # Our prompts are already role-tagged dicts, so pass them through.
        msgs = [{"role": m["role"], "content": m["content"]} for m in messages]

        last = None
        for attempt in range(self.max_retries):
            try:
                kw = dict(
                    model=self.model,
                    messages=msgs,
                    max_tokens=cfg.max_tokens,
                    temperature=min(cfg.temperature, 1.0),
                )
                if cfg.top_p < 1.0:
                    kw["top_p"] = cfg.top_p
                resp = self.client.chat.completions.create(**kw)
                # OpenAI-format usage: prompt_tokens / completion_tokens
                u = getattr(resp, "usage", None)
                if u is not None:
                    tin = getattr(u, "prompt_tokens", 0) or 0
                    tout = getattr(u, "completion_tokens", 0) or 0
                else:
                    tin = tout = 0
                with self._lock:
                    self.tokens_in += tin
                    self.tokens_out += tout
                    self.spent += self._cost(tin, tout)
                    self.n_calls += 1
                return resp.choices[0].message.content or ""
            except BudgetExceeded:
                raise
            except Exception as e:
                last = e
                # On the very first call, surface the error immediately with detail
                # so misconfiguration (bad base_url, missing key, unexpected
                # response shape) is diagnosable instead of silently retried.
                if self.n_calls == 0 and attempt == 0:
                    import sys
                    print(f"[haiku backend] first call failed: {type(e).__name__}: {e}",
                          file=sys.stderr)
                time.sleep(min(2 ** attempt, 16))
        raise RuntimeError(
            f"{self.model}: generation failed after {self.max_retries} retries. "
            f"Last error: {type(last).__name__}: {last}. "
            f"Check --base-url ({self.client.base_url}) and API key."
        )

    def summary(self) -> dict:
        return {
            "model": self.model,
            "n_calls": self.n_calls,
            "tokens_in": self.tokens_in,
            "tokens_out": self.tokens_out,
            "spent_usd": round(self.spent, 4),
            "budget_usd": self.budget,
            "remaining_usd": round(self.remaining(), 4),
        }

    def close(self) -> None:
        pass
