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
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://127.0.0.1:8080/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "no-key-required")
LLM_MODEL = os.getenv("LLM_MODEL", "local-model")
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "false").lower() in ("true", "1", "yes")

# PRISM Telemetry
PRISMTRACE_HOST = os.getenv("PRISMTRACE_HOST", "https://prism-api-prod.up.railway.app").rstrip("/")
PRISMTRACE_PROJECT_ID = os.getenv("PRISMTRACE_PROJECT_ID", "066e7755-d375-4690-b4a7-4492d33f680b")
PRISMTRACE_API_KEY = os.getenv("PRISMTRACE_API_KEY", "")
# Stable agent identity for PRISM (do NOT rename casually -- guardrails/alerts
# are scoped to AGENT_ID). AGENT_NAME is display-only.
AGENT_ID = os.getenv("AGENT_ID", "roadside-claimguard")
AGENT_NAME = os.getenv("AGENT_NAME", "ClaimGuard FNOL Agent")

