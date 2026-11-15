"""Dataset loaders. Each returns list[Instance] in the unified schema.

Paragraph-level granularity throughout (see paper Sec. 5.1): sentence-level
would push M to 40-60 and make the O(MN) interventional pipeline unaffordable.

Offline use: run scripts/00_prepare_data.py on a networked machine to cache
processed JSONL under data/processed/, copy it to the offline server, and the
loaders read it directly. `hf_name` lets you point at a regional mirror; set
the env var HF_DATASETS_OFFLINE=1 to forbid any network access entirely.
"""
from __future__ import annotations

import os
import re

from .schema import Instance, Source, read_jsonl

# Default HF repo ids, overridable per call via `hf_name` (e.g. a mirror).
_DEFAULT_HF = {
    "hotpotqa": "hotpotqa/hotpot_qa",
    "musique": "dgslibisey/MuSiQue",
}

PROCESSED_DIR = os.environ.get("BBATTR_PROCESSED_DIR", "data/processed")


def _processed_path(name: str, split: str) -> str:
    return os.path.join(PROCESSED_DIR, f"{name}_{split}.jsonl")


def _maybe_cached(name: str, split: str, limit: int | None,
                  hops: list[int] | None = None) -> list[Instance] | None:
    """Return instances from a pre-processed JSONL if one exists.

    This is the offline fast path: if scripts/00_prepare_data.py has been run,
    no HF access happens. Filtering by limit/hops is applied to the cache too,
    so a broadly-cached file still serves narrow requests.

    Warns when the cache cannot satisfy the request, since a cache built with a
    small --limit silently caps every later run: the caller asks for the full
    set and quietly receives whatever was cached first.
    """
    path = _processed_path(name, split)
    if not os.path.exists(path):
        return None
    insts = read_jsonl(path)
    n_cached = len(insts)

    if limit and limit > n_cached:
        print(f"  ! cached {name}/{split} holds only {n_cached} instances but "
              f"{limit} were requested. Re-run 00_prepare_data.py with a larger "
              f"--limit, or delete {path} to read from the source.")
    if name == "musique":
        hops_present = {i.n_hop for i in insts if i.n_hop is not None}
        if len(hops_present) < 2:
            print(f"  ! cached {name}/{split} contains only hop levels "
                  f"{sorted(hops_present)}; it was probably built with a small "
                  f"--limit in file order. Delete {path} and re-cache for a "
                  f"hop-diverse set.")

    if hops is not None:
        insts = [i for i in insts if i.n_hop in hops]
    if limit:
        insts = insts[:limit]
    return insts


def _load_hf(hf_name: str, config: str | None, split: str):
    """Load from HF (or a local dataset dir), honouring offline mode."""
    from datasets import load_dataset

    # A local path saved via datasets.save_to_disk is also accepted.
    if os.path.isdir(hf_name):
        from datasets import load_from_disk
        ds = load_from_disk(hf_name)
        return ds[split] if split in ds else ds
    if config:
        return load_dataset(hf_name, config, split=split)
    return load_dataset(hf_name, split=split)


def _answer_ok(inst: Instance, max_words: int | None) -> bool:
    """Short-answer suitability. The string-equality change detector (Sec. 3.4)
    is reliable only for short entity answers; ~89% of MuSiQue and ~91% of
    HotpotQA answers are <=4 words, so filtering the long tail costs ~10% of
    data and removes the compound-phrase answers that break exact matching."""
    if max_words is None:
        return True
    return len(inst.answer.split()) <= max_words




def load_hotpotqa(
    split: str = "validation",
    limit: int | None = None,
    hf_name: str | None = None,
    only_type: str | None = None,
    config: str | None = "distractor",
    max_answer_words: int | None = 4,
    min_gold: int | None = None,
) -> list[Instance]:
    """HotpotQA distractor setting: 10 paragraphs, 2 of them gold.

    Gold is identified by title membership in supporting_facts, since
    supporting_facts records (title, sent_id) pairs and we work at paragraph
    granularity.

    `hf_name` can point at a filtered variant such as
    yapeichang/hotpotqa-filtered (fullwiki validation, gold answers
    LLM-verified), in which case pass config=None since that repo has a single
    default config. `only_type` keeps just 'bridge' or 'comparison': bridge is
    genuine multi-hop and suits attribution, whereas comparison is mostly binary
    (yes/no or either/or), which gives ablation a ~50% flip prior and poor
    signal-to-noise -- the same reason yes/no questions are dropped elsewhere.
    """
    cached = _maybe_cached("hotpotqa", split, None)
    if cached is not None:
        insts = cached
        if only_type:
            insts = [i for i in insts if i.meta.get("type") == only_type]
        if min_gold:
            insts = [i for i in insts if len(i.gold_indices) >= min_gold]
        if limit:
            insts = insts[:limit]
        return insts

    name = hf_name or _DEFAULT_HF["hotpotqa"]
    # The canonical repo needs the "distractor" config; filtered mirrors expose
    # a single default config, so callers pass config=None for those.
    cfg = config if name == _DEFAULT_HF["hotpotqa"] else None
    ds = _load_hf(name, cfg, split)

    out = []
    for r in ds:
        gold_titles = set(r["supporting_facts"]["title"])
        titles = r["context"]["title"]
        sent_lists = r["context"]["sentences"]

        sources = [
            Source(
                idx=i,
                title=t,
                text="".join(sents).strip(),
                is_gold=(t in gold_titles),
            )
            for i, (t, sents) in enumerate(zip(titles, sent_lists))
        ]
        # Drop instances whose gold titles are absent from the context.
        if not any(s.is_gold for s in sources):
            continue

        out.append(
            Instance(
                qid=r["id"],
                question=r["question"],
                answer=r["answer"],
                sources=sources,
                dataset="hotpotqa",
                n_hop=None,
                meta={"type": r["type"], "level": r["level"]},
            )
        )
    out = [i for i in out if _answer_ok(i, max_answer_words)]
    if only_type:
        out = [i for i in out if i.meta.get("type") == only_type]
    if min_gold:
        out = [i for i in out if len(i.gold_indices) >= min_gold]
    return out[:limit] if limit else out


_HOP_RE = re.compile(r"^(\d)hop")


def load_musique(
    split: str = "validation",
    limit: int | None = None,
    hops: list[int] | None = None,
    answerable_only: bool = True,
    hf_name: str | None = None,
    balance_hops: bool = False,
    max_answer_words: int | None = 4,
) -> list[Instance]:
    """MuSiQue: ~20 paragraphs, gold count equals hop count (2/3/4).

    `hops` filters to specific hop subsets, which is how Sec. 6.5 stratifies
    the empty-prediction analysis. Note M~20 here versus M=10 for HotpotQA:
    random baselines and query costs are not comparable across the two.

    `balance_hops=True` draws roughly equal numbers per hop count. Without it,
    taking the first `limit` rows yields almost all 2-hop instances (they come
    first in the file), which silently defeats the hop-stratified analysis.
    """
    cached = _maybe_cached("musique", split, None, hops)
    if cached is not None:
        return _postfilter_musique(cached, limit, hops, balance_hops, max_answer_words)

    ds = _load_hf(hf_name or _DEFAULT_HF["musique"], None, split)

    out = []
    for r in ds:
        if answerable_only and not r.get("answerable", True):
            continue
        m = _HOP_RE.match(r["id"])
        n_hop = int(m.group(1)) if m else None
        if hops is not None and n_hop not in hops:
            continue

        sources = [
            Source(
                idx=i,
                title=p["title"],
                text=p["paragraph_text"].strip(),
                is_gold=bool(p["is_supporting"]),
            )
            for i, p in enumerate(r["paragraphs"])
        ]
        if not any(s.is_gold for s in sources):
            continue

        out.append(
            Instance(
                qid=r["id"],
                question=r["question"],
                answer=r["answer"],
                sources=sources,
                dataset="musique",
                n_hop=n_hop,
                answer_aliases=list(r.get("answer_aliases") or []),
                meta={},
            )
        )
    return _postfilter_musique(out, limit, hops, balance_hops, max_answer_words)


def _postfilter_musique(insts, limit, hops, balance_hops, max_answer_words=4):
    """Apply answer-length filter, hop filter, optional hop balancing, and limit
    -- shared by the online and cached paths for identical selections."""
    insts = [i for i in insts if _answer_ok(i, max_answer_words)]
    if hops is not None:
        insts = [i for i in insts if i.n_hop in hops]
    if balance_hops and limit:
        from collections import defaultdict
        buckets = defaultdict(list)
        for i in insts:
            buckets[i.n_hop].append(i)
        per = max(1, limit // max(1, len(buckets)))
        out = []
        for h in sorted(buckets):
            out.extend(buckets[h][:per])
        return out[:limit]
    if limit:
        insts = insts[:limit]
    return insts


LOADERS = {"hotpotqa": load_hotpotqa, "musique": load_musique}


def load_dataset_by_name(name: str, **kw) -> list[Instance]:
    if name not in LOADERS:
        raise KeyError(f"unknown dataset {name!r}; available: {list(LOADERS)}")
    return LOADERS[name](**kw)
