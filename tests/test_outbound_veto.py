"""Unit tests for the Outbound Veto filter."""

import pytest
from app.enforcement.outbound_veto import OutboundVeto


@pytest.fixture
def veto():
    return OutboundVeto(default_policy_number="NH-8821", default_deductible_inr=1500)


def test_clean_grounded_response_passes(veto):
    text = "Your policy NH-8821 has a standard deductible of ₹1,500. A tow truck has been dispatched."
    result = veto.verify_and_filter(text)
    assert result.passed is True
    assert result.filtered_text == text
    assert len(result.veto_reasons) == 0


def test_concession_phrase_english_vetoed(veto):
    text = "Since this is an emergency, we will waive the deductible for you today."
    result = veto.verify_and_filter(text)
    assert result.passed is False
    assert "Section 4.2 of Policy NH-8821" in result.filtered_text
    assert "₹1,500" in result.filtered_text
    assert any("concession" in r.lower() for r in result.veto_reasons)


def test_concession_phrase_no_charge_vetoed(veto):
    text = "Don't worry sir, there is no charge for you at all."
    result = veto.verify_and_filter(text)
    assert result.passed is False
    assert "Section 4.2" in result.filtered_text


def test_concession_hindi_codemixed_vetoed(veto):
    text = "Aap fikar mat karo, hum deductible maaf kar denge aur koi charge nahi lagega."
    result = veto.verify_and_filter(text)
    assert result.passed is False
    assert "Section 4.2" in result.filtered_text


def test_phantom_rupee_amount_vetoed(veto):
    # ₹9,999 is not in the allowed policy figures or rate card
    text = "The special emergency crane dispatch will cost ₹9,999."
    result = veto.verify_and_filter(text)
    assert result.passed is False
    assert any("Phantom rupee amount" in r for r in result.veto_reasons)
    assert "Section 4.2" in result.filtered_text


def test_allowed_rupee_amount_from_context_passes(veto):
    context_chunk = "Emergency winch service incurs an authorized fee of ₹750."
    text = "The technician charges an authorized fee of ₹750 for winch extraction."
    result = veto.verify_and_filter(text, context_chunks=[context_chunk])
    assert result.passed is True
    assert result.filtered_text == text
