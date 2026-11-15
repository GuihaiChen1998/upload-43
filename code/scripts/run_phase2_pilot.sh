#!/usr/bin/env bash
# Phase-2 pilot: full method grid + RM(K=64) + LOI on a small hop-stratified
# subset per model x dataset, to measure cost per instance and tune K.
# Main models: 12 instances; capability tier: 6. P* with 3 matched-T full repeats;
# V1/P1 also repeat 1 (run-to-run stability).
set -u
cd "$(dirname "$0")/.."
set -a; . /home/claude/.mht_api.env; set +a
ALL=V1,V2,V3,V4,V5,V6,V7,P1,P2,P3,P4,P5,RM,LOI
run() {  # model n ds
  local m=$1 n=$2 ds=$3
  python3 -u scripts/17_run_closed.py --model configs/models/closed/$m.yaml --dataset $ds \
    --methods $ALL --sample-n $n --tag pilot --rm-k 64 --full-repeats 3 --outer-workers 3 --inner-workers 3 --sample-workers 5
  python3 -u scripts/17_run_closed.py --model configs/models/closed/$m.yaml --dataset $ds \
    --methods V1,P1 --sample-n $n --tag pilot --full-repeats 3 --repeat 1 --outer-workers 3 --inner-workers 3 --sample-workers 5
}
mkdir -p results/closed/raw/logs
for m in claude-haiku-5-5 gpt-6-luna gemini-2.5-flash-lite; do
  for ds in hotpotqa musique; do run $m 12 $ds >> results/closed/raw/logs/pilot.$m.$ds.log 2>&1 & done
done
for m in gemini-2.5-flash gpt-6.1-terra; do
  for ds in hotpotqa musique; do run $m 6 $ds >> results/closed/raw/logs/pilot.$m.$ds.log 2>&1 & done
done
wait
echo PILOT_DONE
