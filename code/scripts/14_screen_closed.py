#!/usr/bin/env python3
"""Evaluable-set screening for closed API models (phase 1).

Same rules as scripts/01c_leakage_check.py (imported, not re-implemented): each
instance is asked once WITHOUT context and once WITH the full context
(answer-only structured output, T=0.01), then bucketed:

  leaked / context_dep / abstained_correct / abstained_wrong / both_wrong / unparsable
  evaluable = context_dep + abstained_correct

Differences from 01c, all for closed endpoints:
  * concurrent requests; v2 cache keys (endpoint/config fingerprint + repeat),
    so reruns replay from cache and independent repeats issue fresh calls;
  * every call's metadata (tokens, latency, served model, finish_reason,
    response id) is kept in the per-instance output;
  * a run manifest guards against resuming with a different configuration;
  * cost is computed from recorded token usage and the per-model price list.

  python scripts/14_screen_closed.py --model configs/models/closed/gpt-6-luna.yaml \
      --dataset hotpotqa --pool union --workers 16 [--limit 20]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)

from src.backends.base import GenConfig
from src.data.schema import read_jsonl
from src.stages.prompting import build_answer_prompt
from src.utils.cache import QueryCache
from src.utils.config import build_backend, load_model_config
from src.utils.parsing import normalize_answer, parse_observation

_spec = importlib.util.spec_from_file_location("leak01c", os.path.join(ROOT, "scripts", "01c_leakage_check.py"))
leak01c = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(leak01c)
_spec2 = importlib.util.spec_from_file_location("run02", os.path.join(ROOT, "scripts", "02_run_method.py"))
run02 = importlib.util.module_from_spec(_spec2)
_spec2.loader.exec_module(run02)

# RMB per million tokens (input, output), as given by the user (2026-11-01).
# claude-haiku-5-5: tian-shu price in RMB (the runapi USD price no longer applies).
PRICE_CNY = {
    "claude-haiku-5-5": (0.025, 0.125),   # tian-shu, RMB (user, 2026-11-01); runapi was USD 0.012/0.058
    "gpt-6-luna": (0.02, 0.1),
    "gemini-2.5-flash-lite": (0.036, 0.144),
    "gemini-2.5-flash": (0.108, 0.89),
    "gpt-6.1-terra": (0.25, 1.25),
}


def call(backend, cache, content, cfg, repeat):
    msgs = [{"role": "user", "content": content}]
    fp = backend.fingerprint(cfg)
    text = cache.get(backend.name, msgs, cfg.temperature, 0, fp, repeat) if cache else None
    if text is not None:
        return text, {"cached": True}
    text, meta = backend.generate_with_meta(msgs, cfg, seed=None)
    meta = {**meta, "cached": False, "repeat": repeat}
    if cache:
        cache.put(backend.name, msgs, cfg.temperature, 0, text, fp, repeat, meta)
    return text, meta


def matches(pred, inst):
    """01c's lenient match; for Qasper also SQuAD-style token F1 >= 0.5 against any gold
    span (the dataset's standard answer metric; spans are often paraphrased). Used for the
    leakage test too, so a looser match can only flag MORE questions as leaked."""
    if leak01c.matches_gold(pred, inst):
        return True
    if inst.dataset == "qasper" and pred:
        from src.pipelines.subset import token_f1
        return max(token_f1(pred, g) for g in [inst.answer] + list(inst.answer_aliases or [])) >= 0.5
    return False


def screen_one(inst, backend, cache, cfg, repeat):
    out = {"qid": inst.qid, "n_hop": inst.n_hop, "gold_answer": inst.answer}
    for tag, content in [("empty", leak01c._no_context_prompt(inst.question)),
                         ("full", build_answer_prompt(inst, structured=True, cot=False))]:
        text, meta = call(backend, cache, content, cfg, repeat)
        obs = parse_observation(text, strict_thinking=False)
        ans = normalize_answer(obs.answer) if obs.ok and obs.answer else None
        out[f"{tag}_raw"] = text
        out[f"{tag}_answer"] = ans
        out[f"{tag}_meta"] = meta
    empty, full = out["empty_answer"], out["full_answer"]
    if empty is None and full is None:
        bucket = "unparsable"
    else:
        full_right = matches(full, inst)
        if leak01c.is_abstention(empty):
            bucket = "abstained_correct" if full_right else "abstained_wrong"
        elif matches(empty, inst):
            bucket = "leaked"
        elif full_right:
            bucket = "context_dep"
        else:
            bucket = "both_wrong"
    out["bucket"] = bucket
    out["evaluable"] = bucket in ("context_dep", "abstained_correct")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="path to a configs/models/closed/*.yaml")
    ap.add_argument("--dataset", required=True, choices=["hotpotqa", "musique", "symfever", "qasper"])
    ap.add_argument("--pool", default=None, choices=["union", "intersection", "audit"])
    ap.add_argument("--instances", default=None,
                    help="jsonl(.gz) of constructed instances (e.g. Symmetric FEVER); replaces --pool")
    ap.add_argument("--limit", type=int, default=None, help="pilot: random subset of the pool (seed 0)")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--repeat", type=int, default=0)
    ap.add_argument("--cache", default=os.path.join(ROOT, "results", "cache", "closed.sqlite"))
    ap.add_argument("--out-root", default=os.path.join(ROOT, "results", "closed", "screen"))
    args = ap.parse_args()

    model_cfg = load_model_config(args.model)
    name = model_cfg["name"]
    backend = build_backend(model_cfg)
    gen = model_cfg.get("gen", {})
    cfg = GenConfig(temperature=0.01, top_p=gen.get("top_p", None),
                    max_tokens=gen.get("max_tokens", 1024))

    if args.instances:
        import gzip
        from src.data.schema import Instance
        op = gzip.open if args.instances.endswith(".gz") else open
        with op(args.instances, "rt", encoding="utf-8") as fh:
            by_qid = {i.qid: i for i in (Instance.from_json(json.loads(l)) for l in fh if l.strip())}
        pool = sorted(by_qid)
        args.pool = os.path.basename(args.instances).split(".jsonl")[0]
    else:
        if not args.pool:
            sys.exit("--pool or --instances is required")
        with open(os.path.join(ROOT, "results", "closed", "pools", f"{args.dataset}.json")) as f:
            pool = json.load(f)[args.pool]
        by_qid = {i.qid: i for i in read_jsonl(os.path.join(ROOT, "data", "processed", f"{args.dataset}_validation.jsonl"))}
    if args.limit:
        pool = sorted(random.Random(0).sample(pool, min(args.limit, len(pool))))
    insts = [by_qid[q] for q in pool]

    tag = f"{args.pool}" + (f".limit{args.limit}" if args.limit else "") + (f".r{args.repeat}" if args.repeat else "")
    out_dir = os.path.join(args.out_root, args.dataset, name)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{tag}.jsonl")
    manifest = {"script": "14_screen_closed", "model": name, "dataset": args.dataset, "pool": args.pool,
                "limit": args.limit, "repeat": args.repeat, "fingerprint": backend.fingerprint(cfg),
                "temperature": cfg.temperature,
                "rules": "01c_leakage_check (imported)" + ("; qasper: + token F1 >= 0.5" if args.dataset == "qasper" else "")}
    run02.check_or_write_manifest(out_path, manifest, allow_unmanifested=False)
    done = run02.already_done(out_path)
    todo = [i for i in insts if i.qid not in done]

    cache = QueryCache(path=args.cache)
    print(f"{name} | {args.dataset} | pool={args.pool} n={len(insts)} todo={len(todo)} workers={args.workers}")
    lock = threading.Lock()
    t0 = time.time()
    n_done = 0
    with open(out_path, "a", encoding="utf-8") as f, ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(screen_one, i, backend, cache, cfg, args.repeat): i.qid for i in todo}
        for fut in as_completed(futs):
            try:
                row = fut.result()
            except Exception as e:  # keep going; failed qids are retried on the next run
                print(f"  ! {futs[fut]}: {type(e).__name__}: {str(e)[:160]}")
                continue
            with lock:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
                f.flush()
                n_done += 1
                if n_done % 50 == 0:
                    print(f"  {n_done}/{len(todo)}  {time.time()-t0:.0f}s")

    rows = [json.loads(l) for l in open(out_path, encoding="utf-8")]
    rows = [r for r in rows if r["qid"] in set(pool)]
    buckets = {k: [] for k in ["leaked", "context_dep", "abstained_correct", "abstained_wrong", "both_wrong", "unparsable"]}
    hop_total, hop_eval = {}, {}
    tin = tout = treason = 0
    lat, calls_new = [], 0
    finish = {}
    for r in rows:
        buckets[r["bucket"]].append(r["qid"])
        h = r["n_hop"]
        if h is not None:
            hop_total[h] = hop_total.get(h, 0) + 1
            hop_eval[h] = hop_eval.get(h, 0) + int(r["evaluable"])
        for t in ("empty", "full"):
            m = r[f"{t}_meta"]
            if not m.get("cached"):
                calls_new += 1
            tin += m.get("prompt_tokens") or 0
            tout += m.get("completion_tokens") or 0
            treason += m.get("reasoning_tokens") or 0
            if m.get("latency_s") is not None:
                lat.append(m["latency_s"])
            fr = m.get("finish_reason")
            finish[fr] = finish.get(fr, 0) + 1
    n = len(rows)
    pin, pout = PRICE_CNY.get(name, (0.0, 0.0))
    summary = {
        "model": name, "endpoint": model_cfg.get("endpoint"), "dataset": args.dataset, "pool": args.pool,
        "n": n, "leak_rate": len(buckets["leaked"]) / n if n else 0,
        "evaluable_rate": (len(buckets["context_dep"]) + len(buckets["abstained_correct"])) / n if n else 0,
        "bucket_counts": {k: len(v) for k, v in buckets.items()},
        "hop_total": hop_total, "hop_evaluable": hop_eval,
        "usage": {"prompt_tokens": tin, "completion_tokens": tout, "reasoning_tokens": treason,
                  "est_cost_cny": round(tin / 1e6 * pin + tout / 1e6 * pout, 4),
                  "mean_latency_s": round(sum(lat) / len(lat), 2) if lat else None,
                  "finish_reasons": finish, "calls_recorded": 2 * n},
        "buckets": buckets,
        "evaluable": buckets["context_dep"] + buckets["abstained_correct"],
    }
    with open(out_path.replace(".jsonl", ".summary.json"), "w") as f:
        json.dump(summary, f, indent=1, ensure_ascii=False, default=str)
    print(json.dumps({k: v for k, v in summary.items() if k not in ("buckets", "evaluable")}, ensure_ascii=False, default=str))
    print(f"cache: {cache.stats}")


if __name__ == "__main__":
    main()
