# Response-cache snapshots (not code)

zstd-compressed snapshot of `code/results/cache/closed.sqlite`, the content-addressed response cache
behind every run reported in the paper (gitignored on `main` because it is ~1.4 GB). The file is the
original cache, unmodified; no API keys inside (checked). Restore on `main` with:

    pip install zstandard
    python code/scripts/restore_cache.py                         # latest snapshot
    python code/scripts/restore_cache.py --snapshot 2026-11-15

- 2026-11-15: 1,503,800 responses (1.39 GB -> 215 MB, 3 parts). SHA256SUMS holds the hash of the
  concatenated `.zst`; `restore_cache.py` checks it before decompressing.
