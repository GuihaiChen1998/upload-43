#!/usr/bin/env bash
# Watchdog helper for the A+ grid: rows per file vs. expected questions, live runners, recent errors.
cd "$(dirname "$0")/.."
for tag in grid_sub grid; do
  for d in results/closed/raw/*/*/$tag; do
    [ -d "$d" ] || continue
    exp=$(python3 -c "import json,sys; print(len(json.load(open(sys.argv[1]))))" "$d/qids.json" 2>/dev/null)
    line="$d (expect $exp):"
    for f in "$d"/*.jsonl; do [ -e "$f" ] && line="$line $(basename "$f" .jsonl)=$(wc -l <"$f")"; done
    echo "$line"
  done
done
echo "--- runners alive:"
pgrep -af 'bash scripts/run_grid.sh' | sed 's#.*run_grid.sh#run_grid.sh#' || echo "(none)"
echo "--- line ends:"; grep -h GRID_LINE_END results/closed/raw/logs/grid_*.log 2>/dev/null
echo "--- recent errors (last 3 per log):"
for l in results/closed/raw/logs/grid_*.log; do
  n=$(grep -c '  ! ' "$l"); [ "$n" -gt 0 ] && { echo "$l: $n errors"; grep '  ! ' "$l" | tail -3 | cut -c1-200; }
done
