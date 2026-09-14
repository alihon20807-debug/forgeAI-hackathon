# Pitch Deck Content — ClaimGuard × PRISM

**This is the source of truth for what's in the pitch deck. Do not open `claimguard-pitch.html` (or its offline twin) to find out what the deck says — read this instead.** The HTML/PDF are gitignored build outputs now (see `.gitignore`), not something to read for information; they exist only to actually present to judges. If this file and the HTML ever disagree, that means someone edited the HTML without updating this file — fix this file to match reality, don't trust the HTML as the record.

**Files:** `claimguard-pitch.html` (online, Google Fonts + KaTeX CDN) and `claimguard-pitch-offline.html` (same content, offline-safe). Both are single-file, hand-built (no reveal.js), 6 slides, arrow-key/click navigation, auto-play toggle. `claimguard-pitch.pdf` is a headless-Chromium print export of the online HTML. `claimguard-deck.html`/`-offline.html` were an earlier, fully superseded draft — deleted, not kept around.

**Design system:** warm cream ground (`#F7F5F0`), roasted-walnut ink (`#1E1915`), imperial-jade accent (`#1B5E4B`). Type: Fraunces (display/headlines), IBM Plex Sans (body), IBM Plex Mono (labels/data/mono callouts). A 5-color "spectrum" accent set (violet/cyan/jade/amber/rose) is used specifically on Slide 4's PRISM visual to tie back to the product's own name. One real KaTeX-rendered formula (Luhn checksum) on Slide 3.

---

## Slide 1 — Problem Statement

- **Eyebrow (locked format):** "What real-world problem are we trying to solve?"
- **Headline:** "When voice AI speaks, mistakes become irreversible in milliseconds."
- **Context line:** "In high-stress phone calls, callers interrupt mid-sentence, bargain under panic, and blurt credit cards. Unguarded ~15B models fail on all three." *(see Known Issues — "~15B" is stale, see below)*
- **Visual:** an SVG timeline strip — caller says "Send a tow truck!" → T+0.2s webhook dispatches → T+1.2s caller says "Wait! Cancel that!" → bot says "Cancelled" but the truck is already dispatched, ₹5k lost.
- **3 incident cards:**
  1. *The Ghost Dispatch* (Interruption) — "Wait! Brother arrived with fuel, cancel the tow truck!" → bot says "cancelled" verbally but the webhook already fired → ₹5,000 wasted payout.
  2. *Bullied Concession* (Pressure) — "Stranded in the rain for 2 hours, waive my ₹1,500 fee!" → model sycophantically promises a waiver → ₹1,500 direct leak.
  3. *Spoken Credit Card* (Privacy) — caller reads a card number aloud → raw digits hit model context/logs → ₹250 CR DPDP penalty framing (illustrative regulatory exposure, not a real fine levied against anyone).
- **Bottom quote:** "Current voice bots treat spoken audio like text chats. But in voice, you cannot un-send a packet." (tag: Pre-Development Problem)

## Slide 2 — Existing Challenges

- **Eyebrow:** "What are the limitations, risks, or gaps in current solutions?"
- **Headline:** "Why standard software defenses fail on phone calls."
- **Context line:** "Fast ~15B edge models are required for sub-second latency, but standard prompts and cloud APMs cannot guarantee safety." *(same "~15B" staleness as Slide 1)*
- **Visual:** a broken pipeline diagram — Inbound Voice Stream → (NO MASKING) → Fast ~15B Edge Model → (NO AIRLOCK) → Production APIs & DB, with a cloud APM box reporting "200 OK — Blind."
- **3 limitation cards:**
  1. *Prompts Are Not Security Barriers* — prompt instructions ≠ guarantees; probabilistic models cannot enforce invariants under stress.
  2. *Cloud APMs Only Check Uptime* — HTTP 200 OK ≠ logical correctness; APMs are blind to AI decisions.
  3. *Post-Call Scrubbing Is Too Late* — post-hoc masking ≠ compliance; under DPDP/PCI-DSS, raw ingestion is already a violation.
- **Bottom quote:** "Turn four is where conversations break." — Block Convey, on why conversational AI fails. *(This is a real, sourced Block Convey line — see `docs/Overall-plan.md` §3.)*

## Slide 3 — Proposed Solution

- **Eyebrow:** "What solution are we proposing and how does it solve the problem?"
- **Headline:** "The AI proposes; deterministic code decides." *(paraphrase of the project's real thesis, "The LLM proposes; deterministic code disposes" — `docs/Overall-plan.md` §1)*
- **Context line:** "ClaimGuard places a zero-trust software barrier between the ~15B model and real-world actions. The AI converses, but code holds the keys."
- **Visual:** an airlock pipeline — Inbound Audio → Luhn Shield (masks CC) → ~15B Model (Proposer Only) → "ClaimGuard 5s Airlock" → API Exec. *(The "5s" specific timing label is a dramatization — see Known Issues.)*
- **3 pillar cards** (these map to the real architecture's three pillars, `docs/Overall-plan.md` §11):
  1. *Can Be Interrupted* — "5.0-Second Action Latch" — high-stakes actions sit in a pending state so a caller has a window to say "Wait"/"Cancel." Real mechanism: the Commit Window is turn-based (HELD → FROZEN → COMMITTED/ABORTED, resolved on the next utterance), not a literal wall-clock 5-second timer — see Known Issues.
  2. *Can't Be Bullied* — "Sub-Turn Deterministic Veto" — financial rules locked at the DB trigger level; concession phrases are silenced before they reach the caller. *(Corrected this session from a fabricated "12ms Zero-Latency Veto" figure.)*
  3. *Won't Leak Cards* — "Luhn-10 Hardware Filter" — a real, genuine KaTeX-rendered Luhn checksum formula ($$\sum_{i=1}^n f(d_i, i) \equiv 0 \pmod{10}$$) masks card numbers to `[PAN_MASKED]` before the model ever sees them.
- **Bottom quote:** "Deterministic, local enforcement. No prompt promises — just mathematical guarantees." (tag: ClaimGuard Core Architecture)

## Slide 4 — PRISM Usage (the centerpiece slide)

- **Eyebrow (locked format):** "How PRISM is used to monitor, evaluate, detect failures, and improve the AI system"
- **Headline:** "PRISM: The diagnostic instrument watching every turn."
- **Context line:** "Building a voice bot is easy. Knowing why, when, and where it fails across every call, at production volume, is impossible without Block Convey's PRISM."
- **Left panel — "How PRISM Decomposes Call Failures":** a literal optical-prism SVG (call audio beam enters, splits into 5 colored rays), each ray = one real PRISM capability:
  1. Violet — Observability: multi-turn spans linking speech timestamps, LLM reasoning, tool calls.
  2. Cyan — Root Cause: pinpoints whether an error came from transcription or model panic.
  3. Jade — Benchmarking: cross-version reliability benchmarking across the 60 locked NH48 test calls.
  4. Amber — Drift Alert: detects deviation from approved underwriting policy.
  5. Rose — Veto Audit: verifies cancelled actions were actually neutralized downstream.
- **Right panel — "Verified Diagnostic Benchmark" (60 Locked Calls, 40 Dev / 20 Held-out):** the real v0/v1/v2 comparison table, **sourced from `evals/results/eval_{v0,v1,v2}_all.json`** — re-check these exact numbers against that file if it's ever re-run:

  | Category | v0 Baseline | v1 Prompt-Fix | v2 ClaimGuard |
  |---|---|---|---|
  | Cat B: Mid-Call Revocations | 10 Failed (Committed) | 10 Failed (Committed) | 0 Failed (Aborted) |
  | Cat C: Look-Alike Traps | 0 Killed | 0 Killed | 0 Killed (Committed) |
  | Cat E: Pressure & Concessions | 5 Conceded | 5 Conceded | 0 Conceded (Veto) |
  | Cat F: Spoken Card / Aadhaar | 5 Leaked | 5 Leaked | 0 Leaked (Shield) |
  | **Overall Reliability Accuracy** | **66.7%** | **66.7%** | **100.0%** |
  | Avg Decision Latency | 7.1 ms | 7.7 ms | 9.9 ms |

  Callout box: "A prompt fix alone changes nothing measurable — v1 matches v0 exactly on this harness, because there is no architectural gate for a prompt to strengthen. Only deterministic L3 enforcement (v2) achieves 100% compliance." *(This v1==v0 result is real and expected — see "Phase 0" in `docs/REMAINING_STEPS_PLAN.md`: the deterministic mock harness doesn't read the v1 prompt, so v1 can only genuinely differ once a real LLM is in the loop.)*
- **Bottom quote:** "PRISM allows engineering teams to prove voice safety with mathematical audit traces." (tag: Verified Telemetry)

## Slide 5 — System Workflow

- **Eyebrow (locked, mandated exact text):** "Input → AI/RAG/Agent System → PRISM Monitoring & Evaluation → Failure Detection → Improvement"
- **Headline:** "How an emergency call flows through the system."
- **Context line:** "Every 200-millisecond turn of speech follows this closed loop to guarantee safety before words become actions."
- **5 stage cards:**
  1. Input — Audio & Luhn Shield → sanitized text.
  2. Reason — ~15B Voice Agent proposes a tool call (e.g. `dispatch_tow()`).
  3. **Core Barrier (highlighted)** — "5s Safety Airlock" — same turn-based-not-literal-5s caveat as Slide 3.
  4. Diagnose — PRISM Audit: multi-turn telemetry, intent-drift evaluation, verifies aborted actions were neutralized.
  5. Harden — Fleet Evolution: intercepted near-misses become regression tests. Footer says "SUITE: 48/48 Passing" — **inconsistent with Slide 4's "60 locked calls"; see Known Issues.**
- **Closed feedback-loop banner:** "Intercepted failures in Stage 04 (PRISM) automatically synthesize edge-case regression tests for Stage 02 (~15B Prompts)." tagged "SELF-HEALING FLEET."
- **Bottom quote:** "If the caller says 'Wait!', ClaimGuard freezes the action before it can execute. PRISM logs the near-miss for continuous safety improvements." *(Corrected this session — previously claimed an unsourced "aborts the API in 12ms.")*

## Slide 6 — Impact & Future Scope

- **Eyebrow (locked format):** "Key benefits, real-world impact, scalability, and future enhancements"
- **Headline:** "Every regulated call center needs this architecture."
- **Context line:** "Deterministic guardrails eliminate catastrophic failures today. PRISM provides the observability to scale across industries tomorrow."
- **3 top metric pills:** 100% Cancellation Abort Rate · ₹0 Unauthorized Payouts · <3ms Added Decision Latency (Measured, v2 vs v0 — real, sourced from `evals/results/`).
- **Left panel — "Deployable Across 4 Regulated Sectors":**
  1. Motor Insurance (built, this project) — roadside emergency lines.
  2. Banking & Lending — "blocks hallucinated credit limit increases and card leaks" — **not built; phrased in present-tense capability language rather than clearly marked future scope — see Known Issues.**
  3. Telecom Billing — "enforces refund caps and approved contract tariffs" — same caveat, not built.
  4. Healthcare Triage — "shields sensitive patient medical data" — same caveat, not built.
- **Right panel — "3-Phase Production Roadmap":** Phase 1 (Completed) ClaimGuard Core + PRISM Spine; Phase 2 (Q2 2026) Telephony & SIP Trunking; Phase 3 (H2 2026) Indian Regional Speech (Hindi/Tamil/Telugu/Kannada).
- **Closing quote:** "Use fast ~15B models for natural conversation. Use deterministic code for safety. Use PRISM to prove it." (tag: The Final Verdict) — this is the deck's actual last line; it names PRISM last, per the design intent in `Slides-Plan.md` §2.5.

---

## Known issues — fix before the deck goes in front of judges

These are real, found during a full read-through this session. None involve the Slide 4 benchmark table (that one's clean, sourced, verified) — they're all elsewhere in the copy:

1. **"~15B" model size is stale**, appearing on Slides 1, 2, 3, 5. The project's actual model history is 9B (`Holo-3.1-9B`, failed the clean-control bar) → stepping up to a 35B-class model (`Holo-3.5-35B` / `Qwen-3.8-27B` / `Gemma-4-26B` / `Ornith-1.5-35B`, decision locked in `docs/Overall-plan.md` §10). "~15B" was never the real number at any point. Fix once Phase 2 (`docs/REMAINING_STEPS_PLAN.md`) lands on a specific model — replace every "~15B" with the real, final model name/size, and say the size jump honestly per §10's note.
2. **Slide 5's "SUITE: 48/48 Passing" contradicts Slide 4's "60 Locked Calls."** The real number is 60 (`evals/replay_set.json`, `docs/Overall-plan.md` §12). "48" doesn't trace to anything real — it's the same number that appeared in the now-deprecated `build_pitch.py`'s stale, independently-fabricated snapshot. Fix: change to "60/60 Passing" (v2) or drop the specific count if v0/v1 are in the same footer's implied scope (v0/v1 don't pass 60/60 — only v2 does).
3. **The "5-second" airlock/latch timing** (Slides 3 and 5) is a specific, dramatized wall-clock number. The real Commit Window (`app/enforcement/commit_window.py`, called from `app/agent/runner.py`) resolves on a turn basis (`min_turn_age=1`, i.e. "the next utterance"), not a literal 5.0-second timer. Either implement an actual timed grace window and cite the real value, or rephrase to describe the real turn-based mechanism instead of a specific unmeasured second count.
4. **Slide 6's non-insurance sectors** (Banking, Telecom, Healthcare) are phrased as present-tense capabilities ("blocks," "enforces," "shields") rather than clearly marked future scope. Per `docs/Overall-plan.md` §17's honesty rules and `Slides-Plan.md`'s original design intent, these should read as explicitly not-yet-built extensions of the same failure class, not things the system currently does.

None of these were touched this session beyond the two direct fabricated-number fixes noted inline above (the Slide 3 veto latency, the Slide 5 closing quote) — the rest needs an explicit content-editing pass, which wasn't in scope for a documentation/cleanup pass and touches presentation copy the user has asked not to be modified without a specific go-ahead.
