#!/bin/sh
# Crop the empty top margin left by removing in-figure titles, then convert to the PDFs the paper includes.
# Run from paper/figures/gpt after `node ../drafts/editable-20261106/render_figures_paper.cjs`.
set -e
crop() { # src out x y w h
  python3 - "$1" "$2" "$3" "$4" "$5" "$6" <<'PY'
import re,sys
src,out,x,y,w,h=sys.argv[1:]
s=open(src).read()
s=re.sub(r'width="\d+" height="\d+" viewBox="0 0 \d+ \d+"',f'width="{w}" height="{h}" viewBox="{x} {y} {w} {h}"',s,count=1)
s=s.replace('<rect width="100%" height="100%" fill="white"/>',f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white"/>',1)
open(out,'w').write(s)
PY
  rsvg-convert -f pdf "$2" -o "../$(basename "$2" .svg).pdf"
}
crop fig_overview_airy.svg      fig_overview.svg  0 62 1200 524
crop fig_frontier_editable.svg  fig_frontier.svg  0 38 1200 674
crop fig_maps_editable.svg      fig_maps.svg      0 64 1125 689
crop fig_dist_editable.svg      fig_dist.svg      0 42 1200 382
