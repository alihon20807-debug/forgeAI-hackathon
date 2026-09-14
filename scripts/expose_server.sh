#!/usr/bin/env bash
# Expose ClaimGuard FastAPI Server (port 8000) via Cloudflare Tunnel
# Instant HTTPS URL for Android phone on hotspot (with full mic permissions)

set -euo pipefail
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

PORT="${1:-8000}"
METHOD="${2:-cloudflared}"

echo "========================================================="
echo " ClaimGuard Mobile Hotspot Exposer"
echo " Exposing Port: $PORT (FastAPI Server)"
echo " Mobile Call UI: https://<tunnel-url>/call"
echo " Judge Viewer:   https://<tunnel-url>/viewer"
echo "========================================================="

exec "$REPO_DIR/scripts/expose_local_model.sh" "$PORT" "$METHOD"
