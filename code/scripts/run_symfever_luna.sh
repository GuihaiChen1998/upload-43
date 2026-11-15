#!/usr/bin/env bash
# luna on S3AI is slow (~0.5 calls/s): primary evaluable set only (evidence_dep),
# cheap methods first, then RM64 (resumable per qid), no repeat-1.
set -u
cd "$(dirname "$0")/.."
set -a; . /home/claude/.mht_api.env; set +a
CFG=configs/models/closed/gpt-6-luna.yaml; NAME=gpt-6-luna
INST=data/constructed/symfever/symfever.all.jsonl.gz
echo "== $(date -u +%FT%TZ) $NAME screen"
python3 -u scripts/14_screen_closed.py --model $CFG --dataset symfever --instances $INST --workers 16 || exit 1
python3 scripts/27_symfever_evaluable.py --model $NAME || exit 1
KEEP=results/closed/screen/symfever/$NAME/symfever.all.evidence_dep.json
for M in V1 P1 LOI RM; do
  echo "== $(date -u +%FT%TZ) $NAME $M"
  python3 -u scripts/17_run_closed.py --model $CFG --dataset symfever --instances $INST --include-qids $KEEP \
    --methods $M --rm-k 64 --full-repeats 3 --tag main --outer-workers 8 --inner-workers 4 --sample-workers 2 || exit 1
done
echo "== $(date -u +%FT%TZ) $NAME ALL DONE"
