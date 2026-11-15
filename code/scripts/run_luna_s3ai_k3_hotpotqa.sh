#!/usr/bin/env bash
# Round 23 addendum: K3 luna HotpotQA methods on S3AI (same endpoint as the K3 premise and all
# HotpotQA luna main runs). The BootToken runner's later hotpotqa K3 call then stops at the
# manifest fingerprint check (no mixing) and proceeds to MuSiQue K3. Resumable.
#   bash scripts/run_luna_s3ai_k3_hotpotqa.sh
set -u
cd "$(dirname "$0")/.."
set -a; . /home/claude/.mht_api.env; set +a
M=configs/models/closed/gpt-6-luna.yaml
W="--outer-workers 4 --inner-workers 2 --sample-workers 1"
mkdir -p results/closed/raw/logs
{
python3 -u scripts/17_run_closed.py --model $M --dataset hotpotqa --instances data/constructed/k3/hotpotqa.gpt-6-luna.n50.v2.jsonl.gz \
  --methods V1,P1,LOI,RM --rm-k 64 --full-repeats 3 --repeat 3 --tag k3pilot_v2 $W
echo LUNA_S3AI_K3_HOTPOTQA_DONE
} >> results/closed/raw/logs/luna_s3ai_k3_hotpotqa.log 2>&1
