"""ContextCite gray-box upper bound -- paper Sec. 5.3.

Runs on open-weight models only: it needs token-level likelihoods, which is
exactly what the black-box setting denies. It marks the ceiling that black-box
methods are measured against.

Install:  pip install context_cite
The library defaults to sentence-level partitioning; we force paragraph-level
so the attribution units match the black-box pipelines (M sources, not M*~5
sentences).
"""
from __future__ import annotations

import numpy as np

from ..data.schema import Instance
from ..pipelines.runner import AttributionResult


def _result(inst: Instance, phi: np.ndarray, n_calls: int, method: str) -> AttributionResult:
    from ..stages.aggregation import to_ranking, to_set
    return AttributionResult(
        qid=inst.qid, method=method, phi=phi,
        ranking=to_ranking(phi), pred_set=to_set(phi, tau=0.5),
        gold=inst.gold_indices, n_calls=n_calls, empty_prediction=False,
        parse_failures=0, n_observations=0,
        meta={"n_hop": inst.n_hop, "M": inst.M, "graybox": True},
    )


class ContextCiteBaseline:
    """Wraps ContextCiter with a paragraph partitioner.

    One model load, reused across instances. num_ablations trades accuracy for
    cost; the ContextCite paper uses 32-256.
    """

    def __init__(self, model_name: str, device: str = "cuda", num_ablations: int = 64):
        from context_cite import ContextCiter
        self.ContextCiter = ContextCiter
        self.model_name = model_name
        self.device = device
        self.num_ablations = num_ablations

    def run(self, inst: Instance) -> AttributionResult:
        # ContextCite partitions `context` internally. We join sources with a
        # unique separator and pass a regex partitioner so each source is one
        # attributable unit, preserving our indexing.
        sep = "\n\n[[[SRC]]]\n\n"
        context = sep.join(s.text for s in inst.sources)

        cc = self.ContextCiter.from_pretrained(
            self.model_name,
            context,
            inst.question,
            device=self.device,
            num_ablations=self.num_ablations,
            partitioner=_ParagraphPartitioner(sep),
        )
        # get_attributions returns a score per source part, aligned to order.
        attr = cc.get_attributions()
        phi = np.asarray(attr, dtype=float).ravel()
        if phi.shape[0] != inst.M:
            # Partitioner drift: fall back to zeros rather than misalign gold.
            phi = np.zeros(inst.M, dtype=float)
        return _result(inst, phi, self.num_ablations, "contextcite")


class _ParagraphPartitioner:
    """Minimal partitioner splitting on our source separator.

    Mirrors the interface context_cite expects (parts + a way to reconstruct);
    kept here so the dependency stays optional and the intent is explicit.
    """

    def __init__(self, sep: str):
        self.sep = sep

    def split(self, context: str):
        return context.split(self.sep)

    def __call__(self, context: str):
        return self.split(context)
