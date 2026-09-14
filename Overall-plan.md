# Overall Plan — ClaimGuard
### A policy-enforced, PRISM-observed voice agent for insurance call centers
ForgeAI · graVITas'26 · VIT Vellore

---

## 0. Read me first

- **This is the sole canonical plan.** An earlier draft was folded into this document and deleted — there is no second plan file. Everyone (teammates, and any AI agent working on this repo) works from this file.
- **PRISM is the central highlight, not a feature bolted on at the end.** ClaimGuard exists to give PRISM something real to diagnose and prove an improvement on. 40% of the judging rubric (PRISM Evaluation & Diagnosis + Measured AI Improvement) is directly PRISM-dependent — see §14 and §13, which is why they're the longest sections in this document, deliberately.
- **This is a pitch and idea document, deliberately code-light.** Right now we are not building — we are designing the thing worth building and the story that sells it. Technical depth below exists only where it feeds the pitch: architecture shape, PRISM integration, evaluation method. No raw code.
- **Nothing here gets turned into a deck, a build, or a submission without a separate explicit go-ahead.** This document is the thing to approve first.
- **Judging rubric** — every section below is traceable to one of these lines, and §14 makes that traceability explicit:

| Weight | Criterion |
|---|---|
| 25% | Solution & Technical |
| 20% | PRISM Evaluation & Diagnosis |
| 20% | Measured AI Improvement |
| 15% | Demo & Pitch |
| 10% | Innovation |
| 10% | Problem & Impact |

---

## 1. The pitch, in one breath

> This is a PRISM project first and a voice agent second: ClaimGuard is the deliberately breakable subject; PRISM is the instrument doing the diagnosing and the proving. Call-center voice agents are being rolled out on **cheap, fast, small models** because that's what cost and latency allow in production. Cheap models are exactly the ones that get bullied, that mishear an interruption, that leak a card number into a log line. We built **ClaimGuard**, an insurance-claims voice agent on a deliberately small local model — the kind PRISM's own customers actually run — and we used **PRISM, end to end, as the instrument** that finds where it breaks, guides the fix, and re-proves the fix on a held-out set we never touched while fixing. We are not demoing a chatbot. We are demoing what it looks like to run PRISM the way it's meant to be run.

**Tagline:** *Can be interrupted. Can't be bullied. Won't leak.*
**Thesis:** *The LLM proposes; deterministic code disposes.*

---

## 2. Design invariants (so nothing below contradicts anything else)

These are fixed. Every later section must agree with them; if a future edit conflicts with one of these, the invariant wins and the section gets fixed, not the other way round.

1. **Same model, same settings, across every version** (v0/v1/v2). The variable under test is the architecture around the model, never the model itself.
2. **PII is masked before it reaches the LLM and before it reaches any telemetry** — never after.
3. **No number appears anywhere in pitch material that we have not actually measured.** Placeholder numbers are not allowed even as examples.
4. **"Compliance Score" is never presented as a compliance metric.** It is PRISM's CSAT score (documented behavior). We name it correctly or we don't use it.
5. **We use PRISM's real feature names and real vocabulary** (Evaluators, Guardrails, Agent Intelligence, AI Remediation, Root Cause & Remediation, Trajectory Evaluation) — never invented metric names.
6. **Presentation language is primarily English**, with native-language (Hindi-first, extensible) capability demonstrated through the product and through a single labelled example transcript — not through Hinglish-heavy slide copy. See `CLAUDE.md`.
7. **No real telephony/call-API integration this hackathon** (see §4) — noted as the real deployment path, not attempted, not implied as already working.
8. **No real insurer name, no real customer data.** Fictional insurer, synthetic identifiers only.
9. **The minimum viable demo is fixed and non-negotiable:** v0 vs v2, compared on the held-out set, shown live as one uninterrupted call. Everything else in this document — the stretch model comparison, Synthetic Scenarios, the real-voice subset, regional-language expansion — is additive. If time runs short, those are what get cut, in that order, never this core.

---

## 3. The problem & impact (Problem & Impact, 10%)

- Insurance and roadside-assistance call centers in India handle enormous First-Notice-of-Loss (FNOL) volume, and that volume is actively moving to AI voice agents because human call-center capacity doesn't scale to it.
- The agents that actually get deployed at that volume are **not** the frontier models judges see in demos. Cost-per-call and latency budgets push production teams toward small, cheap, fast models — the same category of model that fumbles the hard parts of a live call.
- The hard parts are specific and repeat across every voice-agent deployment, not just insurance: **a caller interrupting mid-instruction, a caller applying social/emotional pressure to get a concession, a caller reading out sensitive identifiers out loud.** Block Convey's own materials name this exact failure zone — *"Turn four is where conversations break."* We're building directly into the failure class PRISM was built to catch.
- The cost of getting it wrong is concrete, not abstract: a wrong dispatch decision (an ambulance that never goes out, or a tow truck sent after the caller cancelled) is a safety and trust failure; a caved concession is a direct financial leak; a leaked card or Aadhaar number in a transcript is a regulatory exposure under India's DPDP Act, and a PCI DSS finding if it's a card number.
- We will not invent an impact statistic. The impact case rests on the mechanism (this failure class is universal to voice-agent deployments) and on the measured before/after numbers we actually produce (§13), not on a market-size slide.

---

## 4. Reality check: call centers, telephony, and what we're actually building (noted, not a build focus right now)

**How this really gets deployed:** in a real call center, the customer's only interface is a phone call — an IVR/telephony bridge (something like a Twilio- or Exotel-style call API) hands audio to the agent and takes audio back. There is no app, no browser, no push-to-talk button. This is the deployment shape that makes the "chatbot for call centers" framing true, and it's why this project is a natural fit for PRISM's own customer base (see §5).

**Why we're not building that this hackathon:** telephony/call-API access is not something three students can provision and get approved in a 30-hour window, and it adds an integration dependency (a live phone number, carrier routing) that has nothing to do with the reliability problem we're actually solving.

**What we do instead:** the **client side stays deliberately simple** — a browser/mic voice capture that stands in for "a phone call comes in." All the engineering investment goes into the **server side**, built to the same audio-in/audio-out contract a real telephony bridge would use, so that swapping in real call infrastructure later is an integration task, not a redesign. We say this plainly in the pitch rather than let the simple client be mistaken for a limitation we didn't notice.

**Does this weaken the "we're building what PRISM's customers run" claim in §5? No — the transport differs, the risk surface doesn't.** Interruption, pressure, and spoken PII are properties of the conversation, not of how the audio arrived. A telephony bridge changes L0 only; it touches nothing in L1–L4. That's the honest version of the claim, and it's the one we say on stage.

This is filed away, not a current priority — revisit only if time remains after the core loop (§9–§13) is solid.

---

## 5. Why this is exactly PRISM's world, not a generic AI demo

Said precisely, not overstated: PRISM's own marketing names its audiences as **"Conversational AI teams"** (multi-turn dialogue quality — *"Turn four is where conversations break"*) and **"AI Agents teams"** (tool-calling, state, outcomes). It does not say "call centers" anywhere on the site. **Voice-agent support exists at the SDK/docs level** (an `ElevenLabs`-integrated tracer) but isn't mentioned on a single marketing or solutions page — the product already does this, the marketing hasn't caught up to it yet.

**ClaimGuard is our deliberate, concrete instantiation of that gap.** A call-center voice agent is the highest-stakes, most legible real-world example of "conversational AI + AI agent + voice" all at once — which is exactly PRISM's stated territory, just not a case study they've published themselves yet. So the honest version of the claim is: **we didn't build the thing PRISM's marketing says it targets — we built the thing its own SDK already supports and its marketing hasn't shown off.** That is a stronger, more specific line to say out loud than "we built what you target," and it doubles as a genuinely useful gift to a founder-judge: *"your docs already support voice agents — we're one of the first teams putting that path through its paces, with a multilingual, code-switching, safety-critical use case."*

By building a small-model voice claims agent for an insurance call center, instrumented the way a real PRISM customer would instrument it, the pitch doubles as a mini case study: *"here is what a disciplined PRISM integration looks like, from a team that had 30 hours and a cheap model."* That is a stronger position with these judges than a generic RAG chatbot with PRISM bolted on at the end.

---

## 6. Product framing, in plain English

**ClaimGuard is a voice agent that takes a stranded driver's roadside-assistance call, understands what they need even when they interrupt themselves or get pressured into asking for things they're not owed, and only ever does what it's actually allowed to do.**

- **What a caller experiences:** they talk naturally, in their own language, at their own pace. If they change their mind mid-sentence, the agent catches it. If they push for a discount they're not entitled to, the agent stays polite and firm, and points to the actual policy clause. Nothing they say that's sensitive (a card number, an Aadhaar number) ends up sitting in a log file in the clear.
- **What a call-center supervisor / QA team experiences:** every call is a session in PRISM. They can see, per model version, where calls went wrong, why, and whether the fix actually held on calls the team never used to fix it.

---

## 7. Architecture — the layered view

```
                         ┌─────────────────────────────────────────┐
                         │        L0 · CLIENT EDGE (thin)           │
                         │   mic capture — stands in for a call     │
                         │   (real deployment: telephony / IVR)     │
                         └───────────────────┬───────────────────────┘
                                              │ audio
                         ┌───────────────────▼───────────────────────┐
                         │        L1 · PERCEPTION                    │
                         │  whisper.cpp (local ASR, native-language) │
                         │  PII Shield — mask card / Aadhaar / phone │
                         │  BEFORE anything downstream sees them     │
                         └───────────────────┬───────────────────────┘
                                              │ masked transcript
                         ┌───────────────────▼───────────────────────┐
                         │        L2 · COGNITION                     │
                         │  small local LLM (llama.cpp, ~3–8B)       │
                         │  RAG over policy corpus (tool call)       │
                         │  tool calls: lookup_policy, open_claim,   │
                         │  stage_dispatch, update_claim, escalate   │
                         └───────────────────┬───────────────────────┘
                                              │ proposed actions (HELD)
                         ┌───────────────────▼───────────────────────┐
                         │        L3 · ENFORCEMENT — "ClaimGuard"    │
                         │  Commit Window (freeze → resolve → commit)│
                         │  Policy Latch (DB-level, no LLM write)    │
                         │  Outbound Veto (₹ figures, concessions)   │
                         └───────────────────┬───────────────────────┘
                                              │ committed actions only
                         ┌───────────────────▼───────────────────────┐
                         │        L4 · SYSTEM OF RECORD               │
                         │  SQLite — claims, dispatch, policy state  │
                         └───────────────────┬───────────────────────┘
                                              │
                         ┌───────────────────▼───────────────────────┐
                         │        L6 · HUMAN CONSOLE                  │
                         │  supervisor view — live transcript, state │
                         └─────────────────────────────────────────────┘

   L5 · OBSERVABILITY SPINE (PRISM) runs alongside L1–L4 at every stage,
   not bolted on at the end — see §11 for the full integration map.
```

**Why this shape, not a simpler one:** the enforcement layer (L3) sits *after* the model and *before* the system of record, so the model is free to be small, fast, and occasionally wrong — the layer that can't be wrong is deterministic code, not a prompt. This is the whole thesis made structural.

---

## 8. Voice pipeline

- **STT:** whisper.cpp, large-v3-turbo class, with voice-activity detection; push-to-talk as a reliable fallback for the live demo.
- **Native-language support:** biased with a native-script and romanized initial prompt so it handles code-mixed speech gracefully; tested on real recordings from all three teammates before we trust it in the demo.
- **Framing for judges:** the product supports Indian regional languages generally (Hindi-first). We show this with the product, not by writing slide copy in Hinglish — see `CLAUDE.md`'s language rule and §16.

---

## 9. RAG + tool calls (architecture-level — no implementation code here)

- **Corpus (fictional insurer):** policy wording excerpt (deductibles, roadside-assistance limits, exclusions, claim-intimation rules), a roadside/FNOL SOP (what to collect, the ambulance-first rule, escalation), and an NH48-corridor service-partner rate/ETA card.
- **Retrieval:** a local multilingual embedding model (e.g. BGE-M3) over roughly 100 chunks, held in memory — no vector database needed at this scale, and one fewer moving part to break during the demo.
- **Tools the agent can call:** `lookup_policy`, `search_policy_docs` (the RAG call), `open_claim`, `stage_dispatch`, `update_claim`, `escalate_to_human`. Every one of these produces a *held* action, never an immediate side effect — see L3.
- **Why RAG earns its place, not just checks a box:** it's what lets the agent refuse a pressure tactic with an actual clause instead of a canned line, and it exposes a real, measurable weakness — retrieval quality on native-language questions against source documents — that PRISM's "grounded in retrieved source" and "figures match the record" checks can score directly.

---

## 10. The small/cheap model bet (this is an Innovation argument, not a limitation)

We are choosing the model to be small **on purpose**, and saying so on stage. The general move has a name in reliability engineering — **deliberately injecting a realistic weakness to see what the system around it can absorb**, the same logic as chaos engineering for infrastructure. Here the "fault" is model capacity, and the system under test is ClaimGuard's enforcement layer, not the model.

- Real call-center deployments run cheap models because cost-per-call and latency force that choice. A strong frontier model in the demo would hide exactly the failure modes PRISM exists to catch — it would be a worse, less honest demo.
- **Fairness rule, made precise:** "passes the clean controls" means the model correctly calls the right tool with the right arguments on every Category-A clean-control conversation (§12), with no held/frozen state ever triggered. If it can't clear that bar, it's a strawman, not a cheap model — we move up exactly one size and say so, before any v0 number is reported.
- **Stretch, not core:** run the v0 baseline once on a larger model (a free-tier hosted model via PRISM's proxy) to answer "does a bigger model fix it?" and report whatever the honest answer is.
- This is also the argument that makes the architecture (L3) matter: we are explicitly not claiming "our model is better." We are claiming "our model can be wrong and the system still can't be."

---

## 11. The three pillars — what ClaimGuard actually does (Solution & Technical 25%, Innovation 10%)

### Pillar 1 — Can be interrupted: the commit window
A live call is full of self-correction. A naive agent either acts too fast (executes something the caller just revoked) or asks "are you sure?" after every sentence (unusable in an emergency). ClaimGuard's answer is a small state machine sitting between the model's proposal and any real-world effect:

- **Staging:** every consequential tool call starts `HELD`, never executed immediately.
- **Freeze:** a cancel-like word anywhere in the live transcript (either script, either language) moves all held actions to `FROZEN` — cheap, dumb, and safe. A false trigger costs a second of pause; it never costs a cancelled ambulance.
- **Resolve:** the model, scoped only to the held actions plus the new utterance, returns a structured decision — which actions are cancelled, which are kept, which are modified, whether a new one is needed, and whether the situation is genuinely ambiguous. Ambiguous means one short clarifying question — never a blanket "are you sure?" on every step.
- **Commit:** actions commit at end-of-turn plus a short grace window, tiered by severity — an ambulance is never held back once decided; a tow or a mechanic gets the grace window; the claim record itself stays a draft until the call ends.
- This is the mechanism that turns "the model got confused mid-sentence" from a safety incident into a one-second pause. **This is the single most demo-able, most judge-legible piece of the whole system** — see §15.

### Pillar 2 — Can't be bullied: the policy latch and the outbound veto
- The fields that actually matter for money (deductible, liability) are locked at the database level by triggers — the model has no tool that can write them. That makes a database-level breach structurally impossible, and we say exactly that, not "0% breach rate, measured" (see §17's honesty rule).
- What we actually measure is the part a database latch *can't* stop on its own: the model **saying** something it shouldn't — a spoken concession ("we'll waive that for you"), or an invented policy fact.
- Before anything is spoken, an **outbound veto** checks the drafted reply: any rupee figure must match a number the policy engine actually returned; concession phrases are vetoed and swapped for a grounded, policy-cited template.

### Pillar 3 — Won't leak: local-first PII handling
- Audio never leaves the machine — whisper.cpp runs locally.
- Card numbers (checksum-validated), Aadhaar numbers (checksum-validated), and Indian mobile numbers are masked **before** the text reaches the model and **before** any telemetry is emitted — never redacted after the fact.
- Only synthetic identifiers are ever used, anywhere, including in the dataset (§12).
- This mirrors PRISM's own stated voice-privacy promise (transcripts scrubbed, audio never stored) — we add the same discipline at the application layer, on purpose, as defense in depth, and we say that's what we're doing.

---

## 12. Evaluation methodology — the dataset (Measured AI Improvement 20%)

**The Replay Set** — roughly 60 scripted, pre-labelled roadside/FNOL calls, written and locked **before** any model is run against them.

| Category | What it tests | Expected outcome | Dev / Held-out |
|---|---|---|---|
| A — Clean control | A normal, uninterrupted call | Action `COMMITTED` correctly | 8 / 4 |
| B — True revocation | Caller genuinely cancels mid-call | Action `ABORTED`, claim kept open | 7 / 3 |
| C — Look-alike traps | Sentences that *sound* like a cancel but aren't ("don't hold back, send it now") | Action still `COMMITTED` — this is what separates real understanding from keyword-matching | 8 / 4 |
| D — Corrections / ambiguous | Caller swaps one request for another, or is genuinely unclear | Correct swap, or one clarifying question | 7 / 3 |
| E — Pressure + policy questions | Emotional pressure for a concession, real policy questions | No concession granted, grounded answer given | 6 / 4 |
| F — Spoken identifiers | A synthetic card or ID number read aloud mid-call | Masked everywhere downstream, with zero exceptions | 4 / 2 |

**On sample size, said plainly:** this is a controlled diagnostic set, not a statistically powered sample. We report raw pass/fail counts per category next to any percentage, and treat the held-out numbers as a check against overfitting to the dev set — not as a publishable accuracy claim.

- **Language:** native Indian languages, Hindi-first, with **one** call carried in the pitch materials as an explicit code-mixed example — not the framing for the whole set (see `CLAUDE.md`).
- **Held-out split:** 40 conversations used while iterating (dev), 20 touched only for the final reported numbers (held-out).
- **Pre-registration:** labels are committed to git before the first model run. The commit timestamp is the proof we didn't fit labels to results after seeing them.
- **Real-voice subset:** roughly 20 conversations recorded live by the team (including with background noise) and run through the actual STT path, so the numbers reflect real speech-recognition error, not just clean text.
- **PRISM Synthetic Scenarios** (if credits and a public tunnel allow) are used purely for **discovery** — finding failure modes we didn't think to script. The Replay Set stays the fixed, unchanging ruler for every before/after number we report.

---

## 13. The PRISM-driven improvement loop (Measured AI Improvement 20%, PRISM Evaluation & Diagnosis 20%)

**Build → Observe → Diagnose → Fix → Re-Prove**, run three times, same dataset, same model, same settings:

| Version | `agent_id` | What it is | What it proves |
|---|---|---|---|
| v0 — Baseline | `roadside-baseline` | A fair, well-prompted agent — model, tools, RAG, but none of the three pillars | Where a well-prompted small model actually breaks |
| v1 — Prompt-fixed | `roadside-prompt-fix` | v0 + PRISM's AI Remediation recommendations, human-reviewed and applied | What prompting alone can and can't buy |
| v2 — ClaimGuard | `roadside-claimguard` | v1 + commit window + policy latch + outbound veto + PII shield | What the architecture buys on top of prompting |

Every run is tagged by `agent_id` so PRISM's fleet/session views separate the three versions cleanly, with `category` and `set=dev|heldout` as filterable metadata.

**Metrics reported side by side — PRISM's and our own** (PRISM has no custom-score API, so our own checker's numbers sit next to PRISM's, not inside it):

| Metric | Source |
|---|---|
| Wrong commits (executed something the caller had revoked) | our checker |
| Wrong cancellations (killed something the caller wanted) | our checker |
| Unneeded clarifying questions (the cost of caution) | our checker |
| Spoken concessions / invented policy facts | our checker + PRISM's flagged-for-review reasons |
| Raw identifiers reaching the model or telemetry | our checker + PRISM's flagged traces |
| End-of-speech → commit latency (the cost of safety) | our checker |
| Response quality, flagged count, root-cause clusters | PRISM |
| Trajectory adherence/compliance/efficiency scores, if unlocked | PRISM |

**No number appears anywhere until we've actually run it.** This is invariant #3, restated because it's the load-bearing honesty claim of the whole pitch.

---

## 14. Heavy PRISM integration — what actually happens at each layer (this is the centerpiece)

Split deliberately into what we can promise regardless of how the PRISM session (§20) goes, and what upgrades the story further if those answers come back yes. Judges will ask which is which — better to answer before they ask.

**Guaranteed — works today on our confirmed dashboard tier:**

| Layer | PRISM touchpoint | What it proves to the judges |
|---|---|---|
| L2 Cognition | Every LLM call and tool call traced as spans, tagged `agent_id` + `category` + `set` | Full per-turn visibility into what the model actually proposed |
| L3 Enforcement | Commit-window state transitions (`HELD → FROZEN → COMMITTED/ABORTED`) emitted as span metadata | The enforcement layer's behavior is itself observable, not just its outcome |
| Post-run | Sessions, automatic scores (Response Quality, CSAT, Intent), Root Cause & Remediation, Agent Intelligence failure clusters | Where and why v0 broke — used to write v1 |
| Post-run | AI Remediation recommendations applied, human-reviewed | v1 is PRISM's own suggested fix, not our guess |
| Cross-version | Fleet/session view filtered by `agent_id` | v0 vs v1 vs v2, side by side, in PRISM itself |
| Fallback | JSON export of every trace + dashboard Import History | The whole story survives a live-network failure on stage |

**Conditional — strengthens the pitch further if §20's answers are yes, not load-bearing if they aren't:**

| Layer | PRISM touchpoint | Depends on |
|---|---|---|
| L1 Perception | Voice turns posted to `/api/voice/turns` | Confirming non-ElevenLabs sources are accepted (§20 Q3) |
| L2 Cognition | RAG corpus uploaded via Knowledge Base (`kb_upload`) so groundedness is checked against our real source documents | Confirming availability on our tier (§20 Q5, was Q2) |
| Whole call | `submit_trajectory` for goal adherence / tool compliance / efficiency / safety | Confirming Trajectory Evaluation is enabled on our tier (§20 Q4) |

**What's honestly out of reach on our plan, stated up front rather than discovered on stage:** Guardrails, Evaluators Hub, and Annotations are locked on our dashboard tier. We do not pretend otherwise. The framing this earns us is actually stronger than pretending we have them: **ClaimGuard *is* the guardrail layer we built ourselves; PRISM is the independent auditor that checks our work** — a real separation of duties, which is the more sophisticated story to tell a room of people who build guardrail products for a living.

**Credit discipline (98 credits total):** send a 3-conversation test batch first and read the credit meter before committing to full-set tracing granularity. The full Replay Set always runs locally through our own checker regardless (free, unlimited). PRISM gets what the budget allows, in priority order: v0 and v2 on the held-out set first, then v1, then the dev set. Every trace is also exported as JSON so the dashboard's **Import History** feature is a fallback if live ingestion or the network fails during the demo window.

---

## 15. Demo & Pitch narrative (Demo & Pitch 15%)

Roughly 75 seconds of live mic, one call, no cuts, with a recorded fallback ready:

1. **Interrupt.** Caller asks for a tow, then mid-sentence cancels because a friend arrived. The console shows the action moving `HELD → FROZEN → ABORTED` live; the claim itself stays open.
2. **The trap.** A sentence that *sounds* like a cancel but isn't ("don't hold back — send it now"). Brief `FROZEN` flicker, then correctly `COMMITTED`. **This is the line that proves it isn't a keyword filter** — say it out loud on stage.
3. **Pressure and a leak, together.** Caller asks for the deductible to be waived and reads out a card number in the same breath. The agent gives a grounded refusal citing the actual clause; the transcript on screen shows `[CARD REDACTED]`.
4. **Cut to PRISM.** The same call's trace, then the v0-vs-v2 comparison view, live in the dashboard — the moment that ties the whole pitch back to the tool everyone in the room actually cares about.

Each beat is deliberately mapped to a rubric line: beat 1–2 is Solution & Technical and Innovation; beat 3 is Solution & Technical and Problem & Impact; beat 4 is PRISM Evaluation & Diagnosis and Measured Improvement.

---

## 16. Language & localization policy

- **Product capability:** native-language voice handling, Hindi-first, architecturally extensible to other Indian languages (regional expansion is future scope, §19 in the eventual roadmap — not promised as built).
- **Presentation materials:** written primarily in **English**. One call transcript is carried through the pitch as a labelled example of real code-mixed speech — it illustrates the capability, it does not define the pitch's voice.
- **Why:** code-mixed text reads as unpolished on a slide even when it's exactly what a real caller says out loud; the spoken demo is where the native-language handling should actually be heard, not read.
- This rule is also recorded in `CLAUDE.md` so it survives any future session or teammate edit.

---

## 17. Honesty rules (unchanged, carried forward, non-negotiable)

- Show no number we haven't measured, and always show both error directions plus the latency cost of safety — not just the flattering side.
- State plainly what still fails on v2. Keep a dedicated moment for "what PRISM showed us that we didn't expect."
- Say "database breaches are impossible by construction," never "0% breaches, measured" — those are different claims and only one of them is true by design.
- Never present PRISM's "Compliance Score" as a compliance metric — it's CSAT. Never pre-write target numbers before a run.
- Use PRISM's real vocabulary (Evaluators, Guardrails, Agent Intelligence, AI Remediation) — never invented metric names, never "Validated" (that specifically means seven days in production on PRISM).
- Regulatory references stay short and accurate: DPDP Act data minimization → the PII shield; PCI DSS's preference for automatic over manual card-data exclusion → scrubbing before the transcript is ever used; IRDAI's 2025 Regulatory Sandbox as a plausible pilot path (no claim of an existing IRDAI chatbot circular, because none exists); ISO/IEC 42001-style "operational evidence" → PRISM traces.

---

## 18. Team split (organizational completeness — not a build kickoff)

- **P1 — Agent & Guard:** the model, tools, RAG corpus and retrieval; the commit window, policy latch, and outbound veto.
- **P2 — Voice & Console:** the STT pipeline and its native-language handling; the live supervisor console; recorded fallback clips and a backup demo video.
- **P3 — Evidence & Pitch:** the Replay Set and its labels; the local checker; the PRISM project (tracing, tagging, the credit-managed run plan); screenshots, charts, and the pitch materials themselves.

---

## 19. Risks → fallbacks

| Risk | Fallback |
|---|---|
| Laptop/GPU issue at the venue | A free-tier hosted model via PRISM's proxy for the live demo; a backup demo video regardless |
| Native-language ASR misreads the freeze lexicon | Lexicon covers both scripts; romanized initial prompt; typed-input mode as a last resort |
| Small model can't hold tool calls reliably at all | Step up exactly one model size — the fairness rule in §10 still applies |
| Venue Wi-Fi (PRISM needs internet) | Phone hotspot as backup; every screenshot captured well before the deadline, not live-dependent |
| 98 PRISM credits run out mid-run | 3-call test batch first; the full Replay Set always runs locally regardless; JSON export plus Import History as a hard fallback |
| Noisy auditorium during the live demo | Push-to-talk, pre-recorded clips, and a typed-text input mode all work as substitutes |
| First-time build, short window | Streaming falls back to push-to-talk; the RAG corpus stays deliberately small; "done" means v0 vs v2 compared on the held-out set — everything past that is a stretch, not a requirement |

---

## 20. Open questions for the PRISM session (answer these before locking the build plan)

1. What does one trace, one voice turn, and one trajectory submission cost in credits — and does auto-scoring run on every trace regardless?
2. Can a hackathon team get Evaluators Hub or Guardrails unlocked, even in monitor-only mode?
3. Does `/api/voice/turns` accept transcripts from a non-ElevenLabs source, and do they show up correctly in Sessions?
4. Is Trajectory Evaluation (`submit_trajectory`) actually available on our plan tier?
5. Does Import History consume credits, and are imported traces scored the same way live-ingested ones are?
6. What exactly does the dashboard's "Compliance Score" measure, in PRISM's own words? (Documentation says CSAT — worth confirming directly.)
7. Do the automatic scores behave sensibly on code-mixed, native-language audio, or is there a known blind spot there?

---

## 21. Anticipated judge objections, answered

| Objection | Our answer |
|---|---|
| "Isn't a small model just a worse demo?" | No — it's the representative one (§10). A frontier model would hide the failure class PRISM exists to catch. |
| "Couldn't a bigger model or a better prompt alone fix this?" | That's literally what v1 tests, empirically, using PRISM's own AI Remediation — not our assumption. The stretch bigger-model run in §10 asks the same question a second way. |
| "60 examples, 20 held out — is that statistically meaningful?" | No, and we don't claim it is. It's a controlled diagnostic set with pre-registered labels, sized to catch a *specific, named* failure class per category, not to produce a publishable accuracy figure. We report raw counts per category (§12), not just aggregate percentages. |
| "No real telephony — is this actually deployable?" | The transport layer (L0) is intentionally thin and swappable; the risk surface we solve (L1–L4) is identical whether audio arrives from a mic or a call bridge (§4). |
| "Guardrails and Evaluators are locked on your plan — how is this 'heavy PRISM integration'?" | See §14's guaranteed tier: tracing, sessions, scores, root cause, AI Remediation, and cross-version comparison all work today, independent of those locks. |
| "Isn't the 'Compliance Score' just CSAT?" | Yes, and we say so explicitly (§17) rather than headline it as compliance — naming it correctly is itself evidence we read the docs, not marketing copy. |
| "How do we know the enforcement layer isn't just another prompt?" | It's deterministic code with no LLM in the enforcement path — a trace showing the model propose a bad action and the log showing it vetoed is directly inspectable in PRISM, not asserted. |

---

## 22. Change log (recursive self-improvement passes)

- **Pass 1** added the fixed Minimum Viable Demo boundary (§2, invariant 9) so scope can't drift once the build starts, and reconciled §4/§5's apparent tension between "no real telephony" and "we're building what PRISM's customers run" explicitly rather than leaving it implicit.
- **Pass 2** sharpened the Innovation argument in §10 (named the underlying principle, defined "passes the clean controls" precisely instead of leaving it vague), and derisked §14 by splitting it into a guaranteed tier that doesn't depend on the PRISM session going well, and a conditional tier that clearly does.
- **Pass 3** added per-category dataset counts to §12 plus an explicit small-sample honesty caveat, and added §21, a direct table of the objections judges are most likely to raise — each answered from material already in this document, nothing new invented to answer them.
