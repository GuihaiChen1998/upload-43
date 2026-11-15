#!/usr/bin/env bash
# K3 premise screening only (repeats 0-2), both datasets, construction v2.
#   MODEL=gpt-6-luna CONC=4 bash scripts/run_k3_premise.sh
set -u
cd "$(dirname "$0")/.."
set -a; . /home/claude/.mht_api.env; set +a
MODEL=${MODEL:-gpt-6-luna}; CONC=${CONC:-4}
mkdir -p results/closed/raw/logs
for ds in hotpotqa musique; do
  python3 -u scripts/20_k3_premise.py --model configs/models/closed/$MODEL.yaml \
    --instances data/constructed/k3/$ds.$MODEL.n50.v2.jsonl.gz --workers $CONC --inner-workers 1 \
    >> results/closed/raw/logs/k3premise_v2.$MODEL.$ds.log 2>&1 &
done
wait
echo K3_PREMISE_DONE
