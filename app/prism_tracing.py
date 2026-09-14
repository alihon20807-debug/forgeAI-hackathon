"""PRISM live tracing for ClaimGuard (custom FastAPI orchestration).

This app is a hand-rolled, tool-calling FastAPI agent (no LangChain / LangGraph),
so PRISM's framework callback handlers do not apply. Per the repo's own
integration recipe (``research/prism/03-fastapi-agent-integration-recipe.md``,
decision-table row "Hand-rolled FastAPI ... no framework"), the sanctioned path
is the SDK's manual client -> ``POST /api/traces``. We emit one flat trace per
conversational turn, grouped into a trajectory by ``session_id`` (one id per
call, already threaded through ``AgentRunner``).

Design invariants (mirroring the SDK's own documented policy):
  * **Fail-open** -- tracing must never break the caller's response. Every
    failure is logged and swallowed, never raised.
  * **One client per process**, not one per request/turn (a per-conversation
    client leaks a connection pool -- SDK ``test_handler_lifecycle.py``).
    Closed on shutdown via :func:`close` (wired in ``app.server`` lifespan).
  * **PII** -- only masked / veto-filtered content is passed in. The SDK does
    not scrub conversation content, so callers must hand us already-redacted
    text (``masked_transcript`` + the outbound-veto-filtered reply).
  * **Explicit host** -- the SDK's built-in default host is a *different*
    domain; we always pass ``host`` from config so traces land on this
    project's backend.
"""

from __future__ import annotations

import logging
import threading
from typing import Any, Dict, List, Optional

from app.config import (
    AGENT_ID,
    AGENT_NAME,
    LLM_MODEL,
    PRISMTRACE_API_KEY,
    PRISMTRACE_HOST,
    PRISMTRACE_PROJECT_ID,
)

logger = logging.getLogger("claimguard.prism")

# Match the SDK's own per-field input/output cap.
_MAX_TEXT = 10_000

# Per Overall-plan.md §13 / HANDOVER.md §4.3: each architecture version gets its
# own PRISM agent_id so the fleet/session view can separate v0/v1/v2 traces.
# AGENT_ID from config is the fallback for any agent_version not in this map.
_AGENT_ID_BY_VERSION: Dict[str, str] = {
    "v0": "roadside-baseline",
    "v1": "roadside-prompt-fix",
    "v2": "roadside-claimguard",
}


def agent_id_for_version(agent_version: str) -> str:
    """Map an architecture version ('v0'/'v1'/'v2') to its PRISM agent_id."""
    return _AGENT_ID_BY_VERSION.get(agent_version, AGENT_ID)

# Process-wide cached client. None = not yet initialised; False = unavailable
# (SDK missing / construction failed) so callers use the raw-HTTP fallback.
_client: Any = None
_client_lock = threading.Lock()


def is_enabled() -> bool:
    """Tracing is active only when a project id and api key are configured."""
    return bool(PRISMTRACE_PROJECT_ID and PRISMTRACE_API_KEY)


def _get_sdk_client():
    """Return a shared ``prismtrace.PRISMtrace`` client, or ``None``.

    Cached for the life of the process. Never raises: if the SDK is not
    installed or the client cannot be built, returns ``None`` and the caller
    falls back to a plain ``httpx`` POST.
    """
    global _client
    if _client is not None:
        return _client or None
    with _client_lock:
        if _client is not None:
            return _client or None
        try:
            from prismtrace import PRISMtrace  # declared dep: prismtrace-sdk>=0.4.3

            _client = PRISMtrace(
                api_key=PRISMTRACE_API_KEY,
                host=PRISMTRACE_HOST,        # explicit -> overrides the SDK's default host
                project_id=PRISMTRACE_PROJECT_ID,
                timeout=15,                  # a cold backend can exceed the 10s default
            )
            logger.info("PRISM SDK client initialised (host=%s).", PRISMTRACE_HOST)
        except Exception as exc:  # ImportError or construction failure
            logger.info("PRISM SDK unavailable (%s); using HTTP fallback.", exc)
            _client = False
        return _client or None


def _emit_via_http(
    *,
    input_messages: List[Dict[str, str]],
    output_message: str,
    latency_ms: int,
    model: str,
    session_id: str,
    agent_id: str,
    metadata: Dict[str, Any],
) -> None:
    """Fire-and-forget ``POST /api/traces`` used when the SDK isn't importable."""
    import httpx  # already a project runtime dependency

    payload = {
        "project_id": PRISMTRACE_PROJECT_ID,
        "model": model,
        "input_messages": input_messages,
        "output_message": output_message,
        "latency_ms": latency_ms,
        "session_id": session_id,
        "agent_id": agent_id,
        "metadata": metadata,
    }
    url = f"{PRISMTRACE_HOST.rstrip('/')}/api/traces"
    headers = {
        # PRISM authenticates on this header, NOT `Authorization: Bearer`.
        "X-PRISMtrace-Key": PRISMTRACE_API_KEY,
        "Content-Type": "application/json",
    }

    def _send() -> None:
        try:
            resp = httpx.post(url, json=payload, headers=headers, timeout=15)
            if not (200 <= resp.status_code < 300):
                logger.warning("PRISM /api/traces %s: %s", resp.status_code, resp.text[:200])
        except Exception as exc:
            logger.warning("PRISM /api/traces failed: %s", exc)

    threading.Thread(target=_send, name="prism-trace", daemon=True).start()


def emit_turn_trace(
    *,
    session_id: str,
    input_text: str,
    output_text: str,
    latency_ms: int,
    model: str,
    agent_version: str,
    tools_called: Optional[List[str]] = None,
    extra_metadata: Optional[Dict[str, Any]] = None,
    agent_id: Optional[str] = None,
) -> None:
    """Emit one flat PRISM trace for a completed turn. Non-blocking, fail-open.

    ``input_text`` / ``output_text`` **must already be PII-masked / veto-filtered**
    -- pass ``masked_transcript`` and the outbound-veto reply, never raw input.

    ``agent_id`` defaults to ``agent_id_for_version(agent_version)`` -- callers
    should not need to pass it explicitly except to override the mapping.
    """
    if not is_enabled():
        return
    try:
        resolved_agent_id = agent_id or agent_id_for_version(agent_version)
        metadata: Dict[str, Any] = {
            "agent_version": agent_version,
            "tools_called": tools_called or [],
        }
        if extra_metadata:
            metadata.update(extra_metadata)

        input_messages = [{"role": "user", "content": (input_text or "")[:_MAX_TEXT]}]
        output_message = (output_text or "")[:_MAX_TEXT]

        client = _get_sdk_client()
        if client is not None:
            # trace_llm() fires its own background thread and never raises.
            client.trace_llm(
                model=model,
                input_messages=input_messages,
                output=output_message,
                latency_ms=int(latency_ms),
                agent_id=resolved_agent_id,
                agent_name=AGENT_NAME,
                session_id=session_id,
                metadata=metadata,
            )
        else:
            _emit_via_http(
                input_messages=input_messages,
                output_message=output_message,
                latency_ms=int(latency_ms),
                model=model,
                session_id=session_id,
                agent_id=resolved_agent_id,
                metadata=metadata,
            )
    except Exception as exc:  # belt-and-suspenders: never break the turn
        logger.warning("PRISM trace emit failed: %s", exc)


def close() -> None:
    """Flush and close the shared client on shutdown. Idempotent, fail-open."""
    global _client
    client = _client
    if client and client is not False:
        try:
            client.close()  # flush() then close the httpx pool
        except Exception as exc:
            logger.info("PRISM client close failed: %s", exc)
    _client = None


class _PrismTracer:
    """Turn-level adapter used by ``AgentRunner.process_turn``.

    ``runner.py`` calls ``get_prism_tracer().trace_turn(...)`` once per turn.
    This thin wrapper folds the runner's per-turn context (turn id, caller id,
    state-machine transitions) into trace metadata, normalises ``tools_called``
    to a list of names, and delegates to :func:`emit_turn_trace` -- so the
    fail-open, masked-content-only, single-client emit path is shared by both
    the object API and the functional API.
    """

    def trace_turn(
        self,
        *,
        session_id: str,
        turn_id: int = 0,
        caller_id: str = "",
        user_input: str = "",
        agent_output: str = "",
        latency_ms: int = 0,
        tools_called: Optional[List[Any]] = None,
        transitions: Optional[List[Dict[str, Any]]] = None,
        agent_version: str = "v2",
        model: Optional[str] = None,
        extra_metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Emit one flat trace for a completed turn. Never raises (fail-open).

        ``user_input`` / ``agent_output`` must already be masked / veto-filtered
        -- the runner passes ``masked_transcript`` and the post-outbound-veto
        reply, never raw caller text.
        """
        # runner.py passes tools_called as ``[{"name": t}, ...]``; the trace
        # metadata only needs the names.
        names: List[str] = []
        for tool in tools_called or []:
            if isinstance(tool, dict):
                name = tool.get("name")
                if name:
                    names.append(str(name))
            elif tool:
                names.append(str(tool))

        meta: Dict[str, Any] = {
            "turn_id": turn_id,
            "caller_id": caller_id,
        }
        if transitions:
            # State hops only -- terse, bounded payload.
            meta["transitions"] = [
                {
                    "action_type": t.get("action_type"),
                    "from_state": t.get("from_state"),
                    "to_state": t.get("to_state"),
                }
                for t in transitions
            ]
        if extra_metadata:
            meta.update(extra_metadata)

        emit_turn_trace(
            session_id=session_id,
            input_text=user_input,
            output_text=agent_output,
            latency_ms=latency_ms,
            model=model or LLM_MODEL,
            agent_version=agent_version,
            tools_called=names,
            extra_metadata=meta,
        )


_tracer: Optional[_PrismTracer] = None
_tracer_lock = threading.Lock()


def get_prism_tracer() -> _PrismTracer:
    """Return the process-wide turn tracer (see :class:`_PrismTracer`)."""
    global _tracer
    if _tracer is None:
        with _tracer_lock:
            if _tracer is None:
                _tracer = _PrismTracer()
    return _tracer
