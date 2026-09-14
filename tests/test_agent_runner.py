"""Unit tests for AgentRunner: tool calling, state management, and fallback resilience."""

import json
import pytest
from unittest.mock import AsyncMock, patch

from app.agent.runner import AgentRunner
from app.db.database import init_db


@pytest.fixture(autouse=True)
def setup_db():
    init_db()


def test_safe_parse_json():
    """Verify _safe_parse_json handles raw dicts, valid JSON, markdown wrappers, and invalid JSON."""
    runner = AgentRunner(use_mock=True)

    # 1. Already dict
    assert runner._safe_parse_json({"key": "val"}) == {"key": "val"}

    # 2. Clean JSON string
    assert runner._safe_parse_json('{"policy_number": "NH-8821"}') == {"policy_number": "NH-8821"}

    # 3. Markdown fenced code block
    fenced = "```json\n{\"incident_location\": \"NH48\"}\n```"
    assert runner._safe_parse_json(fenced) == {"incident_location": "NH48"}

    # 4. Plain triple backtick fence
    plain_fence = "```\n{\"eta_minutes\": 20}\n```"
    assert runner._safe_parse_json(plain_fence) == {"eta_minutes": 20}

    # 5. Invalid JSON string
    assert runner._safe_parse_json("not valid json at all") == {}

    # 6. Empty / None
    assert runner._safe_parse_json("") == {}
    assert runner._safe_parse_json(None) == {}


@pytest.mark.asyncio
async def test_mock_turn_clean_and_revocation():
    """Verify process_turn in mock mode handles initial breakdown and mid-call revocation."""
    runner = AgentRunner(use_mock=True)
    session_id = "test-runner-sess-01"

    # Turn 1: Caller needs tow truck
    res1 = await runner.process_turn(
        session_id=session_id,
        turn_id=1,
        caller_id="caller_01",
        raw_transcript="Car broke down on NH48, need a tow truck.",
        masked_transcript="Car broke down on NH48, need a tow truck.",
        agent_version="v2",
    )
    assert res1["session_id"] == session_id
    assert res1["turn_id"] == 1
    assert "tow truck" in res1["agent_response"].lower()
    assert res1["current_claim"] is not None
    assert res1["current_claim"]["deductible_inr"] == 1500

    # Turn 2: Caller revokes mid-call
    res2 = await runner.process_turn(
        session_id=session_id,
        turn_id=2,
        caller_id="caller_01",
        raw_transcript="Wait, don't send the tow truck, my cousin just showed up!",
        masked_transcript="Wait, don't send the tow truck, my cousin just showed up!",
        agent_version="v2",
    )
    assert "cancelled" in res2["agent_response"].lower()
    transitions = res2["state_machine"]["transitions"]
    assert any(t["to_state"] == "ABORTED" for t in transitions)


@pytest.mark.asyncio
async def test_llm_tool_calling_simulation():
    """Verify LLM tool execution loop when model returns tool calls."""
    runner = AgentRunner(use_mock=False)
    session_id = "test-llm-tool-sess"

    mock_tool_call_response = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": "call_open_1",
                            "type": "function",
                            "function": {
                                "name": "open_claim",
                                "arguments": json.dumps({
                                    "policy_number": "NH-8821",
                                    "incident_location": "NH48 Km 62 near Manesar",
                                    "incident_description": "Engine overheating",
                                }),
                            },
                        },
                        {
                            "id": "call_dispatch_2",
                            "type": "function",
                            "function": {
                                "name": "stage_dispatch",
                                "arguments": json.dumps({
                                    "service_type": "towing",
                                    "pickup_location": "NH48 Km 62 near Manesar",
                                    # Note: claim_id omitted to test auto-injection
                                }),
                            },
                        },
                    ],
                }
            }
        ]
    }

    mock_final_reply = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Claim has been opened and a tow truck is staged to NH48 Km 62.",
                }
            }
        ]
    }

    with patch.object(runner, "_call_llm", AsyncMock(side_effect=[mock_tool_call_response, mock_final_reply])):
        res = await runner.process_turn(
            session_id=session_id,
            turn_id=1,
            caller_id="caller_sim",
            raw_transcript="I am stuck near Manesar, please send a tow truck.",
            masked_transcript="I am stuck near Manesar, please send a tow truck.",
            agent_version="v2",
        )

        assert res["session_id"] == session_id
        assert "staged" in res["agent_response"]
        assert session_id in runner._session_claims
        assert runner._session_claims[session_id].startswith("CLM-")
        assert res["current_claim"] is not None
        assert res["current_claim"]["claim_id"] == runner._session_claims[session_id]


@pytest.mark.asyncio
async def test_llm_failure_resilience_fallback():
    """Verify that if the LLM endpoint is unreachable, AgentRunner gracefully falls back to mock."""
    runner = AgentRunner(use_mock=False)
    session_id = "test-llm-fail-sess"

    with patch.object(runner, "_call_llm", AsyncMock(side_effect=ConnectionError("llama-server offline"))):
        res = await runner.process_turn(
            session_id=session_id,
            turn_id=1,
            caller_id="caller_fail",
            raw_transcript="My car broke down near Manesar.",
            masked_transcript="My car broke down near Manesar.",
            agent_version="v2",
        )
        # Verify fallback succeeded and did not raise an exception
        assert res["session_id"] == session_id
        assert len(res["agent_response"]) > 0
