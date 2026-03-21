#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"
MODEL_PATH="$ROOT_DIR/models/kokoro-v1.0.onnx"
VOICES_PATH="$ROOT_DIR/models/voices-v1.0.bin"
DEFAULT_VOICE="${KOKORO_DEFAULT_VOICE:-af_sarah}"

usage() {
  cat <<'EOF'
Usage:
  scripts/generate_wav.sh <input.txt> <output.wav> [extra kokoro-tts args]

Example:
  scripts/generate_wav.sh ./line.txt ./line.wav --voice af_sarah --speed 1.0

Notes:
  - The script uses the local .venv and models/ directory in this repo.
  - Extra CLI arguments are passed through to kokoro-tts unchanged.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -lt 2 ]]; then
  usage
  exit 1
fi

if [[ ! -x "$VENV_PYTHON" ]]; then
  echo "Missing virtual environment: $VENV_PYTHON"
  echo "Run: python3 -m venv .venv && .venv/bin/pip install -e ."
  exit 1
fi

if [[ ! -f "$MODEL_PATH" || ! -f "$VOICES_PATH" ]]; then
  echo "Missing model assets in $ROOT_DIR/models"
  exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"
shift 2

echo "Using voice: $DEFAULT_VOICE"

PYTHONUNBUFFERED=1 "$VENV_PYTHON" "$ROOT_DIR/scripts/run_kokoro.py" \
  "$INPUT_FILE" \
  "$OUTPUT_FILE" \
  --voice "$DEFAULT_VOICE" \
  --lang en-us \
  --speed 1.0 \
  --model "$MODEL_PATH" \
  --voices "$VOICES_PATH" \
  "$@"
