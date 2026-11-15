#!/usr/bin/env python3
"""Run one method on one model over one dataset.

The atomic unit of the experiment grid. 03_run_all.py calls this in a loop, but
it is runnable standalone for debugging a single cell.

  python scripts/02_run_method.py --method P4 --model qwen3-8b \
      --dataset hotpotqa --n-instances 200

Results stream to results/raw/<dataset>/<model>/<method>.jsonl as they complete,
so a crash loses at most one instance and reruns skip finished qids.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tqdm import tqdm

from src.data.loaders import load_dataset_by_name
from src.eval.filtering import (
    filter_instances, is_yesno, load_evaluable_qids, load_leaked_qids,
    stratified_sample,
)
from src.eval.metrics import summarize
from src.pipelines.registry import get_method
from src.pipelines.runner import run_method
from src.utils.cache import QueryCache
from src.utils.config import build_backend, build_gen_config, load_base, load_model_config
from src.utils.parsing import ThinkingLeakError


def already_done(path: str) -> set[str]:
    if not os.path.exists(path):
        return set()
    done = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                done.add(json.loads(line)["qid"])
            except Exception:
                pass
    return done


def run_manifest(args, method, model_cfg, backend, cfg, n_samples, agg) -> dict:
    """Everything that defines what an output file means. Resuming into a file
    whose manifest differs would silently mix incompatible rows."""
    safe_model_cfg = {k: v for k, v in model_cfg.items()
                      if "key" not in k.lower() and "token" not in k.lower()}
    return {
        "method": method.mid,
        "dataset": args.dataset,
        "split": args.split,
        "model_cfg": safe_model_cfg,
        "fingerprint": backend.fingerprint(cfg),
        "n_samples": n_samples,
        "aggregation": agg,
        "repeat": args.repeat,
        "n_full_repeats": args.full_repeats,
        "legacy_cache_keys": args.legacy_cache_keys,
    }


def check_or_write_manifest(out_path: str, manifest: dict, allow_unmanifested: bool) -> None:
    mpath = out_path + ".manifest.json"
    has_rows = os.path.exists(out_path) and os.path.getsize(out_path) > 0
    if os.path.exists(mpath):
        with open(mpath, encoding="utf-8") as f:
            old = json.load(f)
        if json.loads(json.dumps(old, sort_keys=True, default=str)) != \
                json.loads(json.dumps(manifest, sort_keys=True, default=str)):
            diff = sorted(k for k in set(old) | set(manifest) if old.get(k) != manifest.get(k))
            sys.exit(f"refusing to resume {out_path}: run configuration differs from its manifest "
                     f"in {diff}. Use a different --out-root or --repeat.")
        return
    if has_rows and not allow_unmanifested:
        sys.exit(f"refusing to resume {out_path}: it has rows but no manifest (legacy run). "
                 f"Pass --allow-unmanifested-resume only if you are sure the configuration matches.")
    with open(mpath, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1, sort_keys=True, default=str)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", required=True)
    ap.add_argument("--model", required=True, help="model config name or path")
    ap.add_argument("--dataset", required=True, choices=["hotpotqa", "musique"])
    ap.add_argument("--split", default="validation")
    ap.add_argument("--n-instances", type=int, default=200)
    ap.add_argument("--hops", type=int, nargs="+", default=None,
                    help="MuSiQue only: restrict to these hop counts")
    ap.add_argument("--out-root", default="results/raw")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--legacy-cache-keys", action="store_true",
                    help="replay the AAAI-27 cache (v1 keys without endpoint/config fingerprint); "
                         "never use for new endpoints")
    ap.add_argument("--measure-full-noise", action="store_true",
                    help="alias for --full-repeats N (perturbation with N>1)")
    ap.add_argument("--full-repeats", type=int, default=0,
                    help="perturbation: also draw K full-context samples at the ablation "
                         "temperature (works for single-pass P1 too) and record "
                         "Pr_T(answer_full != a0) per instance")
    ap.add_argument("--repeat", type=int, default=0,
                    help="independent measurement index: fresh cache namespace and seeds; "
                         "outputs go to <METHOD>.r<repeat>.jsonl when > 0")
    ap.add_argument("--allow-unmanifested-resume", action="store_true",
                    help="resume into an output file written before manifests existed")
    ap.add_argument("--resume", action="store_true", default=True)
    ap.add_argument("--exclude-leaked", default=None,
                    help="path to a 01c leakage.json; skips instances the model "
                         "answers without context (no causal signal to detect)")
    ap.add_argument("--only-qids", default=None,
                    help="path to a 01c report; evaluate ONLY its evaluable set "
                         "(no leakage AND model answers correctly) -- the subset "
                         "where gold supporting facts are a valid target")
    ap.add_argument("--outer-workers", type=int, default=1,
                    help="instances processed in parallel; size with "
                         "inner-workers to saturate all vLLM replicas")
    ap.add_argument("--inner-workers", type=int, default=1,
                    help="parallel ablations per instance (perturbation only)")
    ap.add_argument("--sample-n", type=int, default=None,
                    help="after filtering, draw this many instances (see "
                         "--stratify-by). Use to cap the O(M*N) cost of the "
                         "interventional methods.")
    ap.add_argument("--stratify-by", default="hop", choices=["hop", "none"],
                    help="balance the sample across strata; 'hop' keeps the "
                         "deep MuSiQue strata from being crowded out")
    ap.add_argument("--sample-seed", type=int, default=0)
    ap.add_argument("--drop-leaked", action="store_true",
                    help="also SKIP leaked instances rather than just tagging "
                         "them (saves queries, but loses the full-set numbers)")
    ap.add_argument("--drop-yesno", action="store_true",
                    help="drop binary-answer questions (~50%% flip prior)")
    args = ap.parse_args()

    base = load_base()
    model_cfg = load_model_config(args.model)
    method = get_method(args.method)
    backend = build_backend(model_cfg)
    cfg = build_gen_config(base, model_cfg)

    n_v = base["sampling"]["n_samples_verbalize"]
    n_p = base["sampling"]["n_samples_perturbation"]
    n_samples = n_v if method.is_verbalize else n_p
    agg = base["aggregation"]

    ld_kw = {"split": args.split, "limit": args.n_instances}
    if args.dataset == "musique":
        # Balance across hop counts unless a specific hop is requested; the
        # first N rows are otherwise almost all 2-hop, ruining Sec. 6.5.
        if args.hops:
            ld_kw["hops"] = args.hops
        else:
            ld_kw["balance_hops"] = True
    instances = load_dataset_by_name(args.dataset, **ld_kw)

    # Evaluation-validity handling (see 01c). Leaked instances have no causal
    # signal for ablation to find. By default we TAG rather than drop them, so a
    # single run yields both the full-set and context-dependent-subset numbers;
    # --drop-leaked additionally skips them to save queries.
    leaked = load_leaked_qids(args.exclude_leaked, model=model_cfg.get("model"))

    if args.only_qids:
        keep = load_evaluable_qids(args.only_qids, model=model_cfg.get("model"))
        n0 = len(instances)
        instances = [i for i in instances if i.qid in keep]
        print(f"  restricted to the evaluable set: {n0} -> {len(instances)}")
        if not instances:
            print("  ! nothing left; is the 01c report from the same dataset "
                  "and sampled over the same instances?")
            return

    if args.drop_yesno or (leaked and args.drop_leaked):
        instances = filter_instances(
            instances, leaked if args.drop_leaked else None, args.drop_yesno
        )
    elif leaked:
        print(f"  tagging {sum(1 for i in instances if i.qid in leaked)} leaked "
              f"instances (kept; aggregate reports both views)")

    # Sampling comes last so the draw is made from the final, filtered pool.
    if args.sample_n:
        instances = stratified_sample(
            instances, args.sample_n, args.stratify_by, args.sample_seed
        )

    model_name = model_cfg.get("name", os.path.basename(args.model).replace(".yaml", ""))
    out_dir = os.path.join(args.out_root, args.dataset, model_name)
    os.makedirs(out_dir, exist_ok=True)
    suffix = f".r{args.repeat}" if args.repeat else ""
    out_path = os.path.join(out_dir, f"{method.mid}{suffix}.jsonl")
    if args.measure_full_noise and not args.full_repeats and not method.is_verbalize:
        args.full_repeats = n_samples if n_samples > 1 else 0
    check_or_write_manifest(
        out_path, run_manifest(args, method, model_cfg, backend, cfg, n_samples, agg),
        args.allow_unmanifested_resume,
    )

    done = already_done(out_path) if args.resume else set()
    todo = [i for i in instances if i.qid not in done]

    cache = None if args.no_cache else QueryCache(
        path=base["cache"]["path"], enabled=base["cache"]["enabled"],
        legacy_keys=args.legacy_cache_keys,
    )

    print(f"{method.mid} | {model_name} | {args.dataset} | "
          f"{len(todo)} to run ({len(done)} done) | N={n_samples}")
    est = sum(method.query_cost(i.M, n_samples) for i in todo)
    print(f"estimated queries: {est:,}")

    import threading
    from concurrent.futures import ThreadPoolExecutor, as_completed

    write_lock = threading.Lock()
    leak_event = threading.Event()
    leak_msg = [None]
    results = []

    # Concurrency model: `outer_workers` instances run in parallel, and for the
    # interventional pipeline each instance fans its M ablations out over
    # `inner_workers`. Total in-flight requests ~= outer*inner, which should be
    # sized to keep every vLLM replica (data_parallel_size) busy. The cache and
    # the output file are both mutex-guarded; the OpenAI client is thread-safe.
    def _work(inst):
        if leak_event.is_set():
            return None
        try:
            res = run_method(
                inst, method, backend,
                cfg=cfg, n_samples=n_samples,
                lam=agg["lambda"], beta=agg["beta"], tau=agg["tau"],
                cache=cache, inner_workers=args.inner_workers,
                n_full_repeats=args.full_repeats, repeat=args.repeat,
            )
        except ThinkingLeakError as e:
            leak_msg[0] = str(e)
            leak_event.set()
            return None
        res.meta["leaked"] = inst.qid in leaked
        res.meta["yesno"] = is_yesno(inst)
        return res

    with open(out_path, "a", encoding="utf-8") as f:
        if args.outer_workers <= 1:
            iterator = (_work(i) for i in todo)
            wrapped = tqdm(iterator, total=len(todo), desc=method.mid)
            for res in wrapped:
                if res is None:
                    if leak_event.is_set():
                        break
                    continue
                f.write(json.dumps(res.to_json(), ensure_ascii=False) + "\n")
                f.flush()
                results.append(res)
        else:
            with ThreadPoolExecutor(max_workers=args.outer_workers) as ex:
                futures = {ex.submit(_work, i): i for i in todo}
                for fut in tqdm(as_completed(futures), total=len(todo),
                                desc=method.mid):
                    res = fut.result()
                    if res is None:
                        continue
                    with write_lock:
                        f.write(json.dumps(res.to_json(), ensure_ascii=False) + "\n")
                        f.flush()
                        results.append(res)

    if leak_event.is_set():
        print(f"\n!! {leak_msg[0]}\n!! thinking mode is NOT disabled for "
              f"{model_name}; results may be invalid. Check the serving flags.")

    if cache:
        print(f"cache: {cache.stats}")
        cache.close()

    if results:
        summ = summarize(results, instances=todo)
        print("summary (this run only):")
        for k, v in summ.items():
            print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")


if __name__ == "__main__":
    main()
