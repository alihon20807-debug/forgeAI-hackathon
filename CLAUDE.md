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

**Canonical implementation: `app/observability/prism_tracer.py` (`PRISMTracer`
/ `TurnTracer`). There is exactly one tracer — do not add a second one.**
A second, parallel tracer (`app/prism_tracing.py`) existed briefly and got
wired into the live call path *alongside* this one — every turn through
`app/server.py`'s `/api/call/turn` fired two independent trace requests to
two different PRISM endpoints, silently doubling credit consumption on a
98-of-100-credit Free-tier budget and producing duplicate, differently-shaped
records for the same conversation in the dashboard. That module is now a
retired stub that raises `ImportError` on import specifically so a stray
reintroduction fails loudly instead of silently resurrecting the double-fire.
The reason this one is canonical, not the other: it matches the team's own
verified research (`research/prism/03-fastapi-agent-integration-recipe.md`'s
decision table recommends structured `/api/spans/ingest` for exactly this
architecture — a hand-rolled FastAPI tool-calling agent), it already had
correct per-version `agent_id` mapping and `category`/`eval_set` support, and
it produces richer nested spans (tool calls and commit-window transitions as
separate child spans, not just flat metadata).

Tracing is wired at: `app/observability/prism_tracer.py` (the tracer itself),
`app/server.py` (`/api/call/turn` builds a `TurnTracer` per request, and calls
`close()` on shutdown), `evals/checker.py` (builds a `TurnTracer` per replay-set
turn — same pattern, so replay-set traces carry `category`/`set` too),
`app/config.py` (env + `.env` loader), `.env.example`, `.gitignore`.

**Standing rule.** Whenever you add or change an agent, chain, graph, tool,
retriever, or any entry point that calls a model, wire it to PRISM before you
finish, by building a `TurnTracer` around that call site the same way
`app/server.py`/`evals/checker.py` do — **do not** make `AgentRunner.process_turn`
trace itself internally again; that's what caused the double-fire. Unwired
code is invisible in the dashboard. If you are unsure whether something is
covered, assume it is not and wire it, but wire it at the *caller*, not inside
the shared method both callers already call.

Only ever pass **masked / veto-filtered** content to the tracer — never raw
caller transcripts or PII. The tracer is fail-open: tracing must never break a
turn.

### How to emit a trace (Python)

```python
from app.observability.prism_tracer import TurnTracer

tracer = TurnTracer(
    session_id=session_id,          # one id per conversation -> one trajectory
    user_utterance=masked_transcript,  # already PII-masked
    agent_version=agent_version,    # "v0" / "v1" / "v2" -> mapped to the right agent_id
    category=category,              # optional: "A_CLEAN_CONTROL".."F_SPOKEN_IDENTIFIERS"
    eval_set=eval_set,               # optional: "dev" / "heldout"
)

# ... call the agent, get back state_machine.transitions ...
for t in transitions:
    tracer.record_enforcement_transition(
        action_id=t["action_id"], action_type=t["action_type"],
        from_state=t["from_state"], to_state=t["to_state"], reason=t["reason"],
    )

tracer.finish(agent_reply=agent_reply, extra_metadata={"turn_id": turn_id})
```

Auth is the `X-PRISMtrace-Key` header — never `Authorization: Bearer`.

### Verify connectivity

There's no separate CLI for this (the old `python -m prismtrace.verify` command
belonged to the now-removed `prismtrace-sdk` dependency, no longer installed).
To check live connectivity: set real `PRISMTRACE_API_KEY`/`PRISMTRACE_PROJECT_ID`
in `.env`, run a 3-call smoke test (`python -m evals.checker --version v2 --split dev`
against a tiny scenario subset, or a manual `/api/call/turn` request), then check
the PRISM dashboard directly for the session — `data/prism_traces.jsonl` always
gets a local entry regardless of live credentials, so its presence alone does
**not** prove a live send succeeded; only the dashboard does.
