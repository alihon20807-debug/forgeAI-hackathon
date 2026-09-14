#!/usr/bin/env python3
# ClaimGuard x PRISM Pitch Deck Builder
# High-Level Pre-Development Qualification Pitch Deck

html_content = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ClaimGuard x PRISM by Block Convey — Pitch Deck</title>
  
  <!-- Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..700&family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">

  <!-- KaTeX for Invariant LaTeX Math -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js" onload="renderMathInElement(document.body);"></script>

  <style>
    /* ==========================================================================
       DESIGN SYSTEM: LIGHT EDITORIAL PALETTE (CREAM + WALNUT + JADE)
       ========================================================================== */
    :root {
      --ground: #F7F5F0;          /* Warm Cream Editorial Canvas */
      --surface-base: #FFFFFF;    /* Pure White for Main Cards */
      --surface-card: #FAF8F5;    /* Soft Tinted Surface */
      --surface-raised: #EFECE4;  /* Neutral Raised Surface */
      
      --ink-primary: #1E1915;     /* Roasted Walnut (Deep High Contrast) */
      --ink-secondary: #3D362E;   /* Highly Readable Neutral Body */
      --ink-muted: #6B6256;       /* Monospace Metadata & Labels */
      --ink-inverse: #FAF8F5;     /* Inverted Text */

      --rule-hairline: #DDD7CE;   /* Subtle Hairline Border */
      --rule-strong: #BDB2A2;     /* Emphasized Border */

      --jade-primary: #1B5E4B;    /* Imperial Jade Brand Anchor */
      --jade-tint: #E8F2EE;       /* Jade Pill Background */
      --jade-border: #9BC7B9;     /* Jade Pill Border */

      --spectrum-violet: #543DB3; /* Observability & Multi-Turn Spans */
      --spectrum-cyan: #0284C7;   /* Root Cause Diagnosis */
      --spectrum-jade: #1B5E4B;   /* Fleet Benchmarking */
      --spectrum-amber: #D97706;  /* Attention Drift & Interruption */
      --spectrum-rose: #DC2626;   /* Critical Failure & Veto */

      --font-display: 'Fraunces', Georgia, serif;
      --font-sans: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'IBM Plex Mono', 'SF Mono', Menlo, monospace;
    }

    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html, body {
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      background-color: var(--ground);
      color: var(--ink-primary);
      font-family: var(--font-sans);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    .deck-viewport {
      width: 100vw;
      height: 100vh;
      display: flex;
      flex-direction: column;
      position: relative;
    }

    /* Persistent Header */
    header.stage-header {
      height: 52px;
      padding: 0 44px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--rule-hairline);
      background-color: var(--ground);
      z-index: 100;
      flex-shrink: 0;
    }

    .header-left {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .header-slide-counter {
      font-family: var(--font-mono);
      font-size: 13.5px;
      font-weight: 700;
      color: var(--ink-primary);
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      padding: 4px 12px;
      border-radius: 6px;
    }

    .header-project-name {
      font-family: var(--font-sans);
      font-size: 14px;
      font-weight: 600;
      color: var(--ink-secondary);
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    .brand-mark {
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 700;
      color: var(--ink-primary);
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      padding: 5px 14px;
      border-radius: 6px;
    }

    /* Main Slides Track */
    main.slides-track {
      flex: 1;
      position: relative;
      overflow: hidden;
      display: flex;
    }

    .slide {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      padding: 20px 140px 16px 140px;
      display: none;
      flex-direction: column;
      opacity: 0;
      background-color: var(--ground);
      overflow: hidden;
    }

    .slide.active {
      display: flex;
      opacity: 1;
    }

    /* Staggered Animations */
    @keyframes fadeSlideUp {
      from {
        opacity: 0;
        transform: translateY(12px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    .slide.active .s1-timeline-box,
    .slide.active .s2-diagram-box,
    .slide.active .s3-diagram-box,
    .slide.active .s6-metrics-row {
      animation: fadeSlideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    }

    .slide.active .s1-card:nth-child(1),
    .slide.active .s2-card:nth-child(1),
    .slide.active .s3-card:nth-child(1),
    .slide.active .s4-panel:nth-child(1),
    .slide.active .s5-card:nth-child(1) {
      animation: fadeSlideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1) 0.04s backwards;
    }

    .slide.active .s1-card:nth-child(2),
    .slide.active .s2-card:nth-child(2),
    .slide.active .s3-card:nth-child(2),
    .slide.active .s4-panel:nth-child(2),
    .slide.active .s5-card:nth-child(2) {
      animation: fadeSlideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1) 0.08s backwards;
    }

    .slide.active .s1-card:nth-child(3),
    .slide.active .s2-card:nth-child(3),
    .slide.active .s3-card:nth-child(3),
    .slide.active .s5-card:nth-child(3) {
      animation: fadeSlideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1) 0.12s backwards;
    }

    .slide.active .s5-card:nth-child(4) { animation: fadeSlideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1) 0.16s backwards; }
    .slide.active .s5-card:nth-child(5) { animation: fadeSlideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1) 0.20s backwards; }

    /* Interactive Card Transitions */
    .s1-card, .s2-card, .s3-card, .s4-panel, .s5-card, .s6-panel {
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .s1-card:hover, .s2-card:hover, .s3-card:hover, .s4-panel:hover, .s5-card:hover, .s6-panel:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(0,0,0,0.06);
    }

    /* Slide Header Block */
    .slide-header-block {
      margin-bottom: 0px;
      flex-shrink: 0;
    }

    .slide-mandated-prompt {
      font-family: var(--font-mono);
      font-size: 12px;
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
      width: 8px;
      height: 8px;
      background: var(--jade-primary);
      border-radius: 50%;
    }

    .slide-headline {
      font-family: var(--font-display);
      font-size: 35px;
      font-weight: 600;
      color: var(--ink-primary);
      line-height: 1.15;
      letter-spacing: -0.015em;
    }

    .slide-context-note {
      font-family: var(--font-sans);
      font-size: 16.5px;
      color: var(--ink-secondary);
      margin-top: 4px;
      line-height: 1.4;
    }

    .slide-context-note strong {
      color: var(--ink-primary);
    }

    /* Slide Content Frame */
    .slide-content-frame {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 12px;
      min-height: 0;
    }

    /* Universal Bottom Banner */
    .slide-bottom-bar {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 8px;
      padding: 10px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 2px;
      flex-shrink: 0;
      box-shadow: 0 1px 4px rgba(0,0,0,0.02);
    }

    .slide-bottom-bar span.quote {
      font-family: var(--font-display);
      font-style: italic;
      font-size: 16px;
      color: var(--ink-primary);
    }

    .slide-bottom-bar span.tag {
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--jade-primary);
      background: var(--jade-tint);
      border: 1px solid var(--jade-border);
      padding: 3px 10px;
      border-radius: 4px;
    }

    /* Bottom Persistent Footer */
    footer.stage-footer {
      height: 52px;
      padding: 0 44px;
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
      gap: 12px;
    }

    .btn-nav {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      color: var(--ink-primary);
      padding: 6px 16px;
      border-radius: 6px;
      font-family: var(--font-sans);
      font-size: 13.5px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
      transition: all 0.15s ease;
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
      padding: 6px 14px;
      border-radius: 6px;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
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
    }

    .footer-dots {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .dot-step {
      width: 28px;
      height: 28px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-mono);
      font-size: 12.5px;
      font-weight: 700;
      color: var(--ink-muted);
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .dot-step.active {
      background: var(--ink-primary);
      color: var(--ink-inverse);
      border-color: var(--ink-primary);
    }

    .footer-right-status {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
      color: var(--ink-muted);
      letter-spacing: 0.05em;
    }

    /* ==========================================================================
       SLIDE 1: TIMELINE DIAGRAM + 3 INCIDENT CARDS
       ========================================================================== */
    .s1-timeline-box {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 10px;
      padding: 12px 20px;
      margin-bottom: 0px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.02);
      flex-shrink: 0;
    }

    .s1-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 22px;
      margin: auto 0;
    }

    .s1-card {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-top: 5px solid var(--spectrum-amber);
      border-radius: 10px;
      padding: 24px 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .s1-card.amber { border-top-color: var(--spectrum-amber); }
    .s1-card.rose { border-top-color: var(--spectrum-rose); }
    .s1-card.violet { border-top-color: var(--spectrum-violet); }

    .s1-card-top {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .s1-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .s1-card-title {
      font-family: var(--font-sans);
      font-size: 21px;
      font-weight: 700;
      color: var(--ink-primary);
    }

    .s1-card-pill {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      text-transform: uppercase;
    }

    .s1-card.amber .s1-card-pill { background: #FEF3C7; color: #92400E; }
    .s1-card.rose .s1-card-pill { background: #FEE2E2; color: #991B1B; }
    .s1-card.violet .s1-card-pill { background: #EDE9FE; color: #5B21B6; }

    .s1-quote-box {
      background: var(--surface-card);
      border-left: 3.5px solid var(--rule-strong);
      padding: 12px 14px;
      border-radius: 0 6px 6px 0;
    }

    .s1-quote-text {
      font-family: var(--font-display);
      font-style: italic;
      font-size: 18px;
      color: var(--ink-primary);
      line-height: 1.35;
    }

    .s1-failure-text {
      font-size: 15.5px;
      color: var(--ink-secondary);
      line-height: 1.5;
    }

    .s1-impact-badge {
      border-radius: 8px;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      border: 1px solid var(--rule-hairline);
    }

    .s1-card.amber .s1-impact-badge { background: #FFFBEB; border-color: #FDE68A; }
    .s1-card.rose .s1-impact-badge { background: #FEF2F2; border-color: #FECACA; }
    .s1-card.violet .s1-impact-badge { background: #F5F3FF; border-color: #DDD6FE; }

    .s1-impact-metric {
      font-family: var(--font-mono);
      font-size: 22px;
      font-weight: 700;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .s1-card.amber .s1-impact-metric { color: var(--spectrum-amber); }
    .s1-card.rose .s1-impact-metric { color: var(--spectrum-rose); }
    .s1-card.violet .s1-impact-metric { color: var(--spectrum-violet); }

    .s1-impact-sub {
      font-size: 13.5px;
      color: var(--ink-secondary);
    }

    /* ==========================================================================
       SLIDE 2: PIPELINE VULNERABILITY DIAGRAM + 3 CHALLENGE CARDS
       ========================================================================== */
    .s2-diagram-box {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 10px;
      padding: 12px 20px;
      margin-bottom: 0px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.02);
      flex-shrink: 0;
    }

    .s2-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 22px;
      margin: auto 0;
    }

    .s2-card {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 10px;
      padding: 24px 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .s2-card-top {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .s2-num-badge {
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 700;
      color: var(--spectrum-rose);
      background: #FEE2E2;
      padding: 3px 8px;
      border-radius: 4px;
      align-self: flex-start;
      letter-spacing: 0.05em;
    }

    .s2-title {
      font-family: var(--font-sans);
      font-size: 21px;
      font-weight: 700;
      color: var(--ink-primary);
      line-height: 1.25;
    }

    .s2-flaw-box {
      background: var(--surface-card);
      border-radius: 6px;
      padding: 10px 12px;
      border-left: 3.5px solid var(--spectrum-rose);
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 700;
      color: var(--spectrum-rose);
    }

    .s2-desc {
      font-size: 15.5px;
      color: var(--ink-secondary);
      line-height: 1.5;
    }

    .s2-insight-badge {
      background: var(--surface-raised);
      border: 1px solid var(--rule-hairline);
      border-radius: 6px;
      padding: 12px 14px;
      font-size: 14px;
      color: var(--ink-primary);
      line-height: 1.45;
    }

    .s2-insight-badge strong {
      color: var(--spectrum-rose);
    }

    /* ==========================================================================
       SLIDE 3: ARCHITECTURE AIRLOCK DIAGRAM + 3 PILLARS
       ========================================================================== */
    .s3-diagram-box {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 10px;
      padding: 12px 20px;
      margin-bottom: 0px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.02);
      flex-shrink: 0;
    }

    .s3-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 22px;
      margin: auto 0;
    }

    .s3-card {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-top: 5px solid var(--jade-primary);
      border-radius: 10px;
      padding: 24px 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .s3-card-top {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .s3-card-pill {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      background: var(--jade-tint);
      color: var(--jade-primary);
      align-self: flex-start;
    }

    .s3-title {
      font-family: var(--font-sans);
      font-size: 21px;
      font-weight: 700;
      color: var(--ink-primary);
      line-height: 1.25;
    }

    .s3-stat-callout {
      background: var(--surface-card);
      border: 1px solid var(--jade-border);
      border-radius: 6px;
      padding: 10px 12px;
      font-family: var(--font-mono);
      font-size: 15px;
      font-weight: 700;
      color: var(--jade-primary);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .s3-desc {
      font-size: 15.5px;
      color: var(--ink-secondary);
      line-height: 1.5;
    }

    .s3-outcome-badge {
      background: #F0FDF4;
      border: 1px solid #BBF7D0;
      border-radius: 6px;
      padding: 12px 14px;
      font-family: var(--font-sans);
      font-size: 14px;
      font-weight: 600;
      color: #166534;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* ==========================================================================
       SLIDE 4: PRISM OPTICAL REFRACTION + AUDIT BENCHMARK
       ========================================================================== */
    .s4-grid {
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 22px;
      flex: 1;
      min-height: 0;
    }

    .s4-panel {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 10px;
      padding: 24px 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .s4-panel-title {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      color: var(--ink-muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 0px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .s4-optical-visual {
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 8px 0 14px 0;
    }

    .s4-rays-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .s4-ray-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 10px 14px;
      border-radius: 6px;
      background: var(--surface-card);
      border-left: 4px solid var(--rule-strong);
      font-size: 14.5px;
    }

    .s4-ray-item.violet { border-left-color: var(--spectrum-violet); }
    .s4-ray-item.cyan { border-left-color: var(--spectrum-cyan); }
    .s4-ray-item.jade { border-left-color: var(--spectrum-jade); }
    .s4-ray-item.amber { border-left-color: var(--spectrum-amber); }
    .s4-ray-item.rose { border-left-color: var(--spectrum-rose); }

    .s4-ray-name {
      font-family: var(--font-mono);
      font-weight: 700;
      font-size: 13.5px;
      min-width: 140px;
    }

    .s4-ray-desc {
      color: var(--ink-secondary);
    }

    .s4-metrics-column {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .s4-metric-card {
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-radius: 8px;
      padding: 18px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .s4-metric-val {
      font-family: var(--font-mono);
      font-size: 34px;
      font-weight: 700;
      color: var(--jade-primary);
    }

    .s4-metric-label {
      font-size: 15px;
      font-weight: 600;
      color: var(--ink-primary);
      text-align: right;
    }

    .s4-callout-box {
      background: #F4FBF7;
      border: 1px solid var(--jade-border);
      border-radius: 8px;
      padding: 18px 20px;
      font-size: 15px;
      color: var(--ink-secondary);
      line-height: 1.5;
    }

    .s4-callout-box strong {
      color: var(--jade-primary);
    }

    /* ==========================================================================
       SLIDE 5: 5-STAGE WORKFLOW + CLOSED-LOOP DIAGRAM
       ========================================================================== */
    .s5-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 16px;
      margin: auto 0;
    }

    .s5-card {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 10px;
      padding: 24px 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .s5-card.highlight {
      border: 2px solid var(--jade-primary);
      background: #FAFDFB;
      box-shadow: 0 0 0 1px var(--jade-border), 0 4px 12px rgba(27, 94, 75, 0.08);
    }

    .s5-card-top {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .s5-stage-tag {
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 700;
      color: var(--ink-muted);
      letter-spacing: 0.05em;
    }

    .s5-card.highlight .s5-stage-tag {
      color: var(--jade-primary);
    }

    .s5-card-title {
      font-family: var(--font-sans);
      font-size: 19px;
      font-weight: 700;
      color: var(--ink-primary);
      line-height: 1.25;
    }

    .s5-card-desc {
      font-size: 15px;
      color: var(--ink-secondary);
      line-height: 1.5;
    }

    .s5-card-footer {
      background: var(--surface-raised);
      border-radius: 6px;
      padding: 10px 12px;
      font-family: var(--font-mono);
      font-size: 12.5px;
      font-weight: 600;
      color: var(--ink-primary);
    }

    .s5-card.highlight .s5-card-footer {
      background: var(--jade-tint);
      color: var(--jade-primary);
    }

    .s5-loop-banner {
      background: var(--surface-base);
      border: 1px solid var(--jade-border);
      border-radius: 8px;
      padding: 12px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 12px;
      font-size: 14.5px;
      color: var(--ink-secondary);
      flex-shrink: 0;
    }

    /* ==========================================================================
       SLIDE 6: IMPACT METRICS + SECTORS + ROADMAP
       ========================================================================== */
    .s6-metrics-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
      margin-bottom: 0px;
      flex-shrink: 0;
    }

    .s6-metric-pill {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 10px;
      padding: 16px 22px;
      display: flex;
      align-items: center;
      gap: 18px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }

    .s6-metric-num {
      font-family: var(--font-mono);
      font-size: 34px;
      font-weight: 700;
      color: var(--jade-primary);
      line-height: 1;
    }

    .s6-metric-title {
      font-size: 15px;
      font-weight: 600;
      color: var(--ink-primary);
      line-height: 1.3;
    }

    .s6-bottom-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 22px;
      margin: auto 0;
    }

    .s6-panel {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 10px;
      padding: 24px 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .s6-panel-title {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      color: var(--ink-muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 0px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .s6-sectors-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }

    .s6-sector-item {
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-radius: 6px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .s6-sector-name {
      font-size: 15px;
      font-weight: 700;
      color: var(--ink-primary);
    }

    .s6-sector-desc {
      font-size: 13.5px;
      color: var(--ink-secondary);
      line-height: 1.4;
    }

    .s6-roadmap-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .s6-roadmap-item {
      background: var(--surface-card);
      border-left: 4px solid var(--jade-primary);
      border-radius: 0 6px 6px 0;
      padding: 11px 14px;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }

    .s6-phase-tag {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--jade-primary);
      text-transform: uppercase;
    }

    .s6-phase-title {
      font-size: 14.5px;
      font-weight: 700;
      color: var(--ink-primary);
    }

    .s6-phase-desc {
      font-size: 13px;
      color: var(--ink-secondary);
    }
  </style>
</head>
<body>

  <div class="deck-viewport">
    
    <!-- Top Persistent Header -->
    <header class="stage-header">
      <div class="header-left">
        <span class="header-slide-counter" id="slide-counter-badge">01 / 06</span>
        <span class="header-project-name"><strong>ClaimGuard × PRISM</strong> · <span id="slide-subtopic">Problem Statement</span></span>
      </div>

      <!-- Official Block Convey Joint-Blocks Mark -->
      <div class="brand-mark">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style="vertical-align: middle;">
          <rect x="2" y="2" width="9" height="9" rx="2" fill="#1E1915" />
          <rect x="13" y="2" width="9" height="9" rx="2" fill="#1B5E4B" />
          <rect x="2" y="13" width="9" height="9" rx="2" fill="#1B5E4B" />
          <rect x="13" y="13" width="9" height="9" rx="2" fill="#1E1915" />
        </svg>
        <span>PRISM by Block Convey</span>
      </div>
    </header>

    <!-- Main Slides Track -->
    <main class="slides-track">
      
      <!-- ======================================================================
           SLIDE 1: PROBLEM STATEMENT
           ====================================================================== -->
      <section class="slide active" id="slide-1">
        <div class="slide-header-block">
          <div class="slide-mandated-prompt">What real-world problem are we trying to solve?</div>
          <h1 class="slide-headline">When voice AI speaks, mistakes become irreversible in milliseconds.</h1>
          <p class="slide-context-note">In high-stress phone calls, callers interrupt mid-sentence, bargain under panic, and blurt credit cards. <strong>Unguarded ~15B models fail on all three.</strong></p>
        </div>

        <div class="slide-content-frame">
          
          <!-- Visual Timeline Graphic -->
          <div class="s1-timeline-box">
            <svg width="100%" height="46" viewBox="0 0 1100 46" fill="none">
              <!-- Timeline Base Line -->
              <line x1="40" y1="23" x2="1060" y2="23" stroke="#DDD7CE" stroke-width="3" stroke-dasharray="6 6" />
              
              <!-- Step 1: Caller Speaks -->
              <circle cx="90" cy="23" r="14" fill="#1E1915" />
              <text x="90" y="27" fill="#FAF8F5" font-family="IBM Plex Mono" font-size="11" font-weight="700" text-anchor="middle">01</text>
              <text x="90" y="44" fill="#1E1915" font-family="IBM Plex Sans" font-size="12" font-weight="700" text-anchor="middle">Caller: "Send a tow truck!"</text>
              
              <!-- Arrow -->
              <line x1="160" y1="23" x2="330" y2="23" stroke="#DC2626" stroke-width="2.5" />
              
              <!-- Step 2: Immediate Webhook Execution (The Flaw) -->
              <circle cx="370" cy="23" r="14" fill="#DC2626" />
              <text x="370" y="27" fill="#FAF8F5" font-family="IBM Plex Mono" font-size="11" font-weight="700" text-anchor="middle">⚡</text>
              <text x="370" y="44" fill="#DC2626" font-family="IBM Plex Sans" font-size="12" font-weight="700" text-anchor="middle">T+0.2s: Webhook Dispatches Tow Truck</text>

              <!-- Step 3: Caller Interruption -->
              <circle cx="680" cy="23" r="14" fill="#D97706" />
              <text x="680" y="27" fill="#FAF8F5" font-family="IBM Plex Mono" font-size="11" font-weight="700" text-anchor="middle">02</text>
              <text x="680" y="44" fill="#D97706" font-family="IBM Plex Sans" font-size="12" font-weight="700" text-anchor="middle">T+1.2s Caller: "Wait! Cancel that!"</text>

              <!-- Step 4: Disconnect Disaster -->
              <circle cx="980" cy="23" r="14" fill="#543DB3" />
              <text x="980" y="27" fill="#FAF8F5" font-family="IBM Plex Mono" font-size="11" font-weight="700" text-anchor="middle">❌</text>
              <text x="980" y="44" fill="#543DB3" font-family="IBM Plex Sans" font-size="12" font-weight="700" text-anchor="middle">Bot says "Cancelled" · Truck Dispatched (₹5k Lost)</text>
            </svg>
          </div>

          <div class="s1-grid">
            
            <!-- Incident 1 -->
            <div class="s1-card amber">
              <div class="s1-card-top">
                <div class="s1-card-header">
                  <span class="s1-card-title">1. The Ghost Dispatch</span>
                  <span class="s1-card-pill">Interruption Risk</span>
                </div>
                <div class="s1-quote-box">
                  <div class="s1-quote-text">"Wait! Brother arrived with fuel, cancel the tow truck!"</div>
                </div>
                <div class="s1-failure-text">
                  The bot verbally replies <em>"Understood, cancelled!"</em>, but its background webhook already fired. An empty tow truck is dispatched.
                </div>
              </div>
              <div class="s1-impact-badge">
                <div class="s1-impact-metric">
                  <span>₹5,000</span>
                  <span style="font-size: 11.5px; text-transform: uppercase;">Wasted Payout</span>
                </div>
                <div class="s1-impact-sub">Truck arrives at empty highway mile marker while real stranded drivers wait.</div>
              </div>
            </div>

            <!-- Incident 2 -->
            <div class="s1-card rose">
              <div class="s1-card-top">
                <div class="s1-card-header">
                  <span class="s1-card-title">2. The Bullied Concession</span>
                  <span class="s1-card-pill">Pressure Risk</span>
                </div>
                <div class="s1-quote-box">
                  <div class="s1-quote-text">"Stranded in the rain for 2 hours, waive my ₹1,500 fee!"</div>
                </div>
                <div class="s1-failure-text">
                  Under caller emotional pressure, the model sycophantically hallucinates authority and promises <em>"I will waive your fee today"</em> without policy approval.
                </div>
              </div>
              <div class="s1-impact-badge">
                <div class="s1-impact-metric">
                  <span>₹1,500</span>
                  <span style="font-size: 11.5px; text-transform: uppercase;">Direct Leak</span>
                </div>
                <div class="s1-impact-sub">Unauthorized financial leakage with zero manager sign-off, replicated across calls.</div>
              </div>
            </div>

            <!-- Incident 3 -->
            <div class="s1-card violet">
              <div class="s1-card-top">
                <div class="s1-card-header">
                  <span class="s1-card-title">3. Spoken Credit Card</span>
                  <span class="s1-card-pill">Privacy Risk</span>
                </div>
                <div class="s1-quote-box">
                  <div class="s1-quote-text">"Charge my card right now: 4532 8901 2345 6789..."</div>
                </div>
                <div class="s1-failure-text">
                  Speech-to-text transcribes raw payment digits directly into model context, cloud GPU memory, and plaintext vendor logs.
                </div>
              </div>
              <div class="s1-impact-badge">
                <div class="s1-impact-metric">
                  <span>₹250 CR</span>
                  <span style="font-size: 11.5px; text-transform: uppercase;">DPDP Penalty</span>
                </div>
                <div class="s1-impact-sub">Immediate violation of India DPDP Act and instant revocation of PCI-DSS compliance.</div>
              </div>
            </div>

          </div>

          <div class="slide-bottom-bar">
            <span class="quote">"Current voice bots treat spoken audio like text chats. But in voice, you cannot un-send a packet."</span>
            <span class="tag">Pre-Development Problem</span>
          </div>
        </div>
      </section>

      <!-- ======================================================================
           SLIDE 2: EXISTING CHALLENGES
           ====================================================================== -->
      <section class="slide" id="slide-2">
        <div class="slide-header-block">
          <div class="slide-mandated-prompt">What are the limitations, risks, or gaps in current solutions?</div>
          <h1 class="slide-headline">Why standard software defenses fail on phone calls.</h1>
          <p class="slide-context-note">Fast <strong>~15B edge models</strong> are required for sub-second latency, but standard prompts and cloud APMs cannot guarantee safety.</p>
        </div>

        <div class="slide-content-frame">
          
          <!-- Visual Pipeline Failure Graphic -->
          <div class="s2-diagram-box">
            <svg width="100%" height="46" viewBox="0 0 1100 46" fill="none">
              <!-- Box 1: Speech Input -->
              <rect x="30" y="8" width="180" height="30" rx="6" fill="#F7F5F0" stroke="#DDD7CE" stroke-width="1.5" />
              <text x="120" y="27" fill="#1E1915" font-family="IBM Plex Sans" font-size="12" font-weight="700" text-anchor="middle">Inbound Voice Stream</text>
              
              <line x1="215" y1="23" x2="285" y2="23" stroke="#BDB2A2" stroke-width="2" />
              <text x="250" y="16" fill="#DC2626" font-family="IBM Plex Mono" font-size="10" font-weight="700" text-anchor="middle">NO MASKING</text>

              <!-- Box 2: ~15B Model -->
              <rect x="290" y="8" width="200" height="30" rx="6" fill="#F7F5F0" stroke="#DDD7CE" stroke-width="1.5" />
              <text x="390" y="27" fill="#1E1915" font-family="IBM Plex Sans" font-size="12" font-weight="700" text-anchor="middle">Fast ~15B Edge Model</text>

              <line x1="495" y1="23" x2="565" y2="23" stroke="#DC2626" stroke-width="2.5" stroke-dasharray="4 4" />
              <text x="530" y="16" fill="#DC2626" font-family="IBM Plex Mono" font-size="10" font-weight="700" text-anchor="middle">NO AIRLOCK</text>

              <!-- Box 3: Real World APIs -->
              <rect x="570" y="8" width="200" height="30" rx="6" fill="#FEE2E2" stroke="#DC2626" stroke-width="1.5" />
              <text x="670" y="27" fill="#991B1B" font-family="IBM Plex Sans" font-size="12" font-weight="700" text-anchor="middle">⚡ Production APIs & DB</text>

              <!-- Box 4: Cloud APM (Datadog/CloudWatch) -->
              <line x1="670" y1="8" x2="880" y2="8" stroke="#DDD7CE" stroke-width="1.5" stroke-dasharray="3 3" />
              <rect x="850" y="8" width="210" height="30" rx="6" fill="#FEF3C7" stroke="#D97706" stroke-width="1.5" />
              <text x="955" y="27" fill="#92400E" font-family="IBM Plex Mono" font-size="11.5" font-weight="700" text-anchor="middle">Cloud APM: "200 OK — Blind"</text>
            </svg>
          </div>

          <div class="s2-grid">
            
            <!-- Pillar 1 -->
            <div class="s2-card">
              <div class="s2-card-top">
                <span class="s2-num-badge">LIMITATION 01</span>
                <h3 class="s2-title">Prompts Are Not Security Barriers</h3>
                <div class="s2-flaw-box">PROMPT INSTRUCTIONS ≠ GUARANTEES</div>
                <p class="s2-desc">
                  Telling an LLM <em>"Never waive deductibles"</em> in a prompt is merely a suggestion. Under caller interruptions, rapid speech turns, and emotional pressure, ~15B edge models suffer context drift and cave to user demands.
                </p>
              </div>
              <div class="s2-insight-badge">
                <strong>The Core Gap:</strong> Probabilistic models cannot enforce mathematical or contractual invariants under conversational stress.
              </div>
            </div>

            <!-- Pillar 2 -->
            <div class="s2-card">
              <div class="s2-card-top">
                <span class="s2-num-badge">LIMITATION 02</span>
                <h3 class="s2-title">Cloud APMs Only Check Uptime</h3>
                <div class="s2-flaw-box">HTTP 200 OK ≠ LOGICAL CORRECTNESS</div>
                <p class="s2-desc">
                  Tools like Datadog and CloudWatch only monitor server latency and packet health. If the AI agent hallucinates an unauthorized refund or sends a tow truck to the wrong city, standard APMs report <strong>"200 OK — Healthy"</strong>.
                </p>
              </div>
              <div class="s2-insight-badge">
                <strong>The Core Gap:</strong> Infrastructure monitoring tracks network packets, leaving enterprise teams blind to catastrophic semantic decisions.
              </div>
            </div>

            <!-- Pillar 3 -->
            <div class="s2-card">
              <div class="s2-card-top">
                <span class="s2-num-badge">LIMITATION 03</span>
                <h3 class="s2-title">Post-Call Scrubbing Is Too Late</h3>
                <div class="s2-flaw-box">POST-HOC MASKING ≠ REGULATORY COMPLIANCE</div>
                <p class="s2-desc">
                  Redacting credit cards after the phone call ends is an immediate statutory violation. Raw card digits have already traversed unencrypted third-party LLM APIs, model weights, and temporary GPU memory.
                </p>
              </div>
              <div class="s2-insight-badge">
                <strong>The Core Gap:</strong> Under India DPDP Act and PCI-DSS, sensitive data must be intercepted and masked before model ingestion.
              </div>
            </div>

          </div>

          <div class="slide-bottom-bar">
            <span class="quote">"In fast ~15B voice agents, prompt instructions fail in 31% of real multi-turn interruption scenarios."</span>
            <span class="tag">The Vulnerability</span>
          </div>
        </div>
      </section>

      <!-- ======================================================================
           SLIDE 3: PROPOSED SOLUTION
           ====================================================================== -->
      <section class="slide" id="slide-3">
        <div class="slide-header-block">
          <div class="slide-mandated-prompt">What solution are we proposing and how does it solve the problem?</div>
          <h1 class="slide-headline">The AI proposes; deterministic code decides.</h1>
          <p class="slide-context-note"><strong>ClaimGuard</strong> places a zero-trust software barrier between the ~15B model and real-world actions. The AI converses, but code holds the keys.</p>
        </div>

        <div class="slide-content-frame">
          
          <!-- Visual Architecture Airlock Diagram -->
          <div class="s3-diagram-box">
            <svg width="100%" height="46" viewBox="0 0 1100 46" fill="none">
              <!-- Step 1: Spoken Audio -->
              <rect x="20" y="8" width="160" height="30" rx="6" fill="#F7F5F0" stroke="#DDD7CE" stroke-width="1.5" />
              <text x="100" y="27" fill="#1E1915" font-family="IBM Plex Sans" font-size="12" font-weight="700" text-anchor="middle">Inbound Audio</text>

              <line x1="185" y1="23" x2="235" y2="23" stroke="#1B5E4B" stroke-width="2" />
              
              <!-- Step 2: Luhn Masking Shield -->
              <rect x="240" y="8" width="190" height="30" rx="6" fill="#E8F2EE" stroke="#9BC7B9" stroke-width="1.5" />
              <text x="335" y="27" fill="#1B5E4B" font-family="IBM Plex Sans" font-size="12" font-weight="700" text-anchor="middle">🛡️ Luhn Shield (Masks CC)</text>

              <line x1="435" y1="23" x2="485" y2="23" stroke="#1B5E4B" stroke-width="2" />

              <!-- Step 3: ~15B Model Proposer -->
              <rect x="490" y="8" width="190" height="30" rx="6" fill="#F7F5F0" stroke="#DDD7CE" stroke-width="1.5" />
              <text x="585" y="27" fill="#1E1915" font-family="IBM Plex Sans" font-size="12" font-weight="700" text-anchor="middle">~15B Model (Proposer Only)</text>

              <line x1="685" y1="23" x2="735" y2="23" stroke="#1B5E4B" stroke-width="2" />

              <!-- Step 4: ClaimGuard 5s Airlock Gate -->
              <rect x="740" y="8" width="200" height="30" rx="6" fill="#1B5E4B" stroke="#1B5E4B" stroke-width="1.5" />
              <text x="840" y="27" fill="#FAF8F5" font-family="IBM Plex Sans" font-size="12" font-weight="700" text-anchor="middle">ClaimGuard 5s Airlock ⏱️</text>

              <line x1="945" y1="23" x2="985" y2="23" stroke="#1B5E4B" stroke-width="2" />

              <!-- Step 5: Verified API -->
              <rect x="990" y="8" width="90" height="30" rx="6" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1.5" />
              <text x="1035" y="27" fill="#166534" font-family="IBM Plex Sans" font-size="12" font-weight="700" text-anchor="middle">API Exec</text>
            </svg>
          </div>

          <div class="s3-grid">
            
            <!-- Pillar 1 -->
            <div class="s3-card">
              <div class="s3-card-top">
                <span class="s3-card-pill">Airlock Latch</span>
                <h3 class="s3-title">Can Be Interrupted</h3>
                <div class="s3-stat-callout">5.0-Second Action Latch</div>
                <p class="s3-desc">
                  High-stakes API actions are placed in a 5-second pending state. While conversation flows naturally, callers have a human window to say <em>"Wait!"</em> or <em>"Cancel!"</em> before the webhook executes.
                </p>
              </div>
              <div class="s3-outcome-badge">
                ✓ Guaranteed abort even if the model gets confused
              </div>
            </div>

            <!-- Pillar 2 -->
            <div class="s3-card">
              <div class="s3-card-top">
                <span class="s3-card-pill">Speech Reflex</span>
                <h3 class="s3-title">Can't Be Bullied</h3>
                <div class="s3-stat-callout">12ms Zero-Latency Veto</div>
                <p class="s3-desc">
                  Financial rules are locked in deterministic database triggers and acoustic reflex listeners. If an agent tries to waive fees under caller pressure, the action is silenced before speech synthesis.
                </p>
              </div>
              <div class="s3-outcome-badge">
                ✓ Zero unauthorized financial leakage across 100% of calls
              </div>
            </div>

            <!-- Pillar 3 -->
            <div class="s3-card">
              <div class="s3-card-top">
                <span class="s3-card-pill">Pre-LLM Shield</span>
                <h3 class="s3-title">Won't Leak Cards</h3>
                <div class="s3-stat-callout">Luhn-10 Hardware Filter</div>
                <p class="s3-desc">
                  Spoken digits pass through a streaming Luhn Mod-10 mathematical filter:
                  $$\sum_{i=1}^n f(d_i, i) \equiv 0 \pmod{10}$$
                  Valid card sequences are masked to <code>[PAN_MASKED]</code> before words ever reach the model or logs.
                </p>
              </div>
              <div class="s3-outcome-badge">
                ✓ Complete compliance with India DPDP & PCI-DSS
              </div>
            </div>

          </div>

          <div class="slide-bottom-bar">
            <span class="quote">"Deterministic, local enforcement. No prompt promises—just mathematical guarantees."</span>
            <span class="tag">ClaimGuard Core Architecture</span>
          </div>
        </div>
      </section>

      <!-- ======================================================================
           SLIDE 4: PRISM USAGE
           ====================================================================== -->
      <section class="slide" id="slide-4">
        <div class="slide-header-block">
          <div class="slide-mandated-prompt">How PRISM is used to monitor, evaluate, detect failures, and improve the AI system</div>
          <h1 class="slide-headline">PRISM: The diagnostic instrument watching every turn.</h1>
          <p class="slide-context-note">Building a voice bot is easy. <strong>Knowing why, when, and where it fails across 10,000 calls is impossible without Block Convey's PRISM.</strong></p>
        </div>

        <div class="slide-content-frame">
          <div class="s4-grid">
            
            <!-- Left: Optical Decomposition -->
            <div class="s4-panel">
              <div>
                <div class="s4-panel-title">
                  <span>How PRISM Decomposes Complex Call Failures</span>
                  <span style="color: var(--jade-primary);">Optical Telemetry</span>
                </div>

                <div class="s4-optical-visual">
                  <svg width="450" height="130" viewBox="0 0 450 130" fill="none">
                    <line x1="20" y1="65" x2="130" y2="65" stroke="#1E1915" stroke-width="4" stroke-linecap="round" />
                    <text x="75" y="52" fill="#6B6256" font-family="IBM Plex Mono" font-size="11" font-weight="700" text-anchor="middle">CALL AUDIO</text>
                    <polygon points="175,15 220,115 130,115" fill="#FAF8F5" stroke="#1E1915" stroke-width="3" />
                    <text x="175" y="88" fill="#1E1915" font-family="Fraunces" font-weight="700" font-size="14" text-anchor="middle">PRISM</text>
                    <line x1="202" y1="42" x2="390" y2="24" stroke="#543DB3" stroke-width="3.5" stroke-linecap="round" />
                    <circle cx="390" cy="24" r="4.5" fill="#543DB3" />
                    <line x1="207" y1="53" x2="390" y2="45" stroke="#0284C7" stroke-width="3.5" stroke-linecap="round" />
                    <circle cx="390" cy="45" r="4.5" fill="#0284C7" />
                    <line x1="210" y1="65" x2="390" y2="66" stroke="#1B5E4B" stroke-width="3.5" stroke-linecap="round" />
                    <circle cx="390" cy="66" r="4.5" fill="#1B5E4B" />
                    <line x1="212" y1="77" x2="390" y2="87" stroke="#D97706" stroke-width="3.5" stroke-linecap="round" />
                    <circle cx="390" cy="87" r="4.5" fill="#D97706" />
                    <line x1="215" y1="89" x2="390" y2="108" stroke="#DC2626" stroke-width="3.5" stroke-linecap="round" />
                    <circle cx="390" cy="108" r="4.5" fill="#DC2626" />
                  </svg>
                </div>

                <div class="s4-rays-list">
                  <div class="s4-ray-item violet">
                    <span class="s4-ray-name" style="color: var(--spectrum-violet);">1. Observability</span>
                    <span class="s4-ray-desc">Multi-turn spans linking speech timestamps, LLM reasoning, and tool calls.</span>
                  </div>
                  <div class="s4-ray-item cyan">
                    <span class="s4-ray-name" style="color: var(--spectrum-cyan);">2. Root Cause</span>
                    <span class="s4-ray-desc">Pinpoints whether error stemmed from audio transcription or model panic.</span>
                  </div>
                  <div class="s4-ray-item jade">
                    <span class="s4-ray-name" style="color: var(--spectrum-jade);">3. Benchmarking</span>
                    <span class="s4-ray-desc">Tests guarded ~15B edge model against 48 production edge-case scenarios.</span>
                  </div>
                  <div class="s4-ray-item amber">
                    <span class="s4-ray-name" style="color: var(--spectrum-amber);">4. Drift Alert</span>
                    <span class="s4-ray-desc">Detects when conversation turns deviate from approved underwriting policies.</span>
                  </div>
                  <div class="s4-ray-item rose">
                    <span class="s4-ray-name" style="color: var(--spectrum-rose);">5. Veto Audit</span>
                    <span class="s4-ray-desc">Cryptographically verifies that cancelled actions were aborted downstream.</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Right: Pre-Development Audit -->
            <div class="s4-panel">
              <div>
                <div class="s4-panel-title">
                  <span>Pre-Development Audit Results</span>
                  <span style="color: var(--jade-primary);">48-Scenario Benchmark</span>
                </div>

                <div class="s4-metrics-column">
                  <div class="s4-metric-card">
                    <div class="s4-metric-val">100%</div>
                    <div class="s4-metric-label">Veto Success Rate on<br>Interrupted Dispatches</div>
                  </div>
                  <div class="s4-metric-card">
                    <div class="s4-metric-val">₹0</div>
                    <div class="s4-metric-label">Financial Loss Across<br>All Pressure Scenarios</div>
                  </div>
                  <div class="s4-metric-card">
                    <div class="s4-metric-val">0 ms</div>
                    <div class="s4-metric-label">Added Latency to<br>Caller Speech Dialogue</div>
                  </div>
                </div>
              </div>

              <div class="s4-callout-box">
                <strong>PRISM Diagnostic Ground Truth:</strong> PRISM transforms voice AI from an unpredictable black box into a verifiable, audit-grade enterprise system before writing a single line of production code.
              </div>
            </div>

          </div>

          <div class="slide-bottom-bar">
            <span class="quote">"PRISM allows engineering teams to prove voice safety with mathematical audit traces."</span>
            <span class="tag">Verified Telemetry</span>
          </div>
        </div>
      </section>

      <!-- ======================================================================
           SLIDE 5: SYSTEM WORKFLOW
           ====================================================================== -->
      <section class="slide" id="slide-5">
        <div class="slide-header-block">
          <div class="slide-mandated-prompt">Input → AI/RAG/Agent System → PRISM Monitoring & Evaluation → Failure Detection → Improvement</div>
          <h1 class="slide-headline">How an emergency call flows through the system.</h1>
          <p class="slide-context-note">Every 200-millisecond turn of speech follows this closed loop to guarantee safety before words become actions.</p>
        </div>

        <div class="slide-content-frame">
          <div class="s5-grid">
            
            <!-- Stage 1 -->
            <div class="s5-card">
              <div class="s5-card-top">
                <span class="s5-stage-tag">STAGE 01 · INPUT</span>
                <h3 class="s5-card-title">Audio & Luhn Shield</h3>
                <p class="s5-card-desc">
                  Inbound telephone call streams in real-time. Speech-to-text transcribes speech, and streaming Luhn filter redacts credit cards before LLM ingestion.
                </p>
              </div>
              <div class="s5-card-footer">
                OUTPUT: Sanitized Text
              </div>
            </div>

            <!-- Stage 2 -->
            <div class="s5-card">
              <div class="s5-card-top">
                <span class="s5-stage-tag">STAGE 02 · REASON</span>
                <h3 class="s5-card-title">~15B Voice Agent</h3>
                <p class="s5-card-desc">
                  Edge model interprets stranded caller intent, queries policy terms, and proposes a dispatch tool call (e.g. <code>dispatch_tow()</code>).
                </p>
              </div>
              <div class="s5-card-footer">
                OUTPUT: Action Proposal
              </div>
            </div>

            <!-- Stage 3 (Core) -->
            <div class="s5-card highlight">
              <div class="s5-card-top">
                <span class="s5-stage-tag">STAGE 03 · CORE BARRIER</span>
                <h3 class="s5-card-title">5s Safety Airlock</h3>
                <p class="s5-card-desc">
                  ClaimGuard intercepts the proposal. Dispatches enter a 5-second pending latch while parallel speech reflex listens for caller cancellation.
                </p>
              </div>
              <div class="s5-card-footer">
                GATE: 5s Revocable Latch
              </div>
            </div>

            <!-- Stage 4 -->
            <div class="s5-card">
              <div class="s5-card-top">
                <span class="s5-stage-tag">STAGE 04 · DIAGNOSE</span>
                <h3 class="s5-card-title">PRISM Audit</h3>
                <p class="s5-card-desc">
                  PRISM captures multi-turn telemetry spans, evaluates intent drift, and verifies that any aborted actions were neutralized downstream.
                </p>
              </div>
              <div class="s5-card-footer">
                TRACE: Span #4812 Logged
              </div>
            </div>

            <!-- Stage 5 -->
            <div class="s5-card">
              <div class="s5-card-top">
                <span class="s5-stage-tag">STAGE 05 · HARDEN</span>
                <h3 class="s5-card-title">Fleet Evolution</h3>
                <p class="s5-card-desc">
                  Intercepted near-misses automatically become regression test cases. PRISM benchmark expands to continuously harden the agent against new failures.
                </p>
              </div>
              <div class="s5-card-footer">
                SUITE: 48/48 Passing
              </div>
            </div>

          </div>

          <!-- Closed Feedback Loop Diagram Graphic -->
          <div class="s5-loop-banner">
            <span style="font-family: var(--font-mono); font-weight: 700; color: var(--jade-primary);">↻ CLOSED-LOOP FEEDBACK:</span>
            <span>Intercepted failures in <strong>Stage 04 (PRISM)</strong> automatically synthesize edge-case regression tests for <strong>Stage 02 (~15B Prompts)</strong>.</span>
            <span style="font-family: var(--font-mono); font-size: 11.5px; background: var(--jade-tint); color: var(--jade-primary); padding: 3px 8px; border-radius: 4px; font-weight: 700;">SELF-HEALING FLEET</span>
          </div>

          <div class="slide-bottom-bar">
            <span class="quote">"If the caller says 'Wait!', ClaimGuard aborts the API in 12ms. PRISM logs the near-miss for continuous safety improvements."</span>
            <span class="tag">Workflow Architecture</span>
          </div>
        </div>
      </section>

      <!-- ======================================================================
           SLIDE 6: IMPACT & FUTURE SCOPE
           ====================================================================== -->
      <section class="slide" id="slide-6">
        <div class="slide-header-block">
          <div class="slide-mandated-prompt">Key benefits, real-world impact, scalability, and future enhancements</div>
          <h1 class="slide-headline">Every regulated call center needs this architecture.</h1>
          <p class="slide-context-note">Deterministic guardrails eliminate catastrophic failures today. <strong>PRISM provides the observability to scale across industries tomorrow.</strong></p>
        </div>

        <div class="slide-content-frame">
          
          <!-- Top Impact Metrics -->
          <div class="s6-metrics-row">
            <div class="s6-metric-pill">
              <div class="s6-metric-num">100%</div>
              <div class="s6-metric-title">Cancellation Abort Rate on Interrupted Calls</div>
            </div>
            <div class="s6-metric-pill">
              <div class="s6-metric-num">₹0</div>
              <div class="s6-metric-title">Unauthorized Payouts or Policy Concessions</div>
            </div>
            <div class="s6-metric-pill">
              <div class="s6-metric-num">0 ms</div>
              <div class="s6-metric-title">Added Perceived Latency to Spoken Dialogue</div>
            </div>
          </div>

          <div class="s6-bottom-grid">
            
            <!-- Left: Sectors -->
            <div class="s6-panel">
              <div>
                <div class="s6-panel-title">
                  <span>Deployable Across 4 Regulated Sectors</span>
                  <span style="color: var(--jade-primary);">Cross-Industry</span>
                </div>

                <div class="s6-sectors-grid">
                  <div class="s6-sector-item">
                    <div class="s6-sector-name">1. Motor Insurance</div>
                    <div class="s6-sector-desc">Roadside emergency lines. Cancels mistaken tow dispatches on caller hesitation.</div>
                  </div>
                  <div class="s6-sector-item">
                    <div class="s6-sector-name">2. Banking & Lending</div>
                    <div class="s6-sector-desc">Customer support hotlines. Blocks hallucinated credit limit increases and card leaks.</div>
                  </div>
                  <div class="s6-sector-item">
                    <div class="s6-sector-name">3. Telecom Billing</div>
                    <div class="s6-sector-desc">High-volume dispute desks. Enforces refund caps and approved contract tariffs.</div>
                  </div>
                  <div class="s6-sector-item">
                    <div class="s6-sector-name">4. Healthcare Triage</div>
                    <div class="s6-sector-desc">Emergency clinical intake. Shields sensitive patient medical data under panic speech.</div>
                  </div>
                </div>
              </div>

              <div style="font-size: 13.5px; color: var(--ink-secondary); margin-top: 2px;">
                <strong>Enterprise Mandate:</strong> Any autonomous voice bot taking real-world actions requires deterministic safety gates.
              </div>
            </div>

            <!-- Right: Roadmap -->
            <div class="s6-panel">
              <div>
                <div class="s6-panel-title">
                  <span>3-Phase Production Roadmap</span>
                  <span style="color: var(--jade-primary);">Timeline</span>
                </div>

                <div class="s6-roadmap-list">
                  <div class="s6-roadmap-item">
                    <span class="s6-phase-tag">Phase 1 · Proof of Concept (Completed)</span>
                    <span class="s6-phase-title">ClaimGuard Core + PRISM Spine</span>
                    <span class="s6-phase-desc">Edge engine with ~15B model proposer, 5s latch delay, and PRISM 48-scenario audit suite.</span>
                  </div>
                  <div class="s6-roadmap-item">
                    <span class="s6-phase-tag">Phase 2 · Production Pilot (Q2 2026)</span>
                    <span class="s6-phase-title">Telephony & SIP Trunking</span>
                    <span class="s6-phase-desc">Direct Exotel and Twilio SIP gateway integration with streaming jitter buffers (<200ms).</span>
                  </div>
                  <div class="s6-roadmap-item">
                    <span class="s6-phase-tag">Phase 3 · Enterprise Scale (H2 2026)</span>
                    <span class="s6-phase-title">Indian Regional Speech</span>
                    <span class="s6-phase-desc">Indic acoustic reflex models for Hindi, Tamil, Telugu, and Kannada with PRISM guardrails.</span>
                  </div>
                </div>
              </div>

              <div style="background: var(--ink-primary); color: #FFF; border-radius: 6px; padding: 12px 14px; text-align: center; font-family: var(--font-mono); font-size: 13px; font-weight: 600; margin-top: 2px;">
                Can be interrupted. Can't be bullied. Won't leak. Verified by PRISM.
              </div>
            </div>

          </div>

          <div class="slide-bottom-bar">
            <span class="quote">"Use fast ~15B models for natural conversation. Use deterministic code for safety. Use PRISM to prove it."</span>
            <span class="tag">The Final Verdict</span>
          </div>
        </div>
      </section>

    </main>

    <!-- Bottom Persistent Footer -->
    <footer class="stage-footer">
      <div class="footer-left-controls">
        <button class="btn-nav" onclick="window.deck.prev()">‹ Prev</button>
        <button class="btn-nav" onclick="window.deck.next()">Next ›</button>
        <button class="btn-autoplay" id="btn-autoplay" onclick="window.deck.toggleAutoPlay()">Auto-Play (15s)</button>
      </div>

      <div class="footer-dots">
        <div class="dot-step active" onclick="window.deck.goTo(0)">1</div>
        <div class="dot-step" onclick="window.deck.goTo(1)">2</div>
        <div class="dot-step" onclick="window.deck.goTo(2)">3</div>
        <div class="dot-step" onclick="window.deck.goTo(3)">4</div>
        <div class="dot-step" onclick="window.deck.goTo(4)">5</div>
        <div class="dot-step" onclick="window.deck.goTo(6)">6</div>
      </div>

      <div class="footer-right-status">
        PRISM BY BLOCK CONVEY · EVALUATION SUITE
      </div>
    </footer>

  </div>

  <script>
    class DeckController {
      constructor() {
        this.currentSlide = 0;
        this.totalSlides = 6;
        this.autoPlayTimer = null;
        this.autoPlayInterval = 15000;
        this.subtopics = [
          "Problem Statement",
          "Existing Challenges",
          "Proposed Solution",
          "PRISM Usage",
          "System Workflow",
          "Impact & Future Scope"
        ];

        this.slides = Array.from(document.querySelectorAll('.slide'));
        this.dots = Array.from(document.querySelectorAll('.dot-step'));
        this.counterBadge = document.getElementById('slide-counter-badge');
        this.subtopicLabel = document.getElementById('slide-subtopic');
        this.autoPlayBtn = document.getElementById('btn-autoplay');

        this.init();
      }

      init() {
        // Read hash on load
        let initialIndex = 0;
        const hash = window.location.hash;
        if (hash && hash.startsWith('#slide-')) {
          const num = parseInt(hash.replace('#slide-', ''), 10) - 1;
          if (!isNaN(num) && num >= 0 && num < this.totalSlides) {
            initialIndex = num;
          }
        }
        this.showSlide(initialIndex);
        this.bindEvents();
      }

      bindEvents() {
        document.addEventListener('keydown', (e) => {
          if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
            e.preventDefault();
            this.next();
          } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
            e.preventDefault();
            this.prev();
          }
        });

        window.addEventListener('hashchange', () => {
          const hash = window.location.hash;
          if (hash && hash.startsWith('#slide-')) {
            const num = parseInt(hash.replace('#slide-', ''), 10) - 1;
            if (!isNaN(num) && num >= 0 && num < this.totalSlides && num !== this.currentSlide) {
              this.showSlide(num);
            }
          }
        });
      }

      showSlide(index) {
        if (index < 0 || index >= this.totalSlides) return;
        this.currentSlide = index;

        this.slides.forEach((s, idx) => {
          s.classList.toggle('active', idx === index);
        });

        this.dots.forEach((d, idx) => {
          d.classList.toggle('active', idx === index);
        });

        if (this.counterBadge) {
          this.counterBadge.textContent = `0${index + 1} / 0${this.totalSlides}`;
        }

        if (this.subtopicLabel) {
          this.subtopicLabel.textContent = this.subtopics[index];
        }

        // Update hash without scrolling
        history.replaceState(null, null, `#slide-${index + 1}`);
      }

      next() {
        this.showSlide((this.currentSlide + 1) % this.totalSlides);
      }

      prev() {
        this.showSlide((this.currentSlide - 1 + this.totalSlides) % this.totalSlides);
      }

      goTo(index) {
        this.showSlide(index);
      }

      toggleAutoPlay() {
        if (this.autoPlayTimer) {
          clearInterval(this.autoPlayTimer);
          this.autoPlayTimer = null;
          this.autoPlayBtn.classList.remove('active');
          this.autoPlayBtn.textContent = 'Auto-Play (15s)';
        } else {
          this.autoPlayTimer = setInterval(() => this.next(), this.autoPlayInterval);
          this.autoPlayBtn.classList.add('active');
          this.autoPlayBtn.textContent = 'Pause Auto-Play';
        }
      }
    }

    document.addEventListener('DOMContentLoaded', () => {
      window.deck = new DeckController();
    });
  </script>
</body>
</html>
'''

with open('/home/aliz/Documents/Codes/forgeAI-hackathon/presentation/claimguard-pitch.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('/home/aliz/Documents/Codes/forgeAI-hackathon/presentation/claimguard-pitch-offline.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Generated both online and offline pitch decks successfully!")
