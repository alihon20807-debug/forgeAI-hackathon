"""Unit tests for ClaimGuard Voice Transcriber and prompt biasing."""

import unittest
from app.voice.transcriber import VoiceTranscriber, HINDI_FNOL_PROMPT_BIAS, GOLDEN_MOCK_SCENARIOS


class TestVoiceTranscriber(unittest.TestCase):
    def setUp(self):
        self.transcriber = VoiceTranscriber(force_mock=True)

    def test_mock_transcribe_audio_bytes_pii_shielding(self):
        # Transcribing simulated audio should return mock turns and mask PII
        # Golden scenario B has card number 4532 0150 1234 5678
        # Rotate until scenario B is processed
        found_b = False
        for _ in range(len(GOLDEN_MOCK_SCENARIOS) + 1):
            res = self.transcriber.transcribe_audio_bytes(b"\x00" * 200)
            if "cousin just showed up" in res.raw_transcript:
                found_b = True
                self.assertIn("[CARD REDACTED]", res.masked_transcript)
                self.assertNotIn("4532 0150 1234 5678", res.masked_transcript)
                self.assertEqual(len(res.redacted_pii), 1)
                self.assertEqual(res.redacted_pii[0]["type"], "CARD_NUMBER")
                break
        self.assertTrue(found_b, "Did not encounter Scenario B in golden mock rotation")

    def test_process_text_turn(self):
        text = "Caller said: contact +91 98765 43210 immediately for tow truck."
        res = self.transcriber.process_text_turn(text)

        self.assertIn("[PHONE REDACTED]", res.masked_transcript)
        self.assertEqual(len(res.redacted_pii), 1)
        self.assertEqual(res.redacted_pii[0]["type"], "PHONE_NUMBER")

    def test_prompt_bias_contains_key_terms(self):
        self.assertIn("ClaimGuard", HINDI_FNOL_PROMPT_BIAS)
        self.assertIn("NH48", HINDI_FNOL_PROMPT_BIAS)
        self.assertIn("Tow truck", HINDI_FNOL_PROMPT_BIAS)
        self.assertIn("नमस्ते", HINDI_FNOL_PROMPT_BIAS)


if __name__ == "__main__":
    unittest.main()
