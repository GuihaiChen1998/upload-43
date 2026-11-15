#!/usr/bin/env python3
"""Restore the API query cache (code/results/cache/closed.sqlite, gitignored, ~0.9 GB) from the
`cache-snapshots` branch, where it is stored zstd-compressed and split into <100 MB parts.

  pip install --break-system-packages zstandard
  python scripts/restore_cache.py [--snapshot 2026-11-04] [--force]

Without the cache, analyses still work (they read results/closed/raw/*.jsonl), but resuming or
extending runs would re-issue API calls that were already paid for.
"""
import argparse
import glob
import hashlib
import os
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO = os.path.abspath(os.path.join(ROOT, ".."))
DST = os.path.join(ROOT, "results", "cache", "closed.sqlite")


def git(*a, cwd=REPO):
    return subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", default=None, help="folder on the cache-snapshots branch (default: latest)")
    ap.add_argument("--force", action="store_true", help="overwrite an existing cache")
    a = ap.parse_args()
    if os.path.exists(DST) and not a.force:
        sys.exit(f"{DST} exists; pass --force to overwrite")
    import zstandard
    git("fetch", "-q", "origin", "cache-snapshots")
    with tempfile.TemporaryDirectory() as tmp:
        wt = os.path.join(tmp, "wt")
        git("worktree", "add", "-q", "--detach", wt, "FETCH_HEAD")
        try:
            snaps = sorted(d for d in os.listdir(wt) if d[:2] == "20" and os.path.isdir(os.path.join(wt, d)))
            snap = a.snapshot or snaps[-1]
            parts = sorted(glob.glob(os.path.join(wt, snap, "closed.sqlite.zst.part*")))
            want = open(os.path.join(wt, snap, "SHA256SUMS")).read().split()[0]
            zst = os.path.join(tmp, "closed.sqlite.zst")
            h = hashlib.sha256()
            with open(zst, "wb") as fo:
                for p in parts:
                    b = open(p, "rb").read()
                    h.update(b)
                    fo.write(b)
            if h.hexdigest() != want:
                sys.exit("sha256 mismatch: snapshot parts are corrupt")
            os.makedirs(os.path.dirname(DST), exist_ok=True)
            with open(zst, "rb") as fi, open(DST + ".tmp", "wb") as fo:
                zstandard.ZstdDecompressor().copy_stream(fi, fo)
            os.replace(DST + ".tmp", DST)
        finally:
            git("worktree", "remove", "--force", wt)
    import sqlite3
    n = sqlite3.connect(DST).execute("select count(*) from cache").fetchone()[0]
    print(f"restored snapshot {snap}: {os.path.getsize(DST) // 2**20} MB, {n} cached responses -> {DST}")


if __name__ == "__main__":
    main()
