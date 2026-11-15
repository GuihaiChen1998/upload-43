#!/usr/bin/env bash
# Follow-up probes for the ICDE pre-reviews (issue #3; instances from 38_build_review_probes.py).
# Resumable: re-run the same command.
#   bash scripts/run_review_probes.sh <model.yaml> <trial|full> <outer> <inner> [which=swap,conflict,unscreened]
# trial: 20 instances per probe (tag <probe>_trial); full: every instance (tag <probe>). Trial calls are
# cache hits in the full run.
set -u
cd "$(dirname "$0")/.."
set -a; . /home/claude/.mht_api.env; set +a
CFG=$1; MODE=$2; OW=$3; IW=$4; WHICH=${5:-swap,conflict,unscreened}
NAME=$(python3 -c "import yaml,sys;print(yaml.safe_load(open('$CFG'))['name'])")
D=data/constructed/review_probes
if [ "$MODE" = trial ]; then EXTRA="--sample-n 20"; SUF=_trial; else EXTRA=""; SUF=""; fi
run() { # dataset instances methods tag
  echo "== $(date -u +%FT%TZ) $NAME $1 $4 $3"
  python3 -u scripts/17_run_closed.py --model "$CFG" --dataset "$1" --instances "$2" $EXTRA --methods "$3" \
    --full-repeats 0 --tag "$4$SUF" --outer-workers "$OW" --inner-workers "$IW" --sample-workers 1 || return 1
}
case ",$WHICH," in *,swap,*) run symfever $D/symfever.$NAME.swap.jsonl.gz V1 probe_swap ;; esac
case ",$WHICH," in *,conflict,*) run symfever $D/symfever.$NAME.conflict.jsonl.gz V1,P1,LOI probe_conflict ;; esac
case ",$WHICH," in *,unscreened,*)
  run hotpotqa $D/hotpotqa.$NAME.unscreened.jsonl.gz V1,LOI probe_unscreened
  run musique $D/musique.$NAME.unscreened.jsonl.gz V1,LOI probe_unscreened ;; esac
echo "== $(date -u +%FT%TZ) $NAME $MODE DONE"
