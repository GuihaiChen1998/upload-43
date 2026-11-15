"""Unified instance schema shared by all datasets, pipelines and metrics.

A single attribution instance is (question, sources, gold source indices).
Everything downstream -- prompting, perturbation, evaluation -- operates on
this structure only, so adding a dataset means writing one loader, not
touching the pipelines.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any
import json


@dataclass
class Source:
    """One attributable unit. Paragraph-level in all current datasets."""

    idx: int  # 0-based position in the instance's source list
    title: str
    text: str
    is_gold: bool = False

    def render(self, display_number: int) -> str:
        """Render for inclusion in a prompt. `display_number` is 1-based."""
        head = f"[{display_number}]"
        if self.title:
            head += f" {self.title}"
        return f"{head}\n{self.text}"


@dataclass
class Instance:
    qid: str
    question: str
    answer: str
    sources: list[Source]
    dataset: str
    n_hop: int | None = None  # MuSiQue only; None for HotpotQA
    answer_aliases: list[str] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def M(self) -> int:
        return len(self.sources)

    @property
    def gold_indices(self) -> list[int]:
        """0-based indices of gold sources. This is the approximation to S*."""
        return [s.idx for s in self.sources if s.is_gold]

    def render_context(self, exclude: int | None = None) -> str:
        """Render the source list, optionally ablating one source.

        Ablation renumbers the remaining sources contiguously (1..M-1) rather
        than leaving a gap. A gap would signal to the model that something was
        removed, which is exactly the confound we are trying to avoid.
        Returns the context string; use `surviving_indices` to map displayed
        numbers back to original indices.
        """
        parts, n = [], 0
        for s in self.sources:
            if exclude is not None and s.idx == exclude:
                continue
            n += 1
            parts.append(s.render(n))
        return "\n\n".join(parts)

    def surviving_indices(self, exclude: int | None = None) -> list[int]:
        """Original 0-based indices in display order, after ablation.

        `surviving_indices(e)[k]` is the original index of the source the model
        sees as number k+1.
        """
        return [s.idx for s in self.sources if exclude is None or s.idx != exclude]

    def render_context_excluding(self, exclude_set) -> str:
        """Render the source list ablating a SET of sources (for top-k drop).

        Like `render_context` but removes every source whose index is in
        `exclude_set`, renumbering survivors contiguously. Used by the top-k
        log-probability drop evaluation, which ablates the k highest-ranked
        sources at once. `exclude_set=set()` renders the full context.
        """
        exclude_set = set(exclude_set or ())
        parts, n = [], 0
        for s in self.sources:
            if s.idx in exclude_set:
                continue
            n += 1
            parts.append(s.render(n))
        return "\n\n".join(parts)

    def to_json(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_json(d: dict) -> "Instance":
        d = dict(d)
        d["sources"] = [Source(**s) for s in d["sources"]]
        return Instance(**d)


def write_jsonl(instances: list[Instance], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for inst in instances:
            f.write(json.dumps(inst.to_json(), ensure_ascii=False) + "\n")


def read_jsonl(path: str) -> list[Instance]:
    with open(path, encoding="utf-8") as f:
        return [Instance.from_json(json.loads(line)) for line in f if line.strip()]
