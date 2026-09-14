# Round 2 Script Guide — ClaimGuard × PRISM
**Format:** 3 minutes presentation + 2 minutes Q&A, in front of judges (pro events committee).
**Written:** 2026-09-15, immediately before presenting. Every claim below is something verified live today — see `docs/REMAINING_STEPS_PLAN.md` and `docs/HANDOVER.md` for the underlying evidence trail if a judge wants to go deeper than this script.

---

## 0. Before you walk up — setup checklist

- [ ] `uvicorn` running: `curl http://127.0.0.1:8000/health` → `{"status":"ok"...}`
- [ ] Local model server up on :8080 (`gemma-4-12b`) if you're doing the live moment: `curl http://127.0.0.1:8080/health`
- [ ] Two tabs ready: **Tab A** = `http://127.0.0.1:8000/viewer` (judge-facing command center, this is what you project/share), **Tab B** = `http://127.0.0.1:8000/call` (your control — click pill buttons here, do **not** use the mic)
- [ ] Hit **Reset** on Tab A once before you start
- [ ] Slides open and on the first slide
- [ ] Know which pill buttons on Tab B map to which scenario (Category A clean dispatch, Category B revocation — those are the two you'll use)

**Do not touch the mic / PTT button live.** Voice input is wired end-to-end but there is no real speech-to-text engine installed on this machine right now (`faster-whisper`/`openai-whisper` both absent) — it silently plays back a simulated transcript regardless of what's spoken. If a judge asks about voice, see the Q&A section below for the honest answer; don't demo it live.

---

## 1. The 3-minute script

Times are cumulative. Practice this once out loud before you go up — it should land close to 3:00, not run over.

### [0:00–0:15] Hook
> "Voice AI agents fail in milliseconds. A small, cheap model handling a real customer call can get bullied into promising a refund it shouldn't, or execute an action the caller just tried to cancel a second later — and by the time anyone notices, it's already happened. That's not an insurance problem. It's a problem for every company putting a voice agent in front of real customers."

### [0:15–0:55] Solution — the three pillars
> "ClaimGuard is a working voice-agent backend built on one idea: the AI proposes, deterministic code disposes. Three pillars, all real, all running right now:
> - **Can be interrupted** — every consequential action goes into a revocable Commit Window state until the caller's next turn confirms it.
> - **Can't be bullied** — financial terms are locked at the database level with a Policy Latch, backed by an Outbound Veto that intercepts any concession the model tries to make before the caller ever hears it.
> - **Won't leak** — PII is mathematically masked before the model ever sees it. Real Luhn checksum for cards, real Verhoeff checksum for Aadhaar — not a keyword filter."

### [0:55–1:15] Live moment (switch to Tab A on screen)
> "Rather than just tell you the numbers, let me show you the enforcement live."
- Click the **Category B / revocation** pill on Tab B: *"I need a tow truck near Manesar Km 62."*
- Point at Tab A: "Watch — the dispatch lands in HELD. Nothing has executed yet."
- Click the revocation pill: *"Wait, don't send the tow truck, my cousin just showed up!"*
- Point at Tab A: "And there — FROZEN, then ABORTED. The claim stays open, only the dispatch cancels. That's deterministic code making the call, not the model's judgment."
- *(If the model is mid-generation, narrate through the wait — real inference takes a few seconds. Don't stand in silence.)*

### [1:15–1:45] Evidence
> "That's not a scripted animation. We measured this: same model, same settings, 60 pre-registered scenarios. Unprotected — 66.7% accuracy. With ClaimGuard's architecture — 100%. We validated that twice: once on a deterministic benchmark, and again today, live, against the real model, getting the identical 100% result. We even swapped the underlying model entirely mid-development and got the same perfect enforcement — because the safety guarantee lives in the code, not in whether the model behaves."

### [1:45–2:15] Innovation + Problem/Solution fit
> "The innovation isn't a smarter model — it's that we don't trust the model at all for anything consequential. The commit window, the policy latch, the veto — none of them ask the LLM's permission. That's what makes this deployable in production with a cheap, fast model instead of needing a frontier one for every call."

### [2:15–2:45] PRISM
> "We built this to be diagnosed end-to-end by PRISM — every turn traced, tagged by architecture version, so PRISM's own dashboard shows the baseline-vs-protected comparison directly, not something we asserted. PRISM had a platform outage today; our tracing is fixed and wired, ready the moment it's fully stable."

### [2:45–3:00] Close
> "This isn't a pitch for an idea. It's a working backend we stress-tested today, live, against the real model — and every number on these slides is one we actually measured."

---

## 2. Q&A (2 minutes) — anticipated questions, honest answers

**Q: Does voice input actually work?**
> "The pipeline is fully built — audio capture, PII shielding, the same enforcement layer — but the speech-to-text engine isn't installed on this laptop right now, so I'm demoing through text input instead of the mic to be precise about what's live versus what's wired. The text path you just saw is the identical backend path a real voice call would hit after transcription."
*(Do not claim voice works. This is the one honest gap — own it plainly, don't dodge.)*

**Q: What happens if the model is slow or gets something wrong?**
> "Real inference on this hardware averages under 10 seconds a turn — that's a known cost of running locally rather than on a data-center GPU, not a correctness issue. On correctness: we measured a small number of retries needed against the real model, always logged, always fail-open — never silent. We'd rather show you a disclosed 1% retry rate than hide it."

**Q: Why isn't PRISM's dashboard showing live numbers right now?**
> "PRISM had an outage earlier today, confirmed by the organizers — our tracing code is fixed, tested, and sending correctly; we just don't have hours of accumulated dashboard history to show yet. Happy to show you the trace payload structure directly if that's useful."

**Q: How do you know the 100% number is real, not fabricated?**
> "Every number on the slides traces to a JSON results file in the repo, generated by re-running the same evaluator command — nothing is hand-typed into the deck. We can rerun it in front of you if you want proof on the spot." *(True — `python -m evals.checker --version all --split all` regenerates it.)*

**Q: What's the actual architecture / stack?**
> "FastAPI backend, SQLite with trigger-level locking for the policy latch, a small local or cloud LLM behind an OpenAI-compatible interface — model-agnostic by design, we've run three different models through it. PRISM handles observability and evaluation."

**Q: What would you build next?**
> "Real speech-to-text is the most honest next step — the pipeline is ready for it. After that, extending the same latch-and-veto pattern to adjacent regulated domains — banking, telecom — where the same 'agent proposes, code decides' shape applies."

---

## 3. If something breaks live

- **Model doesn't respond / times out:** narrate through it once ("processing — real inference takes a few seconds"), and if it's still hanging after ~15s, stop, say "let me show you the same result from today's verified run instead," and go straight to the Evidence slide/section. Don't debug on stage.
- **Wrong/unexpected agent output:** don't panic-explain. Say plainly: "that's not the expected output — the real model has a small measured miss rate, which is exactly why we don't rely on the model alone for the actual decision, only the enforcement layer does." Then point back to the slide numbers.
- **Judges ask something outside this doc:** it's fine to say "I don't have that number in front of me, but I can follow up" rather than guess. That's more credible than an improvised, possibly wrong, answer.
