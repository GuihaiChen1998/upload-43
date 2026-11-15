#!/usr/bin/env bash
# luna on Symmetric FEVER, split across endpoints by qid shard (round 28, user: S3AI + boottoken ~half each).
# Both configs fingerprint as S3AI (boottoken via gpt-6-luna@boottoken-s3fp.yaml), so they share the S3AI
# manifest, output files and response cache; each call records its served_base_url.
#   bash scripts/run_symfever_luna_split.sh configs/models/closed/gpt-6-luna.yaml 0,1,2,3,4,5,6,7,8/20 8 4
#   bash scripts/run_symfever_luna_split.sh configs/models/closed/gpt-6-luna.yaml 9,...,19/20 8 4
set -u
cd "$(dirname "$0")/.."
set -a; . /home/claude/.mht_api.env; set +a
CFG=$1; SHARD=$2; OUTER=${3:-8}; INNER=${4:-4}; NAME=gpt-6-luna
INST=data/constructed/symfever/symfever.all.jsonl.gz
KEEP=results/closed/screen/symfever/$NAME/symfever.all.evidence_dep.json
for M in V1 P1 LOI RM; do
  echo "== $(date -u +%FT%TZ) $NAME $M shard $SHARD $(basename $CFG)"
  python3 -u scripts/17_run_closed.py --model $CFG --dataset symfever --instances $INST --include-qids $KEEP \
    --methods $M --rm-k 64 --full-repeats 3 --tag main --outer-workers $OUTER --inner-workers $INNER \
    --sample-workers 2 --shard $SHARD || exit 1
done
echo "== $(date -u +%FT%TZ) $NAME shard $SHARD ALL DONE"
