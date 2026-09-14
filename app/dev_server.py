"""ClaimGuard Local Development Server for Pratham.

Provides:
- Static file serving for the Live Supervisor Console (frontend/).
- REST API turn endpoints matching HANDOVER.md §4.
- Pre-LLM mathematical PII scrubbing on all incoming turns.
- Standalone development without depending on Ali's machine being online.
"""

from __future__ import annotations

import os
from typing import Any, List, Optional
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.security.pii_shield import PIIShield, redact_pii
from app.voice.transcriber import VoiceTranscriber, get_default_transcriber

app = FastAPI(
    title="ClaimGuard × PRISM — Supervisor & Edge Dev Server",
    version="1.0.0",
    description="L0 Client Edge, L1 Perception STT & L6 Human Supervisor Console endpoints."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TurnRequest(BaseModel):
    session_id: str
    turn_id: int
    caller_id: str
    raw_transcript: str
    masked_transcript: Optional[str] = None
    redacted_pii: Optional[List[dict[str, Any]]] = None


class StateTransition(BaseModel):
    action_id: str
    action_type: str
    from_state: str
    to_state: str
    reason: str


class ClaimState(BaseModel):
    claim_id: str
    status: str
    deductible_inr: int
    locked_fields: List[str]


class TurnResponse(BaseModel):
    session_id: str
    turn_id: int
    raw_transcript: str
    masked_transcript: str
    redacted_pii: List[dict[str, Any]]
    agent_response: str
    state_machine: dict[str, Any]
    current_claim: ClaimState


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "subsystems": {
            "L0_edge": "ready",
            "L1_perception": "faster-whisper-ready",
            "L1_pii_shield": "luhn-verhoeff-active",
            "L6_console": "mounted",
        }
    }


@app.post("/api/call/turn", response_model=TurnResponse)
def process_call_turn(payload: TurnRequest):
    """Client -> Server Turn Request matching HANDOVER.md §4.1.
    Applies mathematical PII scrubbing before any downstream logic.
    """
    # Invariant 2: Mathematical PII scrubbing pre-LLM, pre-telemetry
    redaction = redact_pii(payload.raw_transcript)
    masked_text = redaction.masked_transcript
    redacted_items = [p.to_dict() for p in redaction.redacted_pii]

    # Deterministic Commit Window resolution simulation
    transitions: List[dict[str, Any]] = []
    lower_text = payload.raw_transcript.lower()

    if any(k in lower_text for k in ["don't send", "dont send", "cancel", "ruk jao", "nahi chahiye", "cousin just showed"]):
        # Cat B / Revocation
        transitions.append({
            "action_id": "act_tow_01",
            "action_type": "stage_dispatch",
            "from_state": "FROZEN",
            "to_state": "ABORTED",
            "reason": f"Caller revocation verified at turn {payload.turn_id}"
        })
        agent_resp = f"Understood. I have cancelled the tow truck dispatch. Your claim remains active under policy NH-8821 with zero charges."
        claim_status = "OPEN_DISPATCH_CANCELLED"

    elif "don't hold back" in lower_text or "dont hold back" in lower_text:
        # Cat C / Look-alike trap
        transitions.append({
            "action_id": "act_tow_02",
            "action_type": "stage_dispatch",
            "from_state": "FROZEN",
            "to_state": "COMMITTED",
            "reason": "Semantic resolution: Affirmative urgency trap avoided"
        })
        agent_resp = "Confirmed. Emergency flatbed tow truck is locked in and dispatched to your location on NH48."
        claim_status = "DISPATCH_EN_ROUTE"

    elif "waive" in lower_text and "deductible" in lower_text:
        # Cat E / Pressure & Policy Latch
        transitions.append({
            "action_id": "act_waiver_01",
            "action_type": "waive_deductible",
            "from_state": "HELD",
            "to_state": "ABORTED",
            "reason": "Policy Latch: Deductible is locked at DB trigger level (Policy NH-8821 §4.2)"
        })
        agent_resp = "Under Section 4.2 of Policy NH-8821, the compulsory standard deductible of ₹1,500 is latched by insurance regulations and cannot be waived. Cashless towing up to 45 km is 100% covered."
        claim_status = "OPEN_POLICY_ENFORCED"

    else:
        # Cat A / Clean Control
        transitions.append({
            "action_id": "act_tow_01",
            "action_type": "stage_dispatch",
            "from_state": "HELD",
            "to_state": "COMMITTED",
            "reason": "Clean turn completion: Grace window elapsed without cancellation cues"
        })
        agent_resp = "I have staged and confirmed an authorized flatbed tow truck to your location on NH48."
        claim_status = "DISPATCH_COMMITTED"

    return TurnResponse(
        session_id=payload.session_id,
        turn_id=payload.turn_id,
        raw_transcript=payload.raw_transcript,
        masked_transcript=masked_text,
        redacted_pii=redacted_items,
        agent_response=agent_resp,
        state_machine={
            "held_actions": [],
            "transitions": transitions
        },
        current_claim=ClaimState(
            claim_id="CLM-40192",
            status=claim_status,
            deductible_inr=1500,
            locked_fields=["deductible_inr", "liability_ratio"]
        )
    )


@app.get("/api/claims/status")
def get_claim_status():
    """Returns active claim state and immutable fields."""
    return {
        "claim_id": "CLM-40192",
        "policy_id": "NH-8821",
        "insured_name": "Vikram Malhotra",
        "vehicle_reg": "DL 01 AB 1234",
        "corridor": "NH48 (Delhi-Gurgaon-Jaipur)",
        "deductible_inr": 1500,
        "deductible_locked_by_sql_trigger": True,
        "towing_allowance_km": 45,
        "status": "OPEN_UNASSIGNED"
    }


@app.post("/api/voice/transcribe")
async def transcribe_voice(
    audio: Optional[UploadFile] = File(None),
    raw_text: Optional[str] = Form(None)
):
    """Transcribes voice audio (or text fallback) and returns shielded transcript."""
    transcriber = get_default_transcriber()

    if audio is not None:
        content = await audio.read()
        res = transcriber.transcribe_audio_bytes(content, audio_format="wav")
    elif raw_text:
        res = transcriber.process_text_turn(raw_text)
    else:
        # Fallback simulation
        res = transcriber.transcribe_audio_bytes(b"\x00" * 200)

    return res.to_dict()


# Mount frontend static directory for instant local UI hosting
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    print("Starting ClaimGuard Local Dev Server on http://localhost:8000")
    uvicorn.run("app.dev_server:app", host="127.0.0.1", port=8000, reload=True)
