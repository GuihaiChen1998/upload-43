#!/usr/bin/env python3
"""Post-hoc analysis of the per-hop perturbation anomaly (Sec. 6.2 / 6.5).

The aggregate tables showed perturbation top-1 RISING with hop count and empty
predictions FALLING -- the opposite of the redundant-path hypothesis. Before
building any explanation on that, this script asks two questions of the existing
result files, and reports significance so a small-sample fluctuation is not
mistaken for a trend.

Q1  RESIDUAL LEAKAGE. Are 2-hop empty-prediction cases (ablation changed
    nothing) concentrated on short, common answers the model could produce
    without the ablated source? If so, the low 2-hop perturbation score is a
    leakage artifact that 01c's all-or-nothing check did not catch, not
    evidence about redundancy.

Q2  PER-HOP GAP. Is the verbalize-vs-perturbation gap concentrated in a
    particular hop stratum? A gap that lives almost entirely in 2-hop points to
    a 2-hop-specific cause rather than a general property of the paradigms.

Reads results/raw/<dataset>/<model>/{V*,P*}.jsonl. No model calls.

  python scripts/07_analyze_hop_gap.py --model qwen3-8b --dataset musique
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def load_cell(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def top1_correct(r) -> bool:
    return bool(r["ranking"]) and r["ranking"][0] in set(r["gold"])


def _fisher_or_chi2(table):
    """2xk contingency test. Prefer scipy; fall back to a chi-square by hand.

    Returns (statistic_name, p_value_or_None). p is None if we cannot compute
    it without scipy and the table is larger than 2x2.
    """
    try:
        from scipy.stats import chi2_contingency, fisher_exact
        if len(table) == 2 and all(len(row) == 2 for row in table):
            _, p = fisher_exact(table)
            return "fisher_exact", p
        chi2, p, _, _ = chi2_contingency(table)
        return "chi2", p
    except Exception:
        return "unavailable", None


def _bin_ci(k, n):
    """Wilson 95% interval -- more honest than normal approx at small n."""
    if n == 0:
        return (0.0, 0.0)
    from math import sqrt
    z = 1.96
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0, centre - half), min(1, centre + half))


def q1_residual_leakage(p_results, dataset):
    """Q1: are 2-hop empty-prediction answers short/common?"""
    print("\n=== Q1: residual leakage in 2-hop empty predictions ===")
    by_hop_empty = defaultdict(list)
    by_hop_all = defaultdict(int)
    for r in p_results:
        h = r.get("meta", {}).get("n_hop")
        if h is None:
            continue
        by_hop_all[h] += 1
        if r.get("empty_prediction"):
            ans = (r.get("baseline_answer") or "").strip()
            by_hop_empty[h].append(ans)

    for h in sorted(by_hop_all):
        empties = by_hop_empty.get(h, [])
        n_all = by_hop_all[h]
        if not empties:
            print(f"  {h}-hop: 0/{n_all} empty predictions")
            continue
        lens = [len(a.split()) for a in empties if a]
        short = sum(1 for L in lens if L <= 2)
        avg_len = sum(lens) / len(lens) if lens else 0
        lo, hi = _bin_ci(len(empties), n_all)
        print(f"  {h}-hop: {len(empties)}/{n_all} empty "
              f"({len(empties)/n_all:.1%}, 95% CI [{lo:.2f},{hi:.2f}]); "
              f"of the empty, mean answer length {avg_len:.1f} words, "
              f"{short}/{len(empties)} are <=2 words")
        sample = [a for a in empties if a][:8]
        if sample:
            print(f"       examples: {sample}")

    print("\n  reading: if 2-hop empties are mostly <=2-word answers while the "
          "deeper strata's are longer, the low 2-hop perturbation score is "
          "consistent with residual leakage (the model reconstructs a short "
          "common answer without the ablated source), not with redundancy.")


def q2_per_hop_gap(v_results, p_results):
    """Q2: is the verbalize-perturbation top-1 gap concentrated by hop?"""
    print("\n=== Q2: verbalize-vs-perturbation gap by hop ===")
    v_by_qid = {r["qid"]: r for r in v_results}
    hop_v = defaultdict(lambda: [0, 0])   # hop -> [correct, total]
    hop_p = defaultdict(lambda: [0, 0])
    paired = defaultdict(lambda: [0, 0])  # hop -> [both-defined, v_correct_p_wrong]

    for pr in p_results:
        qid = pr["qid"]
        vr = v_by_qid.get(qid)
        if vr is None:
            continue
        h = pr.get("meta", {}).get("n_hop")
        if h is None:
            continue
        vc, pc = top1_correct(vr), top1_correct(pr)
        hop_v[h][0] += vc; hop_v[h][1] += 1
        hop_p[h][0] += pc; hop_p[h][1] += 1

    print(f"  {'hop':>4} {'n':>5} {'V top1':>8} {'P top1':>8} {'gap':>7}  95% CI on gap")
    hop_tables = []
    for h in sorted(hop_v):
        vk, vn = hop_v[h]; pk, pn = hop_p[h]
        vt, pt = vk / vn, pk / pn
        gap = vt - pt
        # CI on the difference of two proportions (independent approx; the two
        # are paired, so this is conservative-ish but fine as a guide).
        from math import sqrt
        se = sqrt(vt * (1 - vt) / vn + pt * (1 - pt) / pn)
        print(f"  {h:>4} {vn:>5} {vt:>8.3f} {pt:>8.3f} {gap:>7.3f}  "
              f"[{gap-1.96*se:+.3f}, {gap+1.96*se:+.3f}]")
        # contingency for perturbation correctness across this hop vs the rest
        hop_tables.append((h, pk, pn - pk))

    # Is perturbation correctness associated with hop at all?
    if len(hop_tables) >= 2:
        table = [[k, wrong] for _, k, wrong in hop_tables]
        name, p = _fisher_or_chi2(table)
        if p is not None:
            verdict = ("significant" if p < 0.05 else "NOT significant")
            print(f"\n  perturbation correctness vs hop: {name} p={p:.3f} "
                  f"({verdict} at 0.05)")
            if p >= 0.05:
                print("  -> the apparent hop trend in perturbation is within "
                      "sampling noise; do NOT claim a hop effect from this model "
                      "alone. Pool models or use the full per-model evaluable set "
                      "(more 4-hop) before concluding.")
            else:
                print("  -> the hop association is unlikely to be pure noise; "
                      "still confirm the direction replicates across models.")
        else:
            print("\n  (install scipy for a significance test: pip install scipy)")

    print("\n  reading: if the gap is large only at 2-hop and shrinks or vanishes "
          "deeper, the paradigm gap is driven by a 2-hop-specific effect (see "
          "Q1), not by a uniform difference between self-report and intervention.")


def q3_pooled_gap(model_dirs, dataset, raw_root):
    """Pool the verbalize-vs-perturbation gap across models -- Sec. 6.2/6.3.

    Two questions the single-model view cannot answer:
      * Is the gap real once we stop looking at one noisy model? Pooling the
        paired (verbalize-correct, perturbation-correct) outcomes across models
        gives a joint test with much more power.
      * Does the gap shrink monotonically with scale? Reports per-model gaps in
        size order and checks strict monotonicity, rather than eyeballing three
        numbers.
    """
    print("\n=== Q3: pooled gap across models ===")

    def best(cells):
        return max(cells.items(),
                   key=lambda kv: sum(top1_correct(r) for r in kv[1]) / len(kv[1]))

    rows = []  # (model, params_b, v_top1, p_top1, gap, n, v_correct, p_correct)
    excluded = []  # models whose verbalize collapsed to ~random
    pooled_v_correct = pooled_p_correct = pooled_n = 0
    # McNemar counts pooled across models: discordant pairs only.
    b = c = 0  # b: V right & P wrong, c: V wrong & P right
    for model, params in model_dirs:
        cell_dir = os.path.join(raw_root, dataset, model)
        v_cells, p_cells = {}, {}
        for path in glob.glob(os.path.join(cell_dir, "*.jsonl")):
            mid = os.path.basename(path).replace(".jsonl", "")
            (v_cells if mid.startswith("V") else p_cells)[mid] = load_cell(path) \
                if (mid.startswith("V") or mid.startswith("P")) else None
        v_cells = {k: v for k, v in v_cells.items() if v is not None}
        p_cells = {k: v for k, v in p_cells.items() if v is not None}
        if not v_cells or not p_cells:
            print(f"  {model}: missing V or P cells, skipped")
            continue
        v_res = best(v_cells)[1]
        p_res = best(p_cells)[1]

        # Verbalize-collapse guard. If the best verbalize method scores at or
        # below chance (|gold|/M averaged), self-report is not producing
        # meaningful attributions -- the model emits parseable but essentially
        # random source numbers. Its negative "gap" reflects a broken verbalize
        # channel, not perturbation superiority, so pooling it would flip the
        # sign of the aggregate. Report it separately as a method-applicability
        # boundary rather than folding it in.
        from statistics import mean as _mean
        chance = _mean([len(set(r["gold"])) / max(1, len(r["phi"])) for r in v_res])
        v_top1 = sum(top1_correct(r) for r in v_res) / len(v_res)
        if v_top1 <= chance * 1.5:
            excluded.append((model, params, v_top1, chance,
                             sum(top1_correct(r) for r in p_res) / len(p_res)))
            continue

        p_by_qid = {r["qid"]: r for r in p_res}
        vk = pk = n = 0
        for vr in v_res:
            pr = p_by_qid.get(vr["qid"])
            if pr is None:
                continue
            n += 1
            vc, pc = top1_correct(vr), top1_correct(pr)
            vk += vc; pk += pc
            if vc and not pc:
                b += 1
            elif pc and not vc:
                c += 1
        rows.append((model, params, vk / n, pk / n, (vk - pk) / n, n))
        pooled_v_correct += vk; pooled_p_correct += pk; pooled_n += n

    if excluded:
        print("  EXCLUDED from pooling (verbalize collapsed to ~chance;")
        print("  report as a self-report applicability boundary, not a gap):")
        for model, params, vt, ch, pt in excluded:
            pstr = f"{params:g}B" if params else "?"
            print(f"    {model} ({pstr}): V top1={vt:.3f} vs chance~{ch:.3f}, "
                  f"P top1={pt:.3f} -> verbalize unusable, perturbation fine")

    if not rows:
        print("  no usable models")
        return

    print(f"  {'model':16s} {'params':>7} {'V top1':>8} {'P top1':>8} {'gap':>7} {'n':>5}")
    for model, params, vt, pt, gap, n in sorted(rows, key=lambda r: r[1] or 0):
        pstr = f"{params:g}B" if params else "?"
        print(f"  {model:16s} {pstr:>7} {vt:>8.3f} {pt:>8.3f} {gap:>+7.3f} {n:>5}")

    # Pooled gap and its joint significance (McNemar on discordant pairs).
    pooled_gap = (pooled_v_correct - pooled_p_correct) / pooled_n
    print(f"\n  pooled: V={pooled_v_correct/pooled_n:.3f} "
          f"P={pooled_p_correct/pooled_n:.3f} gap={pooled_gap:+.3f} (n={pooled_n})")
    print(f"  discordant pairs: V-right-P-wrong={b}, P-right-V-wrong={c}")
    try:
        from scipy.stats import binomtest
        # McNemar's exact test: under H0 the discordant pairs split 50/50.
        res = binomtest(b, b + c, 0.5, alternative="two-sided")
        pval = res.pvalue
        print(f"  McNemar exact p={pval:.2e} "
              f"({'gap is real' if pval < 0.05 else 'not significant'})")
    except Exception:
        from math import sqrt
        chi = (abs(b - c) - 1) ** 2 / (b + c) if (b + c) else 0
        print(f"  McNemar chi2(cc)={chi:.1f} (install scipy for exact p)")

    # Monotonicity of the scale trend.
    ordered = [r for r in sorted(rows, key=lambda r: r[1] or 0) if r[1]]
    gaps = [r[4] for r in ordered]
    if len(gaps) >= 3:
        strictly_down = all(a > b for a, b in zip(gaps, gaps[1:]))
        strictly_up = all(a < b for a, b in zip(gaps, gaps[1:]))
        trend = ("monotonically SHRINKS with scale" if strictly_down else
                 "monotonically GROWS with scale" if strictly_up else
                 "is NOT monotonic in scale")
        print(f"\n  gap {trend}: {[f'{g:+.3f}' for g in gaps]}")
        # decompose: is shrinkage driven by P or V?
        p_delta = ordered[-1][3] - ordered[0][3]
        v_delta = ordered[-1][2] - ordered[0][2]
        print(f"  across the size range: P top1 {p_delta:+.3f}, "
              f"V top1 {v_delta:+.3f} "
              f"-> change is driven by the "
              f"{'perturbation' if abs(p_delta) > abs(v_delta) else 'verbalize'} side")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=None, help="single-model mode")
    ap.add_argument("--models", nargs="+", default=None,
                    help="pooled multi-model mode: 'name:params' pairs, e.g. "
                         "qwen3-1.7b:1.7 qwen3-4b:4 qwen3-8b:8")
    ap.add_argument("--dataset", default="musique")
    ap.add_argument("--raw-root", default="results/raw")
    ap.add_argument("--v-method", default=None,
                    help="verbalize method to use (default: best by top-1)")
    ap.add_argument("--p-method", default=None,
                    help="perturbation method to use (default: best by top-1)")
    args = ap.parse_args()

    if args.models:
        model_dirs = []
        for spec in args.models:
            if ":" in spec:
                name, params = spec.rsplit(":", 1)
                model_dirs.append((name, float(params)))
            else:
                model_dirs.append((spec, None))
        q3_pooled_gap(model_dirs, args.dataset, args.raw_root)
        return

    if not args.model:
        ap.error("provide --model (single) or --models (pooled)")

    cell_dir = os.path.join(args.raw_root, args.dataset, args.model)
    if not os.path.isdir(cell_dir):
        print(f"no results at {cell_dir}")
        return

    v_cells, p_cells = {}, {}
    for path in glob.glob(os.path.join(cell_dir, "*.jsonl")):
        mid = os.path.basename(path).replace(".jsonl", "")
        rows = load_cell(path)
        if mid.startswith("V"):
            v_cells[mid] = rows
        elif mid.startswith("P"):
            p_cells[mid] = rows

    if not p_cells:
        print("no perturbation results found; Q1 and Q2 need P* cells")
        return

    def best(cells):
        return max(cells.items(),
                   key=lambda kv: sum(top1_correct(r) for r in kv[1]) / len(kv[1]))

    p_mid = args.p_method or best(p_cells)[0]
    p_results = p_cells[p_mid]
    print(f"model={args.model} dataset={args.dataset}")
    print(f"perturbation method: {p_mid} (n={len(p_results)})")

    q1_residual_leakage(p_results, args.dataset)

    if v_cells:
        v_mid = args.v_method or best(v_cells)[0]
        print(f"\nverbalize method: {v_mid} (n={len(v_cells[v_mid])})")
        q2_per_hop_gap(v_cells[v_mid], p_results)
    else:
        print("\nno verbalize cells; skipping Q2")


if __name__ == "__main__":
    main()
