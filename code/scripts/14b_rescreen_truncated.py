#!/usr/bin/env python3
"""Re-screen instances whose screening call was cut off by max_tokens.

With hidden-reasoning models (gpt-6-luna) the NO-context call sometimes spends
the whole budget reasoning and returns no answer (finish_reason='length'). The
01c rules read a missing answer as an abstention, so such an instance can land
in `abstained_correct` (evaluable) although the model might well know the
answer -- i.e. a possible leak would be counted as evaluable. We re-ask only
the truncated call(s) with a larger budget and re-bucket with the same rules.

The original rows are kept; updated rows go to <pool>.retrunc.jsonl and
16_summarize_screening.py lets them replace the originals.

  python scripts/14b_rescreen_truncated.py --model configs/models/closed/gpt-6-luna.yaml \
      --dataset musique --pool union --max-tokens 8192
"""
from __future__ import annotations

import argparse
import importlib.util
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

_s = importlib.util.spec_from_file_location("screen14", os.path.join(ROOT, "scripts", "14_screen_closed.py"))
screen14 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(screen14)
leak01c = screen14.leak01c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--dataset", required=True, choices=["hotpotqa", "musique"])
    ap.add_argument("--pool", required=True, choices=["union", "intersection", "audit"])
    ap.add_argument("--max-tokens", type=int, default=8192)
    ap.add_argument("--workers", type=int, default=20)
    ap.add_argument("--cache", default=os.path.join(ROOT, "results", "cache", "closed.sqlite"))
    args = ap.parse_args()

    mc = load_model_config(args.model)
    be = build_backend(mc)
    gen = mc.get("gen", {})
    cfg = GenConfig(temperature=0.01, top_p=gen.get("top_p", None), max_tokens=args.max_tokens)
    cache = QueryCache(path=args.cache)
    d = os.path.join(ROOT, "results", "closed", "screen", args.dataset, mc["name"])
    rows = [json.loads(l) for l in open(os.path.join(d, f"{args.pool}.jsonl"), encoding="utf-8")]
    trunc = [r for r in rows if any(r[f"{t}_meta"].get("finish_reason") == "length" for t in ("empty", "full"))]
    by_qid = {i.qid: i for i in read_jsonl(os.path.join(ROOT, "data", "processed", f"{args.dataset}_validation.jsonl"))}
    print(f"{mc['name']} {args.dataset} {args.pool}: {len(trunc)} truncated rows -> re-ask at max_tokens={args.max_tokens}")

    def redo(r):
        inst = by_qid[r["qid"]]
        r = dict(r)
        prompts = {"empty": leak01c._no_context_prompt(inst.question),
                   "full": build_answer_prompt(inst, structured=True, cot=False)}
        for t in ("empty", "full"):
            if r[f"{t}_meta"].get("finish_reason") != "length":
                continue
            text, meta = screen14.call(be, cache, prompts[t], cfg, 0)
            obs = parse_observation(text, strict_thinking=False)
            r[f"{t}_raw"] = text
            r[f"{t}_answer"] = normalize_answer(obs.answer) if obs.ok and obs.answer else None
            r[f"{t}_meta"] = {**meta, "rescreened_max_tokens": args.max_tokens}
        empty, full = r["empty_answer"], r["full_answer"]
        if empty is None and full is None:
            b = "unparsable"
        else:
            fr = leak01c.matches_gold(full, inst)
            if leak01c.is_abstention(empty):
                b = "abstained_correct" if fr else "abstained_wrong"
            elif leak01c.matches_gold(empty, inst):
                b = "leaked"
            elif fr:
                b = "context_dep"
            else:
                b = "both_wrong"
        r["bucket_before_rescreen"] = r["bucket"]
        r["bucket"] = b
        r["evaluable"] = b in ("context_dep", "abstained_correct")
        return r

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        new = list(ex.map(redo, trunc))
    with open(os.path.join(d, f"{args.pool}.retrunc.jsonl"), "w", encoding="utf-8") as f:
        for r in new:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    from collections import Counter
    print("transitions:", dict(Counter((r["bucket_before_rescreen"], r["bucket"]) for r in new)))
    print("still truncated:", sum(any(r[f"{t}_meta"].get("finish_reason") == "length" for t in ("empty", "full")) for r in new))


if __name__ == "__main__":
    main()
