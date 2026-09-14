"""Unit tests for SQLite Policy Latch triggers."""

import sqlite3
import pytest
from app.db.database import (
    get_connection,
    init_db,
    lookup_policy_db,
    create_claim_db,
    get_claim_db,
    update_claim_notes_db,
)


@pytest.fixture
def memory_db():
    """Create a fresh in-memory SQLite database with schema and triggers."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    with open("app/db/schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    return conn


def test_seed_policies_exist(memory_db):
    """Verify seed policies are populated."""
    policy = lookup_policy_db(policy_number="NH-8821", conn=memory_db)
    assert policy is not None
    assert policy["holder_name"] == "Rajesh Sharma"
    assert policy["deductible_inr"] == 1500
    assert policy["liability_ratio"] == 1.0


def test_create_claim_latched_from_policy(memory_db):
    """Verify that claim creation properly inherits locked deductible and liability."""
    claim = create_claim_db(
        policy_number="NH-8821",
        incident_location="NH48 Km 62 near Manesar",
        incident_description="Engine breakdown, vehicle smoking",
        claim_id="CLM-TEST01",
        conn=memory_db,
    )
    assert claim["claim_id"] == "CLM-TEST01"
    assert claim["deductible_inr"] == 1500
    assert claim["liability_ratio"] == 1.0
    assert "deductible_inr" in claim["locked_fields"]


def test_policy_latch_prevents_deductible_update(memory_db):
    """Verify SQL trigger blocks any UPDATE to deductible_inr (e.g. LLM waiver attempt)."""
    create_claim_db(
        policy_number="NH-8821",
        incident_location="NH48 Km 45",
        incident_description="Tire burst",
        claim_id="CLM-WAIVER-ATTEMPT",
        conn=memory_db,
    )

    with pytest.raises(sqlite3.DatabaseError) as exc_info:
        memory_db.execute(
            "UPDATE claims SET deductible_inr = 0 WHERE claim_id = 'CLM-WAIVER-ATTEMPT'"
        )
    assert "POLICY_LATCH_BREACH" in str(exc_info.value)
    assert "latched and immutable" in str(exc_info.value)

    # Verify claim in DB remains unchanged
    c = get_claim_db("CLM-WAIVER-ATTEMPT", conn=memory_db)
    assert c["deductible_inr"] == 1500


def test_policy_latch_prevents_liability_ratio_update(memory_db):
    """Verify SQL trigger blocks any UPDATE to liability_ratio."""
    create_claim_db(
        policy_number="NH-8821",
        incident_location="NH48 Km 50",
        incident_description="Fender bender",
        claim_id="CLM-LIABILITY-ATTEMPT",
        conn=memory_db,
    )

    with pytest.raises(sqlite3.DatabaseError) as exc_info:
        memory_db.execute(
            "UPDATE claims SET liability_ratio = 0.5 WHERE claim_id = 'CLM-LIABILITY-ATTEMPT'"
        )
    assert "POLICY_LATCH_BREACH" in str(exc_info.value)


def test_policy_latch_prevents_tampered_claim_insert(memory_db):
    """Verify SQL trigger blocks inserting a claim with manipulated deductible."""
    with pytest.raises(sqlite3.DatabaseError) as exc_info:
        memory_db.execute(
            """
            INSERT INTO claims (claim_id, policy_number, incident_location, incident_description, deductible_inr, liability_ratio, status)
            VALUES ('CLM-TAMPERED', 'NH-8821', 'NH48 Km 10', 'Scratch', 0, 1.0, 'OPEN_UNASSIGNED')
            """
        )
    assert "POLICY_LATCH_BREACH" in str(exc_info.value)


def test_allowed_updates_succeed(memory_db):
    """Verify non-financial fields (notes, status) can be updated normally."""
    create_claim_db(
        policy_number="NH-8821",
        incident_location="NH48 Km 75",
        incident_description="Overheated engine",
        claim_id="CLM-SAFE-UPDATE",
        conn=memory_db,
    )

    success = update_claim_notes_db("CLM-SAFE-UPDATE", "Tow dispatched to Neemrana", conn=memory_db)
    assert success is True

    c = get_claim_db("CLM-SAFE-UPDATE", conn=memory_db)
    assert c["notes"] == "Tow dispatched to Neemrana"
    assert c["deductible_inr"] == 1500
