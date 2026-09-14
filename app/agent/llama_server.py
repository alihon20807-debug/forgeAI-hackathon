"""llama.cpp (llama-server) Python lifecycle and execution wrapper for ClaimGuard.

Defaults to Holo-3.1-9B (Q5_K_M GGUF) running locally with GPU offloading
on the Master Demo Server (Ali's machine, RTX 5080).
"""

from __future__ import annotations

import argparse
import logging
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

import httpx

from app.config import (
    DEFAULT_MODEL_PATH,
    FALLBACK_MODEL_PATH,
    LLAMA_SERVER_BIN,
    LLM_BASE_URL,
)

logger = logging.getLogger("claimguard.llama_server")


class LlamaCppServer:
    """Manages the local llama-server instance running Holo 9B."""

    def __init__(
        self,
        model_path: Optional[str] = None,
        host: str = "127.0.0.1",
        port: int = 8080,
        n_gpu_layers: int = 99,
        ctx_size: int = 4096,
        binary_path: Optional[str] = None,
    ) -> None:
        self.model_path = model_path or os.getenv("MODEL_PATH", str(DEFAULT_MODEL_PATH))
        self.fallback_model = str(FALLBACK_MODEL_PATH)
        self.host = host
        self.port = port
        self.n_gpu_layers = n_gpu_layers
        self.ctx_size = ctx_size
        self.binary_path = binary_path or os.getenv("LLAMA_SERVER_BIN", str(LLAMA_SERVER_BIN))
        self.process: Optional[subprocess.Popen] = None

    def resolve_model_path(self) -> str:
        """Resolve valid model file path, falling back if necessary."""
        if os.path.isfile(self.model_path):
            return self.model_path
        if os.path.isfile(self.fallback_model):
            logger.warning(
                f"Default model {self.model_path} not found. Falling back to {self.fallback_model}"
            )
            return self.fallback_model
        raise FileNotFoundError(
            f"No GGUF model found at {self.model_path} or fallback {self.fallback_model}"
        )

    def is_healthy(self, timeout: float = 2.0) -> bool:
        """Check if llama-server is currently running and responding to /health."""
        try:
            url = f"http://{self.host}:{self.port}/health"
            with httpx.Client(timeout=timeout) as client:
                res = client.get(url)
                return res.status_code == 200 and res.json().get("status") == "ok"
        except Exception:
            return False

    def get_status(self) -> Dict[str, Any]:
        """Query server status, slots, and props."""
        healthy = self.is_healthy()
        info: Dict[str, Any] = {
            "healthy": healthy,
            "host": self.host,
            "port": self.port,
            "configured_model": self.model_path,
        }
        if healthy:
            try:
                with httpx.Client(timeout=3.0) as client:
                    props = client.get(f"http://{self.host}:{self.port}/props").json()
                    info["server_props"] = props
            except Exception as e:
                info["props_error"] = str(e)
        return info

    def start(self, wait_ready: bool = True, timeout: float = 30.0) -> bool:
        """Start llama-server in the background if not already running."""
        if self.is_healthy():
            logger.info(f"llama-server is already healthy at http://{self.host}:{self.port}")
            return True

        resolved_model = self.resolve_model_path()
        cmd = [
            self.binary_path,
            "-m", resolved_model,
            "--host", self.host,
            "--port", str(self.port),
            "-ngl", str(self.n_gpu_layers),
            "-c", str(self.ctx_size),
            "--jinja",
            "--metrics",
        ]

        logger.info(f"Launching llama-server: {' '.join(cmd)}")
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=os.setsid if hasattr(os, "setsid") else None,
        )

        if not wait_ready:
            return True

        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_healthy():
                logger.info("llama-server is healthy and ready for inference.")
                return True
            if self.process and self.process.poll() is not None:
                err = self.process.stderr.read() if self.process.stderr else "Unknown error"
                raise RuntimeError(f"llama-server terminated unexpectedly: {err}")
            time.sleep(0.5)

        raise TimeoutError(f"llama-server failed to become healthy within {timeout}s")

    def stop(self) -> None:
        """Stop the server process if managed by this instance."""
        if self.process and self.process.poll() is None:
            logger.info("Stopping managed llama-server process...")
            try:
                if hasattr(os, "killpg"):
                    os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                else:
                    self.process.terminate()
                self.process.wait(timeout=5)
            except Exception as e:
                logger.warning(f"Error terminating process: {e}")
            self.process = None


def get_default_llama_server() -> LlamaCppServer:
    return LlamaCppServer()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ClaimGuard llama.cpp Server Controller")
    parser.add_argument("action", choices=["start", "stop", "status", "health"], default="status", nargs="?")
    args = parser.parse_args()

    server = get_default_llama_server()

    if args.action == "health":
        healthy = server.is_healthy()
        print(f"Health: {'OK' if healthy else 'DOWN'}")
        sys.exit(0 if healthy else 1)
    elif args.action == "status":
        status = server.get_status()
        import pprint
        pprint.pprint(status)
    elif args.action == "start":
        print(f"Starting llama-server with default Holo-3.1-9B...")
        try:
            server.start(wait_ready=True)
            print("llama-server successfully started!")
        except Exception as e:
            print(f"Failed to start server: {e}")
            sys.exit(1)
    elif args.action == "stop":
        server.stop()
        print("llama-server stop command issued.")
