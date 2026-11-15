#!/usr/bin/env bash
# K3 pilot (design v2, construction v2 = filler bound to slot): premise screening at
# repeats 0-2, method evaluation at repeat 3 (V1, P1 + 3 matched-T full repeats, LOI, RM64).
#   MODEL=gpt-6-luna CONC=4 bash scripts/run_k3_pilot.sh
# Variants whose prompts are unchanged from construction v1 are served from the cache
# (v1 premise calls are reused, only the changed CF variants cost new calls).
# S3AI saturates at ~1 call/s (2026-11-01), so luna uses ~4 concurrent per dataset.
set -u
cd "$(dirname "$0")/.."
set -a; . /home/claude/.mht_api.env; set +a
MODEL=${MODEL:-gpt-6-luna}
CONC=${CONC:-4}
TAG=${TAG:-k3pilot_v2}
M=configs/models/closed/$MODEL.yaml
H=$(( CONC / 2 > 0 ? CONC / 2 : 1 ))
mkdir -p results/closed/raw/logs
for ds in hotpotqa musique; do
  I=data/constructed/k3/$ds.$MODEL.n50.v2.jsonl.gz
  ( python3 -u scripts/20_k3_premise.py --model $M --instances $I --workers $CONC --inner-workers 1
    python3 -u scripts/17_run_closed.py --model $M --dataset $ds --instances $I --methods V1,P1,LOI,RM \
      --rm-k 64 --full-repeats 3 --repeat 3 --tag $TAG --outer-workers $H --inner-workers 2 --sample-workers 2
  ) >> results/closed/raw/logs/$TAG.$MODEL.$ds.log 2>&1 &
done
wait
echo K3_PILOT_DONE
