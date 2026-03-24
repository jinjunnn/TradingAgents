#!/bin/bash
# Auto-install Python dependencies into a local venv.
# Only reinstalls when requirements.txt changes (hash-based check).

set -e

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
VENV_DIR="${PLUGIN_ROOT}/.venv"
REQ_FILE="${PLUGIN_ROOT}/scripts/requirements.txt"
REQ_HASH_FILE="${VENV_DIR}/.req-hash"

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR" 2>/dev/null || {
    echo "[tradingagents] Warning: could not create venv" >&2
    exit 0
  }
fi

# Check if requirements changed
if command -v md5 >/dev/null 2>&1; then
  CURRENT_HASH=$(md5 -q "$REQ_FILE")
elif command -v md5sum >/dev/null 2>&1; then
  CURRENT_HASH=$(md5sum "$REQ_FILE" | cut -d' ' -f1)
else
  CURRENT_HASH="unknown"
fi

CACHED_HASH=$(cat "$REQ_HASH_FILE" 2>/dev/null || echo "")

if [ "$CURRENT_HASH" != "$CACHED_HASH" ]; then
  echo "[tradingagents] Installing Python dependencies..."
  "$VENV_DIR/bin/pip" install -q -r "$REQ_FILE" 2>/dev/null
  echo "$CURRENT_HASH" > "$REQ_HASH_FILE"
  echo "[tradingagents] Dependencies installed."
else
  echo "[tradingagents] Dependencies up to date."
fi
