"""Query-level cache.

The interventional pipeline issues O(M*N) calls per instance, so a run that
dies at 80% must not start over. Just as important: the cache stores RAW
responses, keyed on everything that affects generation but nothing that
affects aggregation. Re-sweeping lambda, beta or tau therefore costs zero
queries -- the observations are already on disk.

Key versions
------------
* legacy (v1, AAAI-27 runs): sha256 of {model, messages, temperature, sample_idx}.
  It omits the endpoint and decoding settings, so two endpoints serving the same
  model name, or a change of max_tokens / top_p / reasoning switches, would
  silently share responses. Kept only so the AAAI-27 cache can be replayed
  (`QueryCache(..., legacy_keys=True)`).
* v2 (default): additionally includes the backend fingerprint (endpoint,
  decoding settings, thinking switches) and a `repeat` index, so independent
  repeated measurements (e.g. stability checks) are never answered from cache.

Each v2 row also stores the fingerprint, per-call metadata (token usage,
latency, retries) and a timestamp, so cost and latency are reported from
records rather than estimated.
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import threading
import time


def _key(model: str, messages: list[dict], temperature: float, sample_idx: int,
         fingerprint: dict | None = None, repeat: int = 0, legacy: bool = False) -> str:
    payload = {
        "model": model,
        "messages": messages,
        "temperature": round(float(temperature), 6),
        "sample_idx": sample_idx,
    }
    if not legacy:
        payload["v"] = 2
        payload["fingerprint"] = fingerprint or {}
        payload["repeat"] = int(repeat)
    s = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class QueryCache:
    def __init__(self, path: str = "results/cache/queries.sqlite", enabled: bool = True,
                 legacy_keys: bool = False):
        self.enabled = enabled
        self.legacy_keys = legacy_keys
        self.hits = 0
        self.misses = 0
        self._lock = threading.Lock()
        if not enabled:
            self.conn = None
            return
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS cache ("
            "k TEXT PRIMARY KEY, response TEXT, model TEXT, temperature REAL)"
        )
        cols = {r[1] for r in self.conn.execute("PRAGMA table_info(cache)")}
        for col, typ in [("fingerprint", "TEXT"), ("meta", "TEXT"), ("created_at", "REAL"),
                         ("key_version", "INTEGER")]:
            if col not in cols:
                self.conn.execute(f"ALTER TABLE cache ADD COLUMN {col} {typ}")
        self.conn.commit()

    def _k(self, model, messages, temperature, sample_idx, fingerprint, repeat):
        return _key(model, messages, temperature, sample_idx, fingerprint, repeat,
                    legacy=self.legacy_keys)

    def get(self, model, messages, temperature, sample_idx,
            fingerprint: dict | None = None, repeat: int = 0) -> str | None:
        if not self.enabled:
            return None
        k = self._k(model, messages, temperature, sample_idx, fingerprint, repeat)
        with self._lock:
            row = self.conn.execute(
                "SELECT response FROM cache WHERE k=?", (k,)
            ).fetchone()
        if row:
            self.hits += 1
            return row[0]
        self.misses += 1
        return None

    def put(self, model, messages, temperature, sample_idx, response: str,
            fingerprint: dict | None = None, repeat: int = 0, meta: dict | None = None) -> None:
        if not self.enabled:
            return
        k = self._k(model, messages, temperature, sample_idx, fingerprint, repeat)
        with self._lock:
            self.conn.execute(
                "INSERT OR REPLACE INTO cache "
                "(k, response, model, temperature, fingerprint, meta, created_at, key_version) "
                "VALUES (?,?,?,?,?,?,?,?)",
                (k, response, model, float(temperature),
                 json.dumps(fingerprint or {}, sort_keys=True, default=str),
                 json.dumps(meta or {}, sort_keys=True, default=str),
                 time.time(), 1 if self.legacy_keys else 2),
            )
            self.conn.commit()

    def usage_summary(self) -> dict:
        """Aggregate recorded token usage / latency over v2 rows, per model."""
        if not self.enabled:
            return {}
        out: dict[str, dict] = {}
        with self._lock:
            rows = self.conn.execute(
                "SELECT model, meta FROM cache WHERE key_version=2"
            ).fetchall()
        for model, meta in rows:
            m = json.loads(meta or "{}")
            s = out.setdefault(model, {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0,
                                       "reasoning_tokens": 0, "latency_s": 0.0})
            s["calls"] += 1
            for f in ("prompt_tokens", "completion_tokens", "reasoning_tokens"):
                s[f] += m.get(f) or 0
            s["latency_s"] += m.get("latency_s") or 0.0
        return out

    @property
    def stats(self) -> dict:
        total = self.hits + self.misses
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": self.hits / total if total else 0.0,
        }

    def close(self) -> None:
        if self.conn:
            self.conn.close()
