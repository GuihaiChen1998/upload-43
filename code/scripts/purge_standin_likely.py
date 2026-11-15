#!/usr/bin/env python3
"""Delete self-probing second-turn ("likely") answers that a stand-in endpoint wrote
into the shared query cache (round 24, haiku split run).

The ggwk1 stand-in for tian-shu shares tian-shu's cache fingerprint
(`fingerprint_base_url`), so its first-turn answers are reused by design. Its
second-turn `likely` answers are not: ggwk1 says "no" far more often than tian-shu,
and V4/V5/P5 weight samples by `likely`. Run this before tian-shu runs P4/P5 (the
P4 baseline's second turn has the same cache key as P3's, which ggwk1 ran).

  python scripts/purge_standin_likely.py --model claude-haiku-5-5 \
      --served-base-url https://www.ggwk1.online/v1 [--dry-run]
"""
import argparse
import json
import os
import sqlite3

ROOT = os.path.join(os.path.dirname(__file__), "..")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--served-base-url", required=True)
    ap.add_argument("--db", default=os.path.join(ROOT, "results", "cache", "closed.sqlite"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    c = sqlite3.connect(a.db, timeout=60)
    rows = c.execute(
        "select k, response, meta from cache where model=? and response like '%\"likely\"%'",
        (a.model,)).fetchall()
    ks = []
    for k, resp, meta in rows:
        try:
            m = json.loads(meta or "{}")
        except json.JSONDecodeError:
            continue
        if m.get("served_base_url") == a.served_base_url:
            ks.append(k)
    print(f"{len(ks)} likely rows served by {a.served_base_url} (of {len(rows)} likely rows)")
    if ks and not a.dry_run:
        c.executemany("delete from cache where k=?", [(k,) for k in ks])
        c.commit()
        print("deleted")


if __name__ == "__main__":
    main()
