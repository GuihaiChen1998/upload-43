"""Prompting stage (pi) -- paper Sec. 4.2.

Three strategies: vanilla, self-probing, chain-of-thought. All impose the
structured-output constraint. Each strategy knows how many turns it needs and
which fields it expects back, so the sampling stage can stay generic.
"""
from __future__ import annotations

from dataclasses import dataclass

from ..data.schema import Instance

# --- Output schemas -------------------------------------------------------
# Sources are requested as a 1-based integer list. Earlier drafts used a
# "{k}-th" string form; plain integers cut the parse failure rate because
# models emit "5th"/"fifth"/"Source 5" inconsistently for ordinal formats.

_SCHEMA_WITH_SOURCES = (
    'Respond with ONLY a JSON object, no other text:\n'
    '{"short_answer": "<the shortest possible answer: a single entity name, a '
    'number, or yes/no — no explanatory phrases>", '
    '"attribute_source_numbers": [<1-based integers of the sources you relied on>]}'
)

_SCHEMA_ANSWER_ONLY = (
    'Respond with ONLY a JSON object, no other text:\n'
    '{"short_answer": "<the shortest possible answer: a single entity name, a '
    'number, or yes/no — no explanatory phrases>"}'
)

_SCHEMA_LIKELY = (
    'Respond with ONLY a JSON object, no other text:\n'
    '{"likely": "yes" or "no" or "unsure"}'
)

_BASE = (
    "Answer the question using only the numbered sources below.\n\n"
    "Sources:\n{context}\n\n"
    "Question: {question}\n\n"
)

_COT_PREFIX = (
    "Think through the question step by step first, then give your final "
    "answer.\n\n"
)

_COT_SUFFIX = (
    "\n\nAfter your reasoning, end your response with the JSON object and "
    "nothing after it."
)


@dataclass
class PromptSpec:
    """What one prompting strategy asks for, in a backend-agnostic form."""

    messages: list[dict]           # first-turn messages
    expect_sources: bool
    expect_likely: bool = False
    followup: str | None = None    # second-turn user message, if any


class PromptingStrategy:
    name: str
    n_turns: int = 1

    def build(self, inst: Instance, exclude: int | None, verbalize: bool) -> PromptSpec:
        raise NotImplementedError

    def followup_for(self, first_sources: list[int] | None) -> str | None:
        return None


class Vanilla(PromptingStrategy):
    name = "vanilla"
    n_turns = 1

    def build(self, inst, exclude, verbalize):
        schema = _SCHEMA_WITH_SOURCES if verbalize else _SCHEMA_ANSWER_ONLY
        content = _BASE.format(
            context=inst.render_context(exclude=exclude), question=inst.question
        ) + schema
        return PromptSpec(
            messages=[{"role": "user", "content": content}],
            expect_sources=verbalize,
        )


class SelfProbing(PromptingStrategy):
    """Two turns: answer, then challenge the first turn.

    The probe target differs by paradigm (Sec. 4.2). Verbalize challenges the
    ATTRIBUTION ("was it really source k?"); perturbation challenges the ANSWER.
    Asking the generic "are you sure?" in the verbalize case would make the
    model assess answer correctness, and the resulting confidence would say
    nothing about attribution quality.
    """

    name = "self_probing"
    n_turns = 2

    def build(self, inst, exclude, verbalize):
        base = Vanilla().build(inst, exclude, verbalize)
        return PromptSpec(
            messages=base.messages,
            expect_sources=verbalize,
            expect_likely=True,
        )

    def followup_for(self, first_sources):
        if first_sources:
            if len(first_sources) == 1:
                ref = f"source {first_sources[0]}"
            else:
                ref = "sources " + ", ".join(str(s) for s in first_sources)
            return (
                f"Are you sure your answer was based on {ref}? "
                + _SCHEMA_LIKELY
            )
        return "Are you sure about the above answer? " + _SCHEMA_LIKELY


class ChainOfThought(PromptingStrategy):
    """CoT. Verbalize pipeline only -- see Sec. 4.5 for the exclusion argument.

    The registry enforces this; the guard here is a second line of defence.
    """

    name = "cot"
    n_turns = 1

    def build(self, inst, exclude, verbalize):
        if not verbalize:
            raise ValueError(
                "CoT x perturbation is excluded by design (Assumption 1); "
                "self-generated reasoning drifts under ablation."
            )
        content = (
            _COT_PREFIX
            + _BASE.format(
                context=inst.render_context(exclude=exclude),
                question=inst.question,
            )
            + _SCHEMA_WITH_SOURCES
            + _COT_SUFFIX
        )
        return PromptSpec(
            messages=[{"role": "user", "content": content}],
            expect_sources=True,
        )


STRATEGIES = {
    "vanilla": Vanilla,
    "self_probing": SelfProbing,
    "cot": ChainOfThought,
}


def get_strategy(name: str) -> PromptingStrategy:
    if name not in STRATEGIES:
        raise KeyError(f"unknown prompting strategy {name!r}")
    return STRATEGIES[name]()


# --- Public helpers for scripts that build ad-hoc prompts (e.g. the stability
# check needs a free-form condition that no strategy produces). Exposing these
# avoids reaching into module privates from outside.

def build_answer_prompt(inst: Instance, *, structured: bool, cot: bool) -> str:
    body = _BASE.format(context=inst.render_context(), question=inst.question)
    if cot:
        if not structured:
            raise ValueError("cot condition is only defined with structured output")
        return _COT_PREFIX + body + _SCHEMA_ANSWER_ONLY + _COT_SUFFIX
    if structured:
        return body + _SCHEMA_ANSWER_ONLY
    return body + "Answer the question."
