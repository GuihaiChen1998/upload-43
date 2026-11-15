#!/usr/bin/env bash
# Round 23 (needs user approval of BootToken cost): luna MuSiQue entirely on BootToken
# (same declared model gpt-6-luna; agreement check in results/closed/analysis/endpoint_agreement/),
# then the K3 luna method phase. The partial S3AI MuSiQue rows (V1 done, P1 10/614) are
# moved, not deleted, to main_s3ai_partial/ so that every MuSiQue luna file has one endpoint.
#   CONC_O=8 bash scripts/run_luna_boottoken_musique.sh
set -u
cd "$(dirname "$0")/.."
set -a; . /home/claude/.mht_api.env; set +a
M=configs/models/closed/gpt-6-luna.yaml
D=results/closed/raw/musique/gpt-6-luna
if grep -q '"base_url": "https://ai.furry.vg/v1"' $D/main/V1.jsonl.manifest.json 2>/dev/null; then
  mkdir -p $D/main_s3ai_partial && mv $D/main/* $D/main_s3ai_partial/
fi
W="--outer-workers ${CONC_O:-8} --inner-workers 3 --sample-workers 2"
mkdir -p results/closed/raw/logs
{
python3 -u scripts/17_run_closed.py --model $M --dataset musique --methods V1,P1,LOI --full-repeats 3 --tag main $W
python3 -u scripts/17_run_closed.py --model $M --dataset musique --methods V1,P1 --full-repeats 3 --repeat 1 --tag main $W
python3 -u scripts/17_run_closed.py --model $M --dataset musique --methods RM --rm-k 64 --tag main $W
echo LUNA_BOOT_MUSIQUE_DONE
for ds in hotpotqa musique; do
  python3 -u scripts/17_run_closed.py --model $M --dataset $ds --instances data/constructed/k3/$ds.gpt-6-luna.n50.v2.jsonl.gz \
    --methods V1,P1,LOI,RM --rm-k 64 --full-repeats 3 --repeat 3 --tag k3pilot_v2 $W
done
echo LUNA_BOOT_K3_DONE
} >> results/closed/raw/logs/luna_boottoken.log 2>&1
