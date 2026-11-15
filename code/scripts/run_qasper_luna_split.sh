#!/usr/bin/env bash
# luna on Qasper (main), methods split across endpoints by qid shard (round 29, user: S3AI + 元衡 + boottoken).
# Screening runs on S3AI first (bash scripts/run_qasper.sh ... is NOT used for luna main); every stand-in config
# fingerprints as S3AI, so all shards share the S3AI manifest, output files and cache.
#   bash scripts/run_qasper_luna_split.sh <cfg> <shard> [outer inner]
set -u
cd "$(dirname "$0")/.."
set -a; . /home/claude/.mht_api.env; set +a
CFG=$1; SHARD=$2; OUTER=${3:-8}; INNER=${4:-4}; NAME=gpt-6-luna
INST=data/constructed/qasper/qasper.all.jsonl.gz
SCR=results/closed/screen/qasper/$NAME/qasper.all.jsonl
for M in V1 P1 LOI RM; do
  echo "== $(date -u +%FT%TZ) $NAME qasper $M shard $SHARD $(basename $CFG)"
  python3 -u scripts/17_run_closed.py --model $CFG --dataset qasper --instances $INST --include-qids $SCR \
    --methods $M --rm-k 64 --full-repeats 3 --tag main --outer-workers $OUTER --inner-workers $INNER \
    --sample-workers 2 --shard $SHARD || exit 1
done
echo "== $(date -u +%FT%TZ) $NAME qasper shard $SHARD ALL DONE"
