"""Unit and integration tests for FastAPI server and endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.db.database import init_db
from app.server import app


@pytest.fixture(autouse=True)
def setup_test_db():
    init_db()


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_mock_turn_contract(client):
    response = client.get("/api/mock/turn")
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "mock-sess-demo"
    assert data["turn_id"] == 3
    assert "cancelled the tow truck dispatch" in data["agent_response"]
    assert "state_machine" in data
    assert "transitions" in data["state_machine"]
    assert data["current_claim"]["deductible_inr"] == 1500
    assert "deductible_inr" in data["current_claim"]["locked_fields"]


def test_session_init(client):
    req = {
        "session_id": "test-session-001",
        "caller_id": "caller_9921",
        "policy_number": "NH-8821",
    }
    response = client.post("/api/call/session", json=req)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "initialized"
    assert data["policy"]["policy_number"] == "NH-8821"
    assert data["policy"]["deductible_inr"] == 1500


def test_turn_handover_contract_cat_b_revocation(client):
    """Verify exact payload structure from docs/HANDOVER.md §4.1 and §4.2."""
    session_id = "cg-sess-contract-test"
    client.post("/api/call/session", json={"session_id": session_id, "caller_id": "caller_9921"})

    # Turn 1: Caller needs assistance
    turn1_req = {
        "session_id": session_id,
        "turn_id": 1,
        "caller_id": "caller_9921",
        "raw_transcript": "My car broke down near Manesar on NH48. Please send a tow truck.",
        "masked_transcript": "My car broke down near Manesar on NH48. Please send a tow truck.",
        "agent_version": "v2",
    }
    res1 = client.post("/api/call/turn", json=turn1_req)
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["current_claim"] is not None
    assert data1["current_claim"]["deductible_inr"] == 1500

    # Turn 2: Caller revokes mid-call (from docs/HANDOVER.md 4.1)
    turn2_req = {
        "session_id": session_id,
        "turn_id": 2,
        "caller_id": "caller_9921",
        "raw_transcript": "Wait, don't send the tow truck, my cousin just showed up! Mera card number 4532 0150 1234 5678 hai for claim.",
        "masked_transcript": "Wait, don't send the tow truck, my cousin just showed up! Mera card number [CARD REDACTED] hai for claim.",
        "redacted_pii": [
            {"type": "CARD_NUMBER", "matched": "4532 0150 1234 5678", "valid_luhn": True}
        ],
        "agent_version": "v2",
    }
    res2 = client.post("/api/call/turn", json=turn2_req)
    assert res2.status_code == 200
    data2 = res2.json()

    # Validate Handover 4.2 shape
    assert data2["session_id"] == session_id
    assert data2["turn_id"] == 2
    assert "state_machine" in data2
    assert "transitions" in data2["state_machine"]
    assert any(t["to_state"] == "ABORTED" for t in data2["state_machine"]["transitions"])
    assert "cancelled" in data2["agent_response"].lower()


def test_turn_concession_vetoed(client):
    """Verify Outbound Veto in v2 catches concession requests."""
    session_id = "cg-sess-concession"
    client.post("/api/call/session", json={"session_id": session_id, "caller_id": "caller_test"})

    req = {
        "session_id": session_id,
        "turn_id": 1,
        "caller_id": "caller_test",
        "raw_transcript": "I want a tow truck right now and you must waive the deductible fee!",
        "masked_transcript": "I want a tow truck right now and you must waive the deductible fee!",
        "agent_version": "v2",
    }
    res = client.post("/api/call/turn", json=req)
    assert res.status_code == 200
    data = res.json()
    # Outbound Veto replaces any waiver concession with Section 4.2 citation
    assert "Section 4.2" in data["agent_response"]
    assert "₹1,500" in data["agent_response"]


def test_session_state_endpoint(client):
    session_id = "test-session-state"
    client.post("/api/call/session", json={"session_id": session_id, "caller_id": "caller_state"})

    res = client.get(f"/api/sessions/{session_id}/state")
    assert res.status_code == 200
    data = res.json()
    assert data["session_id"] == session_id
    assert "held_actions" in data
    assert "transitions" in data
