#!/usr/bin/env python3
"""Token-level cost of each estimator and of the routing plan (Explore B2, B9, B10), read from the
response cache with zero model calls.

Every main run is replayed through the same pipeline code with a backend that never calls the API:
each cache lookup also returns the stored serving metadata (prompt / completion / reasoning tokens,
latency), which is summed per instance and estimator. The replay uses the fingerprint recorded in
each result file's manifest, so it reads exactly the cached responses the run used; a lookup that
misses is counted (it would have been an API call) and reported.

  python scripts/37_token_cost.py [--n 0]   # n > 0: first n instances of each cell's common set
  -> results/closed/analysis/token_cost.{json,md}

Needs the full cache (python scripts/restore_cache.py, snapshot 2026-11-06 or later).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import threading
from collections import defaultdict

import numpy as np

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)


def _load(name, rel):
    s = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


A = _load("a36", "scripts/36_review_audit.py")
t28 = A.t28
from src.pipelines.registry import get_method  # noqa: E402
from src.pipelines.runner import FULL_NOISE_REPEAT_OFFSET, run_method  # noqa: E402
from src.pipelines.subset import reference_answer, run_leave_one_in, run_random_mask  # noqa: E402
from src.utils.cache import QueryCache  # noqa: E402
from src.utils.config import build_gen_config, load_base, load_model_config  # noqa: E402

CACHE = os.path.join(ROOT, "results", "cache", "closed.sqlite")
_tls = threading.local()


class MetaCache(QueryCache):
    """QueryCache whose hits also add the stored token usage to the current bucket."""

    def get(self, model, messages, temperature, sample_idx, fingerprint=None, repeat=0):
        k = self._k(model, messages, temperature, sample_idx, fingerprint, repeat)
        with self._lock:
            row = self.conn.execute("SELECT response, meta FROM cache WHERE k=?", (k,)).fetchone()
        b = _tls.bucket
        if row is None:
            b["miss"] += 1
            return None
        m = json.loads(row[1] or "{}")
        part = "noise" if repeat >= FULL_NOISE_REPEAT_OFFSET else "est"
        b[f"{part}_calls"] += 1
        # provider-independent input size: characters of the prompt (resellers' prompt_tokens can include
        # injected system text, so the paper reports characters for input and provider tokens for output)
        b[f"{part}_chars"] += sum(len(m_.get("content") or "") for m_ in messages)
        b[f"{part}_in"] += m.get("prompt_tokens") or 0
        b[f"{part}_out"] += m.get("completion_tokens") or 0
        b[f"{part}_reason"] += m.get("reasoning_tokens") or 0
        b[f"{part}_lat"] += m.get("latency_s") or 0.0
        return row[0]

    def put(self, *a, **k):
        pass


class NoCallBackend:
    def __init__(self, name, fp):
        self.name, self._fp = name, fp

    def fingerprint(self, cfg):
        return self._fp

    def generate_with_meta(self, messages, cfg, seed=None):
        _tls.bucket["miss_issued"] += 1
        raise RuntimeError("cache miss")

    def generate(self, *a, **k):
        return self.generate_with_meta(*a, **k)[0]


def replay(method, inst, fp, model, cache, base, cfg):
    _tls.bucket = defaultdict(float)
    be = NoCallBackend(model, fp)
    agg = base["aggregation"]
    try:
        if method in ("V1", "P1"):
            m = get_method(method)
            run_method(inst, m, be, cfg=cfg, n_samples=base["sampling"]["n_samples_verbalize"] if m.is_verbalize
                       else base["sampling"]["n_samples_perturbation"], lam=agg["lambda"], beta=agg["beta"],
                       tau=agg["tau"], cache=cache, repeat=0, n_full_repeats=0 if m.is_verbalize else 3)
        elif method == "LOI":
            run_leave_one_in(inst, be, cfg, cache=cache, repeat=0, tau=agg["tau"])
        elif method == "REF":
            reference_answer(inst, be, cfg, cache, 0)
        elif method == "RM64":
            run_random_mask(inst, be, cfg, K=64, cache=cache, repeat=0, tau=agg["tau"])
    except Exception:
        _tls.bucket["error"] += 1
    return dict(_tls.bucket)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=0)
    args = ap.parse_args()
    base = load_base()
    cache = MetaCache(path=CACHE)
    out = []
    for ds in A.DATASETS:
        insts = A.instances(ds)
        for model in A.MODELS:
            L = A.load(ds, model)
            if L is None:
                continue
            by, common = L
            qs = common[: args.n] if args.n else common
            cfg = build_gen_config(base, load_model_config(os.path.join(ROOT, "configs", "models", "closed", f"{model}.yaml")))
            per = {}
            for meth in ("V1", "P1", "LOI", "RM64", "REF"):
                if meth != "REF" and meth not in by:
                    continue
                man = json.load(open(os.path.join(A.RAW, ds, model, "main", f"{'LOI' if meth == 'REF' else meth}.jsonl.manifest.json")))
                per[meth] = {q: replay(meth, insts[q], man["fingerprint"], model, cache, base, cfg) for q in qs}
            row = {"dataset": ds, "model": model, "n": len(qs)}
            for meth, d in per.items():
                vals = list(d.values())
                row[meth] = {k: float(np.mean([v.get(k, 0) for v in vals])) for k in
                             ("est_calls", "est_chars", "est_in", "est_out", "est_reason", "est_lat", "miss", "error")}
            # routing LOI -> RM64 / RM@32 in tokens: shared reference counted once
            if "RM64" in per:
                for rm in ("RM64",):
                    tin, tout, tin_rm, tout_rm, tch, tch_rm = [], [], [], [], [], []
                    for q in qs:
                        p = np.asarray(by["LOI"][q]["phi"], float)
                        go = not A.unique_max(p)
                        lo, rmq, v = per["LOI"][q], per["RM64"][q], per["V1"][q]
                        # LOI and RM buckets both contain the shared reference a0: count it once
                        r0 = per["REF"][q]
                        tin.append(lo.get("est_in", 0) + ((rmq.get("est_in", 0) - r0.get("est_in", 0)) if go else 0))
                        tout.append(lo.get("est_out", 0) + ((rmq.get("est_out", 0) - r0.get("est_out", 0)) if go else 0))
                        tin_rm.append(rmq.get("est_in", 0)); tout_rm.append(rmq.get("est_out", 0))
                        tch.append(lo.get("est_chars", 0) + ((rmq.get("est_chars", 0) - r0.get("est_chars", 0)) if go else 0))
                        tch_rm.append(rmq.get("est_chars", 0))
                    row["route_LOI_RM64"] = {"in": float(np.mean(tin)), "out": float(np.mean(tout)),
                                             "rm_in": float(np.mean(tin_rm)), "rm_out": float(np.mean(tout_rm)),
                                             "chars": float(np.mean(tch)), "rm_chars": float(np.mean(tch_rm)),
                                             "saving_chars": 1 - np.mean(tch) / np.mean(tch_rm),
                                             "saving_in": 1 - np.mean(tin) / np.mean(tin_rm),
                                             "saving_out": 1 - np.mean(tout) / np.mean(tout_rm)}
            print(ds, model, json.dumps({k: (v if not isinstance(v, dict) else {kk: round(vv, 1) for kk, vv in v.items()})
                                         for k, v in row.items()}), flush=True)
            out.append(row)
    os.makedirs(A.OUT, exist_ok=True)
    json.dump(out, open(os.path.join(A.OUT, "token_cost.json"), "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
