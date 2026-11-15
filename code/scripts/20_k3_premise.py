#!/usr/bin/env python3
"""K3 premise screening (design v2, 2.3): repeats 0-2 only.

Per constructed variant and repeat r in {0,1,2}, with the same answer-only
prompt the methods use (subset_prompt == Vanilla, so keys are shared with
nothing evaluated at repeat >= 3):
  full        all passages                     -> correct?
  drop_ap     answer passage removed            -> still correct? (a copy substitutes)
  drop_group  answer passage + all its copies   -> still correct? (group necessity)
For redundancy 0, drop_group == drop_ap (one call).
Correctness uses the 01c matching rule (unchanged).

  python scripts/20_k3_premise.py --model configs/models/closed/gpt-6-luna.yaml \
      --instances data/constructed/k3/musique.gpt-6-luna.n50.jsonl.gz
  -> results/closed/k3/<pool>/<model>/premise.jsonl (+ .cost.json)
"""
from __future__ import annotations

import argparse
import gzip
import importlib.util
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)

from src.data.schema import Instance  # noqa: E402
from src.pipelines.subset import _answers_for, subset_prompt  # noqa: E402
from src.utils.cache import QueryCache  # noqa: E402
from src.utils.config import build_backend, build_gen_config, load_base, load_model_config  # noqa: E402
from src.utils.parsing import normalize_answer  # noqa: E402


def _load(name, rel):
    s = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


run17 = _load("run17", "scripts/17_run_closed.py")
leak01c = run17.screen14.leak01c
PRICE_CNY = run17.screen14.PRICE_CNY
PREMISE_REPEATS = (0, 1, 2)


def premise_one(inst, backend, cfg, cache, workers):
    M = inst.M
    ap = inst.meta["answer_passage"]
    group = set(inst.meta["redundancy_group"])
    probes = {"full": list(range(M)), "drop_ap": [i for i in range(M) if i != ap]}
    if group != {ap}:
        probes["drop_group"] = [i for i in range(M) if i not in group]
    out = {"qid": inst.qid, "base_qid": inst.meta["base_qid"], "condition": inst.meta["condition"],
           "redundancy": inst.meta["redundancy"], "n_hop": inst.n_hop, "M": M}
    calls = 0
    for r in PREMISE_REPEATS:
        names = list(probes)
        obs, c = _answers_for([subset_prompt(inst, probes[n]) for n in names], backend, cfg, cache, r, workers)
        calls += c
        for n, o in zip(names, obs):
            a = normalize_answer(o.answer) if o.ok and o.answer else None
            out.setdefault(f"{n}_answer", []).append(a)
            out.setdefault(f"{n}_correct", []).append(bool(leak01c.matches_gold(a, inst)) if a else False)
    if "drop_group" not in probes:
        out["drop_group_answer"], out["drop_group_correct"] = out["drop_ap_answer"], out["drop_ap_correct"]
    return out, calls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--instances", required=True)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--inner-workers", type=int, default=3)
    ap.add_argument("--cache", default=os.path.join(ROOT, "results", "cache", "closed.sqlite"))
    args = ap.parse_args()

    mc = load_model_config(args.model)
    name = mc["name"]
    backend = run17.MeteredBackend(build_backend(mc))
    cfg = build_gen_config(load_base(), mc)
    op = gzip.open if args.instances.endswith(".gz") else open
    with op(args.instances, "rt", encoding="utf-8") as fh:
        insts = sorted((Instance.from_json(json.loads(l)) for l in fh if l.strip()), key=lambda i: i.qid)
    pool = os.path.basename(args.instances).replace(".jsonl.gz", "").replace(".jsonl", "")
    out_dir = os.path.join(ROOT, "results", "closed", "k3", pool, name)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "premise.jsonl")
    done = set()
    if os.path.exists(out_path):
        done = {json.loads(l)["qid"] for l in open(out_path, encoding="utf-8")}
    todo = [i for i in insts if i.qid not in done]
    cache = QueryCache(path=args.cache)
    t0 = time.time()
    print(f"K3 premise | {name} | {pool} | todo {len(todo)} (done {len(done)})", flush=True)
    n_ok = 0
    with open(out_path, "a", encoding="utf-8") as f, ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(premise_one, i, backend, cfg, cache, args.inner_workers): i.qid for i in todo}
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
