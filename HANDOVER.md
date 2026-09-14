# ClaimGuard × PRISM — Team Handover & Work Allocation Brief
**Event:** ForgeAI Hackathon · graVITas'26 · VIT Vellore  
**Core Thesis:** *PRISM is the hero, ClaimGuard is the vehicle. The LLM proposes; deterministic code disposes.*  
**Canonical Plan:** Refer to `Overall-plan.md` (authoritative document). Do not deviate from design invariants.

---

## 1. Executive Context & Invariants

ClaimGuard is an insurance First-Notice-of-Loss (FNOL) voice agent running on a deliberately small, cheap local model (the kind deployed in high-volume production call centers). PRISM is used as the end-to-end diagnostic and evaluation instrument that reveals where cheap models fail, guides prompt fixes (v1), and proves the architectural safety layer (v2 ClaimGuard) on a locked 60-call held-out benchmark.

### Non-Negotiable Invariants
1. **Model Consistency:** Same small model and same generation parameters across all runs (v0 Baseline, v1 Prompt-Fixed, v2 ClaimGuard). The variable under test is the architecture, never model size.
2. **Pre-LLM PII Shielding:** Spoken card numbers (Luhn check), Aadhaar numbers (Verhoeff check), and Indian phone numbers are masked **before** the transcript reaches the LLM and **before** any telemetry is emitted.
3. **Deterministic Enforcement:** Financial terms (deductibles, policy limits, liability) are latched at the database level with SQL triggers. Concession phrases and phantom ₹ amounts are blocked by an Outbound Veto.
4. **Honesty & Metrics:** Never fabricate numbers. PRISM’s "Compliance Score" is explicitly documented as CSAT—call it CSAT or response quality, never compliance. Use PRISM’s verified terminology: Evaluators, Guardrails, Agent Intelligence, AI Remediation, Trajectory Evaluation.
5. **Language Framing:** Pitch and documentation are in **clean English**. Native Indian language (Hindi-first code-mixed) capability is demonstrated live in the voice demo and in one labelled transcript example, not in Hinglish slide copy (see `CLAUDE.md`).

---

## 2. Infrastructure & Server Strategy

> [!IMPORTANT]
> **DEVELOPMENT VS. FINAL DEMO SERVER RULE:**
> - **During Development:** Every teammate runs their **own laptop as their local server**. Work against local mock servers or lightweight stubs. Do NOT create cross-machine network dependencies or wait on Ali's machine during dev.
> - **For Final Demo & Official Benchmark Run:** **Ali’s laptop** has local model execution capacity (GPU, local LLM via llama.cpp/Ollama, local whisper ASR). His machine will act as the unified master server running the full stack for the live evaluation and judge demo.
> - **Safety Fallback:** If local hardware encounters venue or thermal issues, fall back to a hosted model via PRISM’s proxy or LiteLLM.

---

## 3. Team Work Allocation & Deliverables

```
                               ┌─────────────────────────────────────────┐
                               │       PRATHAM: L0, L1 & L6              │
                               │  - Whisper ASR (Hindi-first PTT)        │
                               │  - Pre-LLM PII Shield (Luhn/Verhoeff)   │
                               │  - Live Supervisor Web Console          │
                               │  - Audio clips & fallback video         │
                               └───────────────────┬─────────────────────┘
                                                   │ Clean masked transcript
                               ┌───────────────────▼─────────────────────┐
                               │          ALI: L2, L3 & L4               │
                               │  - Local Model Inference & RAG          │
                               │  - L3 Commit Window State Machine       │
                               │  - L3 Policy Latch & Outbound Veto      │
                               │  - FastAPI Backend & SQLite DB          │
                               │  - *Master Host for Final Demo*         │
                               └───────────────────┬─────────────────────┘
                                                   │ Spans & State Transitions
                               ┌───────────────────▼─────────────────────┐
                               │           OJAS: L5 & EVALS              │
                               │  - PRISM Tracing SDK Integration        │
                               │  - 60-call Replay Set (Pre-registered)  │
                               │  - Automated Local Checker              │
                               │  - PRISM 98-Credit Run Management       │
                               │  - Pitch Deck Measured Data Injection   │
                               └─────────────────────────────────────────┘
```

---

### 👤 Teammate 1: Ali
**Role:** Backend Lead, Intelligence & Enforcement Architect  
**Subsystems:** L2 Cognition, L3 Enforcement ("ClaimGuard"), L4 System of Record, Master Demo Server

#### Primary Responsibilities:
1. **Core Agent & RAG (`app/agent/`, `app/rag/`):**
   - Implement the tool-calling loop for the small model (e.g. Llama-3-8B / Qwen-2.5-7B via llama.cpp or Ollama with LiteLLM proxy fallback).
   - Implemented tools: `lookup_policy`, `search_policy_docs`, `open_claim`, `stage_dispatch`, `update_claim`, `escalate_to_human`.
   - Build in-memory policy retriever over the NH48 corridor insurer documents (deductibles, roadside rules, partner towing rates).
2. **Deterministic Enforcement Engine (`app/enforcement/`):**
   - **Commit Window State Machine:** Consequential tool actions start in state `HELD`. If cancellation keywords occur, state shifts immediately to `FROZEN`. A dedicated resolution step settles whether to `COMMIT` or `ABORT`.
   - **Policy Latch:** SQLite schema in `app/db/` with SQL triggers preventing any tool or LLM write from altering deductibles or liability status.
   - **Outbound Veto:** Intercept model responses before speech/return. Regex check that any ₹ figure exists in retrieved context, and block concession phrases ("we will waive", "no charge for you") with a grounded policy clause citation.
3. **FastAPI Server (`app/server.py`):**
   - REST/WebSocket routes for session start, turn processing, and live state broadcast to Pratham’s console.
   - Provide clean mock endpoints for Pratham and Ojas to test against locally during development.
4. **Final Demo Server Environment:**
   - Maintain the master setup scripts (`scripts/run_local_model.sh`, `scripts/start_server.sh`) ready to run the entire stack on your laptop for the final presentation.

---

### 👤 Teammate 2: Pratham
**Role:** Voice Pipeline, Security & Supervisor Console Lead  
**Subsystems:** L0 Client Edge, L1 Perception, L6 Human Console, Media Assets

#### Primary Responsibilities:
1. **Perception & Speech-to-Text (`app/voice/`):**
   - Local STT using `whisper.cpp` (or Faster-Whisper) with prompt biasing for Indian accents and Hindi code-mixed speech.
   - Implement Push-to-Talk (PTT) as the robust primary capture mode for the noisy auditorium demo, with text fallback.
2. **Client-Side Mathematical PII Shield (`app/security/pii_shield.py`):**
   - Card masking: 13-19 digit detection with **Luhn checksum verification** → replace with `[CARD REDACTED]`.
   - Aadhaar masking: 12-digit Indian national ID with **Verhoeff algorithm verification** → replace with `[AADHAAR REDACTED]`.
   - Phone masking: 10-digit Indian mobile regex (+91 / 6-9 prefix) → replace with `[PHONE REDACTED]`.
   - **Invariant:** Runs BEFORE transcript is sent to Ali’s backend or Ojas’s telemetry!
3. **Live Supervisor Console (`frontend/`):**
   - Premium, clean UI following the project design system (Warm cream `#F8F6F1`, Roasted walnut `#1E1915`, Jade green `#1B5E4B` verification badges, PRISM rainbow accents).
   - Dynamic real-time components:
     - Audio recording / PTT button & audio waveform.
     - Live transcript box showing incoming text and real-time redaction banners.
     - **Commit Window Visualizer:** Animated cards transitioning live between `HELD` (Amber) ➔ `FROZEN` (Purple/Blue) ➔ `COMMITTED` (Jade) / `ABORTED` (Crimson).
     - Live Dispatch & Claim State table.
   - **Dev Mode:** Include a built-in mock toggle in the frontend so you can test all animations and UI states without needing Ali's backend running.
4. **Demo Insurance Fallbacks:**
   - Record 20 real-voice test audio files (with ambient background noise).
   - Produce a 75-second crisp screen recording of the golden demo flow as a zero-risk backup video.

---

### 👤 Teammate 3: Ojas
**Role:** PRISM Observability Lead, Evaluation Harness & Evidence Architect  
**Subsystems:** L5 Observability Spine, Dataset, Local Checker, Dashboard Evidence

#### Primary Responsibilities:
1. **PRISM Integration & Tracing (`app/observability/`):**
   - Use `prismtrace-sdk` / direct manual span ingestion (`POST /api/spans/ingest`) based on recipes in `research/prism/03-fastapi-agent-integration-recipe.md`.
   - Single shared `httpx.Client` lifecycle. Auth header: `X-PRISMtrace-Key`.
   - Tag all spans with `agent_id` (`roadside-baseline` for v0, `roadside-prompt-fix` for v1, `roadside-claimguard` for v2), `category` (A–F), and `set` (`dev` | `heldout`).
   - Log Commit Window transitions as span metadata (`transition: HELD->FROZEN->ABORTED`).
2. **Replay Set Construction (`evals/replay_set.json`):**
   - 60 scripted, pre-labelled test calls across 6 categories (40 Dev / 20 Held-out):
     - Cat A: Clean control (8 dev / 4 heldout)
     - Cat B: True revocation mid-call (7 dev / 3 heldout)
     - Cat C: Look-alike traps ("don't hold back, send it now") (8 dev / 4 heldout)
     - Cat D: Corrections & ambiguous requests (7 dev / 3 heldout)
     - Cat E: Emotional pressure & concession requests (6 dev / 4 heldout)
     - Cat F: Spoken identifiers (cards, Aadhaar) (4 dev / 2 heldout)
   - Pre-register by committing to git *before* benchmarking begins.
3. **Automated Checker (`evals/checker.py`):**
   - Run replay conversations against agent versions; calculate:
     - Wrong commits (executed after cancellation)
     - Wrong cancellations (killed wanted dispatches)
     - Spurious clarifying questions
     - Concession / ungrounded figure leaks
     - PII leakage count (target: 0)
     - Decision latency
4. **PRISM Runs & Credit Discipline (98 Credits Total):**
   - Run a 3-call smoke test batch first to verify credit burn rate.
   - Run v0 baseline and v2 ClaimGuard on held-out set as top priority; run v1 as prompt-fix bridge.
   - Export all session traces to JSON for PRISM's *Import History* offline fallback.
5. **Pitch Deck Data Injection:**
   - Capture PRISM dashboard screenshots (trace view with spans, Agent Intelligence failure clusters, CSAT/response quality deltas).
   - Inject measured, verified numbers into `presentation/claimguard-pitch.html`.

---

## 4. Inter-Module API & Contract Definitions

### 4.1 Client ➔ Server Turn Request (`POST /api/call/turn`)
```json
{
  "session_id": "cg-sess-2026-09-001",
  "turn_id": 3,
  "caller_id": "caller_9921",
  "raw_transcript": "Wait, don't send the tow truck, my cousin just showed up! Mera card number 4532 0150 1234 5678 hai for claim.",
  "masked_transcript": "Wait, don't send the tow truck, my cousin just showed up! Mera card number [CARD REDACTED] hai for claim.",
  "redacted_pii": [
    { "type": "CARD_NUMBER", "matched": "4532 0150 1234 5678", "valid_luhn": true }
  ]
}
```

### 4.2 Server ➔ Client Response (`200 OK`)
```json
{
  "session_id": "cg-sess-2026-09-001",
  "turn_id": 3,
  "agent_response": "Understood. I have cancelled the tow truck dispatch. Your claim remains active under policy NH-8821.",
  "state_machine": {
    "held_actions": [],
    "transitions": [
      {
        "action_id": "act_tow_01",
        "action_type": "stage_dispatch",
        "from_state": "FROZEN",
        "to_state": "ABORTED",
        "reason": "Caller revocation verified at turn 3"
      }
    ]
  },
  "current_claim": {
    "claim_id": "CLM-40192",
    "status": "OPEN_UNASSIGNED",
    "deductible_inr": 1500,
    "locked_fields": ["deductible_inr", "liability_ratio"]
  }
}
```

### 4.3 Server ➔ PRISM Ingest Span Contract (`POST /api/spans/ingest`)
```json
{
  "trace_id": "tr-sess-001-turn-03",
  "session_id": "cg-sess-2026-09-001",
  "spans": [
    {
      "span_id": "sp-turn-03",
      "name": "enforcement_commit_window",
      "start_time": "2026-09-14T17:40:00.000Z",
      "end_time": "2026-09-14T17:40:00.210Z",
      "attributes": {
        "agent_id": "roadside-claimguard",
        "category": "B_TRUE_REVOCATION",
        "set": "heldout",
        "action_held": "stage_dispatch",
        "action_final": "ABORTED",
        "pii_masked": true
      }
    }
  ]
}
```

---

## 5. Ready-to-Use Kickoff Prompts for Each Teammate

*Copy and paste the appropriate block below into your AI coding assistant (Antigravity, Claude Code, Cursor, etc.):*

### 📋 Kickoff Prompt for ALI (Backend, Enforcement & Server)
```text
You are pair programming with Ali on ClaimGuard (ForgeAI Hackathon).
Refer to Overall-plan.md for all architectural invariants and CLAUDE.md.

YOUR ROLE: Backend Lead, Intelligence & Enforcement Architect (L2 Cognition + L3 Enforcement + L4 Storage).
IMPORTANT SERVER NOTE: During development, you will run the backend locally on your own machine. For the final demo, your laptop will act as the master host for the team's live presentation and benchmark runs.

YOUR CORE DELIVERABLES:
1. app/agent/: Small-model tool loop (Llama-3-8B or Qwen-2.5-7B via llama.cpp or LiteLLM proxy fallback) with tools: lookup_policy, open_claim, stage_dispatch, update_claim, escalate_to_human.
2. app/rag/: Lightweight policy retrieval over NH48 corridor insurance policy text and SOPs.
3. app/enforcement/: 
   - Commit Window state machine (HELD -> FROZEN -> RESOLVE -> COMMITTED/ABORTED).
   - Policy Latch: SQLite DB triggers locking deductible and liability fields against LLM writes.
   - Outbound Veto: Intercepts spoken concession phrases and unverified rupee amounts before responses are finalized.
4. app/server.py: FastAPI server exposing /api/call/turn and /api/claims/status with OpenAPI documentation.
5. scripts/run_local_model.sh and scripts/start_server.sh for 1-command startup on demo day.

Start by implementing app/enforcement/commit_window.py and the SQLite policy latch schema in app/db/.
```

---

### 📋 Kickoff Prompt for PRATHAM (Voice, Security & Console)
```text
You are pair programming with Pratham on ClaimGuard (ForgeAI Hackathon).
Refer to Overall-plan.md and presentation/Slides-Plan.md for UI design guidelines and system flow.

YOUR ROLE: Voice Pipeline, Security & Supervisor Console Lead (L0 Client Edge + L1 Perception + L6 Human Console).
IMPORTANT SERVER NOTE: During development, run a lightweight local mock server or client dev server on your own laptop. Do not depend on Ali's machine being online while you develop.

YOUR CORE DELIVERABLES:
1. app/voice/: Speech-to-text integration using whisper.cpp / Faster-Whisper with Hindi/code-mixed prompt bias and Push-to-Talk (PTT) keyboard/button trigger.
2. app/security/pii_shield.py: Pre-LLM, pre-telemetry mathematical PII scrubber:
   - Credit/Debit cards: 13-19 digits with Luhn algorithm validation -> [CARD REDACTED].
   - Aadhaar: 12-digit numbers with Verhoeff algorithm validation -> [AADHAAR REDACTED].
   - Mobile: 10-digit Indian numbers -> [PHONE REDACTED].
3. frontend/: Live Supervisor Console matching the design system (warm cream #F8F6F1 canvas, roasted walnut typography #1E1915, imperial jade green #1B5E4B accents).
   - Live waveform & PTT control.
   - Real-time streaming transcript with dynamic redaction badges.
   - Commit Window board showing cards transition live: HELD (Amber) -> FROZEN (Purple) -> COMMITTED (Jade) / ABORTED (Crimson).
   - Standalone Mock Mode: Toggle to simulate incoming audio and state transitions locally without needing Ali's backend.
4. Recorded voice dataset: 20 noisy voice clips from the team and a recorded 75s screencast of the live call demo as emergency fallback.

Start by implementing app/security/pii_shield.py with unit tests for Luhn and Verhoeff checks.
```

---

### 📋 Kickoff Prompt for OJAS (PRISM Observability & Evals)
```text
You are pair programming with Ojas on ClaimGuard (ForgeAI Hackathon).
Refer to Overall-plan.md, research/prism/03-fastapi-agent-integration-recipe.md, and 10-evaluation-playbook.md.

YOUR ROLE: PRISM Observability Lead, Benchmark & Evaluation Architect (L5 Observability Spine + Replay Set + Checker).
IMPORTANT SERVER NOTE: During development, run the evaluation scripts against local mock agents or test harnesses on your own machine. Do not block on Ali's laptop.

YOUR CORE DELIVERABLES:
1. evals/replay_set.json: 60 pre-registered benchmark calls across categories A-F (40 dev / 20 held-out). Commit this to git before model evaluation begins.
2. evals/checker.py: Automated local evaluator scoring wrong commits, wrong cancellations, spurious clarifying questions, spoken concessions, PII leaks, and decision latency.
3. app/observability/prism_tracer.py: Direct PRISM tracing integration (using verified manual span ingest POST /api/spans/ingest).
   - Persistent httpx.Client singleton. Header: X-PRISMtrace-Key.
   - Tag spans with agent_id (roadside-baseline, roadside-prompt-fix, roadside-claimguard), category (A-F), and set (dev/heldout).
   - Emit Commit Window transitions as span attributes.
4. PRISM Run Execution (Strict 98-credit budget):
   - Run 3-call smoke test to verify credit consumption.
   - Run v0 baseline and v2 ClaimGuard on held-out set.
   - Export all session traces to JSON for PRISM Import History fallback.
5. Pitch Deck Integration:
   - Extract PRISM dashboard screenshots (span trace tree, Agent Intelligence failure clusters, CSAT/response quality deltas).
   - Update presentation/claimguard-pitch.html with the verified measured data.

Start by creating evals/replay_set.json with the 60 pre-registered conversation scenarios.
```
