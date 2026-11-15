"""Parsing of structured model outputs, with explicit failure accounting.

The structured-output constraint (paper Sec. 3.3) is what lets us decide
"did the answer change?" by string comparison instead of semantic equivalence
judging. That only holds if parsing is reliable, so every failure is counted
and reported rather than silently swallowed.
"""
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass

# Fenced code block, with or without a language tag.
_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)
# A <think>...</think> block. Should never appear once thinking is disabled;
# if it does, that is a configuration error we want to surface loudly.
_THINK = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
_THINK_OPEN = re.compile(r"<think>", re.IGNORECASE)


class ThinkingLeakError(RuntimeError):
    """Raised when a model emits reasoning despite thinking being disabled."""


@dataclass
class ParsedObservation:
    """One observation o = (a, r, u) from paper Sec. 3.3."""

    answer: str | None = None            # a: short_answer
    sources: list[int] | None = None     # r: 1-based as emitted by the model
    likely: str | None = None            # u: yes / no / unsure
    ok: bool = False
    raw: str = ""
    error: str | None = None


def _extract_json_blob(text: str) -> str | None:
    """Pull the most plausible JSON object out of a model response."""
    m = _FENCE.search(text)
    if m:
        text = m.group(1)
    start = text.find("{")
    if start < 0:
        return None
    # Scan for the matching close brace, respecting strings and escapes.
    depth, in_str, esc = 0, False, False
    for i, ch in enumerate(text[start:], start):
        if esc:
            esc = False
            continue
        if ch == "\\":
            esc = True
        elif ch == '"':
            in_str = not in_str
        elif not in_str:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start : i + 1]
    return None


def normalize_answer(s: str) -> str:
    """Canonical form for the string-equality test in the perturbation pipeline.

    Deliberately conservative: casing, surrounding articles, punctuation and
    whitespace only. We do NOT do stemming or synonym matching -- that would
    reintroduce the semantic-equivalence judgment the structured-output
    constraint exists to avoid.
    """
    s = unicodedata.normalize("NFKC", str(s)).lower().strip()
    s = re.sub(r"[\u2018\u2019\u201c\u201d]", "'", s)
    s = re.sub(r"^(the|a|an)\s+", "", s)
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _coerce_sources(v) -> list[int] | None:
    """Accept int, list, or strings like '3', '3rd', '[2, 5]'."""
    if v is None:
        return None
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return [v]
    if isinstance(v, str):
        nums = re.findall(r"\d+", v)
        return [int(n) for n in nums] if nums else None
    if isinstance(v, (list, tuple)):
        out = []
        for x in v:
            got = _coerce_sources(x)
            if got:
                out.extend(got)
        return out or None
    return None


_LIKELY_MAP = {
    "yes": "yes", "y": "yes", "true": "yes", "sure": "yes", "certain": "yes",
    "no": "no", "n": "no", "false": "no",
    "unsure": "unsure", "uncertain": "unsure", "maybe": "unsure",
    "not sure": "unsure", "unknown": "unsure",
}


def _coerce_likely(v) -> str | None:
    if v is None:
        return None
    key = str(v).strip().lower().strip(".!")
    return _LIKELY_MAP.get(key)


def parse_observation(
    text: str,
    expect_sources: bool = False,
    expect_likely: bool = False,
    strict_thinking: bool = True,
) -> ParsedObservation:
    """Parse one model response into a ParsedObservation.

    `expect_sources` / `expect_likely` declare which fields the prompting
    strategy asked for; a missing expected field is a parse failure.
    `strict_thinking` raises if a <think> block leaked through, which almost
    always means thinking mode was not actually disabled.
    """
    obs = ParsedObservation(raw=text)

    if strict_thinking and _THINK_OPEN.search(text or ""):
        raise ThinkingLeakError(
            "model emitted a <think> block; thinking mode is not disabled"
        )
    text = _THINK.sub("", text or "")

    blob = _extract_json_blob(text)
    if blob is None:
        obs.error = "no_json_object"
        return obs

    try:
        d = json.loads(blob)
    except json.JSONDecodeError:
        # One salvage attempt: single quotes and trailing commas are the two
        # most common deviations from strict JSON.
        try:
            fixed = re.sub(r",\s*([}\]])", r"\1", blob.replace("'", '"'))
            d = json.loads(fixed)
        except json.JSONDecodeError:
            obs.error = "malformed_json"
            return obs

    if not isinstance(d, dict):
        obs.error = "not_an_object"
        return obs

    lower = {str(k).lower(): v for k, v in d.items()}

    ans = lower.get("short_answer", lower.get("answer"))
    if ans is not None and not isinstance(ans, (dict, list)):
        obs.answer = str(ans).strip()

    obs.sources = _coerce_sources(
        lower.get("attribute_source_numbers", lower.get("attribute_source_number"))
    )
    obs.likely = _coerce_likely(lower.get("likely"))

    missing = []
    if obs.answer is None or obs.answer == "":
        missing.append("short_answer")
    if expect_sources and not obs.sources:
        missing.append("attribute_source_numbers")
    if expect_likely and obs.likely is None:
        missing.append("likely")

    if missing:
        obs.error = "missing:" + ",".join(missing)
        return obs

    obs.ok = True
    return obs
