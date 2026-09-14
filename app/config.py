"""Configuration settings for ClaimGuard backend."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Best-effort local .env loader (dependency-free). Populates os.environ from a
# gitignored .env for local runs (uvicorn / pytest / scripts) so PRISM + LLM
# config "just works". Never overrides vars already set in the real
# environment, and never fails the import if the file is missing or malformed.
_ENV_FILE = BASE_DIR / ".env"
if _ENV_FILE.exists():
    try:
        for _line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
            _line = _line.strip()
            if not _line or _line.startswith("#") or "=" not in _line:
                continue
            _key, _, _val = _line.partition("=")
            os.environ.setdefault(_key.strip(), _val.strip())
    except Exception:
        pass

# Database
DB_PATH = Path(os.getenv("CLAIMGUARD_DB_PATH", DATA_DIR / "claimguard.db"))

# LLM inference (llama-server / LiteLLM)
LLAMA_SERVER_BIN = Path(os.getenv("LLAMA_SERVER_BIN", "/home/aliz/.local/bin/llama-server"))
DEFAULT_MODEL_PATH = Path(os.getenv("MODEL_PATH", "/home/aliz/Documents/Codes/AI_Stuff/models/Holo/Holo-3.1-9B.i1-Q5_K_M.gguf"))
FALLBACK_MODEL_PATH = Path("/home/aliz/Documents/Codes/doc2md/models/gemma-4-12B-it-Q4_0.gguf")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://127.0.0.1:8080/v1")
# An empty LLM_API_KEY (the correct .env value for a local, no-auth
# llama-server) must NOT become an empty Authorization header -- httpx
# rejects "Bearer " (trailing space, no token) outright as an illegal
# header value, which silently killed every real-model call and made
# every turn fall back to the mock. `or` treats "" the same as unset.
LLM_API_KEY = os.getenv("LLM_API_KEY") or "no-key-required"
LLM_MODEL = os.getenv("LLM_MODEL", "Holo-3.1-9B")
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "false").lower() in ("true", "1", "yes")

# PRISM Telemetry
PRISMTRACE_HOST = os.getenv("PRISMTRACE_HOST", "https://prism-api-prod.up.railway.app").rstrip("/")
PRISMTRACE_PROJECT_ID = os.getenv("PRISMTRACE_PROJECT_ID", "066e7755-d375-4690-b4a7-4492d33f680b")
PRISMTRACE_API_KEY = os.getenv("PRISMTRACE_API_KEY", "")
# Stable agent identity for PRISM (do NOT rename casually -- guardrails/alerts
# are scoped to AGENT_ID). AGENT_NAME is display-only.
AGENT_ID = os.getenv("AGENT_ID", "roadside-claimguard")
AGENT_NAME = os.getenv("AGENT_NAME", "ClaimGuard FNOL Agent")

