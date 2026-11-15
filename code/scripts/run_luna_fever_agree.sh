#!/usr/bin/env bash
# Cross-endpoint agreement trial for luna on Symmetric FEVER (round 28): P1 on 30 evidence-dependent
# qids already done on S3AI, re-run with a FRESH reference on another endpoint (own fingerprint, own tag).
set -u
cd "$(dirname "$0")/.."
set -a; . /home/claude/.mht_api.env; set +a
EP=$1   # zhihui | boottoken
python3 -u scripts/17_run_closed.py --model configs/models/closed/gpt-6-luna@$EP.yaml --dataset symfever \
  --instances data/constructed/symfever/symfever.all.jsonl.gz \
  --include-qids results/closed/raw/symfever/gpt-6-luna/agree_qids.json \
  --methods P1 --full-repeats 3 --tag agree_$EP --outer-workers 6 --inner-workers 4 --sample-workers 2
