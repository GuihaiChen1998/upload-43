#!/usr/bin/env python3
"""Build the Symmetric-FEVER fact-verification extension (zero model calls).

Source data (all pinned; see data/raw/symfever/PROVENANCE.md):
  * Symmetric FEVER v0.2 (Schuster et al., 2019), dev/test JSONL, commit fa25d17.
    Each row is (claim, ONE evidence sentence, SUPPORTS|REFUTES). Rows come in
    families of four: original claim C with original evidence E, plus the
    synthetic C' and E' (ids = original id + 7-digit suffix), so that
    (C,E),(C,E'),(C',E),(C',E') carry opposite labels pairwise.
  * Official FEVER shared_task_dev.jsonl: page names and sentence ids of every
    annotated evidence set of the ORIGINAL claim (used for titles and to keep
    alternative evidence out of the distractors).
  * FEVER 2017 Wikipedia dump (wiki-pages.zip), reduced to the 324 pages those
    evidence sets touch (wiki_subset.jsonl.gz).

Instance construction (one instance per Symmetric row):
  * M = 10 numbered sentences, each rendered with its page title.
  * Gold = the row's own evidence sentence (E or E'), exactly one gold source.
  * Distractors: up to N_SAME sentences from the gold sentence's page that are
    NOT in any annotated evidence set of the original claim, plus sentences
    from pages of other families (never a page the family itself touches).
  * The four rows of a family share the distractors and the slot layout; only
    the gold slot's text (E vs E') and the claim (C vs C') differ. Gold slots are
    random across families (seeded by family id).
  * Question asks for a verdict answerable as yes / no / unknown, so the
    instance goes through the unchanged QA pipeline: gold answer "yes" for
    SUPPORTS, "no" for REFUTES; removing the gold sentence should move a
    context-faithful model to "unknown" (which the screening code already
    treats as an abstention).

  python scripts/26_build_symfever.py --symfever-dir <FeverSymmetric checkout> \
      --fever-dev <shared_task_dev.jsonl> --wiki-subset <wiki_subset.jsonl.gz>
"""
from __future__ import annotations

import argparse
import collections
import difflib
import gzip
import hashlib
import json
import os
import random
import re
import sys
import unicodedata

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
from src.data.schema import Instance, Source  # noqa: E402

M = 10
N_SAME = 3
MIN_TOKENS = 6
QUESTION = ('Is the following claim true according to the sources? Claim: "{claim}" '
            'Answer "yes" if the sources support the claim, "no" if they contradict it, '
            'or "unknown" if they do not contain enough information.')

_TOK = {"-LRB-": "(", "-RRB-": ")", "-LSB-": "[", "-RSB-": "]", "-LCB-": "{", "-RCB-": "}",
        "``": '"', "''": '"', "--": "–"}


def detok(s: str) -> str:
    """Undo FEVER/PTB tokenisation for display (keeps the words unchanged)."""
    for k, v in _TOK.items():
        s = s.replace(k, v)
    s = re.sub(r"\s+([,.;:!?%)\]}])", r"\1", s)
    s = re.sub(r"([(\[{])\s+", r"\1", s)
    s = re.sub(r"\s+'s\b", "'s", s)
    s = re.sub(r"\s+n't\b", "n't", s)
    s = re.sub(r'"\s+(.*?)\s+"', r'"\1"', s)
    return re.sub(r"\s+", " ", s).strip()


def title_of(page: str) -> str:
    return detok(page.replace("_", " "))


def key(s: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s)).strip().lower()


def page_lines(rec) -> dict[int, str]:
    out = {}
    for ln in rec["lines"].split("\n"):
        parts = ln.split("\t")
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].strip():
            out[int(parts[0])] = parts[1].strip()
    return out


def family_of(rid: str) -> str:
    return rid[:-7] if len(rid) >= 8 and rid[-7:-1] == "000000" else rid


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symfever-dir", required=True)
    ap.add_argument("--fever-dev", required=True)
    ap.add_argument("--wiki-subset", required=True)
    ap.add_argument("--out-dir", default=os.path.join(ROOT, "data", "constructed", "symfever"))
    ap.add_argument("--seed", type=int, default=20261104)
    args = ap.parse_args()

    dev = {}
    for l in open(args.fever_dev, encoding="utf-8"):
        r = json.loads(l)
        dev[r["id"]] = r
    wiki = {}
    with gzip.open(args.wiki_subset, "rt", encoding="utf-8") as f:
        for l in f:
            r = json.loads(l)
            wiki[unicodedata.normalize("NFC", r["id"])] = page_lines(r)

    splits = {}
    for sp in ["dev", "test"]:
        p = os.path.join(args.symfever_dir, "symmetric_v0.2", f"fever_symmetric_{sp}.jsonl")
        splits[sp] = [json.loads(l) for l in open(p, encoding="utf-8")]

    # --- per-family facts: pages touched, annotated evidence, the gold line ---------------
    fams = {}
    for sp, rows in splits.items():
        g = collections.defaultdict(list)
        for r in rows:
            g[family_of(r["id"])].append(r)
        for fid, rs in g.items():
            assert len(rs) == 4, (sp, fid, len(rs))
            d = dev[int(fid)]
            ev = {(unicodedata.normalize("NFC", e[2]), e[3]) for es in d["evidence"] for e in es if e[2]}
            orig = next(r for r in rs if r["id"] == fid)
            # locate the original evidence sentence among the annotated lines
            # (Symmetric FEVER re-tokenised some quotes, so use a near-exact match: the most
            #  similar annotated line, then any line of a touched page, at ratio >= 0.9.)
            def best(cands):
                sc = [(difflib.SequenceMatcher(None, key(t), key(orig["evidence"])).ratio(), pi)
                      for pi, t in cands]
                sc = [x for x in sc if x[0] >= 0.9]
                return [max(sc)[1]] if sc else []
            hit = best([((p, i), wiki[p].get(i, "")) for p, i in ev if p in wiki])
            if not hit:
                hit = best([((p, i), t) for p in {p for p, _ in ev} if p in wiki for i, t in wiki[p].items()])
            fams[fid] = {"split": sp, "rows": rs, "evidence": ev, "pages": {p for p, _ in ev},
                         "gold": hit[0] if hit else None, "orig_evidence": orig["evidence"]}

    unmatched = [f for f, v in fams.items() if v["gold"] is None]
    print(f"families {len(fams)}; gold line not located in dump: {len(unmatched)} {unmatched[:8]}")

    # --- distractor pools ---------------------------------------------------------------
    def ok(t):
        return len(t.split()) >= MIN_TOKENS

    all_lines = [(p, i, t) for p, ls in wiki.items() for i, t in ls.items() if ok(t)]
    os.makedirs(args.out_dir, exist_ok=True)
    stats = collections.Counter()
    out = {"dev": [], "test": []}
    for fid in sorted(fams, key=int):
        F = fams[fid]
        if F["gold"] is None:
            stats["dropped_family_no_gold_line"] += 1
            continue
        rng = random.Random(f"{args.seed}:{fid}")
        gpage, gline = F["gold"]
        banned_text = {key(r["evidence"]) for r in F["rows"]}
        same = [(gpage, i, t) for i, t in sorted(wiki[gpage].items())
                if (gpage, i) not in F["evidence"] and ok(t) and key(t) not in banned_text]
        same = rng.sample(same, min(N_SAME, len(same)))
        other = [x for x in all_lines if x[0] not in F["pages"] and key(x[2]) not in banned_text]
        other_pages = sorted({x[0] for x in other})
        pick_pages = rng.sample(other_pages, M - 1 - len(same))
        others = []
        for p in pick_pages:  # one sentence per other page
            cand = [x for x in other if x[0] == p]
            others.append(rng.choice(cand))
        distract = same + others
        rng.shuffle(distract)
        gslot = rng.randrange(M)
        stats[f"n_same_page={len(same)}"] += 1
        for r in sorted(F["rows"], key=lambda r: r["id"]):
            srcs, k = [], 0
            for slot in range(M):
                if slot == gslot:
                    srcs.append(Source(idx=slot, title=title_of(gpage), text=detok(r["evidence"]), is_gold=True))
                else:
                    p, _, t = distract[k]
                    k += 1
                    srcs.append(Source(idx=slot, title=title_of(p), text=detok(t), is_gold=False))
            is_orig_c = r["claim"] == next(x for x in F["rows"] if x["id"] == fid)["claim"]
            is_orig_e = key(r["evidence"]) == key(F["orig_evidence"])
            lab = r["gold_label"]
            inst = Instance(
                qid=f"symfever_{r['id']}", question=QUESTION.format(claim=detok(r["claim"])),
                answer="yes" if lab == "SUPPORTS" else "no", sources=srcs, dataset="symfever",
                n_hop=None, answer_aliases=[],
                meta={"family": fid, "split": F["split"], "label": lab, "orig_claim": is_orig_c,
                      "orig_evidence": is_orig_e, "gold_slot": gslot, "n_same_page": len(same),
                      "gold_page": gpage, "gold_line": gline, "symfever_id": r["id"]})
            out[F["split"]].append(inst)
            stats[f"{F['split']}:{lab}"] += 1
            stats[f"{F['split']}:claim={'C' if is_orig_c else 'C2'},evid={'E' if is_orig_e else 'E2'}"] += 1

    for sp, insts in out.items():
        path = os.path.join(args.out_dir, f"symfever.{sp}.jsonl.gz")
        with gzip.open(path, "wt", encoding="utf-8") as f:
            for i in insts:
                f.write(json.dumps(i.to_json(), ensure_ascii=False) + "\n")
        print(f"wrote {len(insts)} -> {path}")
    prov = {"seed": args.seed, "M": M, "n_same_page_max": N_SAME, "min_tokens": MIN_TOKENS,
            "question_template": QUESTION, "stats": dict(sorted(stats.items())),
            "unmatched_families": unmatched,
            "inputs_sha256": {
                "fever_symmetric_dev.jsonl": sha256(os.path.join(args.symfever_dir, "symmetric_v0.2", "fever_symmetric_dev.jsonl")),
                "fever_symmetric_test.jsonl": sha256(os.path.join(args.symfever_dir, "symmetric_v0.2", "fever_symmetric_test.jsonl")),
                "shared_task_dev.jsonl": sha256(args.fever_dev),
                "wiki_subset.jsonl.gz": sha256(args.wiki_subset)}}
    with open(os.path.join(args.out_dir, "build_info.json"), "w") as f:
        json.dump(prov, f, indent=1, ensure_ascii=False)
    print(json.dumps(prov["stats"], indent=1))


if __name__ == "__main__":
    main()
