#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python "$ROOT/reproduce.py" --mesh --backend auto --h 0.8 0.5 0.3 0.2 --out-dir "$ROOT/results"
python -m unittest discover -s "$ROOT/tests" -v
