"""ARC-JSD gray-box upper bound -- ADAPTER INTERFACE ONLY.

ARC-JSD (https://github.com/ruizheliUOA/ARC_JSD) attributes via Jensen-Shannon
divergence between full-context and ablated-context output DISTRIBUTIONS, so it
needs full next-token distributions, not just the target sequence's logprob --
a heavier gray-box requirement than ContextCite. It is reported as the primary
upper bound (newer, faster, stronger top-1 per its paper).

This file is a stub. To wire it in:
  1. git clone https://github.com/ruizheliUOA/ARC_JSD
  2. confirm its entry point accepts (model, context parts, query) and returns
     one score per part at paragraph granularity;
  3. implement `run` below, returning an AttributionResult exactly as
     ContextCiteBaseline does.

Kept behind a clear NotImplementedError so an accidental invocation fails loudly
rather than silently producing zeros that would look like a real upper bound.
"""
from __future__ import annotations

from ..data.schema import Instance
from ..pipelines.runner import AttributionResult


class ARCJSDBaseline:
    def __init__(self, model_name: str, device: str = "cuda", **kwargs):
        self.model_name = model_name
        self.device = device
        self.kwargs = kwargs

    def run(self, inst: Instance) -> AttributionResult:
        raise NotImplementedError(
            "ARC-JSD adapter not implemented. Clone "
            "https://github.com/ruizheliUOA/ARC_JSD, verify its paragraph-level "
            "interface, and fill in run() to return an AttributionResult with "
            "meta['graybox']=True. Until then, use ContextCite as the upper bound."
        )
