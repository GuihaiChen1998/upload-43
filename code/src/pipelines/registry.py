"""Method registry -- paper Sec. 4.5.

Defines the 12 viable methods (V1-V7, P1-P5) and refuses the infeasible
combinations. Three distinct reasons a cell can be empty:

  STRUCTURAL   sampling/aggregation coupling: direct needs N=1, consistency
               and uncertainty-aware need N>1. Definitional, not a choice.
  FIELD        uncertainty-aware needs u != None, so it cannot follow vanilla
               prompting. A consequence of the prompt design.
  PRINCIPLED   CoT x perturbation. The only genuine methodological exclusion:
               self-generated reasoning drifts under ablation and inflates
               epsilon in Assumption 1 (Sec. 3.4).
"""
from __future__ import annotations

from dataclasses import dataclass


class InfeasibleMethod(ValueError):
    pass


@dataclass(frozen=True)
class MethodSpec:
    mid: str
    paradigm: str      # "verbalize" | "perturbation"
    prompting: str     # "vanilla" | "self_probing" | "cot"
    sampling: str      # "single_pass" | "multi_sample"
    aggregation: str   # "direct" | "consistency" | "uncertainty"

    @property
    def is_verbalize(self) -> bool:
        return self.paradigm == "verbalize"

    def query_cost(self, M: int, N: int) -> int:
        """Q(A) from Sec. 4.6. kappa=2 for self-probing (two turns)."""
        kappa = 2 if self.prompting == "self_probing" else 1
        n = 1 if self.sampling == "single_pass" else N
        return n * kappa if self.is_verbalize else (M * n + 1) * kappa


def validate(paradigm: str, prompting: str, sampling: str, aggregation: str) -> None:
    if aggregation == "direct" and sampling != "single_pass":
        raise InfeasibleMethod("STRUCTURAL: direct aggregation requires N=1")
    if aggregation in ("consistency", "uncertainty") and sampling != "multi_sample":
        raise InfeasibleMethod(f"STRUCTURAL: {aggregation} aggregation requires N>1")
    if aggregation == "uncertainty" and prompting != "self_probing":
        raise InfeasibleMethod(
            "FIELD: uncertainty-aware aggregation needs the `likely` field, "
            "which only self-probing produces"
        )
    if prompting == "cot" and paradigm == "perturbation":
        raise InfeasibleMethod(
            "PRINCIPLED: CoT x perturbation is excluded (Assumption 1); "
            "reasoning-chain drift makes ablation observations uninterpretable"
        )


def _mk(mid, paradigm, prompting, sampling, aggregation) -> MethodSpec:
    validate(paradigm, prompting, sampling, aggregation)
    return MethodSpec(mid, paradigm, prompting, sampling, aggregation)


METHODS: dict[str, MethodSpec] = {
    m.mid: m
    for m in [
        # Verbalize: all three prompting strategies available.
        _mk("V1", "verbalize", "vanilla", "single_pass", "direct"),
        _mk("V2", "verbalize", "vanilla", "multi_sample", "consistency"),
        _mk("V3", "verbalize", "self_probing", "single_pass", "direct"),
        _mk("V4", "verbalize", "self_probing", "multi_sample", "consistency"),
        _mk("V5", "verbalize", "self_probing", "multi_sample", "uncertainty"),
        _mk("V6", "verbalize", "cot", "single_pass", "direct"),
        _mk("V7", "verbalize", "cot", "multi_sample", "consistency"),
        # Perturbation: CoT unavailable, hence 5 methods rather than 7.
        _mk("P1", "perturbation", "vanilla", "single_pass", "direct"),
        _mk("P2", "perturbation", "vanilla", "multi_sample", "consistency"),
        _mk("P3", "perturbation", "self_probing", "single_pass", "direct"),
        _mk("P4", "perturbation", "self_probing", "multi_sample", "consistency"),
        _mk("P5", "perturbation", "self_probing", "multi_sample", "uncertainty"),
    ]
}


def get_method(mid: str) -> MethodSpec:
    if mid not in METHODS:
        raise KeyError(f"unknown method {mid!r}; available: {list(METHODS)}")
    return METHODS[mid]


def verbalize_methods() -> list[MethodSpec]:
    return [m for m in METHODS.values() if m.is_verbalize]


def perturbation_methods() -> list[MethodSpec]:
    return [m for m in METHODS.values() if not m.is_verbalize]
