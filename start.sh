#!/bin/bash
# HelpOS — Local Dev Start Script
# Usage: ./start.sh

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

echo ""
echo "  ╔═══════════════════════════════╗"
echo "  ║   HelpOS — Local AI Engine   ║"
echo "  ╚═══════════════════════════════╝"
echo ""

# ── 1. Create venv if missing ─────────────────────────────
if [ ! -d "$VENV_DIR" ]; then
  echo "→ Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

# ── 2. Install / update dependencies ─────────────────────
echo "→ Installing dependencies..."
"$VENV_DIR/bin/pip" install -q -r "$PROJECT_DIR/backend/requirements.txt"

# ── 3. Warn if Ollama is not running ─────────────────────
if ! curl -sf http://localhost:11434 > /dev/null 2>&1; then
  echo ""
  echo "  ⚠  Ollama is not running."
  echo "     Start it with:  ollama serve"
  echo "     Pull a model:   ollama pull llama3"
  echo ""
fi

# ── 4. Launch server ──────────────────────────────────────
echo "→ Starting HelpOS at http://localhost:8000"
echo "   Press Ctrl+C to stop."
echo ""

cd "$PROJECT_DIR"
"$VENV_DIR/bin/uvicorn" backend.app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
