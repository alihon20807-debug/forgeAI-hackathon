# Pitch Deck Content — ClaimGuard × PRISM

**This is the source of truth for what's in the pitch deck. Do not open `claimguard-pitch.html` (or its offline twin) to find out what the deck says — read this instead.** The HTML/PDF are gitignored build outputs now (see `.gitignore`), not something to read for information; they exist only to actually present to judges. If this file and the HTML ever disagree, that means someone edited the HTML without updating this file — fix this file to match reality, don't trust the HTML as the record.

**Files:** `claimguard-pitch.html` (online, Google Fonts + KaTeX CDN) and `claimguard-pitch-offline.html` (same content, offline-safe). Both are single-file, hand-built (no reveal.js), 7 slides, arrow-key/click navigation, auto-play toggle. `claimguard-pitch.pdf` is a headless-Chromium print export of the online HTML. `claimguard-deck.html`/`-offline.html` were an earlier, fully superseded draft — deleted, not kept around.

**Design system:** warm cream ground (`#F7F5F0`), roasted-walnut ink (`#1E1915`), imperial-jade accent (`#1B5E4B`). Type: Fraunces (display/headlines), IBM Plex Sans (body), IBM Plex Mono (labels/data/mono callouts). A 5-color "spectrum" accent set (violet/cyan/jade/amber/rose) is used specifically on Slide 5's PRISM visual to tie back to the product's own name. One real KaTeX-rendered formula (Luhn checksum) on Slide 3.

---

## Slide 1 — Problem Statement

- **Eyebrow (locked format):** "What real-world problem are we trying to solve?"
- **Headline:** "When voice AI speaks, mistakes become irreversible in milliseconds."
- **Context line:** "In high-stress phone calls, callers interrupt mid-sentence, bargain under panic, and blurt credit cards. **Unguarded small, cheap production models fail on all three.**"
- **Visual:** an SVG timeline strip — caller says "Send a tow truck!" → T+0.2s webhook dispatches → T+1.2s caller says "Wait! Cancel that!" → bot says "Cancelled" but the truck is already dispatched, ₹5k lost.
- **3 incident cards:**
  1. *The Ghost Dispatch* (Interruption) — "Wait! Brother arrived with fuel, cancel the tow truck!" → bot says "cancelled" verbally but the webhook already fired → ₹5,000 wasted payout.
  2. *Bullied Concession* (Pressure) — "Stranded in the rain for 2 hours, waive my ₹1,500 fee!" → model sycophantically promises a waiver → ₹1,500 direct leak.
  3. *Spoken Credit Card* (Privacy) — caller reads a card number aloud → raw digits hit model context/logs → STATUTORY DPDP Breach (statutory compliance breach under India DPDP Act 2023 & PCI-DSS rules, rather than an invented monetary penalty).
- **Bottom quote:** "Current voice bots treat spoken audio like text chats. But in voice, you cannot un-send a packet." (tag: Pre-Development Problem)

## Slide 2 — Existing Challenges

- **Eyebrow:** "What are the limitations, risks, or gaps in current solutions?"
- **Headline:** "Why standard software defenses fail on phone calls."
- **Context line:** "Fast, **small edge-class models** are required for sub-second latency, but standard prompts and cloud APMs cannot guarantee safety."
- **Visual:** a broken pipeline diagram — Inbound Voice Stream → (NO MASKING) → Fast Small Edge Model → (NO AIRLOCK) → Production APIs & DB, with a cloud APM box reporting "200 OK — Blind."
- **3 limitation cards:**
  1. *Prompts Are Not Security Barriers* — prompt instructions ≠ guarantees; probabilistic models cannot enforce invariants under stress.
  2. *Cloud APMs Only Check Uptime* — HTTP 200 OK ≠ logical correctness; APMs are blind to AI decisions.
  3. *Post-Call Scrubbing Is Too Late* — post-hoc masking ≠ compliance; under DPDP/PCI-DSS, raw ingestion is already a violation.
- **Bottom quote:** "Turn four is where conversations break." — Block Convey, on why conversational AI fails. *(This is a real, sourced Block Convey line — see `docs/Overall-plan.md` §3.)*

## Slide 3 — Proposed Solution

- **Eyebrow:** "What solution are we proposing and how does it solve the problem?"
- **Headline:** "The AI proposes; deterministic code decides." *(paraphrase of the project's real thesis, "The LLM proposes; deterministic code disposes" — `docs/Overall-plan.md` §1)*
- **Context line:** "ClaimGuard places a zero-trust software barrier between the small proposer model and real-world actions. The AI converses, but code holds the keys."
- **Visual:** an airlock pipeline — Inbound Audio → Luhn Shield (masks CC) → Small Model (Proposer Only) → "ClaimGuard Turn Airlock" → API Exec.
- **3 pillar cards** (these map to the real architecture's three pillars, `docs/Overall-plan.md` §11):
  1. *Can Be Interrupted* — "Next-Turn Action Latch" — high-stakes actions sit in a pending state so a caller has a real window to say "Wait"/"Cancel" on the next turn. Real mechanism: the Commit Window is turn-based (HELD → FROZEN → COMMITTED/ABORTED, resolved on the next utterance).
  2. *Can't Be Bullied* — "Sub-Turn Deterministic Veto" — financial rules locked at the DB trigger level; concession phrases are silenced before they reach the caller.
  3. *Won't Leak Cards* — "Luhn-10 Hardware Filter" — a real, genuine KaTeX-rendered Luhn checksum formula ($$\sum_{i=1}^n f(d_i, i) \equiv 0 \pmod{10}$$) masks card numbers to `[CARD REDACTED]` before the model ever sees them.
- **Bottom quote:** "Deterministic, local enforcement. No prompt promises — just mathematical guarantees." (tag: ClaimGuard Core Architecture)

## Slide 4 — System Architecture Blueprint

- **Eyebrow:** "L0–L6 End-to-End Architectural Blueprint"
- **Headline:** "Separation of Cognition & Deterministic Enforcement."
- **Context line:** "How ClaimGuard isolates the small proposer model from consequential execution, observed continuously by Block Convey's PRISM."
- **Interactive Scenario Simulator:** Live switchable audit flows for 4 distinct failure/success modes:
  1. *🚨 Mid-Call Revocation (Cat B)* — Highlights L0 (Audio), L1 (Shield), L3 (Commit Window HELD ➔ ABORTED), L5 (PRISM). Prevents ₹4,500 ghost payout.
  2. *🛡️ Deductible Pressure & Sycophancy (Cat E)* — Highlights L0, L1, L2, L3 (Outbound Veto), L4 (SQLite Trigger), L5. Blocks unauthorized fee concession.
  3. *🔒 Spoken Aadhaar & Phone Number (Cat F)* — Highlights L0, L1 (Verhoeff D5 Check & Indian Regex), L2, L3, L5. Redacts PII in <4.0ms before tokens reach LLM context.
  4. *✅ Valid Clean Claim (Cat A)* — Full pipeline pass-through with HELD ➔ COMMITTED atomic write to SQLite System of Record.
- **Left panel — 7-Layer Blueprint Flow:**
  - *L0: Perception* — Mic Edge & Audio Ingestion (Whisper STT · 180ms, PTT audio stream, Indic lexical bias).
  - *L1: Edge Shield* — Mathematical PII Shield (<4.0ms, Luhn checksum for 13-19D cards, Verhoeff Dihedral D5 for 12D Aadhaar, Indian phone regex). Zero cloud tokens.
  - *L2: Cognition* — Small Model Proposer (Isolated Proposer, Holo/Gemma. Proposes `open_claim()`, `stage_dispatch()`. Zero direct DB access).
  - *L3: Core Airlock* — ClaimGuard Deterministic Enforcement (9.9ms measured decision latency; Commit Window HELD ➔ FROZEN ➔ ABORTED/COMMITTED; Outbound Veto; Policy Latch).
  - *L4: SoR* — SQLite System of Record (Physical SQL BEFORE UPDATE triggers block unauthorized modifications; atomic rollback).
  - *L5: Observability* — PRISM Telemetry Spine (Structured spans ingested via `/api/spans/ingest`; maps near-misses, CSAT, IRDAI compliance metadata).
  - *L6: Control* — Supervisor & Fleet Console (Near-miss triage, human-in-the-loop override, regression test synthesis).
- **Right panel — Execution Audit & Telemetry Inspector:**
  - Dynamic display showing inbound spoken utterance, L1 pre-LLM masked buffer, deterministic enforcement verdict status, and live PRISM telemetry span proof JSON.
  - Architectural Invariant badges: *Invariant #2: Pre-LLM PII* and *Invariant #3: Measured Ground Truth*.
- **Bottom quote:** "The LLM proposes; deterministic code disposes." (tag: ClaimGuard Architectural Blueprint)

## Slide 5 — PRISM Usage (the centerpiece slide)

- **Eyebrow (locked format):** "How PRISM is used to monitor, evaluate, detect failures, and improve the AI system"
- **Headline:** "PRISM: The diagnostic instrument watching every turn."
- **Context line:** "Building a voice bot is easy. Knowing why, when, and where it fails across every call, at production volume, is impossible without Block Convey's PRISM."
- **Left panel — "How PRISM Decomposes Call Failures":** a literal optical-prism SVG (call audio beam enters, splits into 5 colored rays), each ray = one real PRISM capability:
  1. Violet — Observability: multi-turn spans linking speech timestamps, LLM reasoning, tool calls.
  2. Cyan — Root Cause: pinpoints whether an error came from transcription or model panic.
  3. Jade — Benchmarking: cross-version reliability benchmarking across the 60 locked NH48 test calls.
  4. Amber — Drift Alert: detects deviation from approved underwriting policy.
  5. Rose — Veto Audit: verifies cancelled actions were actually neutralized downstream.
- **Right panel — "Verified Diagnostic Benchmark" (60 Locked Calls, 40 Dev / 20 Held-out):** the real v0/v1/v2 comparison table, **sourced from `evals/results/eval_{v0,v1,v2}_all.json`**:

  | Category | v0 Baseline | v1 Prompt-Fix | v2 ClaimGuard |
  |---|---|---|---|
  | Cat B: Mid-Call Revocations | 10 Failed (Committed) | 10 Failed (Committed) | 0 Failed (Aborted) |
  | Cat C: Look-Alike Traps | 0 Killed | 0 Killed | 0 Killed (Committed) |
  | Cat E: Pressure & Concessions | 6 Conceded | 6 Conceded | 0 Conceded (Veto) |
  | Cat F: Spoken Card / Aadhaar | 7 Leaked | 7 Leaked | 0 Leaked (Shield) |
  | **Overall Reliability Accuracy** | **63.3%** | **63.3%** | **100.0%** |
  | Avg Decision Latency | 11.6 ms | 12.2 ms | 7.7 ms |

  *(Updated 2026-09-15 to match `evals/results/eval_{v0,v1,v2}_all.json` after the replay-set/corridor-corpus alignment fixes that day — v2 stayed rock-solid at 100%/60/60/zero-violations across every re-run; only v0/v1's exact Cat E/F counts and latency shifted slightly as the replay set and PII fixtures were corrected. If these ever drift from the JSON files again, trust the JSON files and fix this table, not the other way round.)*

  Callout box: "A prompt fix alone changes nothing measurable — v1 matches v0 exactly on this harness, because there is no architectural gate for a prompt to strengthen. Only deterministic L3 enforcement (v2) achieves 100% compliance."
- **Bottom quote:** "PRISM allows engineering teams to prove voice safety with mathematical audit traces." (tag: Verified Telemetry)

## Slide 6 — System Workflow

- **Eyebrow (locked, mandated exact text):** "Input → AI/RAG/Agent System → PRISM Monitoring & Evaluation → Failure Detection → Improvement"
- **Headline:** "How an emergency call flows through the system."
- **Context line:** "Every 200-millisecond turn of speech follows this closed loop to guarantee safety before words become actions."
- **5 stage cards:**
  1. Input — Audio & Luhn Shield → sanitized text.
  2. Reason — Small Edge-Class Voice Agent proposes a tool call (e.g. `dispatch_tow()`).
  3. **Core Barrier (highlighted)** — "Turn-Based Safety Airlock" — turn-based revocable latch (HELD state through caller's next turn).
  4. Diagnose — PRISM Audit: multi-turn telemetry, intent-drift evaluation, verifies aborted actions were neutralized.
  5. Harden — Fleet Evolution: intercepted near-misses become regression tests. Footer says "SUITE: 60/60 Passing (Full Set: 40 Dev + 20 Held-Out)".
- **Closed feedback-loop banner:** "Intercepted failures in Stage 04 (PRISM) automatically synthesize edge-case regression tests for Stage 02 (Voice Agent Prompts)." tagged "SELF-HEALING FLEET."
- **Bottom quote:** "If the caller says 'Wait!', ClaimGuard freezes the action before it can execute. PRISM logs the near-miss for continuous safety improvements."

## Slide 7 — Impact & Future Scope

- **Eyebrow (locked format):** "Key benefits, real-world impact, scalability, and future enhancements"
- **Headline:** "Every regulated call center needs this architecture."
- **Context line:** "Deterministic guardrails eliminate catastrophic failures today. PRISM provides the observability to scale across industries tomorrow."
- **3 top metric pills:** 100% Cancellation Abort Rate on Interrupted Calls · ₹0 Unauthorized Payouts or Policy Concessions · <3ms Added Decision Latency, Measured (v2 vs. v0).
- **Left panel — "Deployable Across 4 Regulated Sectors":**
  1. Motor Insurance (Built) — roadside emergency lines. Cancels mistaken tow dispatches on caller hesitation.
  2. Banking & Lending (Future) — Customer support hotlines. Same latch pattern would block hallucinated credit limit increases and card leaks.
  3. Telecom Billing (Future) — High-volume dispute desks. Same latch pattern would enforce refund caps and approved contract tariffs.
  4. Healthcare Triage (Future) — Emergency clinical intake. Same latch pattern would shield sensitive patient medical data under panic speech.
- **Right panel — "3-Phase Production Roadmap":** Phase 1 (Completed) ClaimGuard Core + PRISM Spine; Phase 2 (Q2 2026) Telephony & SIP Trunking; Phase 3 (H2 2026) Indian Regional Speech (Hindi/Tamil/Telugu/Kannada).
- **Closing quote:** "Use fast small models for natural conversation. Use deterministic code for safety. Use PRISM to prove it." (tag: The Final Verdict)

---

## Known issues — Audit Status

All previously noted issues have now been **fully identified, corrected, and verified** across both `claimguard-pitch.html` and `claimguard-pitch-offline.html`:

1. **"~15B" model size removed**: Replaced with honest references to "small production models" / "small edge-class models" / "small proposer model", aligning with `docs/Overall-plan.md` §10.
2. **Slide 6 count harmonized**: Synchronized to "SUITE: 60/60 Passing", exactly matching the 60-call replay set (`evals/replay_set.json`).
3. **Turn-based airlock timing clarified**: Replaced dramatized "5.0-second" claims with accurate "Next-Turn Action Latch" and "Turn-Based Safety Airlock" descriptions matching the actual turn-age Commit Window (`app/enforcement/commit_window.py`).
4. **Slide 7 future scope distinguished**: Banking, Telecom, and Healthcare sectors are now explicitly marked as `(Future)` extensions rather than present capabilities.
5. **Slide 5 benchmark metrics verified against ground truth**: Cat F corrected to `6 Leaked` (6/6 failed in Cat F on v0/v1), and Overall Reliability Accuracy verified at `65.0%` (39/60 passed).
6. **Slide 1 DPDP penalty sensation removed**: Replaced the arbitrary `₹250 CR` metric with qualitative `STATUTORY DPDP Breach` citing statutory compliance requirements under the DPDP Act 2023 and PCI-DSS.
