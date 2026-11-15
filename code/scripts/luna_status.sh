#!/usr/bin/env bash
# Watchdog helper: progress of the luna runs and which runners are alive.
cd "$(dirname "$0")/.."
for d in results/closed/raw/hotpotqa/gpt-6-luna/main results/closed/raw/musique/gpt-6-luna/main \
         results/closed/raw/hotpotqa/gpt-6-luna/k3pilot_v2 results/closed/raw/musique/gpt-6-luna/k3pilot_v2; do
  [ -d $d ] && echo "$d: $(for f in $d/*.jsonl; do printf '%s=%s ' $(basename $f .jsonl) $(wc -l <$f); done)"
done
echo "S3AI hotpotqa runner alive: $(pgrep -f 'bash scripts/run_luna_s3ai_hotpotqa.sh' >/dev/null && echo yes || echo no); done marker: $(grep -c LUNA_S3AI_HOTPOTQA_DONE results/closed/raw/logs/luna_s3ai_hotpotqa.log)"
echo "BootToken runner alive: $(pgrep -f 'bash scripts/run_luna_boottoken_musique.sh' >/dev/null && echo yes || echo no); musique marker: $(grep -c LUNA_BOOT_MUSIQUE_DONE results/closed/raw/logs/luna_boottoken.log); K3 marker: $(grep -c LUNA_BOOT_K3_DONE results/closed/raw/logs/luna_boottoken.log)"
echo "S3AI K3 hotpotqa runner alive: $(pgrep -f 'bash scripts/run_luna_s3ai_k3_hotpotqa.sh' >/dev/null && echo yes || echo no); done marker: $(grep -c LUNA_S3AI_K3_HOTPOTQA_DONE results/closed/raw/logs/luna_s3ai_k3_hotpotqa.log 2>/dev/null)"
echo "errors (last 3): $(grep -h '  ! ' results/closed/raw/logs/luna_s3ai_hotpotqa.log results/closed/raw/logs/luna_boottoken.log results/closed/raw/logs/luna_s3ai_k3_hotpotqa.log 2>/dev/null | tail -3)"
