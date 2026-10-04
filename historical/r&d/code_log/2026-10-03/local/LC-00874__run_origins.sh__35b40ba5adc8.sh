#!/usr/bin/env bash
set -euo pipefail
ROOT=/home/Kepler/star_docgen
MODEL="${1:-$(ollama list | awk 'NR==2{print $1}')}"
python "$ROOT/star_docgen.py" --corpus "$ROOT/corpus" --output "$ROOT/output" --model "$MODEL" --docs Origins.pdf Research-Analysis+Testing.pdf Research-Analysis+Testing_pt.2.pdf Research-Analysis+Testing_pt.3.pdf Branch_Rersearch-Analysis+Testing_pt.4.pdf
