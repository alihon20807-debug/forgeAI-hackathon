"""SQLite Database Manager for ClaimGuard."""

import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.config import DB_PATH

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    path = db_path or DB_PATH
    if path != Path(":memory:"):
        path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


get_db = get_connection


def init_db(db_path: Optional[Path] = None) -> None:
    """Bootstrap schema, tables, triggers, and seed policies."""
    conn = get_connection(db_path)
    with conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
    conn.close()


def lookup_policy_db(
    policy_number: Optional[str] = None,
    vehicle_number: Optional[str] = None,
    conn: Optional[sqlite3.Connection] = None,
) -> Optional[Dict[str, Any]]:
    """Lookup policy details by policy number or vehicle number."""
    close_after = False
    if conn is None:
        conn = get_connection()
        close_after = True

    try:
        cursor = conn.cursor()
        if policy_number and vehicle_number:
            cursor.execute(
                "SELECT * FROM policies WHERE policy_number = ? OR vehicle_number = ?",
                (policy_number.strip().upper(), vehicle_number.strip().upper()),
            )
        elif policy_number:
            cursor.execute(
                "SELECT * FROM policies WHERE policy_number = ?",
                (policy_number.strip().upper(),),
            )
        elif vehicle_number:
            cursor.execute(
                "SELECT * FROM policies WHERE vehicle_number = ?",
                (vehicle_number.strip().upper(),),
            )
        else:
            return None

        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        if close_after:
            conn.close()


def create_claim_db(
    policy_number: str,
    incident_location: str,
    incident_description: str,
    claim_id: Optional[str] = None,
    conn: Optional[sqlite3.Connection] = None,
) -> Dict[str, Any]:
    """Create a new claim record with policy financial latching.
    
    Deductible and liability ratio are fetched directly from the authoritative
    policy record to satisfy the database latch trigger.
    """
    close_after = False
    if conn is None:
        conn = get_connection()
        close_after = True

    try:
        cursor = conn.cursor()
        norm_policy = policy_number.strip().upper()
        cursor.execute("SELECT deductible_inr, liability_ratio FROM policies WHERE policy_number = ?", (norm_policy,))
        policy_row = cursor.fetchone()
        if not policy_row:
            raise ValueError(f"Cannot create claim: Policy {policy_number} not found in System of Record.")

        deductible = policy_row["deductible_inr"]
        liability = policy_row["liability_ratio"]
        cid = claim_id or f"CLM-{uuid.uuid4().hex[:6].upper()}"
        now = datetime.now(timezone.utc).isoformat()

        cursor.execute(
            """
            INSERT INTO claims (claim_id, policy_number, incident_location, incident_description, deductible_inr, liability_ratio, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, 'OPEN_UNASSIGNED', ?, ?)
            """,
            (cid, norm_policy, incident_location, incident_description, deductible, liability, now, now),
        )
        conn.commit()

        return {
            "claim_id": cid,
            "policy_number": norm_policy,
            "incident_location": incident_location,
            "incident_description": incident_description,
            "deductible_inr": deductible,
            "liability_ratio": liability,
            "status": "OPEN_UNASSIGNED",
            "locked_fields": ["deductible_inr", "liability_ratio"],
            "created_at": now,
        }
    finally:
        if close_after:
            conn.close()


def get_claim_db(claim_id: str, conn: Optional[sqlite3.Connection] = None) -> Optional[Dict[str, Any]]:
    close_after = False
    if conn is None:
        conn = get_connection()
        close_after = True

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM claims WHERE claim_id = ?", (claim_id.strip().upper(),))
        row = cursor.fetchone()
        if not row:
            return None
        res = dict(row)
        res["locked_fields"] = ["deductible_inr", "liability_ratio"]
        return res
    finally:
        if close_after:
            conn.close()


def update_claim_notes_db(claim_id: str, notes: str, conn: Optional[sqlite3.Connection] = None) -> bool:
    close_after = False
    if conn is None:
        conn = get_connection()
        close_after = True

    try:
        now = datetime.now(timezone.utc).isoformat()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE claims SET notes = ?, updated_at = ? WHERE claim_id = ?",
            (notes, now, claim_id.strip().upper()),
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        if close_after:
            conn.close()


def stage_dispatch_db(
    claim_id: str,
    service_type: str,
    pickup_location: str,
    vendor_name: Optional[str] = None,
    eta_minutes: Optional[int] = None,
    cost_inr: int = 0,
    dispatch_id: Optional[str] = None,
    status: str = "HELD",
    conn: Optional[sqlite3.Connection] = None,
) -> Dict[str, Any]:
    close_after = False
    if conn is None:
        conn = get_connection()
        close_after = True

    try:
        did = dispatch_id or f"DISP-{uuid.uuid4().hex[:6].upper()}"
        now = datetime.now(timezone.utc).isoformat()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO dispatches (dispatch_id, claim_id, service_type, pickup_location, vendor_name, eta_minutes, cost_inr, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (did, claim_id.strip().upper(), service_type, pickup_location, vendor_name, eta_minutes, cost_inr, status, now, now),
        )
        conn.commit()
        return {
            "dispatch_id": did,
            "claim_id": claim_id,
            "service_type": service_type,
            "pickup_location": pickup_location,
            "vendor_name": vendor_name,
            "eta_minutes": eta_minutes,
            "cost_inr": cost_inr,
            "status": status,
        }
    finally:
        if close_after:
            conn.close()


def update_dispatch_status_db(
    dispatch_id: str,
    status: str,
    conn: Optional[sqlite3.Connection] = None,
) -> bool:
    close_after = False
    if conn is None:
        conn = get_connection()
        close_after = True

    try:
        now = datetime.now(timezone.utc).isoformat()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE dispatches SET status = ?, updated_at = ? WHERE dispatch_id = ?",
            (status.upper(), now, dispatch_id),
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        if close_after:
            conn.close()


def get_dispatches_by_claim_db(claim_id: str, conn: Optional[sqlite3.Connection] = None) -> List[Dict[str, Any]]:
    close_after = False
    if conn is None:
        conn = get_connection()
        close_after = True

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dispatches WHERE claim_id = ?", (claim_id.strip().upper(),))
        return [dict(r) for r in cursor.fetchall()]
    finally:
        if close_after:
            conn.close()
