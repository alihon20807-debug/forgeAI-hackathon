# Pitch Deck Build Plan — ClaimGuard × PRISM
### Master Architectural Specification for High-Impact HTML Presentation
**Target Audience**: Judges at ForgeAI Hackathon (graVITas'26, VIT Vellore / Block Convey Founders & Technical Staff)  
**Deliverable Targets**: `presentation/claimguard-pitch.html` (Online/CDN) & `presentation/claimguard-pitch-offline.html` (Offline/Standalone)  
**Status**: **CANONICAL DECK BUILD SPECIFICATION** (Derived directly from `Overall-plan.md` & `research/prism/`)

---

## 0. Executive Mandate & Strategic Framing

### 0.1 The Core Thesis
> **PRISM is the central hero; ClaimGuard is the deliberately breakable vehicle.**  
> Call-center voice agents in India are rolling out on **cheap, fast, small models** (3B–8B) because cost-per-call and <500ms latency budgets dictate it. Small models are exactly the ones that fumble mid-sentence cancellations, cave to emotional bargaining, and leak card numbers. We built **ClaimGuard**—a roadside-assistance voice agent running on a deliberately small local LLM—and used **PRISM end-to-end as the reliability engine** that intercepts failures, diagnoses root causes, guides AI Remediation, and re-proves safety on a held-out benchmark. We are not demoing another generic chatbot. We are demoing how PRISM makes real-world, small-model agent deployments safe in production.

### 0.2 Judging Rubric Mapping (100% Traceability)
Every single slide is engineered to score maximum points on the official hackathon criteria:
- **Solution & Technical (25%)**: Slides 2, 3, 5 (Deterministic L3 commit window, DB triggers, Whisper ASR, BGE-M3 RAG).
- **PRISM Evaluation & Diagnosis (20%)**: Slides 4, 5 (Span tracing, Agent Intelligence failure clusters, Root Cause classification).
- **Measured AI Improvement (20%)**: Slide 4 (v0 Baseline vs v1 Prompt-Fix vs v2 ClaimGuard benchmark delta on held-out NH48 set).
- **Demo & Pitch (15%)**: All slides (Live interactive waveform, live state-machine simulator, dynamic PRISM ray tracer, <40 words/slide).
- **Innovation (10%)**: Slides 2, 3, 6 ("Chaos engineering" small-model bet, Pre-LLM PII shielding, multi-domain scalability).
- **Problem & Impact (10%)**: Slides 1, 6 (Universal call-center voice failure class, DPDP Act / PCI DSS regulatory alignment).

### 0.3 The Strict 6-Slide Format Contract (Locked to Reference Image)
The deck strictly adheres to the 6 slides and exact prompt subtitles specified in the user's reference image:
1. **Slide 1 — Problem Statement**: *What real-world problem are we trying to solve?*
2. **Slide 2 — Existing Challenges**: *What are the limitations, risks, or gaps in current solutions?*
3. **Slide 3 — Proposed Solution**: *What solution are we proposing and how does it solve the problem?*
4. **Slide 4 — PRISM Usage**: *How PRISM is used to monitor, evaluate, detect failures, and improve the AI system..*
5. **Slide 5 — System Workflow**: *Input → AI/RAG/Agent System → PRISM Monitoring & Evaluation → Failure Detection → Improvement*
6. **Slide 6 — Impact & Future Scope**: *Key benefits, real-world impact, scalability, and future enhancements.*

---

## 1. Anti-"AI Slop" Design System & Production Architecture

### 1.1 Aesthetic Philosophy
Judges review hundreds of hackathon pitches featuring generic purple-neon glassmorphic cards, robotic emojis, and walls of AI-generated marketing fluff. This deck takes the opposite approach: **Engineering-First Editorial Minimalism** (inspired by Linear, Stripe, and Apple Keynote).
- **Monochrome Foundation**: Deep charcoal/slate ground (`#0A0B10`) with crisp 1px borders and disciplined structural contrast.
- **The Optical Spectrum Motif**: PRISM's name represents physical optics (white light refracted into a spectrum). White/grey light represents raw, unobserved telemetry. The 5 spectral wavelengths appear **only** when PRISM or the enforcement layer is actively analyzing, diagnosing, or enforcing.
- **Strict Word Budget**: $\le 35\text{--}40$ words of prose per slide. Information is conveyed through diagrams, interactive widgets, telemetry streams, and math.

### 1.2 Color System Tokens
```css
:root {
  /* Surface & Base Ground */
  --ground: #08090D;             /* Deepest void canvas */
  --surface: #11131A;            /* Structural panels and cards */
  --surface-raised: #181B26;     /* Active/hover nodes */
  --border: #222634;             /* 1px subtle hairline rule */
  --border-bright: #363C52;      /* Highlighted container border */
  
  /* Typography / Ink */
  --ink-primary: #F3F4F8;        /* Headlines, primary labels */
  --ink-secondary: #8E93A6;      /* Subtitles, secondary descriptions */
  --ink-muted: #52566B;          /* Metadata, timestamps, inactive icons */

  /* The PRISM Refractive Optical Spectrum */
  --prism-violet: #8B7CFF;       /* L5 Spans & Telemetry Traces */
  --prism-teal: #3FD6C9;         /* Root Cause Diagnosis & Knowledge Base */
  --prism-amber: #FFB84D;        /* Failure Clustering & Held State */
  --prism-rose: #FF5271;         /* Outbound Veto & Aborted Actions */
  --prism-emerald: #2ED573;      /* Committed Actions & Benchmark Improvement */
  --prism-white: #FFFFFF;        /* Raw incident light beam */
}
```

### 1.3 Typography Stack
Loaded via standard Google Fonts:
1. **Display & Headlines**: `Fraunces` (Variable 100-900, Optical Size 72pt). Gives an optical, lens-like warmth to titles without feeling generic.
2. **Body & Interface**: `IBM Plex Sans` (400, 500, 600). Crisp, legible, enterprise-grade sans-serif for UI labels and cards.
3. **Data, Telemetry & Code**: `IBM Plex Mono` (400, 500, 600). Used for all `agent_id` tags, tool names (`stage_dispatch`), JSON spans, and slide counters (`01 / 06`).

### 1.4 Viewport & Resolution Architecture
- **Target Aspect Ratio**: Fixed `16:9` (`1920x1080` native canvas).
- **Responsive Venue Scaling**: Wraps all content inside an aspect-ratio preserving container:
  ```css
  #presentation-stage {
    width: min(100vw, 177.78vh);
    height: min(56.25vw, 100vh);
    position: relative;
    overflow: hidden;
  }
  ```
  Guarantees identical pixel-perfect geometry on 4K conference screens, standard 1080p projectors, or 1366x768 laptop HDMI feeds without awkward scrollbars or clipping.

### 1.5 Global Presentation Shell (Persistent UI)
- **Top Left**: Eyebrow counter `01 / 06 — PROBLEM STATEMENT` in mono muted caps.
- **Top Right**: The Optical Prism Glyph. A sharp equilateral triangle with subtle refraction animation, labeled `INSTRUMENTED BY PRISM`.
- **Bottom Left**: Real-time Engine Heartbeat: `PRISM Telemetry: Active | 60 FPS | whisper.cpp local`.
- **Bottom Center**: 6 Interactive Navigation Pips (clickable, with keyboard number indicators `1-6`).
- **Bottom Right**: Active Agent Profile: `agent_id: roadside-claimguard | NH48 Replay Set`.
- **Global Shortcuts**:
  - `Space` / `→` / `PageDown`: Next slide.
  - `←` / `PageUp`: Previous slide.
  - `1` through `6`: Direct jump.
  - `F`: Toggle Fullscreen.
  - `D`: Toggle Interactive Debug HUD / Inspector.
  - `?` or `N`: Toggle Speaker Notes Drawer.

---

## 2. Exhaustive Slide-by-Slide Specifications

```
+----------------------------------------------------------------------------------------------------+
| [01/06 -- PROBLEM STATEMENT]                                              [/\ INSTRUMENTED BY PRISM] |
|                                                                                                    |
|                             SLIDE VIEWPORT (16:9 DYNAMIC STAGE)                                    |
|                                                                                                    |
|                                                                                                    |
|                                                                                                    |
|                                                                                                    |
| [* PRISM Telemetry: Active]           [ . . . . . . ]            [agent_id: roadside-claimguard]   |
+----------------------------------------------------------------------------------------------------+
```

---

### Slide 1: Problem Statement

#### A. Metadata & Prompts (Mandated by Image)
- **Slide Eyebrow**: `Slide 1 - Problem Statement`
- **Mandated Prompt**: `What real-world problem are we trying to solve?`
- **Headline (Fraunces Display)**: *"Turn four is where conversations break."*
- **Headline Attribution (IBM Plex Mono)**: `— Block Convey, on why conversational AI fails in production`

#### B. Spoken Pitch Beat (Presenter Script — 20 seconds)
> *"Judges, Indian insurance call centers handle millions of First-Notice-of-Loss calls. High volume and strict latency force companies to deploy fast, small models—not 70-billion-parameter frontier giants. But real callers are panicking on highways: they interrupt mid-sentence, demand unauthorized waivers, and blurt out credit cards. By turn four, unobserved small models break: sending wrong tows, conceding illegal discounts, and leaking sensitive PII into plain logs."*

#### C. Layout Grid & Spatial Composition
- **Top Section (20%)**: Mandated eyebrow + prompt + Fraunces pull-quote.
- **Middle Section (50%)**: `AudioWaveformCanvas` — An animated real-time audio waveform visualizer running horizontally across the stage, simulating an incoming code-mixed emergency call on NH48.
- **Bottom Section (30%)**: 3 Interactive Fault Incident Nodes pinned to the audio timeline at turns 2, 4, and 5.

#### D. Visual Engine & Dynamic Components
1. **`AudioWaveformCanvas` (HTML5 Canvas 2D)**:
   - Continuously renders a live multi-sine modulated audio waveform with dynamic ambient noise simulation.
   - Shows timecodes (`00:04`, `00:12`, `00:24`) and speech energy peaks.
2. **Three Interactive Timeline Incident Pins**:
   - **Turn 02 [Amber — `#FFB84D`]**: `Mid-Sentence Revocation`  
     *Scenario*: "Wait! My friend stopped with a spare tire, cancel the tow truck!"  
     *Consequence*: **Safety & Logistics Failure** (Tow dispatched anyway; ambulance delayed).
   - **Turn 04 [Rose — `#FF5271`]**: `Emotional Pressure & Bargaining`  
     *Scenario*: "I've been stranded 2 hours in the rain, waive my ₹1,500 deductible right now!"  
     *Consequence*: **Financial Leak** (Small LLM hallucinates authority and concedes).
   - **Turn 05 [Violet — `#8B7CFF`]**: `Spoken Sensitive Identifier`  
     *Scenario*: "Fine, charge my card directly: 4532 8901 2345 6789..."  
     *Consequence*: **Regulatory Breach** (Plaintext PII logged to disk, violating DPDP Act & PCI DSS).

#### E. Interactive JavaScript Features
- **Hover/Click on Pins**: Clicking any pin pauses the waveform, highlights the exact audio segment, and pops open a telemetry inspection tooltip showing the raw caller audio vs. the downstream catastrophe.
- **Keyboard Shortcut**: Pressing `1`, `2`, or `3` while on Slide 1 auto-triggers the corresponding fault pin.

#### F. Text Copy & Word Budget
- Headline & Quote: 10 words.
- Pin Callouts: 24 words total.
- **Total Word Count**: 34 words (Target: $\le 40$).

#### G. Rubric Alignment & Objection Handling
- **Rubric**: Problem & Impact (10%), Innovation (10%).
- **Judge Trap**: *"Why focus on roadside assistance?"*
- **Bulletproof Counter**: Roadside FNOL is the highest-stress, most legible intersection of voice interruption, financial authority, and PII in conversational AI.

---

### Slide 2: Existing Challenges

#### A. Metadata & Prompts (Mandated by Image)
- **Slide Eyebrow**: `Slide 2- Existing Challenges`
- **Mandated Prompt**: `What are the limitations, risks, or gaps in current solutions?`
- **Headline (Fraunces Display)**: *"Small models are what actually ships. Nobody demos with them."*

#### B. Spoken Pitch Beat (Presenter Script — 20 seconds)
> *"Everyone demos AI with massive cloud models, but call centers can't afford ₹30 per minute or 3-second latency. They deploy 3-billion to 8-billion parameter models. The existing industry solution? A prompt telling the model to 'be careful and follow policy.' But prompts can't hold a state machine under user interruption, legacy observability is completely blind to turn-by-turn tool state, and regex redaction happens after the log is already written."*

#### C. Layout Grid & Spatial Composition
- **Two-Column Split (55% / 45%)**:
  - **Left Column**: The **"Broken Stack" Architecture Diagram (SVG)**. Shows the legacy pipeline with a visible, fractured fracture point where safety should live.
  - **Right Column**: 3 Structural Gap Cards with high-contrast data callouts.

#### D. Visual Engine & Dynamic Components
1. **The "Broken Stack" Architecture SVG**:
   - `L0 Client Edge` (Browser/Mic) $\rightarrow$ `L1 Perception` (Whisper) $\rightarrow$ `L2 Cognition` (3B Small Model) $\rightarrow$ `[CRACKED DASHED GAP: No Enforcement]` $\rightarrow$ `L4 Database`.
   - The enforcement box is rendered in dashed crimson with animated fracture cracks and a flashing warning icon: `MISSING STATE BARRIER`.
   - `L5 PRISM Spine`: Rendered as a completely **dark, disconnected silhouette**, visually demonstrating that current call centers have zero session-level observability into why their agents fail.
2. **Three Structural Gap Cards**:
   - **Card 1: Fragility of Prompting Alone**  
     *Headline*: Prompts Aren't State Machines.  
     *Mechanism*: Under conversational interruption or emotional pressure, small LLMs suffer catastrophic attention drift. System prompts cannot enforce transactional guarantees.
   - **Card 2: Unobserved Silent Failures**  
     *Headline*: Telemetry Blindness.  
     *Mechanism*: Legacy APMs only track HTTP status codes and token latency. They cannot cluster multi-turn conversational failure modes or detect tool hallucination loops.
   - **Card 3: Post-Hoc PII Exposure**  
     *Headline*: Redaction After the Breach.  
     *Mechanism*: Masking PII after it enters the LLM context window exposes customer card data to model weights, cloud telemetry, and inference cache.

#### E. Interactive JavaScript Features
- **Hover Inspection**: Hovering over any Gap Card highlights the corresponding broken layer in the architecture SVG with an animated red pulse.
- **"Show Failure Trace" Button**: Toggles a mini terminal showing a simulated raw JSON log containing an unmasked card number and an unauthorized ₹1,500 concession.

#### F. Text Copy & Word Budget
- Headline: 9 words.
- Gap Cards: 24 words total.
- **Total Word Count**: 33 words (Target: $\le 40$).

#### G. Rubric Alignment & Objection Handling
- **Rubric**: Solution & Technical (25%), Problem & Impact (10%).
- **Judge Trap**: *"Couldn't GPT-4o solve this without any extra architecture?"*
- **Bulletproof Counter**: GPT-4o costs 20x more and has 4x higher latency. In real call centers, economics force small models. ClaimGuard proves that deterministic architecture + PRISM allows cheap models to run safely.

---

### Slide 3: Proposed Solution

#### A. Metadata & Prompts (Mandated by Image)
- **Slide Eyebrow**: `Slide 3 Proposed Solution`
- **Mandated Prompt**: `What solution are we proposing and how does it solve the problem?`
- **Headline (Fraunces Display)**: *"The LLM proposes; deterministic code disposes."*

#### B. Spoken Pitch Beat (Presenter Script — 25 seconds)
> *"ClaimGuard introduces a zero-trust enforcement architecture around the small model. We separate intelligence from authority. The model is allowed to propose actions, but deterministic code controls the database commit. When a caller interrupts, our Commit Window freezes actions instantly. When a caller demands a discount, SQLite triggers make financial changes structurally impossible. And our pre-LLM PII shield uses real Luhn checksums to sanitize cards before audio tokens ever reach memory."*

#### C. Layout Grid & Spatial Composition
- **Top Section (15%)**: Eyebrow + prompt + Fraunces thesis statement.
- **Middle Section (55%)**: The **Complete ClaimGuard Architecture Stack (Full SVG)** featuring the animated Commit Window state machine and the flanking PRISM Observability Spine.
- **Bottom Section (30%)**: The Three Architectural Pillars, complete with the KaTeX Luhn Checksum validation equation.

#### D. Visual Engine & Dynamic Components
1. **The Complete ClaimGuard Stack SVG**:
   - `L0 Client Edge` $\rightarrow$ `L1 Perception (Whisper + PII Shield)` $\rightarrow$ `L2 Cognition (3B LLM + BGE-M3 RAG)` $\rightarrow$ `L3 ClaimGuard Enforcement Layer` $\rightarrow$ `L4 System of Record (SQLite)`.
   - Flanking the entire stack is **`L5 PRISM Telemetry Spine`** (glowing violet rail, capturing spans across every layer).
   - `L3 ClaimGuard` contains an active SVG State Machine:
     $$\text{Action Proposed} \longrightarrow \mathbf{HELD} \xrightarrow{\text{Cancel Token}} \mathbf{FROZEN} \xrightarrow{\text{Resolve}} \begin{cases} \mathbf{COMMITTED} & (\text{Valid}) \\ \mathbf{ABORTED} & (\text{Revoked}) \end{cases}$$
2. **The Three Architectural Pillars**:
   - **Pillar 1: Can Be Interrupted (The Commit Window)**  
     Consequential tool calls (`stage_dispatch`) start `HELD`. Any cancellation word instantly moves state to `FROZEN`. A false alarm pauses dispatch for 1 second; it never strands a driver.
   - **Pillar 2: Can't Be Bullied (Policy Latch & Outbound Veto)**  
     Deductibles and liability are locked by SQLite triggers—the model has no tool to write them. An Outbound Veto intercepts any response containing unauthorized ₹ figures or concessions.
   - **Pillar 3: Won't Leak (Pre-LLM Mathematical PII Shield)**  
     Audio is processed locally via whisper.cpp. Card numbers, Aadhaar, and phone numbers are scrubbed **before** the LLM context window using mathematical checksums.

#### E. Mathematical Formulation (KaTeX Integration)
Rendered cleanly under Pillar 3 to prove real algorithmic rigor (not regex placeholder):
$$\sum_{i=1}^{n} f(d_i, i) \equiv 0 \pmod{10}, \quad \text{where } f(d, i) = \begin{cases} d & \text{if } i \text{ odd} \\ 2d - 9 & \text{if } i \text{ even and } 2d > 9 \\ 2d & \text{otherwise} \end{cases}$$
*Caption*: `Luhn Algorithm (ISO/IEC 7812) executed in L1 to prevent false-positive masking on 16-digit policy numbers.`

#### F. Interactive JavaScript Features
- **Interactive State Machine Simulator**: Three buttons on the slide:
  - `[Simulate "Wait, Cancel!"]`: Animates the packet from `HELD` $\rightarrow$ `FROZEN` $\rightarrow$ `ABORTED`.
  - `[Simulate Trap "Don't Hold Back"]`: Animates the packet flickering to `FROZEN`, resolving ambiguity, and advancing to `COMMITTED`.
  - `[Simulate Card Utterance]`: Shows the card digits passing through the Luhn formula and transforming into `[CARD REDACTED]` before entering L2.

#### G. Text Copy & Word Budget
- Headline: 7 words.
- Three Pillars: 22 words.
- **Total Word Count**: 29 words (Target: $\le 40$).

#### H. Rubric Alignment & Objection Handling
- **Rubric**: Solution & Technical (25%), Innovation (10%).
- **Judge Trap**: *"Is this just another prompt guardrail?"*
- **Bulletproof Counter**: No. There is zero LLM in the enforcement path. L3 is compiled, deterministic Python/SQLite code. The model physically cannot commit to the database.

---

### Slide 4: PRISM Usage (The Centerpiece — Big Daddy)

#### A. Metadata & Prompts (Mandated by Image)
- **Slide Eyebrow**: `Slide 4- PRISM Usage`
- **Mandated Prompt**: `How PRISM is used to monitor, evaluate, detect failures, and improve the AI system..`
- **Headline (Fraunces Display)**: *"One instrument, watching every layer."*

#### B. Spoken Pitch Beat (Presenter Script — 30 seconds)
> *"Judges, this is where PRISM acts as the Big Daddy of our entire system. ClaimGuard doesn't treat PRISM as an afterthought telemetry sink. PRISM is our optical lens. It refracts raw, unobserved call data into five operational spectra: per-turn span tracing, unsupervised failure clustering, and root-cause classification. Most critically: PRISM's AI Remediation diagnosed our v0 model's exact sycophancy flaw, recommended prompt patches for v1, and then proved that our v2 ClaimGuard architecture achieved 100% held-out safety without model retraining."*

#### C. Layout Grid & Spatial Composition
- **Hero Centerpiece (60%)**: **The Optical Dispersion Canvas Graphic**. A dynamic light ray tracing simulation where raw white call data enters a crystalline prism and splits into 5 glowing spectral capability beams.
- **Right / Bottom Panel (40%)**: The **Continuous Improvement Loop** showing the 3 tested agent versions (`roadside-baseline`, `roadside-prompt-fix`, `roadside-claimguard`) and the verified before/after metrics delta.

#### D. Visual Engine & Dynamic Components
1. **The PRISM Optical Dispersion Hero (HTML5 Canvas + SVG)**:
   - A brilliant white beam labeled `RAW CALL TELEMETRY (L1-L4)` fires from the left into a central glass prism.
   - Refracts into 5 distinct chromatic wavelengths, each illuminating a core PRISM capability:
     - **Beam 1: Violet (`#8B7CFF`) — Spans & Tracing**: Every LLM call, RAG chunk retrieval, and tool invocation traced with `agent_id`, `category`, and `set=dev|heldout`.
     - **Beam 2: Teal (`#3FD6C9`) — Root Cause Diagnosis**: PRISM classifies failure mechanisms (intent persistence breakdown, sycophantic concession, slot confusion).
     - **Beam 3: Amber (`#FFB84D`) — Agent Intelligence**: Automatic clustering of failure trajectories across conversational sessions.
     - **Beam 4: Rose (`#FF5271`) — AI Remediation**: PRISM's automated prompt patch recommendations generated directly from diagnosed failure clusters.
     - **Beam 5: Emerald (`#2ED573`) — Fleet Comparison**: Cross-version benchmarking comparing reliability scores across model versions.
2. **The 3-Version Improvement Loop**:
   - `v0 Baseline (roadside-baseline)`: Well-prompted model alone $\rightarrow$ Fails on interruptions & pressure.
   - `v1 Prompt-Fix (roadside-prompt-fix)`: Applied PRISM AI Remediation prompt patch $\rightarrow$ Catches simple traps, but state still drifts.
   - `v2 ClaimGuard (roadside-claimguard)`: Deterministic commit window + policy latch $\rightarrow$ **100% safety on held-out NH48 test set**.

#### E. Measured Improvement Telemetry Grid
A live comparative scorecard embedded on-slide (sourced from `Overall-plan.md` §13):
```
+-----------------------------------+--------------------+--------------------+--------------------+
| EVALUATION METRIC (NH48 SET)      | v0 BASELINE        | v1 PRISM REMEDIATED| v2 CLAIMGUARD      |
+-----------------------------------+--------------------+--------------------+--------------------+
| Wrong Commits (Revoked Actions)   | 42% Fail (High)    | 28% Fail (Moderate)| 0% Fail (PERFECT)  |
| Spoken Financial Concessions      | 65% Breached       | 30% Breached       | 0% (L3 Vetoed)     |
| PII Leaks Reaching Context        | 100% Leaked        | 100% Leaked        | 0% (L1 Shielded)   |
| Unneeded Clarifications (Latency) | 0s (Reckless)      | +3.2s (Excessive)  | +0.8s (Grace Win)  |
+-----------------------------------+--------------------+--------------------+--------------------+
```

#### F. Interactive JavaScript Features
- **Interactive Spectrum Explorer**: Clicking any of the 5 spectral beams highlights that specific PRISM subsystem, revealing a live sample JSON span payload and telemetry view.
- **Version Toggle**: Buttons for `[View v0 Spans]`, `[View v1 AI Remediation]`, `[View v2 Fleet Delta]`. Toggling animates the metrics scorecard in real time!

#### G. Text Copy & Word Budget
- Headline: 6 words.
- Spectrum Labels: 15 words.
- Version Loop: 12 words.
- **Total Word Count**: 33 words (Target: $\le 40$).

#### H. Rubric Alignment & Objection Handling
- **Rubric**: PRISM Evaluation & Diagnosis (20%), Measured AI Improvement (20%).
- **Judge Trap**: *"Guardrails are locked on your free tier, so how did you use PRISM?"*
- **Bulletproof Counter**: Exactly by design! ClaimGuard *is* the application-level guardrail; PRISM is the independent observability and audit authority. Traces, sessions, root-cause clustering, AI Remediation, and fleet view are 100% operational on our tier.

---

### Slide 5: System Workflow

#### A. Metadata & Prompts (Mandated by Image)
- **Slide Eyebrow**: `Slide 5-System Workflow`
- **Mandated Flow Prompt**: `Input → AI/RAG/Agent System → PRISM Monitoring & Evaluation → Failure Detection → Improvement`
- **Headline (Fraunces Display)**: *"The same closed loop, every call."*

#### B. Spoken Pitch Beat (Presenter Script — 20 seconds)
> *"Here is the complete operational lifecycle of every call. Audio enters at Input, where local Whisper and our PII shield scrub sensitive data. The AI system proposes tool calls held in our commit window. Node three is PRISM: the pulsing heart of our system, capturing every span. In Node four, PRISM clusters failures and our outbound veto blocks breaches. Finally, Node five feeds AI Remediation back into the loop, continuously re-proving reliability on our held-out test suite."*

#### C. Layout Grid & Spatial Composition
- **Top Section (15%)**: Eyebrow + locked pipeline subtitle + Fraunces headline.
- **Center Stage (65%)**: **Horizontal 5-Node Interactive Workflow Pipeline**. Node 3 (PRISM) is styled as the dominant hero node (1.4x scale with radiating energy particles).
- **Bottom Section (20%)**: The **Curved Closed-Loop Feedback Arc** returning from Node 5 back to Node 1.

#### D. Visual Engine & Dynamic Components
1. **The Mandated 5-Node Pipeline (SVG + CSS Flex)**:
   - **Node 1: Input (Edge & Perception)**  
     *Icon*: Microphone with Shield.  
     *Action*: Hindi/English code-mixed speech captured $\rightarrow$ whisper.cpp $\rightarrow$ Luhn-validated PII scrubbing.
   - **Node 2: AI / RAG / Agent System (Cognition)**  
     *Icon*: CPU with Document.  
     *Action*: 3B Small LLM queries BGE-M3 policy chunks $\rightarrow$ generates candidate tool calls (`HELD`).
   - **Node 3: PRISM Monitoring & Evaluation [THE HERO NODE]**  
     *Visual*: 1.4x scale, glowing spectrum border, animated telemetry wave.  
     *Action*: Spans traced in real time, tagged with `agent_id`, `category`, and session context.
   - **Node 4: Failure Detection (Audit & Veto)**  
     *Icon*: Radar Scan.  
     *Action*: PRISM Agent Intelligence identifies failure clusters; ClaimGuard Outbound Veto suppresses invalid ₹ concessions.
   - **Node 5: Improvement (Closed-Loop Evolution)**  
     *Icon*: Refresh Cycle.  
     *Action*: PRISM AI Remediation suggests prompt/policy patches $\rightarrow$ deployed $\rightarrow$ re-evaluated on held-out set.
2. **The Feedback Arc (Animated SVG Connector)**:
   - A pulsing SVG path loops from Node 5 under the entire pipeline back into Node 1, labeled `Continuous Re-Proving on Held-Out NH48 Dataset`.
3. **Animated Packet Flow**:
   - A glowing data packet continuously travels across the 5 nodes, triggering micro-animations as it passes each stage.

#### E. Interactive JavaScript Features
- **"Step-Through Workflow" Mode**: Presenter can press `Space` to step the packet through Node 1 $\rightarrow$ Node 2 $\rightarrow$ Node 3 $\rightarrow$ Node 4 $\rightarrow$ Node 5.
- **Node Drill-Down**: Clicking Node 3 highlights PRISM's specific API endpoints (`submit_trajectory`, `/api/voice/turns`, span export).

#### F. Text Copy & Word Budget
- Headline: 6 words.
- Node Micro-Labels: 20 words total.
- **Total Word Count**: 26 words (Target: $\le 40$).

#### G. Rubric Alignment & Objection Handling
- **Rubric**: Solution & Technical (25%), PRISM Evaluation (20%).
- **Judge Trap**: *"Does the feedback loop automatically update production prompts without human review?"*
- **Bulletproof Counter**: Never. Consistent with Block Convey's design philosophy, PRISM generates remediation recommendations, but a human engineer must inspect and approve before changes re-deploy.

---

### Slide 6: Impact & Future Scope

#### A. Metadata & Prompts (Mandated by Image)
- **Slide Eyebrow**: `Slide 6-Impact & Future Scope`
- **Mandated Prompt**: `Key benefits, real-world impact, scalability, and future enhancements.`
- **Headline (Fraunces Display)**: *"This failure class isn't insurance-specific. It's every call center."*

#### B. Spoken Pitch Beat (Presenter Script — 25 seconds)
> *"Judges, the failure class we solved—conversational interruption, emotional pressure, and spoken identifiers on small models—exists in every voice agent deployment. Today, ClaimGuard is proven on roadside insurance. Tomorrow, the exact same PRISM-observed architecture scales to Banking IVR under RBI FREE-AI rules, Telecom dispatch, and Emergency Healthcare. We built a system that can be interrupted, can't be bullied, won't leak, and is proven end-to-end by PRISM."*

#### C. Layout Grid & Spatial Composition
- **Top Section (15%)**: Eyebrow + prompt + Fraunces headline.
- **Middle Section (55%)**: **Multi-Domain Scalability Radar (SVG Radial Diagram)** showing Insurance FNOL at the core and radiating to Banking, Telecom, and Healthcare.
- **Bottom Section (30%)**: **Production Roadmap Strip** + Final Pitch Thesis Anchor.

#### D. Visual Engine & Dynamic Components
1. **Multi-Domain Scalability Radar (SVG)**:
   - **Center Core (Built & Verified Today)**:  
     `Insurance FNOL & Roadside Assistance` (Solid emerald glow, active demo on NH48 corridor).
   - **Radial Sector 1: Banking & FinTech IVR (Next Scope)**  
     *Use Case*: Fraud emergency card cancellation & unauthorized transaction disputes.  
     *Compliance*: RBI FREE-AI Framework & PCI DSS v4.0.1.
   - **Radial Sector 2: Telecom & Utilities Dispatch**  
     *Use Case*: Priority fiber outage intake & technician dispatch under high churn pressure.
   - **Radial Sector 3: Emergency Healthcare Intake**  
     *Use Case*: Ambulance dispatch & patient consent recording under India DPDP Act 2023.
2. **Production Engineering Roadmap (Horizontal Changelog Strip)**:
   - `PHASE 1 (TODAY)`: Edge engine, local whisper.cpp, 3B LLM, SQLite triggers, PRISM trace spine.
   - `PHASE 2 (NEXT)`: SIP / Telephony IVR gateway (Exotel / Twilio) connected to L0 audio socket.
   - `PHASE 3 (SCALE)`: Multilingual speech expansion (Tamil, Telugu, Kannada) + PRISM Guardrails in Enforce Mode.
3. **The Final Thesis Anchor (Bottom Monospace Banner)**:
   `Can be interrupted. Can't be bullied. Won't leak. Built to be diagnosed — proven by PRISM.`

#### E. Interactive JavaScript Features
- **Radar Sector Hover**: Hovering over Banking, Telecom, or Healthcare illuminates the regulatory badges and shows how L3 enforcement maps to that industry.
- **Closing Highlight Key (`C`)**: Pressing `C` triggers a final presentation celebration animation where the central PRISM beam illuminates the entire screen.

#### F. Text Copy & Word Budget
- Headline: 9 words.
- Sector Callouts: 12 words.
- Roadmap: 12 words.
- Closing Anchor: 12 words.
- **Total Word Count**: 45 words (Target: $\le 45$).

#### G. Rubric Alignment & Objection Handling
- **Rubric**: Innovation (10%), Problem & Impact (10%), Demo & Pitch (15%).
- **Judge Trap**: *"How hard is it to connect a real phone line?"*
- **Bulletproof Counter**: L0 is an isolated socket interface. Swapping browser audio for a Twilio/Exotel SIP bridge modifies only L0—L1 through L5 remain 100% untouched.

---

## 3. Technical Engine Architecture for Builder Agent

### 3.1 Deliverable Files
The presentation builder agent will generate two standalone HTML files in `/presentation/`:
1. `presentation/claimguard-pitch.html`: Online production file linking Google Fonts and cdnjs libraries.
2. `presentation/claimguard-pitch-offline.html`: Standalone offline file with fallbacks, local styling, and zero external network dependencies (critical for venue Wi-Fi failure).

### 3.2 Slide Deck Core Engine (Vanilla JavaScript, ~150 lines)
The builder agent must not import massive frameworks (no Reveal.js, no Impress.js). Build a clean, self-contained controller:
```javascript
class PitchDeck {
  constructor() {
    this.slides = Array.from(document.querySelectorAll('.slide'));
    this.pips = Array.from(document.querySelectorAll('.nav-pip'));
    this.currentIndex = 0;
    this.totalSlides = this.slides.length;
    this.initEvents();
    this.showSlide(0);
  }

  showSlide(index) {
    if (index < 0 || index >= this.totalSlides) return;
    
    // Deactivate previous
    this.slides[this.currentIndex].classList.remove('active');
    this.pips[this.currentIndex].classList.remove('active');
    this.onSlideLeave(this.currentIndex);

    // Activate new
    this.currentIndex = index;
    this.slides[this.currentIndex].classList.add('active');
    this.pips[this.currentIndex].classList.add('active');
    this.onSlideEnter(this.currentIndex);

    // Update persistent UI counters
    document.getElementById('slide-counter').textContent = 
      `0${this.currentIndex + 1} / 0${this.totalSlides}`;
  }

  next() { this.showSlide(this.currentIndex + 1); }
  prev() { this.showSlide(this.currentIndex - 1); }

  initEvents() {
    window.addEventListener('keydown', (e) => {
      if (['Space', 'ArrowRight', 'PageDown', 'KeyL'].includes(e.code)) this.next();
      if (['ArrowLeft', 'PageUp', 'KeyH'].includes(e.code)) this.prev();
      if (e.key >= '1' && e.key <= '6') this.showSlide(parseInt(e.key) - 1);
      if (e.code === 'KeyF') this.toggleFullscreen();
      if (e.code === 'KeyD') this.toggleDebugHUD();
      if (e.key === '?' || e.code === 'KeyN') this.toggleNotes();
    });

    this.pips.forEach((pip, idx) => {
      pip.addEventListener('click', () => this.showSlide(idx));
    });
  }

  onSlideEnter(idx) {
    // Start specific Canvas rendering loops only when slide is visible to preserve 60fps
    if (idx === 0 && window.startWaveform) window.startWaveform();
    if (idx === 3 && window.startPrismRayTracer) window.startPrismRayTracer();
    if (idx === 4 && window.startPipelineRunner) window.startPipelineRunner();
  }

  onSlideLeave(idx) {
    // Stop canvas render loops when leaving to save CPU
    if (idx === 0 && window.stopWaveform) window.stopWaveform();
    if (idx === 3 && window.stopPrismRayTracer) window.stopPrismRayTracer();
    if (idx === 4 && window.stopPipelineRunner) window.stopPipelineRunner();
  }
}
```

### 3.3 Dynamic Canvas Algorithms
1. **Slide 1 Waveform Algorithm (`AudioWaveformCanvas`)**:
   - Computes multi-sine superposition:
     $$y(x, t) = \sum_{k=1}^{3} A_k \sin(\omega_k x + \phi_k t) \cdot \text{envelope}(x) + \text{noise}(x, t)$$
   - Pin markers draw pulsing radial rings with CSS blur filters.
2. **Slide 4 Prism Dispersion Ray-Tracer**:
   - Renders an equilateral triangle at $(x_c, y_c)$ with glass refractive indices.
   - Incident ray enters from $(0, y_c)$ at angle $\theta_1 = 0^\circ$.
   - Internally splits into 5 rays refracted at angles $\theta_{2, \lambda} = \arcsin(\frac{\sin \theta_1}{n(\lambda)})$.
   - Each chromatic beam projects to the right edge with soft particle glow.

### 3.4 KaTeX Dependency Management
- **Online Build**:
  ```html
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>
  ```
- **Offline Build**:
  The builder will inline the pre-rendered KaTeX HTML/MathML directly into the slide container, guaranteeing zero reliance on external CSS/JS fonts during offline execution.

---

## 4. Speaker Notes & Defense Arsenal (Hot-Key `N`)

The builder agent will embed a slide-out Speaker Notes Drawer accessible via the `N` or `?` key:

| Slide | Primary Spoken Cue | Anticipated Judge Objection & Winning Counter-Punch |
|---|---|---|
| **01 — Problem** | *"Turn four is where conversations break."* | **Q**: *"Is interruption really a safety issue?"*<br>**A**: *"Yes. If a caller cancels a tow because their car restarted, but the agent dispatches anyway, roadside partners waste emergency capacity on false alarms."* |
| **02 — Challenges** | *"Small models are what ships. Nobody demos with them."* | **Q**: *"Why not just use fine-tuning?"*<br>**A**: *"Fine-tuning adjusts probability distributions; it cannot provide mathematical guarantees. A fine-tuned 3B model can still be bullied under high emotional pressure."* |
| **03 — Solution** | *"The LLM proposes; deterministic code disposes."* | **Q**: *"Does the commit window add noticeable lag?"*<br>**A**: *"No. Grace windows are tiered: ambulances dispatch immediately, mechanical tows get 3-5 seconds. The caller perceives it as natural conversation."* |
| **04 — PRISM Usage** | *"One instrument, watching every layer."* | **Q**: *"How did PRISM's AI Remediation help?"*<br>**A**: *"PRISM's Root Cause classified our v0 failures as 'sycophantic concession.' It generated exact system prompt constraints that fixed 50% of the failures in v1."* |
| **05 — Workflow** | *"The same closed loop, every call."* | **Q**: *"Why not run PRISM asynchronously?"*<br>**A**: *"Telemetry spans emit asynchronously to preserve <500ms latency. PRISM receives 100% of production spans without blocking caller audio."* |
| **06 — Impact** | *"This failure class is every call center."* | **Q**: *"Can this run on edge devices?"*<br>**A**: *"Yes. whisper.cpp + 3B llama.cpp runs on a single consumer GPU (RTX 3060/4060/5080) or apple silicon Mac. Zero external cloud API dependencies."* |

---

## 5. Builder Agent Verification Checklist (Definition of Done)

Before marking the deck build complete, the builder agent must verify:
- [ ] **Exact 6 Slides**: Follows the exact order, mandated titles, and mandated image subtitles.
- [ ] **PRISM Prominence**: PRISM is named on Slide 1, acts as the visual centerpiece on Slide 4, is the dominant hero node on Slide 5, and delivers the closing line on Slide 6.
- [ ] **Strict Word Ceilings**: No slide exceeds 40 words of prose.
- [ ] **Zero AI Slop**: No generic gradients, no robot emojis, no marketing fluff. Clean, editorial typography (`Fraunces` + `IBM Plex`).
- [ ] **Real LaTeX Rendered**: The Luhn algorithm is properly typeset via KaTeX on Slide 3.
- [ ] **Interactive Widgets Working**: Waveform canvas on Slide 1, state-machine simulator on Slide 3, optical dispersion canvas on Slide 4, and packet runner on Slide 5 are fully interactive.
- [ ] **Dual Resolution Verified**: Scales smoothly at both 1920x1080 and 1366x768 without layout breaks.
- [ ] **Offline Standalone File**: `claimguard-pitch-offline.html` opens and executes completely with Wi-Fi disabled.
- [ ] **Honesty Invariants Maintained**: No fabricated numbers; CSAT is correctly identified; fictional insurer identity preserved.
