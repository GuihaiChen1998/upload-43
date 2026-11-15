#!/usr/bin/env bash
# Phase-2 main run, plan A (user decision 2026-11-02, round 22): full evaluable set
# (main models: union pool, tier: intersection pool), methods V1, P1 (+3 matched-T full
# repeats), LOI, RM (K=64), plus V1/P1 repeat 1. MExGen-LOO is re-scored from P1 offline.
# Pilot rows are reused through the shared cache. Resumable (per-method output files).
#   bash scripts/run_phase2_main.sh                  # all non-luna models in parallel
#   MODELS="gemini-2.5-flash-lite" bash scripts/run_phase2_main.sh
set -u
cd "$(dirname "$0")/.."
set -a; . /home/claude/.mht_api.env; set +a
MODELS=${MODELS:-"claude-haiku-5-5 gemini-2.5-flash-lite gemini-2.5-flash gpt-6.1-terra"}
TAG=${TAG:-main}
mkdir -p results/closed/raw/logs
workers() {  # model -> "outer inner sample"
  case $1 in
    claude-haiku-5-5)      echo "6 4 2" ;;
    gemini-2.5-flash-lite) echo "6 4 2" ;;
    *)                     echo "4 3 2" ;;   # flash / terra share the xiaojingai endpoint with lite
  esac
}
run() {  # model ds
  local m=$1 ds=$2; read -r o i s <<<"$(workers $m)"
  local M=configs/models/closed/$m.yaml
  python3 -u scripts/17_run_closed.py --model $M --dataset $ds --methods V1,P1,LOI \
    --full-repeats 3 --tag $TAG --outer-workers $o --inner-workers $i --sample-workers $s
  python3 -u scripts/17_run_closed.py --model $M --dataset $ds --methods V1,P1 \
    --full-repeats 3 --repeat 1 --tag $TAG --outer-workers $o --inner-workers $i --sample-workers $s
  python3 -u scripts/17_run_closed.py --model $M --dataset $ds --methods RM --rm-k 64 \
    --tag $TAG --outer-workers $o --inner-workers $i --sample-workers $s
  echo "MAIN_DONE $m $ds"
}
for m in $MODELS; do
  for ds in hotpotqa musique; do run $m $ds >> results/closed/raw/logs/$TAG.$m.$ds.log 2>&1 & done
done
wait
echo PHASE2_MAIN_DONE
