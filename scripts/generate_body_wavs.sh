#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"

if [[ ! -x "$VENV_PYTHON" ]]; then
  echo "Missing virtual environment: $VENV_PYTHON"
  exit 1
fi

PYTHONUNBUFFERED=1 "$VENV_PYTHON" "$ROOT_DIR/scripts/generate_body_wavs.py" "$@"
