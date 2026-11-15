"""Config loading. Merges base.yaml with per-model / per-dataset overrides and
builds the concrete objects (backend, GenConfig) the runner needs.
"""
from __future__ import annotations

import os

import yaml

from ..backends.base import GenConfig

_CONFIG_ROOT = os.environ.get("BBATTR_CONFIG_ROOT", "configs")


def _load_yaml(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_base() -> dict:
    return _load_yaml(os.path.join(_CONFIG_ROOT, "base.yaml"))


def load_model_config(name: str) -> dict:
    path = name if os.path.exists(name) else os.path.join(
        _CONFIG_ROOT, "models", f"{name}.yaml"
    )
    return _load_yaml(path)


def build_backend(model_cfg: dict):
    """Instantiate a backend from a model config. Imports are local so that a
    machine without, say, the anthropic package can still use the openai path."""
    backend = model_cfg.get("backend", "openai")
    if backend == "openai":
        from ..backends.openai_backend import OpenAIBackend
        import os as _os
        api_key = model_cfg.get("api_key", "EMPTY")
        # Allow ${ENV_VAR} indirection so keys stay out of the config files.
        if isinstance(api_key, str) and api_key.startswith("${") and api_key.endswith("}"):
            api_key = _os.environ.get(api_key[2:-1], "EMPTY")
        return OpenAIBackend(
            model=model_cfg["model"],
            base_url=model_cfg.get("base_url", "http://localhost:8000/v1"),
            api_key=api_key,
            disable_thinking=model_cfg.get("disable_thinking", True),
            send_thinking_kwarg=model_cfg.get("send_thinking_kwarg", True),
            max_retries=model_cfg.get("max_retries", 4),
            timeout=model_cfg.get("timeout", 180.0),
            fingerprint_base_url=model_cfg.get("fingerprint_base_url"),
        )
    if backend == "anthropic":
        from ..backends.anthropic_backend import AnthropicBackend
        return AnthropicBackend(model=model_cfg["model"])
    raise KeyError(f"unknown backend {backend!r}")


def build_gen_config(base: dict, model_cfg: dict) -> GenConfig:
    gen = dict(model_cfg.get("gen", {}))
    return GenConfig(
        temperature=base["sampling"]["single_pass_temperature"],
        top_p=gen["top_p"] if "top_p" in gen else 0.8,   # explicit null -> omit
        top_k=gen.get("top_k", 20),
        max_tokens=gen.get("max_tokens", 256),
        presence_penalty=gen.get("presence_penalty", 0.0),
    )
