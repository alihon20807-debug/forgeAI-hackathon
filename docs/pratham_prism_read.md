# PRISM Portal & Traces Guide for Pratham

**Target:** ForgeAI Hackathon · graVITas'26 · VIT Vellore  
**Core Thesis:** *PRISM is the hero, ClaimGuard is the vehicle. 40% of the judging rubric directly depends on PRISM evaluation & diagnosis.*

---

## 1. Executive Summary & Current State

The pipeline and observability infrastructure are built, tested, and passing offline:
- **Canonical Tracer:** [`app/observability/prism_tracer.py`](file:///home/aliz/Documents/Codes/forgeAI-hackathon/app/observability/prism_tracer.py) (`TurnTracer` / `PRISMTracer`).
- **Trace Tagging:** Every trace is correctly tagged with `agent_id` (`roadside-baseline` for v0, `roadside-prompt-fix` for v1, `roadside-claimguard` for v2), `category` (A–F), and `set` (`dev`/`heldout`).
- **Enforcement Spans:** Commit Window state machine transitions (`HELD` ➔ `FROZEN` ➔ `COMMITTED`/`ABORTED`) are recorded as discrete spans.
- **Benchmark & Diagnostic Script:** [`scripts/prism_benchmark.py`](file:///home/aliz/Documents/Codes/forgeAI-hackathon/scripts/prism_benchmark.py) supports `--status`, `--smoke`, `--heldout`, and `--export`.
- **Local Fallback:** Traces buffer automatically to [`data/prism_traces.jsonl`](file:///home/aliz/Documents/Codes/forgeAI-hackathon/data/prism_traces.jsonl) and [`data/prism_traces_export.json`](file:///home/aliz/Documents/Codes/forgeAI-hackathon/data/prism_traces_export.json) for PRISM's *Import History* feature.

---

## 2. Architectural Review & Technical Nuances

### 2.1 Schema Compliance: `span_type` Values
- In [`app/observability/prism_tracer.py:184`](file:///home/aliz/Documents/Codes/forgeAI-hackathon/app/observability/prism_tracer.py#L184), enforcement state transitions are emitted with:
  ```python
  "span_type": "guardrail"
  ```
- **Nuance:** PRISM's SDK and ingestion engine specify a closed vocabulary for `span_type`:
  ```
  chain | llm | tool | agent | retrieval
  ```
- **Risk & Fix:** If the PRISM portal drops or errors on `"guardrail"`, update `span_type` to `"tool"` or `"chain"` and keep the enforcement details in `attributes`:
  ```python
  "span_type": "tool",
  "name": "enforcement_commit_window"
  ```

### 2.2 Trace Ingestion vs. Cloud Reachability
- **Outbound Tracing (Passive):** Pushing traces and spans from your laptop to `https://prism-api-prod.up.railway.app` is outbound HTTPS. It requires **no tunneling or port forwarding**.
- **Inbound Evaluation (Active Proxy / Synthetic Scenarios):** If you use PRISM’s cloud-hosted synthetic scenarios generator or reverse proxy to call the local LLM, PRISM cannot hit `http://localhost:8080`. For that use case, run:
  ```bash
  ./scripts/expose_local_model.sh 8080
  # or ./scripts/run_local_model.sh --expose
  ```
  This creates a zero-friction Cloudflare tunnel (`https://<hash>.trycloudflare.com/v1`).

---

## 3. Checklist: What Pratham Has Left to Do

### Step 1: Environment Setup
Create a `.env` file at the root of the repo (refer to `.env.example`):
```bash
PRISMTRACE_HOST=https://prism-api-prod.up.railway.app
PRISMTRACE_PROJECT_ID=066e7755-d375-4690-b4a7-4492d33f680b
PRISMTRACE_API_KEY=<YOUR_ACTUAL_PRISM_API_KEY>
```

### Step 2: Diagnostic Probe (0 Credits)
Verify that the host, project, and authentication key are valid:
```bash
uv run python -m scripts.prism_benchmark --status
```
Expected output: `PRISM endpoint healthy (HTTP 200/201)`.

### Step 3: Smoke Test Run (3 Credits)
Execute a mandatory 3-scenario smoke test (Cat A clean control, Cat B revocation, Cat E emotional pressure):
```bash
uv run python -m scripts.prism_benchmark --smoke
```
* **Portal Check:** Open the PRISM dashboard immediately.
* Confirm that 3 session traces appear under project `066e7755-d375-4690-b4a7-4492d33f680b`.
* Verify credit consumption on the account (Free Tier budget: 98 credits).

### Step 4: Held-Out Benchmark Ingestion (Priority: v0 and v2)
Once the smoke test confirms clean ingestion:
```bash
uv run python -m scripts.prism_benchmark --heldout
```
* Ingests the 20 pre-registered held-out calls for `v0` (`roadside-baseline`) and `v2` (`roadside-claimguard`).
* Ingest `v1` (`roadside-prompt-fix`) only if credits permit.

### Step 5: Capture Visual Evidence for Pitch Deck
Capture three high-resolution screenshots from the PRISM portal:
1. **Span Trace Tree:** A turn showing nested tool calls, PII redaction, and `enforcement_commit_window` state transitions.
2. **Agent Intelligence & Failure Hotspots:** Dashboard view displaying v0 failure clusters (wrong commits in Cat B, concession leaks in Cat E) compared to v2 clean compliance.
3. **CSAT / Response Quality Delta:** The before-and-after evaluation summary.

Save the screenshots under `assets/prism/` (e.g., `assets/prism/trace_tree.png`, `assets/prism/failure_clusters.png`).

### Step 6: Deck Integration & PDF Re-Export
1. Update Slide 4 in `presentation/claimguard-pitch.html` and `presentation/claimguard-pitch-offline.html` to reference the captured screenshots.
2. Re-export the PDF:
   ```bash
   node /home/aliz/Documents/Codes/md2pdf/md2pdf.js presentation/claimguard-pitch.html -o presentation/claimguard-pitch.pdf
   ```

---

## 4. Potential Blockers & Mitigations

| Blocker | Impact | Mitigation |
|---|---|---|
| **Missing API Key / .env** | Cannot send live traces; operates only in local buffer mode | Ensure `.env` is created on the demo machine with valid credentials. |
| **Credit Burn Exhaustion** | 98-credit budget exceeded before held-out traces are recorded | Never run the full 60-call dev set on live credits. Stick strictly to `--smoke` (3 calls) $\to$ `--heldout` (v0 + v2, 40 calls). |
| **Ingest Rate Limit (HTTP 429)** | Ingestion drops spans during rapid batch execution (limit: 200 req/min) | Run batch scripts with a small inter-scenario pause (`--heldout` includes pacing). |
| **Venue Wi-Fi Failure / High Latency** | Cloud portal unreachable during live judging | Use [`data/prism_traces_export.json`](file:///home/aliz/Documents/Codes/forgeAI-hackathon/data/prism_traces_export.json) with PRISM’s *Import History* feature or project offline slides with saved screenshots. |

---

## 5. How Teammates Can Support Pratham

* **Ali:** Host the local LLM server and expose it via tunnel if cloud synthetic evaluation is requested; monitor server logs during benchmark runs.
* **Ojas:** Help capture and crop PRISM dashboard screenshots; ensure Slide 4 styling in `claimguard-pitch.html` fits the project design aesthetic.
