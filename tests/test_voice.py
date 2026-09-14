"""Unit tests for ClaimGuard Voice Transcriber and prompt biasing."""

import unittest
from app.voice.transcriber import VoiceTranscriber, HINDI_FNOL_PROMPT_BIAS, GOLDEN_MOCK_SCENARIOS


class TestVoiceTranscriber(unittest.TestCase):
    def setUp(self):
        self.transcriber = VoiceTranscriber(force_mock=True)

    def test_mock_transcribe_audio_bytes_pii_shielding(self):
        # Transcribing simulated audio should return mock turns and mask PII
        # Golden scenario B has card number 4111 1111 1111 1111
        # Rotate until scenario B is processed
        found_b = False
        for _ in range(len(GOLDEN_MOCK_SCENARIOS) + 1):
            res = self.transcriber.transcribe_audio_bytes(b"\x00" * 200)
            if "cousin just showed up" in res.raw_transcript:
                found_b = True
                self.assertIn("[CARD REDACTED]", res.masked_transcript)
                self.assertNotIn("4111 1111 1111 1111", res.masked_transcript)
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

    def test_audio_manifest_integrity(self):
        import json
        from pathlib import Path
        repo_root = Path(__file__).resolve().parent.parent
        manifest_file = repo_root / "assets" / "audio" / "manifest.json"
        self.assertTrue(manifest_file.exists(), "manifest.json does not exist")

        with open(manifest_file, "r", encoding="utf-8") as f:
            specs = json.load(f)

        self.assertGreaterEqual(len(specs), 20, "Should have at least 20 audio specs")
        for s in specs:
            filepath = s.get("filepath", "")
            self.assertFalse(filepath.startswith("C:"), f"Absolute Windows path leaked: {filepath}")
            self.assertTrue(filepath.startswith("assets/audio/"), f"Expected relative path: {filepath}")
            actual_file = repo_root / filepath
            self.assertTrue(actual_file.exists(), f"Referenced audio file missing: {filepath}")
            self.assertGreater(actual_file.stat().st_size, 1000, f"File too small: {filepath}")


if __name__ == "__main__":
    unittest.main()
