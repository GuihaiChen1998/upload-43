"""OpenAI-compatible backend, used for vLLM-served open-weight models.

Thinking mode is disabled explicitly via chat_template_kwargs. This is not
cosmetic: self-generated reasoning is context that drifts under ablation, so
leaving it on would inflate epsilon in Assumption 1 and quietly invalidate the
whole perturbation pipeline. The leak check in utils.parsing is the backstop.
"""
from __future__ import annotations

import time

from .base import Backend, GenConfig


class OpenAIBackend(Backend):
    def __init__(
        self,
        model: str,
        base_url: str = "http://localhost:8000/v1",
        api_key: str = "EMPTY",
        disable_thinking: bool = True,
        send_thinking_kwarg: bool = True,
        max_retries: int = 4,
        timeout: float = 180.0,
        fingerprint_base_url: str | None = None,
    ):
        from openai import OpenAI

        self.name = model
        self.model = model
        self.base_url = base_url
        # A stand-in endpoint for the same declared model (user decision 2026-11-03:
        # trust that every endpoint's declared model is identical). With this set,
        # the manifest and the query cache see the original endpoint, so a run can
        # continue in the same result files and reuse that endpoint's cached answers.
        self.fingerprint_base_url = fingerprint_base_url
        self.disable_thinking = disable_thinking
        # Third-party gateways may reject unknown extra_body fields; let a config
        # turn the chat_template_kwargs injection off for those endpoints.
        self.send_thinking_kwarg = send_thinking_kwarg
        self.max_retries = max_retries
        self.client = OpenAI(base_url=base_url, api_key=api_key, timeout=timeout)
        self.supports_seed = True

    def _extra_body(self, cfg: GenConfig) -> dict:
        body = {}
        if self.send_thinking_kwarg:
            body["top_k"] = cfg.top_k
            if self.disable_thinking:
                # Qwen3 honours this through vLLM's chat template kwargs. Models
                # without a thinking mode ignore it harmlessly. Third-party
                # gateways may not, hence send_thinking_kwarg.
                body["chat_template_kwargs"] = {"enable_thinking": False}
        body.update(cfg.extra)
        return body

    def fingerprint(self, cfg: GenConfig) -> dict:
        fp = super().fingerprint(cfg)
        if self.fingerprint_base_url:
            fp["base_url"] = self.fingerprint_base_url
        fp.update({
            "send_thinking_kwarg": self.send_thinking_kwarg,
            "disable_thinking": self.disable_thinking,
            "extra_body": self._extra_body(cfg),
        })
        return fp

    def generate(self, messages, cfg: GenConfig, seed: int | None = None) -> str:
        return self.generate_with_meta(messages, cfg, seed)[0]

    def generate_with_meta(self, messages, cfg: GenConfig, seed: int | None = None):
        """Returns (text, meta). meta carries token usage, latency and retries,
        so that query cost can be reported from logs rather than estimated."""
        last = None
        for attempt in range(self.max_retries):
            try:
                kw = dict(
                    model=self.model,
                    messages=messages,
                    temperature=cfg.temperature,
                    max_tokens=cfg.max_tokens,
                )
                if cfg.top_p is not None:
                    kw["top_p"] = cfg.top_p
                body = self._extra_body(cfg)
                if body:
                    kw["extra_body"] = body
                if cfg.presence_penalty:
                    kw["presence_penalty"] = cfg.presence_penalty
                if seed is not None and self.send_thinking_kwarg:
                    # Local vLLM honours seed; some gateways reject it.
                    kw["seed"] = seed
                t0 = time.time()
                resp = self.client.chat.completions.create(**kw)
                u = getattr(resp, "usage", None)
                details = getattr(u, "completion_tokens_details", None) if u else None
                meta = {
                    "latency_s": round(time.time() - t0, 3),
                    "retries": attempt,
                    "prompt_tokens": getattr(u, "prompt_tokens", None) if u else None,
                    "completion_tokens": getattr(u, "completion_tokens", None) if u else None,
                    "reasoning_tokens": getattr(details, "reasoning_tokens", None) if details else None,
                    "served_model": getattr(resp, "model", None),
                    # the endpoint that actually answered (differs from the
                    # fingerprint's base_url when fingerprint_base_url is set)
                    "served_base_url": self.base_url,
                    "response_id": getattr(resp, "id", None),
                    "finish_reason": getattr(resp.choices[0], "finish_reason", None),
                    "request": {"temperature": cfg.temperature, "top_p": cfg.top_p,
                                "max_tokens": cfg.max_tokens},
                }
                return resp.choices[0].message.content or "", meta
            except Exception as e:  # transient server / rate-limit errors
                last = e
                time.sleep(min(2 ** attempt, 30))
        raise RuntimeError(f"{self.model}: generation failed after retries: {last}")
