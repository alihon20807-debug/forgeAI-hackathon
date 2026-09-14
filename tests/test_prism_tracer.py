"""Unit tests for PRISM Observability Tracer."""

import json
from pathlib import Path
import pytest

from evals.checker import Evaluator
from app.db.database import init_db
from app.observability.prism_tracer import (
    PRISMTracer,
    TurnTracer,
    get_agent_id_for_version,
)


def test_agent_id_mapping():
    assert get_agent_id_for_version("v0") == "roadside-baseline"
    assert get_agent_id_for_version("v1") == "roadside-prompt-fix"
    assert get_agent_id_for_version("v2") == "roadside-claimguard"
    assert get_agent_id_for_version(None) == "roadside-claimguard"


def test_turn_tracer_spans_and_local_buffering(tmp_path):
    custom_tracer = PRISMTracer(
        host="https://prism.test",
        project_id="00000000-0000-0000-0000-000000000000",
        api_key="",  # No network call
    )

    tracer = TurnTracer(
        session_id="test-sess-prism",
        user_utterance="Tow chahiye near Manesar",
        agent_version="v2",
        category="A_CLEAN_CONTROL",
        eval_set="dev",
        tracer=custom_tracer,
    )

    with tracer.span(name="lookup_policy", span_type="tool") as rec:
        rec["output"] = {"policy": "NH-8821", "deductible": 1500}

    tracer.record_enforcement_transition(
        action_id="act_tow_01",
        action_type="stage_dispatch",
        from_state="HELD",
        to_state="COMMITTED",
        reason="Turn confirmed",
    )

    assert len(tracer.spans) == 2  # tool span + enforcement transition span

    tracer.finish(agent_reply="Aapka claim intimation ho gaya hai.")

    # Verify that local buffer file exists and contains valid JSON
    from app.observability.prism_tracer import TRACES_FILE
    assert TRACES_FILE.exists()
    with open(TRACES_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) >= 1
        last_trace = json.loads(lines[-1])
        assert last_trace["session_id"] == "test-sess-prism"
        assert last_trace["metadata"]["agent_id"] == "roadside-claimguard"
        assert len(last_trace["spans"]) == 3  # root + tool + enforcement


@pytest.mark.asyncio
async def test_evaluator_traces_masked_replay_text(monkeypatch, tmp_path):
    import app.observability.prism_tracer as prism_tracer

    trace_file = tmp_path / "traces.jsonl"
    monkeypatch.setattr(prism_tracer, "TRACES_FILE", trace_file)
    init_db()

    raw_card = "My card number is 4532 0150 1234 5678."
    await Evaluator(agent_version="v2", split_filter="dev", limit=1).evaluate_scenario(
        {
            "id": "security-regression",
            "category": "F_SPOKEN_IDENTIFIERS",
            "split": "dev",
            "turns": [raw_card],
        }
    )

    payload = json.loads(trace_file.read_text(encoding="utf-8").splitlines()[-1])
    assert raw_card not in trace_file.read_text(encoding="utf-8")
    assert payload["spans"][0]["input_text"] == "My card number is [CARD REDACTED]."


@pytest.mark.asyncio
async def test_benchmark_runner_traces_masked_replay_text(monkeypatch, tmp_path):
    from scripts.prism_benchmark import run_scenario
    import app.observability.prism_tracer as prism_tracer

    trace_file = tmp_path / "traces.jsonl"
    monkeypatch.setattr(prism_tracer, "TRACES_FILE", trace_file)

    class StubRunner:
        async def process_turn(self, **_kwargs):
            return {"agent_response": "ok", "state_machine": {"transitions": []}}

    raw_card = "My card number is 4532 0150 1234 5678."
    await run_scenario(
        {"id": "security-regression", "category": "F_SPOKEN_IDENTIFIERS", "split": "dev", "turns": [raw_card]},
        version="v2",
        runner=StubRunner(),
        tracer_client=PRISMTracer(api_key=""),
    )

    payload = json.loads(trace_file.read_text(encoding="utf-8").splitlines()[-1])
    assert raw_card not in trace_file.read_text(encoding="utf-8")
    assert payload["spans"][0]["input_text"] == "My card number is [CARD REDACTED]."
