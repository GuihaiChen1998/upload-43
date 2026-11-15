#!/usr/bin/env bash
# Symmetric-FEVER full run for one model (resumable: re-run the same command).
#   bash scripts/run_symfever.sh <model.yaml> <methods> <screen_workers> <outer> <inner> <sample> [repeat1_methods]
# 1) screen all 1420 instances  2) evaluable sets  3) methods on full-correct rows (repeat 0)
# 4) optional repeat-1 methods (e.g. V1,P1) as in the main experiment.
set -u
cd "$(dirname "$0")/.."
set -a; . /home/claude/.mht_api.env; set +a
CFG=$1; METHODS=$2; SW=$3; OW=$4; IW=$5; SPW=$6; R1=${7:-}
NAME=$(python3 -c "import yaml,sys;print(yaml.safe_load(open('$CFG'))['name'])")
INST=data/constructed/symfever/symfever.all.jsonl.gz
echo "== $(date -u +%FT%TZ) $NAME screen"
python3 -u scripts/14_screen_closed.py --model "$CFG" --dataset symfever --instances $INST --workers "$SW" || exit 1
python3 scripts/27_symfever_evaluable.py --model "$NAME" || exit 1
KEEP=results/closed/screen/symfever/$NAME/symfever.all.full_correct.json
echo "== $(date -u +%FT%TZ) $NAME methods $METHODS"
python3 -u scripts/17_run_closed.py --model "$CFG" --dataset symfever --instances $INST --include-qids $KEEP \
  --methods "$METHODS" --rm-k 64 --full-repeats 3 --tag main --outer-workers "$OW" --inner-workers "$IW" --sample-workers "$SPW" || exit 1
if [ -n "$R1" ]; then
  echo "== $(date -u +%FT%TZ) $NAME repeat-1 $R1"
  python3 -u scripts/17_run_closed.py --model "$CFG" --dataset symfever --instances $INST --include-qids $KEEP \
    --methods "$R1" --full-repeats 3 --repeat 1 --tag main --outer-workers "$OW" --inner-workers "$IW" --sample-workers "$SPW" || exit 1
fi
echo "== $(date -u +%FT%TZ) $NAME ALL DONE"
