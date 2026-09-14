# PRISM / PRISMtrace — SDK & Integration Ground Truth

Scope: `prismtrace-sdk` package internals, every integration path, constructor
signatures, flush/lifecycle/async behavior. All claims are marked:

- **VERIFIED** — seen directly in SDK source (file:line, from the downloaded
  sdist) or fetched docs (URL given).
- **INFERRED** — reasoned from verified material, not stated outright.
- **NOT FOUND** — searched for, not present in any source available tonight.

Ground truth source: `prismtrace-sdk` **v0.4.3**, downloaded from PyPI as
`prismtrace_sdk-0.4.3.tar.gz` (sdist) and the matching wheel, both fetched
from `https://files.pythonhosted.org/...` on 2026-09-14, extracted to
`/tmp/.../scratchpad/prism/extracted/prismtrace_sdk-0.4.3/`. Wheel `RECORD`
hashes match the sdist files 1:1 — same code either way. Local paths cited
below are relative to that extraction root.

Latest release per PyPI JSON (`https://pypi.org/pypi/prismtrace-sdk/json`):
`0.3.2, 0.4.0, 0.4.1, 0.4.2, 0.4.3`. **0.4.3 is current** as of research date.

## IMPORTANT: two different hosts appear in the wild — pick the right one

- The SDK's own hardcoded default (`prismtrace/_config.py:33`, `DEFAULT_HOST`)
  is **`https://api.prism.blockconvey.com`**. **VERIFIED**, file:
  `prismtrace/_config.py` line 33: `DEFAULT_HOST = "https://api.prism.blockconvey.com"`.
- The public marketing/docs site (`blockconvey.com/docs`) and its quickstart
  examples use **`https://prism.blockconvey.com`** for both the dashboard and
  as `PRISMTRACE_HOST` in cURL examples. **VERIFIED** via
  `https://blockconvey.com/docs/quickstart` (fetched 2026-09-14).
- These are plausibly the same backend behind two DNS names (app host vs.
  API host), but this was **not proven** — no cross-request was made tonight
  to confirm `api.prism.blockconvey.com` and `prism.blockconvey.com` route to
  identical infrastructure. **Recommendation for the team:** always set
  `PRISMTRACE_HOST` explicitly from the value shown on your own
  **Settings → Project** page (or API keys page) rather than trusting either
  hardcoded default — resolution order below shows the explicit value always
  wins anyway. **Open question for Block Convey staff** (see recipe file).

## Resolution order for host/key/project (all handlers use this)

Verified in `prismtrace/_config.py` (`resolve_host`) and independently
duplicated (with identical precedence) in `langchain_handler.py::_resolve_host`
and inline in several other modules:

1. Explicit constructor argument (`host=` / `endpoint=`).
2. Environment variable, first non-empty of: `PRISMTRACE_HOST`, then
   `PRISMTRACE_ENDPOINT`.
3. `DEFAULT_HOST` (`https://api.prism.blockconvey.com`).

Env vars read across the whole SDK: `PRISMTRACE_API_KEY`,
`PRISMTRACE_PROJECT_ID`, `PRISMTRACE_HOST` (and the legacy
`PRISMTRACE_ENDPOINT` alias). **VERIFIED**, `_config.py`.

Auth header on every single HTTP call the SDK makes:
`X-PRISMtrace-Key: pt-sk-...` — **never** `Authorization: Bearer`. Verified
repeatedly across every module (`client.py`, `langchain_handler.py`,
`litellm_callback.py`, `claude_tracer.py`, `google_adk.py`,
`openai_agents.py`, `elevenlabs_voice.py`, `otel.py`). The `otel.py` module
docstring explicitly calls out a historical bug where it sent
`Authorization: Bearer` and got silently rejected/unauthenticated — a strong
signal this header name is load-bearing and easy to get wrong.

## Install

```bash
pip install "prismtrace-sdk>=0.4.3"
```

Single runtime dependency: `httpx>=0.24.0` (from
`prismtrace_sdk.egg-info/requires.txt` and `setup.py`, both **VERIFIED**).
`python_requires=">=3.8"`. Framework integrations (`langchain-core`,
`litellm`, `google-adk`, `openai-agents`, `opentelemetry-sdk`,
`elevenlabs`) are **not** SDK dependencies — each integration module does a
guarded `try/import` and raises a clear `ImportError` with a pip-install
hint if the framework isn't installed (verified in every module, e.g.
`langchain_handler.py:18-32`, `litellm_callback.py:216-221`).

README also documents a git-install fallback for pre-PyPI days (now moot
since 0.4.3 is live on PyPI):
```bash
pip install "git+https://github.com/Block-Convey/prismtrace.git#subdirectory=sdk/python"
```
This is the **only GitHub URL found anywhere in the package or docs**:
`github.com/Block-Convey/prismtrace`, subdirectory `sdk/python`. **VERIFIED**
(PyPI long_description / `PKG-INFO`). Not independently confirmed reachable
tonight (no `gh`/network check performed against it — treat as INFERRED that
it's public, since a `pip install git+https://...` command without an SSH
form or token implies a public repo).

## Package anatomy (wheel/sdist layout)

```
prismtrace/
  __init__.py           # public API surface — see exports below
  _config.py             # DEFAULT_HOST + resolve_host()
  _session.py            # ambient session contextvar: session(), current_session(),
                          #   bind_session(), unbind_session(), resolve_session()
  client.py               # PRISMtrace — manual/core client (trace_llm, trajectories, KB)
  langchain_handler.py    # PRISMtraceCallbackHandler
  langgraph_helper.py     # PRISMtraceLangGraphHandler, wrap_langgraph()
  google_adk.py           # PRISMtraceADKAdapter (BETA)
  litellm_callback.py     # install_litellm()
  claude_tracer.py        # ClaudeAgentTracer (raw Anthropic SDK tool-use loop)
  openai_agents.py        # PRISMtraceTracingProcessor, install_openai_agents() (PREVIEW)
  elevenlabs_voice.py      # PRISMtraceVoiceTracer, install_elevenlabs_voice()
  otel.py                  # PRISMtraceInstrumentor, PRISMtraceSpanExporter
  verify.py                 # `python -m prismtrace.verify` CLI
tests/                      # 12 test files, useful as executable spec (see below)
setup.py / setup.cfg
README.md                   # the fullest and most reliable source of examples
```

Public exports from `prismtrace/__init__.py` (**VERIFIED**, full file read):

```python
__version__ = "0.4.3"
__all__ = [
    "PRISMtrace",
    "session", "current_session", "bind_session", "unbind_session", "resolve_session",
    "PRISMtraceCallbackHandler",           # LangChain — Supported
    "ClaudeAgentTracer",                   # Anthropic direct — Supported
    "PRISMtraceLangGraphHandler", "wrap_langgraph",  # LangGraph — Supported
    "PRISMtraceADKAdapter",                # Google ADK — Beta
    "install_litellm",                     # LiteLLM — Supported (Universal Gateway)
    "PRISMtraceTracingProcessor", "install_openai_agents",  # OpenAI Agents SDK — Preview
    "PRISMtraceVoiceTracer", "install_elevenlabs_voice",     # ElevenLabs — Supported
    "PRISMtraceInstrumentor", "PRISMtraceSpanExporter",       # OpenTelemetry
]
```

Status labels ("Supported" / "Beta" / "Preview") are the SDK's own, taken
verbatim from module docstrings and the `__init__.py` comments — this is the
most reliable maturity signal available.

---

## 1. Core manual client — `prismtrace.PRISMtrace` (`client.py`)

```python
from prismtrace import PRISMtrace

pt = PRISMtrace(
    api_key="pt-sk-your-key",
    host="https://api.prism.blockconvey.com",   # or your PRISMTRACE_HOST
    project_id="your-project-id",
    timeout=10,                                    # seconds, default 10
)
```

Constructor signature (**VERIFIED**, `client.py:43-49`):
```python
def __init__(self, api_key: str, host: str, project_id: str, timeout: int = 10)
```
Note: unlike every other handler, `PRISMtrace.__init__` does **not**
fall back to env vars for `api_key`/`project_id` — `host` and `project_id`
are plain required positional/keyword args here with no `os.getenv` fallback
inside `client.py` itself (contrast with `PRISMtraceCallbackHandler`, which
does read env vars when args are omitted). Pass them explicitly.

### `trace_llm()` — one manual LLM call

```python
def trace_llm(
    self, model: str, input_messages: list, output: str, latency_ms: int,
    token_count_input: int = 0, token_count_output: int = 0,
    trace_id: Optional[str] = None, agent_id: Optional[str] = None,
    agent_name: Optional[str] = None, session_id: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> None
```
**VERIFIED**, `client.py:73-133`. Fires a background **non-daemon thread**
per call that POSTs to `/api/traces` (fire-and-forget from the caller's
point of view — see Async/threading section below). `agent_id` is the
*stable* identity used for guardrail/alert scoping — changing it re-identifies
the agent to the platform (explicit warning in the docstring). `session_id`
resolution: explicit arg → `metadata["session_id"]` → ambient session
(`prismtrace.session(...)`) → nothing (field omitted).

```python
@pt.trace()          # decorator form
def ask_bot(question):
    ...
    return "answer"
```
**VERIFIED**, `client.py:174-190`. Wraps a plain function, timing it and
posting `input_messages=[{"role":"user","content":str(args)}]`,
`output_message=str(result)` — crude, string-coerces everything. Fine for a
demo, not for structured tool-call tracing.

### `submit_trajectory()` — the trajectory-evaluation entry point

```python
def submit_trajectory(
    self, steps: list[dict], *, agent_name: str = "default-agent",
    agent_id: Optional[str] = None, conversation_id: Optional[str] = None,
    request_id: Optional[str] = None, model: Optional[str] = None,
    final_status: str = "success", async_send: bool = False,
) -> Optional[dict]
```
**VERIFIED**, `client.py:196-254`. POSTs to `/api/trajectories`. Each step
dict (per the README and code comments):
```python
{
    "step_type": "reasoning" | "tool_call" | "final_answer" | ...,
    "label": "short description",
    "output_summary": "what this step produced",     # optional but recommended
    "tool_name": "...",                                 # required when step_type == "tool_call"
    "input_summary": "...",                              # optional
    "duration_ms": 200,                                   # optional
    "token_count": 150,                                    # optional
    "status": "success" | "error",                          # default "success"
}
```
`conversation_id` resolves through the same ambient-session machinery
(`resolve_session`), so a trajectory submitted inside a
`with prismtrace.session(...)` block groups under that id automatically.
`agent_id` falls back to `agent_name` if omitted — **but the code comment
warns this makes the display NAME the platform identity**: renaming the
agent later creates what the platform treats as a new agent and detaches
every rule scoped to the old name. Pass a real, stable `agent_id`.

Returns `{"id": ..., "step_count": ..., "created_at": ...}` on success (per
README), or `None` on failure (never raises — see fail-open policy below).
`async_send=True` fires it on a background thread like `trace_llm`, instead
of blocking.

Companion read/write methods (**VERIFIED**, `client.py:301-314`):
```python
pt.get_trajectory(trajectory_id) -> Optional[dict]                 # GET  /api/trajectories/{id}
pt.get_trajectory_evaluation(trajectory_id) -> Optional[dict]      # GET  /api/trajectories/{id}/evaluation
pt.retrigger_evaluation(trajectory_id) -> Optional[dict]           # POST /api/trajectories/{id}/evaluate?project_id=...
```
This is the **only re-evaluation trigger found anywhere in the SDK** — useful
if you change your evaluator config and want to re-score an already-submitted
run without resubmitting the trajectory.

### Knowledge base methods

```python
pt.kb_upload(filename, content, *, agent_id=None, description=None, content_type="text/plain") -> Optional[dict]
pt.kb_search(query, *, agent_id=None, limit=5) -> list[dict]
pt.kb_list_documents(agent_id=None) -> list[dict]
pt.kb_delete_document(doc_id) -> bool
```
**VERIFIED**, `client.py:320-395`. Hit `POST /api/knowledge-base/documents`
(multipart file upload), `POST /api/knowledge-base/search`,
`GET /api/knowledge-base/documents`, `DELETE /api/knowledge-base/documents/{id}`.
Out of scope for this brief's core ask (tool-call tracing), but noted since
it's a real, working feature — not evaluator-related.

### Lifecycle

```python
pt.flush(timeout: float = 2.0)   # waits for pending background POST threads (join with timeout)
pt.close()                        # flush() then closes the httpx connection pool; idempotent
with PRISMtrace(...) as pt: ...   # context manager calls close() on exit
```
**VERIFIED**, `client.py:256-299`. An `atexit` hook flushes every live
`PRISMtrace` instance automatically (via a `weakref.WeakSet`, so it doesn't
keep instances alive) — but relying on atexit in a long-running server
process (FastAPI) is the wrong pattern; call `flush()`/`close()` on shutdown
explicitly (see file 03).

---

## 2. LangChain — `PRISMtraceCallbackHandler` (`langchain_handler.py`)

```python
from prismtrace import PRISMtraceCallbackHandler
from langchain_anthropic import ChatAnthropic

handler = PRISMtraceCallbackHandler(
    api_key=None,          # falls back to PRISMTRACE_API_KEY env var
    project_id=None,       # falls back to PRISMTRACE_PROJECT_ID
    endpoint=None,         # alias for host=
    host=None,             # falls back to PRISMTRACE_HOST / PRISMTRACE_ENDPOINT / DEFAULT_HOST
    session_id=None,       # explicit session id; ambient session used if omitted
    agent_name=None,       # stamped into span/run metadata
    source="langchain",
    timeout=10,
)
llm = ChatAnthropic(model="claude-sonnet-4-5-20250514", callbacks=[handler])
```
Constructor: `client.py`... actually `langchain_handler.py:125-135`
**VERIFIED**. Raises `ValueError` at construction if neither
`api_key`/`PRISMTRACE_API_KEY` nor `project_id`/`PRISMTRACE_PROJECT_ID` are
available — fails fast, not silently.

**Concurrency/correctness properties, all directly verified from the source
and pinned by tests** (`tests/test_handler_concurrency.py`,
`tests/test_langchain_agent_spans.py`):

- **One handler is safe to share across concurrent runs.** Per-run state
  (`_RunState`: trace_id, span buffer, open-span map, chain depth) is keyed
  by the LangChain *root run id*, not stored as flat handler attributes. A
  prior bug (documented in the code comments as the reason this rework
  exists) had two concurrent requests share one `depth` counter and
  interleave spans into a single trace under the wrong `trace_id`. Fixed as
  of 0.4.x. **VERIFIED** — this is exactly what
  `test_two_concurrent_runs_produce_two_traces` and
  `test_concurrent_runs_keep_their_own_ambient_sessions` assert against a
  real `langchain_core` install with two threads racing.
- **14 callback hooks implemented**: `on_chain_start/end/error`,
  `on_llm_start/end/error`, `on_chat_model_start/end/error`,
  `on_tool_start/end/error`, `on_agent_action/finish`,
  `on_retriever_start/end`. Every LangChain **tool call** shows up as a span
  with `span_type="tool"`, `name=<tool name>`, `input_text` = the tool's
  raw input string, `output_text` = the tool's raw return value string
  (`on_tool_start`/`on_tool_end`, `langchain_handler.py:506-524`).
- **AgentExecutor structure is preserved correctly** (this was a real,
  documented, now-fixed bug — ADR-0147 / KAN-48 per code comments): the
  chain span (`span_type="chain"`), each `agent:{tool_name}` action span
  (`span_type="agent"`), and each tool-call span (`span_type="tool"`) are
  all emitted with correct `parent_span_id` pointing at the chain span, not
  overwriting one another. Verified directly by
  `tests/test_langchain_agent_spans.py::test_an_agent_executor_run_keeps_its_root_span`.
  This matters directly for the hackathon agent: `open_claim`,
  `stage_dispatch`, `cancel_dispatch`, `update_claim` tool calls made
  through a LangChain `AgentExecutor` will each land as their own
  `span_type="tool"` row, nested under the correct agent/chain spans.
- **Ambient session precedence**: explicit `session_id` constructor arg >
  ambient `with prismtrace.session(...)` > handler's own generated uuid.
  Session is read **when a run starts**, not when the handler is
  constructed or when it flushes — so one long-lived handler built at
  import time still correctly groups whatever session is open around each
  call (verified, `_session.py` docstring + `test_session_ambient.py`).
- **Flush semantics**: `handler.flush()` sends every buffered run's spans to
  `POST /api/spans/ingest` and returns `True` only if at least one run had
  spans and the POST succeeded (2xx). A mid-run `flush()` force-closes any
  still-open spans (stamps `end_time`, appends to the buffer) — the chain
  can still legitimately end afterward, and the run bookkeeping is designed
  to unwind cleanly either way
  (`test_a_mid_run_flush_does_not_strand_the_run`).
- **No state leak across runs**: after 25 sequential chain invocations,
  `handler._runs == {}` — completed runs are actively discarded, not
  accumulated (`test_repeated_runs_do_not_accumulate_state`). Safe to keep
  one handler alive for the life of a FastAPI process.
- **`close()` flushes first, then closes the httpx pool; idempotent; also a
  context manager.** Every handler opens its own `httpx.Client` in its
  constructor — the SDK's own test suite (`test_handler_lifecycle.py`)
  exists specifically because their own generated onboarding guidance used
  to tell customers to build one handler per conversation and never close
  it, leaking one connection pool per conversation. **Build one handler per
  process, not per request/conversation, and close it on shutdown.**

Span payload shape POSTed to `/api/spans/ingest` — see file 02 for the full
schema; the fields set per-span here are: `span_id`, `parent_span_id`,
`name`, `span_type` (`chain`/`llm`/`tool`/`agent`/`retrieval`), `input_text`
(capped 10,000 chars), `output_text` (capped 10,000 chars), `metadata`,
`start_time`/`end_time` (ISO8601 UTC), `duration_ms`, `status`
(`ok`/`error`), `error_message`, `token_count_input`/`output`, `cost_usd`,
`model`. **VERIFIED**, `langchain_handler.py:308-337`.

---

## 3. LangGraph — `PRISMtraceLangGraphHandler` + `wrap_langgraph()` (`langgraph_helper.py`)

```python
from prismtrace import PRISMtraceLangGraphHandler, wrap_langgraph

handler = PRISMtraceLangGraphHandler(
    api_key="pt-sk-...", project_id="your-project-id",
    host="https://api.prism.blockconvey.com", agent_name="support-graph",
)
graph = wrap_langgraph(compiled_graph, handler)

with prismtrace.session("conversation-1"):
    graph.invoke({"messages": [("user", "hello")]})
```
**VERIFIED**, full file read. `PRISMtraceLangGraphHandler` is a thin
**subclass of `PRISMtraceCallbackHandler`** — identical 14 callback hooks,
identical flush path, identical concurrency guarantees described above. Its
only behavior change: every span name gets a `[langgraph]` prefix so the
backend's "architecture extractor" renders the run as framework=langgraph
instead of generic langchain (`_FRAMEWORK_TAG = "[langgraph]"`,
`langgraph_helper.py:38`, do-not-rename comment tied to a specific backend
file).

`wrap_graph()` / `wrap_langgraph()` monkey-patches `invoke`, `ainvoke`,
`stream`, `astream` on the compiled graph object so the handler is
auto-injected into `config={"callbacks": [...]}` on every call — existing
callbacks the caller passes are preserved, not replaced. Idempotent
(re-wrapping detects the `__prismtrace_wrapped__` marker and skips). Note a
documented, fixed bug in the source comments: `Pregel.invoke` forwards
`config` *positionally* into `.stream()` which is *also* patched, so the
wrapper must write the injected config back into whichever slot
(positional vs. keyword) it actually arrived through, or you get
`TypeError: Pregel.stream() got multiple values for argument 'config'`.
Already fixed in 0.4.3; a landmine if a hackathon team try to hand-roll
their own monkey-patch instead of using `wrap_langgraph`.

---

## 4. Google ADK — `PRISMtraceADKAdapter` (`google_adk.py`) — BETA

```python
from prismtrace import PRISMtraceADKAdapter
from google.adk.agents import LlmAgent

adapter = PRISMtraceADKAdapter(
    api_key="pt-sk-...", project_id="your-project-id",
    agent_name="my-adk-agent", endpoint=None, session_id=None, timeout=10,
)

agent = LlmAgent(
    name="loan_assistant", model="gemini-3.6-flash",
    instruction="...", tools=[lookup_rate],
    before_model_callback=adapter.before_model,
    after_model_callback=adapter.after_model,
    before_tool_callback=adapter.before_tool,
    after_tool_callback=adapter.after_tool,
    before_agent_callback=adapter.before_agent,
    after_agent_callback=adapter.after_agent,
)
```
**VERIFIED**, full file read (914 lines — the largest and most defensively
written module in the SDK). Key points relevant to a tool-calling agent:

- **Tool calls require wiring `before_tool_callback`/`after_tool_callback`
  explicitly.** If only `after_tool` is wired, every tool trace gets
  `latency_ms=0` and `metadata.tool_latency_unavailable=True`
  (`google_adk.py:14-16, 383-455`). Wire both for real timing.
- **ADK does not deliver model or tool errors through its own callbacks at
  all.** You must wrap your own model/tool calls in `try/except` and call
  `adapter.record_model_error(exc, callback_context=ctx)`,
  `adapter.record_tool_error(exc, callback_context=ctx, tool_name=...)`, or
  `adapter.record_runner_error(exc)` before re-raising. Each posts a trace
  with `status="error"` (via `metadata["status"]="error"`) plus
  `error_type` (exception class name) and a **secret-scrubbed**
  `error_message`. **VERIFIED**, `google_adk.py:461-597`.
- **Secret scrubbing is real and specific**: a regex table
  (`_SECRET_PATTERNS`, `google_adk.py:116-149`) redacts `pt-sk-...`,
  OpenAI-style `sk-...`/`sk-proj-...`, Anthropic `sk-ant-...`, Google
  `AIza...` keys, `Authorization: Bearer ...`, `x-api-key: ...`, and
  generic `api_key=...` patterns, applied to any error string before it's
  POSTed, length-capped at 4000 chars. This is the **only place in the
  whole SDK doing content redaction** — everywhere else, whatever you pass
  as `input_text`/`output_message` goes to the server verbatim (the SDK
  does **not** scrub PII/PAN/Aadhaar from your conversation content — see
  the caveat in file 03).
- **Sub-agent hierarchy metadata** is stamped on every trace:
  `agent_name`, `agent_id`, `parent_agent_id`, `agent_path` (root→leaf list),
  `root_agent_name`, `node_id`, `parent_node_id`, `invocation_id`,
  `step_order`, `adk_event_type` (`model_call`/`tool_call`/`model_error`/
  `tool_error`/`runner_error`). Multi-agent handoffs are reconstructable
  server-side from this metadata even without nested spans.
- Posts to `POST /api/traces` (the simple trace endpoint, not
  `/api/spans/ingest`) — **no new backend endpoints**, per the module
  docstring.
- Thread-safety: ADK runs model calls under asyncio but tool calls in a
  threadpool; a single `threading.Lock` guards the adapter's internal
  pending-pairing dict and step counters because both paths can race
  (`google_adk.py:236`).

---

## 5. LiteLLM — `install_litellm()` (`litellm_callback.py`) — the multi-provider gateway path

```python
import litellm
from prismtrace import install_litellm

install_litellm(
    api_key="pt-sk-...", project_id="your-project-id",
    endpoint=None,                       # resolves via resolve_host()
    agent_name="litellm-gateway",
    session_id_factory=None,             # callable(kwargs)->str; default = ambient session or per-call uuid
    timeout=10,
)

response = litellm.completion(
    model="gpt-4o",   # any of LiteLLM's ~100 supported providers
    messages=[{"role": "user", "content": "hello"}],
)
```
**VERIFIED**, full file read. This is the module docstring's own framing —
LiteLLM is "a unified router/proxy for ~100 LLM providers (OpenAI,
Anthropic, Bedrock, Azure, Gemini, Cohere, Mistral, **Ollama**, etc.)"
(`litellm_callback.py:3-6`). **This is the actually-supported path for
Groq/OpenRouter/vLLM/Ollama/local models** — LiteLLM itself natively routes
to those, and `install_litellm()` traces every completion regardless of
underlying provider, in one call. (The zero-code *proxy* at
`/proxy/openai/v1` only forwards to the real OpenAI API — see file 02 for
that distinction; it is **not** a universal gateway.)

Mechanism: registers a single callable on LiteLLM's module-level
`litellm.success_callback` and `litellm.failure_callback` lists (LiteLLM's
documented, "production-blessed" tracing extension point per the docstring).
`install()` is idempotent — calling it twice replaces the previous
forwarder rather than double-registering
(`_filter()` strips prior `_LiteLLMTraceForwarder` instances first,
`litellm_callback.py:232-240`).

Payload posted to `POST /api/traces` per completion:
- `model`: tagged as `"litellm:{underlying_model}"` so the backend's
  architecture extractor detects `framework=litellm` while preserving the
  real model id.
- `session_id`: `kwargs["metadata"]["session_id"]` if the caller set one
  via LiteLLM's own `metadata=` channel, else the `session_id_factory`
  (default: ambient `prismtrace.session()` if open, else a fresh uuid per
  completion — **not** shared across a multi-call agent run unless you open
  a session or pass metadata explicitly).
- `metadata`: `{"framework":"litellm","agent_name":...,"agent_id":...,
  "source":"litellm-gateway","session_id":...,"underlying_provider_model":...,
  "error":...}`.
- Token counts read from `response.usage.prompt_tokens` /
  `.completion_tokens` (best-effort `_dig()` helper, returns 0 if absent).
- Latency computed from LiteLLM's own `start_time`/`end_time`, handling
  both `datetime` and epoch-float forms across LiteLLM versions.
- **Tool calls are not specially modeled here** — LiteLLM's callback gives
  you the raw request/response `kwargs`; if the response contains
  `tool_calls`, they are not extracted into separate spans by this
  integration. It posts one flat trace per `litellm.completion()` call. If
  your agent's tool-calling loop makes N model calls through LiteLLM, you
  get N traces, correlated by session_id (if you set one) but with no
  parent/child span structure. For structured tool-call spans, prefer
  `ClaudeAgentTracer` (Anthropic-only) or manual `/api/spans/ingest`.
- Fails open: wraps its own forwarding logic in try/except and prints a
  warning rather than raising — **tracing failure never breaks the LLM
  call** (a consistent policy across every module in this SDK).

---

## 6. Claude tool-use tracing — `ClaudeAgentTracer` (`claude_tracer.py`)

The **only integration in the SDK that natively builds a full agentic
tool-use loop with structured spans AND auto-submits a trajectory.**
Directly relevant as a reference implementation even if the hackathon
project doesn't use raw Anthropic SDK, because it shows exactly what
PRISM's trajectory/tool-call data model expects.

```python
import anthropic
from prismtrace.claude_tracer import ClaudeAgentTracer

client = anthropic.Anthropic()
tracer = ClaudeAgentTracer(
    anthropic_client=client, api_key="pt-sk-...", project_id="your-project-id",
    endpoint=None, agent_name="weather-agent", emit_trajectory=True,
    session_id=None, timeout=15,
)

tools = [{
    "name": "get_weather",
    "description": "Get the weather for a location",
    "input_schema": {"type": "object", "properties": {"location": {"type": "string"}}, "required": ["location"]},
}]

def execute_tool(name: str, input_data: dict) -> str:
    if name == "get_weather":
        return f"72F and sunny in {input_data['location']}"
    return "Unknown tool"

result = tracer.run(
    messages=[{"role": "user", "content": "What's the weather in SF?"}],
    tools=tools, system="You are a helpful assistant.",
    tool_executor=execute_tool,
    session_id=None,           # optional per-call override; else tracer.session_id; else ambient
)
# result = {"response": <Anthropic response>, "trace_id": ..., "trajectory_id": ...,
#           "iterations": N, "spans_count": N, "trajectory_steps": N}
```
**VERIFIED**, full file read (412 lines). `tracer.run()` drives the whole
loop internally (up to `max_iterations=10` default): calls the model, if
`response.stop_reason == "tool_use"` it invokes your `tool_executor(name,
input) -> str` for each `tool_use` block, appends `tool_result` blocks back
into the conversation, and repeats. Emits:
- A `chain`-type **root span** (`span_type="chain"`, `name="claude_agent_run"`).
- One `llm`-type span per model call (`name=f"llm:{model}"`).
- One `tool`-type span per tool call (`name=<tool name>`, `input_text` =
  `json.dumps(tool.input)`, `output_text` = the tool's return string,
  `status="error"` + `error_message` if `tool_executor` raised).
- One `agent`-type span per iteration summarizing which tools fired.
All POSTed together to `POST /api/spans/ingest`.
- **Also auto-submits a trajectory** to `POST /api/trajectories` with step
  types `reasoning`/`tool_call`/`final_answer` mirroring the spans — this is
  what feeds PRISM's trajectory evaluation (goal adherence / tool
  compliance / efficiency / safety scoring per the README). Both the spans
  POST and the trajectory POST carry the **same resolved session_id**
  (`conversation_id`) — a documented fix (code comment references a
  regression where the trajectory carried a session but the spans POST
  didn't, so the same run split across two disconnected views).

Auto-instrument mode (wraps `client.messages.create` transparently, no
explicit loop):
```python
tracer.instrument_client()
response = client.messages.create(model=..., max_tokens=1024, messages=[...])
# every call now auto-traced; tool_use blocks in the response become
# separate tool spans, but no tool EXECUTION is captured (this mode never
# calls a tool_executor — it only observes what the model asked for, not
# what happened when you ran it)
```
**Anthropic-only.** No equivalent tracer exists in the SDK for OpenAI or
Gemini tool-use loops driven directly against their SDKs (i.e. without
LangChain/LiteLLM/OpenAI-Agents in between).

---

## 7. OpenAI Agents SDK — `install_openai_agents()` (`openai_agents.py`) — **PREVIEW, with known structural gaps**

```python
from agents import Agent, Runner
from prismtrace import install_openai_agents

install_openai_agents(
    api_key="pt-sk-...", project_id="your-project-id",
    endpoint=None, agent_name="openai-agents-agent", timeout=10,
)

agent = Agent(name="my-agent", instructions="...")
result = await Runner.run(agent, "hello")
```
**VERIFIED**, full file read. Implements the OpenAI Agents SDK's
`TracingProcessor` protocol (`on_trace_start`, `on_trace_end`,
`on_span_start`, `on_span_end`, `shutdown`, `force_flush`), registered via
`agents.tracing.add_trace_processor()` (falls back to
`set_trace_processors()` if that's absent; raises `RuntimeError` with a
clear message if the installed `openai-agents` version exposes neither).

**Explicitly documented, self-acknowledged limitations (why this is
labeled PREVIEW and not Supported)** — straight from the module docstring:

1. **Span hierarchy is flattened.** Each Agents-SDK span becomes its own
   independent `POST /api/traces` call rather than a nested span tree on
   one parent trace. Handoff structure is only reconstructable via shared
   `session_id`, not as parent/child rows.
2. **Agent-boundary spans are dropped entirely** (not just flattened) —
   `_ENCLOSING_SPAN_KINDS = {"agent", "AgentSpanData"}` are never forwarded
   at all. This is deliberate and tested
   (`tests/test_openai_agents_enclosing_spans.py`): an agent span's
   duration *is* the sum of its children's durations, so forwarding both
   double-counted total run time (documented as ADR-0137, and the exact
   same reasoning `google_adk.py` uses to skip agent-boundary traces). The
   fix: only leaf work (`generation`, `function`/tool-call, `handoff`)
   becomes a trace; the run still groups correctly via shared
   `session_id`.
3. **Streaming chunks are not aggregated** — only the final response text
   is captured at span end.
4. **Tool call results arrive as separate traces tagged `tool_call`**, not
   nested under the generation span that produced the call.

Session mapping: one Agents-SDK top-level trace (`Runner.run()`) maps 1:1 to
one PRISMtrace `session_id` — the ambient session
(`prismtrace.session(...)`), if open, wins over a generated uuid. All child
spans within that Agents-SDK trace inherit the same `session_id`.

Payload per forwarded span: `model` tagged as
`"openai-agents:{span_kind}:{model}"`, `metadata.framework="openai_agents"`,
plus `agents_span_kind`, `agents_trace_id`, `agents_span_id` for
cross-referencing back to the Agents SDK's own trace viewer if you use both.

**Bottom line for the hackathon:** if the team's FastAPI tool-calling agent
uses the OpenAI Agents SDK, tool calls DO show up (as `function`-kind spans
carrying `input`/`output`), but the run's nested structure is flatter than
what LangChain or `ClaudeAgentTracer` produce, and total-duration rollups
are more trustworthy post-fix (agent-boundary double counting is already
patched) — but there's no trajectory auto-submission here the way there is
for `ClaudeAgentTracer`, so no automatic goal/tool-compliance PRISM scoring
unless you also call `pt.submit_trajectory()` yourself alongside it.

---

## 8. ElevenLabs voice — `PRISMtraceVoiceTracer` (`elevenlabs_voice.py`)

Two independent ingestion paths — **use exactly one per agent, never both**
(explicit warning in the docstring; double-ingests the same call under two
ids otherwise):

**A. Post-call webhook (no code)** — configure in the ElevenLabs dashboard,
subscribe to `post_call_transcription` only (not `post_call_audio` — PRISM
rejects audio events), store the signing secret on the PRISM connector.

**B. Live tracing during the call:**
```python
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from prismtrace import PRISMtraceVoiceTracer

tracer = PRISMtraceVoiceTracer(
    api_key="pt-sk-...", project_id="your-project-id",
    agent_name="Support line", agent_id=None, conversation_id=None,
    timeout=10, on_error=None,
)
conversation = Conversation(
    ElevenLabs(api_key=ELEVENLABS_API_KEY), AGENT_ID,
    requires_auth=True, audio_interface=DefaultAudioInterface(),
    **tracer.callbacks(),
)
conversation.start_session()
conversation_id = conversation.wait_for_session_end()
tracer.finalize(conversation_id)
```
**VERIFIED**, full file read. `tracer.callbacks()` returns exactly three
kwargs wired to ElevenLabs' own documented `Conversation` callback params:
`callback_user_transcript`, `callback_agent_response`,
`callback_agent_response_correction` (the last one handles barge-in —
records only the *corrected* text the caller actually heard, discards the
superseded draft). Each turn is POSTed individually to
`POST /api/voice/turns` (**not** `/api/traces` or `/api/spans/ingest` — a
distinct endpoint) with `{project_id, conversation_id, turns:[{role,
message}], status, agent_id, agent_name, start_index}`.

**Server-side PII scrubbing is real but explicitly not the SDK's job**:
"Transcripts are scrubbed for PII on the server before storage, and audio
is never sent to or stored by PRISM" (module docstring, and repeated in the
class docstring). This module is deliberately "a thin HTTP client" — no
Presidio or similar runs client-side, so the scrubbing guarantee lives
entirely on PRISM's backend, not in anything under your control. Relevant
to the team's PII-leakage test scenario: if using this path for the voice
leg, PII scrubbing is automatic; if you instead route the transcript
through `/api/traces` or a generic SDK handler, **no such scrubbing is
documented or implied** — that data reaches PRISM verbatim.

Thread-safety: a `threading.Lock` guards the turn-index counter since
ElevenLabs invokes callbacks from its own WebSocket thread
(`elevenlabs_voice.py:76-77, 196-198`).

`finalize()` POSTs a zero-turn batch with `status="done"` to seal the call,
and returns a mapping dict correlating PRISM's (possibly provisional)
`traced_conversation_id` with ElevenLabs' real `conversation_id` — needed
because ElevenLabs only returns its real conversation id when the session
ends, but turns need a stable grouping key from the very first callback.

---

## 9. OpenTelemetry — two distinct paths, and which one to actually use (`otel.py`)

**Path A — OTLP over HTTP directly, no SDK at all (RECOMMENDED for
FastAPI + any GenAI instrumentation library):**
```bash
OTEL_EXPORTER_OTLP_ENDPOINT=https://api.prism.blockconvey.com/api/otlp
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf     # or http/json — gRPC is NOT served
OTEL_EXPORTER_OTLP_HEADERS=X-PRISMtrace-Key=pt-sk-...
```
Point any standard OTel exporter (in any language) at this — no
`prismtrace-sdk` install needed. **Critical, repeated in both the README and
docs**: do **not** append `/v1/traces` — the OTLP spec appends the signal
path itself, so the value above resolves on its own to
`POST /api/otlp/v1/traces`. Setting `OTEL_EXPORTER_OTLP_PROTOCOL` explicitly
matters — an exporter defaulting to gRPC (the Java SDK does) fails silently
against this endpoint. **VERIFIED**, README + `otel.py` module docstring +
`https://blockconvey.com/docs/integrations`.

Reads standard OpenTelemetry GenAI semantic-convention attributes with
graceful fallback to superseded spellings (table, `otel.py:58-73` and the
README): `gen_ai.response.model`/`gen_ai.request.model`, `gen_ai.usage.
{input,output}_tokens` (falls back to `.prompt_tokens`/`.completion_tokens`),
`gen_ai.input.messages`/`gen_ai.prompt`, `gen_ai.output.messages`/
`gen_ai.completion`, `gen_ai.conversation.id`/`session.id` for session,
`gen_ai.operation.name` for span type (`chat`/`text_completion`/
`generate_content`→`llm`, `embeddings`→`retrieval`, `execute_tool`→`tool`,
`invoke_agent`/`create_agent`→`agent`). **Also handles indexed/flattened
message attributes** (`gen_ai.prompt.0.role`, `gen_ai.prompt.0.content` —
openllmetry-style — and `llm.input_messages.0.message.role` —
OpenInference-style), which is exactly what popular auto-instrumentation
libraries emit for tool-calling frameworks. A `prismtrace.*`-prefixed
attribute (`prismtrace.span_type`, `prismtrace.input`, `prismtrace.output`,
`prismtrace.model`, `prismtrace.session_id`, etc.) always overrides
whatever the semantic-convention reading produces, if you want manual
control on specific spans.

**Path B — `PRISMtraceInstrumentor`/`PRISMtraceSpanExporter` (in-process
shim, converts OTel spans to `/api/spans/ingest` calls without running an
exporter):**
```python
from prismtrace import PRISMtraceInstrumentor
instrumentor = PRISMtraceInstrumentor()
instrumentor.instrument(api_key="pt-sk-...", project_id="...", endpoint=None, session_id=None, timeout=10)
tracer = instrumentor.get_tracer("my-service")
with prismtrace.session("conversation-1"):
    with tracer.start_as_current_span("process_request"):
        ...
instrumentor.shutdown()
```
Requires `pip install opentelemetry-sdk opentelemetry-api` (not bundled).
The module's own docstring says plainly: **"this is usually NOT what you
want"** — reach for it only if already on this SDK and not wanting to run a
separate exporter/Collector; otherwise Path A is simpler and
language-agnostic. Session handling here needs a dedicated
`_AmbientSessionProcessor` span processor because a `BatchSpanProcessor`
exports on its own thread where the ambient-session contextvar doesn't
reach — the session has to be stamped onto the span *at start*, not read at
export time (`otel.py:331-357`, directly relevant gotcha if you ever build
something similar yourself).

---

## Async / threading / FastAPI-relevant gotchas (cross-cutting, all VERIFIED)

1. **Every "fire" call across the whole SDK is synchronous-blocking `httpx`,
   dispatched from a background `threading.Thread`, not `asyncio`.** There
   is no `async def` anywhere in the SDK and no `httpx.AsyncClient` usage.
   In a FastAPI async request handler, calling `handler.flush()`,
   `pt.trace_llm(...)`, or any of the `install_*` callback paths does not
   block the event loop for the fire step (background thread), but
   `flush()`/`close()` **do block** (via `thread.join(timeout)`) — call
   those from a sync context or `await asyncio.to_thread(handler.flush)` if
   calling from an async request handler and you need to guarantee delivery
   before responding.
2. **Fail-open is a hard, repeated design invariant**: every module wraps
   its POST calls in try/except and prints a warning to stdout/stderr
   rather than raising. Tracing failures **never** break the agent's actual
   response to the user. Good for production safety, bad for debugging
   silently-missing traces during the hackathon — **watch stderr for
   `PRISMtrace warning: ...` / `[prismtrace ...] forward failed: ...`
   lines** if traces aren't showing up in the dashboard.
3. **`timeout` defaults vary by handler** (all pinned by
   `tests/test_handler_timeout.py`): `PRISMtrace` core client, LangChain,
   ADK, OpenAI Agents, LiteLLM, OTel exporter, voice tracer = **10s**;
   `ClaudeAgentTracer` = **15s**. Test file's own docstring documents a real
   production incident: "a cold or redeploying backend routinely exceeds
   10s on its first request" (referenced as bug KAN-47, hit twice during
   their own staging verification on 2026-09-10) — **the SDK fails open, so
   a slow backend silently drops the batch with only a printed warning**.
   If the PRISM backend is cold when the hackathon starts (likely, given a
   student-facing shared multi-tenant service under load), consider passing
   a higher `timeout=` explicitly, especially for the first request of a
   session.
4. **Contextvars (the ambient `prismtrace.session(...)`) do NOT propagate
   across a plain `threading.Thread` or a process pool** — they do
   propagate into `asyncio` tasks. If the agent's tool execution happens in
   a thread pool executor (common for blocking DB/HTTP calls inside async
   FastAPI handlers), the session must be carried across by hand:
   ```python
   session_id = prismtrace.current_session()
   # ... hand off to the worker ...
   token = prismtrace.bind_session(session_id)
   try:
       run_tool(...)
   finally:
       prismtrace.unbind_session(token)
   ```
   **VERIFIED**, `_session.py` docstring + `test_a_thread_does_not_inherit_the_session`
   + the Google ADK adapter's own internal workaround for exactly this
   problem (`google_adk.py:230-232`, `_invocation_sessions` cache — ADK
   dispatches tool calls to a threadpool while model calls run in asyncio).
5. **`session_id` must be a non-empty string or `session(...)`/
   `bind_session(...)` raises `ValueError`** — an empty or whitespace-only
   id is deliberately rejected rather than silently treated as "no
   session" (`_session.py::_normalize`, verified by
   `test_an_empty_session_id_is_rejected`).
6. **Building a new handler per request/conversation leaks a connection
   pool per conversation** — this is explicitly called a past mistake in
   their own onboarding guidance (`test_handler_lifecycle.py` docstring:
   "Our own generated setup brief told customers to build the handler once
   per conversation, so following it literally leaked a connection pool per
   conversation"). **For a FastAPI app: construct each handler/tracer once
   at app startup (e.g., in a lifespan handler or module-level singleton),
   reuse it across requests, and call `.close()` on shutdown.** Session
   scoping across concurrent requests is handled correctly by the ambient
   session contextvar + per-run-id partitioning described above — you do
   **not** need one handler per conversation for correctness.
7. **`PRISMtraceCallbackHandler.trace_id` and `._spans` are still readable
   as properties for backward compatibility**, but now proxy into a
   reserved-key bucket (`_LEGACY_RUN_KEY`) rather than being real flat
   state — don't rely on `handler.trace_id` to mean "the trace id of the
   request I just made" in a concurrent app; it reflects a legacy
   single-run assumption.

---

## What is NOT in the SDK (scope boundaries, all NOT FOUND after reading every module)

- **No async/await API anywhere.** No `AsyncClient`, no `async def` methods.
- **No batching/queueing layer** — every trace/span POST is a single
  synchronous HTTP request per call (fired off a background thread); there
  is no local buffering-and-batch-flush-on-interval mechanism to reduce
  request volume beyond LangChain's natural per-run buffering.
- **No retry logic** on failed POSTs — a failed request is logged and
  dropped, not retried.
- **No custom-score or annotation push method** on `PRISMtrace` or any
  handler (see file 02 for the API-level confirmation of this gap and the
  `metadata` workaround).
- **No OpenAI- or Gemini-native tool-use tracer** equivalent to
  `ClaudeAgentTracer` — that pattern exists only for the raw Anthropic SDK.
- **No dataset/experiment/versioning class or method** in the SDK. Version
  tagging, if done at all, is a `metadata` convention you invent yourself
  (see file 03).
