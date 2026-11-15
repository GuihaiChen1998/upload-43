#!/usr/bin/env bash
# Round 23: luna split by dataset across endpoints. HotpotQA stays entirely on S3AI
# (V1/P1/LOI already done there): V1/P1 repeat 1, then RM64. Resumable.
#   bash scripts/run_luna_s3ai_hotpotqa.sh
set -u
cd "$(dirname "$0")/.."
set -a; . /home/claude/.mht_api.env; set +a
M=configs/models/closed/gpt-6-luna.yaml
W="--outer-workers 4 --inner-workers 2 --sample-workers 1"
mkdir -p results/closed/raw/logs
{
python3 -u scripts/17_run_closed.py --model $M --dataset hotpotqa --methods V1,P1 --full-repeats 3 --repeat 1 --tag main $W
python3 -u scripts/17_run_closed.py --model $M --dataset hotpotqa --methods RM --rm-k 64 --tag main $W
echo LUNA_S3AI_HOTPOTQA_DONE
} >> results/closed/raw/logs/luna_s3ai_hotpotqa.log 2>&1
