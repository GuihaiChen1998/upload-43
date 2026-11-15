#!/usr/bin/env python3
"""Cross-endpoint agreement for one model (round 23: gpt-6-luna on S3AI vs BootToken).

Re-asks the K3 premise probes (full / drop_ap / drop_group, repeats 0-2) of a reference
endpoint's premise.jsonl on a second endpoint, then compares:
  correctness rate per probe on each endpoint,
  answer agreement across endpoints (same repeat) vs. within the reference endpoint
  (repeat r vs r+1), and the premise verdicts (drop_ap survives / drop_group breaks).
If cross-endpoint agreement is close to within-endpoint agreement, the two endpoints are
treated as the same model and results of different (method, dataset) files may come from
different endpoints (each file's manifest records its endpoint).

  python scripts/24_endpoint_agreement.py --model configs/models/closed/gpt-6-luna.yaml \
      --ref-premise results/closed/k3/hotpotqa.gpt-6-luna.n50.v2/gpt-6-luna/premise.jsonl \
      --instances data/constructed/k3/hotpotqa.gpt-6-luna.n50.v2.jsonl.gz --conditions F,C
"""
from __future__ import annotations

import argparse
import gzip
import importlib.util
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
from src.data.schema import Instance  # noqa: E402
from src.utils.cache import QueryCache  # noqa: E402
from src.utils.config import build_backend, build_gen_config, load_base, load_model_config  # noqa: E402

_s = importlib.util.spec_from_file_location("k3p", os.path.join(ROOT, "scripts", "20_k3_premise.py"))
k3p = importlib.util.module_from_spec(_s)
_s.loader.exec_module(k3p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--ref-premise", required=True)
    ap.add_argument("--instances", required=True)
    ap.add_argument("--conditions", default="F,C")
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    conds = set(args.conditions.split(","))
    mc = load_model_config(args.model)
    backend = k3p.run17.MeteredBackend(build_backend(mc))
    cfg = build_gen_config(load_base(), mc)
    cache = QueryCache(path=os.path.join(ROOT, "results", "cache", "closed.sqlite"))
    ref = {r["qid"]: r for r in map(json.loads, open(args.ref_premise, encoding="utf-8"))}
    with gzip.open(args.instances, "rt", encoding="utf-8") as fh:
        insts = [Instance.from_json(json.loads(l)) for l in fh if l.strip()]
    insts = [i for i in insts if i.meta["condition"] in conds and i.qid in ref]
    with ThreadPoolExecutor(args.workers) as ex:
        rows = list(ex.map(lambda i: k3p.premise_one(i, backend, cfg, cache, 1)[0], insts))
    stats = {}
    for probe in ("full", "drop_ap", "drop_group"):
        n = agree_x = agree_w = nw = 0
        acc_ref = acc_new = 0
        for r in rows:
            a, b = ref[r["qid"]][f"{probe}_answer"], r[f"{probe}_answer"]
            ca, cb = ref[r["qid"]][f"{probe}_correct"], r[f"{probe}_correct"]
            for k in range(3):
                n += 1
                agree_x += a[k] == b[k]
                acc_ref += ca[k]
                acc_new += cb[k]
            for k in range(2):
                nw += 1
                agree_w += a[k] == a[k + 1]
        stats[probe] = {"n": n, "acc_ref": round(acc_ref / n, 3), "acc_new": round(acc_new / n, 3),
                        "agree_cross": round(agree_x / n, 3), "agree_within_ref": round(agree_w / nw, 3)}
    u = backend.usage
    out = {"model": mc["name"], "endpoint": mc.get("endpoint"), "instances": args.instances,
           "conditions": sorted(conds), "n_variants": len(rows), "stats": stats, "usage": u}
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    json.dump(out, open(args.out, "w"), indent=1)
    with open(args.out.replace(".json", ".rows.jsonl"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
