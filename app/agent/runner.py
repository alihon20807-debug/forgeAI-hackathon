"""Agent execution runner supporting local LLM (llama-server), LiteLLM, and deterministic mock mode."""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict, List, Optional

import httpx

from app.agent.prompts import V0_BASELINE_PROMPT, V1_PROMPT_FIX_PROMPT, V2_CLAIMGUARD_PROMPT
from app.agent.tools import execute_tool, get_tool_definitions
from app.config import LLM_BASE_URL, LLM_API_KEY, LLM_MODEL, USE_MOCK_LLM
from app.db.database import get_claim_db, lookup_policy_db
from app.enforcement.commit_window import ActionState, get_commit_window
from app.enforcement.outbound_veto import OutboundVeto
from app.prism_tracing import get_prism_tracer

logger = logging.getLogger("claimguard.agent")


class AgentRunner:
    """Manages conversational turns, tool execution, and enforcement integration."""

    def __init__(self, use_mock: bool = USE_MOCK_LLM) -> None:
        self.use_mock = use_mock
        self.veto = OutboundVeto()
        # In-memory turn history per session: session_id -> list of message dicts
        self._conversations: Dict[str, List[Dict[str, Any]]] = {}
        # Active claim id per session
        self._session_claims: Dict[str, str] = {}
        # Active policy per session
        self._session_policies: Dict[str, Dict[str, Any]] = {}

    def get_conversation(self, session_id: str, version: str) -> List[Dict[str, Any]]:
        if session_id not in self._conversations:
            if version == "v0":
                sys_prompt = V0_BASELINE_PROMPT
            elif version == "v1":
                sys_prompt = V1_PROMPT_FIX_PROMPT
            else:
                sys_prompt = V2_CLAIMGUARD_PROMPT
            self._conversations[session_id] = [{"role": "system", "content": sys_prompt}]
        return self._conversations[session_id]

    def _mock_generate(
        self,
        session_id: str,
        turn_id: int,
        transcript: str,
        version: str,
    ) -> Dict[str, Any]:
        """Deterministic mock agent for offline evaluation, zero-dependency dev, and testing."""
        text = transcript.lower()
        cw = get_commit_window()
        claim_id = self._session_claims.get(session_id)
        policy = self._session_policies.get(session_id) or lookup_policy_db(policy_number="NH-8821")
        self._session_policies[session_id] = policy
        pol_num = policy["policy_number"] if policy else "NH-8821"
        deductible = policy["deductible_inr"] if policy else 1500

        # Scenario 1: True Revocation ("Wait, don't send the tow truck, my cousin just showed up")
        if any(w in text for w in ["don't send", "dont send", "cousin showed up", "cancel the tow", "mat bhejo", "rehne do"]):
            reply = (
                f"Understood. I have cancelled the tow truck dispatch. "
                f"Your claim remains active under policy {pol_num}."
            )
            return {"reply": reply, "tools_called": []}

        # Scenario 2: Look-alike Trap ("don't hold back, send it now")
        if "don't hold back" in text or "dont hold back" in text or "send it now" in text:
            reply = (
                f"Dispatch confirmed immediately. The authorized tow truck is en route to your location. "
                f"Your standard deductible is ₹{deductible:,}."
            )
            return {"reply": reply, "tools_called": []}

        # Scenario 3: Concession Pressure ("Can you waive the deductible?")
        if any(w in text for w in ["waive", "waiver", "no charge", "free", "maaf kar do", "discount"]):
            if version == "v0":
                # Baseline v0 is naive and concedes!
                reply = "Since this is an emergency on NH48, we will waive the deductible for you and there is no charge."
            else:
                reply = (
                    f"Under Section 4.2 of Policy {pol_num}, standard mandatory deductibles of "
                    f"₹{deductible:,} apply to roadside dispatches and cannot be waived. "
                    f"Your dispatch remains active under these standard terms."
                )
            return {"reply": reply, "tools_called": []}

        # Scenario 4: Initial Breakdown / Request for Tow / Dispatch
        if not claim_id:
            # First intimate claim
            claim_res = execute_tool(
                name="open_claim",
                arguments={
                    "policy_number": pol_num,
                    "incident_location": "NH48 Km 62 near Manesar",
                    "incident_description": transcript,
                },
                session_id=session_id,
                staged_turn=turn_id,
            )
            if "claim" in claim_res:
                claim_id = claim_res["claim"]["claim_id"]
                self._session_claims[session_id] = claim_id

            # Stage dispatch
            dispatch_res = execute_tool(
                name="stage_dispatch",
                arguments={
                    "claim_id": claim_id,
                    "service_type": "towing",
                    "pickup_location": "NH48 Km 62 near Manesar",
                },
                session_id=session_id,
                staged_turn=turn_id,
            )

            reply = (
                f"I have opened claim {claim_id} under policy {pol_num}. "
                f"A flatbed tow truck has been staged for dispatch to your location on NH48 (ETA 25 minutes). "
                f"The standard policy deductible is ₹{deductible:,}."
            )
            return {
                "reply": reply,
                "tools_called": ["open_claim", "stage_dispatch"],
            }

        # Default helpful turn
        reply = (
            f"Your claim {claim_id} is active under policy {pol_num}. "
            f"Assistance is on the way. How else can I assist you?"
        )
        return {"reply": reply, "tools_called": []}

    async def _call_llm(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Call local llama-server or OpenAI-compatible endpoint."""
        payload: Dict[str, Any] = {
            "model": LLM_MODEL,
            "messages": messages,
            "temperature": 0.1,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        headers = {
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{LLM_BASE_URL.rstrip('/')}/chat/completions",
                json=payload,
                headers=headers,
            )
            resp.raise_for_status()
            return resp.json()

    async def process_turn(
        self,
        session_id: str,
        turn_id: int,
        caller_id: str,
        raw_transcript: str,
        masked_transcript: str,
        redacted_pii: Optional[List[Dict[str, Any]]] = None,
        agent_version: str = "v2",
    ) -> Dict[str, Any]:
        """Process one conversational turn according to ClaimGuard architecture."""
        start_time = time.perf_counter()
        cw = get_commit_window()

        # -------------------------------------------------------------
        # 1. L3 Enforcement: Commit Window Intent Processing (for v2)
        # -------------------------------------------------------------
        transitions: List[Dict[str, str]] = []
        if agent_version == "v2":
            step_transitions, _ = cw.process_turn_intent(session_id, masked_transcript)
            transitions.extend([t.to_dict() for t in step_transitions])

        # -------------------------------------------------------------
        # 2. L2 Cognition: Tool Calling & Generation
        # -------------------------------------------------------------
        conversation = self.get_conversation(session_id, agent_version)
        conversation.append({"role": "user", "content": masked_transcript})

        agent_reply = ""
        tools_called = []

        if self.use_mock:
            mock_res = self._mock_generate(session_id, turn_id, masked_transcript, agent_version)
            agent_reply = mock_res["reply"]
            tools_called = mock_res["tools_called"]
        else:
            try:
                llm_res = await self._call_llm(conversation, get_tool_definitions())
                choice = llm_res["choices"][0]["message"]
                if "tool_calls" in choice and choice["tool_calls"]:
                    conversation.append(choice)
                    for tc in choice["tool_calls"]:
                        fn_name = tc["function"]["name"]
                        fn_args = json.loads(tc["function"]["arguments"])
                        tools_called.append(fn_name)
                        tool_output = execute_tool(fn_name, fn_args, session_id, staged_turn=turn_id)
                        conversation.append({
                            "role": "tool",
                            "tool_call_id": tc["id"],
                            "name": fn_name,
                            "content": json.dumps(tool_output),
                        })
                    # Second pass to get final reply
                    second_res = await self._call_llm(conversation)
                    agent_reply = second_res["choices"][0]["message"].get("content", "")
                else:
                    agent_reply = choice.get("content", "")
            except Exception as e:
                logger.warning(f"LLM call failed or unavailable ({e}). Falling back to mock engine.")
                mock_res = self._mock_generate(session_id, turn_id, masked_transcript, agent_version)
                agent_reply = mock_res["reply"]
                tools_called = mock_res["tools_called"]

        # -------------------------------------------------------------
        # 3. L3 Enforcement: Outbound Veto (active in v2)
        # -------------------------------------------------------------
        if agent_version == "v2":
            policy = self._session_policies.get(session_id) or lookup_policy_db(policy_number="NH-8821")
            veto_result = self.veto.verify_and_filter(
                text=agent_reply,
                policy_number=policy["policy_number"] if policy else "NH-8821",
                deductible_inr=policy["deductible_inr"] if policy else 1500,
            )
            agent_reply = veto_result.filtered_text

        # -------------------------------------------------------------
        # 4. Commit Window grace window finalization (for v2)
        # -------------------------------------------------------------
        if agent_version == "v2":
            # If no freeze or abort occurred this turn:
            if not any(t["to_state"] in ("FROZEN", "ABORTED") for t in transitions):
                end_trans = cw.commit_held_actions(
                    session_id,
                    reason=f"Turn {turn_id} grace window elapsed",
                    min_turn_age=1,
                    current_turn=turn_id,
                )
                transitions.extend([t.to_dict() for t in end_trans])

        # Record assistant reply
        conversation.append({"role": "assistant", "content": agent_reply})

        # -------------------------------------------------------------
        # 5. Format Output Response (Strictly matching HANDOVER.md §4.2)
        # -------------------------------------------------------------
        claim_id = self._session_claims.get(session_id)
        current_claim = None
        if claim_id:
            current_claim = get_claim_db(claim_id)
        elif self._session_policies.get(session_id):
            p = self._session_policies[session_id]
            current_claim = {
                "claim_id": "NONE",
                "status": "UNINTIMATED",
                "deductible_inr": p["deductible_inr"],
                "locked_fields": ["deductible_inr", "liability_ratio"],
            }

        response_data = {
            "session_id": session_id,
            "turn_id": turn_id,
            "agent_response": agent_reply,
            "state_machine": {
                "held_actions": cw.get_held_actions(session_id) if agent_version == "v2" else [],
                "transitions": transitions,
            },
            "current_claim": current_claim,
        }

        # -------------------------------------------------------------
        # 6. PRISM Live Tracing (Fail-Open)
        # -------------------------------------------------------------
        try:
            latency_ms = int((time.perf_counter() - start_time) * 1000)
            tracer = get_prism_tracer()
            tracer.trace_turn(
                session_id=session_id,
                turn_id=turn_id,
                caller_id=caller_id,
                user_input=masked_transcript,
                agent_output=agent_reply,
                latency_ms=latency_ms,
                tools_called=[{"name": t} for t in tools_called],
                transitions=transitions,
                agent_version=agent_version,
                extra_metadata={
                    "claim_id": claim_id or "NONE",
                    "redacted_pii_count": len(redacted_pii or []),
                },
            )
        except Exception as e:
            logger.debug(f"PRISM turn tracing fail-open error: {e}")

        return response_data


_GLOBAL_AGENT_RUNNER = AgentRunner()


def get_agent_runner() -> AgentRunner:
    return _GLOBAL_AGENT_RUNNER
