"""FastAPI Server for ClaimGuard.

Provides REST and WebSocket endpoints for FNOL voice agent processing,
deterministic state machine transitions, policy latch queries, and live
supervisor console monitoring.
"""

from __future__ import annotations

import json
import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.agent.runner import get_agent_runner
from app.db.database import get_claim_db, get_dispatches_by_claim_db, init_db, lookup_policy_db
from app.enforcement.commit_window import get_commit_window
from app.observability.prism_tracer import close as close_prism_tracer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("claimguard.server")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database and triggers
    logger.info("Initializing ClaimGuard SQLite Database and Policy Latch triggers...")
    init_db()
    logger.info("ClaimGuard Database initialized successfully.")
    yield
    # Shutdown
    logger.info("ClaimGuard Server shutting down.")
    close_prism_tracer()  # flush + close the shared PRISM client (fail-open)


app = FastAPI(
    title="ClaimGuard × PRISM Voice Agent API",
    description="Deterministic enforcement layer (L3) and System of Record (L4) for FNOL claims.",
    version="0.1.0",
    lifespan=lifespan,
)

from pathlib import Path
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

# CORS middleware for supervisor console
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
    app.mount("/console", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="console")


@app.get("/")
@app.get("/call")
def get_phone_ui():
    """Dead-simple mobile phone call UI for the presenter."""
    phone_html = FRONTEND_DIR / "phone.html"
    if phone_html.exists():
        return FileResponse(phone_html)
    return RedirectResponse(url="/console")


@app.get("/viewer")
def get_viewer_ui():
    """Dead-simple real-time live inspection viewer for judges."""
    viewer_html = FRONTEND_DIR / "viewer.html"
    if viewer_html.exists():
        return FileResponse(viewer_html)
    return RedirectResponse(url="/console")


# -----------------------------------------------------------------------------
# Request & Response Models (Strictly matching docs/HANDOVER.md §4.1 & §4.2)
# -----------------------------------------------------------------------------

class RedactedPII(BaseModel):
    type: str
    matched: str
    valid_luhn: Optional[bool] = None
    valid_verhoeff: Optional[bool] = None


class TurnRequest(BaseModel):
    session_id: str
    turn_id: int
    caller_id: str
    raw_transcript: str
    masked_transcript: str
    redacted_pii: Optional[List[RedactedPII]] = Field(default_factory=list)
    agent_version: Optional[str] = "v2"  # "v0", "v1", "v2"


class StateTransitionModel(BaseModel):
    action_id: str
    action_type: str
    from_state: str
    to_state: str
    reason: str


class StateMachineModel(BaseModel):
    held_actions: List[Dict[str, Any]] = Field(default_factory=list)
    transitions: List[StateTransitionModel] = Field(default_factory=list)


class CurrentClaimModel(BaseModel):
    claim_id: str
    status: str
    deductible_inr: int
    liability_ratio: Optional[float] = 1.0
    locked_fields: List[str] = Field(default_factory=lambda: ["deductible_inr", "liability_ratio"])


class TurnResponse(BaseModel):
    session_id: str
    turn_id: int
    agent_response: str
    state_machine: StateMachineModel
    current_claim: Optional[CurrentClaimModel] = None
    raw_transcript: Optional[str] = None
    masked_transcript: Optional[str] = None
    redacted_pii: Optional[List[Dict[str, Any]]] = None


class SessionInitRequest(BaseModel):
    session_id: str
    caller_id: str
    policy_number: Optional[str] = "NH-8821"


# -----------------------------------------------------------------------------
# WebSocket Manager for Live Supervisor Console & Judge Live Viewer
# -----------------------------------------------------------------------------

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.global_connections: List[WebSocket] = []

    async def connect(self, session_id: str, websocket: WebSocket):
        await websocket.accept()
        if session_id in ("all", "live"):
            self.global_connections.append(websocket)
        else:
            if session_id not in self.active_connections:
                self.active_connections[session_id] = []
            self.active_connections[session_id].append(websocket)

    def disconnect(self, session_id: str, websocket: WebSocket):
        if websocket in self.global_connections:
            self.global_connections.remove(websocket)
        if session_id in self.active_connections:
            if websocket in self.active_connections[session_id]:
                self.active_connections[session_id].remove(websocket)

    async def broadcast(self, session_id: str, message: Dict[str, Any]):
        # Broadcast to session-specific subscribers
        if session_id in self.active_connections:
            for connection in list(self.active_connections[session_id]):
                try:
                    await connection.send_text(json.dumps(message))
                except Exception:
                    self.disconnect(session_id, connection)
        # Broadcast to global live viewers (e.g. judges' screen)
        for connection in list(self.global_connections):
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                if connection in self.global_connections:
                    self.global_connections.remove(connection)


manager = ConnectionManager()


# -----------------------------------------------------------------------------
# REST Routes
# -----------------------------------------------------------------------------

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "claimguard-backend", "version": "0.1.0"}


@app.post("/api/call/session")
def init_session(req: SessionInitRequest):
    """Initialize a call session and pre-fetch policy details."""
    policy = lookup_policy_db(policy_number=req.policy_number)
    cw = get_commit_window()
    cw.clear_session(req.session_id)
    return {
        "status": "initialized",
        "session_id": req.session_id,
        "caller_id": req.caller_id,
        "policy": policy,
    }


@app.post("/api/call/turn", response_model=TurnResponse)
async def process_turn(req: TurnRequest):
    """Process a single conversational turn with defense-in-depth PII shielding and PRISM tracing."""
    from app.observability.prism_tracer import TurnTracer
    from app.security.pii_shield import redact_pii

    masked_transcript = req.masked_transcript
    redacted_pii = [p.model_dump() for p in (req.redacted_pii or [])]

    # Pre-LLM PII defense-in-depth: If client didn't pre-mask, scrub mathematically
    if not masked_transcript or masked_transcript == req.raw_transcript:
        shield_res = redact_pii(req.raw_transcript)
        masked_transcript = shield_res.masked_transcript
        if shield_res.redacted_pii:
            for item in shield_res.redacted_pii:
                redacted_pii.append(item.to_dict())

    runner = get_agent_runner()

    # Initialize PRISM turn tracer
    tracer = TurnTracer(
        session_id=req.session_id,
        user_utterance=masked_transcript,
        agent_version=req.agent_version or "v2",
        is_mock=runner.use_mock,
    )

    result = await runner.process_turn(
        session_id=req.session_id,
        turn_id=req.turn_id,
        caller_id=req.caller_id,
        raw_transcript=req.raw_transcript,
        masked_transcript=masked_transcript,
        redacted_pii=redacted_pii,
        agent_version=req.agent_version or "v2",
    )

    # Record Commit Window transitions as PRISM spans
    for t in result["state_machine"]["transitions"]:
        tracer.record_enforcement_transition(
            action_id=t["action_id"],
            action_type=t["action_type"],
            from_state=t["from_state"],
            to_state=t["to_state"],
            reason=t["reason"],
        )

    # Flush spans in background
    tracer.finish(
        agent_reply=result["agent_response"],
        extra_metadata={
            "turn_id": req.turn_id,
            "caller_id": req.caller_id,
            "pii_redacted_count": len(redacted_pii),
        },
    )

    result["raw_transcript"] = req.raw_transcript
    result["masked_transcript"] = masked_transcript
    result["redacted_pii"] = redacted_pii

    # Broadcast turn and state machine transitions to connected supervisor consoles and live viewers
    broadcast_payload = dict(result)
    broadcast_payload["type"] = "TURN_PROCESSED"
    await manager.broadcast(req.session_id, broadcast_payload)

    return result


@app.post("/api/voice/transcribe")
async def transcribe_voice(
    file: UploadFile = File(...),
    session_id: Optional[str] = Form(None),
    turn_id: Optional[int] = Form(1),
    caller_id: Optional[str] = Form("caller_edge"),
):
    """Local ASR endpoint with Whisper and pre-LLM mathematical PII redaction."""
    import time
    from app.voice.transcriber import get_default_transcriber
    transcriber = get_default_transcriber()
    t0 = time.perf_counter()
    audio_bytes = await file.read()
    result = transcriber.transcribe_audio_bytes(audio_bytes, file.filename or "audio.wav")
    latency_ms = round((time.perf_counter() - t0) * 1000, 2)
    return {
        "status": "success",
        "session_id": session_id or "session_edge",
        "turn_id": turn_id,
        "caller_id": caller_id,
        "raw_transcript": result.raw_transcript,
        "masked_transcript": result.masked_transcript,
        "redacted_pii": result.redacted_pii,
        "latency_ms": latency_ms,
        "language": result.detected_language,
        "engine": result.engine,
    }


@app.get("/api/claims/{claim_id}")
def get_claim_details(claim_id: str):
    """Fetch authoritative claim details and staged/committed dispatches."""
    claim = get_claim_db(claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail=f"Claim {claim_id} not found")
    dispatches = get_dispatches_by_claim_db(claim_id)
    return {"claim": claim, "dispatches": dispatches}


@app.get("/api/sessions/{session_id}/state")
def get_session_state(session_id: str):
    """Fetch live Commit Window status and action transitions for a session."""
    cw = get_commit_window()
    return {
        "session_id": session_id,
        "held_actions": cw.get_held_actions(session_id),
        "all_actions": cw.get_all_actions(session_id),
        "transitions": cw.get_transitions(session_id),
    }


@app.get("/api/mock/turn")
def get_mock_turn():
    """Mock endpoint for supervisor UI (Ojas) and evals (Pratham) local development."""
    return {
        "session_id": "mock-sess-demo",
        "turn_id": 3,
        "agent_response": "Understood. I have cancelled the tow truck dispatch. Your claim remains active under policy NH-8821.",
        "state_machine": {
            "held_actions": [],
            "transitions": [
                {
                    "action_id": "act_tow_01",
                    "action_type": "stage_dispatch",
                    "from_state": "FROZEN",
                    "to_state": "ABORTED",
                    "reason": "Caller revocation verified at turn 3",
                }
            ],
        },
        "current_claim": {
            "claim_id": "CLM-40192",
            "status": "OPEN_UNASSIGNED",
            "deductible_inr": 1500,
            "locked_fields": ["deductible_inr", "liability_ratio"],
        },
    }


# -----------------------------------------------------------------------------
# WebSocket Route for Supervisor Console
# -----------------------------------------------------------------------------

@app.websocket("/ws/session/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(session_id, websocket)
    cw = get_commit_window()
    # Send initial state immediately
    await websocket.send_text(json.dumps({
        "type": "INITIAL_STATE",
        "session_id": session_id,
        "held_actions": cw.get_held_actions(session_id),
        "transitions": cw.get_transitions(session_id),
    }))
    try:
        while True:
            # Keep connection open and receive supervisor commands if any
            data = await websocket.receive_text()
            logger.info(f"Received WS message from console for session {session_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(session_id, websocket)


@app.websocket("/ws/live")
async def live_websocket_endpoint(websocket: WebSocket):
    """Global WebSocket feed for the judge backend viewer."""
    await manager.connect("live", websocket)
    await websocket.send_text(json.dumps({
        "type": "INITIAL_STATE",
        "session_id": "live-stream",
        "status": "connected",
        "message": "Connected to ClaimGuard Real-Time Live Inspection Stream",
    }))
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received WS message on /ws/live: {data}")
    except WebSocketDisconnect:
        manager.disconnect("live", websocket)


@app.post("/api/session/reset")
def reset_demo_session(session_id: Optional[str] = "demo-session"):
    """Reset session commit window and active claim state for clean demo restarts."""
    cw = get_commit_window()
    cw.clear_session(session_id)
    runner = get_agent_runner()
    runner._conversations.pop(session_id, None)
    runner._session_claims.pop(session_id, None)
    runner._session_policies.pop(session_id, None)
    runner._session_naive_committed.pop(session_id, None)
    return {"status": "reset", "session_id": session_id}
