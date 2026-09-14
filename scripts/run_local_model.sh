#!/usr/bin/env bash
# Launch local small LLM via llama-server for ClaimGuard Master Demo Server
# Runs with full GPU offloading on RTX 5080

set -euo pipefail

# Default model path (can be overridden with MODEL_PATH env variable)
DEFAULT_MODEL="/home/aliz/Documents/Codes/AI_Stuff/models/Holo/Holo-3.1-9B.i1-Q5_K_M.gguf"
FALLBACK_MODEL="/home/aliz/Documents/Codes/doc2md/models/gemma-4-12B-it-Q4_0.gguf"

MODEL="${MODEL_PATH:-$DEFAULT_MODEL}"

if [ ! -f "$MODEL" ]; then
    if [ -f "$FALLBACK_MODEL" ]; then
        echo "Default model not found at $MODEL. Using fallback: $FALLBACK_MODEL"
        MODEL="$FALLBACK_MODEL"
    else
        echo "Error: No model found at $MODEL or $FALLBACK_MODEL"
        echo "Please set MODEL_PATH to a valid GGUF file."
        exit 1
    fi
fi

LLAMA_SERVER="${LLAMA_SERVER_BIN:-/home/aliz/.local/bin/llama-server}"

if ! command -v "$LLAMA_SERVER" &>/dev/null; then
    if command -v llama-server &>/dev/null; then
        LLAMA_SERVER="llama-server"
    else
        echo "Error: llama-server not found at $LLAMA_SERVER or in PATH."
        exit 1
    fi
fi

EXPOSE="${EXPOSE:-0}"
for arg in "$@"; do
    if [ "$arg" == "--expose" ] || [ "$arg" == "--tunnel" ]; then
        EXPOSE=1
    fi
done

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8080}"
N_GPU_LAYERS="${N_GPU_LAYERS:-99}"
CTX_SIZE="${CTX_SIZE:-8192}"

echo "========================================================="
echo " ClaimGuard Local LLM Server (Master Demo Host: Ali)"
echo " Model: $MODEL"
echo " GPU Offload: $N_GPU_LAYERS layers"
echo " Context Size: $CTX_SIZE"
echo " Endpoint: http://$HOST:$PORT/v1"
echo "========================================================="

TUNNEL_PID=""
cleanup() {
    if [ -n "$TUNNEL_PID" ] && kill -0 "$TUNNEL_PID" 2>/dev/null; then
        echo "Stopping tunnel..."
        kill "$TUNNEL_PID" 2>/dev/null || true
    fi
}
trap cleanup EXIT INT TERM

if [ "$EXPOSE" = "1" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    echo "Starting public tunnel in background..."
    "$SCRIPT_DIR/expose_local_model.sh" "$PORT" &
    TUNNEL_PID=$!
    # Brief pause so banner prints before llama-server logs start
    sleep 2
fi

exec "$LLAMA_SERVER" \
    -m "$MODEL" \
    --host "$HOST" \
    --port "$PORT" \
    -ngl "$N_GPU_LAYERS" \
    -c "$CTX_SIZE" \
    --metrics
