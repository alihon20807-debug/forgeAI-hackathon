# Recipe: Tracing a FastAPI tool-calling voice agent in PRISM

Target system (from the hackathon brief): a Python/FastAPI, Hinglish/
Tanglish roadside-insurance-claims voice agent calling tools `open_claim`,
`stage_dispatch`, `cancel_dispatch`, `update_claim`. Goal: trace ~50
scripted baseline conversations, inspect failures in PRISM, fix the agent,
re-run the same 50, and show a before/after comparison — with PRISM
evaluation as 20% of judging and measured improvement as another 20%.

All code below is built directly from the verified SDK API surface and
payload schemas documented in `01-integration-sdk.md` and
`02-api-and-payloads.md` in this directory — read those for the full
citation trail (file:line in the downloaded `prismtrace-sdk` 0.4.3 source,
and URLs for docs pages). This file is the synthesis: what to actually
write tonight. Status labels: **VERIFIED** (grounded directly in source/docs
cited in the other two files), **INFERRED** (reasoned, not directly stated),
**NOT FOUND** (searched, absent).

---

## 0. Setup

```bash
pip install "prismtrace-sdk>=0.4.3"     # only runtime dep: httpx>=0.24.0 — VERIFIED
```
```bash
export PRISMTRACE_HOST=https://prism.blockconvey.com   # copy the exact value from your Settings page —
                                                          # the SDK's own hardcoded fallback is a DIFFERENT
                                                          # host, api.prism.blockconvey.com — see 01-integration-sdk.md
export PRISMTRACE_PROJECT_ID=<uuid>
export PRISMTRACE_API_KEY=pt-sk-...
python -m prismtrace.verify     # VERIFIED CLI — prints CREDENTIAL OK/FAIL and LIVE CONNECTED/WAITING FOR LIVE
```
Run `verify` again after the very first real request lands, to confirm
`live_connected: true` before trusting the integration.

Auth header used by every request in this recipe: `X-PRISMtrace-Key:
pt-sk-...` — never `Authorization: Bearer` (**VERIFIED**, repeatedly
confirmed across SDK source; see 02-api-and-payloads.md).

---

## 1. Which integration path fits this agent?

Decision table, all **VERIFIED** from source (01-integration-sdk.md has the
full detail per row):

| If the agent's tool loop is built on... | Use | Tool-call fidelity |
|---|---|---|
| Raw Anthropic SDK (`anthropic.Anthropic().messages.create`) driving the loop yourself | `prismtrace.claude_tracer.ClaudeAgentTracer` | Best: structured tool spans **and** auto-submitted trajectory feeding PRISM's built-in tool-compliance/goal-adherence evaluator |
| LangChain `AgentExecutor` or a plain chain calling tools | `PRISMtraceCallbackHandler` | Good: verified-correct nested chain/agent/tool spans (a real historical bug where AgentExecutor lost its root span is fixed and pinned by tests) |
| LangGraph | `PRISMtraceLangGraphHandler` + `wrap_langgraph()` | Same as LangChain (it's a thin subclass), tagged `[langgraph]` |
| LiteLLM (recommended if routing to Groq/OpenRouter/local vLLM/Ollama — see §6) | `install_litellm()` | Flat: one `/api/traces` row per model call, no nested tool spans, no trajectory |
| OpenAI Agents SDK | `install_openai_agents()` (PREVIEW) | Partial: tool-call spans forwarded individually but hierarchy is flattened, no trajectory auto-submit |
| Hand-rolled FastAPI + any provider's SDK directly, no framework | Manual `POST /api/spans/ingest` (recipe below) | As good as you build it — this is the most likely fit for a from-scratch tool-calling voice agent |
| ElevenLabs Conversational AI for the voice leg | `PRISMtraceVoiceTracer` (live) or the post-call webhook | Turn-level; server-side PII scrubbing is real here specifically |

For a from-scratch FastAPI voice agent (most likely shape for this
hackathon project), the **manual span-ingest recipe in §2** is the
realistic path — there is no SDK tracer that wraps an arbitrary
custom tool-calling loop end-to-end the way `ClaudeAgentTracer` does for
raw Anthropic.

---

## 2. Manual span tracing — copy-pasteable FastAPI integration

Build the HTTP client **once**, at process startup, not per request or per
conversation. Every SDK handler opens its own `httpx.Client`; the SDK's own
test suite (`test_handler_lifecycle.py`) exists specifically because their
generated onboarding guidance used to tell customers to build one handler
per conversation, leaking a connection pool per call — **VERIFIED**, see
01-integration-sdk.md §"Lifecycle". Don't repeat that mistake.

```python
# prism_tracing.py
import os, uuid, threading
from datetime import datetime, timezone
from contextlib import contextmanager
import httpx
import prismtrace   # pip install prismtrace-sdk — used here only for the ambient session contextvar

PRISM_HOST = os.environ["PRISMTRACE_HOST"].rstrip("/")
PROJECT_ID = os.environ["PRISMTRACE_PROJECT_ID"]
HEADERS = {
    "X-PRISMtrace-Key": os.environ["PRISMTRACE_API_KEY"],
    "Content-Type": "application/json",
}
AGENT_ID = "roadside-claims-agent"          # pick once, never change (see identity warning below)
AGENT_VERSION = os.environ.get("AGENT_VERSION", "baseline")   # "baseline" | "v2" — the whole before/after mechanism

# One shared connection pool for the life of the process.
_client = httpx.Client(headers=HEADERS, timeout=15)   # 15s: SDK's own ClaudeAgentTracer uses 15s against a
                                                         # backend documented as sometimes taking >10s cold (KAN-47)

def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _post_spans(trace_id: str, session_id: str, spans: list[dict], extra_metadata: dict | None = None) -> None:
    """Fire-and-forget POST to /api/spans/ingest on a background thread.

    Mirrors the SDK's own fail-open policy: tracing must never break the
    agent's actual response to the caller. Errors are printed, not raised.
    """
    payload = {
        "trace_id": trace_id,
        "project_id": PROJECT_ID,
        "session_id": session_id,
        "metadata": {"agent_id": AGENT_ID, "agent_version": AGENT_VERSION, **(extra_metadata or {})},
        "spans": spans,
    }
    def _send():
        try:
            resp = _client.post(f"{PRISM_HOST}/api/spans/ingest", json=payload)
            if not (200 <= resp.status_code < 300):
                print(f"[prism] spans/ingest {resp.status_code}: {resp.text[:200]}")
        except Exception as e:
            print(f"[prism] spans/ingest failed: {e}")
    threading.Thread(target=_send, daemon=False).start()


class TurnTracer:
    """One instance per conversational turn. Collects a root span plus one
    tool span per tool call, then flushes them all together as one trace.
    """
    def __init__(self, session_id: str, user_utterance: str):
        self.session_id = session_id
        self.trace_id = str(uuid.uuid4())
        self.root_span_id = str(uuid.uuid4())
        self.user_utterance = user_utterance
        self.start_iso = _iso_now()
        self.tool_spans: list[dict] = []

    @contextmanager
    def tool_call(self, tool_name: str, input_payload: dict):
        """Wrap a tool invocation: with tracer.tool_call('open_claim', {...}) as record: ..."""
        span_id = str(uuid.uuid4())
        start = _iso_now()
        record = {"output": None, "status": "ok", "error_message": None}
        try:
            yield record
        except Exception as exc:
            record["status"] = "error"
            record["error_message"] = str(exc)
            raise
        finally:
            end = _iso_now()
            self.tool_spans.append({
                "span_id": span_id,
                "parent_span_id": self.root_span_id,
                "name": tool_name,
                "span_type": "tool",
                "input_text": str(input_payload)[:10000],
                "output_text": str(record["output"])[:10000] if record["output"] is not None else None,
                "metadata": {},
                "start_time": start,
                "end_time": end,
                "status": record["status"],
                "error_message": record["error_message"],
            })

    def finish(self, agent_reply: str, extra_metadata: dict | None = None):
        end_iso = _iso_now()
        root = {
            "span_id": self.root_span_id,
            "parent_span_id": None,
            "name": "agent_turn",
            "span_type": "chain",
            "input_text": self.user_utterance[:10000],
            "output_text": agent_reply[:10000],
            "metadata": {},
            "start_time": self.start_iso,
            "end_time": end_iso,
            "status": "ok",
        }
        _post_spans(self.trace_id, self.session_id, [root, *self.tool_spans], extra_metadata)
```

Usage inside a FastAPI request handler (or wherever the agent loop lives):

```python
from prism_tracing import TurnTracer
import prismtrace

async def handle_turn(call_id: str, user_utterance: str):
    session_id = f"claim-call-{call_id}"          # SAME session_id every turn in this call -> groups the conversation
    with prismtrace.session(session_id):             # ambient session; carries across if you also use SDK handlers
        tracer = TurnTracer(session_id, user_utterance)

        # --- your actual agent/tool logic ---
        with tracer.tool_call("open_claim", {"policy_id": "POL-1123"}) as rec:
            rec["output"] = open_claim(policy_id="POL-1123")   # your real tool function

        # mid-sentence cancellation scenario:
        with tracer.tool_call("cancel_dispatch", {"claim_id": "CLM-4821"}) as rec:
            rec["output"] = cancel_dispatch(claim_id="CLM-4821")

        agent_reply = "Aapka dispatch cancel ho gaya, sir."
        tracer.finish(
            agent_reply,
            extra_metadata={
                # your own judgment, since PRISM has no custom-score API — see §5
                "wrong_commit": False,
                "sycophancy_detected": False,
                "pii_leaked": False,
            },
        )
        return agent_reply
```

Add to FastAPI's lifespan so the connection pool closes cleanly on shutdown:
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from prism_tracing import _client as prism_http_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    prism_http_client.close()

app = FastAPI(lifespan=lifespan)
```

### Threading/async caveat — VERIFIED, important for a voice agent

`prismtrace.session(...)` is a `contextvars.ContextVar`. It propagates into
`asyncio` tasks automatically but **not** across a plain `threading.Thread`
or process-pool worker. If tool execution is offloaded to a thread pool
(common for blocking telephony/DB calls inside an async FastAPI handler),
carry the session id across by hand:
```python
sid = prismtrace.current_session()
# ... hand off to the worker ...
token = prismtrace.bind_session(sid)
try:
    run_tool_in_thread(...)
finally:
    prismtrace.unbind_session(token)
```
**VERIFIED**, `_session.py` docstring + the Google ADK adapter's own
internal workaround for exactly this problem (see 01-integration-sdk.md §4).

### Simpler fallback — flat `/api/traces`, no nested spans

If the team wants coverage without building span trees, POST one flat
trace per turn instead (loses tool-call span detail but is far less code):
```python
import httpx, os

httpx.post(f"{os.environ['PRISMTRACE_HOST']}/api/traces",
    headers={"X-PRISMtrace-Key": os.environ["PRISMTRACE_API_KEY"]},
    json={
        "project_id": os.environ["PRISMTRACE_PROJECT_ID"],
        "model": "claude-sonnet-4-6",
        "input_messages": [{"role": "user", "content": user_utterance}],
        "output_message": agent_reply,
        "latency_ms": latency_ms,
        "session_id": f"claim-call-{call_id}",
        "agent_id": "roadside-claims-agent",
        "metadata": {
            "agent_version": "baseline",
            "tool_called": "cancel_dispatch",
            "wrong_commit": False,
        },
    })
```
**VERIFIED** shape (see 02-api-and-payloads.md `/api/traces` section for
every field and the required-vs-optional table).

---

## 3. Session modeling for a multi-turn voice call

Use **one `session_id` per phone call**, shared across every turn/trace/
span in that call — e.g. `f"claim-call-{call_id}"`. This is purely a
string-matching convention server-side; there is no session-creation
endpoint (**VERIFIED**, 02-api-and-payloads.md, "Tool calls, spans,
sessions — the data model, summarized"). `session_id` **cannot be
backfilled** once traces are sent without it (**VERIFIED**, quickstart
docs) — decide the id scheme before the baseline run, not after.

For the ElevenLabs voice leg specifically, if using `PRISMtraceVoiceTracer`,
note it derives its own `session_id` as `f"elevenlabs:{conversation_id}"`
internally (**VERIFIED**, `elevenlabs_voice.py`) — a *different* value from
whatever you'd pick for the FastAPI-side agent tracing. If both the voice
transport and the agent's tool logic are being traced, either pick one
ingestion path for the whole call, or deliberately correlate the two
session ids via metadata (e.g. store the ElevenLabs `conversation_id`
inside your FastAPI-side trace's `metadata`), since PRISM will otherwise
treat them as two unrelated conversations.

---

## 4. Guardrails: proxy (inline) vs. everything else (post-hoc) — relevant to PII/sycophancy scenarios

**VERIFIED**, `https://blockconvey.com/docs/proxy`: guardrails only run
**inline/blocking** on the zero-code proxy path — "a blocked request never
reaches the provider, and a blocked response is withheld from your user
while the original is still recorded for you to review." Every SDK-based
integration in this recipe (manual spans, LangChain handler, LiteLLM
callback, etc.) is **observational only** — it records what already
happened, it cannot prevent a bad response (a PII leak, a sycophantic
deductible waiver) from reaching the caller. If the team wants PRISM to
actively **block** a PII leak or a sycophancy-driven bad tool call in real
time (rather than just detect it after the fact for the demo), that
requires routing the actual model call itself through
`/proxy/openai/v1` or `/proxy/anthropic` — not just adding SDK tracing on
top of a direct provider call. This is a real architectural choice to make
tonight before the baseline run, not an afterthought. Full guardrail
rule-type detail (PII patterns, India-specific identifiers, etc.) is
another research agent's scope — this recipe only confirms the inline-vs-
post-hoc mechanism.

---

## 5. Custom scores / annotations — the gap, and the workaround

**NOT FOUND**: no endpoint anywhere (SDK or docs) to push a custom
score/annotation onto a trace. The docs' own API reference states plainly:
"No custom score endpoints are documented... No evaluator result push
endpoint is exposed... No manual annotation API documented" (**VERIFIED**,
`https://blockconvey.com/docs/api-reference`, quoted in full in
02-api-and-payloads.md).

**Workaround, and it's a solid one**: the `metadata` object on
`/api/traces` and `/api/spans/ingest` is explicitly **"Free-form.
Filterable in dashboard."** (**VERIFIED**, docs reference table). Use it
for exactly the judgment calls the hackathon needs to demonstrate:
```json
"metadata": {
  "agent_version": "baseline",
  "wrong_commit": true,
  "sycophancy_detected": true,
  "pii_leaked": false,
  "scenario_tag": "mid_sentence_cancellation"
}
```
This is not a PRISM-native score (won't appear on the 6-dimension
scorecard or feed the built-in auto-scores — that's the other research
agent's territory to confirm), but it **is** dashboard-filterable, which is
enough to: (a) manually tag every trace in your 50-conversation baseline
and v2 runs with pass/fail judgments as you review them in PRISM, and
(b) filter/export by `metadata.agent_version` to build your own before/
after tally for the "Measured AI Improvement" judging criterion.

The only PRISM-**native** evaluation signal available via API is the
trajectory evaluator (`POST /api/trajectories` → automated goal-adherence/
tool-compliance/efficiency/safety scoring, **VERIFIED** from the SDK
README and `client.py`) — but that's PRISM's own automated judgment, not a
channel for your own custom pass/fail labels.

---

## 6. Version tagging & before/after workflow — the whole mechanism, end to end

There is **no dataset/experiment/A-B/run-comparison feature found in the
SDK or the API surface reached tonight** (**NOT FOUND** — this agent did
not have scope/budget to check the dashboard UI directly; the other
research thread covering Evaluators Hub / dashboard features may know
more). At the integration layer, version comparison is entirely a
convention you build yourself:

1. Set an env var `AGENT_VERSION=baseline` for the entire baseline run;
   stamp it into `metadata.agent_version` on every trace/span (as shown
   throughout this recipe).
2. Run all ~50 scripted conversations, each with its own `session_id`
   (e.g. `baseline-001` … `baseline-050`), all carrying
   `metadata.agent_version="baseline"`.
3. Review failures in PRISM (mid-sentence cancellations, sycophancy, PII
   leakage), tagging each reviewed trace's `metadata` with your own
   pass/fail judgment fields (§5) — either at emit time if you already know
   the expected outcome (scripted test set), or via a follow-up
   `metadata`-only update if the SDK/API supports partial metadata patch
   (**NOT CONFIRMED** — no `PATCH`/`PUT` on `/api/traces` was found in
   anything read tonight; safest assumption is metadata must be set at
   trace-send time, so decide your pass/fail criteria and self-check logic
   *before* the run, or replay the same inputs a second time with corrected
   metadata rather than trying to edit already-sent traces).
4. Fix the agent. Set `AGENT_VERSION=v2`, re-run the same 50 scripted
   conversations verbatim, same session-id scheme with a `v2-` prefix.
5. In PRISM's dashboard, filter by `metadata.agent_version` to produce the
   before/after view — exact filter/compare UI capability is outside this
   agent's verified scope; confirm with the Evaluators-Hub research thread
   or ask Block Convey staff directly (see open questions).

---

## 7. Open questions for Block Convey staff at the hackathon PRISM session

1. Is `https://prism.blockconvey.com` and the SDK's hardcoded default
   `https://api.prism.blockconvey.com` the same backend? Which should we
   standardize `PRISMTRACE_HOST` on?
2. Is there truly no API to push a custom score/annotation onto a trace, or
   does an undocumented endpoint exist? Given "Measured AI Improvement" is
   20% of judging, what's the intended way to attach our own pass/fail
   judgment to a trace programmatically, at hackathon scale (50+50
   conversations)?
3. Is there a dataset/experiment/run-comparison feature in the dashboard
   that pairs with `metadata.agent_version` filtering, or is manual
   dashboard filtering the actually-intended before/after workflow?
4. Can `metadata` on an already-sent trace be updated after the fact (a
   PATCH-like operation), or is trace content immutable once POSTed?
5. Does the zero-code proxy support any non-Anthropic/OpenAI/Gemini backend
   (Groq, OpenRouter, local vLLM/Ollama, Gemma specifically) under any
   configuration, or is `install_litellm()` the only sanctioned path for
   those providers? (Docs explicitly say "three routes exist and only
   three" — worth confirming this hasn't changed.)
6. Free tier is listed as 25,000 traces/month, 14-day retention, no
   guardrails, no Evaluators Hub (per `/docs/reference`) — confirm this is
   current and sufficient for baseline + v2 runs plus iteration, and
   whether the "no guardrails on Free tier" limit blocks the PII/sycophancy
   guardrail scenarios the team wants to demonstrate.
7. For a voice agent split across ElevenLabs (transport) and FastAPI
   (tool logic): is there a recommended way to correlate
   `PRISMtraceVoiceTracer`'s `elevenlabs:{conversation_id}` session with a
   separately-traced FastAPI-side session for the same call, so both show
   up as one conversation rather than two?
