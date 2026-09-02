#!/usr/bin/env bash
# Print one hash covering every diagram source, the render config, and every
# rendered PNG. regen.sh writes this to .stamp; the sync check recomputes it
# and compares. A mismatch means a source or PNG changed without regen.sh.
set -euo pipefail
cd "$(dirname "$0")"
shasum -a 256 *.mmd *-config.json *.png | shasum -a 256 | cut -d' ' -f1
