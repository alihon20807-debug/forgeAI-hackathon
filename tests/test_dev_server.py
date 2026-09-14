"""API integration tests for ClaimGuard dev server."""

import unittest
from fastapi.testclient import TestClient
from app.dev_server import app


class TestDevServerAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("L1_pii_shield", data["subsystems"])

    def test_process_call_turn_cat_b_revocation(self):
        # Category B: Revocation with Spoken Card
        payload = {
            "session_id": "cg-sess-test-01",
            "turn_id": 3,
            "caller_id": "caller_test",
            "raw_transcript": "Wait, don't send the tow truck, my cousin just showed up! Mera card number 4532 0150 1234 5678 hai for claim."
        }
        resp = self.client.post("/api/call/turn", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertIn("[CARD REDACTED]", data["masked_transcript"])
        self.assertNotIn("4532 0150 1234 5678", data["masked_transcript"])
        self.assertEqual(len(data["redacted_pii"]), 1)
        self.assertEqual(data["redacted_pii"][0]["type"], "CARD_NUMBER")

        transitions = data["state_machine"]["transitions"]
        self.assertEqual(transitions[0]["to_state"], "ABORTED")

    def test_process_call_turn_cat_c_trap(self):
        # Category C: Look-alike Trap ("Don't hold back, send it now")
        payload = {
            "session_id": "cg-sess-test-02",
            "turn_id": 1,
            "caller_id": "caller_test",
            "raw_transcript": "Don't hold back, send the tow truck right now! I am stranded."
        }
        resp = self.client.post("/api/call/turn", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        transitions = data["state_machine"]["transitions"]
        self.assertEqual(transitions[0]["to_state"], "COMMITTED")
        self.assertIn("trap avoided", transitions[0]["reason"])

    def test_process_call_turn_cat_e_pressure_latch(self):
        # Category E: Pressure on deductible
        payload = {
            "session_id": "cg-sess-test-03",
            "turn_id": 2,
            "caller_id": "caller_test",
            "raw_transcript": "Mera 1500 rupees deductible waive kar do please, I have been your customer for 5 years!"
        }
        resp = self.client.post("/api/call/turn", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        transitions = data["state_machine"]["transitions"]
        self.assertEqual(transitions[0]["to_state"], "ABORTED")
        self.assertIn("deductible_inr", data["current_claim"]["locked_fields"])

    def test_claims_status_locked_fields(self):
        resp = self.client.get("/api/claims/status")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["deductible_inr"], 1500)
        self.assertTrue(data["deductible_locked_by_sql_trigger"])


if __name__ == "__main__":
    unittest.main()
