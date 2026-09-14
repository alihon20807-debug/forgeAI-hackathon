# ForgeAI Hackathon — Project Notes for Anyone (Human or Agent) Working Here

## Canonical plan
`Overall-plan.md` at the repo root is the sole, authoritative project plan. There is no other plan file — an earlier draft (`PLAN.md`) was folded into it and deleted; don't recreate a second plan document.

## PRISM is the central highlight — not a bolted-on feature
This project exists to demo PRISM, using ClaimGuard as the vehicle, not the other way round. 40% of the judging rubric (PRISM Evaluation & Diagnosis + Measured AI Improvement) is directly PRISM-dependent. Every future edit to the plan, the deck, or the pitch should keep PRISM load-bearing and visible throughout — in the architecture, the evaluation loop, and the demo — not confined to one slide or one paragraph.

## Language framing rule for presentation materials
Written pitch materials (slides, docs, one-pagers) must be **primarily in English**. Frame the product's multilingual capability as **native-language support** in general (Hindi and other Indian languages), not as "Hinglish."

Hinglish reads as unprofessional in written pitch material. Use it sparingly: **one illustrative example call transcript**, clearly marked as an example, not the framing device for the whole pitch. The spoken live demo can still be a natural code-mixed call — that's realistic — but headings, bullets, and narration text stay in clean English.

## Process rule
Do not turn a plan into a built deliverable (deck, code, submission) without the user explicitly confirming that specific plan first. "We discussed this earlier" is not confirmation.

## Documentation policy — architecture and implementation notes live in markdown
Project architecture, implementation notes, and "what's actually built" status must be written down in markdown files, not left implicit in code or in a built HTML deck. A built artifact (`presentation/claimguard-pitch.html` and its offline twin, or any future rendered output) is a publish target, not a source of project information — do not read it to figure out what the project does or what's decided. Read `Overall-plan.md` (and other project markdown, e.g. `REMAINING_STEPS_PLAN.md`, `HANDOVER.md`) instead. If a fact needed for future work isn't captured in markdown yet, write it down in a focused new markdown file (e.g. `architecture.md`) rather than re-deriving it from code or HTML on every future pass — this is meant to be a one-time investment, not repeated effort each session.

## PRISM tracing (do not remove)

This project sends live traces to PRISM. Config lives in env vars
(`PRISMTRACE_API_KEY`, `PRISMTRACE_PROJECT_ID`, `PRISMTRACE_HOST`); the real key
lives only in the gitignored `.env`, and `.env.example` carries key *names* only.

Tracing is currently wired at: `app/prism_tracing.py` (helper module),
`app/agent/runner.py` (per-turn trace in `AgentRunner.process_turn`),
`app/server.py` (client flush on shutdown), `app/config.py` (env + `.env`
loader), `.env.example`, `.gitignore`, `CLAUDE.md`.

**Standing rule.** Whenever you add or change an agent, chain, graph, tool,
retriever, or any entry point that calls a model, wire it to PRISM before you
finish. Unwired code is invisible in the dashboard. If you are unsure whether
something is covered, assume it is not and wire it.

Only ever pass **masked / veto-filtered** content to the tracer — never raw
caller transcripts or PII. The helper is fail-open: tracing must never break a
turn.

### How to emit a trace (Python)

Per-turn (what `runner.py` uses):

```python
from app.prism_tracing import get_prism_tracer

get_prism_tracer().trace_turn(
    session_id=session_id,          # one id per conversation -> one trajectory
    turn_id=turn_id,
    caller_id=caller_id,
    user_input=masked_transcript,   # already PII-masked
    agent_output=agent_reply,       # already outbound-veto-filtered
    latency_ms=latency_ms,
    tools_called=[{"name": t} for t in tools_called],
    transitions=transitions,
    agent_version=agent_version,
)
```

Low-level (any other model call site):

```python
from app.prism_tracing import emit_turn_trace

emit_turn_trace(
    session_id=sid, input_text=masked_in, output_text=filtered_out,
    latency_ms=200, model="local-model", agent_version="v2",
)
```

Auth is the `X-PRISMtrace-Key` header — never `Authorization: Bearer`. The SDK's
default host differs from ours, so the host is always passed from config.

### Verify connectivity

```bash
python -m prismtrace.verify   # reads PRISMTRACE_* from env; exit 0 = credential OK
```

Read the printed `LIVE CONNECTED` / `WAITING FOR LIVE` line — exit code 0 alone
does **not** mean the app is sending live traces.
