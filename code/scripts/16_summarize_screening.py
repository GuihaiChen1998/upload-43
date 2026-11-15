#!/usr/bin/env python3
"""Summarise the closed-model evaluable screening (phase 1).

For every model x dataset x pool summary written by 14_screen_closed.py:
evaluable / leak rates, evaluable set size, recorded token usage and cost.

Audit: the audit sample is drawn OUTSIDE the open-model union (MuSiQue
stratified by hop, proportional allocation). The share of audit instances that
are evaluable for a closed model estimates how many of that model's evaluable
instances the union misses:
    missed ~= rate_audit x N_outside   (MuSiQue: sum over hop strata of
                                       rate_h x N_outside_h)
with a Wilson 95% interval on the rate (stratified rates combined with the
stratum weights).

  python scripts/16_summarize_screening.py   # -> results/closed/screen/summary.{json,md}
"""
from __future__ import annotations

import glob
import importlib.util
import json
import math
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
SCREEN = os.path.join(ROOT, "results", "closed", "screen")
_s = importlib.util.spec_from_file_location("screen14", os.path.join(ROOT, "scripts", "14_screen_closed.py"))
screen14 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(screen14)
BUCKETS = ["leaked", "context_dep", "abstained_correct", "abstained_wrong", "both_wrong", "unparsable"]


def load_rows(summary_path: str) -> tuple[list[dict], int]:
    """Rows of one screening run, with rows from <pool>.retrunc.jsonl (re-screened
    after max_tokens truncation) replacing the originals."""
    base = summary_path.replace(".summary.json", "")
    rows = {json.loads(l)["qid"]: json.loads(l) for l in open(base + ".jsonl", encoding="utf-8")}
    n_re = 0
    if os.path.exists(base + ".retrunc.jsonl"):
        for l in open(base + ".retrunc.jsonl", encoding="utf-8"):
            r = json.loads(l)
            rows[r["qid"]] = r
            n_re += 1
    return list(rows.values()), n_re


def stats(rows: list[dict], model: str) -> dict:
    b = {k: [] for k in BUCKETS}
    hop_total, hop_eval, fin = {}, {}, {}
    tin = tout = 0
    for r in rows:
        b[r["bucket"]].append(r["qid"])
        h = r.get("n_hop")
        if h is not None:
            hop_total[str(h)] = hop_total.get(str(h), 0) + 1
            hop_eval[str(h)] = hop_eval.get(str(h), 0) + int(r["evaluable"])
        for t in ("empty", "full"):
            m = r[f"{t}_meta"]
            tin += m.get("prompt_tokens") or 0
            tout += m.get("completion_tokens") or 0
            fin[m.get("finish_reason")] = fin.get(m.get("finish_reason"), 0) + 1
    pin, pout = screen14.PRICE_CNY.get(model, (0.0, 0.0))
    n = len(rows)
    ev = b["context_dep"] + b["abstained_correct"]
    return {"n": n, "buckets": b, "evaluable": ev, "evaluable_rate": len(ev) / n if n else 0,
            "leak_rate": len(b["leaked"]) / n if n else 0, "hop_total": hop_total, "hop_evaluable": hop_eval,
            "finish_reasons": fin, "prompt_tokens": tin, "completion_tokens": tout,
            "est_cost_cny": round(tin / 1e6 * pin + tout / 1e6 * pout, 4)}


def wilson(k, n, z=1.96):
    if n == 0:
        return (math.nan, math.nan)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def main():
    pools = {ds: json.load(open(os.path.join(ROOT, "results", "closed", "pools", f"{ds}.json")))
             for ds in ("hotpotqa", "musique")}
    rows, audit_rows = [], []
    for f in sorted(glob.glob(os.path.join(SCREEN, "*", "*", "*.summary.json"))):
        if ".limit" in os.path.basename(f):
            continue
        meta = json.load(open(f))
        run_rows, n_re = load_rows(f)
        st = stats(run_rows, meta["model"])
        s = {**meta, **st}
        n_pool = len(pools[s["dataset"]][s["pool"]])
        rec = {
            "model": s["model"], "endpoint": s.get("endpoint"), "dataset": s["dataset"], "pool": s["pool"],
            "n_done": s["n"], "n_pool": n_pool, "complete": s["n"] == n_pool, "n_rescreened_truncated": n_re,
            "evaluable": len(s["evaluable"]), "evaluable_rate": round(s["evaluable_rate"], 3),
            "leak_rate": round(s["leak_rate"], 3), "buckets": {k: len(v) for k, v in st["buckets"].items()},
            "prompt_tokens": st["prompt_tokens"], "completion_tokens": st["completion_tokens"],
            "est_cost_cny": st["est_cost_cny"], "finish_reasons": st["finish_reasons"],
            "hop_evaluable": st["hop_evaluable"], "hop_total": st["hop_total"],
            "evaluable_qids": s["evaluable"],
        }
        rows.append(rec)
        if s["pool"] == "audit":
            P = pools[s["dataset"]]
            if s["dataset"] == "musique":
                tot, var_terms, N = 0.0, [], P["n_outside_union"]
                for h, Nh in P["outside_union_strata"].items():
                    nh = int(st["hop_total"].get(str(h), 0))
                    kh = int(st["hop_evaluable"].get(str(h), 0))
                    if nh:
                        ph = kh / nh
                        tot += ph * Nh
                        var_terms.append((Nh / N) ** 2 * ph * (1 - ph) / max(nh - 1, 1))
                rate = tot / N
                se = math.sqrt(sum(var_terms))
                lo, hi = max(0.0, rate - 1.96 * se), min(1.0, rate + 1.96 * se)
            else:
                k, n, N = len(s["evaluable"]), s["n"], P["n_outside_union"]
                rate = k / n if n else math.nan
                lo, hi = wilson(k, n)
            audit_rows.append({"model": s["model"], "dataset": s["dataset"], "audit_n": s["n"],
                               "audit_evaluable_rate": round(rate, 3), "ci": [round(lo, 3), round(hi, 3)],
                               "n_outside_union": N, "est_missed_evaluable": round(rate * N),
                               "est_missed_ci": [round(lo * N), round(hi * N)]})
    out = {"screening": rows, "audit": audit_rows}
    with open(os.path.join(SCREEN, "summary.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    lines = ["| 模型 | 端点 | 数据集 | 池 | 完成/池 | 截断重筛 | 可评估 | 可评估率 | 泄漏率 | 估算花费(¥) |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['model']} | {r['endpoint']} | {r['dataset']} | {r['pool']} | {r['n_done']}/{r['n_pool']} | "
                     f"{r['n_rescreened_truncated']} | {r['evaluable']} | {r['evaluable_rate']} | {r['leak_rate']} | {r['est_cost_cny']} |")
    lines += ["", "| 模型 | 数据集 | 审计 n | 审计可评估率 [95% CI] | 并集外总数 | 估计漏掉的可评估题 [CI] |", "|---|---|---|---|---|---|"]
    for a in audit_rows:
        lines.append(f"| {a['model']} | {a['dataset']} | {a['audit_n']} | {a['audit_evaluable_rate']} {a['ci']} | "
                     f"{a['n_outside_union']} | {a['est_missed_evaluable']} {a['est_missed_ci']} |")
    md = "\n".join(lines)
    with open(os.path.join(SCREEN, "summary.md"), "w") as f:
        f.write(md + "\n")
    print(md)


if __name__ == "__main__":
    main()
