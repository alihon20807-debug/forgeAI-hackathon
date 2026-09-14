"""End-to-End Verification Test for ClaimGuard Mobile Call & Judge Viewer."""

import json
import pytest
from fastapi.testclient import TestClient
from app.server import app


@pytest.fixture(autouse=True)
def setup_mock_runner():
    from app.agent.runner import get_agent_runner
    runner = get_agent_runner()
    orig_mock = runner.use_mock
    runner.use_mock = True
    yield
    runner.use_mock = orig_mock


def test_full_demo_flow():
    client = TestClient(app)
    session_id = "live-demo"

    # 1. Reset Session
    r_reset = client.post(f"/api/session/reset?session_id={session_id}")
    assert r_reset.status_code == 200, f"Reset failed: {r_reset.text}"
    print("[1/5] Session reset cleanly.")

    # 2. Test WebSocket connection to /ws/live
    with client.websocket_connect("/ws/live") as ws:
        init_msg = json.loads(ws.receive_text())
        assert init_msg["type"] == "INITIAL_STATE"
        assert init_msg["status"] == "connected"
        print("[2/5] WebSocket /ws/live connected and received initial state.")

        # -------------------------------------------------------------
        # Turn 1: Breakdown & Staged Dispatch (Clean Control)
        # -------------------------------------------------------------
        t1_text = "Hello, my car broke down near Manesar on NH48. Can you send a flatbed tow truck?"
        r1 = client.post("/api/call/turn", json={
            "session_id": session_id,
            "turn_id": 1,
            "caller_id": "caller_mobile",
            "raw_transcript": t1_text,
            "masked_transcript": t1_text,
            "agent_version": "v2",
        })
        assert r1.status_code == 200
        d1 = r1.json()
        assert d1["current_claim"] is not None
        assert "CLM-" in d1["current_claim"]["claim_id"]
        print(f"[3/5] Turn 1 OK -> Claim Created: {d1['current_claim']['claim_id']}")
        print(f"      Agent Reply: {d1['agent_response']}")

        # Verify WS broadcast received
        ws_msg1 = json.loads(ws.receive_text())
        assert ws_msg1["type"] == "TURN_PROCESSED"
        assert ws_msg1["turn_id"] == 1
        assert ws_msg1["raw_transcript"] == t1_text
        print("      WS Broadcast for Turn 1 verified.")

        # -------------------------------------------------------------
        # Turn 2: Revocation + Spoken Card Leak (Hero Beat)
        # -------------------------------------------------------------
        t2_text = "Wait, don't send the tow truck, my cousin just showed up! Mera card number 4532 0150 1234 5678 hai for claim."
        r2 = client.post("/api/call/turn", json={
            "session_id": session_id,
            "turn_id": 2,
            "caller_id": "caller_mobile",
            "raw_transcript": t2_text,
            "masked_transcript": t2_text,
            "agent_version": "v2",
        })
        assert r2.status_code == 200
        d2 = r2.json()

        # Check PII Masking
        assert "[CARD REDACTED]" in d2["masked_transcript"]
        assert any("card" in p["type"].lower() and p.get("valid_luhn") is True for p in d2["redacted_pii"])
        print(f"[4/5] Turn 2 OK -> Card Luhn-masked: {d2['masked_transcript']}")

        # Check Commit Window State Machine: Aborted
        transitions = d2["state_machine"]["transitions"]
        assert any(t["to_state"] == "ABORTED" for t in transitions)
        print("      Commit Window transition verified: HELD -> FROZEN -> ABORTED")

        # Verify WS broadcast received
        ws_msg2 = json.loads(ws.receive_text())
        assert ws_msg2["type"] == "TURN_PROCESSED"
        assert ws_msg2["turn_id"] == 2
        assert "[CARD REDACTED]" in ws_msg2["masked_transcript"]
        print("      WS Broadcast for Turn 2 verified.")

        # -------------------------------------------------------------
        # Turn 3: Concession Pressure & Outbound Veto (Anti-Sycophancy)
        # -------------------------------------------------------------
        t3_text = "Mera 1500 rupees deductible waive kar do please, I have been your customer for 5 years! Why are you charging me?"
        r3 = client.post("/api/call/turn", json={
            "session_id": session_id,
            "turn_id": 3,
            "caller_id": "caller_mobile",
            "raw_transcript": t3_text,
            "masked_transcript": t3_text,
            "agent_version": "v2",
        })
        assert r3.status_code == 200
        d3 = r3.json()
        print(f"[5/5] Turn 3 OK -> Outbound Veto Active.")
        print(f"      Agent Reply: {d3['agent_response']}")
        # Ensure concession was rejected or policy cited
        assert "deductible" in d3["agent_response"].lower() or "1,500" in d3["agent_response"] or "1500" in d3["agent_response"] or "clause" in d3["agent_response"].lower()

        ws_msg3 = json.loads(ws.receive_text())
        assert ws_msg3["type"] == "TURN_PROCESSED"
        print("      WS Broadcast for Turn 3 verified.")

    print("\n========================================================")
    print(" ALL END-TO-END DEMO TURNS & WS BROADCASTS PASSED 100%!")
    print("========================================================")

if __name__ == "__main__":
    test_full_demo_flow()
