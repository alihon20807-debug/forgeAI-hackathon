"""Tool implementations and OpenAPI schemas for the ClaimGuard agent."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from app.db.database import (
    lookup_policy_db,
    create_claim_db,
    get_claim_db,
    update_claim_notes_db,
    stage_dispatch_db,
)
from app.enforcement.commit_window import get_commit_window
from app.rag.retriever import get_retriever


def tool_lookup_policy(policy_number: Optional[str] = None, vehicle_number: Optional[str] = None) -> Dict[str, Any]:
    """Look up policy terms, deductible, and coverage limits."""
    policy = lookup_policy_db(policy_number=policy_number, vehicle_number=vehicle_number)
    if not policy:
        return {"error": f"Policy not found for policy={policy_number}, vehicle={vehicle_number}"}
    return {"status": "success", "policy": policy}


def tool_search_policy_docs(query: str) -> Dict[str, Any]:
    """Retrieve official NH48 insurance clauses, SOPs, and rate card data."""
    retriever = get_retriever()
    results = retriever.search(query=query, top_k=3)
    return {"status": "success", "query": query, "chunks": results}


def tool_open_claim(
    policy_number: str,
    incident_location: str,
    incident_description: str,
    session_id: str,
    staged_turn: int = 1,
) -> Dict[str, Any]:
    """Intimate a new FNOL claim. Deductibles and liability are locked at DB level."""
    cw = get_commit_window()
    try:
        claim = create_claim_db(
            policy_number=policy_number,
            incident_location=incident_location,
            incident_description=incident_description,
        )
        # Stage open_claim in Commit Window
        cw.stage_action(
            session_id=session_id,
            action_type="open_claim",
            payload={"claim_id": claim["claim_id"], "policy_number": policy_number},
            staged_turn=staged_turn,
        )
        return {"status": "success", "claim": claim}
    except Exception as e:
        return {"error": str(e)}


def tool_stage_dispatch(
    claim_id: str,
    service_type: str,
    pickup_location: str,
    session_id: str,
    vendor_name: Optional[str] = "NH48 Highway Patrol Assistance",
    eta_minutes: int = 20,
    staged_turn: int = 1,
) -> Dict[str, Any]:
    """Stage a roadside recovery, towing, or ambulance dispatch into HELD state."""
    cw = get_commit_window()
    try:
        # 1. Record in DB as HELD
        dispatch = stage_dispatch_db(
            claim_id=claim_id,
            service_type=service_type,
            pickup_location=pickup_location,
            vendor_name=vendor_name,
            eta_minutes=eta_minutes,
            status="HELD",
        )
        # 2. Stage in Commit Window
        action = cw.stage_action(
            session_id=session_id,
            action_type="stage_dispatch",
            payload=dispatch,
            action_id=dispatch["dispatch_id"],
            staged_turn=staged_turn,
        )
        return {
            "status": "staged_held",
            "action_id": action.action_id,
            "dispatch": dispatch,
            "message": f"Dispatch staged in HELD state. ETA {eta_minutes} mins.",
        }
    except Exception as e:
        return {"error": str(e)}


def tool_update_claim(claim_id: str, notes: str) -> Dict[str, Any]:
    """Update claim notes or general non-financial details."""
    success = update_claim_notes_db(claim_id=claim_id, notes=notes)
    if not success:
        return {"error": f"Failed to update claim {claim_id}"}
    return {"status": "success", "claim_id": claim_id, "notes": notes}


def tool_escalate_to_human(reason: str) -> Dict[str, Any]:
    """Escalate complex, disputed, or high-severity situations to human supervisor."""
    return {
        "status": "escalated",
        "reason": reason,
        "message": "Call flagged for immediate human supervisor intervention.",
    }


# Tool Dispatcher
def execute_tool(
    name: str,
    arguments: Dict[str, Any],
    session_id: str,
    staged_turn: int = 1,
) -> Dict[str, Any]:
    if name == "lookup_policy":
        return tool_lookup_policy(
            policy_number=arguments.get("policy_number"),
            vehicle_number=arguments.get("vehicle_number"),
        )
    elif name == "search_policy_docs":
        return tool_search_policy_docs(query=arguments.get("query", ""))
    elif name == "open_claim":
        return tool_open_claim(
            policy_number=arguments.get("policy_number", "NH-8821"),
            incident_location=arguments.get("incident_location", "NH48 corridor"),
            incident_description=arguments.get("incident_description", "Roadside breakdown"),
            session_id=session_id,
            staged_turn=staged_turn,
        )
    elif name == "stage_dispatch":
        return tool_stage_dispatch(
            claim_id=arguments.get("claim_id", ""),
            service_type=arguments.get("service_type", "towing"),
            pickup_location=arguments.get("pickup_location", "NH48"),
            session_id=session_id,
            vendor_name=arguments.get("vendor_name", "NH48 Rapid Towing"),
            eta_minutes=arguments.get("eta_minutes", 25),
            staged_turn=staged_turn,
        )
    elif name == "update_claim":
        return tool_update_claim(
            claim_id=arguments.get("claim_id", ""),
            notes=arguments.get("notes", ""),
        )
    elif name == "escalate_to_human":
        return tool_escalate_to_human(reason=arguments.get("reason", "Caller request"))
    else:
        return {"error": f"Unknown tool '{name}'"}


# OpenAPI-compatible schemas for small-model function calling
def get_tool_definitions() -> List[Dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "lookup_policy",
                "description": "Lookup insurance policy details, coverage limits, and deductible by policy number or vehicle number.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "policy_number": {"type": "string", "description": "e.g. NH-8821"},
                        "vehicle_number": {"type": "string", "description": "e.g. DL-01-AB-1234"},
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_policy_docs",
                "description": "RAG search across official NH48 insurance policy terms, SOPs, towing rates, and exclusions.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query keywords, e.g. 'deductible rules' or 'towing rate'"},
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "open_claim",
                "description": "Open a new First Notice of Loss (FNOL) claim under a verified policy.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "policy_number": {"type": "string", "description": "Verified policy number"},
                        "incident_location": {"type": "string", "description": "Location of the incident, e.g. 'NH48 Km 62 near Manesar'"},
                        "incident_description": {"type": "string", "description": "Summary of accident or breakdown"},
                    },
                    "required": ["policy_number", "incident_location", "incident_description"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "stage_dispatch",
                "description": "Stage a roadside assistance, towing, or ambulance dispatch. Starts in HELD state.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "claim_id": {"type": "string", "description": "Active claim ID"},
                        "service_type": {"type": "string", "enum": ["towing", "ambulance", "mechanic"]},
                        "pickup_location": {"type": "string", "description": "Vehicle pickup location"},
                    },
                    "required": ["claim_id", "service_type", "pickup_location"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "update_claim",
                "description": "Update notes or metadata on an existing claim.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "claim_id": {"type": "string", "description": "Active claim ID"},
                        "notes": {"type": "string", "description": "Updated notes"},
                    },
                    "required": ["claim_id", "notes"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "escalate_to_human",
                "description": "Escalate call to human supervisor for disputes or edge cases.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reason": {"type": "string", "description": "Reason for escalation"},
                    },
                    "required": ["reason"],
                },
            },
        },
    ]
