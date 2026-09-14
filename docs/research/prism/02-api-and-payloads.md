# PRISM API Reference — Endpoints, Payload Schemas, Data Model

Status legend: **VERIFIED** (cite URL or SDK file:line), **INFERRED**,
**NOT FOUND**. Two ground-truth sources were cross-checked against each
other for this file: (a) `prismtrace-sdk` v0.4.3 source (see file 01 for
provenance), which is what actually constructs and sends these payloads,
and (b) `https://blockconvey.com/docs/api-reference`,
`https://blockconvey.com/docs/integrations`, `https://blockconvey.com/docs/quickstart`,
and `https://blockconvey.com/docs/reference` (fetched 2026-09-14). Where
the two disagree or one adds detail the other lacks, both are noted.

## Base URLs — two hostnames in circulation

- SDK hardcoded default: `https://api.prism.blockconvey.com` (`_config.py`,
  **VERIFIED** from source).
- Docs site quickstart/reference: `https://prism.blockconvey.com` (**VERIFIED**
  via WebFetch of `/docs/quickstart` and `/docs/reference`).
- Treat `PRISMTRACE_HOST` as the single source of truth and copy it verbatim
  from your own project's Settings page rather than assuming either default
  — see file 01 for the full discussion. All endpoint paths below are
  identical regardless of which host you use.

## Authentication (every endpoint, all requests)

Header: `X-PRISMtrace-Key: pt-sk-...`
**Never** `Authorization: Bearer ...` — multiple independent sources
confirm this is enforced, including a fixed historical bug in the SDK's own
OTel exporter (`otel.py` docstring: "it authenticated with `Authorization:
Bearer`, but the ingest route reads only `X-PRISMtrace-Key`... depending on
`INGEST_AUTH_MODE` that is either a 401 or an ingest with no credential
checked at all"). **VERIFIED**, cross-confirmed by SDK source and docs.

Key scopes (**VERIFIED**, `/docs/api-reference` + `/docs/integrations`):
- `ingest` — send traces/spans (what your application key should carry)
- `read` — read traces, analyses, balances
- `operate` — trigger credit-spending actions

Legacy: a body-level `api_key` field on `/api/traces` is deprecated but
still accepted; responses using it carry an `X-PRISMtrace-Deprecation`
header (**VERIFIED**, `/docs/api-reference`). Use the header, not the body
field.

---

## `POST /api/traces` — one exchange record

The simplest, most universal endpoint. Used directly by the LiteLLM
callback, the Google ADK adapter, the OpenAI Agents processor, and the raw
cURL quickstart. **VERIFIED** end-to-end: the exact field set below is
confirmed both by the docs page and by reading every SDK call site that
builds this payload (`litellm_callback.py:157-175`, `google_adk.py:779-789`,
`openai_agents.py:219-238`, `client.py:103-123`).

### Required fields
| Field | Type | Notes |
|---|---|---|
| `project_id` | string (UUID) | From Settings → Project |
| `model` | string | Drives per-model cost/latency breakdowns. SDK integrations **tag** this field to signal framework, e.g. `"litellm:gpt-4o"`, `"google-adk:gemini-3.6-flash"`, `"openai-agents:generation:gpt-4o"` — the backend's "architecture extractor" parses this string to detect framework. If you hand-roll `/api/traces` calls yourself, plain model names work fine; framework tagging is an SDK convention, not a requirement. |
| `input_messages` | array of `{role, content}` | |
| `output_message` | string | The agent's reply text |
| `latency_ms` | int | "Send 0 if unmeasured" per docs |

### Optional fields
| Field | Type | Notes |
|---|---|---|
| `session_id` | string | Groups traces into one conversation. **"Cannot be backfilled"** per quickstart docs — get it right at send time. |
| `agent_id` | string | Stable identifier; scopes guardrail/alert rules and Model Inventory. **Do not change once picked** — changing it re-identifies the agent to every rule (explicit warning in SDK docstring, `client.py:89-97`). |
| `agent_name` | string | Human display label — free to change |
| `user_identifier` | string | End-user id from your system |
| `trace_id` | string | Your own id. **Resending the same `trace_id` returns the existing trace instead of creating a duplicate** — de-dup / idempotency built in. |
| `token_count_input` / `token_count_output` | int | Default 0 |
| `metadata` | object | **Free-form, filterable key-value pairs.** This is the mechanism for version tagging (see file 03) — there is no dedicated "version" field. |

### Example request
```json
POST https://prism.blockconvey.com/api/traces
X-PRISMtrace-Key: pt-sk-...
Content-Type: application/json

{
  "project_id": "00000000-0000-0000-0000-000000000000",
  "model": "claude-sonnet-4-6",
  "input_messages": [{"role": "user", "content": "Gaadi kharab ho gayi, tow chahiye"}],
  "output_message": "Aapka claim CLM-4821 open ho gaya hai. Tow truck 20 minute mein pahunchega.",
  "latency_ms": 420,
  "session_id": "call-9f21a3",
  "agent_id": "roadside-claims-agent",
  "agent_name": "Roadside Claims Bot",
  "token_count_input": 45,
  "token_count_output": 32,
  "user_identifier": "caller-4521",
  "metadata": {
    "agent_version": "baseline",
    "channel": "voice",
    "language": "hinglish"
  }
}
```

### Response
`200` with the stored trace: `id`, `cost_usd`, `session_id` (**VERIFIED**,
`/docs/api-reference`).

### Error codes (this and every endpoint)
| Status | Meaning |
|---|---|
| 401 | Missing/invalid credential, or wrong header name |
| 402 | Insufficient credits or plan limit exceeded — response body names `insufficient_credits` or `plan_limit_reached` |
| 403 | Valid key, wrong project, or key lacks required scope |
| 404 | Project does not exist |
| 415 | Unsupported content type (e.g. gRPC hitting the OTLP endpoint) |
| 429 | Rate limited — **200 requests/minute on the ingest endpoint** |

`200` responses can still carry an `X-PRISMtrace-Plan-Warning` header when
you exceed a volume/model ceiling — the trace is still stored despite the
warning (**VERIFIED**, `/docs/integrations`).

---

## `POST /api/spans/ingest` — structured span trees (trace/agent-run detail)

This is the endpoint that produces the nested trace/span view (root chain
span → agent/tool/llm child spans) rather than a flat one-row-per-call
trace. Used by `PRISMtraceCallbackHandler` (LangChain/LangGraph),
`ClaudeAgentTracer`, and `PRISMtraceSpanExporter` (OTel shim).
**VERIFIED** directly against every SDK call site that builds this payload:
`langchain_handler.py:639-648`, `claude_tracer.py:264-276`, `otel.py:285-293`.

### Top-level payload
```json
{
  "trace_id": "string",
  "project_id": "string (UUID)",
  "session_id": "string (optional but strongly recommended)",
  "metadata": {},
  "spans": [ /* array of span objects, see below */ ]
}
```

### Span object — every field the SDK populates
```json
{
  "span_id": "string",
  "parent_span_id": "string | null",
  "name": "string",
  "span_type": "chain | llm | tool | agent | retrieval",
  "input_text": "string | null   (capped ~10,000 chars by the SDK)",
  "output_text": "string | null  (capped ~10,000 chars by the SDK)",
  "metadata": {},
  "start_time": "ISO8601 UTC timestamp",
  "end_time": "ISO8601 UTC timestamp | null",
  "duration_ms": "number | null",
  "status": "ok | error",
  "error_message": "string | null",
  "token_count_input": "int | null",
  "token_count_output": "int | null",
  "cost_usd": "number | null",
  "model": "string | null   (only meaningful on llm-type spans)"
}
```
`span_type` values actually emitted by the SDK, confirmed by grepping every
module: **`chain`, `llm`, `tool`, `agent`, `retrieval`**
(`langchain_handler.py` uses all five; `claude_tracer.py` uses
`chain`/`llm`/`tool`/`agent`; `otel.py`'s `_OPERATION_SPAN_TYPES` maps OTel
GenAI operation names onto this same five-value set, defaulting unknown
values to `chain`). **No other `span_type` values were found anywhere** —
treat this as the closed vocabulary for the field unless the dashboard docs
(out of this agent's scope) say otherwise.

### Example — a tool-calling turn (shape matches what `ClaudeAgentTracer` and `PRISMtraceCallbackHandler` actually send)
```json
{
  "trace_id": "8f14e45f-ceea-4dbb-b1a7-7ad3f3c1e14a",
  "project_id": "00000000-0000-0000-0000-000000000000",
  "session_id": "call-9f21a3",
  "spans": [
    {
      "span_id": "root-1",
      "parent_span_id": null,
      "name": "claude_agent_run",
      "span_type": "chain",
      "input_text": "[{\"role\": \"user\", \"content\": \"Gaadi kharab ho gayi\"}]",
      "output_text": "Aapka claim open ho gaya hai.",
      "metadata": {"total_iterations": 2, "model": "claude-sonnet-4-6"},
      "start_time": "2026-09-14T10:00:00.000Z",
      "end_time": "2026-09-14T10:00:03.200Z",
      "duration_ms": 3200,
      "status": "ok"
    },
    {
      "span_id": "llm-1",
      "parent_span_id": "root-1",
      "name": "llm:claude-sonnet-4-6",
      "span_type": "llm",
      "input_text": "...",
      "output_text": null,
      "metadata": {"iteration": 1},
      "start_time": "2026-09-14T10:00:00.000Z",
      "end_time": "2026-09-14T10:00:01.100Z",
      "duration_ms": 1100,
      "status": "ok",
      "token_count_input": 220,
      "token_count_output": 40,
      "model": "claude-sonnet-4-6"
    },
    {
      "span_id": "tool-1",
      "parent_span_id": "root-1",
      "name": "open_claim",
      "span_type": "tool",
      "input_text": "{\"policy_id\": \"POL-1123\", \"incident_type\": \"breakdown\"}",
      "output_text": "{\"claim_id\": \"CLM-4821\", \"status\": \"open\"}",
      "metadata": {"tool_id": "toolu_01abc"},
      "start_time": "2026-09-14T10:00:01.100Z",
      "end_time": "2026-09-14T10:00:01.340Z",
      "duration_ms": 240,
      "status": "ok"
    }
  ]
}
```
**This is the pattern to replicate manually for a FastAPI tool-calling
agent that doesn't use LangChain, LiteLLM, or the Anthropic SDK directly** —
see file 03 for a copy-pasteable version wired to `open_claim`,
`stage_dispatch`, `cancel_dispatch`, `update_claim`.

---

## `POST /api/trajectories` — the trajectory-evaluation surface

The endpoint that feeds PRISM's **automated trajectory evaluation**
(described in the SDK README as scoring "goal adherence, tool compliance,
efficiency, and safety"). **VERIFIED** from `client.py::submit_trajectory`
and `claude_tracer.py:280-303`; **not independently confirmed on the docs
site** tonight (the `/docs/api-reference` fetch summarized `/api/traces`,
`/api/spans/ingest`, and `/api/otlp/v1/traces` but did not surface
`/api/trajectories` in its listing — likely just because the WebFetch
summary didn't include every endpoint, not necessarily that it's undocumented).
Treat the endpoint's *existence and shape* as VERIFIED (it's exercised by
the SDK against a real backend, per the README's working example) and its
*documentation status on the marketing site* as unconfirmed.

### Payload (`client.py:223-242`)
```json
{
  "project_id": "string",
  "conversation_id": "string  (ambient session id, or a generated uuid)",
  "request_id": "string  (defaults to a generated uuid)",
  "agent_id": "string  (falls back to agent_name if omitted — see the identity warning in file 01)",
  "agent_name": "string",
  "steps": [
    {
      "step_type": "reasoning | tool_call | final_answer",
      "label": "string",
      "input_summary": "string (optional)",
      "output_summary": "string (optional, recommended)",
      "tool_name": "string  (required when step_type == tool_call)",
      "duration_ms": "int (optional)",
      "token_count": "int (optional)",
      "status": "success | error   (default success)"
    }
  ],
  "total_duration_ms": "int  (SDK sums step durations for you if you use client.py's helper)",
  "final_status": "success | error",
  "model": "string | null"
}
```

### Companion endpoints (all **VERIFIED**, `client.py:301-314`)
| Endpoint | Method | Purpose |
|---|---|---|
| `/api/trajectories/{id}` | GET | Fetch a trajectory + its steps |
| `/api/trajectories/{id}/evaluation` | GET | Fetch PRISM's evaluation results for it |
| `/api/trajectories/{id}/evaluate?project_id=...` | POST | Re-trigger evaluation (e.g. after changing evaluator config) |

Evaluation runs **asynchronously after submission** — `get_trajectory_evaluation`
must be polled/re-fetched rather than expecting a result inline with the
submit response (per README comment: "Check evaluation results (runs async
after submission)").

**Direct relevance to the hackathon's tool-calling correctness use case**:
this is the closest thing PRISM has to a built-in "tool-call correctness /
trajectory quality" evaluator mentioned in the research questions — it's a
**built-in automated evaluator over the trajectory you submit**, scoring
tool compliance and goal adherence. It is not a place to push your **own**
custom pass/fail judgment (e.g. `wrong_commit=1`) — see the Custom
Scores section below for that gap.

---

## `POST /api/otlp/v1/traces` — OpenTelemetry Protocol ingestion

**VERIFIED**, both SDK (`otel.py` docstring, README) and docs
(`/docs/integrations`, `/docs/api-reference`).

- Set `OTEL_EXPORTER_OTLP_ENDPOINT` to `.../api/otlp` **without** the
  `/v1/traces` suffix — OTLP's own spec appends the signal path
  automatically, giving the full path above. Appending it yourself breaks
  ingestion.
- `OTEL_EXPORTER_OTLP_PROTOCOL` must be set explicitly to `http/protobuf` or
  `http/json`. **gRPC is not served** — an exporter that defaults to gRPC
  (explicitly called out: "the Java SDK does") fails silently.
- `OTEL_EXPORTER_OTLP_HEADERS=X-PRISMtrace-Key=pt-sk-...`
- Supported request encodings: `application/x-protobuf`,
  `application/protobuf`, `application/json`.
- Reads OpenTelemetry GenAI semantic-convention attributes automatically —
  no `prismtrace.*` attributes needed if you're already using standard
  GenAI instrumentation. See file 01 §9 for the full attribute-mapping
  table (this is genuinely the most portable, language-agnostic ingestion
  path — any OTel-instrumented service in any language can point at this
  with zero PRISM-specific code).
- Resource attribute `prismtrace.project_id` can override which project a
  batch of OTLP spans lands in, checked against the API key
  (**VERIFIED**, `/docs/api-reference`).

---

## `POST /api/voice/turns` — ElevenLabs live voice turns

**VERIFIED**, `elevenlabs_voice.py:205-224`. Not mentioned on the fetched
docs pages tonight (SDK-only confirmation). Payload:
```json
{
  "project_id": "string",
  "conversation_id": "string",
  "turns": [{"role": "user | agent", "message": "string"}],
  "status": "in-progress | done",
  "agent_id": "string | null",
  "agent_name": "string",
  "start_index": "int"
}
```
Server scrubs PII from transcript text before storage (per SDK docstring;
this guarantee is specific to this endpoint / the voice ingestion path —
see file 01 §8 for the caveat that this scrubbing is **not** documented as
applying to `/api/traces` or `/api/spans/ingest`).

---

## `POST /api/setup-doctor/handshake` and `GET /api/setup-doctor` — connectivity verification

**VERIFIED**, `verify.py` (full file read) + `/docs/quickstart`.

```bash
curl -sS -X POST "$PRISMTRACE_HOST/api/setup-doctor/handshake" \
  -H "Content-Type: application/json" -H "X-PRISMtrace-Key: $PRISMTRACE_API_KEY" \
  -d '{"project_id": "'"$PRISMTRACE_PROJECT_ID"'", "send_test_trace": true}'

curl -sS "$PRISMTRACE_HOST/api/setup-doctor?project_id=$PRISMTRACE_PROJECT_ID" \
  -H "X-PRISMtrace-Key: $PRISMTRACE_API_KEY"
```
`GET /api/setup-doctor` response fields (`verify.py::render`,
`/docs/api-reference`):
- `live_connected`: bool — a **real, non-demo** trace was received (not the
  handshake's synthetic test trace)
- `app_connected`: stricter — trace came from the customer's own
  application specifically
- `blocked_step`: which pipeline stage is stuck, one of `event_received`,
  `trace_normalized`, `analysis_ready`
- `steps`: array of `{status, title, detail}` for a human-readable pipeline
  view (`verify.py::render` prints these with ✓/·/? symbols)
- `overall`: an overall status string

Also available as a CLI the team can literally run tonight to sanity-check
their setup before writing any agent code:
```bash
python -m prismtrace.verify   # reads PRISMTRACE_HOST/PROJECT_ID/API_KEY from env
```
Exit codes: `0` = credential OK (does **not** mean the app is sending live
traces — you must also read the printed `LIVE CONNECTED` / `WAITING FOR
LIVE` line); `1` = doctor unreachable; `2` = credential/args wrong.
**VERIFIED**, `verify.py:1-14`.

---

## Credits / entitlements (read-only, GET) — cross-referenced only

Not this agent's core scope (pricing/PRISMX is assigned elsewhere), but the
endpoints exist and are worth knowing since a `402` from `/api/traces` will
point here:
```
GET /api/credits/summary
GET /api/credits/ledger
GET /api/credits/catalog
GET /api/entitlements
GET /api/entitlements/usage
```
**VERIFIED**, `/docs/api-reference` and `/docs/reference`.

---

## The zero-code proxy — exact scope, and what it does NOT cover

**VERIFIED**, fetched directly: `https://blockconvey.com/docs/proxy` quotes
the docs verbatim as **"Three routes exist and only three"**:

| Provider | Proxy base URL |
|---|---|
| Anthropic | `https://prism.blockconvey.com/proxy/anthropic` |
| OpenAI | `https://prism.blockconvey.com/proxy/openai/v1` |
| Gemini | `https://prism.blockconvey.com/proxy/gemini` |

### OpenAI Python client through the proxy
```python
import openai
client = openai.OpenAI(
    base_url="https://prism.blockconvey.com/proxy/openai/v1",
    api_key=os.environ["OPENAI_API_KEY"],   # your real OpenAI key — the proxy forwards to actual OpenAI
    default_headers={"X-PRISMtrace-Key": os.environ["PRISMTRACE_API_KEY"]},
)
```
### Gemini client through the proxy
```python
import google.generativeai as genai
genai.configure(
    api_key=os.environ["GOOGLE_API_KEY"],
    client_options={"api_endpoint": "https://prism.blockconvey.com/proxy/gemini"},
    default_headers={"X-PRISMtrace-Key": os.environ["PRISMTRACE_API_KEY"]},
)
```
**VERIFIED**, `/docs/integrations` (fetched verbatim).

### IMPORTANT — refutes an assumption in the research brief
**The proxy is a pass-through to the real OpenAI / Anthropic / Gemini APIs,
authenticated with YOUR real provider API key — it is NOT a universal
OpenAI-compatible gateway.** The docs explicitly say only three routes
exist. There is **no evidence the proxy accepts a third-party
OpenAI-compatible backend** (Groq, OpenRouter, local vLLM, Ollama) by
pointing `base_url` at it with a different `api_key` — nothing in the docs
or SDK suggests the proxy inspects `api_key`/model name to route elsewhere,
and the explicit "only three" framing strongly implies it does not.
**INFERRED** (not a positive confirmation either way that it actively
*rejects* a non-matching key — simply that this usage is undocumented and
unsupported).

**Gemma models via the Gemini API**: **NOT FOUND.** No page or SDK file
mentions Gemma by name. Google does serve some Gemma models through the
Gemini API surface (general product knowledge, not PRISM-specific) — since
the proxy is a transparent forward to Gemini's real endpoint, a Gemma model
name that the Gemini API itself accepts would plausibly pass through
untouched, but this is **speculation, not verified** for PRISM specifically.

**What actually IS the right path for Groq / OpenRouter / vLLM / Ollama /
other OpenAI-compatible backends: `install_litellm()`.** LiteLLM itself
natively routes to all of these providers (its own docstring in the SDK
lists Ollama explicitly among ~100 supported providers), and
`install_litellm()` traces every `litellm.completion()` call regardless of
which underlying provider it routed to, with **zero extra PRISM-side
configuration per provider**. This is the correct, SDK-verified answer —
see file 01 §5. Route local/non-major-provider models through LiteLLM, not
through the zero-code proxy.

Guardrail behavior on the proxy specifically (**VERIFIED**, `/docs/proxy`):
"Guardrails on the proxy run on the call itself: a blocked request never
reaches the provider, and a blocked response is withheld from your user
while the original is still recorded for you to review." This is
**preventive/inline blocking**, unique to the proxy path — SDK-based
integrations (LangChain handler, LiteLLM callback, etc.) are all
**observational/post-hoc**: they trace what already happened, they cannot
block a call before it reaches the provider. Latency overhead of the proxy
itself: **"roughly 5 to 15 ms depending on region"** (**VERIFIED**, same
page) — before any guardrail evaluation time on top.

Azure AI Foundry: use the OpenAI proxy route with an `x-azure-endpoint`
header naming your resource (**VERIFIED**, `/docs/integrations`).

### Tunneling local models for PRISM cloud reachability
If attempting to route PRISM's cloud reverse proxy or cloud-based Synthetic Scenarios / Evaluators to a local model running on your machine (`localhost:8080`), PRISM's cloud servers cannot reach `127.0.0.1` directly.
- **Solution:** Expose the local port via Cloudflare Tunnel (`cloudflared tunnel --url http://localhost:8080`, wrapped in `scripts/expose_local_model.sh` and `scripts/run_local_model.sh --expose`).
- **Why Cloudflare Tunnel over ngrok:** Zero account/token setup for ephemeral tunnels, no monthly bandwidth/request caps, and crucially **no HTML interstitial warning page** (`ngrok-skip-browser-warning`) that silently breaks API proxy and JSON forwarding. Pinggy SSH (`ssh -p 443 -R0:localhost:8080 a.pinggy.io`) provides an instant zero-binary fallback.

---

## Custom scores / manual annotations — what exists and what doesn't

Directly answering the research brief's question 3/4 (API side).

**NOT FOUND anywhere** — no dedicated "push a custom score" or "push an
annotation" endpoint in the API reference, the reference quick-lookup
table, or the SDK source. The `/docs/api-reference` fetch's own summary
states this outright under "Notable Constraints":
> "No custom score endpoints are documented. Automatic scoring occurs on
> all traces; metered actions are triggered via the dashboard, not API."
> "No evaluator result push endpoint is exposed. Evaluators Hub scores are
> collected through the dashboard UI or imports."
> "No manual annotation API documented. Annotations are managed through the
> dashboard interface."
(quoted from the WebFetch summary of `https://blockconvey.com/docs/api-reference`,
2026-09-14)

**The only two API-level mechanisms available tonight to attach your own
signal to a trace:**

1. **`metadata` (free-form, filterable key-value object)** on `/api/traces`
   and `/api/spans/ingest`. This is not a "score" in PRISM's own scoring
   sense (won't feed the 0–100 auto-scores or show up on the scorecard —
   that's the other research agent's territory), but it **is** filterable
   in the dashboard per the docs' own description of the field
   ("Free-form. Filterable in dashboard."). This is the mechanism to use
   for:
   - Your own boolean/numeric judgment, e.g.
     `"metadata": {"wrong_commit": true, "reviewer_note": "cancelled the wrong dispatch mid-sentence"}`
   - Version tagging: `"metadata": {"agent_version": "baseline"}` vs.
     `"metadata": {"agent_version": "v2-fixed-sycophancy"}` — then filter/
     compare in the dashboard by that metadata key. **This is the
     recommended before/after mechanism** — see file 03.
2. **`submit_trajectory()` → `final_status` and per-step `status`**
   (`"success"`/`"error"`) — a coarser, PRISM-native signal that does feed
   the trajectory evaluator, but it's a status enum, not an arbitrary
   scoring channel, and it only applies if you're using the trajectory
   endpoint at all.

**Practical implication for the hackathon**: there is no API call that
says "PRISM, record that this specific trace was a wrong-tool-call
failure as a first-class score." The workaround is metadata tagging +
building your own before/after comparison (counting `metadata.wrong_commit
== true` across your baseline vs. v2 trace sets, either by exporting traces
or by whatever filter/dashboard capability the Evaluators-Hub research
agent confirms). **Open question for Block Convey staff**: ask directly
whether a custom-score API is on their roadmap or exists under an
undocumented endpoint — the gap is large enough (given the hackathon's
explicit "evidence-based improvement" judging criterion) that it's worth a
direct question rather than assuming the metadata workaround is the
intended path.

---

## Tool calls, spans, sessions — the data model, summarized

- **Trace** = one exchange (one model call, from PRISM's simplest view) —
  `/api/traces`.
- **Span** = one step inside a run (model call, tool call, chain, agent
  decision, retrieval) with parent/child nesting — `/api/spans/ingest`.
  `span_type ∈ {chain, llm, tool, agent, retrieval}` (closed vocabulary,
  see above).
- **Trajectory** = an ordered list of `{reasoning, tool_call, final_answer}`
  steps submitted specifically for PRISM's automated evaluation (goal
  adherence / tool compliance / efficiency / safety) — `/api/trajectories`.
  Distinct from spans: a trajectory is evaluation input, a span is trace
  detail. The SDK's richest integrations (`ClaudeAgentTracer`) emit BOTH
  for the same run, correlated by `session_id`.
- **Session** = the grouping key across multiple traces/spans/trajectory
  submissions that make up one conversation — carried as `session_id`
  everywhere. Ambient session context (`prismtrace.session(...)`) is a
  client-side SDK convenience only; the actual grouping happens server-side
  purely off the `session_id` string value you send. You can achieve
  identical grouping via raw HTTP calls (no SDK) by just sending the same
  `session_id` string on every call belonging to one conversation — this is
  the important portable takeaway for a from-scratch FastAPI integration.
- **Tool calls specifically**: represented as `span_type="tool"` spans
  (structured path) or as flat `/api/traces` rows tagged in metadata
  (LiteLLM/ADK path) or as `tool_call`-type trajectory steps (evaluation
  path). There is no dedicated "tool call" object/endpoint separate from
  these three representations.
- **Agent identity**: `agent_id` (stable, rule-scoping) vs. `agent_name`
  (display, free to change) is a real, enforced distinction across every
  endpoint that accepts both — always set `agent_id` deliberately once and
  never change it for the life of the project.
