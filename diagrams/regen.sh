#!/usr/bin/env bash
# Regenerate the README diagram PNGs from their .mmd sources and update the
# sync stamp that CI verifies. This script is the only supported way to
# regenerate: running mmdc by hand skips the stamp and CI will fail.
#
# Why PNGs instead of a ```mermaid block: GitHub renders Mermaid in the
# viewer's browser, measuring label text in one font and drawing it in
# another. Labels clip, and each browser clips differently. Pre-rendering
# removes the viewer's browser from the loop.
set -euo pipefail
cd "$(dirname "$0")"

npx -y -p @mermaid-js/mermaid-cli mmdc -i orgchart.mmd -o orgchart-light.png -b transparent -s 2
npx -y -p @mermaid-js/mermaid-cli mmdc -i orgchart.mmd -o orgchart-dark.png  -b transparent -s 2 -c dark-config.json

./stamp.sh > .stamp
echo "Rendered 2 PNGs and updated .stamp"
