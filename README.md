# ClaimGuard × PRISM (ForgeAI Hackathon)

A voice agent for roadside insurance claims — cancellable dispatches, anti-sycophancy policy locks, and pre-LLM PII scrubbing — instrumented end-to-end with Block Convey's PRISM as the diagnostic and evaluation layer. Native-language (Hindi-first) voice capability; written docs stay in English (see `CLAUDE.md`).

## Documentation

**Everything else lives in `docs/`** — read `docs/Overall-plan.md` first, it's the sole canonical plan. `CLAUDE.md` (this directory) holds the standing rules for anyone (human or agent) working in this repo; read it before making changes.

| Doc | What it is |
|---|---|
| `docs/Overall-plan.md` | The canonical plan — architecture, invariants, evaluation methodology, PRISM integration, demo narrative |
| `docs/REMAINING_STEPS_PLAN.md` | Live execution tracker — what's done, what's left, in what order |
| `docs/HANDOVER.md` | Team role split, API contracts, and a "common mistakes" list worth reading before touching evals or telemetry |
| `docs/presentation/DECK-CONTENT.md` | What's actually in the pitch deck — read this, not the deck HTML |
| `docs/research/prism/` | Verified PRISM API/SDK research |

## Repository layout

- **`app/`** — FastAPI backend: voice/PII (`app/security/`, `app/voice/`), agent + RAG (`app/agent/`, `app/rag/`), enforcement (`app/enforcement/`), observability (`app/observability/`)
- **`evals/`** — the 60-call pre-registered replay set and local checker
- **`frontend/`** — live supervisor console
- **`presentation/`** — the built pitch deck (HTML/PDF); gitignored, build output only, not documentation
- **`docs/`** — all project documentation (see above)

## Setup

Copy `.env.example` to `.env` and fill in your API keys. See `.env.example` for required environment variables.
