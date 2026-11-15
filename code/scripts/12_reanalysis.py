#!/usr/bin/env python3
"""Phase-0 re-analysis of the AAAI-27 per-instance results (no model calls).

Fixes the evaluation issues found in the ICDE revision audit
(docs/审稿意见逐条应对表.md, section E):

  E1  "empty prediction" was "no score >= tau", not "all-zero score vector".
      We split it into explicit signal fields.
  E2  Spearman was computed on rankings whose ties were broken by source index.
      We report tie-preserving Spearman on the raw scores.
  E5  top-1 broke ties by index. We also report the expected top-1 when the
      winner is drawn uniformly from the highest-score tie group.

and adds zero-cost diagnostics:
  - output-conditioned answer-string baseline (a weak corroborative attributor;
    uses the target model's answer, needs no attribution query)
  - recall of gold passages with / without the answer string (at tau and
    tie-aware recall@k)
  - hop analysis relative to the random floor, with a logistic-regression
    effect size controlling for chance (MuSiQue)
  - non-gold deletion sensitivity (exploratory, E3): per-draw change rate and
    "changed in at least one draw" share, reported separately because N differs

Usage:
  python scripts/12_reanalysis.py            # writes results/reanalysis/
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import unicodedata
from collections import defaultdict

import numpy as np
from scipy.stats import binomtest, spearmanr

ROOT = os.path.join(os.path.dirname(__file__), "..")
RAW = os.path.join(ROOT, "results", "raw")
DATA = os.path.join(ROOT, "data", "processed")
OUT = os.path.join(ROOT, "results", "reanalysis")

DATASETS = ["hotpotqa", "musique"]
MODELS = ["qwen3-1.7b", "qwen3-4b", "qwen3-8b", "gemma3-1b", "gemma3-4b", "gemma3-12b"]
FAMILY = {m: ("qwen3" if m.startswith("qwen") else "gemma3") for m in MODELS}
V_METHODS = [f"V{i}" for i in range(1, 8)]
P_METHODS = [f"P{i}" for i in range(1, 6)]
TAU = 0.5
SEED = 0
N_BOOT = 4000
# P5 reuses P4's queries and only adds a confidence-drop term, so the
# answer-change signal of P5 is read off P4. P3 = P1 with a second-turn probe
# that does not enter the score (direct aggregation), so it is its own source.
ANSWER_SIGNAL_SOURCE = {"P1": "P1", "P2": "P2", "P3": "P3", "P4": "P4", "P5": "P4"}


# ----------------------------------------------------------------- loading
def load_rows(ds: str, model: str, method: str) -> dict[str, dict]:
    path = os.path.join(RAW, ds, model, f"{method}.jsonl")
    with open(path) as f:
        return {r["qid"]: r for r in map(json.loads, f)}


def load_passages(ds: str) -> dict[str, dict]:
    path = os.path.join(DATA, f"{ds}_validation.jsonl")
    if not os.path.exists(path):
        sys.exit(f"missing {path}; run: gunzip -k {path}.gz")
    out = {}
    with open(path) as f:
        for line in f:
            x = json.loads(line)
            out[x["qid"]] = x
    return out


# ----------------------------------------------------------------- per-instance quantities
def tie_group(phi: np.ndarray) -> np.ndarray:
    return np.flatnonzero(phi == phi.max())


def top1_fixed(r: dict) -> float:
    return float(r["ranking"][0] in r["gold"])


def top1_tieavg(r: dict) -> float:
    """Expected top-1 hit if the winner is drawn uniformly from the max-score tie group."""
    phi = np.asarray(r["phi"], dtype=float)
    T = tie_group(phi)
    gold = set(r["gold"])
    return sum(int(i) in gold for i in T) / len(T)


def signal_fields(phi: np.ndarray) -> dict:
    return {
        "all_zero": bool(not np.any(phi)),
        "below_tau_nonzero": bool(np.any(phi) and not np.any(phi >= TAU)),
        "reaches_tau": bool(np.any(phi >= TAU)),
        "unique_max": bool(len(tie_group(phi)) == 1),
    }


_ARTICLE = re.compile(r"^(the|a|an)\s+")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).lower().strip()
    s = s.replace("’", "'").replace("‘", "'")
    s = _ARTICLE.sub("", s)
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def contains(text: str, answer: str) -> bool:
    a = norm(answer)
    if not a:
        return False
    return re.search(r"(?<!\w)" + re.escape(a) + r"(?!\w)", norm(text)) is not None


# ----------------------------------------------------------------- statistics
def paired_boot_ci(diff: np.ndarray, rng: np.random.Generator) -> tuple[float, float]:
    if diff.size == 0:
        return (math.nan, math.nan)
    idx = rng.integers(0, diff.size, size=(N_BOOT, diff.size))
    means = diff[idx].mean(axis=1)
    return (float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5)))


def mcnemar_exact(a: np.ndarray, b: np.ndarray) -> tuple[int, int, float]:
    """a, b: 0/1 arrays. b_ = only a correct, c_ = only b correct."""
    b_ = int(np.sum((a == 1) & (b == 0)))
    c_ = int(np.sum((a == 0) & (b == 1)))
    if b_ + c_ == 0:
        return b_, c_, 1.0
    return b_, c_, float(binomtest(b_, b_ + c_, 0.5).pvalue)


def wilson(k: float, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (math.nan, math.nan)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def logistic_fit(X: np.ndarray, y: np.ndarray, iters: int = 50):
    """Plain IRLS logistic regression; returns (coef, se). X includes intercept."""
    beta = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ beta))
        W = p * (1 - p) + 1e-9
        H = X.T @ (X * W[:, None])
        g = X.T @ (y - p)
        step = np.linalg.solve(H, g)
        beta += step
        if np.max(np.abs(step)) < 1e-8:
            break
    p = 1 / (1 + np.exp(-X @ beta))
    H = X.T @ (X * (p * (1 - p))[:, None])
    se = np.sqrt(np.diag(np.linalg.inv(H)))
    return beta, se


def mean(xs) -> float:
    xs = list(xs)
    return float(np.mean(xs)) if xs else math.nan


# ----------------------------------------------------------------- analyses
def method_table(ds, model, rows_by_method):
    out = []
    any_rows = next(iter(rows_by_method.values()))
    floor = mean(len(r["gold"]) / r["meta"]["M"] for r in any_rows.values())
    for meth, rows in rows_by_method.items():
        fields = [signal_fields(np.asarray(r["phi"], float)) for r in rows.values()]
        rec = {
            "dataset": ds, "model": model, "method": meth, "n": len(rows),
            "random_floor": floor,
            "top1_fixed": mean(top1_fixed(r) for r in rows.values()),
            "top1_tieavg": mean(top1_tieavg(r) for r in rows.values()),
            "old_empty_rate": mean(r["empty_prediction"] for r in rows.values()),
            "all_zero": mean(f["all_zero"] for f in fields),
            "below_tau_nonzero": mean(f["below_tau_nonzero"] for f in fields),
            "reaches_tau": mean(f["reaches_tau"] for f in fields),
            "unique_max": mean(f["unique_max"] for f in fields),
            "parse_failures": mean(r["parse_failures"] / max(r["n_observations"], 1) for r in rows.values()),
        }
        if meth.startswith("P"):
            src = rows_by_method[ANSWER_SIGNAL_SOURCE[meth]]
            cov = {q: bool(np.any(np.asarray(src[q]["phi"], float))) for q in rows}
            rec["answer_change_coverage"] = mean(cov.values())
            rec["conf_only_signal"] = mean(
                (not cov[q]) and bool(np.any(np.asarray(rows[q]["phi"], float))) for q in rows
            )
            covered = [q for q in rows if cov[q]]
            uncovered = [q for q in rows if not cov[q]]
            rec["n_covered"] = len(covered)
            rec["top1_tieavg_covered"] = mean(top1_tieavg(rows[q]) for q in covered)
            rec["top1_fixed_covered"] = mean(top1_fixed(rows[q]) for q in covered)
            rec["top1_fixed_uncovered"] = mean(top1_fixed(rows[q]) for q in uncovered)
            rec["top1_tieavg_uncovered"] = mean(top1_tieavg(rows[q]) for q in uncovered)
        out.append(rec)
    return out


def matched_gaps(ds, model, R, rng):
    """V_i vs P_i on all instances and on instances where P_i has an answer-change signal."""
    out = []
    for i in range(1, 6):
        V, P = R[f"V{i}"], R[f"P{i}"]
        src = R[ANSWER_SIGNAL_SOURCE[f"P{i}"]]
        q_all = sorted(set(V) & set(P))
        q_cov = [q for q in q_all if np.any(np.asarray(src[q]["phi"], float))]
        for subset, qs in [("all", q_all), ("covered", q_cov)]:
            vt = np.array([top1_tieavg(V[q]) for q in qs])
            pt = np.array([top1_tieavg(P[q]) for q in qs])
            vf = np.array([top1_fixed(V[q]) for q in qs])
            pf = np.array([top1_fixed(P[q]) for q in qs])
            lo, hi = paired_boot_ci(vt - pt, rng)
            b_, c_, p = mcnemar_exact(vf, pf)
            out.append({
                "dataset": ds, "model": model, "pair": f"V{i}/P{i}", "subset": subset, "n": len(qs),
                "V_tieavg": mean(vt), "P_tieavg": mean(pt), "gap_tieavg": mean(vt - pt),
                "gap_ci_lo": lo, "gap_ci_hi": hi,
                "V_fixed": mean(vf), "P_fixed": mean(pf), "gap_fixed": mean(vf - pf),
                "mcnemar_b": b_, "mcnemar_c": c_, "mcnemar_p": p,
            })
    return out


def spearman_rows(ds, model, R):
    out = []
    pairs = [("V7", "P5"), ("V2", "P5")] + [(f"V{i}", f"P{i}") for i in range(1, 6)]
    for a, b in pairs:
        A, B = R[a], R[b]
        fixed, tied, n_const = [], [], 0
        for q in set(A) & set(B):
            pa, pb = np.asarray(A[q]["phi"], float), np.asarray(B[q]["phi"], float)
            if pa.std() == 0 or pb.std() == 0:
                n_const += 1
                continue
            M = len(pa)
            ra = -np.array([A[q]["ranking"].index(k) for k in range(M)])
            rb = -np.array([B[q]["ranking"].index(k) for k in range(M)])
            fixed.append(spearmanr(ra, rb)[0])
            tied.append(spearmanr(pa, pb)[0])
        out.append({"dataset": ds, "model": model, "pair": f"{a}/{b}", "n_defined": len(tied),
                    "n_constant_excluded": n_const,
                    "rho_index_tiebreak": mean(fixed), "rho_tie_preserving": mean(tied)})
    return out


def expected_topk_inclusion(phi: np.ndarray, k: int) -> np.ndarray:
    """P(source i is in the top-k) when ties at the cut-off are broken uniformly."""
    phi = np.asarray(phi, float)
    order = np.sort(np.unique(phi))[::-1]
    inc = np.zeros_like(phi)
    slots = k
    for v in order:
        grp = np.flatnonzero(phi == v)
        if slots <= 0:
            break
        take = min(slots, len(grp))
        inc[grp] = take / len(grp)
        slots -= take
    return inc


def string_baseline(ds, model, R, passages):
    """Output-conditioned string baseline (no extra query to the target model).

    It uses the target model's own full-context answer (the P1 baseline answer,
    T=0.01), so it is NOT model-free; it needs no attribution query. Passages
    whose text contains that answer string are tied at the top.

    `gold_without_answer_string` = gold passages that do not contain the P1
    answer string. This is a lexical category, not a verified reasoning role
    (aliases, pronouns, titles and incidental mentions break the
    correspondence), and V1's own answer may differ from P1's answer.
    Recall is reported (i) at tau (deployment view; fallback not counted) and
    (ii) as tie-aware recall@k with k = |gold| (independent of set size).
    """
    P1, V1 = R["P1"], R["V1"]
    hits, agree, v_in_contains, n_def = [], [], [], 0
    rec_tau = {("V1", "with"): [], ("V1", "without"): [], ("P1", "with"): [], ("P1", "without"): []}
    rec_k = {key: [] for key in rec_tau}
    set_size = {"V1": [], "P1": []}
    gold_contains_frac = []
    for q, r in P1.items():
        ans = r.get("baseline_answer")
        if not ans or q not in passages:
            continue
        src = passages[q]["sources"]
        has = np.array([contains(s["title"] + " " + s["text"], ans) for s in src])
        gold = set(r["gold"])
        gold_contains_frac.append(mean(has[g] for g in gold))
        if has.any():
            n_def += 1
            T = np.flatnonzero(has)
            hits.append(sum(int(i) in gold for i in T) / len(T))
            agree.append(float(V1[q]["ranking"][0] in set(T.tolist())))
        else:
            hits.append(len(gold) / len(src))
        v_in_contains.append(float(has[V1[q]["ranking"][0]]))
        for meth, rows in [("V1", V1), ("P1", P1)]:
            phi = np.asarray(rows[q]["phi"], float)
            pred = set(np.flatnonzero(phi >= TAU).tolist())  # fallback not counted
            set_size[meth].append(len(pred))
            inc = expected_topk_inclusion(phi, len(gold))
            for g in gold:
                key = (meth, "with" if has[g] else "without")
                rec_tau[key].append(float(g in pred))
                rec_k[key].append(float(inc[g]))
    out = {
        "dataset": ds, "model": model, "n": len(hits),
        "frac_answer_found_in_some_passage": n_def / max(len(hits), 1),
        "output_conditioned_string_top1_tieavg": mean(hits),
        "V1_top1_agrees_with_string_match": mean(agree),
        "V1_top1_contains_P1_answer": mean(v_in_contains),
        "gold_passages_containing_answer": mean(gold_contains_frac),
        "V1_mean_set_size_at_tau": mean(set_size["V1"]),
        "P1_mean_set_size_at_tau": mean(set_size["P1"]),
    }
    for (meth, kind), v in rec_tau.items():
        tag = "gold_with_answer_string" if kind == "with" else "gold_without_answer_string"
        out[f"{meth}_recall_at_tau_{tag}"] = mean(v)
        out[f"{meth}_recall_at_k_{tag}"] = mean(rec_k[(meth, kind)])
    out["n_gold_with_answer_string"] = len(rec_tau[("V1", "with")])
    out["n_gold_without_answer_string"] = len(rec_tau[("V1", "without")])
    return out


def hop_rows(model, R, rng):
    """Per-hop accuracy against the random floor.

    On MuSiQue the gold count equals the hop count, so the random floor g/M is a
    deterministic function of hop: hop and chance cannot both enter one
    regression (perfectly collinear). We therefore report (i) a chance-corrected
    accuracy kappa_h = (acc_h - floor_h) / (1 - floor_h) per hop with a bootstrap
    CI, (ii) the 4-hop minus 2-hop difference in kappa with a CI, and (iii) an
    uncorrected logistic odds ratio per hop for reference -- its direction is
    biased upward by the rising floor.
    """
    out = []
    for meth in ["V1", "V7", "P1", "P5"]:
        rows = R[meth]
        by = defaultdict(list)
        X, y = [], []
        for r in rows.values():
            h = r["meta"]["n_hop"]
            chance = len(r["gold"]) / r["meta"]["M"]
            by[h].append((top1_tieavg(r), chance))
            X.append([1.0, float(h)])
            y.append(top1_fixed(r))
        try:
            beta, se = logistic_fit(np.array(X), np.array(y))
            if not np.all(np.isfinite(se)) or abs(beta[1]) > 20:
                raise ValueError("separation / non-convergence")
            or_hop = math.exp(beta[1]); lo = math.exp(beta[1] - 1.96 * se[1]); hi = math.exp(beta[1] + 1.96 * se[1])
        except (np.linalg.LinAlgError, ValueError, OverflowError, FloatingPointError):
            or_hop = lo = hi = math.nan

        def kappa(pairs):
            a = np.array([p[0] for p in pairs]); c = np.array([p[1] for p in pairs])
            return (a.mean() - c.mean()) / (1 - c.mean())

        def kappa_ci(pairs):
            arr = np.array(pairs)
            ks = [kappa(arr[rng.integers(0, len(arr), len(arr))]) for _ in range(1000)]
            return float(np.percentile(ks, 2.5)), float(np.percentile(ks, 97.5))

        hops = sorted(by)
        diff = lo_d = hi_d = math.nan
        if 2 in by and 4 in by:
            a2, a4 = np.array(by[2]), np.array(by[4])
            diff = kappa(a4) - kappa(a2)
            ds_ = [kappa(a4[rng.integers(0, len(a4), len(a4))]) - kappa(a2[rng.integers(0, len(a2), len(a2))])
                   for _ in range(1000)]
            lo_d, hi_d = float(np.percentile(ds_, 2.5)), float(np.percentile(ds_, 97.5))
        for h in hops:
            acc = mean(a for a, _ in by[h]); fl = mean(c for _, c in by[h]); n = len(by[h])
            klo, khi = kappa_ci(by[h])
            out.append({"model": model, "method": meth, "hop": h, "n": n, "top1_tieavg": acc,
                        "random_floor": fl, "kappa_chance_corrected": kappa(by[h]),
                        "kappa_ci_lo": klo, "kappa_ci_hi": khi,
                        "kappa_4hop_minus_2hop": diff, "diff_ci_lo": lo_d, "diff_ci_hi": hi_d,
                        "uncorrected_OR_per_hop": or_hop, "OR_ci_lo": lo, "OR_ci_hi": hi})
    return out


def noise_proxy(ds, model, R):
    """Sensitivity to deleting NON-gold passages (exploratory; not a noise bound).

    Two quantities, because P1 uses N=1 and P2/P4 use N=3:
      *_any_change_frac   share of non-gold sources with phi > 0, i.e. "changed
                          in at least one of N draws" -- mechanically larger for
                          N=3 (1-(1-p)^3 vs p), so NOT comparable across N;
      *_per_draw_rate     mean phi over non-gold sources (= per-draw change rate),
                          the comparable quantity.
    Non-gold is not the same as behaviourally irrelevant, and the temperatures are
    not matched (baseline T=0.01), so neither is a causal temperature effect.
    """
    out = {"dataset": ds, "model": model}
    for meth in ["P1", "P2", "P4"]:
        any_frac, per_draw = [], []
        for r in R[meth].values():
            phi = np.asarray(r.get("meta", {}).get("answer_phi") or r["phi"], float)
            ng = [i for i in range(len(phi)) if i not in set(r["gold"])]
            any_frac.append(mean(phi[i] > 0 for i in ng))
            per_draw.append(mean(phi[i] for i in ng))
        out[f"{meth}_nongold_any_change_frac"] = mean(any_frac)
        out[f"{meth}_nongold_per_draw_rate"] = mean(per_draw)
    return out


def first_source_rate(R):
    return {m: mean(r["ranking"][0] == 0 for r in R[m].values()) for m in ["V1", "V7", "P1"]}


# ----------------------------------------------------------------- main
def write_csv(path, rows):
    import csv
    if not rows:
        return
    keys = list(rows[0].keys())
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    rng = np.random.default_rng(SEED)

    T_method, T_gap, T_rho, T_str, T_hop, T_noise, T_first = [], [], [], [], [], [], []
    for ds in DATASETS:
        passages = load_passages(ds)
        for model in MODELS:
            R = {m: load_rows(ds, model, m) for m in V_METHODS + P_METHODS}
            T_method += method_table(ds, model, R)
            T_gap += matched_gaps(ds, model, R, rng)
            T_rho += spearman_rows(ds, model, R)
            T_str.append(string_baseline(ds, model, R, passages))
            T_noise.append(noise_proxy(ds, model, R))
            T_first.append({"dataset": ds, "model": model, **{f"{k}_first_source_rate": v for k, v in first_source_rate(R).items()}})
            if ds == "musique":
                T_hop += hop_rows(model, R, rng)

    write_csv(os.path.join(args.out, "methods.csv"), T_method)
    write_csv(os.path.join(args.out, "matched_gaps.csv"), T_gap)
    write_csv(os.path.join(args.out, "spearman.csv"), T_rho)
    write_csv(os.path.join(args.out, "string_baseline.csv"), T_str)
    write_csv(os.path.join(args.out, "hop_musique.csv"), T_hop)
    write_csv(os.path.join(args.out, "noise_proxy.csv"), T_noise)
    write_csv(os.path.join(args.out, "first_source_rate.csv"), T_first)
    print("wrote", sorted(os.listdir(args.out)))


if __name__ == "__main__":
    main()
