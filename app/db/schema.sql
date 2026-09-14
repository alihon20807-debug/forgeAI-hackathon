-- ClaimGuard System of Record & Policy Latch Schema
-- Invariant: Financial terms (deductibles, policy limits, liability) are latched
-- at the database level with SQL triggers. LLM tools cannot alter them.

PRAGMA foreign_keys = ON;

-- 1. Policies Table (Authoritative System of Record)
CREATE TABLE IF NOT EXISTS policies (
    policy_number TEXT PRIMARY KEY,
    holder_name TEXT NOT NULL,
    vehicle_number TEXT NOT NULL,
    deductible_inr INTEGER NOT NULL,
    roadside_limit_inr INTEGER NOT NULL,
    liability_ratio REAL NOT NULL DEFAULT 1.0,
    coverage_type TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 2. Claims Table
CREATE TABLE IF NOT EXISTS claims (
    claim_id TEXT PRIMARY KEY,
    policy_number TEXT NOT NULL REFERENCES policies(policy_number),
    incident_location TEXT,
    incident_description TEXT,
    deductible_inr INTEGER NOT NULL,
    liability_ratio REAL NOT NULL DEFAULT 1.0,
    status TEXT NOT NULL DEFAULT 'OPEN_UNASSIGNED', -- DRAFT, OPEN_UNASSIGNED, DISPATCHED, RESOLVED, CLOSED
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 3. Dispatches Table (Roadside Assistance, Towing, Ambulance)
CREATE TABLE IF NOT EXISTS dispatches (
    dispatch_id TEXT PRIMARY KEY,
    claim_id TEXT NOT NULL REFERENCES claims(claim_id),
    service_type TEXT NOT NULL, -- towing, ambulance, mechanic
    pickup_location TEXT NOT NULL,
    vendor_name TEXT,
    eta_minutes INTEGER,
    cost_inr INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'HELD', -- HELD, FROZEN, COMMITTED, ABORTED
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ----------------------------------------------------------------------------
-- POLICY LATCH TRIGGERS: Structural Immutability of Financial Terms
-- ----------------------------------------------------------------------------

-- Trigger 1: Prohibit any update to deductible_inr or liability_ratio on claims
CREATE TRIGGER IF NOT EXISTS trg_claims_lock_financials_update
BEFORE UPDATE OF deductible_inr, liability_ratio ON claims
BEGIN
    SELECT RAISE(ABORT, 'POLICY_LATCH_BREACH: Financial terms (deductible_inr, liability_ratio) are latched and immutable.');
END;

-- Trigger 2: Prohibit inserting a claim with manipulated deductible or liability ratio
-- Values MUST match the authoritative policies table.
CREATE TRIGGER IF NOT EXISTS trg_claims_lock_financials_insert
BEFORE INSERT ON claims
FOR EACH ROW
WHEN NEW.deductible_inr != (SELECT deductible_inr FROM policies WHERE policy_number = NEW.policy_number)
   OR NEW.liability_ratio != (SELECT liability_ratio FROM policies WHERE policy_number = NEW.policy_number)
BEGIN
    SELECT RAISE(ABORT, 'POLICY_LATCH_BREACH: Claim financial parameters (deductible_inr, liability_ratio) must match immutable policy record.');
END;

-- ----------------------------------------------------------------------------
-- SEED POLICIES FOR REPLAY & DEMONSTRATION
-- ----------------------------------------------------------------------------
INSERT OR IGNORE INTO policies (policy_number, holder_name, vehicle_number, deductible_inr, roadside_limit_inr, liability_ratio, coverage_type)
VALUES
    ('NH-8821', 'Rajesh Sharma', 'DL-01-AB-1234', 1500, 5000, 1.0, 'NH48 Commercial Roadside Comprehensive'),
    ('NH-4019', 'Priya Patel', 'MH-02-XY-9876', 2500, 10000, 1.0, 'Expressway Fleet Priority'),
    ('NH-5502', 'Amit Verma', 'HR-26-DK-5541', 1500, 5000, 1.0, 'Standard Passenger Corridor Cover'),
    ('NH-9921', 'Sunil Rao', 'KA-03-MG-4412', 1500, 7500, 1.0, 'Interstate Long-Haul Platinum');
