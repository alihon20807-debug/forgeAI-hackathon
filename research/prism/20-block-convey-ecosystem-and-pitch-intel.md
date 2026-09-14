# Block Convey / PRISM Ecosystem Research

Scope: company, products, pricing, positioning/terminology/competitors, content & prior events, India insurance regulatory hooks, and pitch intelligence. Every claim labeled **VERIFIED** (source URL), **INFERRED**, or **NOT FOUND** / **NOT RESEARCHED**. Researched 2026-09-14.

---

## 1. Block Convey — Company & Products

### Company basics
- Block Convey is an AI governance / AI reliability company building **PRISM** (and a separate product **PRISMX**). **VERIFIED** (https://blockconvey.com, https://blockconvey.com/about)
- Founded 2023 (one source says 2022), HQ New York, NY, USA. ~6 employees. **VERIFIED** (search-derived from Crustdata/Tracxn profiles: https://profiles.crustdata.com/company/block-convey, https://tracxn.com/d/companies/block-convey/__FkenDXLpL6JhNy5qOXh-JpLh-uyYlJzK11Jr2Ecu6to)
- No confirmed India office/team found. **NOT FOUND** (same Crustdata/Tracxn search summaries state team appears US-based)
- Funding: last round described as an "accelerator round," ~$120,000 total raised, angel-backed/privately held; one Tracxn snippet called it "unfunded." Numbers are inconsistent across sources — treat as **INFERRED / low confidence**, not solid enough to quote to judges. (Crunchbase org page https://www.crunchbase.com/organization/money-convey — full page blocked/403 on direct fetch; PitchBook page https://pitchbook.com/profiles/company/517457-89 blocked/403)
- Accelerator: **Fintech Sandbox** — Block Convey is listed as a Fintech Sandbox startup. **VERIFIED** (https://www.fintechsandbox.org/startup/block-convey/). Fintech Sandbox supports early-stage fintech companies with data access/infrastructure/community; page did not give enrollment dates or selection rationale.

### Leadership / team
- **Arun Prasad (Arun P.)** — Founder & CEO. Based in New York; attended NYU. **VERIFIED** (https://www.crunchbase.com/person/arun-prasad-eb04, https://www.linkedin.com/in/arun-p-0b037688/, https://blockconvey.com/about)
- **Aishwarya Birla** — CTO. **VERIFIED** (https://blockconvey.com/about; corroborated via search of Crustdata/RocketReach profiles)
- **Pavan Marisetti** — COO. **VERIFIED** (same sources)
- The /about page itself states "Full bios are being finalised" — i.e., Block Convey has not published detailed bios. **VERIFIED** (https://blockconvey.com/about)
- Public appearances mentioned on /about: **NYU AI Conference, 2024** and **Venture Studios Summit, 2024**. **VERIFIED** (https://blockconvey.com/about)
- No named judges/engineers for ForgeAI confirmed. **NOT RESEARCHED** (would need the Gravitas event page's judge list, not fetched in this pass).

### Origin story — important for pitch color
- A GitHub repo **finos-labs/dtcc-i-h-2025-prism** documents a project called "PRISM" built for the **DTCC AI Hackathon 2025** (June 9–12, 2025, "leverage AI and ML technologies to address critical challenges in financial markets"). Team: **Kritin Madhavan, Arun Prasad, Shiv Mohith S, Adithyah Nair**. Description: "an AI-powered solution designed to enhance risk management and governance in financial markets," with real-time drift analysis, bias/fairness scoring, red-team security testing, SHAP/LIME explainability, audit reporting. **VERIFIED** (https://github.com/finos-labs/dtcc-i-h-2025-prism)
- The same three additional names (Adithyah Nair, Kritin Madhavan) plus Arun Prasad are listed as **Product Hunt "Makers"** for "PRISM by Block Convey." **VERIFIED** (https://www.producthunt.com/products/prism-by-block-convey)
- **INFERRED**: PRISM the product literally began as this DTCC/FINOS hackathon submission by (part of) the eventual Block Convey founding team, then became a company. This is a strong, concrete, citable talking point: *"PRISM itself was born at a hackathon — you're in exactly the position their own founders were."*

### Product history / evolution (VERIFIED via Product Hunt + current site)
- **Early positioning (Product Hunt launch, 2025, 128 upvotes, #6 Day Rank)**: "PRISM by Block Convey: Monitor models, explain decisions, & future-proof models." Described as "an open, plug-and-play platform... for AI startups and developers... to conduct model audits, bias checks, and generate explainability reports," turning "complex model evaluations into simple, blood-test-style readiness reports." Tagline: "making AI model evaluation stupid simple, in minutes, not weeks." **VERIFIED** (https://www.producthunt.com/products/prism-by-block-convey)
- **Current positioning (live site, Sept 2026)**: PRISM is now an **AI agent / LLM-application observability, testing and remediation platform** — traces, sessions, synthetic scenarios, evaluators, guardrails, agent intelligence, end-user intelligence, AI remediation. **VERIFIED** (https://blockconvey.com/prism)
- **INFERRED**: clear product evolution from "model audits / bias & fairness / explainability reports for compliance" (2025 launch) → "production AI agent observability + reliability platform, still compliance/regulator-flavored" (current). This matters for the pitch: judges likely still care deeply about the *governance/compliance* roots even though the product surface is now "observability."
- Company self-description on /about: began "with AI governance and observability" before building PRISM as the comprehensive testing/improvement platform. **VERIFIED** (https://blockconvey.com/about)

### Two products: PRISM vs PRISMX vs "PRISMtrace"
- **PRISM** = the main platform: captures every LLM/agent call, scores quality, traces, evaluates, and (per third-party summaries) "exports regulator-ready audit packs." **VERIFIED** core (https://blockconvey.com/prism); "regulator-ready audit packs" phrase is from search-engine-cached summaries of Block Convey copy, not independently re-confirmed by direct fetch — treat as **INFERRED/likely-accurate**.
- **PRISMtrace** = NOT a separate product; it is the **brand name of PRISM's tracing/SDK layer and subdomain**. The app lives at `prism.blockconvey.com`; the Python package is `prismtrace-sdk` (import name `prismtrace`); docs subpath is `/prismtrace/docs`. Class names in the SDK use the `PRISMtrace` prefix (e.g., `PRISMtraceCallbackHandler`, `PRISMtraceVoiceTracer`). **VERIFIED** (https://blockconvey.com/prismtrace/docs, https://blockconvey.com/docs)
- **PRISMX** = a **distinct, separate product**: a **browser-based DLP (data-loss-prevention) layer** that stops PII, PHI, and credentials/source code from leaving the endpoint when employees use ChatGPT, Claude, Gemini, and Copilot. Deployed as a managed browser extension via Intune / Google Admin / Jamf; intercepts paste-and-prompt traffic. Every release is mapped to EU AI Act, SOX, GDPR, DORA, PCI DSS, NIST AI RMF, HIPAA obligations. **VERIFIED via search-engine-indexed page summaries** (query results describing https://blockconvey.com/solutions with cached page title "Solutions — PRISM and PRISMX by Audience and Role," and third-party company-profile text). **CAVEAT**: direct WebFetch of https://blockconvey.com/solutions and https://blockconvey.com/prismx on 2026-09-14 did **not** show PRISMX content (either 404 or PRISMX absent from the rendered page) — the live site may have since removed, hidden, or renamed PRISMX, or it may require JS rendering not captured by the fetch tool. **Flag this as current-state-uncertain**: don't assume PRISMX is prominently sold today; mention it only as "Block Convey also has/had a second product, PRISMX, for browser-level PII/PHI DLP" without over-claiming its current availability.
- **Practical implication for the team**: for the hackathon, the relevant product is **PRISM** (traces/evaluators/guardrails/agent intelligence), reached at `prism.blockconvey.com`, via the `prismtrace-sdk` / PRISMtrace tracer classes. PRISMX (DLP-in-the-browser) is not directly relevant to a voice-agent FNOL demo.

### PRISM's six connected capabilities (core vocabulary — VERIFIED, https://blockconvey.com/prism)
1. **Synthetic Scenarios** (Beta) — "Tell PRISM what the AI should do. It creates realistic users, changing requests, missing details, tool problems, and edge cases."
2. **AI Observability** — inspect traces, sessions, agent runs, retrieval, tools, timing, retries, scores, outcomes in one view.
3. **Agent Intelligence** — pattern recognition across runs: user intent, conversation quality, recurring failures, knowledge gaps.
4. **Evaluators** (Builder tier+) — reusable evaluation criteria; score selected runs; review failed examples.
5. **AI Remediation** — combines user goal + actual outcome + trace data + probable cause → guided fix.
6. **End User Intelligence** (Growth tier+) — user-level patterns, friction points, unresolved goals.

Additional confirmed terms: **Guardrails** (policy-compliance monitoring with configurable trigger rates; Monitor vs Enforce modes), **root-cause classification**, **reliability score** (composite metric across six weighted dimensions — exact dimensions not published), **100% production session coverage** (not sampling-based), **human approval required before changes deploy**, **monthly scoring reports with delta tracking**. **VERIFIED** (https://blockconvey.com/prism)

### Target audiences by role/solution page (VERIFIED, https://blockconvey.com/solutions, /solutions/*)
- **Builders** — "From working demo to real-user ready."
- **AI Agents** teams — tool-calling failures: "The tool returned 200. The task still failed." Failure types named: incorrect tool selection, state misalignment (e.g., intent="refund" when goal was "exchange"), failed handoffs, stale state, loops/retries.
- **Conversational AI** teams — multi-turn dialogue quality. Key line: **"Turn four is where conversations break"** — tests for "interruptions, corrections, vague requests, repeated questions, tone changes, and mid-conversation decisions." (Extremely close to the hackathon project's own scenario space — mid-sentence cancellations, corrections, tone.)
- **RAG Applications** — "Know whether retrieval or generation failed."
- **Enterprise/compliance-focused** — EU AI Act, NIST AI RMF, ISO 42001, HIPAA, and (separately, on /compliance) SR 11-7, NY DFS Part 500, NAIC Model Bulletin, CFPB/Reg B, GDPR, DORA, SOX, PCI DSS (see Section 5 below).
- No solution page or blog content mentions **voice agents, multilingual/code-mixed language, or insurance FNOL specifically** at the marketing-copy level — **NOT FOUND** on /solutions/conversational-ai or /solutions/ai-agents. However, **voice agent integration exists at the SDK/docs level** (see below) — the marketing site hasn't caught up to a capability the product already has. This is a gap the hackathon team can exploit rhetorically ("we're proving out a capability Block Convey's own docs support but their marketing hasn't showcased yet").

### Voice agent support — directly relevant, high-value finding
- PRISM docs list **Voice Agents** as one of the integration paths (alongside Python SDK, TypeScript/JS, OpenTelemetry, Zero-Code Proxy, Warehouses). **VERIFIED** (https://blockconvey.com/docs)
- Concretely documented for **ElevenLabs**: two options — (1) post-call webhook, no code; (2) live tracing via a class called **`PRISMtraceVoiceTracer`**. **VERIFIED** (https://blockconvey.com/prismtrace/docs)
- Explicit privacy claim: **"Transcripts are scrubbed for PII on the server before storage, and audio is never sent to or stored by PRISM."** **VERIFIED** (https://blockconvey.com/prismtrace/docs) — this is a strong, quotable phrase that validates the team's own PII-scrubbing safety layer as "exactly the kind of thing PRISM already expects voice-agent builders to care about."

### SDK / integration technical reference (cross-reference only — full API detail is other agents' scope)
- Python package: `prismtrace-sdk>=0.4.3`, import as `prismtrace`. **VERIFIED**
- Core endpoint: `POST /api/traces` (fields: `project_id`, `model`, `input_messages`, `output_message`, `latency_ms`; optional `session_id`, `agent_id`). **VERIFIED**
- Auth header: `X-PRISMtrace-Key` (NOT `Authorization: Bearer`). **VERIFIED**
- Credentials: `PRISMTRACE_HOST=https://prism.blockconvey.com`, `PRISMTRACE_PROJECT_ID` (UUID), `PRISMTRACE_API_KEY` (`pt-sk-...`, shown once). **VERIFIED**
- Framework handlers: `PRISMtraceCallbackHandler` (LangChain), `PRISMtraceLangGraphHandler` + `wrap_langgraph()` (LangGraph), `PRISMtraceADKAdapter` (Google ADK), `install_litellm()` (LiteLLM), `install_openai_agents()` (OpenAI Agents SDK). **VERIFIED** (https://blockconvey.com/prismtrace/docs)
- Zero-code proxy routes: `/proxy/anthropic`, `/proxy/openai/v1`, `/proxy/gemini`. OpenTelemetry OTLP endpoint at `/api/otlp` (also referenced as `/api/otlp/v1/traces`). **VERIFIED**
- Setup verification: `POST /api/setup-doctor/handshake` and `GET /api/setup-doctor` with `send_test_trace: true`. **VERIFIED**
- (Deep SDK/API integration mechanics are explicitly out of this agent's scope per the task brief — flagging only what's needed for company/product/pitch context.)

---

## 2. Pricing, Plans & Limits

(Source: https://blockconvey.com/pricing, cross-checked twice — **VERIFIED** unless noted)

| Plan | Price | Monthly credits | Positioning |
|---|---|---|---|
| **Free** | $0/mo | 100 credits | "Connect a real app and understand the first failure before you pay." Solo builders/small teams. |
| **Builder** | $20/mo | 500 credits | "Most popular." "Protect and evaluate production AI without losing the simplicity of Free." |
| **Growth** | $50/mo | 1,500 credits | "Operate AI across more users, workflows, and production history." Teams with real users, multiple projects. |
| **Managed** | $300/mo | 10,000 credits | Hands-on implementation support; teams wanting guided rollout. |
| **Enterprise** | Custom | Custom (defined in agreement) | Governance, security, regulated workflows. |

**All plans include**: Knowledge Base; every supported connector; Traces / Trace Detail / Sessions; Agent Runs / Scores / Metrics / Alerts; Agent Intelligence; root-cause investigation and remediation recommendations; Synthetic Scenarios (when enabled, consumes credits).

**Builder adds**: Guardrail monitoring and enforcement on verified runtime paths; Monitor and Enforce modes; Evaluators Hub (presets + custom criteria); human review queue; more systems/models/members/projects/retention capacity; priority support.

**Growth adds**: End User Management; User Risk Profiles "backed by available evidence"; longer audit history; user-level and team-level intelligence; higher limits across projects/systems/models/members/storage.

**Managed adds**: dedicated Slack channel; guided onboarding and architecture review; implementation assistance for LangChain/LangGraph/SDK paths; first-trace verification.

**Enterprise adds**: advanced governance workflows; private deployment; data residency; custom retention; dedicated infrastructure; custom connectors; SSO/SCIM; "AI Reliability Program"; contractual service levels.

**Exact numeric limits (seats, retention days, storage GB, # of projects/systems/models per tier)**: **NOT FOUND** — the pricing page describes these qualitatively ("more capacity," "higher limits," "longer audit history") rather than with hard numbers in the fetched content. Do not invent numbers; if the team needs exact figures for their 120-minute PRISM session, ask Block Convey staff directly during onboarding.

**Credits system**:
- Credits are the unit for "new AI-powered work" — shared across analysis, intelligence, evaluation, remediation, reporting, and Synthetic Scenarios. **VERIFIED**
- At zero credits: new AI-powered actions pause; no automatic overage or forced plan change; existing traces/findings/recommendations/evaluations/profiles/reports remain readable. **VERIFIED**
- Top-up: **minimum 100 credits for $10**; purchased credits tracked separately from monthly credits and don't expire until used; monthly credits do not roll over; failed jobs release reserved credits. **VERIFIED**
- **"PRISM credits" likely cover** (INFERRED from the above): running a synthetic-scenario batch, running an evaluator pass over a batch of traces, generating an Agent Intelligence report, generating an AI Remediation recommendation, generating an End User Intelligence report. Raw trace ingestion/storage itself appears to be **not** credit-metered (traces/sessions/agent runs are listed as included on all plans without credit caveats) — only the "AI-powered" analysis actions consume credits. This matters for the hackathon: **sending traces during the 120-minute session and free-credit allotment should be cheap; running many synthetic-scenario batches or evaluator passes is what will burn credits fastest.**

**Self-serve signup flow (VERIFIED, https://blockconvey.com/docs)**: create account at `prism.blockconvey.com/signup` → get project credentials (host/project ID/API key) → send one test trace via curl → verify via `/api/setup-doctor` → pick an integration path (SDK, OTel, zero-code proxy, LangChain/LangGraph, voice).

**"120-minute PRISM session" and "free credits" (event rules)**: **NOT RESEARCHED / not found on blockconvey.com** — this appears to be an arrangement specific to the ForgeAI hackathon (per event rules given in the task), not documented on Block Convey's public site. Team should get the exact credit grant and session scope directly from organizers, not assume it maps to a specific listed plan.

---

## 3. Positioning, Terminology & Competitors

### Core marketing taglines (VERIFIED, https://blockconvey.com)
- "Find AI failures before users do."
- "It passed your tests. Then it met a real user."
- "From working demo to real-user ready."
- "The tool returned 200. The task still failed."
- "Turn four is where conversations break."
- "Test with users you have not met yet." (Synthetic Scenarios)
- "See what your AI keeps getting wrong." (Agent Intelligence)
- "Every step the agent took, in one view." (Agent Observability)
- "From failure to a clear next step." (AI Remediation)

### Glossary of real PRISM terminology (term — meaning — source)
| Term | Meaning (as used by Block Convey) | Source |
|---|---|---|
| **Trace** | A single detailed execution log/record of one AI agent response or call (send one trace per response). | https://blockconvey.com/docs, https://blockconvey.com/prismtrace/docs |
| **Session** | A complete production record grouping traces into one user conversation/interaction, keeping intent, state, tool calls, and outcome attached. | https://blockconvey.com/prism |
| **Agent run** | A complete execution trace of one AI agent task. | https://blockconvey.com/solutions/ai-agents |
| **Synthetic Scenarios** | AI-generated realistic test users/situations (changing requests, missing details, tool problems, edge cases) created from a description of what the AI should do. Beta. Consumes credits. | https://blockconvey.com/prism |
| **Evaluators** | Reusable, repeatable scoring criteria applied to selected runs; supports presets + custom criteria (Evaluators Hub); Builder tier+. | https://blockconvey.com/prism |
| **Agent Intelligence** | Cross-run pattern recognition: user intent, conversation quality, recurring failure patterns, knowledge gaps. | https://blockconvey.com/prism |
| **Agent Observability / AI Observability** | Unified view of traces, sessions, agent runs, retrieval, tools, timing, retries, scores, outcomes. | https://blockconvey.com/prism |
| **End User Intelligence** | User-level pattern analysis: friction points, unresolved goals, risk profiles ("User Risk Profiles"). Growth tier+. | https://blockconvey.com/prism, /pricing |
| **AI Remediation** | Combines user goal + actual outcome + trace data + probable cause into a guided fix recommendation; human approval required before deploy. | https://blockconvey.com/prism |
| **Guardrails** | Policy-compliance monitoring with configurable trigger rates; **Monitor mode** vs **Enforce mode**; enforcement on "verified runtime paths." | https://blockconvey.com/pricing |
| **Root-cause classification / investigation** | Automated categorization of *why* a run failed. | https://blockconvey.com/prism |
| **Reliability score** | A composite metric scored across six weighted dimensions (exact dimensions not published). | https://blockconvey.com/prism (per fetch synthesis) |
| **Intent persistence** | Whether the agent correctly retains/tracks user intent across turns — named failure mode. | https://blockconvey.com/alternatives (witness-ai-alternative page context) |
| **Outcome mismatch** | When the agent's result doesn't match the user's actual goal even though the tool call "succeeded." | https://blockconvey.com/solutions/ai-agents |
| **Slot filling** | Parameter/field extraction quality in a conversational turn. | https://blockconvey.com/alternatives (witness-ai-alternative page context) |
| **State misalignment** | Example given: agent's tracked intent = "refund" when the user's actual goal was "exchange the order." | https://blockconvey.com/solutions/ai-agents |
| **PRISMtrace** | The tracing/SDK brand name and subdomain (`prism.blockconvey.com`, package `prismtrace-sdk`, classes prefixed `PRISMtrace*`). | https://blockconvey.com/prismtrace/docs |
| **AI Reliability Program** | Enterprise add-on: connect production AI → build baseline → review failures → prioritize improvements → give leadership evidence of progress. Six deliverables: platform access, guided setup/architecture review, reliability baseline, recurring technical review, prioritized remediation backlog, executive reliability report. Explicitly **excludes** unlimited custom engineering, unlimited connector dev, automatic legal certification, autonomous repo changes, autonomous production remediation. | https://blockconvey.com/ai-reliability-program |
| **PRISMX** | Separate product: browser-level DLP layer blocking PII/PHI/credentials from leaving the endpoint via ChatGPT/Claude/Gemini/Copilot; managed extension via Intune/Google Admin/Jamf. | search-cached page summaries (see Section 1 caveat) |

### Compliance/regulatory framework language (VERIFIED, https://blockconvey.com/compliance) — full list, 12 frameworks with Block Convey's own phrasing
- **EU AI Act**: "Risk classification, logging, and human oversight duties for AI systems in the EU."
- **NIST AI RMF**: "The govern, map, measure, manage cycle. Traces, evaluations, and reviews become the measure and manage record."
- **ISO/IEC 42001**: "The auditable AI management system standard. Operational evidence for the clauses an internal auditor asks to see."
- **SR 11-7 (Model Risk Management)**: "Model risk management discipline applied to AI and LLMs. Monitoring, validation, and change history in one place."
- **NY DFS Part 500**: "Cybersecurity oversight extended to AI systems, with incident evidence and access records examiners expect."
- **NAIC Model Bulletin** (insurance-specific!): "AI governance for insurers: documented testing, decision oversight, and incident handling with evidence attached."
- **CFPB / Regulation B (Fair Lending)**: "Adverse decisions need explanations. Session-level evidence of what the model saw, did, and decided."
- **HIPAA**: "PHI inside AI workflows. Redaction activity and access records that support the Privacy and Security Rules."
- **GDPR**: "Lawful processing and data minimization for AI. Evidence of what was collected, kept, and deleted."
- **DORA**: "ICT risk and incident reporting for EU financial entities, with AI systems part of the operational record."
- **SOX**: "AI touching financial reporting needs documented controls and change management. Versioned, reviewable evidence."
- **PCI DSS**: "Cardholder data kept out of AI logs. Guardrail events and redaction evidence on the paths that matter."
- **DPDP, RBI, IRDAI, SEBI are NOT mentioned anywhere on blockconvey.com** — **VERIFIED absence** (fetched /compliance directly; page enumerates the 12 above and stops). This is an opening for the team: Block Convey has explicitly built for insurance governance (NAIC Model Bulletin) and fair-decision explainability (Reg B) but has **not yet localized to Indian regulation** — the team can position their project as *"showing Block Convey's own framework extended to the IRDAI/DPDP/RBI context they haven't covered yet."*

### Security/data posture (VERIFIED, https://blockconvey.com/security)
- "Your AI data stays under your control" — customer app/workflow vs Block Convey processing/storage kept separate.
- Data collected only as needed for failure analysis: prompts/responses (if configured), session/trace IDs, model/provider metadata, tool calls, retrieval context, timing/token/cost data, user identifiers only if customer-configured.
- PII/sensitive-data handling with **redaction options**; project-scoped credentials; configurable retention; hosted-to-private deployment flexibility for enterprise.
- Certifications/frameworks referenced on /security: EU AI Act, NIST AI RMF, ISO 42001, HIPAA (subset of the fuller /compliance list).
- DPA available on request; subprocessor list published; vulnerability-reporting contact provided.

### Competitors named on Block Convey's own site (3 confirmed "alternatives" pages)
1. **`/alternatives/witness-ai-alternative`** — vs **WitnessAI**. WitnessAI = enterprise AI security/governance platform with both an applications-side product and an employee-DLP-side product (similar shape to PRISM+PRISMX). Differences: deployment posture, breadth of production observability, pricing model. **Block Convey's claimed differentiators**: compliance-first evidence as a core surface; self-host option for data-residency-sensitive workloads; tight integration with LLM platforms regulated firms standardize on (Databricks, Snowflake, Azure AI Foundry, AWS Bedrock); audit-grade exports; agent trajectory tracing; ISO 42001 alignment — "lean toward financial-services and healthcare buyers." **VERIFIED** (https://blockconvey.com/alternatives/witness-ai-alternative, corroborated via search-index snippet)
2. **`/alternatives/lakera-alternative`** — vs **Lakera** (LLM security platform: prompt-injection defense, AI red-teaming — Lakera Guard, Lakera Red). **Block Convey's claimed differentiator**: PRISM is the choice "when you need the full operational surface — trace logging, quality evaluation, agent trajectories, audit exports — alongside guardrails and red teaming," and "when compliance officers and CROs are buyers as well as security teams." Implies Lakera is narrower/security-team-only; PRISM covers the compliance-officer buyer persona too. **VERIFIED** (https://blockconvey.com/alternatives/lakera-alternative, corroborated via search-index snippet)
3. **`/alternatives/credo-ai-alternative`** — vs **Credo AI** (governance-first: AI registry, policy packs, assessments — "policy layer," strong for orgs early in AI-governance journey). **Block Convey's claimed differentiator**: Credo AI's operational layer (production observability, real-time guardrails, agent traceability) is "comparatively lighter"; PRISM is for orgs that already have AI in production and need continuous evidence — "every LLM call traced, every output scored, every guardrail event logged, every agent decision reconstructable... the operational layer compliance teams actually defend in audits, not just the policy layer they document on SharePoint." **VERIFIED** (https://blockconvey.com/alternatives/credo-ai-alternative, corroborated via search-index snippet)
- **No comparison pages found** for Langfuse, LangSmith, Arize, Helicone, Braintrust, or Galileo. **VERIFIED absence** (direct fetches of guessed URLs `/alternatives/langfuse-alternative`, `/alternatives/langsmith-alternative`, `/alternatives/arize-alternative` returned no comparison content / effectively 404-equivalent). Block Convey positions itself against **AI-security and AI-governance** platforms (WitnessAI, Lakera, Credo AI), **not** against the general-purpose LLM-observability/eval tooling category (Langfuse/LangSmith/Arize/Helicone/Braintrust/Galileo). **INFERRED takeaway**: Block Convey sees its category as "AI governance/compliance evidence for regulated buyers," not "developer observability tooling" — echo *that* framing, not generic MLOps observability language, when pitching to them.

### Terminology/phrases to AVOID (not PRISM's real vocabulary)
- Do **not** say "LangSmith-style tracing" or compare to Langfuse/Arize/Helicone/Braintrust/Galileo by name — Block Convey doesn't position against them; using that language signals the team doesn't know Block Convey's actual competitive frame.
- Avoid generic "observability platform" alone — Block Convey's preferred self-description is **"reliability layer"** / **"AI Reliability Program"** / **governance-and-evidence** language, not just "observability."
- Avoid inventing exact numeric plan limits (seats/retention days/storage) — the public pricing page does not publish them; stating a fabricated number would be an easily-caught error in front of the people who wrote the page.
- Avoid claiming PRISMX features (DLP browser extension) as part of what the team used, unless they actually used PRISMX — current site state is uncertain (see caveat above); safer to only claim **PRISM** (traces/evaluators/guardrails/synthetic scenarios/agent intelligence/remediation) usage.

---

## 4. Content, Community & Prior Events

- **Blog**: `/resources/blog` explicitly states **"No posts published yet"** — "The first posts are being written... the guides cover the same ground in the meantime." **VERIFIED** (https://blockconvey.com/resources/blog)
- **Guides**: `/resources/guides` lists **12 forthcoming (not-yet-published) guide titles**, all "coming soon": "How to Test an AI Agent Beyond the Happy Path," "LLM Observability: What to Capture and Why It Matters," "Agent Tracing: From User Goal to Final Outcome," "Synthetic Scenarios for Testing Real AI Behavior," "AI Agent Evaluation Across Tools, State, and Outcomes," "How to Debug an AI Agent That Took the Wrong Action," "RAG Evaluation: Retrieval, Context, and Generation," "Chatbot Testing for Multi-Turn Conversations," "LLM Guardrails: Monitor First, Then Enforce," "AI Remediation: From Failure to Validated Improvement," "LangChain Observability for Real User Outcomes," "LangGraph Observability Across Nodes, Tools, and State." None mention hallucination, sycophancy, voice, insurance, or multilingual by name. **VERIFIED** (https://blockconvey.com/resources/guides)
- **Glossary**: `/resources/glossary` is also unpublished — "Definitions are being published... Terms appear here as each definition is reviewed." **VERIFIED** (https://blockconvey.com/resources/glossary)
- **Changelog**: no changelog page/link found in navigation or docs structure. **NOT FOUND**
- **Careers page**: `/careers` returned 404 at fetch time — no open roles page found. **NOT FOUND**
- **Case studies / customers**: `/customers` and `/case-studies` both returned 404 / no content at fetch time. **No named customers, logos, or case studies found anywhere** in this research pass. **NOT FOUND**
- **Product Hunt**: PRISM launched on Product Hunt (2025) — **128 upvotes, #6 Day Rank**. Tagline: "Monitor models, explain decisions, & future-proof models." Makers: **Arun Prasad, Adithyah Nair, Kritin Madhavan**. Top review (Stepan Solodnev): product "looks very promising," "a really necessary thing in the era of AI growth." Comment theme: time-savings, "it's a great product. Saves a lot of time." Sentiment uniformly positive in visible comments. **VERIFIED** (https://www.producthunt.com/products/prism-by-block-convey)
- **X/Twitter**: account exists at `x.com/blockconvey`; content could not be retrieved (fetch returned HTTP 402/paywalled). **NOT RESEARCHED** (blocked)
- **LinkedIn**: company page `linkedin.com/company/block-convey-inc`; at least one post found via search titled "Block Convey - Explainer" and another "How Block Convey PRISM solves regulatory challenges" (team/behind-the-scenes/startup-life themed). Full post content not retrieved — **NOT RESEARCHED in depth** (only titles/snippets surfaced by search).
- **YouTube**: no Block Convey / PRISM-specific videos found; searches returned unrelated "Prism" results (Nutanix Prism Central, a PRISM project-management methodology, a video game called Prism). **NOT FOUND**
- **GitHub org**: no official `block-convey` GitHub organization found. Found instead: (a) **finos-labs/dtcc-i-h-2025-prism** — the DTCC AI Hackathon 2025 repo that appears to be PRISM's origin project (see Section 1); (b) two **third-party hackathon repos that integrate with PRISM/PrismTrace as a tool**, described below.
- **PyPI packages**: only one confirmed — **`prismtrace-sdk`** (current documented version `>=0.4.3`), import name `prismtrace`. **VERIFIED** (https://blockconvey.com/prismtrace/docs). No other Block Convey PyPI packages found.
- **Podcasts / Medium / Substack / webinars**: **NOT FOUND** in this research pass.

### Prior hackathon usage of PRISM found on GitHub (two concrete examples — useful as "prior art" reference points, not official Block Convey-run events)
1. **`Abhinaykrishna2/block-convey-hackathon`** — project **SENTINEL**, an "autonomous AI security analyst" for enterprise vendor security questionnaires; uses a 9,646-node knowledge graph + multi-turn decision loop + persistent memory to prevent hallucination while answering compliance questions. Explicitly logs "Full trajectory trace logged to PRISM Trace SDK" as part of a "guardrailed agent loop." Benchmarked against a 66-question test suite with a claimed zero-hallucination rate. No hackathon name, date, judging notes, or results/placement stated in the README. **VERIFIED partial** (https://github.com/Abhinaykrishna2/block-convey-hackathon) — **hackathon identity and outcome NOT FOUND**.
2. **`IshaPatro/MoneyTalks`** — project **WhaleWatch**, an AI SaaS revenue-concentration-risk analysis agent (identifies "whale" customers driving disproportionate revenue / hidden churn risk). Instruments two Claude call sites with PrismTrace: *"every real Claude call (prompt, response, latency, token counts) is traced so a hallucinated number or a silent template fallback shows up in a dashboard."* Integration is optional/no-ops without credentials. Single contributor listed; no hackathon name found. Demo figures: $34.55M MRR, +20.8% MoM growth, largest customer 34.7% of MRR, $830.2K negative portfolio movement (as illustrative demo data, not real company data). **VERIFIED partial** (https://github.com/IshaPatro/MoneyTalks) — **hackathon identity NOT FOUND**.
- **DTCC AI Hackathon 2025** (see Section 1) is the clearest *documented* precedent of "PRISM at a hackathon," but note it predates Block Convey as a company — it's the *origin* event, not a "Block Convey sponsors a hackathon" event.
- **No prior Gravitas/VIT event with Block Convey involvement found.** Web search for `Gravitas VIT "Block Convey" hackathon` surfaced only generic Gravitas hackathon pages (Hack the Hackathon, VINHACK) with no Block Convey connection. **NOT FOUND** — this strongly suggests **ForgeAI 2026 is Block Convey's first (or first well-indexed) presence at VIT/Gravitas**, i.e., there is no prior "what judges praised" data to mine — the team should not claim continuity with a past VIT event.
- **General conclusion**: Block Convey has **very thin public content/community footprint** — no blog posts, no glossary entries, no case studies, no changelog, no YouTube channel found. The company is young, small (~6 people), and mostly pre-content-marketing. **This is itself useful pitch intelligence**: the team is likely one of the more visible, concrete "PRISM in production use" case studies Block Convey will have anywhere online — worth explicitly noting in the pitch that a polished writeup/demo is something Block Convey could actually reuse as their first real case study.

---

## 5. Regulatory Hooks for an Indian Insurance Voice Agent

Short, sourced notes on what a compliance-focused judge (from a company whose own site emphasizes EU AI Act / NIST AI RMF / ISO 42001 / SR 11-7 / NY DFS / NAIC / Reg B / HIPAA / GDPR / DORA / SOX / PCI DSS) would expect an **Indian insurance** voice-agent team to reference. None of these India-specific items appear on blockconvey.com itself (confirmed absent, Section 3) — bringing them is how the team demonstrates regulatory sophistication *beyond* what Block Convey's own materials currently cover.

- **RBI FREE-AI Framework** ("Framework for Responsible and Ethical Enablement of AI") — RBI committee report issued **13 August 2025** (committee constituted Dec 2024). Survey found **20.8%** of surveyed entities already deploying AI in customer support/sales/underwriting/cybersecurity, **67%** exploring further use cases. Seven guiding principles ("Sutras") including public trust as foundation, disclosure of AI usage, human override authority, "responsible innovation over cautionary restraint." Structured around **six pillars**: Infrastructure, Policy, Capacity, Governance, Protection, Assurance, with **26 actionable recommendations** (AI sandboxes, indigenous financial AI models, governance/audit/incident-reporting mechanisms). Proposes **proportionate, risk-based regulation** — lighter touch for low-risk use cases, stricter for high-risk. **VERIFIED** (https://dvararesearch.com/summary-of-the-rbi-free-ai-committee-report/, https://www.khaitanco.com — Ergo summary PDF, KPMG summaries at kpmg.com/in). **Pitch hook**: an FNOL voice agent with cancellation/anti-sycophancy/PII safety layers is a textbook "high-risk, customer-facing, human-override-required" use case under FREE-AI's proportionate-risk logic — cite the **human-override "Sutra"** directly against the team's mid-sentence-cancellation safety layer.
- **IRDAI** — no single unified "AI chatbot" regulation found, but: (a) IRDAI's **InsurTech Working Group** has flagged **chatbot/voicebot-enabled claims handling** as a technology reshaping Indian insurance; (b) **IRDAI Regulatory Sandbox Regulations 2025** (notified 3 Jan 2025) widen sandbox scope to cover innovation "across the insurance value chain," including relaxation from existing regulations/circulars — directly relevant if the team frames their agent as a sandbox-style pilot; (c) IRDAI Policyholder Protection Regulations require insurers to maintain policy/claims records with strict confidentiality for medical/sensitive data and mandated security safeguards for third-party service providers (relevant to any voice-agent vendor architecture). **VERIFIED** (https://www.mondaq.com/india/insurance-laws-and-products/1773748/, https://www.legal500.com/developments/thought-leadership/irdais-regulatory-sandbox-regulations-2025-key-changes-for-insurance-innovation/). **No IRDAI-specific chatbot/voicebot technical circular with detailed AI rules was found** — **NOT FOUND** at circular level; treat IRDAI point as "sandbox + general policyholder-protection + InsurTech Working Group direction," not a specific AI rulebook.
- **DPDP Act 2023 + DPDP Rules 2025** — Rules notified **17 November 2025** (per PIB), operationalizing the 2023 Act; rollout in **three phases**, full compliance expected by **13 May 2027**. Core mechanism: **explicit, informed, freely-withdrawable consent**; **standalone, clear, simple consent notices** stating specific purpose; **verifiable consent required for children and persons with disabilities**. **VERIFIED** (https://en.wikipedia.org/wiki/Digital_Personal_Data_Protection_Rules,_2025, https://www.pib.gov.in/PressReleasePage.aspx?PRID=2190014). Sector interplay: IRDAI record-retention mandates for policies/claims can **conflict** with DPDP erasure rights — insurers must reconcile "must retain per IRDAI" vs. "must honor deletion request per DPDP." **VERIFIED** (https://www.dpo-india.com/Blogs/interplay-india%E2%80%99s-dpdp-act/). **Pitch hook**: the team's PII-scrubbing safety layer for a spoken/code-mixed conversation is a concrete, demoable **DPDP data-minimization + purpose-limitation** control — explicitly cite "we only capture what's needed for this FNOL call, nothing else" as data-minimization in action, and note the retention-vs-erasure tension as a known unresolved area (shows depth).
- **PCI DSS — spoken card data**: standard technique is **"pause and resume"** — recording is paused before card-data capture, resumed after — but **PCI DSS v4.0.1 explicitly disfavors manual pause/resume** because it doesn't reliably/automatically/predictably exclude card data from scope; a missed pause brings the whole recording into PCI scope. **Better-practice alternative: DTMF masking/suppression**, which routes keypad tones straight to a payment processor so card digits never reach the agent, transcript, or recording at all. **VERIFIED** (https://sycurio.com/blog/unlocking-the-truth-how-pause-and-resume-impacts-contact-center-pci-compliance, https://www.paytia.com/resources/blog/contact-centre-pci-compliance-guide). **Pitch hook**: since the project is FNOL (claims), not payment collection, card data may not even arise — but if any deductible/premium payment flow is discussed in the demo, explicitly say the team **avoided manual pause/resume in favor of never letting spoken card digits enter the transcript/LLM context at all** (automatic exclusion, not manual discipline) — this is exactly the "automated, predictable" posture PCI DSS v4.0.1 now requires, and it directly parallels Block Convey's own compliance-page language: *"Cardholder data kept out of AI logs. Guardrail events and redaction evidence on the paths that matter."*
- **ISO/IEC 42001** — first certifiable international AI-management-system standard; applicable across industries; certification can help **reduce liability/tech-E&O insurance premiums** by demonstrating third-party-validated risk controls; helps org implement consistent risk/impact/accountability processes for AI. Block Convey already names ISO 42001 as one of its core compliance frameworks ("the auditable AI management system standard... evidence for the clauses an internal auditor asks to see"). **VERIFIED** (https://www.tuvsud.com/en-us/services/auditing-and-system-certification/iso-iec-42001-artificial-intelligence-management-system, https://blockconvey.com/compliance). **Pitch hook**: frame PRISM traces/evaluators/guardrail logs generated during the demo explicitly as **"the kind of operational evidence an ISO 42001 internal auditor would ask to see"** — echoes Block Convey's own phrase almost verbatim, which is a deliberate, safe way to "speak their language."

**Summary of what a Block Convey judge would expect mentioned, briefly**: DPDP data-minimization/consent, RBI FREE-AI's human-override principle, IRDAI's sandbox/InsurTech direction (not a specific chatbot circular — don't overclaim one exists), automated (not manual) card-data exclusion if payment flows appear, and ISO 42001-style "operational evidence" framing tying directly back to PRISM's own traces/evaluators/guardrail logs.

---

## 6. Pitch Intelligence for Judges

**Who's likely judging / what they care about (INFERRED from all above, since no ForgeAI judge list was retrieved — NOT RESEARCHED directly)**: given the founding team's own trajectory (model-audit/bias/explainability → agent observability, DTCC/FINOS fintech-hackathon roots, Fintech Sandbox accelerator, compliance-framework-heavy site content spanning EU AI Act/NIST/ISO 42001/SR 11-7/NY DFS/NAIC/Reg B/HIPAA/GDPR/DORA/SOX/PCI DSS), judges are plausibly a mix of **founder/technical staff** (Arun Prasad, Aishwarya Birla, Pavan Marisetti, or people they send) who will personally know PRISM's real feature set and will notice both accurate and inaccurate terminology use. Assume the audience cares about **regulated-industry evidence generation**, not generic "cool demo" AI engineering.

### What Block Convey would most want to see demonstrated (concrete, evidence-based)
1. **Real trace volume, not a screenshot**: since "100% production session coverage" and per-response tracing are core PRISM claims, show a live trace count growing during the demo, not a static screenshot — proves the "every LLM call traced" claim Block Convey uses against Credo AI.
2. **Synthetic Scenarios used to *find* the weakness, not just fix a pre-known bug**: the rules require "identify a real weakness" via PRISM — align this explicitly with PRISM's own tagline "test with users you have not met yet." Generate scenarios covering code-mixed Hinglish/Tanglish interruptions, mid-sentence cancellations, and a customer pushing for a deductible waiver — these map almost exactly onto Block Convey's own named failure categories (**intent persistence**, **slot filling**, **state misalignment**, **outcome mismatch**, "turn four is where conversations break").
3. **Guardrails in Monitor → Enforce mode transition**: demonstrate a guardrail catching the anti-sycophancy failure (agent inappropriately granting a deductible waiver) first in Monitor mode (observed), then flipped to Enforce mode (blocked) — this literally re-enacts Block Convey's own guide title "LLM Guardrails: Monitor First, Then Enforce."
4. **Evaluators with before/after delta**: run an Evaluator pass before the fix and after the fix on the same failure class, showing the **reliability score** (or a custom scored dimension) move — this satisfies "Measured AI Improvement" (20% of judging) in PRISM's own native vocabulary (delta tracking, monthly scoring reports concept, applied live instead of monthly).
5. **Root-cause / AI Remediation flow used as designed**: show the actual PRISM-generated probable-cause + remediation recommendation, then the team's human-approved fix — mirrors "human approval required before changes deploy," which is a differentiator Block Convey states explicitly.
6. **PII-scrubbing safety layer framed as their own quoted phrase**: PRISM's own voice-agent docs say *"Transcripts are scrubbed for PII on the server before storage, and audio is never sent to or stored by PRISM."* The team's PII-scrubbing layer is independently-built but conceptually identical — say so explicitly; it proves the team understands what PRISM itself already promises its voice-agent users, and shows defense-in-depth (app-level scrubbing *and* PRISM's own scrubbing).
7. **Insurance-specific regulatory framing using PRISM's actual compliance language**: cite **NAIC Model Bulletin** phrasing ("documented testing, decision oversight, and incident handling with evidence attached") and **Reg B** phrasing ("adverse decisions need explanations... session-level evidence of what the model saw, did, and decided") almost verbatim, then extend it explicitly to IRDAI/DPDP/RBI FREE-AI — this is the single highest-leverage move: it shows the team read Block Convey's own compliance page and is extending Block Convey's own worldview into a market (India insurance) Block Convey hasn't documented yet.
8. **Voice-agent capability as an implicit gap-fill**: Block Convey's marketing solution pages (Conversational AI, AI Agents) never mention voice agents or multilingual/code-mixed language, even though the docs/SDK already support ElevenLabs voice tracing. Explicitly note this in the pitch: *"Your docs already support voice agents (PRISMtraceVoiceTracer) — we're one of the first teams putting that path through its paces with a multilingual, code-switching, safety-critical use case."* This is a genuinely novel angle a founder-judge would likely find flattering and technically credible, since it's accurate (VERIFIED docs, Section 1) and not exaggerated.

### Phrases/claims a demo could concretely *prove* (i.e., don't just assert — show it happening on screen)
- "100% production session coverage, not sampling" → show every test call appearing as a trace.
- "Guardrail monitoring and enforcement on verified runtime paths" → show a specific guardrail rule firing on the sycophancy/deductible-waiver scenario.
- "Root-cause investigation and remediation recommendations" → show PRISM's generated root-cause text, not just an internal team guess.
- "Human approval required before changes deploy" → explicitly show a human (team member) approving the remediation before redeploying the agent.
- "Turn four is where conversations break" → structure at least one synthetic scenario to specifically break around turn 3–4 with a mid-sentence cancellation, and show PRISM catching it.

### Jargon/phrases to avoid (not Block Convey's real vocabulary — a founder-judge would notice)
- Don't call PRISM a "Langfuse/LangSmith/Arize/Helicone/Braintrust/Galileo competitor" or benchmark against them by name — Block Convey positions against **WitnessAI, Lakera, and Credo AI** instead (AI governance/security category, not general MLOps observability). Using the wrong comparison set signals the team didn't do this homework.
- Don't say "we used Block Convey's LLM observability platform" as the sole description — prefer their own phrase, **"reliability layer,"** or name the specific capability (Synthetic Scenarios / Evaluators / Guardrails / Agent Intelligence / AI Remediation) rather than the generic category term.
- Don't cite specific numeric plan limits (seats, retention days, storage GB) as if known — they are not published; if asked, say the team used [Free/Builder/Growth — whichever tier was actually used] and defer exact limits to Block Convey.
- Don't claim PRISMX (browser DLP) usage unless actually used — its current availability on the live site is uncertain (Section 1 caveat); misclaiming it in front of the CTO would be an easily-caught error.
- Don't claim a specific IRDAI "AI chatbot circular" exists with named technical requirements — none was found; frame IRDAI correctly as "sandbox regulations + InsurTech Working Group direction + general policyholder-protection duties," not a chatbot-specific rulebook.
- Don't overstate Block Convey's funding/scale (numbers found were inconsistent/low-confidence) — safer to not cite funding figures at all in the pitch.

### Gaps flagged as not researched in this pass (for other agents / follow-up)
- Full LinkedIn company-page post history and content (only titles/snippets surfaced).
- X/Twitter feed content (fetch blocked, HTTP 402).
- Exact numeric pricing-tier limits (seats/retention/storage) — not published publicly; would need direct confirmation from Block Convey staff at the event.
- Full detail on the "120-minute PRISM session" and "free credits" grant structure for ForgeAI specifically — not documented on blockconvey.com; is an event-specific arrangement, get it from organizers.
- Named ForgeAI/Gravitas judge list and their individual backgrounds — not retrieved in this pass.
- PRISMX's current live-site status/availability — contradictory evidence (present in cached/third-party summaries, absent on direct fetch of /solutions and /prismx on 2026-09-14).
