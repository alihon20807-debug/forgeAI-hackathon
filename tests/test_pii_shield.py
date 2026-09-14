"""Unit tests for ClaimGuard PII Shield (Luhn, Verhoeff, Indian Phone)."""

import unittest
from app.security.pii_shield import (
    PIIShield,
    generate_verhoeff_check_digit,
    redact_pii,
    validate_luhn,
    validate_verhoeff,
)


class TestPIIShield(unittest.TestCase):
    def setUp(self):
        self.shield = PIIShield()

    # -------------------------------------------------------------
    # 1. Luhn Algorithm Unit Tests
    # -------------------------------------------------------------
    def test_luhn_valid_cards(self):
        # Known valid credit cards (test / synthetic numbers)
        valid_cards = [
            "4532015012345671",      # Visa 16 digits (checksum = 1)
            "4532 0150 1234 5671",  # Visa with spaces
            "4532-0150-1234-5671",  # Visa with dashes
            "4532 0150 1234 5678",  # Handover brief canonical test card
            "5412751234123452",      # Mastercard 16 digits
            "378282246310005",       # Amex 15 digits
            "6011111111111117",      # Discover 16 digits
            "6521501234567810",      # RuPay test format
        ]
        for card in valid_cards:
            with self.subTest(card=card):
                self.assertTrue(validate_luhn(card), f"Failed for valid card: {card}")

    def test_luhn_invalid_cards(self):
        # Numbers failing Luhn check
        invalid_cards = [
            "4532015012345679",      # 1 off from valid Visa
            "1111222233334445",      # Fails Luhn (sum = 61)
            "1234567890123456",      # Random 16 digits (fails Luhn)
            "12345",                 # Too short (<13 digits)
            "123456789012345678901", # Too long (>19 digits)
        ]
        for card in invalid_cards:
            with self.subTest(card=card):
                self.assertFalse(validate_luhn(card), f"Expected false for invalid card: {card}")

    # -------------------------------------------------------------
    # 2. Verhoeff Algorithm Unit Tests (Aadhaar)
    # -------------------------------------------------------------
    def test_verhoeff_calculation_and_validation(self):
        # 11-digit Aadhaar prefixes starting with 2-9
        prefixes = ["36759834601", "28914562093", "98123456789"]
        for prefix in prefixes:
            check_digit = generate_verhoeff_check_digit(prefix)
            full_aadhaar = f"{prefix}{check_digit}"
            self.assertTrue(validate_verhoeff(full_aadhaar), f"Generated valid Aadhaar must pass: {full_aadhaar}")

            # Corrupting the last digit must fail
            corrupted = f"{prefix}{(check_digit + 1) % 10}"
            self.assertFalse(validate_verhoeff(corrupted), f"Corrupted check digit must fail: {corrupted}")

    def test_verhoeff_disallows_zero_or_one_prefix(self):
        # Invariant: Aadhaar numbers never start with 0 or 1
        prefix = "01234567890"
        check_digit = generate_verhoeff_check_digit(prefix)
        self.assertFalse(validate_verhoeff(f"{prefix}{check_digit}"))

        prefix = "11234567890"
        check_digit = generate_verhoeff_check_digit(prefix)
        self.assertFalse(validate_verhoeff(f"{prefix}{check_digit}"))

    # -------------------------------------------------------------
    # 3. Transcript Masking: Cards, Aadhaar, Phone
    # -------------------------------------------------------------
    def test_redact_card_in_fnol_transcript(self):
        # Example from docs/HANDOVER.md §4.1
        raw = "Wait, don't send the tow truck, my cousin just showed up! Mera card number 4532 0150 1234 5678 hai for claim."
        result = self.shield.mask(raw)

        self.assertIn("[CARD REDACTED]", result.masked_transcript)
        self.assertNotIn("4532 0150 1234 5678", result.masked_transcript)
        self.assertEqual(len(result.redacted_pii), 1)
        self.assertEqual(result.redacted_pii[0].type, "CARD_NUMBER")
        self.assertTrue(result.redacted_pii[0].valid_luhn)

    def test_redact_aadhaar_in_transcript(self):
        # Generate valid synthetic Aadhaar
        prefix = "36759834601"
        check_digit = generate_verhoeff_check_digit(prefix)
        valid_aadhaar_spaced = f"{prefix[:4]} {prefix[4:8]} {prefix[8:]}{check_digit}"

        raw = f"Aadhaar number note kar lijiye: {valid_aadhaar_spaced} verify karne ke liye."
        result = self.shield.mask(raw)

        self.assertIn("[AADHAAR REDACTED]", result.masked_transcript)
        self.assertNotIn(valid_aadhaar_spaced, result.masked_transcript)
        self.assertEqual(len(result.redacted_pii), 1)
        self.assertEqual(result.redacted_pii[0].type, "AADHAAR_NUMBER")
        self.assertTrue(result.redacted_pii[0].valid_verhoeff)

    def test_redact_phone_numbers(self):
        cases = [
            ("Call me at +91 98765 43210 immediately.", "[PHONE REDACTED]"),
            ("Mera contact number 09876543210 hai.", "[PHONE REDACTED]"),
            ("Alternative number: 9123456789.", "[PHONE REDACTED]"),
            ("+91-8877665544 par update bhejo.", "[PHONE REDACTED]"),
        ]
        for raw, expected_token in cases:
            with self.subTest(raw=raw):
                res = self.shield.mask(raw)
                self.assertIn(expected_token, res.masked_transcript)
                self.assertEqual(res.redacted_pii[0].type, "PHONE_NUMBER")

    def test_multiple_pii_in_single_turn(self):
        # Multiple sensitive identifiers in one turn
        raw = "Mera card 4532-0150-1234-5671 aur phone +91 98765 43210 note karo."
        res = self.shield.mask(raw)

        self.assertEqual(
            res.masked_transcript,
            "Mera card [CARD REDACTED] aur phone [PHONE REDACTED] note karo."
        )
        self.assertEqual(len(res.redacted_pii), 2)
        types = [item.type for item in res.redacted_pii]
        self.assertIn("CARD_NUMBER", types)
        self.assertIn("PHONE_NUMBER", types)

    # -------------------------------------------------------------
    # 4. Negative Controls / Non-PII Safeguards
    # -------------------------------------------------------------
    def test_pin_codes_not_redacted(self):
        raw = "Mera location Bangalore pin code 560001 hai near MG Road."
        res = self.shield.mask(raw)
        self.assertEqual(res.masked_transcript, raw)
        self.assertEqual(len(res.redacted_pii), 0)

    def test_policy_and_claim_ids_not_redacted(self):
        raw = "Policy number NH-8821 under claim CLM-40192 deductible is 1500."
        res = self.shield.mask(raw)
        self.assertEqual(res.masked_transcript, raw)
        self.assertEqual(len(res.redacted_pii), 0)

    def test_invalid_card_failing_luhn_not_redacted(self):
        # A 16 digit number that fails Luhn shouldn't be tagged as CARD
        # e.g., tracking ID or random hardware ID
        raw = "Tracking number 1234 5678 9012 3456 has been generated."
        # Confirm it fails Luhn
        self.assertFalse(validate_luhn("1234 5678 9012 3456"))
        res = self.shield.mask(raw)
        # Should not have [CARD REDACTED]
        self.assertNotIn("[CARD REDACTED]", res.masked_transcript)

    def test_convenience_function(self):
        res = redact_pii("Card 4532 0150 1234 5678")
        self.assertIn("[CARD REDACTED]", res.masked_transcript)


if __name__ == "__main__":
    unittest.main()
