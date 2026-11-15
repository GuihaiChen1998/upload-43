#!/usr/bin/env python3
"""Does the endpoint honour `temperature`? (phase 1 sanity check)

Two probes per model, each repeated K times as independent calls (repeat index
in the cache key, so nothing is replayed):

  open   an open-ended prompt that invites variation; at T=0.7 a working
         endpoint should return several distinct texts, at T=0.01 few or one.
  task   the full-context answer-only prompt of a few real instances, i.e. the
         variation that actually feeds the perturbation signal.

No variation at T=0.7 on the open probe suggests the parameter is ignored (or
the provider caches). Variation at T=0.01 means "low temperature" is not
deterministic on that endpoint -- relevant for the single-pass methods.

  python scripts/15_check_temperature.py --model configs/models/closed/gpt-6-luna.yaml
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)

from src.backends.base import GenConfig
from src.data.schema import read_jsonl
from src.stages.prompting import build_answer_prompt
from src.utils.cache import QueryCache
from src.utils.config import build_backend, load_model_config
from src.utils.parsing import normalize_answer, parse_observation

OPEN_PROMPT = "Invent a short, unusual name for a fictional coffee shop and give it in one line, nothing else."


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--n-task", type=int, default=3)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--cache", default=os.path.join(ROOT, "results", "cache", "closed.sqlite"))
    ap.add_argument("--out-dir", default=os.path.join(ROOT, "results", "closed", "temperature"))
    args = ap.parse_args()
    mc = load_model_config(args.model)
    be = build_backend(mc)
    cache = QueryCache(path=args.cache)
    gen = mc.get("gen", {})
    insts = read_jsonl(os.path.join(ROOT, "data", "processed", "musique_validation.jsonl"))[: args.n_task]
    probes = [("open", OPEN_PROMPT, None)] + [("task", build_answer_prompt(i, structured=True, cot=False), i.qid) for i in insts]

    def one(job):
        probe, content, qid, T, rep = job
        cfg = GenConfig(temperature=T, top_p=gen.get("top_p", None), max_tokens=gen.get("max_tokens", 1024))
        msgs = [{"role": "user", "content": content}]
        fp = be.fingerprint(cfg)
        # repeat offset 200000 + rep: a namespace reserved for this check
        text = cache.get(be.name, msgs, T, 0, fp, 200_000 + rep)
        meta = {"cached": True}
        if text is None:
            text, meta = be.generate_with_meta(msgs, cfg, seed=None)
            cache.put(be.name, msgs, T, 0, text, fp, 200_000 + rep, meta)
        ans = None
        if probe == "task":
            o = parse_observation(text, strict_thinking=False)
            ans = normalize_answer(o.answer) if o.ok and o.answer else None
        return {"probe": probe, "qid": qid, "T": T, "repeat": rep, "text": text.strip(), "answer": ans,
                "finish_reason": meta.get("finish_reason"), "served_model": meta.get("served_model")}

    jobs = [(p, c, q, T, r) for (p, c, q) in probes for T in (0.01, 0.7) for r in range(args.k)]
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        rows = list(ex.map(one, jobs))

    summary = {"model": mc["name"], "endpoint": mc.get("endpoint"), "k": args.k, "probes": {}}
    for (p, c, q) in probes:
        key = p if p == "open" else f"task:{q}"
        summary["probes"][key] = {}
        for T in (0.01, 0.7):
            rs = [r for r in rows if r["probe"] == p and r["qid"] == q and r["T"] == T]
            summary["probes"][key][str(T)] = {
                "distinct_texts": len({r["text"] for r in rs}),
                "distinct_answers": len({r["answer"] for r in rs}) if p == "task" else None,
            }
    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, f"{mc['name']}.json"), "w") as f:
        json.dump({"summary": summary, "rows": rows}, f, indent=1, ensure_ascii=False)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
