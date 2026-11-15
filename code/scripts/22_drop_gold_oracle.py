#!/usr/bin/env python3
"""Oracle group intervention on the ORIGINAL presentation (GPT's suggestion in issue #1,
round 20): remove every gold passage at once and ask again (repeats 0-2).

If the answer survives without any gold passage, the source-level ablations cannot
attribute the answer to gold evidence: either a non-gold passage carries the answer
(distractor redundancy) or the model answers from its own knowledge. This bounds how
much of the all-zero mass on the original data is due to redundancy *among gold
passages* (which only a group intervention reveals) versus everything else.

Rows record whether any non-gold passage contains a normalised gold answer string
(answer-bearing distractor) so results can be stratified.

  python scripts/22_drop_gold_oracle.py --model configs/models/closed/claude-haiku-5-5.yaml --dataset hotpotqa
  -> results/closed/oracle/<dataset>/<model>/drop_gold.jsonl (+ .cost.json)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)

from src.pipelines.subset import _answers_for, subset_prompt  # noqa: E402
from src.utils.cache import QueryCache  # noqa: E402
from src.utils.config import build_backend, build_gen_config, load_base, load_model_config  # noqa: E402
from src.utils.parsing import normalize_answer  # noqa: E402

import importlib.util  # noqa: E402

_s = importlib.util.spec_from_file_location("run17", os.path.join(ROOT, "scripts", "17_run_closed.py"))
run17 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(run17)
leak01c = run17.screen14.leak01c
PRICE_CNY = run17.screen14.PRICE_CNY
REPEATS = (0, 1, 2)


def answer_bearing_distractors(inst) -> list[int]:
    golds = [normalize_answer(a) for a in [inst.answer, *inst.answer_aliases] if a]
    golds = [g for g in golds if g]
    out = []
    for i, s in enumerate(inst.sources):
        if s.is_gold:
            continue
        t = normalize_answer(s.text)
        if any(f" {g} " in f" {t} " for g in golds):
            out.append(i)
    return out


def one(inst, backend, cfg, cache, workers):
    keep = [i for i, s in enumerate(inst.sources) if not s.is_gold]
    n_gold = len(inst.sources) - len(keep)
    row = {"qid": inst.qid, "n_hop": inst.n_hop, "M": len(inst.sources), "n_gold": n_gold,
           "answer_bearing_distractors": answer_bearing_distractors(inst)}
    calls = 0
    for r in REPEATS:
        obs, c = _answers_for([subset_prompt(inst, keep)], backend, cfg, cache, r, workers)
        calls += c
        o = obs[0]
        a = normalize_answer(o.answer) if o.ok and o.answer else None
        row.setdefault("answer", []).append(a)
        row.setdefault("correct", []).append(bool(leak01c.matches_gold(a, inst)) if a else False)
    return row, calls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--dataset", required=True, choices=["hotpotqa", "musique"])
    ap.add_argument("--pool", default=None)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--cache", default=os.path.join(ROOT, "results", "cache", "closed.sqlite"))
    args = ap.parse_args()

    mc = load_model_config(args.model)
    name = mc["name"]
    pool = args.pool or ("intersection" if mc.get("role") == "tier" else "union")
    backend = run17.MeteredBackend(build_backend(mc))
    cfg = build_gen_config(load_base(), mc)
    qids = set(run17.evaluable_qids(name, args.dataset, pool))
    by_qid = {i.qid: i for i in run17.read_jsonl(os.path.join(ROOT, "data", "processed", f"{args.dataset}_validation.jsonl"))}
    insts = sorted((by_qid[q] for q in qids), key=lambda i: i.qid)
    out_dir = os.path.join(ROOT, "results", "closed", "oracle", args.dataset, name)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "drop_gold.jsonl")
    done = set()
    if os.path.exists(out_path):
        done = {json.loads(l)["qid"] for l in open(out_path, encoding="utf-8")}
    todo = [i for i in insts if i.qid not in done]
    cache = QueryCache(path=args.cache)
    t0 = time.time()
    print(f"drop-gold oracle | {name} | {args.dataset}/{pool} | todo {len(todo)} (done {len(done)})", flush=True)
    n_ok = 0
    with open(out_path, "a", encoding="utf-8") as f, ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(one, i, backend, cfg, cache, 1): i.qid for i in todo}
        for fut in as_completed(futs):
            try:
                row, _ = fut.result()
            except Exception as e:
                print(f"  ! {futs[fut]}: {type(e).__name__}: {str(e)[:200]}", flush=True)
                continue
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()
            n_ok += 1
    u = backend.usage
    pin, pout = PRICE_CNY.get(name, (0.0, 0.0))
    cost = u["prompt_tokens"] / 1e6 * pin + u["completion_tokens"] / 1e6 * pout
    cpath = out_path.replace(".jsonl", ".cost.json")
    prev = json.load(open(cpath)) if os.path.exists(cpath) else {"runs": []}
    prev["runs"].append({**u, "est_cost_cny": round(cost, 5), "n_instances_run": n_ok,
                         "wall_s": round(time.time() - t0, 1), "time": time.strftime("%Y-%m-%d %H:%M:%S")})
    json.dump(prev, open(cpath, "w"), indent=1)
    print(f"  done {n_ok}/{len(todo)}  issued calls {u['calls']}  ≈¥{cost:.4f}  cache {cache.stats}", flush=True)


if __name__ == "__main__":
    main()
