#!/usr/bin/env bash
# Expose local model (llama-server) or FastAPI server via Cloudflare Tunnel (default), Pinggy, or ngrok.
# Solves localhost reachability for PRISM reverse proxy, cloud evaluators, or remote team access.

set -euo pipefail

PORT="${1:-${PORT:-8080}}"
METHOD="${2:-${METHOD:-cloudflared}}"

# ANSI Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BOLD}=========================================================${NC}"
echo -e "${BOLD}  ClaimGuard Model & Service Exposer (for PRISM Access)  ${NC}"
echo -e "${BOLD}=========================================================${NC}"

# Check if port is currently listening
if ! ss -tulpn 2>/dev/null | grep -q ":$PORT "; then
    echo -e "${YELLOW}Notice: No process currently listening on port $PORT.${NC}"
    echo -e "If you haven't started llama-server yet, run in another terminal:"
    echo -e "  ${CYAN}./scripts/run_local_model.sh${NC}"
    echo -e "Starting tunnel anyway so it is ready when your server starts up..."
    echo ""
fi

CLOUDFLARED_BIN="${CLOUDFLARED_BIN:-/home/aliz/.local/bin/cloudflared}"
if ! command -v "$CLOUDFLARED_BIN" &>/dev/null; then
    if command -v cloudflared &>/dev/null; then
        CLOUDFLARED_BIN="cloudflared"
    fi
fi

cleanup() {
    echo ""
    echo -e "${YELLOW}Stopping tunnel and cleaning up...${NC}"
    if [ -n "${TUNNEL_PID:-}" ] && kill -0 "$TUNNEL_PID" 2>/dev/null; then
        kill "$TUNNEL_PID" 2>/dev/null || true
    fi
    rm -f "${LOG_FILE:-}"
    exit 0
}
trap cleanup INT TERM EXIT

case "$METHOD" in
    cloudflared)
        if ! command -v "$CLOUDFLARED_BIN" &>/dev/null; then
            echo -e "${RED}Error: cloudflared binary not found at $CLOUDFLARED_BIN${NC}"
            echo "Falling back to Pinggy (SSH-based tunnel, zero install needed)..."
            METHOD="pinggy"
        else
            echo -e "Using ${GREEN}Cloudflare Tunnel${NC} (no account required, no interstitial warning pages, unlimited bandwidth)..."
            LOG_FILE=$(mktemp /tmp/cloudflared-tunnel-XXXXXX.log)
            
            "$CLOUDFLARED_BIN" tunnel --url "http://localhost:$PORT" > "$LOG_FILE" 2>&1 &
            TUNNEL_PID=$!

            echo -e "Waiting for tunnel URL from Cloudflare Edge..."
            URL=""
            for _ in {1..30}; do
                if ! kill -0 "$TUNNEL_PID" 2>/dev/null; then
                    echo -e "${RED}cloudflared failed to start. Logs:${NC}"
                    cat "$LOG_FILE"
                    exit 1
                fi
                URL=$(grep -o 'https://[a-zA-Z0-9.-]*\.trycloudflare\.com' "$LOG_FILE" | head -n 1 || true)
                if [ -n "$URL" ]; then
                    break
                fi
                sleep 0.5
            done

            if [ -z "$URL" ]; then
                echo -e "${RED}Could not extract Cloudflare Tunnel URL. Check logs:${NC}"
                cat "$LOG_FILE"
                exit 1
            fi

            echo ""
            echo -e "${GREEN}${BOLD}=========================================================================${NC}"
            echo -e "${GREEN}${BOLD}  PUBLIC TUNNEL READY FOR PRISM${NC}"
            echo -e "${GREEN}${BOLD}=========================================================================${NC}"
            echo -e "  ${BOLD}Local Port:${NC}        http://localhost:$PORT"
            echo -e "  ${BOLD}Public HTTPS URL:${NC}  ${CYAN}${BOLD}$URL${NC}"
            echo -e "  ${BOLD}OpenAI Base URL:${NC}   ${CYAN}${BOLD}$URL/v1${NC}"
            echo -e "${GREEN}${BOLD}=========================================================================${NC}"
            echo ""
            echo -e "${BOLD}How to use this with PRISM & ClaimGuard:${NC}"
            echo -e "  1. If setting up PRISM Reverse Proxy / Cloud Evaluator upstream:"
            echo -e "     Target URL -> ${CYAN}$URL/v1${NC}"
            echo -e "  2. If pointing ClaimGuard backend to this tunnel:"
            echo -e "     Update .env -> ${CYAN}LLM_BASE_URL=$URL/v1${NC}"
            echo -e "  3. Test connectivity:"
            echo -e "     ${CYAN}curl $URL/v1/models${NC}"
            echo ""
            echo -e "Tunnel running. Press ${BOLD}Ctrl+C${NC} to stop."
            wait "$TUNNEL_PID"
        fi
        ;;

    pinggy)
        echo -e "Using ${GREEN}Pinggy${NC} via standard OpenSSH..."
        echo -e "Connecting to a.pinggy.io on port 443..."
        ssh -p 443 -R0:localhost:"$PORT" \
            -o StrictHostKeyChecking=no \
            -o ServerAliveInterval=30 \
            a.pinggy.io
        ;;

    ngrok)
        if ! command -v ngrok &>/dev/null; then
            echo -e "${RED}Error: ngrok is not installed. You can run with cloudflared or pinggy instead.${NC}"
            exit 1
        fi
        echo -e "Starting ngrok tunnel on port $PORT..."
        ngrok http "$PORT"
        ;;

    *)
        echo -e "${RED}Unknown method: $METHOD. Options: cloudflared, pinggy, ngrok${NC}"
        exit 1
        ;;
esac
