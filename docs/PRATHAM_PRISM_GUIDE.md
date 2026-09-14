# PRISM Observability & Evidence Guide (for Pratham)
**Canonical Reference:** `docs/Overall-plan.md` §13 & §14  
**Primary Subsystems:** PRISM Tracing, Ingestion, 98-Credit Budget, Dashboard Screenshots

---

## ⚡ Quickstart — 4 Commands to Complete All PRISM Deliverables

### Step 0: Set Your PRISM API Key
Set your key in your terminal (or add `PRISMTRACE_API_KEY=pt-sk-...` to `.env`):
```bash
export PRISMTRACE_API_KEY="pt-sk-your-key-here"
```
*(Project ID is pre-configured to `066e7755-d375-4690-b4a7-4492d33f680b`, Host is `https://prism-api-prod.up.railway.app`)*

---

### Step 1: Test Connection (0 Credits, Diagnostic Probe)
Verify that your API key and project ID are accepted:
```bash
.venv/bin/python scripts/prism_benchmark.py --status
```
✅ Expected: `PRISM probe status: 200` / `PRISM endpoint healthy`.

---

### Step 2: 3-Call Smoke Test (Mandatory Credit Discipline)
Per `Overall-plan.md` §14, run exactly 3 representative calls (Cat A, Cat B, Cat E) first:
```bash
.venv/bin/python scripts/prism_benchmark.py --smoke
```
1. Open your PRISM dashboard.
2. Check your credit burn (confirm remaining credits out of the 98-credit budget).
3. Confirm that the 3 sessions appear with `agent_id="roadside-claimguard"`.

---

### Step 3: Ingest the Held-Out Benchmark Suite
Run the 20 pre-registered held-out test calls across `v0 Baseline`, `v1 Prompt-Fix`, and `v2 ClaimGuard`:
```bash
.venv/bin/python scripts/prism_benchmark.py --heldout
```
- Automatically tags every trace with:
  - `agent_id`: `roadside-baseline` (v0) / `roadside-prompt-fix` (v1) / `roadside-claimguard` (v2)
  - `category`: `A_CLEAN_CONTROL` to `F_SPOKEN_IDENTIFIERS`
  - `set`: `heldout`
- Automatically records Commit Window transitions (`HELD -> FROZEN -> ABORTED`) as span attributes.

---

### Step 4: Export JSON for Dashboard Import History (Offline Fallback)
Export all local buffer traces into a clean PRISM-compliant JSON array:
```bash
.venv/bin/python scripts/prism_benchmark.py --export
```
✅ Output: `data/prism_traces_export.json`  
This file can be uploaded via PRISM's **Import History** button in case auditorium Wi-Fi fails during the pitch.

---

## 📸 What Screenshots to Capture for the Pitch Deck (Slide 4)

Capture these 3 views from your PRISM dashboard and drop them into `assets/prism/`:
1. **Span Trace Tree (`assets/prism/trace_tree.png`):**
   - Click any Cat B call (e.g. `cg-v2-B_heldout_01`).
   - Shows the root `agent_turn` with child spans for `enforcement_commit_window` displaying `transition: HELD->FROZEN->ABORTED`.
2. **Session / Fleet Comparison View (`assets/prism/fleet_comparison.png`):**
   - Filter by `agent_id`: compare `roadside-baseline` vs `roadside-claimguard`.
   - Highlights the 0% vs 100% cancellation abort rate.
3. **Agent Intelligence / CSAT Delta (`assets/prism/csat_quality.png`):**
   - Shows automatic response quality and compliance/CSAT scores across versions.

---

## 🛠️ Architecture & Under-the-Hood Details

- **Single Canonical Tracer:** `app/observability/prism_tracer.py` (`TurnTracer`).
- **Endpoint:** Direct manual span ingest (`POST /api/spans/ingest`).
- **Headers:** `X-PRISMtrace-Key: <key>` and `Content-Type: application/json`.
- **Fail-Open:** If the network drops, traces are automatically saved locally to `data/prism_traces.jsonl` without failing user turns.
