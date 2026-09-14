# ClaimGuard — Remaining Tasks & Execution Plan
**Canonical Reference:** `docs/Overall-plan.md` | **Team Brief:** `docs/HANDOVER.md`
**Target:** ForgeAI Hackathon · graVITas'26 · VIT Vellore
**Core Thesis:** *PRISM is the hero, ClaimGuard is the vehicle. The LLM proposes; deterministic code disposes.*
**Ordering principle (per `docs/Overall-plan.md` §0):** presentation is the top strategic lever. Phases below are ordered so the work that produces judge-facing, PRISM-forward evidence happens first — not by rubric-section order.

---

## 1. Status Overview

| Subsystem | Owner | Current State | Remaining Needs |
|---|---|---|---|
| **L0/L6 Console & Edge** | Ojas | Done (`frontend/` + `/console`) | Demo rehearsal, backup screencast |
| **L1 Perception & Security** | Ojas | Done (`pii_shield.py`, transcriber stub) | Real audio clips (.wav), live Whisper STT check |
| **L2 Cognition & RAG** | Ali | Done (`app/agent/`, `app/rag/`) | Live local LLM server test (`use_mock=False`) — real-LLM tool-call path already hardened (safe JSON parsing, claim-id auto-injection) |
| **L3 Enforcement** | Ali | Done (Commit Window, Latch, Veto) | Verified against live model tool output |
| **L4 System of Record** | Ali | Done (`claimguard.db` + triggers) | Verified in end-to-end flow |
| **L5 PRISM Observability** | Pratham | Single canonical tracer (`app/observability/prism_tracer.py`); tagging bug + a double-firing duplicate-tracer bug both found + fixed this session, before any credits spent | 3-call smoke test, 98-credit budget run, screenshots — **now the top-priority remaining item** |
| **Evals & Benchmark** | Pratham | **Fixed this session** — was silently rigged (see Phase 0), now honestly measured | Known harness limit: v1 can't differ from v0 without a real LLM (Phase 2 addresses this) |
| **Presentation & Pitch** | Team | Deck HTML + PDF corrected to match honest numbers (this session); dead deck fragments removed | Add real PRISM screenshots once Phase 1 lands |

---

## 2. Phase 0 — Eval Harness Integrity Fix (COMPLETE, this session, 2026-09-14)

**Why this exists:** before anything else got planned, the eval numbers already on disk and already baked into the pitch deck were audited against `docs/Overall-plan.md`'s own non-negotiable invariant #3 ("no number appears anywhere in pitch material that we have not actually measured"). They failed that audit. This had to be fixed before any further planning made sense, because a fabricated benchmark discovered by a judge — and PRISM's own team is a very plausible judge here — would be far more damaging than any deck-polish issue.

**What was found:**
- `evals/checker.py` hardcoded pass/fail outcomes by `agent_version` string (e.g. forcing `wrong_commit = True` for v0/v1 Category B regardless of what the agent actually did), and `app/agent/runner.py`'s deterministic mock (`_mock_generate`) scripted a *different proposed reply* for v0 vs. v1/v2 on the concession-pressure scenario. Together these made the "measured" v0/v1/v2 comparison circular — it reproduced whatever story was written into the harness, not the architecture's real behavior.
- `presentation/claimguard-pitch.html` (and its offline twin) had a v1 row showing 83.3% accuracy with "0 Conceded / 0 Leaked" — a number that traced directly back to that same rigged harness, not to an honest run.
- The same deck also carried unrelated fabricated/inconsistent copy: an invented quote ("~15B voice agents... fail in 31%...") with no source, an unsourced "10,000 calls" framing, a "12ms Zero-Latency Veto" label that contradicts itself, and a false "0ms added latency" claim.
- `build_pitch.py` at the repo root is a **self-regenerating landmine**: running it silently overwrites both deck HTML files with an entirely different, independently-fabricated version (a mismatched "48-scenario" count, an invented "₹250 CR DPDP Penalty" figure) and rewrites itself to keep doing so on every run.

**What was fixed:**
- `app/agent/runner.py`: the mock's concession-scenario reply is now identical regardless of version (the model's proposal never changes across versions, per invariant #1); a new uniform rule — not scripted per category — makes v0/v1 dispatches commit immediately and irreversibly on any turn a `stage_dispatch` tool call happens, because those versions genuinely have no commit-window gate (`agent_version == "v2"` is the only gate in the code).
- `evals/checker.py`: removed the per-version/per-category hardcoded override block entirely; outcomes now fall out purely from the real `final_dispatch_state` the runner produces. Also extended the "no PII shield" condition from v0-only to v0-and-v1, matching `docs/Overall-plan.md` §13's own architecture table (PII shield is bundled into v2 only).
- Re-ran `python -m evals.checker --version all --split all` and `--split heldout`; all 45 existing tests still pass. Results now live at `evals/results/eval_{v0,v1,v2}_{all,heldout}.json`.
- Corrected the deck's Slide-4 table and callout in both `claimguard-pitch.html` and `claimguard-pitch-offline.html` to the new honest numbers, and replaced the four unrelated fabricated lines with sourced or defensible copy.
- Neutered `build_pitch.py` — it now refuses to run and explains why in its docstring, instead of silently reintroducing every fixed problem.
- Updated `docs/presentation/readme.md` to say clearly which files are current vs. superseded, and that Slide 4's numbers must be re-checked against `evals/results/` if those files ever change.

**What the honest numbers now say (`--split all`, 60 calls):**

| Metric | v0 Baseline | v1 Prompt-Fix | v2 ClaimGuard |
|---|---|---|---|
| Overall accuracy | 66.7% | 66.7% | 100.0% |
| Wrong commits (Cat B) | 10 | 10 | 0 |
| Concession leaks (Cat E) | 5 | 5 | 0 |
| PII leaks (Cat F) | 6 | 6 | 0 |
| Avg decision latency | 7.1 ms | 7.7 ms | 9.9 ms |

**The one new honest finding to know about:** v1 is now *identical* to v0. This isn't a bug — the deterministic mock never reads `V1_PROMPT_FIX_PROMPT` (only a real LLM call would let a prompt matter), so on this harness "prompting alone" has nothing to work with. That's actually a clean, defensible talking point (v2's callout box already says so: architecture beats prompting, measured, not just asserted), but it also means v1 should be presented as a stretch/context slide, not a headline claim, until Phase 2 below gives it a chance to be real. This matches `docs/Overall-plan.md` §2 invariant 9, which already treats v0-vs-v2 as the required core and v1 as additive.

---

## 3. Phase 1 — Live PRISM Cloud Ingestion & Dashboard Evidence (Pratham) — **highest remaining priority**

This is promoted ahead of everything else in this plan: it's 40% of the judging rubric (PRISM Evaluation & Diagnosis + Measured AI Improvement) and it's the concrete, screenshot-able proof that "PRISM is the hero," which is the whole point of the project.

**Update — live tracing landed, and two bugs in it got caught before any credits were spent:** Pratham's PR (`app/prism_tracing.py`, merged from `origin/main`, PR #2) wires real PRISM ingestion into every turn — well-built (fail-open, PII-masked-content-only, single shared client, SDK-with-HTTP-fallback). Reviewing it before Phase 1 actually runs turned up two real bugs, both now fixed (commit `fix(prism): tag traces with per-version agent_id and replay category/set`):
- Every trace was tagged with the *same* hardcoded `agent_id` no matter which architecture version ran the turn — this would have made PRISM's fleet/session view unable to tell v0/v1/v2 apart at all, silently breaking the entire comparison this project exists to demonstrate. Fixed: `agent_id_for_version()` now maps `v0`/`v1`/`v2` → `roadside-baseline`/`roadside-prompt-fix`/`roadside-claimguard`, matching `docs/HANDOVER.md`'s own span contract.
- `category` (A–F) and `set` (dev/heldout) were never threaded through to the tracer, so a live replay-set run wouldn't have been filterable by either in the PRISM dashboard. Fixed: both now flow `evals/checker.py` → `AgentRunner.process_turn` → `_PrismTracer.trace_turn` → the trace metadata.
- Also caught in the same pass: a prior edit to `pyproject.toml` had *replaced* the `python-multipart` dependency with `prismtrace-sdk` instead of adding both — would have broken the `UploadFile`/`Form` audio-upload endpoints (`app/server.py`, `app/dev_server.py`) on a fresh `uv sync`. Restored.

None of this was fabricated data — it was a real plumbing gap in genuinely good work, the kind that only shows up once you check what the dashboard would actually receive.

**Second update — a bigger issue found next: two PRISM tracers were live at once.** Separately, `app/server.py`'s `/api/call/turn` (the actual live-demo endpoint) was wired to an *older* tracer (`app/observability/prism_tracer.py`, a `TurnTracer`) that predates `app/prism_tracing.py` and was never removed. Both were firing on every single live turn — `TurnTracer` posting structured spans to `/api/spans/ingest`, and `AgentRunner.process_turn`'s own internal call (from the previous fix, above) posting a flat trace to `/api/traces`. That's ~2x credit burn on every rehearsal and on demo day itself, plus duplicate, differently-shaped dashboard records for the same conversation — exactly during beat 4 of the demo script, where the PRISM dashboard is on screen. The older tracer turned out to be the better-fitted one anyway (matches the team's own verified research recommendation for a hand-rolled tool-calling agent, already had correct `agent_id`/`category`/`set` support, richer nested spans) — so **`app/observability/prism_tracer.py` is now the sole canonical tracer**, `app/prism_tracing.py` is retired (raises `ImportError` if imported), `AgentRunner.process_turn` no longer traces itself internally, and `evals/checker.py` now builds a `TurnTracer` per replay-set turn the same way `server.py` does. `prismtrace-sdk` was also dropped from `pyproject.toml` since nothing uses it anymore. All 50 tests still pass; see `CLAUDE.md`'s "PRISM tracing" section for the current usage pattern before touching this again.

- [ ] Verify `PRISMTRACE_API_KEY` / `PRISMTRACE_PROJECT_ID` / `PRISMTRACE_HOST` are set (see `.env.example`, `app/config.py`).
- [ ] Run a 3-call smoke test against the live endpoint; check the credit meter against the 98-credit budget before committing to full-set ingestion.
- [ ] Ingest the 20 held-out calls for `v0` (`roadside-baseline`) and `v2` (`roadside-claimguard`) first — priority order per `docs/Overall-plan.md` §14 — then `v1` (`roadside-prompt-fix`) only if credits allow. Given v1 == v0 on the current mock harness (Phase 0 finding), spending credits on a v1 run that will visibly show "identical to baseline" is a legitimate but weaker use of the budget than doubling down on v0/v2 — hold off on v1 ingestion until Phase 2 (below) makes it a real prompt-driven run, unless credits are abundant.
- [x] Confirmed each span is tagged `agent_id` / `category` / `set` correctly (fixed this pass — see above); Commit Window transitions (`HELD → FROZEN/COMMITTED → ABORTED`) already show up in span metadata via `transitions`.
- [ ] Export all traces to JSON (Import History fallback — see `docs/Overall-plan.md` §19 risk table for the Wi-Fi-fails-mid-demo case).
- [ ] Capture screenshots: span trace tree, Agent Intelligence failure clusters (v0 vs v2), CSAT/response-quality comparison. Save under `assets/prism/`.
- [ ] Drop the real screenshots into Slide 4 of `claimguard-pitch.html`/`-offline.html` alongside (or in place of) the SVG diagram, then **re-export `claimguard-pitch.pdf`** — it's currently stale relative to the Phase 0 HTML fixes.

---

## 4. Phase 2 — Real Local LLM Validation (Ali) — makes v1 real, strengthens v0/v2 further

Not blocking (the MVD boundary in `docs/Overall-plan.md` §2 invariant 9 is satisfied by the honest mock-based v0-vs-v2 result already), but the highest-leverage way to make the story stronger before Phase 1's traces go up. **This phase is already underway** — a local `llama-server` was serving `Holo-3.1-9B` at `127.0.0.1:8080`, `USE_MOCK_LLM` is unset (defaults false), and `app/agent/tools.py` already picked up robustness fixes for alternate real-model argument key names (`location`/`service` as well as `pickup_location`/`service_type`). The 9B model failed the clean-control bar (below), so the decision has since moved to a 35B-class swap — see the locked decision below.

- [x] **Diagnosed gap:** ran a read-only two-turn diagnostic against the live model in `agent_version="v2"` for the Category B revocation scenario (`AgentRunner(use_mock=False).process_turn(...)`, no code changed). Turn 1 ("I need a tow truck, my car broke down on NH48 near Manesar.") never produced a tool call at all — the model responded conversationally, asking about passenger safety and policy info first, with **zero tool calls**. That means nothing was ever staged into the Commit Window, so turn 2's revocation had nothing to freeze or abort. This is a tool-calling *elicitation* problem with the model, not a bug in the enforcement layer — `app/enforcement/commit_window.py` and `outbound_veto.py` were not implicated.
- [x] **Decision locked (2026-09-14):** this is exactly the scenario `docs/Overall-plan.md` §10's fairness rule anticipated, and the 9B model failed it outright — a strawman, not a fair cheap-model baseline. Per the rule, the model steps up. Confirmed via a separate planning session (see `docs/nemotron_ultra_findings.md` for the discussion; the decision itself is now recorded in `docs/Overall-plan.md` §10/§19/§20 as canonical, not just in that transcript): **step up to a 35B-class model** — candidates `Holo-3.5-35B`, `Qwen-3.8-27B`, `Gemma-4-26B`, `Ornith-1.5-35B`. Also confirmed: the project is on **PRISM's Free tier**.
- [x] **Ali, next action (COMPLETED):** brought up `Holo-3.1-35B-A3B.i1-IQ4_XS.gguf` on local `llama-server` (`127.0.0.1:8080`). Validated it clears Category A cleanly (staged `open_claim` and `stage_dispatch` into `HELD` in <6s) and cleanly executes Category B revocation (transitions `HELD -> FROZEN -> ABORTED`).
- [x] **Multi-round tool chaining & robust parsing:** Added multi-round execution loop (up to 4 rounds) with safe JSON & XML parsing (`_extract_text_tool_calls`), claim ID auto-injection, and fallback handling in `app/agent/runner.py`.
- [x] **PRISM benchmark tooling & held-out ingestion:** Created `scripts/prism_benchmark.py` (`--smoke`, `--heldout`, `--export`, `--status`). Verified 3-call smoke test, completed 20 held-out calls for v0/v1/v2, and exported 181 trace sessions to `data/prism_traces_export.json` for Import History fallback.
- [x] **PRISM reverse proxy & cloud reachability tooling ready:** since PRISM runs in the cloud and cannot reach `localhost:8080`, created `scripts/expose_local_model.sh` and added `--expose` flag to `scripts/run_local_model.sh`. Uses Cloudflare Tunnel (`cloudflared`, no sign-up, no HTML interstitial warning screen) to expose local `llama-server` at `https://<tunnel>.trycloudflare.com/v1`.
- [x] All 50 tests pass offline in `tests/test_server.py`, `tests/test_agent_runner.py`, etc.

---

## 5. Phase 3 — Real Voice Audio & STT Validation (Ojas)

- [ ] Fix `assets/audio/manifest.json` — its `filepath` fields are still absolute Windows paths (`C:\Curiosity\Hackathon\...`) from wherever it was generated; convert to relative paths so the pipeline works on any teammate's machine.
- [ ] Record ~20 real-voice clips across categories A–F, with ambient highway/room noise, per `docs/Overall-plan.md` §12's real-voice-subset plan.
- [ ] Run clips through `app/voice/transcriber.py`; confirm prompt-biasing captures code-mixed Hindi ("bhejo", "deductible maaf", "rehne do") and spoken digits, and that `app/security/pii_shield.py` still redacts correctly on noisier, real transcripts (not just the clean synthetic ones the checker uses).

---

## 6. Phase 4 — Golden Demo Rehearsal & Backup Video (whole team)

- [ ] Rehearse the 4-beat live demo (`docs/Overall-plan.md` §15), now against the honestly-fixed console/enforcement behavior.
- [ ] Record a clean 75-second backup screencast (`assets/demo/claimguard_golden_demo_backup.mp4`) in case the live demo fails on stage.
- [ ] Verify `scripts/start_server.sh` boots `/console` cleanly with zero warnings; confirm a phone-hotspot fallback is ready for venue Wi-Fi.

---

## 7. Deck & doc hygiene (small, do before anyone else opens the deck)

- [x] Corrected the five fabricated/inconsistent numbers in `claimguard-pitch.html` and `claimguard-pitch-offline.html` (this session).
- [x] Neutered `build_pitch.py` so it can't silently reintroduce them.
- [x] Clarified `docs/presentation/readme.md` on which files are current.
- [x] Re-exported `claimguard-pitch.pdf` from the corrected HTML via headless Chromium (6 pages, ~1.1MB) — no longer stale.
- [x] Removed `claimguard-pitch.archive` and `ignore.ignore` — confirmed via repo-wide grep that nothing referenced either file; both were dead fragments of the old `build_pitch.py` output, sitting at the repo root outside `presentation/` where they were easy to open by mistake.
- [x] Verified `evals/replay_set.json`'s per-category dev/held-out counts exactly match `docs/Overall-plan.md` §12's table (8/4, 7/3, 8/4, 7/3, 6/4, 4/2 = 40/20) — no drift found here.
- [ ] After Phase 1 lands real screenshots, revisit Slide 4 so it isn't still SVG-only where a real screenshot would land better.

---

## 8. Team Ownership Matrix

| Task Area | Primary Owner | Secondary / Support |
|---|---|---|
| PRISM Ingestion & Dashboard Evidence (Phase 1) | **Pratham** | Ali |
| Local LLM Runner & Server Stability (Phase 2) | **Ali** | Pratham |
| Voice Clips, STT & Demo Screencast (Phase 3) | **Ojas** | Pratham |
| Live Pitch Rehearsal & Timing (Phase 4) | **All Three** | — |
| Eval harness integrity (Phase 0) | Fixed by this session's agent | Pratham to review the diff in `evals/checker.py` / `app/agent/runner.py` |
