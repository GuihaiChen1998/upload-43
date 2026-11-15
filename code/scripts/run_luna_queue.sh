#!/usr/bin/env bash
# Single serial luna queue (S3AI saturates near 1 call/s; ~8 concurrent in total).
# Order: cheap plan-A methods first, then RM, then K3 method phase. Resumable.
# Whether luna RM is cut to <=200 hop-stratified questions per dataset is still open;
# RM is last so that decision can be taken before it starts.
#   bash scripts/run_luna_queue.sh
set -u
cd "$(dirname "$0")/.."
set -a; . /home/claude/.mht_api.env; set +a
M=configs/models/closed/gpt-6-luna.yaml
L=results/closed/raw/logs/luna_queue.log
W="--outer-workers 4 --inner-workers 2 --sample-workers 1"
mkdir -p results/closed/raw/logs
{
for ds in hotpotqa musique; do
  python3 -u scripts/17_run_closed.py --model $M --dataset $ds --methods V1,P1,LOI --full-repeats 3 --tag main $W
done
for ds in hotpotqa musique; do
  python3 -u scripts/17_run_closed.py --model $M --dataset $ds --methods V1,P1 --full-repeats 3 --repeat 1 --tag main $W
done
echo "LUNA_CHEAP_DONE"
for ds in hotpotqa musique; do
  python3 -u scripts/17_run_closed.py --model $M --dataset $ds --methods RM --rm-k 64 --tag main $W
done
echo "LUNA_RM_DONE"
for ds in hotpotqa musique; do
  python3 -u scripts/17_run_closed.py --model $M --dataset $ds --instances data/constructed/k3/$ds.gpt-6-luna.n50.v2.jsonl.gz \
    --methods V1,P1,LOI,RM --rm-k 64 --full-repeats 3 --repeat 3 --tag k3pilot_v2 $W
done
echo "LUNA_QUEUE_DONE"
} >> $L 2>&1
