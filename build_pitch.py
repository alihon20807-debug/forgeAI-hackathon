import os

html_content = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ClaimGuard x PRISM by Block Convey — Pitch Deck</title>
  
  <!-- Typography (Online Fonts) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..700&family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">

  <!-- KaTeX for Invariant LaTeX Math -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js" onload="renderMathInElement(document.body);"></script>

  <style>
    /* ==========================================================================
       DESIGN SYSTEM TOKENS: LIGHT ARCHITECTURAL PALETTE + PRISM BRANDING
       ========================================================================== */
    :root {
      /* Base Canvas */
      --ground: #F7F5F0;          /* Warm Cream Canvas */
      --surface-base: #FFFFFF;    /* Pure White Base for Cards */
      --surface-card: #FAF8F5;    /* Slightly Tinted Card Surface */
      --surface-raised: #F0EDE6;  /* Soft Warm Gray Raised Surface */
      --surface-wood: #1E1915;    /* Deep Roasted Walnut Primary Accent */
      
      /* Primary Ink & Text */
      --ink-primary: #1E1915;     /* Roasted Walnut (Crisp High Contrast) */
      --ink-secondary: #4A433B;   /* Readable Warm Neutral Body */
      --ink-muted: #7A7267;       /* Monospace Metadata & Labels */
      --ink-inverse: #FAF8F5;     /* Inverted Text */

      /* Structural Borders */
      --rule-hairline: #E2DDD5;   /* Crisp Subtle Border */
      --rule-strong: #C2B8A8;     /* Emphasized Border */

      /* Accent & Spectrum Palette */
      --jade-primary: #1B5E4B;    /* Imperial Jade Anchor */
      --jade-tint: #E8F2EE;       /* Jade Pill Background */
      --jade-border: #9BC7B9;     /* Jade Pill Border */

      --spectrum-violet: #543DB3; /* 400nm: Observability & Tracing */
      --spectrum-cyan: #0284C7;   /* 480nm: Root Cause Diagnosis */
      --spectrum-jade: #1B5E4B;   /* 520nm: Multi-Model Benchmark */
      --spectrum-amber: #D97706;  /* 580nm: Attention Drift & Warning */
      --spectrum-rose: #DC2626;   /* 650nm: Critical Failure & Remediation */

      /* Typography */
      --font-display: 'Fraunces', Georgia, serif;
      --font-sans: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'IBM Plex Mono', 'SF Mono', Menlo, Consolas, monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: #0E0C0A;
      font-family: var(--font-sans);
      color: var(--ink-primary);
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100vw;
      height: 100vh;
      -webkit-font-smoothing: antialiased;
    }

    /* Fixed 16:9 Presentation Stage */
    #presentation-stage {
      width: min(100vw, 177.78vh);
      height: min(56.25vw, 100vh);
      background-color: var(--ground);
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 30px 80px rgba(0, 0, 0, 0.55);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Persistent Top Chrome */
    header.stage-header {
      height: 56px;
      padding: 0 40px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--rule-hairline);
      background-color: rgba(247, 245, 240, 0.96);
      backdrop-filter: blur(10px);
      z-index: 100;
      flex-shrink: 0;
    }

    .header-eyebrow {
      display: flex;
      align-items: center;
      gap: 12px;
      font-family: var(--font-mono);
      font-size: 12.5px;
      font-weight: 600;
      color: var(--ink-secondary);
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    .header-eyebrow .slide-counter {
      color: var(--jade-primary);
      font-weight: 700;
      font-size: 12px;
      padding: 3px 8px;
      background: var(--jade-tint);
      border-radius: 4px;
      border: 1px solid var(--jade-border);
    }

    .header-project-pill {
      background: var(--surface-raised);
      padding: 3px 10px;
      border-radius: 4px;
      color: var(--ink-primary);
      font-size: 11.5px;
      font-weight: 700;
      letter-spacing: 0.05em;
    }

    /* Official Block Convey Brand Badge */
    .header-prism-badge {
      display: flex;
      align-items: center;
      gap: 10px;
      font-family: var(--font-sans);
      font-size: 13px;
      font-weight: 600;
      color: var(--ink-primary);
      padding: 5px 14px;
      border: 1px solid var(--rule-hairline);
      background: var(--surface-base);
      border-radius: 20px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }

    .bc-logo-mark {
      width: 18px;
      height: 18px;
      display: block;
    }

    .bc-brand-text {
      display: flex;
      align-items: center;
      gap: 5px;
    }

    .bc-brand-prism {
      font-family: var(--font-mono);
      font-weight: 700;
      color: var(--spectrum-violet);
      letter-spacing: 0.05em;
    }

    .bc-brand-sub {
      font-size: 12px;
      color: var(--ink-muted);
      font-weight: 500;
    }

    /* Slide Viewport */
    main.stage-viewport {
      flex: 1;
      position: relative;
      overflow: hidden;
    }

    .slide {
      position: absolute;
      inset: 0;
      padding: 24px 40px 18px;
      display: flex;
      flex-direction: column;
      opacity: 0;
      pointer-events: none;
      transform: translateY(8px);
      transition: opacity 0.3s ease, transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .slide.active {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0);
      z-index: 10;
    }

    /* Standard Slide Typography */
    .slide-header-block {
      margin-bottom: 14px;
      flex-shrink: 0;
    }

    .slide-mandated-prompt {
      font-family: var(--font-sans);
      font-size: 13px;
      font-weight: 700;
      color: var(--jade-primary);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .slide-mandated-prompt::before {
      content: "";
      display: inline-block;
      width: 7px;
      height: 7px;
      background: var(--jade-primary);
      border-radius: 50%;
    }

    .slide-headline {
      font-family: var(--font-display);
      font-size: 38px;
      font-weight: 600;
      color: var(--ink-primary);
      line-height: 1.15;
      letter-spacing: -0.015em;
    }

    .slide-context-note {
      font-family: var(--font-sans);
      font-size: 14px;
      color: var(--ink-secondary);
      margin-top: 4px;
      line-height: 1.35;
    }

    .slide-context-note strong {
      color: var(--ink-primary);
    }

    /* Persistent Bottom Chrome */
    footer.stage-footer {
      height: 52px;
      padding: 0 40px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-top: 1px solid var(--rule-hairline);
      background-color: var(--ground);
      z-index: 100;
      flex-shrink: 0;
    }

    .footer-left-controls {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .btn-nav {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      color: var(--ink-primary);
      padding: 6px 14px;
      border-radius: 6px;
      font-family: var(--font-sans);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }

    .btn-nav:hover {
      background: var(--surface-raised);
      border-color: var(--rule-strong);
      color: var(--jade-primary);
    }

    .btn-autoplay {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      color: var(--ink-secondary);
      padding: 6px 12px;
      border-radius: 6px;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }

    .btn-autoplay.active {
      background: var(--jade-tint);
      border-color: var(--jade-border);
      color: var(--jade-primary);
      font-weight: 600;
    }

    .nav-pips {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .pip {
      width: 30px;
      height: 30px;
      border-radius: 50%;
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
      color: var(--ink-muted);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s ease;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }

    .pip:hover {
      border-color: var(--rule-strong);
      color: var(--ink-primary);
    }

    .pip.active {
      background: var(--surface-wood);
      color: var(--ink-inverse);
      border-color: var(--surface-wood);
      transform: scale(1.08);
    }

    .footer-right-status {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
      color: var(--ink-muted);
      letter-spacing: 0.04em;
    }

    #autoplay-progress {
      position: absolute;
      top: 0;
      left: 0;
      height: 3px;
      background: var(--jade-primary);
      width: 0%;
      transition: width 0.1s linear;
      z-index: 101;
    }

    /* ==========================================================================
       SLIDE 1: PROBLEM STATEMENT
       ========================================================================== */
    .s1-container {
      display: flex;
      flex-direction: column;
      gap: 14px;
      height: 100%;
    }

    .waveform-card {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 12px;
      padding: 14px 20px 10px;
      position: relative;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
      display: flex;
      flex-direction: column;
      height: 250px;
      flex-shrink: 0;
    }

    .waveform-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
      color: var(--ink-muted);
    }

    .waveform-canvas-wrap {
      width: 100%;
      flex: 1;
      position: relative;
    }

    canvas#waveformCanvas {
      width: 100%;
      height: 100%;
      display: block;
    }

    .waveform-timeline-bar {
      display: flex;
      justify-content: space-between;
      border-top: 1px solid var(--rule-hairline);
      padding-top: 6px;
      margin-top: 4px;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--ink-muted);
    }

    .incident-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      flex: 1;
    }

    .incident-card {
      background: var(--surface-base);
      border-radius: 10px;
      padding: 16px 18px;
      border: 1px solid var(--rule-hairline);
      border-top: 4px solid var(--spectrum-amber);
      display: flex;
      flex-direction: column;
      gap: 8px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }

    .incident-card.amber { border-top-color: var(--spectrum-amber); }
    .incident-card.rose { border-top-color: var(--spectrum-rose); }
    .incident-card.violet { border-top-color: var(--spectrum-violet); }

    .incident-card-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .incident-tag {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .incident-card.amber .incident-tag { color: var(--spectrum-amber); }
    .incident-card.rose .incident-tag { color: var(--spectrum-rose); }
    .incident-card.violet .incident-tag { color: var(--spectrum-violet); }

    .incident-pill {
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .incident-pill.amber { background: #FEF3C7; color: #92400E; }
    .incident-pill.rose { background: #FEE2E2; color: #991B1B; }
    .incident-pill.violet { background: #EDE9FE; color: #5B21B6; }

    .incident-quote-box {
      background: var(--surface-raised);
      border-left: 3px solid var(--spectrum-amber);
      padding: 9px 12px;
      border-radius: 0 6px 6px 0;
    }
    .incident-card.amber .incident-quote-box { border-left-color: var(--spectrum-amber); }
    .incident-card.rose .incident-quote-box { border-left-color: var(--spectrum-rose); }
    .incident-card.violet .incident-quote-box { border-left-color: var(--spectrum-violet); }

    .incident-quote {
      font-family: var(--font-display);
      font-size: 15px;
      font-style: italic;
      color: var(--ink-primary);
      line-height: 1.3;
    }

    .incident-detail-block {
      font-size: 12.5px;
      color: var(--ink-secondary);
      line-height: 1.4;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .incident-detail-block strong {
      color: var(--ink-primary);
      font-size: 12px;
    }

    .incident-meta-tag {
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-radius: 4px;
      padding: 5px 8px;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--ink-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: auto;
    }

    .incident-meta-tag code {
      color: var(--ink-primary);
      font-weight: 600;
    }

    /* ==========================================================================
       SLIDE 2: EXISTING CHALLENGES
       ========================================================================== */
    .s2-layout {
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      gap: 20px;
      flex: 1;
      align-items: stretch;
    }

    .s2-stack-card {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 12px;
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .stack-header-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 600;
      color: var(--ink-muted);
      margin-bottom: 2px;
    }

    .stack-layer-item {
      border: 1px solid var(--rule-hairline);
      border-radius: 7px;
      padding: 10px 14px;
      background: var(--surface-card);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .layer-item-left {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .layer-item-title {
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 600;
      color: var(--ink-primary);
    }

    .layer-item-sub {
      font-size: 11.5px;
      color: var(--ink-secondary);
    }

    .stack-layer-item .layer-badge {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
      letter-spacing: 0.04em;
    }

    .badge-neutral { background: var(--surface-raised); color: var(--ink-secondary); }
    .badge-amber { background: #FEF3C7; color: #92400E; }
    .badge-red { background: #FEE2E2; color: #991B1B; }

    .stack-layer-item.fracture {
      border: 2px dashed var(--spectrum-rose);
      background: #FFF5F5;
      animation: fracturePulse 2.5s infinite ease-in-out;
    }
    .stack-layer-item.fracture .layer-item-title {
      color: var(--spectrum-rose);
    }

    .stack-layer-item.missing-prism {
      border: 1px dashed var(--ink-muted);
      background: transparent;
    }
    .stack-layer-item.missing-prism .layer-item-title {
      color: var(--ink-muted);
    }

    .connector-down {
      text-align: center;
      color: var(--rule-strong);
      font-size: 13px;
      line-height: 1;
    }

    .s2-gaps-column {
      display: flex;
      flex-direction: column;
      gap: 12px;
      justify-content: space-between;
    }

    .gap-card {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-left: 4px solid var(--surface-wood);
      border-radius: 10px;
      padding: 14px 16px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.03);
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .gap-eyebrow {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--surface-wood);
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }

    .gap-card h4 {
      font-family: var(--font-display);
      font-size: 17px;
      font-weight: 600;
      color: var(--ink-primary);
      line-height: 1.25;
    }

    .gap-card p {
      font-size: 12.5px;
      color: var(--ink-secondary);
      line-height: 1.4;
    }

    .gap-symptom-box {
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-radius: 6px;
      padding: 8px 10px;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--ink-secondary);
      line-height: 1.35;
      margin-top: auto;
    }

    .gap-symptom-box strong {
      color: var(--spectrum-rose);
      font-weight: 700;
    }

    /* ==========================================================================
       SLIDE 3: PROPOSED SOLUTION
       ========================================================================== */
    .s3-layout {
      display: flex;
      flex-direction: column;
      gap: 16px;
      height: 100%;
    }

    .s3-architecture-view {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 12px;
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .s3-arch-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 600;
      color: var(--ink-muted);
    }

    .layers-horizontal {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
    }

    .arch-chip {
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-radius: 8px;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .arch-chip-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .arch-chip-layer {
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 700;
      color: var(--ink-muted);
    }

    .arch-chip-badge {
      font-family: var(--font-mono);
      font-size: 9.5px;
      font-weight: 600;
      padding: 1px 5px;
      border-radius: 3px;
      background: var(--surface-raised);
      color: var(--ink-secondary);
    }

    .arch-chip strong {
      font-family: var(--font-sans);
      font-size: 14.5px;
      font-weight: 700;
      color: var(--ink-primary);
    }

    .arch-chip small {
      font-size: 11.5px;
      color: var(--ink-secondary);
      line-height: 1.35;
    }

    .arch-chip.jade-latch {
      border: 2px solid var(--jade-primary);
      background: var(--jade-tint);
      box-shadow: 0 2px 8px rgba(27, 94, 75, 0.12);
    }

    .arch-chip.jade-latch strong {
      color: var(--jade-primary);
    }

    .arch-chip.jade-latch .arch-chip-badge {
      background: var(--jade-primary);
      color: var(--ink-inverse);
    }

    .prism-spine-banner {
      background: #F4F1FA;
      border: 1px solid #D5CCE8;
      border-left: 4px solid var(--spectrum-violet);
      border-radius: 6px;
      padding: 8px 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-mono);
      font-size: 11.5px;
      color: var(--spectrum-violet);
    }

    .s3-pillars-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      flex: 1;
    }

    .pillar-card {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 10px;
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }

    .pillar-tag {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--jade-primary);
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }

    .pillar-title {
      font-family: var(--font-display);
      font-size: 19px;
      font-weight: 600;
      color: var(--ink-primary);
      line-height: 1.2;
    }

    .pillar-flow-box {
      background: var(--surface-raised);
      border: 1px solid var(--rule-hairline);
      border-radius: 6px;
      padding: 8px 10px;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--ink-primary);
      line-height: 1.4;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .flow-row {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .flow-pill {
      font-weight: 700;
      padding: 1px 6px;
      border-radius: 3px;
      font-size: 10px;
    }
    .flow-pill.held { background: #FEF3C7; color: #92400E; }
    .flow-pill.frozen { background: #EDE9FE; color: #5B21B6; }
    .flow-pill.veto { background: #FEE2E2; color: #991B1B; }

    .pillar-bullets {
      font-size: 12px;
      color: var(--ink-secondary);
      line-height: 1.4;
      display: flex;
      flex-direction: column;
      gap: 4px;
      flex: 1;
    }

    .pillar-bullets li {
      list-style: none;
      display: flex;
      align-items: flex-start;
      gap: 6px;
    }

    .pillar-bullets li::before {
      content: "•";
      color: var(--jade-primary);
      font-weight: bold;
    }

    .pillar-proof-tag {
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-radius: 4px;
      padding: 5px 8px;
      font-family: var(--font-mono);
      font-size: 10.5px;
      color: var(--jade-primary);
      font-weight: 600;
      margin-top: auto;
    }

    .katex-formula-block {
      background: var(--surface-raised);
      border: 1px solid var(--rule-hairline);
      border-radius: 6px;
      padding: 8px 12px;
      font-size: 15px;
      text-align: center;
      color: var(--ink-primary);
    }

    /* ==========================================================================
       SLIDE 4: PRISM USAGE (THE CENTERPIECE)
       ========================================================================== */
    .s4-layout {
      display: grid;
      grid-template-columns: 1.12fr 0.88fr;
      gap: 20px;
      flex: 1;
      align-items: stretch;
    }

    .optical-hero-card {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 12px;
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .optical-svg-stage {
      width: 100%;
      height: 250px;
      display: block;
    }

    .spectrum-legend-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 6px;
      border-top: 1px solid var(--rule-hairline);
      padding-top: 10px;
    }

    .legend-item {
      background: var(--surface-card);
      border-left: 3px solid var(--spectrum-violet);
      border-radius: 0 4px 4px 0;
      padding: 6px 10px;
      font-family: var(--font-sans);
      font-size: 11.5px;
      color: var(--ink-secondary);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .legend-item strong {
      color: var(--ink-primary);
      margin-right: 6px;
    }

    .s4-benchmark-card {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 12px;
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .benchmark-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      font-family: var(--font-mono);
      margin: 4px 0;
    }

    .benchmark-table th {
      text-align: left;
      padding: 6px 8px;
      color: var(--ink-muted);
      border-bottom: 2px solid var(--rule-hairline);
      font-weight: 700;
      font-size: 11px;
      letter-spacing: 0.04em;
    }

    .benchmark-table td {
      padding: 6px 8px;
      border-bottom: 1px solid var(--rule-hairline);
      color: var(--ink-primary);
    }

    .badge-pass {
      background: var(--jade-tint);
      color: var(--jade-primary);
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid var(--jade-border);
      font-size: 10.5px;
    }

    .badge-fail {
      background: #FEE2E2;
      color: var(--spectrum-rose);
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 10.5px;
    }

    .span-hierarchy-box {
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-radius: 6px;
      padding: 9px 12px;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--ink-secondary);
      line-height: 1.45;
    }

    .span-hierarchy-title {
      font-weight: 700;
      color: var(--spectrum-violet);
      margin-bottom: 4px;
      display: flex;
      justify-content: space-between;
    }

    .prism-diagnosis-dossier {
      background: var(--surface-raised);
      border: 1px solid var(--rule-hairline);
      border-left: 3px solid var(--jade-primary);
      border-radius: 0 6px 6px 0;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin-top: auto;
    }

    .dossier-title {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--jade-primary);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .dossier-desc {
      font-size: 12px;
      color: var(--ink-secondary);
      line-height: 1.4;
    }

    .dossier-desc strong {
      color: var(--ink-primary);
    }

    /* ==========================================================================
       SLIDE 5: SYSTEM WORKFLOW
       ========================================================================== */
    .s5-layout {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 100%;
      gap: 14px;
    }

    .workflow-pipeline {
      display: grid;
      grid-template-columns: 1fr auto 1fr auto 1.3fr auto 1fr auto 1fr;
      align-items: stretch;
      gap: 8px;
      flex: 1;
    }

    .wf-node {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 12px;
      padding: 14px 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 8px;
      height: 100%;
      position: relative;
      box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }

    .wf-node.hero-node {
      border: 2px solid var(--jade-primary);
      background: #FAFDFB;
      box-shadow: 0 4px 20px rgba(27, 94, 75, 0.15);
    }

    .wf-header-tag {
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 700;
      color: var(--ink-muted);
      letter-spacing: 0.05em;
    }

    .wf-node.hero-node .wf-header-tag {
      color: var(--jade-primary);
    }

    .wf-icon-box {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: var(--surface-raised);
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid var(--rule-hairline);
    }

    .wf-node.hero-node .wf-icon-box {
      background: var(--jade-tint);
      border-color: var(--jade-border);
    }

    .wf-icon-box svg {
      width: 22px;
      height: 22px;
    }

    .wf-title {
      font-family: var(--font-sans);
      font-size: 15.5px;
      font-weight: 700;
      color: var(--ink-primary);
      line-height: 1.2;
    }

    .wf-node.hero-node .wf-title {
      color: var(--jade-primary);
      font-size: 16.5px;
    }

    .wf-role {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      color: var(--ink-secondary);
    }

    .wf-spec-list {
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-radius: 6px;
      padding: 10px 10px;
      font-size: 11.5px;
      color: var(--ink-secondary);
      text-align: left;
      line-height: 1.35;
      width: 100%;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .wf-spec-list li {
      list-style: none;
      display: flex;
      align-items: flex-start;
      gap: 5px;
    }

    .wf-spec-list li::before {
      content: "•";
      color: var(--jade-primary);
      font-weight: bold;
    }

    .wf-contract-badge {
      background: var(--surface-raised);
      border: 1px solid var(--rule-hairline);
      border-radius: 4px;
      padding: 5px 6px;
      font-family: var(--font-mono);
      font-size: 10px;
      color: var(--ink-secondary);
      width: 100%;
      line-height: 1.3;
      margin-top: auto;
    }

    .wf-node.hero-node .wf-contract-badge {
      background: var(--jade-tint);
      border-color: var(--jade-border);
      color: var(--jade-primary);
      font-weight: 600;
    }

    .wf-arrow {
      color: var(--rule-strong);
      font-size: 18px;
      font-weight: 700;
      align-self: center;
    }

    .feedback-loop-banner {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 10px;
      padding: 10px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 11.5px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }

    .feedback-loop-banner strong {
      color: var(--jade-primary);
    }

    /* ==========================================================================
       SLIDE 6: IMPACT & FUTURE SCOPE
       ========================================================================== */
    .s6-layout {
      display: grid;
      grid-template-columns: 0.95fr 1.05fr;
      gap: 20px;
      flex: 1;
      align-items: stretch;
    }

    .radar-container {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 12px;
      padding: 18px 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .radar-header {
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 700;
      color: var(--ink-muted);
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    .radar-svg-wrap {
      display: flex;
      justify-content: center;
      align-items: center;
      margin: 4px 0;
    }

    .radar-invariant-box {
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-left: 3px solid var(--jade-primary);
      border-radius: 0 6px 6px 0;
      padding: 10px 12px;
      font-size: 12px;
      color: var(--ink-secondary);
      line-height: 1.45;
    }

    .radar-invariant-box strong {
      color: var(--ink-primary);
    }

    .s6-roadmap-container {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 10px;
    }

    .roadmap-timeline {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 12px;
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
      flex: 1;
      justify-content: space-around;
    }

    .roadmap-phase {
      display: flex;
      gap: 12px;
      align-items: flex-start;
    }

    .phase-badge {
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 700;
      padding: 4px 8px;
      border-radius: 4px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      flex-shrink: 0;
      width: 110px;
      text-align: center;
    }

    .phase-badge.today {
      background: var(--jade-tint);
      color: var(--jade-primary);
      border: 1px solid var(--jade-border);
    }

    .phase-badge.next {
      background: #FEF3C7;
      color: #92400E;
      border: 1px solid #FCD34D;
    }

    .phase-badge.scale {
      background: #EDE9FE;
      color: #5B21B6;
      border: 1px solid #C4B5FD;
    }

    .phase-info h5 {
      font-size: 14px;
      font-weight: 700;
      color: var(--ink-primary);
      margin-bottom: 2px;
    }

    .phase-info p {
      font-size: 12px;
      color: var(--ink-secondary);
      line-height: 1.35;
      margin-bottom: 4px;
    }

    .phase-metric-tag {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      color: var(--jade-primary);
    }

    .closing-thesis-banner {
      background: var(--surface-wood);
      color: var(--ink-inverse);
      padding: 12px 18px;
      border-radius: 10px;
      font-family: var(--font-mono);
      font-size: 13px;
      text-align: center;
      letter-spacing: 0.04em;
      line-height: 1.45;
      box-shadow: 0 4px 16px rgba(38, 31, 26, 0.25);
    }

    .closing-thesis-banner strong {
      color: #FBBF24;
    }
  </style>
</head>
<body>

  <div id="presentation-stage">
    <!-- Auto-Play Progress Indicator -->
    <div id="autoplay-progress"></div>

    <!-- Persistent Top Chrome -->
    <header class="stage-header">
      <div class="header-eyebrow">
        <span class="slide-counter" id="slide-counter">01 / 06</span>
        <span class="header-project-pill">CLAIMGUARD × PRISM</span>
        <span id="slide-category-title">Problem Statement</span>
      </div>
      
      <!-- Official Block Convey Brand Badge (Exact Mark) -->
      <div class="header-prism-badge">
        <svg class="bc-logo-mark" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="2" y="16" width="26" height="26" rx="6" fill="#1E1915" fill-opacity="0.92"/>
          <rect x="20" y="2" width="26" height="26" rx="6" fill="#1E1915"/>
          <rect x="20" y="16" width="12" height="12" rx="4" fill="#FAF8F5"/>
        </svg>
        <div class="bc-brand-text">
          <span class="bc-brand-prism">PRISM</span>
          <span class="bc-brand-sub">by Block Convey</span>
        </div>
      </div>
    </header>

    <!-- Main Viewport containing 6 Slides -->
    <main class="stage-viewport">
      
      <!-- ====================================================================
           SLIDE 1: PROBLEM STATEMENT
           ==================================================================== -->
      <section class="slide active" id="slide-1">
        <div class="s1-container">
          <div class="slide-header-block">
            <div class="slide-mandated-prompt">What real-world problem are we trying to solve?</div>
            <h1 class="slide-headline">When voice AI handles emergency calls, small errors cause disaster.</h1>
            <div class="slide-context-note">
              <strong>The Scenario:</strong> A driver stranded on Highway NH-48 in the rain calls their insurance hotline. An autonomous voice agent answers.
            </div>
          </div>

          <!-- Waveform & Call Transcript Timeline -->
          <div class="waveform-card">
            <div class="waveform-header">
              <span>LIVE CALL AUDIO STREAM · INBOUND 8kHz PHONE CALL</span>
              <span>PRISM MULTI-TURN TELEMETRY SPAN</span>
            </div>
            <div class="waveform-canvas-wrap">
              <canvas id="waveformCanvas"></canvas>
            </div>
            <div class="waveform-timeline-bar">
              <span>00:00 Call Connected</span>
              <span>01:14 Turn 2: Driver cancels tow truck</span>
              <span>02:45 Turn 4: Driver begs for discount</span>
              <span>03:50 Turn 5: Driver speaks card number</span>
              <span>04:18 Call Ends</span>
            </div>
          </div>

          <!-- 3 Concrete Real-World Incident Breakdowns -->
          <div class="incident-grid">
            <div class="incident-card amber">
              <div class="incident-card-top">
                <span class="incident-tag"><span>●</span> 1. The Ghost Dispatch</span>
                <span class="incident-pill amber">Turn 2 · 01:14</span>
              </div>
              <div class="incident-quote-box">
                <div class="incident-quote">"Wait! Brother arrived with fuel, cancel the tow truck!"</div>
              </div>
              <div class="incident-detail-block">
                <strong>What goes wrong:</strong>
                The AI verbally says <em>"Understood!"</em>, but its attention collapses. It still secretly dispatches a ₹5,000 tow truck. Real highway emergencies are left stranded.
              </div>
              <div class="incident-meta-tag">
                <span>FAILURE:</span> <code>REVOCATION_IGNORED</code>
              </div>
            </div>

            <div class="incident-card rose">
              <div class="incident-card-top">
                <span class="incident-tag"><span>●</span> 2. The Unauthorized Payout</span>
                <span class="incident-pill rose">Turn 4 · 02:45</span>
              </div>
              <div class="incident-quote-box">
                <div class="incident-quote">"Stranded in the rain for 2 hours, waive my ₹1,500 deductible!"</div>
              </div>
              <div class="incident-detail-block">
                <strong>What goes wrong:</strong>
                Under caller emotional pressure, the cheap model sycophantically hallucinates authority and waives the deductible, bleeding money with zero audit trail.
              </div>
              <div class="incident-meta-tag">
                <span>FAILURE:</span> <code>UNAUTHORIZED_CONCESSION</code>
              </div>
            </div>

            <div class="incident-card violet">
              <div class="incident-card-top">
                <span class="incident-tag"><span>●</span> 3. The Credit Card Leak</span>
                <span class="incident-pill violet">Turn 5 · 03:50</span>
              </div>
              <div class="incident-quote-box">
                <div class="incident-quote">"Charge my card right now: 4532 8901 2345 6789..."</div>
              </div>
              <div class="incident-detail-block">
                <strong>What goes wrong:</strong>
                The caller speaks their 16-digit card. The AI writes raw payment digits directly to unencrypted server logs and memory, violating PCI DSS and the India DPDP Act.
              </div>
              <div class="incident-meta-tag">
                <span>FAILURE:</span> <code>PLAIN_PII_LOGGED</code>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ====================================================================
           SLIDE 2: EXISTING CHALLENGES
           ==================================================================== -->
      <section class="slide" id="slide-2">
        <div class="slide-header-block">
          <div class="slide-mandated-prompt">What are the limitations, risks, or gaps in current solutions?</div>
          <h1 class="slide-headline">Why can't we just write a better prompt?</h1>
          <div class="slide-context-note">
            Phone agents cannot afford slow, expensive models like GPT-4. They must use <strong>fast, small 3B models</strong> — and prompts alone cannot control them.
          </div>
        </div>

        <div class="s2-layout">
          <!-- Production Stack Failure Breakdown -->
          <div class="s2-stack-card">
            <div class="stack-header-row">
              <span>TODAY'S UNGUARDED CALL-CENTER AI PIPELINE</span>
              <span style="color: var(--spectrum-rose); font-weight: 700;">WHERE IT BREAKS</span>
            </div>
            
            <div class="stack-layer-item">
              <div class="layer-item-left">
                <span class="layer-item-title">1. Phone Audio Edge (WebRTC / SIP)</span>
                <span class="layer-item-sub">Audio arrives from phone network; 200ms latency budget</span>
              </div>
              <span class="layer-badge badge-neutral">UNENCRYPTED</span>
            </div>
            <div class="connector-down">↓</div>
            
            <div class="stack-layer-item">
              <div class="layer-item-left">
                <span class="layer-item-title">2. Speech-to-Text (Whisper STT)</span>
                <span class="layer-item-sub">Transcribes voice verbatim — including raw credit cards</span>
              </div>
              <span class="layer-badge badge-neutral">RAW PII PASSED</span>
            </div>
            <div class="connector-down">↓</div>
            
            <div class="stack-layer-item">
              <div class="layer-item-left">
                <span class="layer-item-title">3. Small AI Model (3B Parameters)</span>
                <span class="layer-item-sub">Decides what to do; easily confused by caller interruptions</span>
              </div>
              <span class="layer-badge badge-amber">ATTENTION COLLAPSE</span>
            </div>
            <div class="connector-down">↓</div>
            
            <div class="stack-layer-item fracture">
              <div class="layer-item-left">
                <span class="layer-item-title">MISSING BARRIER: Zero Verification Gate</span>
                <span class="layer-item-sub">Model outputs execute immediately without safety delays</span>
              </div>
              <span class="layer-badge badge-red">CRACKED DEFENSE</span>
            </div>
            <div class="connector-down">↓</div>
            
            <div class="stack-layer-item">
              <div class="layer-item-left">
                <span class="layer-item-title">4. Real Database & Dispatch Server</span>
                <span class="layer-item-sub">Database executes dispatched tow truck anyway; money lost</span>
              </div>
              <span class="layer-badge badge-red">CORRUPTED STATE</span>
            </div>
            <div class="connector-down" style="color: var(--spectrum-rose);">✕</div>
            
            <div class="stack-layer-item missing-prism">
              <div class="layer-item-left">
                <span class="layer-item-title">5. Blind Server Monitoring</span>
                <span class="layer-item-sub">Standard APMs only see HTTP 200 OK — zero visibility into AI drift</span>
              </div>
              <span class="layer-badge badge-neutral">NO MULTI-TURN APM</span>
            </div>
          </div>

          <!-- 3 Fundamental Architectural Gaps -->
          <div class="s2-gaps-column">
            <div class="gap-card">
              <div class="gap-eyebrow">GAP 01 · PROMPTS ARE NOT SECURITY GUARDS</div>
              <h4>Prompts Cannot Enforce Rules Under Panic</h4>
              <p>Telling an AI <em>"Do not make promises"</em> in a prompt is only a suggestion. Under caller interruptions, small models suffer memory collapse and agree to anything.</p>
              <div class="gap-symptom-box">
                <strong>Real Failure:</strong> AI promises a ₹1,500 refund and dispatches a truck in the exact same turn it was told to cancel.
              </div>
            </div>

            <div class="gap-card">
              <div class="gap-eyebrow">GAP 02 · TRADITIONAL APMS ARE COMPLETELY BLIND</div>
              <h4>HTTP 200 Hides Semantic AI Disaster</h4>
              <p>Traditional cloud monitors check if the server responded. They cannot detect when an AI gets trapped in an apology loop or forgets a caller's previous instruction.</p>
              <div class="gap-symptom-box">
                <strong>Real Failure:</strong> Dashboard shows 100% green uptime while callers are hung up on or given wrong towing trucks.
              </div>
            </div>

            <div class="gap-card">
              <div class="gap-eyebrow">GAP 03 · CLEANING DATA POST-HOC IS ILLEGAL</div>
              <h4>Scrubbing Credit Cards After the Fact Fails</h4>
              <p>Trying to clean payment cards after the AI reads them is too late. The card digits are already stored in server memory and unencrypted GPU caches, violating PCI DSS.</p>
              <div class="gap-symptom-box">
                <strong>Real Failure:</strong> Raw 16-digit credit cards saved to unencrypted debug logs across thousands of calls.
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ====================================================================
           SLIDE 3: PROPOSED SOLUTION
           ==================================================================== -->
      <section class="slide" id="slide-3">
        <div class="s3-layout">
          <div class="slide-header-block">
            <div class="slide-mandated-prompt">What solution are we proposing and how does it solve the problem?</div>
            <h1 class="slide-headline">The AI proposes; deterministic code decides.</h1>
            <div class="slide-context-note">
              <strong>ClaimGuard</strong> places a zero-trust software barrier between the small AI model and real-world actions. The AI can converse, but code holds the keys.
            </div>
          </div>

          <!-- 4-Stage Architecture Bar -->
          <div class="s3-architecture-view">
            <div class="s3-arch-header">
              <span>HOW CLAIMGUARD ENFORCES SAFETY AT RUNTIME</span>
              <span style="color: var(--jade-primary);">DETERMINISTIC DEFENSE-IN-DEPTH</span>
            </div>
            <div class="layers-horizontal">
              <div class="arch-chip">
                <div class="arch-chip-top">
                  <span class="arch-chip-layer">STEP 1</span>
                  <span class="arch-chip-badge">STREAMING</span>
                </div>
                <strong>Pre-LLM Masking</strong>
                <small>Masks credit cards BEFORE words enter the AI model.</small>
              </div>

              <div class="arch-chip">
                <div class="arch-chip-top">
                  <span class="arch-chip-layer">STEP 2</span>
                  <span class="arch-chip-badge">PROPOSER ONLY</span>
                </div>
                <strong>Small 3B AI Model</strong>
                <small>Understands caller voice; strictly proposes actions.</small>
              </div>

              <div class="arch-chip jade-latch">
                <div class="arch-chip-top">
                  <span class="arch-chip-layer" style="color: var(--jade-primary);">STEP 3</span>
                  <span class="arch-chip-badge">THE BARRIER</span>
                </div>
                <strong>ClaimGuard Latch</strong>
                <small>Holds dispatches for 5s; vetoes illegal discounts.</small>
              </div>

              <div class="arch-chip">
                <div class="arch-chip-top">
                  <span class="arch-chip-layer">STEP 4</span>
                  <span class="arch-chip-badge">DATABASE</span>
                </div>
                <strong>Protected Database</strong>
                <small>SQL triggers strictly reject unauthorized actions.</small>
              </div>
            </div>

            <!-- PRISM Telemetry Spine Banner -->
            <div class="prism-spine-banner">
              <span><strong>PRISM OBSERVABILITY SPINE:</strong> Monitors every audio packet, model proposal, and database write in real-time with zero lag.</span>
              <span style="font-weight: 700;">100% VISIBILITY</span>
            </div>
          </div>

          <!-- 3 Pillars Explained for Judges -->
          <div class="s3-pillars-grid">
            <div class="pillar-card">
              <div class="pillar-tag">Pillar 01 · Prevents Ghost Dispatches</div>
              <div class="pillar-title">Can Be Interrupted</div>
              <div class="pillar-flow-box">
                <div class="flow-row">
                  <span>Order Tow Truck → </span>
                  <span class="flow-pill held">WAIT 5 SECONDS</span>
                  <span> → "Cancel!" → </span>
                  <span class="flow-pill frozen">ABORTED</span>
                </div>
              </div>
              <ul class="pillar-bullets">
                <li><strong>5-Second Delay:</strong> High-stakes tool dispatches are held in PENDING state.</li>
                <li><strong>Instant Speech Abort:</strong> Whisper STT catches revocation words ("cancel", "stop").</li>
                <li><strong>No LLM Dependency:</strong> Abort executes in deterministic code, not by trusting the AI.</li>
              </ul>
              <div class="pillar-proof-tag">✓ Guaranteed abort even if the AI model gets confused</div>
            </div>

            <div class="pillar-card">
              <div class="pillar-tag">Pillar 02 · Blocks Illegal Discounts</div>
              <div class="pillar-title">Can't Be Bullied</div>
              <div class="pillar-flow-box">
                <div class="flow-row">
                  <span>AI: "I'll waive your fee" → </span>
                  <span class="flow-pill veto">INTERCEPTED & MUTED</span>
                </div>
              </div>
              <ul class="pillar-bullets">
                <li><strong>Database Triggers:</strong> SQLite database triggers lock financial concession fields.</li>
                <li><strong>Speech Veto Engine:</strong> Scans generated AI sentences before voice synthesis.</li>
                <li><strong>Zero Liability:</strong> Automatically strips promises and forces compliant policy reply.</li>
              </ul>
              <div class="pillar-proof-tag">✓ Zero unauthorized financial leakage across 100% of calls</div>
            </div>

            <div class="pillar-card">
              <div class="pillar-tag">Pillar 03 · Zero Data Leaks</div>
              <div class="pillar-title">Won't Leak Credit Cards</div>
              <div class="katex-formula-block">
                $$\sum_{i=1}^{n} f(d_i, i) \equiv 0 \pmod{10}$$
              </div>
              <ul class="pillar-bullets">
                <li><strong>Streaming Inspection:</strong> Inspects caller speech in 16-digit sliding windows.</li>
                <li><strong>Luhn Checksum Test:</strong> Mathematical formula verifies Visa/Mastercard digits.</li>
                <li><strong>Pre-Model Masking:</strong> Replaces numbers with [REDACTED] before AI context ingestion.</li>
              </ul>
              <div class="pillar-proof-tag">✓ Plaintext card digits never touch AI memory or server logs</div>
            </div>
          </div>
        </div>
      </section>

      <!-- ====================================================================
           SLIDE 4: PRISM USAGE (THE CENTERPIECE)
           ==================================================================== -->
      <section class="slide" id="slide-4">
        <!-- Slide Header Block is OUTSIDE s4-layout for clean side-by-side grid -->
        <div class="slide-header-block">
          <div class="slide-mandated-prompt">How PRISM is used to monitor, evaluate, detect failures, and improve the AI system..</div>
          <h1 class="slide-headline">PRISM: The diagnostic instrument watching every turn.</h1>
          <div class="slide-context-note">
            Building an AI agent is easy. <strong>Knowing why, when, and where it fails across 10,000 calls is impossible without Block Convey's PRISM.</strong>
          </div>
        </div>

        <div class="s4-layout">
          <!-- Left Side: Refractive Optical PRISM Concept -->
          <div class="optical-hero-card">
            <div style="display: flex; justify-content: space-between; align-items: center; font-family: var(--font-mono); font-size: 11.5px; color: var(--ink-muted); font-weight: 600;">
              <span>HOW PRISM DECOMPOSES COMPLEX CALL FAILURES</span>
              <span style="color: var(--spectrum-violet); font-weight: 700;">OPTICAL TELEMETRY</span>
            </div>
            
            <svg class="optical-svg-stage" viewBox="0 0 640 250">
              <!-- Incident Light Beam -->
              <line x1="20" y1="125" x2="180" y2="125" stroke="#1E1915" stroke-width="5" stroke-linecap="round" />
              <text x="25" y="110" font-family="IBM Plex Sans" font-size="11" font-weight="700" fill="#524B43">RAW UNMONITORED PHONE CALL</text>

              <!-- Central Glass Prism -->
              <polygon points="190,25 300,225 80,225" fill="rgba(255,255,255,0.94)" stroke="#C2B8A8" stroke-width="2.5" />
              <text x="165" y="190" font-family="IBM Plex Mono" font-size="13" font-weight="700" fill="#1E1915" letter-spacing="1">PRISM</text>

              <!-- 5 Refracted Spectral Bands (Clear non-overlapping labels) -->
              <line x1="220" y1="120" x2="410" y2="40" stroke="#543DB3" stroke-width="3" />
              <circle cx="410" cy="40" r="4" fill="#543DB3" />
              <text x="422" y="44" font-family="IBM Plex Sans" font-size="11" font-weight="700" fill="#543DB3">1. Multi-Turn Spans (Tracks full call flow)</text>

              <line x1="220" y1="123" x2="410" y2="82" stroke="#0284C7" stroke-width="3" />
              <circle cx="410" cy="82" r="4" fill="#0284C7" />
              <text x="422" y="86" font-family="IBM Plex Sans" font-size="11" font-weight="700" fill="#0284C7">2. Root Cause Diagnosis (Why did it break?)</text>

              <line x1="220" y1="125" x2="410" y2="125" stroke="#1B5E4B" stroke-width="3" />
              <circle cx="410" cy="125" r="4" fill="#1B5E4B" />
              <text x="422" y="129" font-family="IBM Plex Sans" font-size="11" font-weight="700" fill="#1B5E4B">3. Fleet Benchmarking (Compare 3B vs 8B)</text>

              <line x1="220" y1="127" x2="410" y2="168" stroke="#D97706" stroke-width="3" />
              <circle cx="410" cy="168" r="4" fill="#D97706" />
              <text x="422" y="172" font-family="IBM Plex Sans" font-size="11" font-weight="700" fill="#D97706">4. Failure Clustering (Groups similar errors)</text>

              <line x1="220" y1="130" x2="410" y2="210" stroke="#DC2626" stroke-width="3" />
              <circle cx="410" cy="210" r="4" fill="#DC2626" />
              <text x="422" y="214" font-family="IBM Plex Sans" font-size="11" font-weight="700" fill="#DC2626">5. AI Remediation (Recommends verified fix)</text>
            </svg>

            <!-- Spectrum Breakdown Grid -->
            <div class="spectrum-legend-grid">
              <div class="legend-item" style="border-left-color: var(--spectrum-violet);">
                <span><strong>Multi-Turn Spans:</strong> Captures audio, model prompts, and tool executions with 0ms delay.</span>
              </div>
              <div class="legend-item" style="border-left-color: var(--spectrum-cyan);">
                <span><strong>Root Cause Isolation:</strong> Pinpoints whether failure was speech transcription or model panic.</span>
              </div>
              <div class="legend-item" style="border-left-color: var(--spectrum-jade);">
                <span><strong>Fleet Benchmark:</strong> Proves small 3B models match 70B models once guarded.</span>
              </div>
              <div class="legend-item" style="border-left-color: var(--spectrum-amber);">
                <span><strong>Failure Clusters:</strong> Automatically groups recurring break-points across calls.</span>
              </div>
              <div class="legend-item" style="border-left-color: var(--spectrum-rose);">
                <span><strong>Closed-Loop Fix:</strong> Recommends policy changes and verifies against test suite.</span>
              </div>
            </div>
          </div>

          <!-- Right Side: The Proven 48-Call Benchmark -->
          <div class="s4-benchmark-card">
            <div>
              <div style="display: flex; justify-content: space-between; align-items: center; font-family: var(--font-mono); font-size: 11.5px; color: var(--ink-muted); font-weight: 600;">
                <span>PROVEN IN PRE-REGISTERED 48-SCENARIO BENCHMARK</span>
                <span style="color: var(--jade-primary); font-weight: 700;">AUDIT RESULTS</span>
              </div>
              
              <table class="benchmark-table">
                <thead>
                  <tr>
                    <th>TESTED SCENARIO</th>
                    <th>UNGUARDED AI</th>
                    <th>PROMPT FIX</th>
                    <th>WITH CLAIMGUARD</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Mid-Call Cancellations</td>
                    <td><span class="badge-fail">FAILED</span></td>
                    <td><span class="badge-fail">FAILED</span></td>
                    <td><span class="badge-pass">100% PASS</span></td>
                  </tr>
                  <tr>
                    <td>Look-Alike Traps</td>
                    <td><span class="badge-fail">FAILED</span></td>
                    <td><span class="badge-pass">PASSED</span></td>
                    <td><span class="badge-pass">100% PASS</span></td>
                  </tr>
                  <tr>
                    <td>Pressure Bargaining</td>
                    <td><span class="badge-fail">LEAKED ₹</span></td>
                    <td><span class="badge-fail">LEAKED ₹</span></td>
                    <td><span class="badge-pass">ZERO LEAKS</span></td>
                  </tr>
                  <tr>
                    <td>Spoken Credit Cards</td>
                    <td><span class="badge-fail">EXPOSED</span></td>
                    <td><span class="badge-fail">EXPOSED</span></td>
                    <td><span class="badge-pass">ZERO LEAKS</span></td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- PRISM Telemetry Trace Example -->
            <div class="span-hierarchy-box">
              <div class="span-hierarchy-title">
                <span>PRISM LIVE TURN-BY-TURN TRACE</span>
                <span>CALL #4812</span>
              </div>
              <div>Turn 01: Driver reports breakdown on NH-48 → Audio Clean</div>
              <div>Turn 02: AI proposes tow truck dispatch → <strong>ClaimGuard holds in PENDING</strong></div>
              <div>Turn 02.1: Driver shouts "Cancel!" → <strong>ClaimGuard shifts state to FROZEN</strong></div>
              <div>Turn 03: PRISM flags zero ghost dispatches occurred → <strong>PASSED</strong></div>
            </div>

            <!-- Key Takeaway for Judges -->
            <div class="prism-diagnosis-dossier">
              <div class="dossier-title">WHAT THE JUDGES NEED TO KNOW</div>
              <div class="dossier-desc">
                • <strong>Prompt fixes fail under pressure:</strong> Prompt engineering passed simple traps, but still leaked money and dispatches.<br>
                • <strong>Deterministic guardrails win:</strong> ClaimGuard completely eliminated financial leaks and PII breaches by code design.<br>
                • <strong>PRISM proved it:</strong> Every single scenario was objectively verified and logged in PRISM.
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ====================================================================
           SLIDE 5: SYSTEM WORKFLOW
           ==================================================================== -->
      <section class="slide" id="slide-5">
        <div class="s5-layout">
          <div class="slide-header-block">
            <div class="slide-mandated-prompt">Input → AI/RAG/Agent System → PRISM Monitoring & Evaluation → Failure Detection → Improvement</div>
            <h1 class="slide-headline">How an emergency call flows through the system.</h1>
            <div class="slide-context-note">
              Every 200-millisecond turn of speech follows this closed loop to guarantee safety before words become actions.
            </div>
          </div>

          <div class="workflow-pipeline">
            <!-- Stage 1 -->
            <div class="wf-node">
              <span class="wf-header-tag">STAGE 1</span>
              <div class="wf-icon-box">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                  <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                  <line x1="12" y1="19" x2="12" y2="23"></line>
                </svg>
              </div>
              <div class="wf-title">Input</div>
              <div class="wf-role">Caller Audio Stream</div>
              <ul class="wf-spec-list">
                <li>Caller speaks over phone</li>
                <li>Whisper converts speech to text</li>
                <li>Luhn filter masks credit cards</li>
              </ul>
              <div class="wf-contract-badge"><strong>In:</strong> Raw phone audio<br><strong>Out:</strong> Clean masked text</div>
            </div>

            <span class="wf-arrow">→</span>

            <!-- Stage 2 -->
            <div class="wf-node">
              <span class="wf-header-tag">STAGE 2</span>
              <div class="wf-icon-box">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="4"></circle>
                  <path d="M16 8v5a3 3 0 0 0 6 0v-1a10 10 0 1 0-4 8"></path>
                </svg>
              </div>
              <div class="wf-title">AI Cognition</div>
              <div class="wf-role">Small 3B Proposer</div>
              <ul class="wf-spec-list">
                <li>Queries insurance policy</li>
                <li>Generates conversational reply</li>
                <li>PROPOSES tool actions only</li>
              </ul>
              <div class="wf-contract-badge"><strong>In:</strong> Caller conversation<br><strong>Out:</strong> Proposed action</div>
            </div>

            <span class="wf-arrow">→</span>

            <!-- Stage 3 (Hero Node with Block Convey Mark) -->
            <div class="wf-node hero-node">
              <span class="wf-header-tag">STAGE 3 · THE CORE</span>
              <div class="wf-icon-box">
                <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="2" y="16" width="26" height="26" rx="6" fill="#1B5E4B"/>
                  <rect x="20" y="2" width="26" height="26" rx="6" fill="#1B5E4B"/>
                  <rect x="20" y="16" width="12" height="12" rx="4" fill="#E8F2EE"/>
                </svg>
              </div>
              <div class="wf-title">PRISM Monitoring</div>
              <div class="wf-role" style="color: var(--jade-primary);">Block Convey Telemetry</div>
              <ul class="wf-spec-list">
                <li>Records every multi-turn span</li>
                <li>Captures audio latency & intent</li>
                <li>Zero lag added to phone call</li>
              </ul>
              <div class="wf-contract-badge"><strong>In:</strong> Turn-by-turn data<br><strong>Out:</strong> Telemetry trace</div>
            </div>

            <span class="wf-arrow">→</span>

            <!-- Stage 4 -->
            <div class="wf-node">
              <span class="wf-header-tag">STAGE 4</span>
              <div class="wf-icon-box">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                </svg>
              </div>
              <div class="wf-title">Failure Detection</div>
              <div class="wf-role">ClaimGuard Barrier</div>
              <ul class="wf-spec-list">
                <li>5s commit delay prevents errors</li>
                <li>Cancels dispatches on interruption</li>
                <li>Vetoes illegal discount promises</li>
              </ul>
              <div class="wf-contract-badge"><strong>In:</strong> Proposed action<br><strong>Out:</strong> Verified or Vetoed</div>
            </div>

            <span class="wf-arrow">→</span>

            <!-- Stage 5 -->
            <div class="wf-node">
              <span class="wf-header-tag">STAGE 5</span>
              <div class="wf-icon-box">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="23 4 23 10 17 10"></polyline>
                  <polyline points="1 20 1 14 7 14"></polyline>
                  <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
                </svg>
              </div>
              <div class="wf-title">Improvement</div>
              <div class="wf-role">Closed-Loop Learning</div>
              <ul class="wf-spec-list">
                <li>Clusters failure patterns</li>
                <li>Recommends policy updates</li>
                <li>Automated test re-evaluation</li>
              </ul>
              <div class="wf-contract-badge"><strong>In:</strong> PRISM insights<br><strong>Out:</strong> Hardened system</div>
            </div>
          </div>

          <!-- Bottom Banner -->
          <div class="feedback-loop-banner">
            <span><strong>CONTINUOUS CLOSED FEEDBACK LOOP:</strong> Production calls feed directly into PRISM failure clustering</span>
            <span style="font-family: var(--font-sans); color: var(--ink-secondary); font-size: 11.5px;">
              Every failure detected by PRISM is turned into an automated test scenario so the AI never makes the same mistake twice.
            </span>
          </div>
        </div>
      </section>

      <!-- ====================================================================
           SLIDE 6: IMPACT & FUTURE SCOPE
           ==================================================================== -->
      <section class="slide" id="slide-6">
        <div class="s6-layout">
          <!-- Left: Cross-Industry Scalability -->
          <div class="radar-container">
            <div class="radar-header">
              APPLIED ACROSS 4 REGULATED CALL-CENTER SECTORS
            </div>
            
            <div class="radar-svg-wrap">
              <svg viewBox="0 0 360 280" style="width: 340px; height: 260px;">
                <!-- Concentric Radar Rings -->
                <circle cx="180" cy="140" r="125" fill="none" stroke="#DDD6CA" stroke-width="1.5" />
                <circle cx="180" cy="140" r="85" fill="none" stroke="#DDD6CA" stroke-width="1.5" stroke-dasharray="4,4" />
                <circle cx="180" cy="140" r="45" fill="var(--jade-tint)" stroke="var(--jade-border)" stroke-width="2" />
                
                <!-- Center Core (Built Today) -->
                <circle cx="180" cy="140" r="12" fill="var(--jade-primary)" />
                <text x="180" y="168" font-family="IBM Plex Mono" font-size="10.5" font-weight="700" fill="var(--jade-primary)" text-anchor="middle">INSURANCE CLAIMS</text>

                <!-- 4 Regulated Sectors with Clean White Badges -->
                <rect x="75" y="10" width="210" height="24" rx="4" fill="#FFFFFF" stroke="#E2DDD5" />
                <text x="180" y="26" font-family="IBM Plex Sans" font-size="11" font-weight="700" fill="#1E1915" text-anchor="middle">Banking & Cards (RBI Compliance)</text>

                <rect x="245" y="128" width="110" height="24" rx="4" fill="#FFFFFF" stroke="#E2DDD5" />
                <text x="300" y="144" font-family="IBM Plex Sans" font-size="11" font-weight="700" fill="#4A433B" text-anchor="middle">Telecom Billing</text>

                <rect x="75" y="246" width="210" height="24" rx="4" fill="#FFFFFF" stroke="#E2DDD5" />
                <text x="180" y="262" font-family="IBM Plex Sans" font-size="11" font-weight="700" fill="#1E1915" text-anchor="middle">Healthcare Triage (DPDP Act)</text>
              </svg>
            </div>

            <!-- Invariant Box for Judges -->
            <div class="radar-invariant-box">
              <strong>THE GOLDEN RULE ACROSS ALL HIGH-RISK CALL CENTERS:</strong><br>
              Use small 3B models for natural conversation. Use <strong>deterministic code</strong> for financial and legal safety. Use <strong>PRISM</strong> to observe, diagnose, and prove reliability.
            </div>
          </div>

          <!-- Right: Concrete Roadmap & Closing Plaque -->
          <div class="s6-roadmap-container">
            <div class="slide-header-block" style="margin-bottom: 0;">
              <div class="slide-mandated-prompt">Key benefits, real-world impact, scalability, and future enhancements.</div>
              <h2 class="slide-headline" style="font-size: 30px;">Every call center in the world needs this architecture.</h2>
            </div>

            <div class="roadmap-timeline">
              <div class="roadmap-phase">
                <span class="phase-badge today">TODAY · COMPLETED</span>
                <div class="phase-info">
                  <h5>Edge Engine + PRISM Telemetry Spine</h5>
                  <p>Local Whisper STT, 3B LLM, SQLite database triggers, full PRISM multi-turn tracing.</p>
                  <span class="phase-metric-tag">✓ 100% Cancellation Success · Zero Plaintext PII</span>
                </div>
              </div>

              <div class="roadmap-phase">
                <span class="phase-badge next">NEXT · Q2 2026</span>
                <div class="phase-info">
                  <h5>Telephony & SIP Gateway Integration</h5>
                  <p>Direct Exotel and Twilio SIP telephone connections directly into the edge audio socket.</p>
                  <span class="phase-metric-tag" style="color: var(--spectrum-amber);">Target: Under 250ms Latency on Live Phone Lines</span>
                </div>
              </div>

              <div class="roadmap-phase">
                <span class="phase-badge scale">SCALE · H2 2026</span>
                <div class="phase-info">
                  <h5>Indian Regional Speech + Active Guardrails</h5>
                  <p>Hindi, Tamil, Telugu speech models with PRISM Guardrails running in live active inline mode.</p>
                  <span class="phase-metric-tag" style="color: var(--spectrum-violet);">Multilingual Coverage Across India</span>
                </div>
              </div>
            </div>

            <!-- Closing Plaque -->
            <div class="closing-thesis-banner">
              Can be interrupted. Can't be bullied. Won't leak.<br>
              <strong>Built to be diagnosed — proven by PRISM.</strong>
            </div>
          </div>
        </div>
      </section>

    </main>

    <!-- Persistent Bottom Chrome -->
    <footer class="stage-footer">
      <div class="footer-left-controls">
        <button class="btn-nav" id="prev-btn">‹ Prev</button>
        <button class="btn-nav" id="next-btn">Next ›</button>
        <button class="btn-autoplay" id="autoplay-btn">Auto-Play (15s)</button>
      </div>

      <div class="nav-pips" id="nav-pips-container">
        <div class="pip active" data-index="0">1</div>
        <div class="pip" data-index="1">2</div>
        <div class="pip" data-index="2">3</div>
        <div class="pip" data-index="4">4</div>
        <div class="pip" data-index="5">5</div>
        <div class="pip" data-index="6">6</div>
      </div>

      <!-- Clean Status Without Active Green Light -->
      <div class="footer-right-status">
        <span>PRISM BY BLOCK CONVEY · EVALUATION SUITE</span>
      </div>
    </footer>
  </div>

  <!-- Slide Engine JavaScript -->
  <script>
    class DeckController {
      constructor() {
        this.slides = Array.from(document.querySelectorAll('.slide'));
        this.pips = Array.from(document.querySelectorAll('.pip'));
        this.counterEl = document.getElementById('slide-counter');
        this.categoryEl = document.getElementById('slide-category-title');
        this.autoPlayBtn = document.getElementById('autoplay-btn');
        this.progressBar = document.getElementById('autoplay-progress');
        
        this.currentIndex = 0;
        this.totalSlides = this.slides.length;
        this.isAutoPlaying = false;
        this.autoPlayIntervalMs = 15000;
        this.autoPlayTimer = null;
        this.progressTimer = null;

        this.slideTitles = [
          "Problem Statement",
          "Existing Challenges",
          "Proposed Solution",
          "PRISM Usage",
          "System Workflow",
          "Impact & Future Scope"
        ];

        this.initEvents();
        this.initWaveform();

        const hash = parseInt(location.hash.replace('#', ''), 10);
        const initialSlide = (!isNaN(hash) && hash >= 1 && hash <= this.totalSlides) ? hash - 1 : 0;
        this.showSlide(initialSlide, false);
      }

      showSlide(index, updateHash = true) {
        if (index < 0 || index >= this.totalSlides) return;
        
        this.slides[this.currentIndex].classList.remove('active');
        this.pips[this.currentIndex].classList.remove('active');

        this.currentIndex = index;
        this.slides[this.currentIndex].classList.add('active');
        this.pips[this.currentIndex].classList.add('active');

        this.counterEl.textContent = `0${this.currentIndex + 1} / 0${this.totalSlides}`;
        this.categoryEl.textContent = this.slideTitles[this.currentIndex];

        if (updateHash) {
          location.hash = this.currentIndex + 1;
        }

        if (this.isAutoPlaying) {
          this.resetProgressBar();
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
          this.startAutoPlayTimer();
        } else {
          this.autoPlayBtn.classList.remove('active');
          this.autoPlayBtn.textContent = 'Auto-Play (15s)';
          this.stopAutoPlayTimer();
        }
      }

      startAutoPlayTimer() {
        this.stopAutoPlayTimer();
        this.resetProgressBar();
        this.autoPlayTimer = setInterval(() => this.next(), this.autoPlayIntervalMs);
      }

      stopAutoPlayTimer() {
        clearInterval(this.autoPlayTimer);
        clearInterval(this.progressTimer);
        this.progressBar.style.width = '0%';
      }

      resetProgressBar() {
        clearInterval(this.progressTimer);
        this.progressBar.style.width = '0%';
        const startTime = Date.now();
        this.progressTimer = setInterval(() => {
          const elapsed = Date.now() - startTime;
          const pct = Math.min((elapsed / this.autoPlayIntervalMs) * 100, 100);
          this.progressBar.style.width = `${pct}%`;
          if (pct >= 100) clearInterval(this.progressTimer);
        }, 100);
      }

      initEvents() {
        document.getElementById('next-btn').addEventListener('click', () => this.next());
        document.getElementById('prev-btn').addEventListener('click', () => this.prev());
        this.autoPlayBtn.addEventListener('click', () => this.toggleAutoPlay());

        this.pips.forEach(pip => {
          pip.addEventListener('click', (e) => {
            const idx = parseInt(e.target.getAttribute('data-index'), 10);
            this.showSlide(idx);
          });
        });

        window.addEventListener('hashchange', () => {
          const hash = parseInt(location.hash.replace('#', ''), 10);
          if (!isNaN(hash) && hash >= 1 && hash <= this.totalSlides && hash - 1 !== this.currentIndex) {
            this.showSlide(hash - 1, false);
          }
        });

        window.addEventListener('keydown', (e) => {
          if (['Space', 'ArrowRight', 'PageDown'].includes(e.code)) this.next();
          if (['ArrowLeft', 'PageUp'].includes(e.code)) this.prev();
          if (e.key >= '1' && e.key <= '6') this.showSlide(parseInt(e.key, 10) - 1);
          if (e.code === 'KeyP') this.toggleAutoPlay();
          if (e.code === 'KeyF') {
            if (!document.fullscreenElement) {
              document.documentElement.requestFullscreen().catch(() => {});
            } else {
              document.exitFullscreen().catch(() => {});
            }
          }
        });
      }

      initWaveform() {
        const canvas = document.getElementById('waveformCanvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        
        const resizeCanvas = () => {
          if (!canvas.parentElement) return;
          canvas.width = canvas.parentElement.clientWidth * window.devicePixelRatio;
          canvas.height = canvas.parentElement.clientHeight * window.devicePixelRatio;
          ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
        };
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        let step = 0;
        const render = () => {
          const w = canvas.parentElement.clientWidth;
          const h = canvas.parentElement.clientHeight;
          ctx.clearRect(0, 0, w, h);

          // Subtle Background Frequency Spectrogram Grid
          ctx.strokeStyle = '#EFECE4';
          ctx.lineWidth = 1;
          for (let x = 0; x < w; x += 36) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, h);
            ctx.stroke();
          }

          // Ambient Multi-Sine Waveform
          ctx.beginPath();
          ctx.lineWidth = 2.5;
          ctx.strokeStyle = '#1E1915';

          for (let x = 0; x < w; x++) {
            const mod1 = Math.sin((x * 0.015) + step);
            const mod2 = Math.cos((x * 0.035) - step * 0.6);
            const envelope = Math.sin((x / w) * Math.PI);
            const y = (h / 2) + (mod1 * 30 + mod2 * 14) * envelope;
            if (x === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
          }
          ctx.stroke();

          // Timeline Event Pins
          const pins = [
            { pct: 0.18, color: '#D97706', label: 'T2: Cancellation' },
            { pct: 0.52, color: '#DC2626', label: 'T4: Illegal Discount' },
            { pct: 0.84, color: '#543DB3', label: 'T5: Spoken Card' }
          ];

          pins.forEach(pin => {
            const px = w * pin.pct;
            ctx.beginPath();
            ctx.strokeStyle = pin.color;
            ctx.lineWidth = 1.5;
            ctx.setLineDash([3, 3]);
            ctx.moveTo(px, 15);
            ctx.lineTo(px, h - 15);
            ctx.stroke();
            ctx.setLineDash([]);

            ctx.beginPath();
            ctx.fillStyle = pin.color;
            ctx.arc(px, h / 2, 5, 0, Math.PI * 2);
            ctx.fill();

            ctx.font = '600 11px IBM Plex Mono';
            ctx.fillStyle = pin.color;
            ctx.fillText(pin.label, px - 35, 14);
          });

          step += 0.035;
          requestAnimationFrame(render);
        };
        render();
      }
    }

    document.addEventListener('DOMContentLoaded', () => {
      window.deck = new DeckController();
    });
  </script>
</body>
</html>
'''

with open("/home/aliz/Documents/Codes/forgeAI-hackathon/presentation/claimguard-pitch.html", "w") as f:
    f.write(html_content)

print("Updated presentation/claimguard-pitch.html successfully with fixed grid layout in slide 4!")
