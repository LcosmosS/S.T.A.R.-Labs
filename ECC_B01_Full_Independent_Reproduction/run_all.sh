#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON:-python}"
if [[ -z "${OUT_DIR:-}" ]]; then
  RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-$$"
  OUT_DIR="$ROOT/runs/run-$RUN_ID"
fi
"$PYTHON_BIN" "$ROOT/reproduce.py" --mesh --backend auto --h 0.8 0.5 0.3 0.2 --out-dir "$OUT_DIR"
"$PYTHON_BIN" -m unittest discover -s "$ROOT/tests" -v
