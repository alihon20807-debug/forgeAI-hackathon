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

exec uv run uvicorn app.server:app --host "$HOST" --port "$PORT" --reload
