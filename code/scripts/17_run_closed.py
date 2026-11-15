#!/usr/bin/env python3
"""Phase 2: attribution methods on closed API models, over their screened
evaluable sets (phase 1; 16_summarize_screening.py merges truncation re-asks).

Methods: V1-V7, P1-P5 (registry), RM<K> (random masking), LOI (leave-one-in).
MExGen-LOO needs no calls (re-scored from P1 by 18_analyze_closed.py).

  set -a; . /home/claude/.mht_api.env; set +a
  python -u scripts/17_run_closed.py --model configs/models/closed/claude-haiku-5-5.yaml \
      --dataset musique --methods V1,P1,RM,LOI --sample-n 12 --tag pilot \
      --rm-k 64 --full-repeats 3 --outer-workers 6 --inner-workers 4

Outputs  results/closed/raw/<ds>/<model>/<tag>/<METHOD>[.r<k>].jsonl (+ .manifest.json,
.cost.json). Cost is computed from the token usage of calls actually issued in
this run (cache hits are free) with the price list of 14_screen_closed.py.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import zlib
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)

from src.data.schema import read_jsonl
from src.eval.filtering import stratified_sample
from src.pipelines.registry import METHODS, get_method
from src.pipelines.runner import run_method
from src.pipelines.subset import run_leave_one_in, run_random_mask
from src.utils.cache import QueryCache
from src.utils.config import build_backend, build_gen_config, load_base, load_model_config


def _load(name, rel):
    s = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


screen14 = _load("screen14", "scripts/14_screen_closed.py")
run02 = screen14.run02


class CacheMiss(RuntimeError):
    pass


class MeteredBackend:
    """Forwards to a backend and sums token usage of issued (non-cached) calls."""

    def __init__(self, inner, cache_only: bool = False):
        self._inner = inner
        self.cache_only = cache_only
        self._lock = threading.Lock()
        self.usage = {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0,
                      "reasoning_tokens": 0, "finish_length": 0, "latency_s": 0.0}

    def __getattr__(self, k):
        return getattr(self._inner, k)

    def generate_with_meta(self, messages, cfg, seed=None):
        if self.cache_only:
            raise CacheMiss("cache-only run would issue an API call")
        text, meta = self._inner.generate_with_meta(messages, cfg, seed=seed)
        with self._lock:
            u = self.usage
            u["calls"] += 1
            for f in ("prompt_tokens", "completion_tokens", "reasoning_tokens"):
                u[f] += (meta or {}).get(f) or 0
            u["finish_length"] += int((meta or {}).get("finish_reason") == "length")
            u["latency_s"] += (meta or {}).get("latency_s") or 0.0
        return text, meta


def evaluable_qids(model: str, dataset: str, pool: str) -> list[str]:
    summ = json.load(open(os.path.join(ROOT, "results", "closed", "screen", "summary.json")))
    for r in summ["screening"]:
        if r["model"] == model and r["dataset"] == dataset and r["pool"] == pool:
            if not r["complete"]:
                sys.exit(f"screening of {model}/{dataset}/{pool} is incomplete")
            return r["evaluable_qids"]
    sys.exit(f"no screening summary for {model}/{dataset}/{pool}; run 16_summarize_screening.py")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--dataset", required=True, choices=["hotpotqa", "musique", "symfever", "qasper"])
    ap.add_argument("--methods", required=True, help="comma list: V1..V7,P1..P5,RM,LOI")
    ap.add_argument("--pool", default=None, help="default: union for role=main, intersection for role=tier")
    ap.add_argument("--sample-n", type=int, default=None, help="hop-stratified subset (pilot / dev)")
    ap.add_argument("--sample-seed", type=int, default=0)
    ap.add_argument("--exclude-qids", default=None, help="jsonl/json of qids to leave out (e.g. the dev set)")
    ap.add_argument("--instances", default=None,
                    help="jsonl(.gz) of constructed instances (e.g. K3); bypasses the evaluable-set lookup")
    ap.add_argument("--include-qids", default=None,
                    help="screening jsonl (keeps rows with evaluable=true) or json list of qids to keep")
    ap.add_argument("--tag", default="main")
    ap.add_argument("--shard", default=None,
                    help="i[,j...]/n: only qids with crc32(qid) %% n in {i,j,...}. Lets several endpoints share one output "
                         "file (stand-in configs with fingerprint_base_url); not part of the manifest.")
    ap.add_argument("--rm-k", type=int, default=32)
    ap.add_argument("--full-repeats", type=int, default=0, help="P*: K extra full-context draws at the ablation T")
    ap.add_argument("--repeat", type=int, default=0)
    ap.add_argument("--outer-workers", type=int, default=6)
    ap.add_argument("--inner-workers", type=int, default=4)
    ap.add_argument("--sample-workers", type=int, default=5, help="concurrent draws of one multi-sample set")
    ap.add_argument("--cache-only", action="store_true",
                    help="never call the API: verify that earlier runs (e.g. the pilot) are fully reused")
    ap.add_argument("--cache", default=os.path.join(ROOT, "results", "cache", "closed.sqlite"))
    args = ap.parse_args()

    import src.stages.sampling as sampling_mod
    sampling_mod.SAMPLE_WORKERS = args.sample_workers
    base = load_base()
    mc = load_model_config(args.model)
    name = mc["name"]
    pool = args.pool or ("intersection" if mc.get("role") == "tier" else "union")
    backend = MeteredBackend(build_backend(mc), cache_only=args.cache_only)
    cfg = build_gen_config(base, mc)
    agg = base["aggregation"]
    n_v, n_p = base["sampling"]["n_samples_verbalize"], base["sampling"]["n_samples_perturbation"]

    if args.instances:
        import gzip
        from src.data.schema import Instance
        op = gzip.open if args.instances.endswith(".gz") else open
        with op(args.instances, "rt", encoding="utf-8") as fh:
            insts = sorted((Instance.from_json(json.loads(l)) for l in fh if l.strip()), key=lambda i: i.qid)
        pool = os.path.basename(args.instances)
    else:
        qids = set(evaluable_qids(name, args.dataset, pool))
        by_qid = {i.qid: i for i in read_jsonl(os.path.join(ROOT, "data", "processed", f"{args.dataset}_validation.jsonl"))}
        insts = sorted((by_qid[q] for q in qids), key=lambda i: i.qid)
    if args.include_qids:
        if args.include_qids.endswith(".jsonl"):
            keep = {json.loads(l)["qid"] for l in open(args.include_qids) if l.strip() and json.loads(l).get("evaluable")}
        else:
            keep = json.load(open(args.include_qids))
            keep = set(keep if isinstance(keep, list) else keep["qids"])
        insts = [i for i in insts if i.qid in keep]
    if args.exclude_qids:
        ex = json.load(open(args.exclude_qids))
        ex = set(ex if isinstance(ex, list) else ex["qids"])
        insts = [i for i in insts if i.qid not in ex]
    if args.sample_n:
        insts = stratified_sample(insts, args.sample_n, "hop" if args.dataset == "musique" else "none",
                                  args.sample_seed, verbose=False)
    out_dir = os.path.join(ROOT, "results", "closed", "raw", args.dataset, name, args.tag)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "qids.json"), "w") as f:
        json.dump(sorted(i.qid for i in insts), f)
    cache = QueryCache(path=args.cache)

    for mid in [m.strip() for m in args.methods.split(",") if m.strip()]:
        is_reg = mid in METHODS
        label = f"RM{args.rm_k}" if mid == "RM" else mid
        suffix = f".r{args.repeat}" if args.repeat else ""
        out_path = os.path.join(out_dir, f"{label}{suffix}.jsonl")
        manifest = {"script": "17_run_closed", "method": label, "model": name, "dataset": args.dataset,
                    "pool": pool, "fingerprint": backend.fingerprint(cfg), "repeat": args.repeat,
                    "n_samples": (n_v if get_method(mid).is_verbalize else n_p) if is_reg else 1,
                    "aggregation": agg, "rm_k": args.rm_k if mid == "RM" else None,
                    "full_repeats": args.full_repeats if is_reg and not get_method(mid).is_verbalize else 0,
                    "sample_n": args.sample_n, "sample_seed": args.sample_seed,
                    "exclude_qids": args.exclude_qids,
                    **({"include_qids": args.include_qids} if args.include_qids else {})}
        run02.check_or_write_manifest(out_path, manifest, allow_unmanifested=False)
        done = run02.already_done(out_path)
        todo = [i for i in insts if i.qid not in done]
        if args.shard:
            sis, sn = args.shard.split("/")
            sis, sn = {int(x) for x in sis.split(",")}, int(sn)
            todo = [i for i in todo if zlib.crc32(i.qid.encode()) % sn in sis]
        u0 = dict(backend.usage)
        t0 = time.time()
        print(f"{label} | {name} | {args.dataset}/{pool} | todo {len(todo)} (done {len(done)})", flush=True)

        def work(inst):
            if is_reg:
                m = get_method(mid)
                return run_method(inst, m, backend, cfg=cfg, n_samples=n_v if m.is_verbalize else n_p,
                                  lam=agg["lambda"], beta=agg["beta"], tau=agg["tau"], cache=cache,
                                  inner_workers=args.inner_workers, repeat=args.repeat,
                                  n_full_repeats=0 if m.is_verbalize else args.full_repeats)
            if mid == "RM":
                return run_random_mask(inst, backend, cfg, K=args.rm_k, cache=cache, repeat=args.repeat,
                                       inner_workers=args.inner_workers, tau=agg["tau"])
            if mid == "LOI":
                return run_leave_one_in(inst, backend, cfg, cache=cache, repeat=args.repeat,
                                        inner_workers=args.inner_workers, tau=agg["tau"])
            raise SystemExit(f"unknown method {mid}")

        n_ok = 0
        with open(out_path, "a", encoding="utf-8") as f, ThreadPoolExecutor(max_workers=args.outer_workers) as ex:
            futs = {ex.submit(work, i): i.qid for i in todo}
            for fut in as_completed(futs):
                try:
                    res = fut.result()
                except Exception as e:  # failed qids are retried on the next run
                    print(f"  ! {futs[fut]}: {type(e).__name__}: {str(e)[:200]}", flush=True)
                    continue
                f.write(json.dumps(res.to_json(), ensure_ascii=False) + "\n")
                f.flush()
                n_ok += 1
                if n_ok % 25 == 0:
                    print(f"  {n_ok}/{len(todo)} {time.time()-t0:.0f}s", flush=True)

        du = {k: backend.usage[k] - u0[k] for k in u0}
        pin, pout = screen14.PRICE_CNY.get(name, (0.0, 0.0))
        cost = du["prompt_tokens"] / 1e6 * pin + du["completion_tokens"] / 1e6 * pout
        cpath = out_path.replace(".jsonl", ".cost.json")
        prev = json.load(open(cpath)) if os.path.exists(cpath) else {"runs": []}
        prev["runs"].append({**du, "est_cost_cny": round(cost, 5), "n_instances_run": n_ok,
                             "wall_s": round(time.time() - t0, 1), "time": time.strftime("%Y-%m-%d %H:%M:%S")})
        json.dump(prev, open(cpath, "w"), indent=1)
        print(f"  done {n_ok}/{len(todo)}  issued calls {du['calls']}  tokens {du['prompt_tokens']}/"
              f"{du['completion_tokens']}  truncated {du['finish_length']}  ≈¥{cost:.4f}", flush=True)
    print(f"cache: {cache.stats}")


if __name__ == "__main__":
    main()
