#!/usr/bin/env python3
"""Analyse the issue-#3 follow-up probes (38_build_review_probes.py, run_review_probes.sh). Zero calls.

  swap        evidence moved to another slot, a same-page sentence in the slot it left: does V1 cite the
              new slot (follows), the old slot (sticks), both?
  conflict    both evidence sentences of a claim present: the verdict reveals the controlling one.
              V1 cites controlling / other / both / neither; P1 and LOI give the causal check.
  unscreened  leaked and wrongly answered QA candidates: LOI unique-max share and how often a unique
              maximum is gold, next to the evaluable-set value (routing trigger outside screening).

  python scripts/39_analyze_probes.py [--suffix _trial]  -> results/closed/analysis/review_probes{suffix}.{json,md}
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import sys

import numpy as np

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
from src.utils.parsing import normalize_answer  # noqa: E402

RAW = os.path.join(ROOT, "results", "closed", "raw")
OUT = os.path.join(ROOT, "results", "closed", "analysis")
D = os.path.join(ROOT, "data", "constructed", "review_probes")
MAIN = ["claude-haiku-5-5", "gpt-6-luna", "gemini-2.5-flash-lite"]


def rows(ds, m, tag, meth):
    p = os.path.join(RAW, ds, m, tag, f"{meth}.jsonl")
    return {json.loads(l)["qid"]: json.loads(l) for l in open(p)} if os.path.exists(p) else {}


def inst(path):
    return {json.loads(l)["qid"]: json.loads(l) for l in gzip.open(path, "rt")}


def top_set(phi):
    p = np.asarray(phi, float)
    return set(np.flatnonzero(np.isclose(p, p.max()))) if p.any() else set()


def ci(x, seed=0, B=2000):
    x = np.asarray(x, float)
    if len(x) == 0:
        return [np.nan] * 3
    bs = x[np.random.default_rng(seed).integers(0, len(x), (B, len(x)))].mean(1)
    return [float(x.mean()), float(np.quantile(bs, .025)), float(np.quantile(bs, .975))]


def swap(m, suf):
    I = inst(os.path.join(D, f"symfever.{m}.swap.jsonl.gz"))
    V = rows("symfever", m, "probe_swap" + suf, "V1")
    base = rows("symfever", m, "main", "V1")
    fol, sti, hit, hit0 = [], [], [], []
    for q, r in V.items():
        mt = I[q]["meta"]
        T = top_set(r["phi"])
        fol.append(mt["new_slot"] in T); sti.append(mt["orig_slot"] in T)
        hit.append(len(T & {mt["new_slot"]}) / len(T) if T else 0.1)
        b = base.get(mt["base_qid"])
        if b:
            T0 = top_set(b["phi"]); hit0.append(len(T0 & {mt["orig_slot"]}) / len(T0) if T0 else 0.1)
    return {"n": len(V), "top1_swapped": ci(hit), "top1_original": float(np.mean(hit0)) if hit0 else np.nan,
            "cites_new_slot": float(np.mean(fol)), "cites_old_slot": float(np.mean(sti))}


def conflict(m, suf):
    I = inst(os.path.join(D, f"symfever.{m}.conflict.jsonl.gz"))
    V, P, L = (rows("symfever", m, "probe_conflict" + suf, k) for k in ("V1", "P1", "LOI"))
    out = {"n": len(V)}
    cls, v_ctrl, v_other, v_both, v_none, p_u, p_ctrl, l_ctrl, agree = ([] for _ in range(9))
    follow_first = []
    for q, v in V.items():
        mt = I[q]["meta"]
        p = P.get(q)
        if p is None or p.get("baseline_answer") is None:
            continue
        a0 = normalize_answer(p["baseline_answer"])
        if a0 == normalize_answer(mt["label_first"]):
            c, o = mt["slot_first"], mt["slot_second"]
        elif a0 == normalize_answer(mt["label_second"]):
            c, o = mt["slot_second"], mt["slot_first"]
        else:
            cls.append("unknown"); continue
        cls.append("first" if c == mt["slot_first"] else "second")
        T = top_set(v["phi"])
        v_ctrl.append(c in T and o not in T); v_other.append(o in T and c not in T)
        v_both.append(c in T and o in T); v_none.append(c not in T and o not in T)
        Tp = top_set(p["phi"])
        p_u.append(len(Tp) == 1); p_ctrl.append(Tp == {c})
        l = L.get(q)
        if l is not None:
            l_ctrl.append(top_set(l["phi"]) == {c})
        if len(Tp) == 1:
            agree.append(c in T and o not in T if Tp == {c} else (next(iter(Tp)) in T))
    n = len(cls)
    out.update({"verdict_first": cls.count("first") / n if n else np.nan,
                "verdict_second": cls.count("second") / n if n else np.nan,
                "verdict_unknown": cls.count("unknown") / n if n else np.nan,
                "n_decided": len(v_ctrl),
                "V1_controlling_only": ci(v_ctrl), "V1_other_only": float(np.mean(v_other)) if v_other else np.nan,
                "V1_both": float(np.mean(v_both)) if v_both else np.nan, "V1_neither": float(np.mean(v_none)) if v_none else np.nan,
                "P1_unique": float(np.mean(p_u)) if p_u else np.nan,
                "P1_unique_is_controlling": float(np.mean(p_ctrl)) if p_ctrl else np.nan,
                "LOI_unique_is_controlling": float(np.mean(l_ctrl)) if l_ctrl else np.nan,
                "V1_agrees_P1_unique": float(np.mean(agree)) if agree else np.nan})
    return out


def unscreened(ds, m, suf):
    I = inst(os.path.join(D, f"{ds}.{m}.unscreened.jsonl.gz"))
    V, L = rows(ds, m, "probe_unscreened" + suf, "V1"), rows(ds, m, "probe_unscreened" + suf, "LOI")
    main = rows(ds, m, "main", "LOI")
    res = {}
    for b in ("leaked", "wrong"):
        qs = [q for q in L if I[q]["meta"]["screen_bucket"] == b and L[q].get("baseline_answer") is not None]
        uq = [q for q in qs if len(top_set(L[q]["phi"])) == 1]
        g = [next(iter(top_set(L[q]["phi"]))) in set(L[q]["gold"]) for q in uq]
        vt = [len(top_set(V[q]["phi"]) & set(V[q]["gold"])) / max(len(top_set(V[q]["phi"])), 1)
              if top_set(V[q]["phi"]) else len(V[q]["gold"]) / len(V[q]["phi"]) for q in qs if q in V]
        res[b] = {"n": len(qs), "LOI_unique": len(uq) / len(qs) if qs else np.nan,
                  "unique_is_gold": ci(g), "V1_top1": float(np.mean(vt)) if vt else np.nan}
    uqm = [q for q, r in main.items() if r.get("baseline_answer") is not None and len(top_set(r["phi"])) == 1]
    res["evaluable"] = {"n": len(main), "LOI_unique": len(uqm) / max(len(main), 1),
                        "unique_is_gold": float(np.mean([next(iter(top_set(main[q]["phi"]))) in set(main[q]["gold"]) for q in uqm]))}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suffix", default="")
    a = ap.parse_args()
    R = {"swap": {}, "conflict": {}, "unscreened": {}}
    for m in MAIN:
        R["swap"][m] = swap(m, a.suffix)
        R["conflict"][m] = conflict(m, a.suffix)
        for ds in ("hotpotqa", "musique"):
            R["unscreened"][f"{ds}/{m}"] = unscreened(ds, m, a.suffix)
    json.dump(R, open(os.path.join(OUT, f"review_probes{a.suffix}.json"), "w"), indent=1, default=float)
    print(json.dumps(R, indent=1, default=lambda x: round(float(x), 3)))


if __name__ == "__main__":
    main()
