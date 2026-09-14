#!/usr/bin/env bash
# One-click startup for ClaimGuard FastAPI Backend Server
# Ali's Demo & Development Server

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

echo "========================================================="
echo " ClaimGuard Backend & Enforcement Server"
echo " Host: $HOST"
echo " Port: $PORT"
echo " Docs: http://$HOST:$PORT/docs"
echo " OpenAPI JSON: http://$HOST:$PORT/openapi.json"
echo " WebSocket: ws://$HOST:$PORT/ws/session/{session_id}"
echo "========================================================="

UVICORN_BIN="$REPO_DIR/.venv/bin/uvicorn"
if [ -f "$UVICORN_BIN" ]; then
    exec "$UVICORN_BIN" app.server:app --host "$HOST" --port "$PORT" --reload
else
    exec uv run uvicorn app.server:app --host "$HOST" --port "$PORT" --reload
fi
