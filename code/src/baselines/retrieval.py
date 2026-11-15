"""Retrieval baselines -- paper Sec. 5.3, shallow reference.

These rank sources by lexical (BM25) or semantic (embedding) similarity to the
question, using no model behaviour at all. They are the bar a real attribution
method must clear: if a method only matches BM25, what it measures may be
question-source lexical overlap rather than the model's actual dependence.
This is especially pointed on HotpotQA, whose distractors are built by lexical
similarity.
"""
from __future__ import annotations

import re

import numpy as np

from ..data.schema import Instance
from ..pipelines.runner import AttributionResult


def _result(inst: Instance, phi: np.ndarray, method: str) -> AttributionResult:
    from ..stages.aggregation import to_ranking, to_set
    return AttributionResult(
        qid=inst.qid, method=method, phi=phi,
        ranking=to_ranking(phi), pred_set=to_set(phi, tau=0.5),
        gold=inst.gold_indices, n_calls=0, empty_prediction=False,
        parse_failures=0, n_observations=0,
        meta={"n_hop": inst.n_hop, "M": inst.M},
    )


def _tok(s: str) -> list[str]:
    return re.findall(r"\w+", s.lower())


def run_bm25(inst: Instance) -> AttributionResult:
    from rank_bm25 import BM25Okapi
    corpus = [_tok(s.text) for s in inst.sources]
    # BM25 needs non-empty docs; guard the degenerate case.
    corpus = [c if c else ["<empty>"] for c in corpus]
    bm = BM25Okapi(corpus)
    phi = np.array(bm.get_scores(_tok(inst.question)), dtype=float)
    return _result(inst, phi, "bm25")


class EmbeddingScorer:
    """Holds a sentence-transformer so it is loaded once, not per instance.

    Semantic counterpart to BM25: BM25 measures lexical overlap, this measures
    semantic similarity. Reporting both lets Sec. 6.2 distinguish a method that
    merely tracks keywords from one that merely tracks meaning -- a black-box
    method matching neither is the interesting case.

    Default model is mxbai-embed-xsmall-v1 (384-dim, MiniLM-based): small
    enough to run on CPU, good enough to discriminate. device='auto' picks CUDA
    when available and falls back to CPU otherwise.
    """

    def __init__(
        self,
        model_name: str = "mixedbread-ai/mxbai-embed-xsmall-v1",
        device: str = "auto",
        max_seq_length: int | None = None,
    ):
        from sentence_transformers import SentenceTransformer

        if device == "auto":
            try:
                import torch
                device = "cuda" if torch.cuda.is_available() else "cpu"
            except Exception:
                device = "cpu"
        self.model = SentenceTransformer(model_name, device=device)
        if max_seq_length:
            self.model.max_seq_length = max_seq_length

    def run(self, inst: Instance) -> AttributionResult:
        texts = [inst.question] + [s.text for s in inst.sources]
        emb = self.model.encode(texts, normalize_embeddings=True)
        q, docs = emb[0], emb[1:]
        phi = docs @ q
        return _result(inst, np.asarray(phi, dtype=float), "embedding")
