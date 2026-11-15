#!/usr/bin/env bash
# Qasper single-hop extension for one model (resumable: re-run the same command).
#   bash scripts/run_qasper.sh <model.yaml> <pilot|main> <screen_workers> <outer> <inner> <sample> [methods] [repeat1_methods]
# pilot: screen a seeded 40-question subset, then methods on <= 8 evaluable questions (tag pilot).
# main : screen all 478 (pilot calls are cache hits), methods on every evaluable question (tag main);
#        analyses drop the pilot qids (test split), as for HotpotQA / MuSiQue.
set -u
cd "$(dirname "$0")/.."
set -a; . /home/claude/.mht_api.env; set +a
CFG=$1; MODE=$2; SW=$3; OW=$4; IW=$5; SPW=$6; METHODS=${7:-V1,P1,LOI,RM}; R1=${8:-}
NAME=$(python3 -c "import yaml,sys;print(yaml.safe_load(open('$CFG'))['name'])")
INST=data/constructed/qasper/qasper.all.jsonl.gz
if [ "$MODE" = pilot ]; then LIM="--limit 40"; SCR=results/closed/screen/qasper/$NAME/qasper.all.limit40.jsonl; EXTRA="--sample-n 8"; TAG=pilot
else LIM=""; SCR=results/closed/screen/qasper/$NAME/qasper.all.jsonl; EXTRA=""; TAG=main; fi
echo "== $(date -u +%FT%TZ) $NAME qasper screen ($MODE)"
python3 -u scripts/14_screen_closed.py --model "$CFG" --dataset qasper --instances $INST $LIM --workers "$SW" || exit 1
echo "== $(date -u +%FT%TZ) $NAME qasper methods $METHODS ($TAG)"
python3 -u scripts/17_run_closed.py --model "$CFG" --dataset qasper --instances $INST --include-qids $SCR $EXTRA \
  --methods "$METHODS" --rm-k 64 --full-repeats 3 --tag $TAG --outer-workers "$OW" --inner-workers "$IW" --sample-workers "$SPW" || exit 1
if [ -n "$R1" ]; then
  echo "== $(date -u +%FT%TZ) $NAME qasper repeat-1 $R1"
  python3 -u scripts/17_run_closed.py --model "$CFG" --dataset qasper --instances $INST --include-qids $SCR $EXTRA \
    --methods "$R1" --full-repeats 3 --repeat 1 --tag $TAG --outer-workers "$OW" --inner-workers "$IW" --sample-workers "$SPW" || exit 1
fi
echo "== $(date -u +%FT%TZ) $NAME qasper $MODE DONE"
