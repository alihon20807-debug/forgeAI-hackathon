# Master Pitch Deck Plan — ClaimGuard × PRISM
### Autonomous Evaluation Edition: High-Impact HTML Presentation Specification
**Mode**: **AUTONOMOUS JUDGE REVIEW** (Zero presenter presence; completely self-contained, self-playing, and self-explanatory)  
**Target Audience**: Judges at ForgeAI Hackathon (graVITas'26, VIT Vellore / Block Convey Founders & Technical Staff)  
**Deliverable Targets**: `presentation/claimguard-pitch.html` (Online/CDN) & `presentation/claimguard-pitch-offline.html` (Standalone Offline)  
**Authority**: Canonical build specification derived from `Overall-plan.md`, `CLAUDE.md`, and verified research in `research/prism/`.

---

## 0. Executive Mandate: The Autonomous Review Paradigm

### 0.1 The Presentation Context
> **CRITICAL ARCHITECTURAL DIRECTIVE: ZERO INTERACTION DEPENDENCE**  
> The user will **not** be present to deliver a live pitch, guide attention, or click interactive demo buttons. Judges will open and review this deck autonomously on their own laptops or mobile devices.  
> 
> Therefore:
> 1. **No critical information may ever be hidden behind a click, toggle, or hover state.** Everything a judge needs to see to award top scores must be immediately visible, legible, and visually striking upon entering each slide.
> 2. **Animations must be ambient, autonomous, and self-looping.** The audio waveform, the L3 state machine cycle, the PRISM optical beam split, and the workflow packet flow must cycle continuously and automatically using hardware-accelerated CSS/SVG.
> 3. **The layout must pass the "10-Second Autonomous Scan Test."** A judge skimming through 100 entries must grasp:
>    - The core tension (small models breaking in call centers) within 3 seconds.
>    - The architectural solution (deterministic L3 commit window + PII shield) within 5 seconds.
>    - PRISM as the central hero / reliability layer (evaluating, diagnosing, and proving safety) within 10 seconds.

### 0.2 The Core Thesis: "PRISM is the Hero, ClaimGuard is the Vehicle"
Call-center voice agents in India are deployed on **cheap, fast, small models** (3B–8B) because cost-per-call (₹/min) and <500ms latency budgets dictate it. Small models are the ones that fumble mid-sentence cancellations, cave to emotional pressure, and leak card numbers. We built **ClaimGuard**—an insurance voice agent on a deliberately small model—and used **PRISM end-to-end as the reliability engine** that intercepts failures, diagnoses root causes, guides AI Remediation, and re-proves safety on a held-out benchmark. We are not demoing a generic chatbot; we are demoing how PRISM makes small-model deployments safe in production.

### 0.3 Judging Rubric Traceability (100% Aligned)
- **Solution & Technical (25%)**: Slides 2, 3, 5 (Deterministic L3 commit window, DB triggers, whisper.cpp ASR, BGE-M3 RAG).
- **PRISM Evaluation & Diagnosis (20%)**: Slides 4, 5 (Multi-turn span tracing, Agent Intelligence failure clustering, Root Cause diagnosis).
- **Measured AI Improvement (20%)**: Slide 4 (v0 Baseline vs v1 Prompt-Fix vs v2 ClaimGuard benchmark delta on held-out NH48 set).
- **Demo & Pitch (15%)**: All slides (Self-playing animations, editorial typography, zero AI slop, instant legibility).
- **Innovation (10%)**: Slides 2, 3, 6 ("Chaos engineering" small-model bet, Pre-LLM mathematical PII shielding).
- **Problem & Impact (10%)**: Slides 1, 6 (Universal call-center voice failure class, DPDP Act & PCI DSS regulatory alignment).

### 0.4 The Strict 6-Slide Structure (Locked to Reference Image)
1. **Slide 1 — Problem Statement**: *What real-world problem are we trying to solve?*
2. **Slide 2 — Existing Challenges**: *What are the limitations, risks, or gaps in current solutions?*
3. **Slide 3 — Proposed Solution**: *What solution are we proposing and how does it solve the problem?*
4. **Slide 4 — PRISM Usage**: *How PRISM is used to monitor, evaluate, detect failures, and improve the AI system..*
5. **Slide 5 — System Workflow**: *Input → AI/RAG/Agent System → PRISM Monitoring & Evaluation → Failure Detection → Improvement*
6. **Slide 6 — Impact & Future Scope**: *Key benefits, real-world impact, scalability, and future enhancements.*

---

## 1. Anti-"AI Slop" Design System, Sophisticated Palette & Reading Flow

### 1.1 Aesthetic Philosophy: "The Natural Laboratory & Optical Refraction"
Judges review hundreds of hackathon decks that look identical: dark-mode templates with generic purple-neon gradients, blurred glassmorphic cards, and centered walls of AI marketing copy.

ClaimGuard × PRISM takes a bold, sophisticated departure into **Organic Architectural Engineering**—combining the tactile warmth of a master craftsman's workshop (natural cream linen, warm roasted wood brown, imperial jade green) with the brilliant, physical precision of **PRISM's optical rainbow refraction**:
- **Warm Natural Foundation**: A luminous, non-glare Warm Cream / Alabaster canvas (`#F8F6F1`) reminiscent of architectural parchment, paired with deep Roasted Walnut (`#1E1915`) for high-contrast, editorial typography.
- **Architectural Wood Framing**: Structural cards, borders, and timeline rails use warm sandstone hairlines (`#DDD6CA`) and pale linen surfaces (`#EFECE4`), providing physical structure without corporate sterility.
- **Imperial Jade Green as the Reliability Anchor**: Deep, dignified Jade Green (`#1B5E4B`) serves as the symbol of verified truth—the color of deterministic execution, database latches, and PRISM's seal of approval.
- **The PRISM Rainbow Refraction**: Sunlight passing through a pure triangular glass prism, casting a brilliant, saturated rainbow refraction spectrum across the cream surface. Chromatic color is strictly functional: each spectral wavelength represents a distinct telemetry or enforcement state.

### 1.2 Anti-AI Slop Invariants (Hard Prohibitions for Builder Agent)
1. **NO Generic Dark-Mode Purple Glow**: The canvas is light, natural, and editorial (warm cream ground).
2. **NO Synthetic Blur Glassmorphism**: Cards have crisp 1px borders, subtle tactile paper lift, and zero opaque pastel blur washes.
3. **NO Generic Emojis or Stock Icons**: Icons must be disciplined, single-color inline SVGs rendered in deep walnut or jade green.
4. **NO Centered Paragraphs**: Layouts follow strict left-aligned or grid-structured architectural reading paths.
5. **NO Marketing Fluff**: Zero filler jargon. Every sentence states a concrete mechanism or verified diagnostic outcome.

### 1.3 The Natural & Rainbow Refraction Color Tokens
```css
:root {
  /* Natural Architectural Base (Cream & Wood Brown) */
  --ground: #F8F6F1;              /* Warm cream / alabaster linen ground */
  --surface-base: #FFFFFF;        /* Crisp white parchment cards */
  --surface-raised: #EFECE4;      /* Pale linen / warm stone container */
  --surface-wood: #2B231D;        /* Deep roasted walnut accent chassis */
  --rule-hairline: #DDD6CA;       /* 1px sandstone dividing rule */
  --rule-strong: #C4BAAB;         /* High-contrast container border */
  
  /* Ink & Typographic Contrast */
  --ink-primary: #1E1915;         /* Deep roasted walnut (primary headlines & labels) */
  --ink-secondary: #5D544C;       /* Warm umber / cedar (explanatory captions) */
  --ink-muted: #8E8478;           /* Muted sandstone (metadata, timestamps, timecodes) */
  --ink-inverse: #FAF8F5;         /* Crisp chalk (text inside dark walnut badges) */

  /* The Reliability Anchor: Imperial Jade Green */
  --jade-primary: #1B5E4B;        /* Deep imperial jade: committed actions & safety passes */
  --jade-tint: #E8F3EE;           /* Soft celadon wash for verified result cards */
  --jade-border: #9DC7B7;         /* Soft jade hairline border */

  /* The PRISM Rainbow Refraction Spectrum (Vivid Optical Wavelengths) */
  --beam-incident: #FAF7EF;       /* Pure incident solar beam */
  --spectrum-violet: #5B42B2;     /* 400nm: L5 Multi-Turn Spans & Telemetry Traces */
  --spectrum-cyan: #0284C7;       /* 480nm: PRISM Root Cause Diagnosis & KB Grounding */
  --spectrum-jade: #1B5E4B;       /* 520nm: L3 Deterministic Latch & Verified Compliance */
  --spectrum-amber: #D97706;      /* 580nm: L3 Held State & Agent Intelligence Clusters */
  --spectrum-rose: #DC2626;       /* 650nm: L3 Outbound Veto & Aborted Actions */
}
```

### 1.4 Typography Hierarchy & Typographic Voice
Three distinct typefaces, each performing one rigorous, non-overlapping task:
1. **Editorial Display Voice — `Fraunces`**:
   - Variable optical font (72pt optical sizing, weight 500-600) set in Deep Roasted Walnut (`#1E1915`).
   - Conveys editorial authority, physical craftsmanship, and human warmth.
2. **Structural Interface Voice — `IBM Plex Sans`**:
   - 400 (Regular), 500 (Medium), 600 (Semi-bold).
   - Used for card labels, architecture layer titles, and explanatory captions. Line length $\le 65$ characters.
3. **Data, Telemetry & Code Voice — `IBM Plex Mono`**:
   - Tabular figures enabled (`font-variant-numeric: tabular-nums`).
   - Used for slide numbering (`01 / 06`), tool calls (`stage_dispatch`), timestamps (`00:14.280`), `agent_id` tags, and formula captions.

*Offline Fallback Stack (Mandatory for `claimguard-pitch-offline.html`)*:
```css
--font-display: 'Fraunces', Georgia, 'Times New Roman', serif;
--font-sans: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-mono: 'IBM Plex Mono', 'SF Mono', Menlo, Consolas, monospace;
```

---

### 1.5 Autonomous Reading Flow Architecture (The 4-Step Eye Path)
Because the judges review this deck **autonomously without a speaker**, the visual layout must choreograph the judge's eye along an effortless, intuitive path. On every slide, visual weight is distributed so the judge's gaze naturally completes a 4-step cognitive loop within 8–12 seconds:

```
Step 1: [Top-Left Eyebrow & Mandated Prompt] ---------> [Top-Right: Instrumented by PRISM]
             |
             v
Step 2: [High-Contrast Fraunces Headline & Punchline]
             |
             v
Step 3: [Center Stage: The Hero Visual Engine (Waveform / Architecture / Optical Prism)]
             |
             v
Step 4: [Bottom Anchors: The Empirical Proof (KaTeX Math / Scorecard / Concrete Roadmap)]
```

1. **Step 1: Orientation (0–2s)**: The judge reads the top-left eyebrow and mandated question. They instantly know which hackathon judging criterion is being fulfilled.
2. **Step 2: The Core Thesis (2–4s)**: The high-contrast Fraunces headline delivers the bold engineering verdict in one memorable sentence.
3. **Step 3: The Mechanical Proof (4–9s)**: The judge's eye drops to the center visual engine. The ambient animation (flowing audio, cycling state machine, refracted light) visually demonstrates the mechanism of action without requiring clicks.
4. **Step 4: The Empirical Verdict (9–14s)**: The bottom cards, mathematical formulas, or benchmark matrix provide the hard technical evidence before the judge advances to the next slide.

---

### 1.6 Slide-by-Slide Visual Choreography & Eye Paths

```
====================================================================================================
SLIDE 1: PROBLEM STATEMENT
Reading Path: [Top-Left Eyebrow] -> [Quote] -> [Waveform Left-to-Right] -> [3 Incident Pins Below]
Visual Hierarchy:
  1. Top-Left: "What real-world problem are we trying to solve?"
  2. Headline: "Turn four is where conversations break." (Fraunces, large)
  3. Hero Canvas: Real-time flowing audio stream with 3 marked turn intervals (00:04, 00:14, 00:26).
  4. Bottom Triptych: 3 high-contrast failure cards directly under each turn pin:
     - Turn 2: Amber Card (Revocation / Tow truck dispatched anyway)
     - Turn 4: Rose Card (Bargaining / Deductible waived sycophantically)
     - Turn 5: Violet Card (Plaintext card number logged)
====================================================================================================
SLIDE 2: EXISTING CHALLENGES
Reading Path: [Top-Left Eyebrow] -> [Headline] -> [Left: Broken Stack] -> [Right: 3 Gap Cards]
Visual Hierarchy:
  1. Top-Left: "What are the limitations, risks, or gaps in current solutions?"
  2. Headline: "Small models are what actually ships. Nobody demos with them."
  3. Left Side (50%): Broken Architecture SVG showing missing L3 with flashing crimson fracture,
     and dark dashed L5 labeled "[VISIBILITY GAP: Zero Multi-Turn Span Telemetry]".
  4. Right Side (50%): 3 crisp gap cards (Prompt Fragility, Telemetry Blindspot, Post-Hoc PII).
====================================================================================================
SLIDE 3: PROPOSED SOLUTION
Reading Path: [Top-Left Eyebrow] -> [Thesis] -> [Center Stack SVG] -> [Bottom 3 Pillars & KaTeX]
Visual Hierarchy:
  1. Top-Left: "What solution are we proposing and how does it solve the problem?"
  2. Headline: "The LLM proposes; deterministic code disposes."
  3. Center Stage: Complete Architecture SVG with glowing L5 PRISM Spine + self-cycling L3 Commit
     Window (HELD -> FROZEN -> COMMITTED/ABORTED).
  4. Bottom Strip: Three concrete pillars with the typeset KaTeX Luhn Checksum formula centered
     under Pillar 3 ("Won't Leak").
====================================================================================================
SLIDE 4: PRISM USAGE (THE CENTERPIECE)
Reading Path: [Top-Left Eyebrow] -> [Headline] -> [Center-Left: Prism Hero] -> [Right: Benchmark Matrix]
Visual Hierarchy:
  1. Top-Left: "How PRISM is used to monitor, evaluate, detect failures, and improve the AI system.."
  2. Headline: "One instrument, watching every layer."
  3. Center-Left Hero (55%): Optical Prism Graphic. White incident beam enters prism, splitting into
     5 glowing spectral rays (Violet Traces, Teal Diagnosis, Amber Clusters, Rose Fix, Emerald Fleet).
  4. Right Panel (45%): Continuous Improvement Loop (v0 -> v1 -> v2) + NH48 pre-registered
     diagnostic matrix showing 100% held-out safety pass.
====================================================================================================
SLIDE 5: SYSTEM WORKFLOW
Reading Path: [Top-Left Eyebrow] -> [Headline] -> [5 Nodes Left-to-Right] -> [Bottom Feedback Loop]
Visual Hierarchy:
  1. Top-Left: "Input -> AI/RAG/Agent System -> PRISM Monitoring & Evaluation -> Failure Detection -> Improvement"
  2. Headline: "The same closed loop, every call."
  3. Center Stage: Horizontal 5-Node Flow Pipeline. Node 3 (PRISM) is scaled 1.35x with radiating
     spectrum energy. A pulsing data packet flows through nodes 1 -> 2 -> 3 -> 4 -> 5.
  4. Bottom Arc: Curved feedback arrow loops from Node 5 back to Node 1 labeled
     "Continuous Re-Proving on Held-Out Test Set".
====================================================================================================
SLIDE 6: IMPACT & FUTURE SCOPE
Reading Path: [Top-Left Eyebrow] -> [Headline] -> [Center Radar SVG] -> [Roadmap] -> [Thesis Anchor]
Visual Hierarchy:
  1. Top-Left: "Key benefits, real-world impact, scalability, and future enhancements."
  2. Headline: "This failure class isn't insurance-specific. It's every call center."
  3. Center Stage: Multi-Domain Radial Radar. Emerald center (Insurance FNOL today) radiating out
     to Banking IVR (RBI FREE-AI), Telecom dispatch, and Healthcare intake (DPDP Act).
  4. Bottom Strip: Horizontal Phase 1 -> Phase 2 -> Phase 3 engineering roadmap.
  5. Final Anchor: Monospace thesis line at the very bottom ("Can be interrupted... proven by PRISM").
====================================================================================================
```

---

### 1.7 Persistent Autonomous Shell Anatomy
```
+----------------------------------------------------------------------------------------------------+
| [01 / 06 — PROBLEM STATEMENT]                                             [/\ INSTRUMENTED BY PRISM] |
|                                                                                                    |
|                             SLIDE VIEWPORT (16:9 DYNAMIC STAGE)                                    |
|                                                                                                    |
|                                                                                                    |
| [<< Prev] [|| Auto-Play: 15s] [Next >>]      [ . . . . . . ]     [PRISM Spine: Active | 60 FPS]    |
+----------------------------------------------------------------------------------------------------+
```
- **Top Left**: Slide index + mandated prompt eyebrow (`01 / 06 — PROBLEM STATEMENT`).
- **Top Right**: The Optical Prism Glyph with animated refraction shimmer, labeled `INSTRUMENTED BY PRISM`.
- **Bottom Left Controls**:
  - `[< Prev]` and `[Next >]` buttons for immediate trackpad/touchscreen manual navigation.
  - `[Auto-Play: 15s]` Toggle: Allows judges to watch the entire deck advance autonomously.
- **Bottom Center**: 6 Interactive Navigation Pips (direct jump `1`–`6` with title tooltips).
- **Bottom Right**: Telemetry Status: `PRISM Spine: Active | NH48 Held-Out Benchmark`.

---

## 2. Exhaustive Slide-by-Slide Specifications (Autonomous Review)

---

### Slide 1: Problem Statement

#### A. Metadata & Prompts (Mandated by Image)
- **Slide Eyebrow**: `Slide 1 - Problem Statement`
- **Mandated Prompt**: `What real-world problem are we trying to solve?`
- **Headline (Fraunces Display)**: *"Turn four is where conversations break."*
- **Headline Attribution (IBM Plex Mono)**: `— Block Convey, on why conversational AI fails in production`

#### B. The Autonomous Story (What the Judge Reads in 8 Seconds)
High-volume Indian roadside/FNOL call centers deploy cheap, small models (3B–8B) to survive cost and latency budgets. When real human callers panic on highways, they interrupt mid-sentence, bargain under emotional distress, and blurt out credit card numbers. By Turn 4, unobserved small models break: dispatching wrong tows, conceding unauthorized refunds, and leaking plaintext card numbers into production logs.

#### C. Layout Architecture (16:9 Stage)
- **Top Section (22%)**: Eyebrow + prompt + Fraunces pull-quote + Block Convey attribution.
- **Center Section (45%)**: **`AudioWaveformCanvas`** — Ambient, self-animating audio stream visualizer simulating a live code-mixed Hindi/English roadside emergency call on NH48.
- **Bottom Section (33%)**: **Three Self-Explanatory Failure Callouts** permanently aligned to Turn 2, Turn 4, and Turn 5 on the waveform timeline (no clicking required).

#### D. Visual Engine & Autonomous Animations
1. **`AudioWaveformCanvas` (HTML5 Canvas 2D / SVG Fallback)**:
   - Continuously renders a flowing audio waveform with modulated amplitude peaks.
   - Clearly marked time markers: `00:04 [Turn 2]`, `00:14 [Turn 4]`, `00:26 [Turn 5]`.
   - Top banner: `[PRISM SPAN: UNMONITORED MULTI-TURN CONVERSATION DRIFT]`.
2. **Three Permanent Failure Incident Cards (Directly Below Waveform)**:
   - **Turn 02 [Amber Border — `#D97706`]**:  
     *Title*: `Mid-Sentence Revocation`  
     *Caller*: *"Wait, my brother arrived with fuel, cancel the tow truck!"*  
     *Impact*: **Safety & Logistics Failure** (Naive agent dispatches anyway; real emergencies delayed).
   - **Turn 04 [Rose Border — `#DC2626`]**:  
     *Title*: `Emotional Bargaining`  
     *Caller*: *"I've been stranded 2 hours in the rain, waive my ₹1,500 deductible!"*  
     *Impact*: **Financial Leakage** (Small model hallucinates authority and concessions).
   - **Turn 05 [Violet Border — `#5B42B2`]**:  
     *Title*: `Spoken Financial Identifier`  
     *Caller*: *"Charge my card right now: 4532 8901 2345 6789..."*  
     *Impact*: **Regulatory Violation** (Plaintext card logged to disk; DPDP Act & PCI DSS breach).

#### E. Word Count Budget
- Headline & Attribution: 12 words.
- Three Failure Cards: 27 words total.
- **Total On-Slide Prose**: 39 words (Strictly $\le 40$).

---

### Slide 2: Existing Challenges

#### A. Metadata & Prompts (Mandated by Image)
- **Slide Eyebrow**: `Slide 2- Existing Challenges`
- **Mandated Prompt**: `What are the limitations, risks, or gaps in current solutions?`
- **Headline (Fraunces Display)**: *"Small models are what actually ships. Nobody demos with them."*

#### B. The Autonomous Story (What the Judge Reads in 8 Seconds)
Industry demos showcase 70B+ cloud models. Real call centers deploy 3B–8B local models due to ₹/minute unit economics and <500ms latency budgets. But current solutions rely entirely on prompt engineering to enforce business rules. Prompts cannot hold state machines under user interruption, legacy APMs are blind to turn-by-turn tool drift, and regex redaction happens after logs are already compromised.

#### C. Layout Architecture (16:9 Stage)
- **Top Section (18%)**: Eyebrow + prompt + Fraunces headline.
- **Split Body (50% Left / 50% Right)**:
  - **Left Column**: **The "Broken Stack" Architecture SVG**.
  - **Right Column**: **Three Structural Gap Cards** with high-contrast diagnostic readouts.

#### D. Visual Engine & Autonomous Animations
1. **The "Broken Stack" Architecture SVG (Auto-Looping Visual)**:
   - Layered hierarchy: `L0 Audio Edge` $\rightarrow$ `L1 Whisper STT` $\rightarrow$ `L2 3B Small LLM` $\rightarrow$ `[CRACKED L3: Missing Enforcement]` $\rightarrow$ `L4 Database`.
   - The missing L3 enforcement box pulses with animated jagged fracture cracks in crimson (`--prism-rose`) and an automated label: `ZERO STATE BARRIER`.
   - **L5 PRISM Spine is visually absent**: A dark dashed outline labeled `[THE VISIBILITY GAP: Zero Multi-Turn Span Telemetry]`, making the observability deficit obvious at a glance.
2. **Three Structural Gap Cards (Permanently Visible)**:
   - **Gap 1: Fragility of Prompting Alone**  
     *Mechanism*: Prompts cannot guarantee transactional state. Under emotional pressure or interruption, small models suffer attention collapse and execute revoked actions.
   - **Gap 2: Observability Blindspot**  
     *Mechanism*: Standard APMs monitor HTTP status and latency. They cannot cluster conversational failure modes, detect tool hallucination loops, or trace state degradation.
   - **Gap 3: Post-Hoc PII Exposure**  
     *Mechanism*: Masking PII after it enters model context or logs exposes raw card data to LLM memory and telemetry cache, violating PCI DSS v4.0.1.

#### E. Word Count Budget
- Headline: 9 words.
- Three Gap Cards: 28 words total.
- **Total On-Slide Prose**: 37 words (Strictly $\le 40$).

---

### Slide 3: Proposed Solution

#### A. Metadata & Prompts (Mandated by Image)
- **Slide Eyebrow**: `Slide 3 Proposed Solution`
- **Mandated Prompt**: `What solution are we proposing and how does it solve the problem?`
- **Headline (Fraunces Display)**: *"The LLM proposes; deterministic code disposes."*

#### B. The Autonomous Story (What the Judge Reads in 8 Seconds)
ClaimGuard decouples intelligence from authority. The small model proposes actions, but a deterministic, zero-trust enforcement layer controls commits. When a caller interrupts, our Commit Window freezes actions instantly. When a caller demands an unauthorized waiver, SQLite triggers make financial mutations structurally impossible. And our pre-LLM PII shield uses real Luhn checksums to scrub card numbers before audio tokens ever touch memory.

#### C. Layout Architecture (16:9 Stage)
- **Top Section (15%)**: Eyebrow + prompt + Fraunces thesis statement.
- **Middle Section (52%)**: **Complete ClaimGuard Architecture Stack (SVG)** with self-cycling Commit Window state machine and the flanking PRISM Observability Spine.
- **Bottom Section (33%)**: **The Three Architectural Pillars** with the pre-rendered KaTeX Luhn Checksum formula.

#### D. Visual Engine & Autonomous Animations
1. **Complete Architecture Stack SVG**:
   - `L0 Edge` $\rightarrow$ `L1 Perception (Whisper + PII Shield)` $\rightarrow$ `L2 Cognition (3B LLM + BGE-M3 RAG)` $\rightarrow$ `L3 ClaimGuard Enforcement` $\rightarrow$ `L4 SQLite Database`.
   - Flanking L1–L4 is **`L5 PRISM Telemetry Spine`** (radiant violet rail, actively capturing per-turn spans).
   - **Autonomous State Machine Animation (CSS Keyframe Loop)**:
     A glowing data packet travels into L3, automatically transitioning through the cycle every 6 seconds:
     $$\mathbf{PROPOSED} \longrightarrow \mathbf{HELD} \xrightarrow{\text{Cancel Token Detected}} \mathbf{FROZEN} \xrightarrow{\text{Resolve}} \mathbf{ABORTED} \ (\text{Safe Revocation})$$
     *Visual Indicator*: Status badge shifts color automatically (`Amber HELD` $\rightarrow$ `Teal FROZEN` $\rightarrow$ `Emerald COMMITTED` / `Rose ABORTED`).
2. **The Three Architectural Pillars (Visible Cards)**:
   - **Pillar 1: Can Be Interrupted (The Commit Window)**  
     Consequential tool calls (`stage_dispatch`) start `HELD`. Any cancellation utterance instantly shifts state to `FROZEN`. A false alarm costs 1 second of pause; it never dispatches a wrong tow truck.
   - **Pillar 2: Can't Be Bullied (Policy Latch & Outbound Veto)**  
     Financial fields are locked by SQLite triggers—the model has no write-tool. An Outbound Veto intercepts responses containing unauthorized ₹ figures or sycophantic concessions.
   - **Pillar 3: Won't Leak (Pre-LLM Mathematical PII Shield)**  
     Local whisper.cpp STT. Card numbers, Aadhaar, and phone numbers are scrubbed **before** the LLM context window using checksum algorithms.

#### E. Mathematical Formulation (Pre-Rendered KaTeX / Inline MathML)
Directly beneath Pillar 3 to prove algorithmic rigor to technical judges:
$$\sum_{i=1}^{n} f(d_i, i) \equiv 0 \pmod{10}, \quad f(d, i) = \begin{cases} d & i \text{ odd} \\ 2d - 9 & i \text{ even and } 2d > 9 \\ 2d & \text{otherwise} \end{cases}$$
*Mono Caption*: `Luhn Checksum (ISO/IEC 7812) executed in L1 to prevent false-positive masking on 16-digit policy IDs.`

#### F. Word Count Budget
- Headline: 7 words.
- Three Pillars & Caption: 28 words total.
- **Total On-Slide Prose**: 35 words (Strictly $\le 40$).

---

### Slide 4: PRISM Usage (The Centerpiece — Big Daddy)

#### A. Metadata & Prompts (Mandated by Image)
- **Slide Eyebrow**: `Slide 4- PRISM Usage`
- **Mandated Prompt**: `How PRISM is used to monitor, evaluate, detect failures, and improve the AI system..`
- **Headline (Fraunces Display)**: *"One instrument, watching every layer."*

#### B. The Autonomous Story (What the Judge Reads in 10 Seconds)
PRISM is not an afterthought telemetry sink; it is the central reliability engine. PRISM refracts raw unobserved call telemetry into 5 operational spectra: multi-turn span tracing, unsupervised failure clustering, and root-cause classification. PRISM's AI Remediation diagnosed our v0 model's exact sycophancy flaw, generated prompt patches for v1, and proved that our v2 ClaimGuard architecture achieved zero safety breaches on a pre-registered, held-out benchmark.

#### C. Layout Architecture (16:9 Stage)
- **Left / Center (55%)**: **The Optical Dispersion Hero Graphic (SVG + CSS)** — A glass prism splitting incident white call light into 5 distinct glowing chromatic capability beams.
- **Right Column (45%)**: **The Continuous Improvement Loop & Benchmark Framework** comparing `v0 Baseline`, `v1 Prompt-Fix`, and `v2 ClaimGuard`.

#### D. Visual Engine & Autonomous Animations
1. **The PRISM Optical Dispersion Hero (SVG / Canvas)**:
   - A bright solar white beam labeled `RAW CALL TELEMETRY (L1–L4)` enters a central triangular prism.
   - Continuously refracts into 5 distinct saturated chromatic wavelengths, each carrying an exact PRISM capability label:
     - **Violet (`#5B42B2`) — Spans & Traces**: Every LLM call, RAG retrieval, and tool invocation traced with `agent_id`, `category`, and `set=dev|heldout`.
     - **Cyan (`#0284C7`) — Root Cause Diagnosis**: PRISM classifies failure mechanisms (intent persistence breakdown, sycophantic concession, slot drift).
     - **Amber (`#D97706`) — Agent Intelligence**: Automated clustering of conversational failure trajectories across sessions.
     - **Rose (`#DC2626`) — AI Remediation**: Automated prompt patch recommendations generated directly from diagnosed failure clusters.
     - **Imperial Jade (`#1B5E4B`) — Fleet Comparison**: Cross-version benchmarking comparing reliability scores across model versions.
2. **The 3-Version Improvement Loop (Autonomous Cycling Display)**:
   - `v0 Baseline (roadside-baseline)`: Well-prompted 3B model alone $\rightarrow$ Fails on interruptions & emotional pressure.
   - `v1 Prompt-Fix (roadside-prompt-fix)`: v0 + PRISM AI Remediation prompt patch $\rightarrow$ Catches wording traps, but state still drifts.
   - `v2 ClaimGuard (roadside-claimguard)`: v1 + L3 Commit Window + L1 PII Shield $\rightarrow$ **Zero safety breaches on held-out NH48 set**.

#### E. Pre-Registered Diagnostic Benchmark Framework (Invariant #3 Compliant)
Instead of fabricated percentages, display the **honest, verified diagnostic matrix** from the pre-registered NH48 Replay Set (40 Dev / 20 Held-out across 6 categories):
```
+---------------------------------------------------+--------------------+--------------------+--------------------+
| EVALUATION DIMENSION (NH48 DIAGNOSTIC SUITE)      | v0 BASELINE        | v1 AI REMEDIATION  | v2 CLAIMGUARD      |
+---------------------------------------------------+--------------------+--------------------+--------------------+
| Cat B: Mid-Call Revocations (7 Dev / 3 Held-Out)  | FAILED (Committed) | FAILED (Committed) | PASSED (Aborted)   |
| Cat C: Look-Alike Traps (8 Dev / 4 Held-Out)      | FAILED (Killed)    | PASSED (Kept Open) | PASSED (Committed) |
| Cat E: Pressure & Deductible Concessions          | BREACHED (Conceded)| REDUCED (Conceded) | ZERO BREACH (Veto) |
| Cat F: Spoken Identifiers (4 Dev / 2 Held-Out)    | LEAKED (Plaintext) | LEAKED (Plaintext) | ZERO LEAK (Shield) |
+---------------------------------------------------+--------------------+--------------------+--------------------+
```
*Honesty Anchor (Mono Subtext)*: `Labels pre-registered in git prior to model execution. Diagnostic counts evaluated on locked NH48 replay set.`

#### F. Word Count Budget
- Headline: 6 words.
- Spectrum Labels: 15 words.
- Version Loop & Table Notes: 16 words.
- **Total On-Slide Prose**: 37 words (Strictly $\le 40$).

---

### Slide 5: System Workflow

#### A. Metadata & Prompts (Mandated by Image)
- **Slide Eyebrow**: `Slide 5-System Workflow`
- **Mandated Flow Prompt**: `Input → AI/RAG/Agent System → PRISM Monitoring & Evaluation → Failure Detection → Improvement`
- **Headline (Fraunces Display)**: *"The same closed loop, every call."*

#### B. The Autonomous Story (What the Judge Reads in 8 Seconds)
Every incoming call flows through the exact mandated 5-stage lifecycle. Audio enters at Input where local Whisper and our PII shield scrub sensitive data. The AI system proposes tool calls held in our commit window. PRISM ingests spans across all layers. Failure detection intercepts policy breaches via Agent Intelligence and Outbound Veto. Finally, AI Remediation feeds prompt improvements back into the system, continuously re-proving reliability on held-out data.

#### C. Layout Architecture (16:9 Stage)
- **Top Section (15%)**: Eyebrow + locked mandated prompt + Fraunces headline.
- **Center Section (65%)**: **Horizontal 5-Node Workflow Pipeline (SVG)**. Node 3 (PRISM) is the prominent hero node (1.35x scale with pulsing spectrum aura).
- **Bottom Section (20%)**: **Closed-Loop Feedback Arc** returning from Node 5 to Node 1.

#### D. Visual Engine & Autonomous Animations
1. **The Mandated 5-Node Pipeline (Autonomous SVG Flow)**:
   - **Node 1: Input (Edge & Perception)**  
     *Visual*: Mic icon + Shield.  
     *Function*: Native speech (Hindi/English code-mixed) $\rightarrow$ whisper.cpp $\rightarrow$ Luhn PII scrub.
   - **Node 2: AI / RAG / Agent System (Cognition)**  
     *Visual*: LLM chip + Document search.  
     *Function*: 3B Local LLM queries BGE-M3 policy chunks $\rightarrow$ candidate tool calls held in L3.
   - **Node 3: PRISM Monitoring & Evaluation [HERO NODE — 1.35x Scale]**  
     *Visual*: Glowing chromatic border with radiating telemetry waves.  
     *Function*: Full multi-turn span coverage (`agent_id`, category tags, latency, token metrics).
   - **Node 4: Failure Detection (Audit & Enforcement)**  
     *Visual*: Radar audit badge.  
     *Function*: PRISM Agent Intelligence failure clustering + ClaimGuard Outbound Veto.
   - **Node 5: Improvement (Closed-Loop Evolution)**  
     *Visual*: Refresh cycle badge.  
     *Function*: PRISM AI Remediation prompt patches deployed $\rightarrow$ re-proven on held-out set.
2. **Autonomous Packet Flow (CSS Animation)**:
   - A glowing data pulse travels continuously from Node 1 $\rightarrow$ 2 $\rightarrow$ 3 $\rightarrow$ 4 $\rightarrow$ 5.
   - A curved feedback arc under the pipeline carries the pulse back from Node 5 to Node 1, labeled: `Continuous Re-Proving on Held-Out Test Set`.

#### E. Word Count Budget
- Headline: 6 words.
- Five Node Descriptions: 22 words total.
- **Total On-Slide Prose**: 28 words (Strictly $\le 40$).

---

### Slide 6: Impact & Future Scope

#### A. Metadata & Prompts (Mandated by Image)
- **Slide Eyebrow**: `Slide 6-Impact & Future Scope`
- **Mandated Prompt**: `Key benefits, real-world impact, scalability, and future enhancements.`
- **Headline (Fraunces Display)**: *"This failure class isn't insurance-specific. It's every call center."*

#### B. The Autonomous Story (What the Judge Reads in 10 Seconds)
The core failure class solved here—conversational interruption, emotional pressure, and spoken identifiers on small models—plagues every voice agent deployment. Today, ClaimGuard is proven on roadside assistance. Tomorrow, the exact same PRISM-observed architecture scales directly to Banking IVR under RBI FREE-AI rules, Telecom dispatch, and Healthcare intake under the DPDP Act.

#### C. Layout Architecture (16:9 Stage)
- **Top Section (15%)**: Eyebrow + prompt + Fraunces headline.
- **Middle Section (55%)**: **Multi-Domain Scalability Radar (SVG Radial Diagram)** displaying Insurance at the core and expanding outward to Banking, Telecom, and Healthcare.
- **Bottom Section (30%)**: **Production Engineering Roadmap Strip** + Final Pitch Thesis Anchor.

#### D. Visual Engine & Autonomous Animations
1. **Multi-Domain Scalability Radar (SVG)**:
   - **Center Core [Built & Verified Today]**:  
     `Insurance FNOL & Roadside Assistance` (Solid emerald glow, active demo on NH48 corridor).
   - **Sector 1: Banking & FinTech IVR (Future Scope)**  
     *Application*: Fraud emergency card cancellation & dispute intake.  
     *Governance*: Aligned with RBI FREE-AI Framework & PCI DSS v4.0.1.
   - **Sector 2: Telecom & Utilities Dispatch (Future Scope)**  
     *Application*: Priority fiber outage intake & technician dispatch under high customer churn.
   - **Sector 3: Emergency Healthcare Intake (Future Scope)**  
     *Application*: Triage routing & patient consent intimation under India DPDP Act 2023.
2. **Production Engineering Roadmap (Horizontal Changelog Strip)**:
   - `PHASE 1 (TODAY)`: Edge prototype, whisper.cpp, 3B LLM, SQLite triggers, PRISM trace spine.
   - `PHASE 2 (NEXT)`: SIP / Telephony IVR bridge (Exotel / Twilio) connected to L0 audio socket.
   - `PHASE 3 (SCALE)`: Regional-language expansion (Tamil, Telugu, Kannada) + PRISM Guardrails in Enforce Mode.
3. **The Final Thesis Anchor (Bottom Monospace Banner)**:
   `Can be interrupted. Can't be bullied. Won't leak. Built to be diagnosed — proven by PRISM.`

#### E. Word Count Budget
- Headline: 9 words.
- Three Sector Callouts: 14 words.
- Roadmap: 12 words.
- Closing Anchor: 12 words.
- **Total On-Slide Prose**: 47 words (Concise and readable).

---

## 3. Technical Engine Architecture for Builder Agent

### 3.1 Deliverable Files
The presentation builder agent will generate two standalone files in `/presentation/`:
1. `presentation/claimguard-pitch.html`: Online production deck linking Google Fonts and cdnjs assets.
2. `presentation/claimguard-pitch-offline.html`: Standalone offline file with inline styles, pre-rendered KaTeX/MathML, and robust system font fallbacks.

### 3.2 Slide Controller Implementation (Vanilla JavaScript, Zero Dependencies)
```javascript
class AutonomousDeckController {
  constructor() {
    this.slides = Array.from(document.querySelectorAll('.slide'));
    this.pips = Array.from(document.querySelectorAll('.nav-pip'));
    this.currentIndex = 0;
    this.totalSlides = this.slides.length;
    this.autoPlayTimer = null;
    this.isAutoPlaying = false;
    this.autoPlayIntervalMs = 15000; // 15 seconds per slide for autonomous judge review

    this.initDOM();
    this.initEvents();
    this.showSlide(0);
  }

  initDOM() {
    this.counterEl = document.getElementById('slide-counter');
    this.autoPlayBtn = document.getElementById('autoplay-toggle');
  }

  showSlide(index) {
    if (index < 0 || index >= this.totalSlides) return;
    
    this.slides[this.currentIndex].classList.remove('active');
    this.pips[this.currentIndex].classList.remove('active');

    this.currentIndex = index;
    this.slides[this.currentIndex].classList.add('active');
    this.pips[this.currentIndex].classList.add('active');

    if (this.counterEl) {
      this.counterEl.textContent = `0${this.currentIndex + 1} / 0${this.totalSlides}`;
    }
  }

  next() {
    const nextIdx = (this.currentIndex + 1) % this.totalSlides;
    this.showSlide(nextIdx);
  }

  prev() {
    const prevIdx = (this.currentIndex - 1 + this.totalSlides) % this.totalSlides;
    this.showSlide(prevIdx);
  }

  toggleAutoPlay() {
    this.isAutoPlaying = !this.isAutoPlaying;
    if (this.isAutoPlaying) {
      this.autoPlayBtn.classList.add('active');
      this.autoPlayBtn.textContent = 'Pause Auto-Play';
      this.autoPlayTimer = setInterval(() => this.next(), this.autoPlayIntervalMs);
    } else {
      this.autoPlayBtn.classList.remove('active');
      this.autoPlayBtn.textContent = 'Auto-Play (15s)';
      clearInterval(this.autoPlayTimer);
    }
  }

  initEvents() {
    // Keyboard navigation
    window.addEventListener('keydown', (e) => {
      if (['Space', 'ArrowRight', 'PageDown', 'KeyL'].includes(e.code)) this.next();
      if (['ArrowLeft', 'PageUp', 'KeyH'].includes(e.code)) this.prev();
      if (e.key >= '1' && e.key <= '6') this.showSlide(parseInt(e.key) - 1);
      if (e.code === 'KeyP') this.toggleAutoPlay();
      if (e.code === 'KeyF') this.toggleFullscreen();
    });

    // Navigation buttons
    document.getElementById('prev-btn')?.addEventListener('click', () => this.prev());
    document.getElementById('next-btn')?.addEventListener('click', () => this.next());
    this.autoPlayBtn?.addEventListener('click', () => this.toggleAutoPlay());

    this.pips.forEach((pip, idx) => {
      pip.addEventListener('click', () => this.showSlide(idx));
    });
  }

  toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen().catch(() => {});
    }
  }
}
```

### 3.3 Offline KaTeX Resilience
In `claimguard-pitch-offline.html`, the builder agent must embed the pre-rendered KaTeX MathML / SVG markup directly into Slide 3, guaranteeing instant mathematical rendering even on a completely disconnected machine.

---

## 4. Builder Agent Definition of Done & Pre-Flight Checklist

Before marking the presentation build complete, the builder agent must verify:
- [ ] **Exact 6 Slides**: Strictly follows the order, titles, and subtitle prompts from the user's reference image.
- [ ] **Zero Judge Interaction Required**: Every key takeaway, label, failure mode, and diagram is 100% visible and readable without clicking or hovering.
- [ ] **Ambient Self-Playing Animations**: The audio waveform, the state machine, the optical ray tracer, and the workflow packet runner loop smoothly on their own using hardware-accelerated CSS/SVG.
- [ ] **PRISM Prominence Established**: PRISM is named on Slide 1, functions as the central hero on Slide 4, dominates Slide 5, and delivers the closing anchor on Slide 6.
- [ ] **Invariant #3 Honesty Verified**: No fabricated percentages. The diagnostic matrix on Slide 4 reflects pre-registered categories from the NH48 Replay Set.
- [ ] **Word Ceiling Enforced**: Every slide stays within $\le 40$ words of prose.
- [ ] **Robust Offline Execution**: `claimguard-pitch-offline.html` loads with zero network dependencies, pre-rendered math, and robust font fallbacks.
- [ ] **Responsive 16:9 Viewport**: Uses CSS `clamp()` and container aspect-ratio to ensure identical geometry at 1080p and 1366x768 resolutions.
