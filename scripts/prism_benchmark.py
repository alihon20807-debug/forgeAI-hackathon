"""PRISM Benchmark Runner & Telemetry Ingestion Tool.

Supports:
1. --smoke: 3-call test run (1 Cat A, 1 Cat B, 1 Cat E) for credit consumption check.
2. --heldout: Runs all 20 held-out benchmark calls across v0, v1, and v2 with full span tags.
3. --export: Compiles buffered local JSONL traces into PRISM Import History JSON.
4. --status: Tests connectivity to PRISM ingest endpoint.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

from app.agent.runner import AgentRunner
from app.config import (
    DATA_DIR,
    PRISMTRACE_API_KEY,
    PRISMTRACE_HOST,
    PRISMTRACE_PROJECT_ID,
)
from app.observability.prism_tracer import PRISMTracer, TurnTracer
from app.security.pii_shield import redact_pii

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("claimguard.prism_runner")

REPLAY_SET_PATH = Path(__file__).resolve().parent.parent / "evals" / "replay_set.json"
TRACES_FILE = DATA_DIR / "prism_traces.jsonl"
EXPORT_FILE = DATA_DIR / "prism_traces_export.json"


def load_replay_set() -> Dict[str, Any]:
    with open(REPLAY_SET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def check_prism_connection(host: str, project_id: str, api_key: str) -> bool:
    """Send a lightweight diagnostic probe to PRISM."""
    if not api_key:
        logger.warning("No PRISMTRACE_API_KEY provided. Operating in local buffering mode.")
        return False

    url = f"{host.rstrip('/')}/api/spans/ingest"
    headers = {
        "X-PRISMtrace-Key": api_key,
        "Content-Type": "application/json",
    }
    probe_payload = {
        "trace_id": f"probe-{int(time.time())}",
        "project_id": project_id,
        "session_id": "probe-session",
        "metadata": {"type": "diagnostic_probe"},
        "spans": [],
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(url, json=probe_payload, headers=headers)
            logger.info(f"PRISM probe status: {resp.status_code}")
            if "X-PRISMtrace-Plan-Warning" in resp.headers:
                logger.warning(f"PRISM Plan Warning: {resp.headers['X-PRISMtrace-Plan-Warning']}")
            if resp.status_code in (200, 201):
                logger.info(f"PRISM endpoint healthy: {resp.text[:150]}")
                return True
            else:
                logger.warning(f"PRISM returned status {resp.status_code}: {resp.text[:200]}")
                return False
    except Exception as e:
        logger.error(f"Failed to connect to PRISM at {url}: {e}")
        return False


async def run_scenario(
    scenario: Dict[str, Any],
    version: str,
    runner: AgentRunner,
    tracer_client: PRISMTracer,
) -> Dict[str, Any]:
    session_id = f"cg-{version}-{scenario['id']}"
    category = scenario["category"]
    split = scenario.get("split", "dev")
    turns = scenario["turns"]

    results = []
    for turn_idx, raw_utterance in enumerate(turns, start=1):
        shield_res = redact_pii(raw_utterance)
        masked_text = shield_res.masked_transcript
        redacted_items = [p.to_dict() for p in shield_res.redacted_pii]

        # v0/v1 simulate unshielded client to evaluate baseline
        if version in ("v0", "v1"):
            call_masked = raw_utterance
            call_pii = []
        else:
            call_masked = masked_text
            call_pii = redacted_items

        turn_tracer = TurnTracer(
            session_id=session_id,
            user_utterance=masked_text,
            agent_version=version,
            category=category,
            eval_set=split,
            tracer=tracer_client,
            is_mock=runner.use_mock,
        )

        turn_res = await runner.process_turn(
            session_id=session_id,
            turn_id=turn_idx,
            caller_id=f"caller_{scenario['id']}",
            raw_transcript=raw_utterance,
            masked_transcript=call_masked,
            redacted_pii=call_pii,
            agent_version=version,
        )

        for tr in turn_res.get("state_machine", {}).get("transitions", []):
            turn_tracer.record_enforcement_transition(
                action_id=tr["action_id"],
                action_type=tr["action_type"],
                from_state=tr["from_state"],
                to_state=tr["to_state"],
                reason=tr.get("reason", "commit_window_event"),
            )

        turn_tracer.finish(agent_reply=turn_res["agent_response"])
        results.append(turn_res)

    return {"session_id": session_id, "turns_count": len(results)}


async def run_smoke_test(tracer_client: PRISMTracer) -> None:
    """Run exactly 3 representative calls (Cat A, Cat B, Cat E) to test credit burn."""
    logger.info("=================================================================")
    logger.info(" Executing PRISM 3-Call Smoke Test (Mandatory Credit Discipline)")
    logger.info("=================================================================")
    replay_data = load_replay_set()
    scenarios = replay_data["scenarios"]

    # Pick 1 from Cat A, 1 from Cat B, 1 from Cat E
    smoke_ids = ["A_dev_01", "B_dev_01", "E_dev_01"]
    smoke_scenarios = [s for s in scenarios if s["id"] in smoke_ids]

    runner = AgentRunner(use_mock=True)
    for s in smoke_scenarios:
        logger.info(f"Running smoke scenario {s['id']} ({s['category']}) with v2 ClaimGuard...")
        res = await run_scenario(s, version="v2", runner=runner, tracer_client=tracer_client)
        logger.info(f" -> Completed {res['session_id']} ({res['turns_count']} turns traced)")

    logger.info("3-call smoke test finished! Check PRISM dashboard for credit delta.")


async def run_heldout_suite(tracer_client: PRISMTracer) -> None:
    """Run all 20 held-out calls for v0, v1, and v2."""
    logger.info("=================================================================")
    logger.info(" Ingesting 20 Held-Out Benchmark Calls across v0, v1, and v2")
    logger.info("=================================================================")
    replay_data = load_replay_set()
    heldout = [s for s in replay_data["scenarios"] if s.get("split") == "heldout"]

    logger.info(f"Found {len(heldout)} held-out scenarios.")
    runner = AgentRunner(use_mock=True)

    for version in ["v0", "v1", "v2"]:
        logger.info(f"\n--- Ingesting Version: {version} ---")
        for s in heldout:
            logger.info(f" Tracing {s['id']} ({s['category']}) for {version}...")
            await run_scenario(s, version=version, runner=runner, tracer_client=tracer_client)

    logger.info("\nAll held-out runs completed and dispatched to PRISM.")


def export_traces_to_json() -> int:
    """Export local JSONL buffer to clean PRISM Import History JSON array."""
    if not TRACES_FILE.exists():
        logger.warning(f"No traces file found at {TRACES_FILE}")
        return 0

    records = []
    with open(TRACES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except Exception:
                    pass

    with open(EXPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    logger.info(f"Exported {len(records)} trace sessions to {EXPORT_FILE}")
    return len(records)


def main():
    parser = argparse.ArgumentParser(description="PRISM Telemetry & Benchmark Ingestion")
    parser.add_argument("--smoke", action="store_true", help="Run 3-call smoke test")
    parser.add_argument("--heldout", action="store_true", help="Run 20 held-out calls for v0/v1/v2")
    parser.add_argument("--export", action="store_true", help="Export local traces to JSON")
    parser.add_argument("--status", action="store_true", help="Check PRISM endpoint connectivity")
    parser.add_argument("--api-key", default=PRISMTRACE_API_KEY, help="PRISM API Key")
    parser.add_argument("--host", default=PRISMTRACE_HOST, help="PRISM Host URL")
    parser.add_argument("--project-id", default=PRISMTRACE_PROJECT_ID, help="PRISM Project UUID")

    args = parser.parse_args()

    tracer_client = PRISMTracer(host=args.host, project_id=args.project_id, api_key=args.api_key)

    if args.status:
        check_prism_connection(args.host, args.project_id, args.api_key)
    elif args.smoke:
        asyncio.run(run_smoke_test(tracer_client))
    elif args.heldout:
        asyncio.run(run_heldout_suite(tracer_client))
    elif args.export:
        export_traces_to_json()
    else:
        parser.print_help()

    tracer_client.flush()


if __name__ == "__main__":
    main()
