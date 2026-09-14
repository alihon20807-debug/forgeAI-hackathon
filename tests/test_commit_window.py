"""Unit tests for the Commit Window state machine."""

import pytest
from app.enforcement.commit_window import (
    CommitWindow,
    ActionState,
)


@pytest.fixture
def cw():
    return CommitWindow()


def test_stage_action_starts_held(cw):
    action = cw.stage_action(
        session_id="sess-001",
        action_type="stage_dispatch",
        payload={"service_type": "towing", "pickup_location": "NH48 Km 62"},
        action_id="act_tow_01",
    )
    assert action.state == ActionState.HELD
    assert action.action_id == "act_tow_01"

    held = cw.get_held_actions("sess-001")
    assert len(held) == 1
    assert held[0]["action_id"] == "act_tow_01"


def test_freeze_trigger_detection(cw):
    assert cw.detect_freeze_trigger("Wait, hold on a second") == "wait"
    assert cw.detect_freeze_trigger("Ruko mat bhejo abhi") == "ruko"
    assert cw.detect_freeze_trigger("Please cancel the tow truck") == "cancel"
    assert cw.detect_freeze_trigger("Bhai rehne do abhi") == "rehne do"
    assert cw.detect_freeze_trigger("Everything is fine, go ahead") is None


def test_turn_freeze_and_abort_on_revocation(cw):
    """Category B: True revocation mid-call."""
    cw.stage_action(
        session_id="sess-revocation",
        action_type="stage_dispatch",
        payload={"service_type": "towing"},
        action_id="act_tow_revoc",
    )

    transcript = "Wait, don't send the tow truck, my cousin just showed up!"
    transitions, trigger = cw.process_turn_intent("sess-revocation", transcript)

    assert trigger == "wait"
    assert len(transitions) >= 1
    # Check that final transition ended in ABORTED
    abort_trans = [t for t in transitions if t.to_state == "ABORTED"]
    assert len(abort_trans) == 1
    assert abort_trans[0].action_id == "act_tow_revoc"

    all_actions = cw.get_all_actions("sess-revocation")
    assert all_actions[0]["state"] == "ABORTED"
    # Uncommitted held actions should now be empty
    assert len(cw.get_held_actions("sess-revocation")) == 0


def test_lookalike_trap_resolves_to_committed(cw):
    """Category C: Look-alike trap ('don't hold back, send it now')."""
    cw.stage_action(
        session_id="sess-trap",
        action_type="stage_dispatch",
        payload={"service_type": "towing"},
        action_id="act_tow_trap",
    )

    transcript = "Please don't hold back, send it now!"
    transitions, trigger = cw.process_turn_intent("sess-trap", transcript)

    assert trigger is not None  # "hold back" tripped safety freeze
    commit_trans = [t for t in transitions if t.to_state == "COMMITTED"]
    assert len(commit_trans) == 1
    assert "look-alike" in commit_trans[0].reason.lower()

    all_actions = cw.get_all_actions("sess-trap")
    assert all_actions[0]["state"] == "COMMITTED"


def test_normal_uninterrupted_call_commits(cw):
    """Category A: Clean control."""
    cw.stage_action(
        session_id="sess-clean",
        action_type="stage_dispatch",
        payload={"service_type": "towing"},
        action_id="act_tow_clean",
    )

    transcript = "Yes, please send the tow truck to Km 62 Manesar."
    transitions, trigger = cw.process_turn_intent("sess-clean", transcript)
    assert trigger is None

    # Commit at end of turn grace window
    commit_transitions = cw.commit_held_actions("sess-clean")
    assert len(commit_transitions) == 1
    assert commit_transitions[0].to_state == "COMMITTED"
