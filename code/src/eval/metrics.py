"""Black-box metrics -- paper Sec. 5.4.

All of these are computable without logits, which is what lets the closed-model
column exist at all. The gray-box log-probability drop lives in eval/graybox.py
and runs on open models only.
"""
from __future__ import annotations

from collections import defaultdict
from statistics import mean


def top1_accuracy(results) -> float:
    """Hitting any link of the reasoning chain counts as correct (Sec. 5.4)."""
    if not results:
        return 0.0
    return mean(1.0 if r.top1_correct else 0.0 for r in results)


def set_f1(results) -> float:
    """Mean per-instance F1 of predicted vs gold source sets."""
    scores = []
    for r in results:
        pred, gold = set(r.pred_set), set(r.gold)
        if not pred and not gold:
            scores.append(1.0)
            continue
        tp = len(pred & gold)
        p = tp / len(pred) if pred else 0.0
        rec = tp / len(gold) if gold else 0.0
        scores.append(2 * p * rec / (p + rec) if p + rec else 0.0)
    return mean(scores) if scores else 0.0


def mean_query_cost(results) -> float:
    return mean(r.n_calls for r in results) if results else 0.0


def parse_failure_rate(results) -> float:
    tot = sum(r.n_observations for r in results)
    return sum(r.parse_failures for r in results) / tot if tot else 0.0


def empty_prediction_rate(results) -> float:
    return mean(1.0 if r.empty_prediction else 0.0 for r in results) if results else 0.0


def random_baseline_top1(instances) -> float:
    """|gold| / M, averaged. Rises with hop count on MuSiQue, so it must be
    reported alongside absolute scores or the numbers get misread."""
    if not instances:
        return 0.0
    return mean(len(i.gold_indices) / i.M for i in instances)


def summarize(results, instances=None) -> dict:
    out = {
        "n": len(results),
        "top1_accuracy": top1_accuracy(results),
        "set_f1": set_f1(results),
        "mean_query_cost": mean_query_cost(results),
        "parse_failure_rate": parse_failure_rate(results),
        "empty_prediction_rate": empty_prediction_rate(results),
    }
    if instances:
        out["random_baseline_top1"] = random_baseline_top1(instances)
    return out


def by_hop(results) -> dict[int, dict]:
    """Stratify by MuSiQue hop count -- Sec. 6.5.

    The prediction is that empty-prediction rate rises with hops: more hops
    means more redundant reasoning paths, and single-source ablation cannot
    detect a source whose removal leaves an alternative path intact.
    """
    groups = defaultdict(list)
    for r in results:
        h = r.meta.get("n_hop")
        if h is not None:
            groups[h].append(r)
    return {h: summarize(rs) for h, rs in sorted(groups.items())}


def agreement(res_v, res_p) -> dict:
    """Verbalize vs perturbation contingency -- Sec. 6.2, Figure 4(a)."""
    by_qid = {r.qid: r for r in res_p}
    cells = dict(both_correct=0, only_v=0, only_p=0, both_wrong_same=0,
                 both_wrong_diff=0, same_top1=0, n=0)
    for v in res_v:
        p = by_qid.get(v.qid)
        if p is None:
            continue
        cells["n"] += 1
        tv, tp = v.ranking[0] if v.ranking else -1, p.ranking[0] if p.ranking else -2
        if tv == tp:
            cells["same_top1"] += 1
        if v.top1_correct and p.top1_correct:
            cells["both_correct"] += 1
        elif v.top1_correct:
            cells["only_v"] += 1
        elif p.top1_correct:
            cells["only_p"] += 1
        elif tv == tp:
            cells["both_wrong_same"] += 1
        else:
            cells["both_wrong_diff"] += 1
    n = cells["n"] or 1
    cells["agreement_rate"] = cells["same_top1"] / n
    return cells


def overlap_with_baseline(method_results, baseline_results) -> dict:
    """Quantify how much a method's attribution coincides with a shallow
    baseline (BM25 / embedding) -- Sec. 6.2 diagnostic.

    This is NOT a contest the method must win. In an empirical study the point
    is interpretive: high overlap with BM25 suggests the method may be tracking
    lexical overlap rather than model behaviour; high overlap with embeddings
    suggests semantic-retrieval-like behaviour; low overlap with both is the
    interesting case, where the black-box signal is not reducible to retrieval.

    Reports three views:
      top1_agreement   -- fraction where the top-1 source coincides
      setF1_of_sets    -- mean F1 between the two predicted sets
      rank_correlation -- mean Spearman rho between the two full rankings
    """
    from statistics import mean

    b_by_qid = {r.qid: r for r in baseline_results}
    top1, setf1, rho = [], [], []
    for m in method_results:
        b = b_by_qid.get(m.qid)
        if b is None:
            continue
        top1.append(1.0 if (m.ranking and b.ranking
                            and m.ranking[0] == b.ranking[0]) else 0.0)

        ms, bs = set(m.pred_set), set(b.pred_set)
        if ms or bs:
            tp = len(ms & bs)
            p = tp / len(ms) if ms else 0.0
            rec = tp / len(bs) if bs else 0.0
            setf1.append(2 * p * rec / (p + rec) if p + rec else 0.0)

        r = _spearman(m.ranking, b.ranking)
        if r is not None:
            rho.append(r)

    return {
        "top1_agreement": mean(top1) if top1 else None,
        "set_f1": mean(setf1) if setf1 else None,
        "rank_correlation": mean(rho) if rho else None,
        "n": len(top1),
    }


def _spearman(rank_a: list[int], rank_b: list[int]) -> float | None:
    """Spearman rho between two rankings given as ordered index lists.

    Each ranking is a permutation of source indices (position 0 = most
    important). Convert to per-index positions, then correlate.
    """
    if not rank_a or not rank_b or len(rank_a) != len(rank_b):
        return None
    n = len(rank_a)
    if n < 2:
        return None
    pos_a = {idx: r for r, idx in enumerate(rank_a)}
    pos_b = {idx: r for r, idx in enumerate(rank_b)}
    common = set(pos_a) & set(pos_b)
    if len(common) < 2:
        return None
    d2 = sum((pos_a[i] - pos_b[i]) ** 2 for i in common)
    k = len(common)
    return 1.0 - (6.0 * d2) / (k * (k * k - 1))


def selection_bias(results, instances) -> dict:
    """Is disagreement directional? -- Sec. 6.2.

    Reports the mean position index of selected vs gold sources. A verbalize
    pipeline that systematically favours early paragraphs, while ablation shows
    no such preference, is evidence for rationalisation rather than introspection.
    Only with a directional effect like this does "systematically" belong in the
    paper's claims.
    """
    by_qid = {i.qid: i for i in instances}
    sel, gold, m = [], [], []
    for r in results:
        inst = by_qid.get(r.qid)
        if not inst or not r.ranking:
            continue
        sel.append(r.ranking[0] / max(1, inst.M - 1))
        gold.extend(g / max(1, inst.M - 1) for g in inst.gold_indices)
        m.append(inst.M)
    return {
        "mean_selected_relpos": mean(sel) if sel else None,
        "mean_gold_relpos": mean(gold) if gold else None,
        "mean_M": mean(m) if m else None,
        "n": len(sel),
    }
