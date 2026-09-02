#!/usr/bin/env bash
# Regenerate every README diagram PNG from its .mmd source and update the
# sync stamp. This script is the only supported way to regenerate: running
# mmdc by hand skips the stamp and the sync check fails.
#
# Why PNGs instead of a ```mermaid block: GitHub renders Mermaid in the
# viewer's browser, measuring label text in one font and drawing it in
# another. Labels clip, and each browser clips differently. Pre-rendering
# removes the viewer's browser from the loop.
set -euo pipefail
cd "$(dirname "$0")"

n=0
for src in *.mmd; do
  name="${src%.mmd}"
  npx -y -p @mermaid-js/mermaid-cli mmdc -i "$src" -o "$name-light.png" -b transparent -s 2 -q -w 1200 -c light-config.json
  npx -y -p @mermaid-js/mermaid-cli mmdc -i "$src" -o "$name-dark.png"  -b transparent -s 2 -q -w 1200 -c dark-config.json
  n=$((n+2))
done

./stamp.sh > .stamp
echo "Rendered $n PNGs and updated .stamp"
