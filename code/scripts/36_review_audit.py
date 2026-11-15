#!/usr/bin/env python3
"""Offline audits requested by the ICDE pre-reviews (issue #3). Zero model calls: everything is
recomputed from the stored per-instance results (results/closed/raw/<ds>/<model>/main/*.jsonl).

Cells: HotpotQA, MuSiQue, Qasper (test split = pilot qids removed) and Symmetric FEVER
(evidence-dependent set). Per cell, on the common valid set of V1, P1, LOI and RM64 (rows for all
four, valid reference a0):

  align     V1's own answer vs the interventional reference a0 (Previum 1, Explore B8): agreement,
            V1-answer correctness, top-1 of V1/P1/LOI/RM64 on agreeing and disagreeing rows,
            paired CI of (RM64 - V1) and (P1 - V1) on agreeing rows.
  rm_empty  sources never kept / never dropped in the first k masks (Explore B11): share of
            instances affected per k, top-1 with zero fill (current) vs excluding those rows.
  mask_var  mask-sampling uncertainty (Previum 2): RM@32 on masks 1-32 vs 33-64 (independent
            draws), and a two-level bootstrap (instances x masks within instance) for RM64 - V1.
  routing   LOI/P1 -> RM@32/RM64 (Explore A2, C3, C9, C11, B17): escalation split into all-zero
            vs tied, top-1 before/after, nominal cost with and without cross-stage reuse of
            single-source masks, paired CI of routed - RM.
  failures  parse failures per estimator (Explore B3): V1 parse failures / empty source lists,
            P1 / LOI / RM draws without a usable answer.
  refstab   reference stability (Explore B5): rows by number of the 3 unablated re-asks that
            differ from a0; top-1 per stratum.
  excess    non-gold ablation change rate minus unablated re-ask change rate (Explore C2, D1).
  position  position-only baselines (Explore B14).
  tost      equivalence of RM64 and V1 at margins 0.03 / 0.05 (Explore C4, B12).
  surrogate ContextCite-style linear surrogate (ridge on the same 64 masks) vs Banzhaf (Explore C8).
  f1equiv   answer-change test with token F1 >= 0.5 as equivalence (Explore B16 / C5, lexical).
  active    pool-based adaptive mask selection (CMU 1): Thompson-style choice of the next mask
            among the 64 observed ones, at k = 8 / 16 / 32, vs the random prefix.

  python scripts/36_review_audit.py            # -> results/closed/analysis/review_audit.{json,md}
"""
from __future__ import annotations

import gzip
import importlib.util
import json
import os
import random
import sys
from collections import Counter

import numpy as np

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)


def _load(name, rel):
    s = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


t28 = _load("t28", "scripts/28_paper_tables.py")
a18 = t28.a18
from src.data.schema import Instance, read_jsonl  # noqa: E402
from src.pipelines.subset import SCALARIZERS, banzhaf, ridge, token_f1  # noqa: E402
from src.utils.parsing import normalize_answer  # noqa: E402

RAW, OUT = a18.RAW, a18.OUT
MODELS = ["claude-haiku-5-5", "gpt-6-luna", "gemini-2.5-flash-lite", "gemini-2.5-flash", "gpt-6.1-terra"]
DATASETS = ["hotpotqa", "musique", "qasper", "symfever"]
B = 2000
top1 = a18.tie_top1


def instances(ds):
    if ds in ("hotpotqa", "musique"):
        return {i.qid: i for i in read_jsonl(os.path.join(ROOT, "data", "processed", f"{ds}_validation.jsonl"))}
    with gzip.open(os.path.join(ROOT, "data", "constructed", ds, f"{ds}.all.jsonl.gz"), "rt", encoding="utf-8") as fh:
        return {i.qid: i for i in (Instance.from_json(json.loads(l)) for l in fh if l.strip())}


def answer_ok(pred, inst):
    """Same rule as screening (14_screen_closed.matches); FEVER: normalised label identity."""
    if pred is None:
        return False
    if inst.dataset == "symfever":
        return normalize_answer(pred) == normalize_answer(inst.answer)
    return bool(_load_screen().matches(pred, inst))


_S14 = None


def _load_screen():
    global _S14
    if _S14 is None:
        _S14 = _load("s14", "scripts/14_screen_closed.py")
    return _S14


def boot(d, clusters=None, seed=0):
    """Bootstrap distribution of mean(d) (instances or whole clusters)."""
    d = np.asarray(d, float)
    rng = np.random.default_rng(seed)
    if clusters is None:
        return d[rng.integers(0, len(d), size=(B, len(d)))].mean(1)
    ids = sorted(set(clusters))
    idx = {c: np.flatnonzero(np.asarray(clusters) == c) for c in ids}
    sums = np.array([d[idx[c]].sum() for c in ids]); cnts = np.array([len(idx[c]) for c in ids])
    pick = rng.integers(0, len(ids), size=(B, len(ids)))
    return sums[pick].sum(1) / cnts[pick].sum(1)


def ci(d, clusters=None, lo=0.025, hi=0.975):
    if len(d) == 0:
        return [np.nan, np.nan, np.nan]
    bs = boot(d, clusters)
    return [float(np.mean(d)), float(np.quantile(bs, lo)), float(np.quantile(bs, hi))]


def unique_max(phi):
    p = np.asarray(phi, float)
    return bool(p.any()) and int(np.sum(np.isclose(p, p.max()))) == 1


def load(ds, model):
    d = os.path.join(RAW, ds, model, "main")
    if not os.path.isdir(d):
        return None
    keep, split = None, "test"
    if ds == "symfever":
        ev = json.load(open(os.path.join(ROOT, "results", "closed", "screen", "symfever", model,
                                         "symfever.all.evaluable.json")))
        keep, split = set(ev["evidence_dep"]), "all"
    _, _, R = t28.load_cell(d, split, keep)
    by = {k: {r["qid"]: r for r in v} for k, v in R.items()}
    if not all(m in by for m in ("V1", "P1", "LOI")):
        return None
    need = [m for m in ("V1", "P1", "LOI", "RM64") if m in by]
    common = set.intersection(*(set(by[m]) for m in need))
    common -= {q for m in need if t28.needs_ref(m) for q, r in by[m].items() if t28.invalid(r)}
    return by, sorted(common)


# ----------------------------------------------------------------------------- audits

def audit_align(ds, model, by, common, insts, cl):
    rows = []
    for q in common:
        v, p = by["V1"][q], by["P1"][q]
        av = (v["meta"].get("answers") or [None])[0]
        a0 = p.get("baseline_answer")
        rows.append({"q": q, "agree": av is not None and normalize_answer(av) == normalize_answer(a0),
                     "v_ok": answer_ok(av, insts[q]), "a0_ok": answer_ok(a0, insts[q])})
    ag = [r["q"] for r in rows if r["agree"]]
    dis = [r["q"] for r in rows if not r["agree"]]
    out = {"n": len(common), "agree": len(ag) / len(common), "n_disagree": len(dis),
           "V1_answer_correct": float(np.mean([r["v_ok"] for r in rows])),
           "a0_correct": float(np.mean([r["a0_ok"] for r in rows])),
           "disagree_V1_correct": float(np.mean([r["v_ok"] for r in rows if not r["agree"]])) if dis else np.nan,
           "disagree_a0_correct": float(np.mean([r["a0_ok"] for r in rows if not r["agree"]])) if dis else np.nan}
    for m in ("V1", "P1", "LOI", "RM64"):
        if m in by:
            out[f"{m}_agree"] = float(np.mean([top1(by[m][q]["phi"], by[m][q]["gold"]) for q in ag]))
            out[f"{m}_disagree"] = float(np.mean([top1(by[m][q]["phi"], by[m][q]["gold"]) for q in dis])) if dis else np.nan
    for m in ("P1", "RM64"):
        if m in by:
            d = [top1(by[m][q]["phi"], by[m][q]["gold"]) - top1(by["V1"][q]["phi"], by["V1"][q]["gold"]) for q in ag]
            out[f"{m}-V1_agree"] = ci(d, [cl[q] for q in ag] if cl else None)
            d = [top1(by[m][q]["phi"], by[m][q]["gold"]) - top1(by["V1"][q]["phi"], by["V1"][q]["gold"]) for q in common]
            out[f"{m}-V1_all"] = ci(d, [cl[q] for q in common] if cl else None)
    # alignment on V1's correct-answer rows (both answers correct, or V1 correct)
    ok = [r["q"] for r in rows if r["v_ok"]]
    out["V1_on_V1correct"] = float(np.mean([top1(by["V1"][q]["phi"], by["V1"][q]["gold"]) for q in ok])) if ok else np.nan
    return out


def rm_y(r, scal="exact"):
    a0 = r.get("baseline_answer")
    return np.array([SCALARIZERS[scal](a, a0) for a in r["meta"]["mask_answers"]], float)


def audit_rm_empty(by, common):
    if "RM64" not in by:
        return None
    out = {}
    for k in (8, 10, 16, 20, 32, 64):
        aff, t_zero, t_excl, n_src = [], [], [], 0
        for q in common:
            r = by["RM64"][q]
            M = len(r["phi"])
            if k in (10, 20) and k != M:
                continue
            masks = np.array(r["meta"]["masks"], bool)[:k]
            empty = (~masks.any(0)) | masks.all(0)
            n_src += int(empty.sum())
            phi = banzhaf(masks, rm_y(r)[:k])
            h = top1(phi, r["gold"])
            aff.append(bool(empty.any())); t_zero.append(h)
            if not empty.any():
                t_excl.append(h)
        if aff:
            out[f"k{k}"] = {"share_inst": float(np.mean(aff)), "src_per_inst": n_src / len(aff),
                            "top1_zero_fill": float(np.mean(t_zero)), "top1_excluding": float(np.mean(t_excl)) if t_excl else np.nan,
                            "n": len(aff)}
    return out


def audit_mask_var(by, common, cl, seed=0):
    if "RM64" not in by:
        return None
    rng = np.random.default_rng(seed)
    a, b, v1 = [], [], []
    for q in common:
        r = by["RM64"][q]
        masks = np.array(r["meta"]["masks"], bool); y = rm_y(r)
        a.append(top1(banzhaf(masks[:32], y[:32]), r["gold"]))
        b.append(top1(banzhaf(masks[32:64], y[32:64]), r["gold"]))
        v1.append(top1(by["V1"][q]["phi"], by["V1"][q]["gold"]))
    a, b, v1 = map(np.array, (a, b, v1))
    out = {"rm32_first": float(a.mean()), "rm32_second": float(b.mean()),
           "halves_diff": ci(a - b, [cl[q] for q in common] if cl else None),
           "halves_hit_agreement": float(np.mean(a == b))}
    # two-level bootstrap: resample instances (or clusters), then the 64 (mask, answer) pairs
    # within each sampled instance; RM64 - V1 and RM64 alone
    R = [by["RM64"][q] for q in common]
    M_ = [np.array(r["meta"]["masks"], bool) for r in R]
    Y_ = [rm_y(r) for r in R]
    G_ = [r["gold"] for r in R]
    n = len(R); nb = 400
    groups = None
    if cl:
        ids = sorted({cl[q] for q in common}); pos = {c: [i for i, q in enumerate(common) if cl[q] == c] for c in ids}
    est_rm, est_d, est_rm_inst_only = [], [], []
    for _ in range(nb):
        if cl:
            pick = [i for c in rng.integers(0, len(ids), len(ids)) for i in pos[ids[c]]]
        else:
            pick = rng.integers(0, n, n)
        h = []
        for i in pick:
            j = rng.integers(0, len(Y_[i]), len(Y_[i]))
            h.append(top1(banzhaf(M_[i][j], Y_[i][j]), G_[i]))
        h = np.array(h)
        est_rm.append(h.mean()); est_d.append((h - v1[pick]).mean())
    base = np.array([top1(r["phi"], r["gold"]) for r in R])
    out["rm64"] = float(base.mean())
    # resampling masks with replacement leaves ~63% distinct masks, which lowers the mean (a smaller
    # effective k); use the two-level bootstrap for the SPREAD only, centred on the observed value
    sd_rm, sd_d = float(np.std(est_rm)), float(np.std(est_d))
    out["rm64_ci_two_level"] = [float(base.mean() - 1.96 * sd_rm), float(base.mean() + 1.96 * sd_rm)]
    out["rm64-V1"] = float((base - v1).mean())
    inst = boot(base - v1, [cl[q] for q in common] if cl else None)
    out["rm64-V1_ci_instances"] = [float(out["rm64-V1"] - 1.96 * np.std(inst)), float(out["rm64-V1"] + 1.96 * np.std(inst))]
    out["rm64-V1_ci_two_level"] = [float(out["rm64-V1"] - 1.96 * sd_d), float(out["rm64-V1"] + 1.96 * sd_d)]
    out["sd_ratio_two_level_vs_instances"] = sd_d / float(np.std(inst)) if np.std(inst) else np.nan
    # within-instance mask-only spread: expected |top-1 change| under a fresh mask set
    return out


def single_mask_overlap(r_rm, k, loi_keys):
    """number of distinct non-full masks among the first k that keep exactly one source (identical to
    a LOI prompt) or drop exactly one source (identical to a P1 prompt at the same draw index 0)."""
    seen, one, loo = set(), 0, 0
    for m in r_rm["meta"]["masks"][:k]:
        t = tuple(m)
        if all(t) or t in seen:
            continue
        seen.add(t)
        s = sum(t)
        one += s == 1
        loo += s == len(t) - 1
    return one, loo


def audit_routing(ds, by, common, cl):
    out = []
    rmb = by.get("RM64", {})
    for cheap in ("LOI", "P1"):
        for rm in ("RM@32", "RM64"):
            if rm not in by or cheap not in by:
                continue
            acc_r, acc_rm, cost_r, cost_r_dedup, cost_rm, grp = [], [], [], [], [], []
            for q in common:
                c, e = by[cheap][q], by[rm][q]
                p = np.asarray(c["phi"], float)
                kind = "unique" if unique_max(p) else ("all_zero" if not p.any() else "tie")
                go = kind != "unique"
                k = 32 if rm == "RM@32" else 64
                c_cheap = t28.nominal_calls(cheap, c)
                c_rm = t28.nominal_calls(rm, e, rmb.get(q))
                one, loo = single_mask_overlap(rmb[q], k, None)
                reuse = one if cheap == "LOI" else 0  # P1 draws are at N=3 sample indices; count none
                acc_r.append(top1((e if go else c)["phi"], c["gold"]))
                acc_rm.append(top1(e["phi"], e["gold"]))
                cost_r.append(c_cheap + ((c_rm - 1) if go else 0))
                cost_r_dedup.append(c_cheap + ((c_rm - 1 - reuse) if go else 0))
                cost_rm.append(c_rm)
                grp.append((kind, top1(c["phi"], c["gold"]), top1(e["phi"], e["gold"])))
            d = np.array(acc_r) - np.array(acc_rm)
            row = {"route": f"{cheap}->{rm}", "n": len(common), "escalated": float(np.mean([g[0] != "unique" for g in grp])),
                   "top1_routed": float(np.mean(acc_r)), "top1_rm": float(np.mean(acc_rm)),
                   "diff": ci(d, [cl[q] for q in common] if cl else None),
                   "cost_routed": float(np.mean(cost_r)), "cost_routed_reuse": float(np.mean(cost_r_dedup)),
                   "cost_rm": float(np.mean(cost_rm)), "saving": 1 - float(np.mean(cost_r)) / float(np.mean(cost_rm))}
            for kind in ("unique", "all_zero", "tie"):
                g = [x for x in grp if x[0] == kind]
                row[f"{kind}_share"] = len(g) / len(grp)
                row[f"{kind}_cheap_top1"] = float(np.mean([x[1] for x in g])) if g else np.nan
                row[f"{kind}_rm_top1"] = float(np.mean([x[2] for x in g])) if g else np.nan
            out.append(row)
    return out


def audit_failures(by, common):
    out = {}
    v = [by["V1"][q] for q in common]
    out["V1_parse_fail"] = float(np.mean([r.get("parse_failures", 0) > 0 for r in v]))
    out["V1_no_source"] = float(np.mean([not np.asarray(r["phi"]).any() for r in v]))
    for m, key in (("P1", "ablated_answers"), ("LOI", "single_answers"), ("RM64", "mask_answers")):
        if m not in by:
            continue
        tot = bad = inst_bad = 0
        for q in common:
            a = by[m][q]["meta"].get(key)
            if a is None:
                continue
            vals = [x for xs in a.values() for x in xs] if isinstance(a, dict) else list(a)
            nb = sum(x is None for x in vals)
            tot += len(vals); bad += nb; inst_bad += nb > 0
        out[f"{m}_draw_fail"] = bad / tot if tot else np.nan
        out[f"{m}_inst_with_fail"] = inst_bad / len(common)
    if "RM64" in by:
        h0, h1 = [], []
        for q in common:
            e = by["RM64"][q]
            masks = np.array(e["meta"]["masks"], bool); ans = e["meta"]["mask_answers"]
            ok = np.array([x is not None for x in ans])
            h0.append(top1(e["phi"], e["gold"]))
            h1.append(top1(banzhaf(masks[ok], rm_y(e)[ok]), e["gold"]) if ok.sum() > 1 else top1(e["phi"], e["gold"]))
        out["RM64_top1_fail_as_change"] = float(np.mean(h0))
        out["RM64_top1_fail_as_missing"] = float(np.mean(h1))
    # unique-max cheap vectors that involved a failed draw (Explore B13)
    nb = 0
    for q in common:
        r = by["LOI"][q]
        if unique_max(r["phi"]) and any(x is None for x in r["meta"].get("single_answers") or []):
            nb += 1
    out["LOI_unique_with_fail"] = nb / len(common)
    return out


def audit_refstab(by, common):
    out = {}
    strata = {}
    for q in common:
        cr = by["P1"][q]["meta"].get("full_context_change_rate")
        nrep = by["P1"][q]["meta"].get("n_full_repeats") or 3
        if cr is None:
            continue
        s = int(round(cr * nrep))
        strata.setdefault(min(s, 2), []).append(q)
    for s, qs in sorted(strata.items()):
        e = {"share": len(qs) / len(common)}
        for m in ("V1", "P1", "LOI", "RM64"):
            if m in by:
                e[m] = float(np.mean([top1(by[m][q]["phi"], by[m][q]["gold"]) for q in qs]))
        out[{0: "0of3", 1: "1of3", 2: "2+of3"}[s]] = e
    return out


def audit_excess(by, common, cl):
    d, ng, sp, qs = [], [], [], []
    for q in common:
        r = by["P1"][q]
        a0 = normalize_answer(r.get("baseline_answer"))
        abl = r["meta"].get("ablated_answers") or {}
        cr = r["meta"].get("full_context_change_rate")
        if cr is None:
            continue
        flips = [normalize_answer(x) != a0 for i, xs in abl.items() if int(i) not in set(r["gold"]) for x in xs if x is not None]
        if not flips:
            continue
        d.append(float(np.mean(flips) - cr)); ng.append(np.mean(flips)); sp.append(cr); qs.append(q)
    return {"nongold_flip": float(np.mean(ng)), "reask_change": float(np.mean(sp)),
            "excess": ci(d, [cl[q] for q in qs] if cl else None)}


def audit_position(by, common):
    pos = Counter()
    M = None
    for q in common:
        r = by["V1"][q]
        M = len(r["phi"])
        for g in r["gold"]:
            pos[g] += 1
    out = {"gold_pos_hist": [pos[i] for i in range(M)]}
    for name, f in (("first", lambda M: 0), ("last", lambda M: M - 1)):
        out[name] = float(np.mean([float(f(len(by["V1"][q]["phi"])) in by["V1"][q]["gold"]) for q in common]))
    mode = pos.most_common(1)[0][0]
    out["modal_pos"] = int(mode)
    out["modal"] = float(np.mean([float(mode in by["V1"][q]["gold"]) for q in common]))
    out["chance"] = float(np.mean([len(by["V1"][q]["gold"]) / len(by["V1"][q]["phi"]) for q in common]))
    v1top = Counter(int(np.argmax(by["V1"][q]["phi"])) for q in common if np.asarray(by["V1"][q]["phi"]).any())
    out["V1_top_pos_hist"] = [v1top[i] for i in range(M)]
    return out


def audit_tost(by, common, cl):
    if "RM64" not in by:
        return None
    d = [top1(by["RM64"][q]["phi"], by["RM64"][q]["gold"]) - top1(by["V1"][q]["phi"], by["V1"][q]["gold"]) for q in common]
    bs = boot(d, [cl[q] for q in common] if cl else None)
    lo, hi = float(np.quantile(bs, .05)), float(np.quantile(bs, .95))
    return {"diff": float(np.mean(d)), "ci90": [lo, hi], "equiv_0.03": bool(lo > -.03 and hi < .03),
            "equiv_0.05": bool(lo > -.05 and hi < .05), "noninf_0.05": bool(lo > -.05), "noninf_0.03": bool(lo > -.03)}


def audit_surrogate(by, common):
    if "RM64" not in by:
        return None
    lin = [top1(by["RM64"][q]["meta"]["scores"]["linear_exact"], by["RM64"][q]["gold"]) for q in common]
    bz = [top1(by["RM64"][q]["phi"], by["RM64"][q]["gold"]) for q in common]
    l32 = []
    for q in common:
        r = by["RM64"][q]
        l32.append(top1(ridge(np.array(r["meta"]["masks"], bool)[:32], rm_y(r)[:32]), r["gold"]))
    return {"banzhaf64": float(np.mean(bz)), "linear64": float(np.mean(lin)), "linear32": float(np.mean(l32))}


def audit_f1equiv(by, common, thr=0.5):
    """Answer change := token F1 < thr (instead of normalised string inequality)."""
    out = {}
    p1, loi, rm, eqshare = [], [], [], []
    for q in common:
        r = by["P1"][q]
        a0 = r.get("baseline_answer"); M = len(r["phi"])
        abl = r["meta"].get("ablated_answers") or {}
        phi = np.zeros(M)
        for i, xs in abl.items():
            xs = [x for x in xs if x is not None]
            if xs:
                phi[int(i)] = np.mean([token_f1(x, a0) < thr for x in xs])
                ch = [x for x in xs if normalize_answer(x) != normalize_answer(a0)]
                eqshare += [token_f1(x, a0) >= thr for x in ch]
        p1.append(top1(phi, r["gold"]))
        L = by["LOI"][q]
        phl = np.array([float(x is not None and token_f1(x, a0) >= thr) for x in L["meta"]["single_answers"]])
        loi.append(top1(phl, L["gold"]))
        if "RM64" in by:
            e = by["RM64"][q]
            y = np.array([float(x is not None and token_f1(x, a0) >= thr) for x in e["meta"]["mask_answers"]])
            rm.append(top1(banzhaf(np.array(e["meta"]["masks"], bool), y), e["gold"]))
    out = {"P1_f1": float(np.mean(p1)), "LOI_f1": float(np.mean(loi)),
           "changes_judged_equiv": float(np.mean(eqshare)) if eqshare else np.nan}
    if rm:
        out["RM64_f1"] = float(np.mean(rm))
    return out


def active_select(masks, y, k, rng):
    """Thompson-style pool-based selection: sample theta_i ~ N(w_i, 1/sqrt(n_i)) from the current
    Banzhaf estimate, propose 'keep the top half', query the unused pool mask nearest to it."""
    K, M = masks.shape
    used = [0]  # start from the first random mask (shared with the prefix design)
    while len(used) < k:
        idx = np.array(used)
        w = banzhaf(masks[idx], y[idx])
        cnt = np.minimum(masks[idx].sum(0), (~masks[idx]).sum(0)) + 1e-6
        th = rng.normal(w, 1 / np.sqrt(cnt))
        prop = th >= np.sort(th)[M // 2]
        rest = [j for j in range(K) if j not in set(used)]
        dist = [(np.sum(masks[j] != prop), rng.random(), j) for j in rest]
        used.append(min(dist)[2])
    idx = np.array(used)
    return banzhaf(masks[idx], y[idx])


def audit_active(by, common, cl, seed=0):
    if "RM64" not in by:
        return None
    rng = np.random.default_rng(seed)
    out = {}
    for k in (8, 16, 32):
        a, r_ = [], []
        for q in common:
            e = by["RM64"][q]
            masks = np.array(e["meta"]["masks"], bool); y = rm_y(e)
            a.append(top1(active_select(masks, y, k, rng), e["gold"]))
            r_.append(top1(banzhaf(masks[:k], y[:k]), e["gold"]))
        out[f"k{k}"] = {"random": float(np.mean(r_)), "active": float(np.mean(a)),
                        "diff": ci(np.array(a) - np.array(r_), [cl[q] for q in common] if cl else None)}
    return out


def main():
    res = []
    only = os.environ.get("AUDIT_ONLY")  # e.g. "hotpotqa:claude-haiku-5-5" for a quick check
    for ds in DATASETS:
        if only and ds != only.split(":")[0]:
            continue
        insts = instances(ds)
        cl = t28.cluster_of(ds)
        for model in MODELS:
            if only and ":" in only and model != only.split(":")[1]:
                continue
            L = load(ds, model)
            if L is None:
                continue
            by, common = L
            print(ds, model, len(common), flush=True)
            res.append({"dataset": ds, "model": model, "n": len(common),
                        "align": audit_align(ds, model, by, common, insts, cl),
                        "rm_empty": audit_rm_empty(by, common),
                        "mask_var": audit_mask_var(by, common, cl),
                        "routing": audit_routing(ds, by, common, cl),
                        "failures": audit_failures(by, common),
                        "refstab": audit_refstab(by, common),
                        "excess": audit_excess(by, common, cl),
                        "position": audit_position(by, common),
                        "tost": audit_tost(by, common, cl),
                        "surrogate": audit_surrogate(by, common),
                        "f1equiv": audit_f1equiv(by, common),
                        "active": audit_active(by, common, cl)})
    json.dump(res, open(os.path.join(OUT, "review_audit.json"), "w"), indent=1, default=float)
    write_md(res)


def f3(x):
    if isinstance(x, (list, tuple)):
        return "[" + ", ".join(f3(v) for v in x) + "]"
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, float):
        return "–" if x != x else f"{x:.3f}"
    return str(x)


def write_md(res):
    L = ["# Offline audits for the ICDE pre-reviews (issue #3)", "",
         "Generated by `scripts/36_review_audit.py` from stored per-instance results, zero model calls. "
         "Each cell: common valid set of V1, P1, LOI, RM64 (QA: test split; FEVER: evidence-dependent). "
         "CIs: paired bootstrap, 2,000 resamples (FEVER: claim families, Qasper: papers).", ""]

    def table(title, cols, get):
        L.extend([f"## {title}", "", "| dataset | model | " + " | ".join(cols) + " |",
                  "|---|---|" + "---|" * len(cols)])
        for r in res:
            v = get(r)
            if v is None:
                continue
            for row in (v if isinstance(v, list) else [v]):
                L.append(f"| {r['dataset']} | {r['model']} | " + " | ".join(f3(row.get(c)) for c in cols) + " |")
        L.append("")

    table("1. Answer alignment: V1's answer vs reference a0", ["n", "agree", "V1_answer_correct", "a0_correct",
          "V1_agree", "P1_agree", "LOI_agree", "RM64_agree", "V1_disagree", "P1_disagree", "RM64_disagree",
          "P1-V1_agree", "RM64-V1_agree"], lambda r: r["align"])
    table("2. RM empty groups (source never kept or never dropped among first k masks)",
          ["k", "share_inst", "src_per_inst", "top1_zero_fill", "top1_excluding"],
          lambda r: [{"k": k[1:], **v} for k, v in (r["rm_empty"] or {}).items()] or None)
    table("3. Mask-sampling uncertainty", ["rm32_first", "rm32_second", "halves_diff", "halves_hit_agreement",
          "rm64", "rm64_ci_two_level", "rm64-V1", "rm64-V1_ci_instances", "rm64-V1_ci_two_level", "sd_ratio_two_level_vs_instances"], lambda r: r["mask_var"])
    table("4. Routing (escalate when the cheap probe has no unique maximum)", ["route", "escalated", "all_zero_share",
          "tie_share", "top1_routed", "top1_rm", "diff", "cost_routed", "cost_routed_reuse", "cost_rm", "saving",
          "all_zero_cheap_top1", "all_zero_rm_top1", "tie_cheap_top1", "tie_rm_top1", "unique_cheap_top1",
          "unique_rm_top1"], lambda r: r["routing"])
    table("5. Draw failures", ["V1_parse_fail", "V1_no_source", "P1_draw_fail", "P1_inst_with_fail", "LOI_draw_fail",
          "LOI_inst_with_fail", "RM64_draw_fail", "RM64_inst_with_fail", "RM64_top1_fail_as_change", "RM64_top1_fail_as_missing", "LOI_unique_with_fail"], lambda r: r["failures"])
    table("6. Reference stability (unablated re-asks differing from a0)", ["stratum", "share", "V1", "P1", "LOI", "RM64"],
          lambda r: [{"stratum": k, **v} for k, v in r["refstab"].items()])
    table("7. Non-gold ablation change minus re-ask change (P1 draws)", ["nongold_flip", "reask_change", "excess"],
          lambda r: r["excess"])
    table("8. Position-only baselines", ["chance", "first", "last", "modal_pos", "modal", "gold_pos_hist", "V1_top_pos_hist"],
          lambda r: r["position"])
    table("9. Equivalence RM64 vs V1 (90% CI, TOST)", ["diff", "ci90", "equiv_0.03", "equiv_0.05", "noninf_0.03",
          "noninf_0.05"], lambda r: r["tost"])
    table("10. Linear surrogate vs Banzhaf (same masks)", ["banzhaf64", "linear64", "linear32"], lambda r: r["surrogate"])
    table("11. Token-F1 >= 0.5 as answer equivalence", ["P1_f1", "LOI_f1", "RM64_f1", "changes_judged_equiv"],
          lambda r: r["f1equiv"])
    table("12. Pool-based adaptive mask selection vs random prefix", ["k", "random", "active", "diff"],
          lambda r: [{"k": k[1:], **v} for k, v in (r["active"] or {}).items()] or None)
    open(os.path.join(OUT, "review_audit.md"), "w").write("\n".join(L))
    print("wrote", os.path.join(OUT, "review_audit.{json,md}"))


if __name__ == "__main__":
    main()
