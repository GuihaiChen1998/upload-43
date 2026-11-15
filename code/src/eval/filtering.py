"""Instance filtering for evaluation validity.

Two filters, both motivated by the 01c diagnostic:

LEAKAGE   Instances the model answers correctly with NO context at all. Ablation
          cannot reveal a dependence that does not exist, so these contribute
          noise to every metric. On HotpotQA with Qwen3-8B this was 26% of
          instances, and it largely explains why ablating a gold source changed
          the answer only ~40% of the time: roughly a third of the evaluation
          set had no causal signal to detect in the first place.

YES/NO    Binary-answer questions. With a two-element answer space, an ablation
          flips the answer with ~50% prior probability regardless of whether the
          removed source mattered, so the signal-to-noise ratio is poor. On
          HotpotQA these were 12 instances of which 10 "leaked" -- mostly
          guessing rather than genuine parametric knowledge.

Leakage is model-specific: a qid leaked for one model may be context-dependent
for another, so leakage files are keyed by model and never shared across them.
"""
from __future__ import annotations

import json
import os

from ..data.schema import Instance
from ..utils.parsing import normalize_answer

_YESNO = {"yes", "no"}


def load_leaked_qids(path: str, model: str | None = None) -> set[str]:
    """Read leaked qids from a 01c leakage.json report.

    If `model` is given and the report was produced for a different model, warn
    loudly rather than silently filtering with the wrong set -- leakage does not
    transfer across models.
    """
    if not path or not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        report = json.load(f)

    reported_model = report.get("model")
    if model and reported_model and os.path.basename(str(reported_model)) != os.path.basename(str(model)):
        print(f"  ! leakage report is for {reported_model!r} but the run targets "
              f"{model!r}; leakage is model-specific, so this filter may be wrong")

    return set(report.get("buckets", {}).get("leaked", []))


def load_evaluable_qids(path: str, model: str | None = None) -> set[str]:
    """Read the evaluable qid set from a 01c report.

    Evaluable = no parametric shortcut AND the model answers correctly with the
    full context. Gold supporting facts are a valid attribution target only
    here: when the model answers wrongly, the evidence it actually used has no
    reason to coincide with the human-annotated gold evidence.
    """
    if not path or not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        report = json.load(f)

    reported_model = report.get("model")
    # An INTERSECTION marker is a deliberately shared set, so the per-model
    # mismatch warning would be noise rather than a signal.
    if (model and reported_model
            and not str(reported_model).startswith("INTERSECTION")
            and os.path.basename(str(reported_model)) != os.path.basename(str(model))):
        print(f"  ! evaluable set is for {reported_model!r} but the run targets "
              f"{model!r}; correctness is model-specific, so this may be wrong")

    ev = report.get("evaluable")
    if ev is None:  # older report format
        b = report.get("buckets", {})
        ev = b.get("context_dep", []) + b.get("abstained_correct", [])
    return set(ev)


def is_yesno(inst: Instance) -> bool:
    return normalize_answer(inst.answer) in _YESNO


def stratified_sample(
    instances: list[Instance],
    n: int,
    stratify_by: str | None = "hop",
    seed: int = 0,
    verbose: bool = True,
) -> list[Instance]:
    """Draw `n` instances, balanced across strata where possible.

    Motivation: the evaluable set is conditioned on the model answering
    correctly, and accuracy falls with hop count, so an unstratified sample
    skews toward shallow instances and leaves the deep strata too thin for the
    hop-stratified analysis. Balancing spends the query budget where it buys
    statistical power.

    Strata smaller than the per-stratum quota are taken whole, and the leftover
    quota is redistributed over the remaining strata rather than silently
    shrinking the sample.
    """
    import random as _random

    if n >= len(instances):
        if verbose:
            print(f"  requested {n} >= available {len(instances)}; using all")
        return list(instances)

    rng = _random.Random(seed)

    if not stratify_by or stratify_by == "none":
        out = list(instances)
        rng.shuffle(out)
        return out[:n]

    if stratify_by != "hop":
        raise KeyError(f"unknown stratify_by {stratify_by!r}")

    strata: dict[object, list[Instance]] = {}
    for inst in instances:
        strata.setdefault(inst.n_hop, []).append(inst)
    for v in strata.values():
        rng.shuffle(v)

    if len(strata) < 2:
        out = list(instances)
        rng.shuffle(out)
        if verbose:
            print(f"  only one stratum present; sampling {n} without balancing")
        return out[:n]

    # Water-filling: repeatedly give each not-yet-exhausted stratum an equal
    # share of what remains, so small strata do not shrink the total.
    picked: dict[object, int] = {k: 0 for k in strata}
    remaining = n
    while remaining > 0:
        open_strata = [k for k in strata if picked[k] < len(strata[k])]
        if not open_strata:
            break
        share = max(1, remaining // len(open_strata))
        progressed = False
        for k in open_strata:
            take = min(share, len(strata[k]) - picked[k], remaining)
            if take <= 0:
                continue
            picked[k] += take
            remaining -= take
            progressed = True
            if remaining == 0:
                break
        if not progressed:
            break

    out = [inst for k in strata for inst in strata[k][: picked[k]]]
    if verbose:
        dist = {k: picked[k] for k in sorted(strata, key=lambda x: (x is None, x))}
        print(f"  stratified sample: {len(out)} instances by {stratify_by} -> {dist}")
    return out


def filter_instances(
    instances: list[Instance],
    leaked_qids: set[str] | None = None,
    drop_yesno: bool = False,
    verbose: bool = True,
) -> list[Instance]:
    """Apply the evaluation-validity filters, reporting what was removed."""
    n0 = len(instances)
    out = instances

    if leaked_qids:
        out = [i for i in out if i.qid not in leaked_qids]
    n_after_leak = len(out)

    if drop_yesno:
        out = [i for i in out if not is_yesno(i)]

    if verbose and len(out) != n0:
        parts = []
        if leaked_qids:
            parts.append(f"{n0 - n_after_leak} leaked")
        if drop_yesno:
            parts.append(f"{n_after_leak - len(out)} yes/no")
        print(f"  filtered {n0} -> {len(out)} instances ({', '.join(parts)})")

    return out
