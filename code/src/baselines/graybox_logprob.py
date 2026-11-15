"""Gray-box leave-one-out logprob-drop attribution, for VALIDATION ONLY.

This is deliberately NOT part of the black-box method space. It exists to answer
one question: are the gold supporting sources a reasonable proxy for the
contributive target phi*? We answer it by measuring, on open-weight models that
expose token logprobs, how much removing each source drops the log-probability of
the model's own answer -- the gray-box signal ContextCite/ARC-JSD are built on --
and then checking how well that ranking agrees with the gold-supporting-fact
ranking (scripts/08_validate_gold.py).

It is kept in src/baselines and uses its own scoring client so the black-box
backends in src/backends stay strictly text-only. Closed models (claude-3-haiku)
cannot be scored this way; that is expected -- validation runs on open models and
its conclusion (gold is/ isn't a good proxy) then justifies using gold uniformly,
including on the closed model.

Method (leave-one-out, no surrogate):
  1. Generate the answer a0 under the full context (greedy).
  2. Score log P(a0 | full context) by teacher-forcing a0 and summing its token
     logprobs.
  3. For each source s_i, score log P(a0 | context without s_i).
  4. drop_i = logP(full) - logP(without s_i). A large drop means removing s_i
     hurt the model's ability to produce its own answer, i.e. s_i was important.
The per-source drops are the attribution scores; we rank sources by them.

Scoring log P(answer | context) uses vLLM's `prompt_logprobs`: we send
prompt = <context+question+answer> and read back the prompt-token logprobs for
exactly the answer tokens. This avoids the echo-logprob quirks of the
completions endpoint and works on any vLLM OpenAI-compatible server.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from ..data.schema import Instance
from ..stages.prompting import PromptingStrategy, get_strategy


@dataclass
class LogprobResult:
    qid: str
    drops: list[float]          # per-source logprob drop, index-aligned to sources
    ranking: list[int]          # source indices sorted by drop desc
    gold: list[int]
    baseline_logprob: float
    answer: str
    meta: dict

    def to_json(self) -> dict:
        return {
            "qid": self.qid,
            "drops": self.drops,
            "ranking": self.ranking,
            "gold": self.gold,
            "baseline_logprob": self.baseline_logprob,
            "answer": self.answer,
            "meta": self.meta,
        }


class LogprobScorer:
    """Scores log P(answer | context) on a vLLM OpenAI-compatible server.

    Separate from the black-box Backend on purpose: this one asks for logprobs,
    which the black-box setting forbids. Only instantiate for open models.
    """

    def __init__(self, model: str, base_url: str = "http://localhost:8000/v1",
                 api_key: str = "EMPTY", timeout: float = 120.0,
                 max_answer_tokens: int = 32):
        from openai import OpenAI
        self.model = model
        self.client = OpenAI(base_url=base_url, api_key=api_key, timeout=timeout)
        self.max_answer_tokens = max_answer_tokens

    def _score_answer_logprob(self, prompt_text: str, answer_text: str) -> float:
        """Return sum of token logprobs of answer_text given prompt_text.

        We concatenate prompt+answer and request prompt_logprobs, then sum the
        logprobs of the trailing tokens that correspond to answer_text. vLLM
        returns one logprob dict per prompt token (the chosen token's logprob is
        included), so we align from the end by answer token count.
        """
        full = prompt_text + answer_text
        # completions endpoint: prompt_logprobs returns per-prompt-token logprobs
        resp = self.client.completions.create(
            model=self.model,
            prompt=full,
            max_tokens=1,
            temperature=0.0,
            echo=True,
            logprobs=1,
            extra_body={"prompt_logprobs": 0},
        )
        choice = resp.choices[0]
        lp = choice.logprobs
        # token_logprobs is a list aligned to tokens; the first is None (BOS).
        token_logprobs = lp.token_logprobs
        tokens = lp.tokens
        # Determine how many trailing tokens belong to the answer by tokenizing
        # the answer alone via a second cheap call is wasteful; instead we locate
        # the answer by its text offset. text_offset gives the char offset of each
        # token; the answer starts at len(prompt_text).
        offsets = lp.text_offset
        start_char = len(prompt_text)
        ans_logprobs = [
            token_logprobs[i]
            for i in range(len(tokens))
            if offsets[i] >= start_char and token_logprobs[i] is not None
        ]
        if not ans_logprobs:
            return float("nan")
        return float(sum(ans_logprobs))

    def score_instance(self, inst: Instance,
                       strategy: PromptingStrategy | None = None) -> LogprobResult:
        """Leave-one-out logprob-drop attribution for one instance."""
        strategy = strategy or get_strategy("vanilla")

        # Build the prompt text for the full context. We reuse the perturbation
        # prompt builder (verbalize=False) so the scored context matches what the
        # black-box perturbation methods see, then render messages to a flat
        # prompt string for the completions endpoint.
        def prompt_for(exclude: int | None) -> str:
            spec = strategy.build(inst, exclude=exclude, verbalize=False)
            # flatten chat messages into a single prompt string for completions
            return "\n".join(m["content"] for m in spec.messages) + "\nAnswer: "

        # 1-2. baseline answer and its logprob under full context
        base_prompt = prompt_for(None)
        gen = self.client.completions.create(
            model=self.model, prompt=base_prompt,
            max_tokens=self.max_answer_tokens, temperature=0.0,
        )
        answer = gen.choices[0].text.strip().split("\n")[0]
        if not answer:
            answer = "(empty)"
        base_lp = self._score_answer_logprob(base_prompt, answer)

        # 3-4. per-source ablation drops
        drops: list[float] = []
        for s in inst.sources:
            abl_prompt = prompt_for(s.idx)
            abl_lp = self._score_answer_logprob(abl_prompt, answer)
            drop = (base_lp - abl_lp) if not math.isnan(abl_lp) else 0.0
            drops.append(drop)

        ranking = sorted(range(len(drops)), key=lambda i: drops[i], reverse=True)
        return LogprobResult(
            qid=inst.qid, drops=drops, ranking=ranking,
            gold=list(inst.gold_indices), baseline_logprob=base_lp,
            answer=answer,
            meta={"n_hop": inst.n_hop, "M": inst.M, "graybox": True},
        )

    def close(self):
        pass
