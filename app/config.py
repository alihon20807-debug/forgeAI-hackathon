"""Configuration settings for ClaimGuard backend."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Database
DB_PATH = Path(os.getenv("CLAIMGUARD_DB_PATH", DATA_DIR / "claimguard.db"))

# LLM inference (llama-server / LiteLLM)
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://127.0.0.1:8080/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "no-key-required")
LLM_MODEL = os.getenv("LLM_MODEL", "local-model")
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "false").lower() in ("true", "1", "yes")

# PRISM Telemetry
PRISMTRACE_HOST = os.getenv("PRISMTRACE_HOST", "https://prism.blockconvey.com").rstrip("/")
PRISMTRACE_PROJECT_ID = os.getenv("PRISMTRACE_PROJECT_ID", "")
PRISMTRACE_API_KEY = os.getenv("PRISMTRACE_API_KEY", "")
AGENT_ID = os.getenv("AGENT_ID", "roadside-claimguard")
