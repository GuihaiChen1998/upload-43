#!/usr/bin/env bash
# Round 24: plan A+ grid (V2-V7, P2-P5; V5/P5 are derived from V4/P4 at zero cost).
#   sub  = tag grid_sub: hop-stratified <=200 questions per dataset, drawn after leaving out the
#          pilot (dev) questions, so the subsample is part of the test split;
#   full = tag grid: the whole evaluable set. Questions already run in grid_sub (and the pilot
#          questions, which ran all 12 methods) are replayed from the query cache with zero API
#          calls (cache key = prompt + endpoint fingerprint + repeat, not the tag), so going from
#          sub to full only pays for the new questions.
# Resumable: rerun the same command after an interruption; failed questions are retried.
#   bash scripts/run_grid.sh <model.yaml> <datasets: hotpotqa,musique> <methods> <phases: sub,full> \
#        <log-name> [outer inner sample]
set -u
cd "$(dirname "$0")/.."
set -a; . /home/claude/.mht_api.env; set +a
M=$1; DSS=$2; METHODS=$3; PHASES=$4; LOG=$5
W="--outer-workers ${6:-6} --inner-workers ${7:-4} --sample-workers ${8:-2}"
NAME=$(python3 -c "import yaml,sys; print(yaml.safe_load(open(sys.argv[1]))['name'])" "$M")
mkdir -p results/closed/raw/logs
{
echo "=== $(date -u +%FT%TZ) start $NAME $DSS $METHODS $PHASES"
for ph in ${PHASES//,/ }; do
  for ds in ${DSS//,/ }; do
    if [ "$ph" = sub ]; then
      python3 -u scripts/17_run_closed.py --model "$M" --dataset "$ds" --methods "$METHODS" --full-repeats 3 \
        --sample-n 200 --exclude-qids "results/closed/raw/$ds/$NAME/pilot/qids.json" --tag grid_sub $W \
        && echo "GRID_DONE sub $NAME $ds $METHODS"
    else
      python3 -u scripts/17_run_closed.py --model "$M" --dataset "$ds" --methods "$METHODS" --full-repeats 3 \
        --tag grid $W && echo "GRID_DONE full $NAME $ds $METHODS"
    fi
  done
done
echo "GRID_LINE_END $NAME $DSS $METHODS $PHASES"
} >> "results/closed/raw/logs/$LOG.log" 2>&1
