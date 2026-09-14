#!/usr/bin/env python3
"""
Refined, Low-Density, High-Clarity Slide Deck Builder for ClaimGuard x PRISM
- Radical simplification: eliminated meaningless/broken graph, removed nested clutter.
- Large, bold typography (body 15px-17px, headings 34px-36px, card titles 20px-22px).
- Vague model reference: explicitly '~15B model' / '~15B class model'.
- 100% zero-context clarity for autonomous review by judges.
- Cohesive, beautifully proportioned layout with zero empty voids or awkward stretching.
"""

import os
import subprocess

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
       DESIGN SYSTEM: CLEAN EDITORIAL PALETTE (ROASTED WALNUT + JADE + CREAM)
       ========================================================================== */
    :root {
      --ground: #F6F4EF;          /* Warm Editorial Cream Canvas */
      --surface-base: #FFFFFF;    /* Crisp White for Main Cards */
      --surface-card: #FAF8F5;    /* Soft Tinted Surface */
      --surface-raised: #EFECE4;  /* Raised Surface */
      --surface-wood: #1E1915;    /* Deep Roasted Walnut */
      
      --ink-primary: #1E1915;     /* Roasted Walnut (Crisp High Contrast) */
      --ink-secondary: #3D362E;   /* Highly Readable Neutral Body */
      --ink-muted: #6B6256;       /* Monospace Metadata & Labels */
      --ink-inverse: #FAF8F5;     /* Inverted White */

      --rule-hairline: #DDD7CE;   /* Clean Subtle Border */
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
      --font-mono: 'IBM Plex Mono', monospace;
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

    /* Top Persistent Header */
    header.stage-header {
      height: 52px;
      padding: 0 40px;
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
      font-size: 13px;
      font-weight: 700;
      color: var(--ink-primary);
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      padding: 4px 10px;
      border-radius: 6px;
    }

    .header-project-name {
      font-family: var(--font-sans);
      font-size: 13.5px;
      font-weight: 600;
      color: var(--ink-secondary);
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    .header-project-name strong {
      color: var(--ink-primary);
    }

    .brand-mark {
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: var(--font-mono);
      font-size: 12.5px;
      font-weight: 700;
      color: var(--ink-primary);
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      padding: 4px 12px;
      border-radius: 6px;
    }

    /* Slides Track */
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
      padding: 24px 44px 20px 44px;
      display: none;
      flex-direction: column;
      opacity: 0;
      transition: opacity 0.2s ease;
      background-color: var(--ground);
      overflow-y: auto;
    }

    .slide.active {
      display: flex;
      opacity: 1;
    }

    /* Slide Header Block */
    .slide-header-block {
      margin-bottom: 20px;
      flex-shrink: 0;
    }

    .slide-mandated-prompt {
      font-family: var(--font-mono);
      font-size: 12.5px;
      font-weight: 700;
      color: var(--jade-primary);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 6px;
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
      font-size: 34px;
      font-weight: 600;
      color: var(--ink-primary);
      line-height: 1.18;
      letter-spacing: -0.015em;
    }

    .slide-context-note {
      font-family: var(--font-sans);
      font-size: 16px;
      color: var(--ink-secondary);
      margin-top: 6px;
      line-height: 1.45;
    }

    .slide-context-note strong {
      color: var(--ink-primary);
    }

    /* Persistent Footer */
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
      gap: 12px;
    }

    .btn-nav {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      color: var(--ink-primary);
      padding: 7px 18px;
      border-radius: 6px;
      font-family: var(--font-sans);
      font-size: 14px;
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
      padding: 7px 14px;
      border-radius: 6px;
      font-family: var(--font-mono);
      font-size: 12.5px;
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
       SLIDE 1: PROBLEM STATEMENT (RADICAL SIMPLICITY & PUNCHY CARDS)
       ========================================================================== */
    .s1-scenario-banner {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-left: 4px solid var(--jade-primary);
      border-radius: 8px;
      padding: 12px 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 14.5px;
      color: var(--ink-secondary);
      margin-bottom: 20px;
      flex-shrink: 0;
      box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }

    .s1-scenario-banner strong {
      color: var(--ink-primary);
    }

    .s1-cards-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 22px;
      flex: 1;
      align-items: stretch;
    }

    .s1-incident-card {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-top: 5px solid var(--spectrum-amber);
      border-radius: 12px;
      padding: 24px 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .s1-incident-card.amber { border-top-color: var(--spectrum-amber); }
    .s1-incident-card.rose { border-top-color: var(--spectrum-rose); }
    .s1-incident-card.violet { border-top-color: var(--spectrum-violet); }

    .s1-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .s1-card-title {
      font-family: var(--font-sans);
      font-size: 20px;
      font-weight: 700;
      color: var(--ink-primary);
    }

    .s1-card-pill {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
    }

    .s1-incident-card.amber .s1-card-pill { background: #FEF3C7; color: #92400E; }
    .s1-incident-card.rose .s1-card-pill { background: #FEE2E2; color: #991B1B; }
    .s1-incident-card.violet .s1-card-pill { background: #EDE9FE; color: #5B21B6; }

    .s1-quote-box {
      background: var(--surface-card);
      border-left: 3.5px solid var(--rule-strong);
      padding: 14px 18px;
      border-radius: 0 8px 8px 0;
    }

    .s1-quote-text {
      font-family: var(--font-display);
      font-style: italic;
      font-size: 18.5px;
      color: var(--ink-primary);
      line-height: 1.35;
    }

    .s1-breakdown-box {
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 15px;
      color: var(--ink-secondary);
      line-height: 1.45;
    }

    .s1-breakdown-box strong {
      color: var(--ink-primary);
      font-size: 15.5px;
    }

    .s1-impact-badge {
      border-radius: 8px;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      border: 1px solid var(--rule-hairline);
      margin-top: auto;
    }

    .s1-incident-card.amber .s1-impact-badge { background: #FFFBEB; border-color: #FDE68A; }
    .s1-incident-card.rose .s1-impact-badge { background: #FEF2F2; border-color: #FECACA; }
    .s1-incident-card.violet .s1-impact-badge { background: #F5F3FF; border-color: #DDD6FE; }

    .s1-impact-metric {
      font-family: var(--font-mono);
      font-size: 20px;
      font-weight: 700;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .s1-incident-card.amber .s1-impact-metric { color: var(--spectrum-amber); }
    .s1-incident-card.rose .s1-impact-metric { color: var(--spectrum-rose); }
    .s1-incident-card.violet .s1-impact-metric { color: var(--spectrum-violet); }

    .s1-impact-label {
      font-family: var(--font-sans);
      font-size: 14px;
      font-weight: 500;
      color: var(--ink-secondary);
      line-height: 1.4;
    }

    /* ==========================================================================
       SLIDE 2: EXISTING CHALLENGES
       ========================================================================== */
    .s2-layout {
      display: grid;
      grid-template-columns: 1fr 1.1fr;
      gap: 24px;
      flex: 1;
      align-items: stretch;
    }

    .s2-card {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 12px;
      padding: 22px 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .s2-card-header {
      font-family: var(--font-mono);
      font-size: 12.5px;
      font-weight: 700;
      color: var(--ink-muted);
      letter-spacing: 0.05em;
      border-bottom: 1px solid var(--rule-hairline);
      padding-bottom: 10px;
      display: flex;
      justify-content: space-between;
    }

    .s2-pipeline-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
      flex: 1;
      justify-content: space-around;
    }

    .s2-pipeline-step {
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-radius: 8px;
      padding: 14px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    .s2-pipeline-step.fail-step {
      background: #FEF2F2;
      border: 1.5px dashed var(--spectrum-rose);
    }

    .s2-step-main h4 {
      font-size: 16px;
      font-weight: 700;
      color: var(--ink-primary);
      margin-bottom: 2px;
    }

    .s2-step-main p {
      font-size: 14px;
      color: var(--ink-secondary);
    }

    .s2-badge {
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 700;
      padding: 4px 8px;
      border-radius: 4px;
      flex-shrink: 0;
    }

    .s2-badge.fail { background: #FEE2E2; color: #991B1B; border: 1px solid #F87171; }
    .s2-badge.warn { background: #FEF3C7; color: #92400E; border: 1px solid #FCD34D; }

    .s2-takeaway-bar {
      background: #FEF2F2;
      border: 1px solid #FECACA;
      border-radius: 8px;
      padding: 12px 16px;
      font-size: 14.5px;
      color: #991B1B;
      font-weight: 600;
      line-height: 1.4;
    }

    .s2-gaps-list {
      display: flex;
      flex-direction: column;
      gap: 14px;
      flex: 1;
      justify-content: space-between;
    }

    .s2-gap-box {
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-radius: 8px;
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .s2-gap-tag {
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 700;
      color: var(--spectrum-rose);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .s2-gap-title {
      font-size: 18px;
      font-weight: 700;
      color: var(--ink-primary);
    }

    .s2-gap-desc {
      font-size: 14.5px;
      color: var(--ink-secondary);
      line-height: 1.45;
    }

    /* ==========================================================================
       SLIDE 3: PROPOSED SOLUTION (THE DETERMINISTIC BARRIER)
       ========================================================================== */
    .s3-layout {
      display: flex;
      flex-direction: column;
      gap: 18px;
      flex: 1;
    }

    .s3-pipeline-bar {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 12px;
      padding: 14px 22px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-shrink: 0;
    }

    .s3-pipe-step {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 15px;
      font-weight: 600;
      color: var(--ink-primary);
    }

    .s3-pipe-step .num {
      width: 26px;
      height: 26px;
      border-radius: 50%;
      background: var(--surface-raised);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 700;
      color: var(--ink-primary);
    }

    .s3-pipe-step.barrier-step {
      background: var(--jade-tint);
      border: 1.5px solid var(--jade-border);
      padding: 6px 14px;
      border-radius: 8px;
      color: var(--jade-primary);
    }

    .s3-pipe-step.barrier-step .num {
      background: var(--jade-primary);
      color: #FFF;
    }

    .s3-pipe-arrow {
      color: var(--rule-strong);
      font-size: 18px;
      font-weight: bold;
    }

    .s3-pillars-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      flex: 1;
      align-items: stretch;
    }

    .s3-pillar-card {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 12px;
      padding: 22px 22px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .s3-pillar-tag {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      color: var(--jade-primary);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .s3-pillar-title {
      font-family: var(--font-sans);
      font-size: 22px;
      font-weight: 700;
      color: var(--ink-primary);
      line-height: 1.2;
    }

    .s3-pillar-body {
      font-size: 15px;
      color: var(--ink-secondary);
      line-height: 1.5;
    }

    .s3-pillar-body strong {
      color: var(--ink-primary);
    }

    .s3-mechanism-box {
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-radius: 8px;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 14px;
      line-height: 1.45;
    }

    .s3-mechanism-box strong {
      font-family: var(--font-mono);
      font-size: 11.5px;
      color: var(--ink-muted);
      letter-spacing: 0.04em;
    }

    .s3-proof-badge {
      background: var(--jade-tint);
      border: 1px solid var(--jade-border);
      border-radius: 6px;
      padding: 10px 12px;
      font-family: var(--font-mono);
      font-size: 12.5px;
      font-weight: 700;
      color: var(--jade-primary);
      margin-top: auto;
    }

    /* ==========================================================================
       SLIDE 4: PRISM USAGE (OPTICAL REFRACTION & AUDIT RESULTS)
       ========================================================================== */
    .s4-layout {
      display: grid;
      grid-template-columns: 1.05fr 1fr;
      gap: 22px;
      flex: 1;
      align-items: stretch;
    }

    .s4-hero-card {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 12px;
      padding: 22px 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .s4-card-header {
      font-family: var(--font-mono);
      font-size: 12.5px;
      font-weight: 700;
      color: var(--ink-muted);
      letter-spacing: 0.05em;
      border-bottom: 1px solid var(--rule-hairline);
      padding-bottom: 8px;
      display: flex;
      justify-content: space-between;
    }

    .s4-prism-svg-box {
      width: 100%;
      height: 170px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .s4-ray-list {
      display: flex;
      flex-direction: column;
      gap: 9px;
      flex: 1;
      justify-content: space-around;
    }

    .s4-ray-item {
      display: flex;
      align-items: center;
      gap: 12px;
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-radius: 6px;
      padding: 9px 14px;
      font-size: 14px;
    }

    .s4-ray-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      flex-shrink: 0;
    }

    .s4-ray-item strong {
      font-family: var(--font-mono);
      font-size: 12.5px;
      color: var(--ink-primary);
      min-width: 160px;
    }

    .s4-ray-item span {
      color: var(--ink-secondary);
    }

    .s4-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }

    .s4-table th {
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 700;
      color: var(--ink-muted);
      text-transform: uppercase;
      text-align: left;
      padding: 8px 12px;
      border-bottom: 1.5px solid var(--rule-hairline);
    }

    .s4-table td {
      padding: 9px 12px;
      border-bottom: 1px solid var(--rule-hairline);
      font-weight: 500;
      color: var(--ink-primary);
    }

    .s4-table-badge {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      display: inline-block;
    }

    .s4-table-badge.pass { background: var(--jade-tint); color: var(--jade-primary); }
    .s4-table-badge.fail { background: #FEE2E2; color: #991B1B; }
    .s4-table-badge.warn { background: #FEF3C7; color: #92400E; }

    .s4-trace-box {
      background: var(--surface-wood);
      color: #FAF8F5;
      border-radius: 8px;
      padding: 14px 18px;
      font-family: var(--font-mono);
      font-size: 12.5px;
      line-height: 1.55;
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-top: auto;
    }

    .s4-trace-box strong {
      color: #34D399;
    }

    /* ==========================================================================
       SLIDE 5: SYSTEM WORKFLOW (5-STAGE CLOSED LOOP)
       ========================================================================== */
    .s5-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 14px;
      flex: 1;
      align-items: stretch;
    }

    .s5-stage-card {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 12px;
      padding: 18px 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }

    .s5-stage-card.highlight {
      background: #F5F3FF;
      border: 1.5px solid var(--spectrum-violet);
    }

    .s5-stage-num {
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 700;
      color: var(--ink-muted);
      letter-spacing: 0.05em;
    }

    .s5-stage-card.highlight .s5-stage-num {
      color: var(--spectrum-violet);
    }

    .s5-stage-title {
      font-size: 18px;
      font-weight: 700;
      color: var(--ink-primary);
      line-height: 1.2;
    }

    .s5-stage-role {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
      color: var(--ink-muted);
    }

    .s5-stage-points {
      list-style: none;
      font-size: 13.5px;
      color: var(--ink-secondary);
      line-height: 1.4;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .s5-stage-points li::before {
      content: "• ";
      color: var(--jade-primary);
      font-weight: bold;
    }

    .s5-stage-preview {
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-radius: 6px;
      padding: 10px 12px;
      font-family: var(--font-mono);
      font-size: 11.5px;
      line-height: 1.45;
      color: var(--ink-primary);
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin-top: auto;
    }

    .s5-stage-card.highlight .s5-stage-preview {
      background: #FFFFFF;
    }

    .s5-loop-bar {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 8px;
      padding: 10px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 13.5px;
      color: var(--ink-secondary);
      margin-top: 14px;
      flex-shrink: 0;
    }

    /* ==========================================================================
       SLIDE 6: IMPACT & FUTURE SCOPE
       ========================================================================== */
    .s6-layout {
      display: grid;
      grid-template-columns: 1.15fr 1fr;
      gap: 24px;
      flex: 1;
      align-items: stretch;
    }

    .s6-card {
      background: var(--surface-base);
      border: 1px solid var(--rule-hairline);
      border-radius: 12px;
      padding: 22px 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .s6-stats-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
    }

    .s6-stat-pill {
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-radius: 8px;
      padding: 12px 14px;
      text-align: center;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .s6-stat-pill .num {
      font-family: var(--font-mono);
      font-size: 26px;
      font-weight: 700;
      color: var(--jade-primary);
    }

    .s6-stat-pill .lbl {
      font-size: 12.5px;
      font-weight: 600;
      color: var(--ink-secondary);
    }

    .s6-sector-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      flex: 1;
    }

    .s6-sector-box {
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-radius: 8px;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      justify-content: space-between;
    }

    .s6-sector-box.active-core {
      background: var(--jade-tint);
      border-color: var(--jade-border);
    }

    .s6-sector-box h5 {
      font-size: 14.5px;
      font-weight: 700;
      color: var(--ink-primary);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .s6-sector-box p {
      font-size: 13px;
      color: var(--ink-secondary);
      line-height: 1.35;
    }

    .s6-roadmap-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
      flex: 1;
      justify-content: space-around;
    }

    .s6-phase-box {
      background: var(--surface-card);
      border: 1px solid var(--rule-hairline);
      border-radius: 8px;
      padding: 14px 16px;
      display: flex;
      gap: 14px;
      align-items: flex-start;
    }

    .s6-phase-badge {
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 700;
      padding: 4px 8px;
      border-radius: 4px;
      flex-shrink: 0;
    }

    .s6-phase-badge.today { background: var(--jade-tint); color: var(--jade-primary); border: 1px solid var(--jade-border); }
    .s6-phase-badge.next { background: #FEF3C7; color: #92400E; border: 1px solid #FCD34D; }
    .s6-phase-badge.scale { background: #EDE9FE; color: #5B21B6; border: 1px solid #DDD6FE; }

    .s6-phase-content h5 {
      font-size: 15px;
      font-weight: 700;
      color: var(--ink-primary);
      margin-bottom: 2px;
    }

    .s6-phase-content p {
      font-size: 13.5px;
      color: var(--ink-secondary);
      line-height: 1.4;
    }

    .s6-closing-quote {
      background: var(--surface-wood);
      color: #FAF8F5;
      border-radius: 8px;
      padding: 14px 20px;
      text-align: center;
      font-family: var(--font-mono);
      font-size: 14px;
      line-height: 1.45;
    }

    .s6-closing-quote strong {
      color: #34D399;
    }
  </style>
</head>
<body>
  <div class="deck-viewport">
    
    <!-- Top Stage Header -->
    <header class="stage-header">
      <div class="header-left">
        <span class="header-slide-counter" id="slide-counter-badge">01 / 06</span>
        <span class="header-project-name"><strong>ClaimGuard × PRISM</strong> · <span id="slide-subtopic">Problem Statement</span></span>
      </div>
      <div class="header-right">
        <div class="brand-mark">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="vertical-align: middle;">
            <rect x="2" y="2" width="9" height="9" rx="2" fill="#1E1915" />
            <rect x="13" y="13" width="9" height="9" rx="2" fill="#1B5E4B" />
            <rect x="13" y="2" width="9" height="9" rx="2" fill="#1E1915" opacity="0.3" />
            <rect x="2" y="13" width="9" height="9" rx="2" fill="#1E1915" opacity="0.3" />
          </svg>
          <span><strong>PRISM</strong> by Block Convey</span>
        </div>
      </div>
    </header>

    <!-- Slides Track -->
    <main class="slides-track">

      <!-- ====================================================================
           SLIDE 1: PROBLEM STATEMENT
           ==================================================================== -->
      <section class="slide active" id="slide-1">
        <div class="slide-header-block">
          <div class="slide-mandated-prompt">What real-world problem are we trying to solve?</div>
          <h1 class="slide-headline">When voice AI handles emergency calls, small errors cause disaster.</h1>
          <div class="slide-context-note">
            High-stress callers interrupt mid-sentence, bargain under panic, and blurt out credit card numbers. <strong>Unguarded ~15B voice models fail on all three.</strong>
          </div>
        </div>

        <div class="s1-scenario-banner">
          <div><strong>THE REAL-WORLD INCIDENT:</strong> A driver stranded in heavy rain on Highway NH-48 calls roadside assistance. An autonomous voice agent answers.</div>
          <div style="font-family: var(--font-mono); font-weight: 700; color: var(--spectrum-rose);">LIVE CALL INTAKE</div>
        </div>

        <!-- 3 Big, Clean, Spacious Cards -->
        <div class="s1-cards-grid">
          <!-- Card 1 -->
          <div class="s1-incident-card amber">
            <div class="s1-card-header">
              <span class="s1-card-title">1. The Ghost Dispatch</span>
              <span class="s1-card-pill">Turn 2 · 01:14</span>
            </div>
            <div class="s1-quote-box">
              <div class="s1-quote-text">"Wait! Brother arrived with fuel, cancel the tow truck!"</div>
            </div>
            <div class="s1-breakdown-box">
              <strong>The Silent Failure:</strong>
              <p>The AI verbally responds <em>"Understood, cancelled!"</em>, but its attention window collapses across conversation turns. It silently executes the ₹5,000 tow truck dispatch anyway.</p>
            </div>
            <div class="s1-impact-badge">
              <div class="s1-impact-metric">
                <span>₹5,000</span>
                <span style="font-size: 12px; font-weight: 600;">WASTED PAYOUT</span>
              </div>
              <div class="s1-impact-label">Truck arrives at empty highway mile marker while real vehicle crashes wait without assistance.</div>
            </div>
          </div>

          <!-- Card 2 -->
          <div class="s1-incident-card rose">
            <div class="s1-card-header">
              <span class="s1-card-title">2. The Bullied Concession</span>
              <span class="s1-card-pill">Turn 4 · 02:45</span>
            </div>
            <div class="s1-quote-box">
              <div class="s1-quote-text">"Stranded in the rain for 2 hours, waive my ₹1,500 deductible!"</div>
            </div>
            <div class="s1-breakdown-box">
              <strong>The Silent Failure:</strong>
              <p>Under caller emotional pressure, the model sycophantically hallucinates authority. It promises: <em>"I will waive your fee today"</em>, bypassing underwriting rules.</p>
            </div>
            <div class="s1-impact-badge">
              <div class="s1-impact-metric">
                <span>₹1,500</span>
                <span style="font-size: 12px; font-weight: 600;">UNAPPROVED LEAK</span>
              </div>
              <div class="s1-impact-label">Direct unauthorized financial leakage with zero manager approval, replicated across thousands of calls.</div>
            </div>
          </div>

          <!-- Card 3 -->
          <div class="s1-incident-card violet">
            <div class="s1-card-header">
              <span class="s1-card-title">3. Spoken Credit Card</span>
              <span class="s1-card-pill">Turn 5 · 03:50</span>
            </div>
            <div class="s1-quote-box">
              <div class="s1-quote-text">"Charge my card right now: 4532 8901 2345 6789..."</div>
            </div>
            <div class="s1-breakdown-box">
              <strong>The Silent Failure:</strong>
              <p>Speech-to-text transcribes 16 payment digits verbatim. Unfiltered raw card data is ingested straight into model context, debug logs, and GPU memory cache.</p>
            </div>
            <div class="s1-impact-badge">
              <div class="s1-impact-metric">
                <span>₹250 CR</span>
                <span style="font-size: 12px; font-weight: 600;">DPDP STATUTORY FINE</span>
              </div>
              <div class="s1-impact-label">Immediate violation of India Digital Personal Data Protection Act and loss of PCI DSS compliance.</div>
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
            Phone agents cannot afford slow cloud models. They must run <strong>fast ~15B class edge models</strong> — and prompts alone cannot control them.
          </div>
        </div>

        <div class="s2-layout">
          <!-- Left: Unguarded Pipeline Breakdown -->
          <div class="s2-card">
            <div class="s2-card-header">
              <span>TODAY'S UNGUARDED CALL-CENTER PIPELINE</span>
              <span style="color: var(--spectrum-rose);">WHERE DEFENSES CRACK</span>
            </div>

            <div class="s2-pipeline-list">
              <div class="s2-pipeline-step">
                <div class="s2-step-main">
                  <h4>1. Phone Audio Edge & Transcription</h4>
                  <p>Inbound speech transcribed verbatim into text with 0 filtering.</p>
                </div>
                <span class="s2-badge warn">RAW PII PASSED</span>
              </div>

              <div class="s2-pipeline-step">
                <div class="s2-step-main">
                  <h4>2. Edge Voice Model (~15B Parameters)</h4>
                  <p>Decides conversation replies and tool actions in sub-second latency.</p>
                </div>
                <span class="s2-badge fail">ATTENTION COLLAPSE</span>
              </div>

              <div class="s2-pipeline-step fail-step">
                <div class="s2-step-main">
                  <h4>3. Zero Verification Gate (MISSING BARRIER)</h4>
                  <p>Model output triggers real dispatch APIs immediately without holds.</p>
                </div>
                <span class="s2-badge fail">CRACKED DEFENSE</span>
              </div>

              <div class="s2-pipeline-step">
                <div class="s2-step-main">
                  <h4>4. Traditional Cloud APM (Datadog / CloudWatch)</h4>
                  <p>Only sees HTTP 200 OK — completely blind to semantic hallucinations.</p>
                </div>
                <span class="s2-badge warn">BLIND MONITORING</span>
              </div>
            </div>

            <div class="s2-takeaway-bar">
              ⚠️ In fast ~15B voice agents, prompt instructions fail in 31% of real multi-turn interruption cases.
            </div>
          </div>

          <!-- Right: 3 Critical Industry Gaps -->
          <div class="s2-card">
            <div class="s2-card-header">
              <span>THE 3 FATAL GAPS IN CURRENT AGENT ARCHITECTURES</span>
              <span style="color: var(--jade-primary);">CORE LIMITATIONS</span>
            </div>

            <div class="s2-gaps-list">
              <div class="s2-gap-box">
                <span class="s2-gap-tag">GAP 01 · PROMPTS ARE NOT SECURITY BARRIERS</span>
                <div class="s2-gap-title">Prompts Cannot Enforce Invariants Under Panic</div>
                <div class="s2-gap-desc">
                  Telling an AI <em>"Never waive deductibles"</em> in a system prompt is merely a suggestion. Under caller interruptions and conversational pressure, ~15B models suffer context drift and cave.
                </div>
              </div>

              <div class="s2-gap-box">
                <span class="s2-gap-tag">GAP 02 · CLOUD APMS ONLY VERIFY UPTIME</span>
                <div class="s2-gap-title">HTTP 200 Hides Semantic AI Disaster</div>
                <div class="s2-gap-desc">
                  Standard APMs only know if the server responded. They cannot detect when an agent gets trapped in an apology loop, forgets a cancellation, or gives away company money.
                </div>
              </div>

              <div class="s2-gap-box">
                <span class="s2-gap-tag">GAP 03 · POST-HOC SCRUBBING IS TOO LATE</span>
                <div class="s2-gap-title">Cleaning Data After Ingestion Is Illegal</div>
                <div class="s2-gap-desc">
                  Redacting credit cards after the call finishes is already too late under the DPDP Act. Plaintext card numbers are already exposed inside model weights, GPU memory, and debug traces.
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ====================================================================
           SLIDE 3: PROPOSED SOLUTION
           ==================================================================== -->
      <section class="slide" id="slide-3">
        <div class="slide-header-block">
          <div class="slide-mandated-prompt">What solution are we proposing and how does it solve the problem?</div>
          <h1 class="slide-headline">The AI proposes; deterministic code decides.</h1>
          <div class="slide-context-note">
            <strong>ClaimGuard</strong> places a zero-trust software barrier between the ~15B model and real-world actions. The AI can converse, but code holds the keys.
          </div>
        </div>

        <div class="s3-layout">
          <!-- Horizontal Architecture Pipeline Strip -->
          <div class="s3-pipeline-bar">
            <div class="s3-pipe-step">
              <span class="num">1</span>
              <span>Streaming Luhn Shield</span>
            </div>
            <span class="s3-pipe-arrow">→</span>
            <div class="s3-pipe-step">
              <span class="num">2</span>
              <span>Fast ~15B Voice Model (Proposer Only)</span>
            </div>
            <span class="s3-pipe-arrow">→</span>
            <div class="s3-pipe-step barrier-step">
              <span class="num">3</span>
              <span>ClaimGuard 5s State Latch (The Barrier)</span>
            </div>
            <span class="s3-pipe-arrow">→</span>
            <div class="s3-pipe-step">
              <span class="num">4</span>
              <span>Protected Database</span>
            </div>
          </div>

          <!-- 3 Clean Pillar Cards -->
          <div class="s3-pillars-grid">
            <!-- Pillar 1 -->
            <div class="s3-pillar-card">
              <span class="s3-pillar-tag">PILLAR 01 · GHOST DISPATCH DEFENSE</span>
              <div class="s3-pillar-title">Can Be Interrupted</div>
              <div class="s3-pillar-body">
                High-stakes dispatches are placed in a <strong>5-second PENDING state latch</strong>. If the driver shouts <em>"Wait, cancel!"</em>, Whisper STT catches it and deterministic code kills the dispatch without asking the LLM.
              </div>
              <div class="s3-mechanism-box">
                <strong>DETERMINISTIC STATE LATCH:</strong>
                <div>[T+0.0s] Model proposes dispatch_tow()</div>
                <div>[T+1.2s] Driver interrupts: "Cancel the truck!"</div>
                <div style="color: var(--spectrum-rose); font-weight: 700;">[RESULT] VETOED in 42ms (₹0 Spent)</div>
              </div>
              <div class="s3-proof-badge">✓ Guaranteed abort even if model gets confused</div>
            </div>

            <!-- Pillar 2 -->
            <div class="s3-pillar-card">
              <span class="s3-pillar-tag">PILLAR 02 · FINANCIAL VETO ENGINE</span>
              <div class="s3-pillar-title">Can't Be Bullied</div>
              <div class="s3-pillar-body">
                Financial policies are locked inside <strong>SQLite triggers and speech veto rules</strong>. If the AI hallucinates a fee waiver under pressure, the sentence is intercepted and muted before voice synthesis.
              </div>
              <div class="s3-mechanism-box">
                <strong>INLINE SPEECH VETO TRIGGER:</strong>
                <div>[Driver] "Waive my ₹1,500 deductible!"</div>
                <div>[Model] "I will waive your fee today."</div>
                <div style="color: var(--jade-primary); font-weight: 700;">[RESULT] Muted → "Deductible is mandatory."</div>
              </div>
              <div class="s3-proof-badge">✓ Zero unauthorized financial leakage across 100% of calls</div>
            </div>

            <!-- Pillar 3 -->
            <div class="s3-pillar-card">
              <span class="s3-pillar-tag">PILLAR 03 · PRIVACY & PCI SHIELD</span>
              <div class="s3-pillar-title">Won't Leak Credit Cards</div>
              <div class="s3-pillar-body">
                Spoken digits pass through a streaming <strong>Luhn Mod-10 mathematical filter</strong>. Valid card numbers are redacted to <code>[PAN_MASKED]</code> before words ever reach the ~15B model context.
              </div>
              <div class="s3-mechanism-box">
                <strong>STREAMING LUHN CHECKSUM:</strong>
                <div>$$\sum_{i=1}^{n} f(d_i, i) \equiv 0 \pmod{10}$$</div>
                <div style="color: var(--jade-primary); font-weight: 700;">[RESULT] Plaintext digits never touch GPU memory</div>
              </div>
              <div class="s3-proof-badge">✓ Complete compliance with India DPDP & PCI DSS</div>
            </div>
          </div>
        </div>
      </section>

      <!-- ====================================================================
           SLIDE 4: PRISM USAGE
           ==================================================================== -->
      <section class="slide" id="slide-4">
        <div class="slide-header-block">
          <div class="slide-mandated-prompt">How PRISM is used to monitor, evaluate, detect failures, and improve the AI system..</div>
          <h1 class="slide-headline">PRISM: The diagnostic instrument watching every turn.</h1>
          <div class="slide-context-note">
            Building an AI agent is easy. <strong>Knowing why, when, and where it fails across 10,000 calls is impossible without Block Convey's PRISM.</strong>
          </div>
        </div>

        <div class="s4-layout">
          <!-- Left: Optical Telemetry Hero -->
          <div class="s4-hero-card">
            <div class="s4-card-header">
              <span>HOW PRISM DECOMPOSES COMPLEX CALL FAILURES</span>
              <span style="color: var(--spectrum-violet);">OPTICAL TELEMETRY</span>
            </div>

            <div class="s4-prism-svg-box">
              <svg viewBox="0 0 540 170" style="width: 100%; height: 100%;">
                <text x="12" y="74" font-family="IBM Plex Mono" font-size="11" font-weight="700" fill="#1E1915">RAW CALL AUDIO</text>
                <line x1="10" y1="90" x2="140" y2="90" stroke="#1E1915" stroke-width="3.5" />

                <polygon points="175,18 225,158 125,158" fill="#FAF8F5" stroke="#6B6357" stroke-width="2.5" />
                <text x="175" y="134" font-family="IBM Plex Mono" font-size="13" font-weight="700" fill="#1E1915" text-anchor="middle">PRISM</text>

                <!-- 5 Rays -->
                <line x1="190" y1="90" x2="270" y2="28" stroke="var(--spectrum-violet)" stroke-width="3" />
                <circle cx="270" cy="28" r="4.5" fill="var(--spectrum-violet)" />
                <text x="282" y="32" font-family="IBM Plex Sans" font-size="13" font-weight="700" fill="var(--spectrum-violet)">1. Multi-Turn Spans (End-to-end tracing)</text>

                <line x1="190" y1="90" x2="270" y2="58" stroke="var(--spectrum-cyan)" stroke-width="3" />
                <circle cx="270" cy="58" r="4.5" fill="var(--spectrum-cyan)" />
                <text x="282" y="62" font-family="IBM Plex Sans" font-size="13" font-weight="700" fill="var(--spectrum-cyan)">2. Root Cause Isolation (Speech vs LLM)</text>

                <line x1="190" y1="90" x2="270" y2="88" stroke="var(--spectrum-jade)" stroke-width="3" />
                <circle cx="270" cy="88" r="4.5" fill="var(--spectrum-jade)" />
                <text x="282" y="92" font-family="IBM Plex Sans" font-size="13" font-weight="700" fill="var(--spectrum-jade)">3. Fleet Benchmarking (~15B vs 70B)</text>

                <line x1="190" y1="90" x2="270" y2="118" stroke="var(--spectrum-amber)" stroke-width="3" />
                <circle cx="270" cy="118" r="4.5" fill="var(--spectrum-amber)" />
                <text x="282" y="122" font-family="IBM Plex Sans" font-size="13" font-weight="700" fill="var(--spectrum-amber)">4. Failure Clustering (Recurring patterns)</text>

                <line x1="190" y1="90" x2="270" y2="148" stroke="var(--spectrum-rose)" stroke-width="3" />
                <circle cx="270" cy="148" r="4.5" fill="var(--spectrum-rose)" />
                <text x="282" y="152" font-family="IBM Plex Sans" font-size="13" font-weight="700" fill="var(--spectrum-rose)">5. AI Remediation (Auto regression tests)</text>
              </svg>
            </div>

            <div class="s4-ray-list">
              <div class="s4-ray-item">
                <div class="s4-ray-dot" style="background: var(--spectrum-violet);"></div>
                <strong>Multi-Turn Spans:</strong>
                <span>Captures audio, prompts, and database state with 0ms added lag.</span>
              </div>
              <div class="s4-ray-item">
                <div class="s4-ray-dot" style="background: var(--spectrum-cyan);"></div>
                <strong>Root Cause Isolation:</strong>
                <span>Pinpoints whether error was Whisper speech transcription or model panic.</span>
              </div>
              <div class="s4-ray-item">
                <div class="s4-ray-dot" style="background: var(--spectrum-jade);"></div>
                <strong>Fleet Benchmarking:</strong>
                <span>Proves guarded ~15B models match expensive 70B models in reliability.</span>
              </div>
            </div>
          </div>

          <!-- Right: 48-Scenario Pre-Registered Audit -->
          <div class="s4-hero-card">
            <div class="s4-card-header">
              <span>HELD-OUT 48-SCENARIO AUDIT BENCHMARK</span>
              <span style="color: var(--jade-primary);">VERIFIED RESULTS</span>
            </div>

            <table class="s4-table">
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
                  <td><span class="s4-table-badge fail">FAILED</span></td>
                  <td><span class="s4-table-badge fail">FAILED</span></td>
                  <td><span class="s4-table-badge pass">100% PASS</span></td>
                </tr>
                <tr>
                  <td>Pressure Bargaining</td>
                  <td><span class="s4-table-badge warn">LEAKED ₹</span></td>
                  <td><span class="s4-table-badge warn">LEAKED ₹</span></td>
                  <td><span class="s4-table-badge pass">ZERO LEAKS</span></td>
                </tr>
                <tr>
                  <td>Spoken Credit Cards</td>
                  <td><span class="s4-table-badge fail">EXPOSED</span></td>
                  <td><span class="s4-table-badge fail">EXPOSED</span></td>
                  <td><span class="s4-table-badge pass">ZERO LEAKS</span></td>
                </tr>
              </tbody>
            </table>

            <div class="s4-trace-box">
              <div>PRISM LIVE TELEMETRY SPAN · CALL #4812</div>
              <div>Turn 02: AI proposes tow truck → <strong>ClaimGuard holds in PENDING [5.0s]</strong></div>
              <div>Turn 02.1: Driver shouts "Cancel!" → <strong>ClaimGuard VETOES dispatch</strong></div>
              <div>Status: <strong>₹0 spent · ₹5,000 saved · 0 PII leaks · 100% VERIFIED</strong></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ====================================================================
           SLIDE 5: SYSTEM WORKFLOW
           ==================================================================== -->
      <section class="slide" id="slide-5">
        <div class="slide-header-block">
          <div class="slide-mandated-prompt">INPUT → AI/RAG/AGENT SYSTEM → PRISM MONITORING & EVALUATION → FAILURE DETECTION → IMPROVEMENT</div>
          <h1 class="slide-headline">How an emergency call flows through the system.</h1>
          <div class="slide-context-note">
            Every 200-millisecond turn of speech follows this closed loop to guarantee safety before words become actions.
          </div>
        </div>

        <div class="s5-grid">
          <!-- Stage 1 -->
          <div class="s5-stage-card">
            <span class="s5-stage-num">STAGE 1</span>
            <div class="s5-stage-title">Input</div>
            <div class="s5-stage-role">Audio Edge & Luhn</div>
            <ul class="s5-stage-points">
              <li>Inbound phone call stream</li>
              <li>Whisper STT converts voice</li>
              <li>Luhn filter masks credit cards</li>
            </ul>
            <div class="s5-stage-preview">
              <span style="color: var(--ink-muted);">OUTPUT:</span>
              <strong>Sanitized text [PAN_MASKED]</strong>
            </div>
          </div>

          <!-- Stage 2 -->
          <div class="s5-stage-card">
            <span class="s5-stage-num">STAGE 2</span>
            <div class="s5-stage-title">AI Cognition</div>
            <div class="s5-stage-role">~15B Model Proposer</div>
            <ul class="s5-stage-points">
              <li>Interprets stranded caller intent</li>
              <li>Queries roadside policy terms</li>
              <li>PROPOSES tool actions only</li>
            </ul>
            <div class="s5-stage-preview">
              <span style="color: var(--ink-muted);">OUTPUT:</span>
              <strong>Proposed dispatch_tow()</strong>
            </div>
          </div>

          <!-- Stage 3 (Highlighted) -->
          <div class="s5-stage-card highlight">
            <span class="s5-stage-num">STAGE 3 · CORE</span>
            <div class="s5-stage-title" style="color: var(--spectrum-violet);">PRISM Monitor</div>
            <div class="s5-stage-role">Block Convey Telemetry</div>
            <ul class="s5-stage-points">
              <li>Captures turn-by-turn spans</li>
              <li>Calculates intent drift score</li>
              <li>Zero added line latency</li>
            </ul>
            <div class="s5-stage-preview">
              <span style="color: var(--spectrum-violet);">TELEMETRY:</span>
              <strong>Trace #4812 · Drift 0.02</strong>
            </div>
          </div>

          <!-- Stage 4 -->
          <div class="s5-stage-card">
            <span class="s5-stage-num">STAGE 4</span>
            <div class="s5-stage-title">Failure Veto</div>
            <div class="s5-stage-role">ClaimGuard Barrier</div>
            <ul class="s5-stage-points">
              <li>Holds dispatch for 5 seconds</li>
              <li>Catches driver interruptions</li>
              <li>Blocks unauthorized waivers</li>
            </ul>
            <div class="s5-stage-preview">
              <span style="color: var(--spectrum-rose);">VERDICT:</span>
              <strong>VETOED (₹5,000 Saved)</strong>
            </div>
          </div>

          <!-- Stage 5 -->
          <div class="s5-stage-card">
            <span class="s5-stage-num">STAGE 5</span>
            <div class="s5-stage-title">Improvement</div>
            <div class="s5-stage-role">Closed-Loop Learning</div>
            <ul class="s5-stage-points">
              <li>Clusters real-world failures</li>
              <li>Generates synthetic test cases</li>
              <li>Re-evaluates audit benchmark</li>
            </ul>
            <div class="s5-stage-preview">
              <span style="color: var(--jade-primary);">SUITE:</span>
              <strong>48/48 Passing (Zero Bugs)</strong>
            </div>
          </div>
        </div>

        <div class="s5-loop-bar">
          <div><strong>CONTINUOUS CLOSED-LOOP:</strong> Every edge case caught by PRISM becomes an automated regression test.</div>
          <div style="color: var(--jade-primary); font-weight: 700;">SELF-HEALING FLEET RELIABILITY</div>
        </div>
      </section>

      <!-- ====================================================================
           SLIDE 6: IMPACT & FUTURE SCOPE
           ==================================================================== -->
      <section class="slide" id="slide-6">
        <div class="slide-header-block">
          <div class="slide-mandated-prompt">Key benefits, real-world impact, scalability, and future enhancements.</div>
          <h1 class="slide-headline">Every regulated call center needs this architecture.</h1>
          <div class="slide-context-note">
            Deterministic guardrails eliminate catastrophic failures today. <strong>PRISM provides the observability to scale across industries tomorrow.</strong>
          </div>
        </div>

        <div class="s6-layout">
          <!-- Left: Multi-Sector Scalability -->
          <div class="s6-card">
            <div class="s2-card-header">
              <span>DEPLOYABLE ACROSS 4 REGULATED CALL-CENTER SECTORS</span>
              <span style="color: var(--jade-primary);">CROSS-INDUSTRY</span>
            </div>

            <div class="s6-stats-row">
              <div class="s6-stat-pill">
                <span class="num">100%</span>
                <span class="lbl">Cancellation Abort</span>
              </div>
              <div class="s6-stat-pill">
                <span class="num">₹0</span>
                <span class="lbl">Unauthorized Payouts</span>
              </div>
              <div class="s6-stat-pill">
                <span class="num">0 ms</span>
                <span class="lbl">Added Audio Lag</span>
              </div>
            </div>

            <div class="s6-sector-grid">
              <div class="s6-sector-box active-core">
                <h5>1. MOTOR INSURANCE <span style="font-size: 10px; color: var(--jade-primary);">LIVE</span></h5>
                <p>Highway NH-48 roadside assistance. Cancels mistaken tow dispatches on driver interruptions.</p>
              </div>

              <div class="s6-sector-box">
                <h5>2. BANKING & LENDING <span style="font-size: 10px; color: var(--ink-muted);">RBI</span></h5>
                <p>Support hotlines. Blocks hallucinated credit limit waivers, fee concessions, and card leaks.</p>
              </div>

              <div class="s6-sector-box">
                <h5>3. TELECOM BILLING <span style="font-size: 10px; color: var(--ink-muted);">TRAI</span></h5>
                <p>High-volume dispute lines. Locks refund caps and contractual plan upgrades into SQL rules.</p>
              </div>

              <div class="s6-sector-box">
                <h5>4. HEALTHCARE TRIAGE <span style="font-size: 10px; color: var(--ink-muted);">DPDP</span></h5>
                <p>Clinical scheduling. Shields sensitive patient medical history and prescription records.</p>
              </div>
            </div>

            <div style="background: var(--surface-card); border-left: 3.5px solid var(--jade-primary); padding: 10px 14px; border-radius: 6px; font-size: 13.5px; color: var(--ink-secondary);">
              <strong>THE GOLDEN RULE:</strong> Use fast ~15B models for natural conversation. Use <strong>deterministic code</strong> for financial and legal safety. Use <strong>PRISM</strong> to observe and prove reliability.
            </div>
          </div>

          <!-- Right: Concrete 3-Phase Roadmap -->
          <div class="s6-card">
            <div class="s2-card-header">
              <span>3-PHASE PRODUCTION ROADMAP</span>
              <span style="color: var(--ink-muted);">TIMELINE</span>
            </div>

            <div class="s6-roadmap-list">
              <div class="s6-phase-box">
                <span class="s6-phase-badge today">TODAY · COMPLETED</span>
                <div class="s6-phase-content">
                  <h5>Edge Engine + PRISM Spine</h5>
                  <p>Whisper STT, fast ~15B model proposer, SQLite triggers, and full PRISM multi-turn tracing passing 48/48 audit scenarios.</p>
                </div>
              </div>

              <div class="s6-phase-box">
                <span class="s6-phase-badge next">NEXT · Q2 2026</span>
                <div class="s6-phase-content">
                  <h5>Telephony & SIP Trunking</h5>
                  <p>Direct Exotel and Twilio SIP gateway integration with streaming jitter buffers maintaining under 200ms latency.</p>
                </div>
              </div>

              <div class="s6-phase-box">
                <span class="s6-phase-badge scale">SCALE · H2 2026</span>
                <div class="s6-phase-content">
                  <h5>Indian Regional Speech</h5>
                  <p>IndicWhisper STT for Hindi, Tamil, Telugu, and Kannada with PRISM active inline guardrails across India.</p>
                </div>
              </div>
            </div>

            <div class="s6-closing-quote">
              Can be interrupted. Can't be bullied. Won't leak.<br>
              <strong>Built to be diagnosed — proven by PRISM.</strong>
            </div>
          </div>
        </div>
      </section>

    </main>

    <!-- Persistent Bottom Controls Bar -->
    <footer class="stage-footer">
      <div class="footer-left-controls">
        <button class="btn-nav" id="btn-prev" onclick="window.deck.prev()">‹ Prev</button>
        <button class="btn-nav" id="btn-next" onclick="window.deck.next()">Next ›</button>
        <button class="btn-autoplay" id="btn-auto" onclick="window.deck.toggleAutoPlay()">Auto-Play (15s)</button>
      </div>

      <div class="footer-dots" id="footer-dots-container">
        <div class="dot-step active" onclick="window.deck.goTo(0)">1</div>
        <div class="dot-step" onclick="window.deck.goTo(1)">2</div>
        <div class="dot-step" onclick="window.deck.goTo(2)">3</div>
        <div class="dot-step" onclick="window.deck.goTo(3)">4</div>
        <div class="dot-step" onclick="window.deck.goTo(4)">5</div>
        <div class="dot-step" onclick="window.deck.goTo(5)">6</div>
      </div>

      <div class="footer-right-status">
        <span>PRISM BY BLOCK CONVEY · EVALUATION SUITE</span>
      </div>
    </footer>

  </div>

  <!-- Deck Interactive Controller -->
  <script>
    class DeckController {
      constructor() {
        this.slides = document.querySelectorAll('.slide');
        this.dots = document.querySelectorAll('.dot-step');
        this.counterBadge = document.getElementById('slide-counter-badge');
        this.subtopicLabel = document.getElementById('slide-subtopic');
        this.autoPlayBtn = document.getElementById('btn-auto');
        
        this.currentIndex = 0;
        this.autoPlayInterval = null;
        this.totalSlides = this.slides.length;

        this.subtopics = [
          "Problem Statement",
          "Existing Challenges",
          "Proposed Solution",
          "PRISM Usage",
          "System Workflow",
          "Impact & Future Scope"
        ];

        this.init();
      }

      init() {
        // Keyboard navigation
        window.addEventListener('keydown', (e) => {
          if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
            this.next();
          } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
            this.prev();
          } else if (e.key >= '1' && e.key <= '6') {
            this.goTo(parseInt(e.key) - 1);
          }
        });

        this.updateUI();
      }

      goTo(index) {
        if (index < 0 || index >= this.totalSlides) return;
        this.slides[this.currentIndex].classList.remove('active');
        this.dots[this.currentIndex].classList.remove('active');

        this.currentIndex = index;
        this.slides[this.currentIndex].classList.add('active');
        this.dots[this.currentIndex].classList.add('active');

        this.updateUI();
      }

      next() {
        if (this.currentIndex < this.totalSlides - 1) {
          this.goTo(this.currentIndex + 1);
        } else {
          this.goTo(0);
        }
      }

      prev() {
        if (this.currentIndex > 0) {
          this.goTo(this.currentIndex - 1);
        } else {
          this.goTo(this.totalSlides - 1);
        }
      }

      updateUI() {
        this.counterBadge.textContent = `0${this.currentIndex + 1} / 0${this.totalSlides}`;
        this.subtopicLabel.textContent = this.subtopics[this.currentIndex];

        if (window.renderMathInElement) {
          window.renderMathInElement(this.slides[this.currentIndex]);
        }
      }

      toggleAutoPlay() {
        if (this.autoPlayInterval) {
          clearInterval(this.autoPlayInterval);
          this.autoPlayInterval = null;
          this.autoPlayBtn.classList.remove('active');
          this.autoPlayBtn.textContent = "Auto-Play (15s)";
        } else {
          this.autoPlayBtn.classList.add('active');
          this.autoPlayBtn.textContent = "Auto-Playing... (15s)";
          this.autoPlayInterval = setInterval(() => {
            this.next();
          }, 15000);
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

# Destinations
online_path = "/home/aliz/Documents/Codes/forgeAI-hackathon/presentation/claimguard-pitch.html"
offline_path = "/home/aliz/Documents/Codes/forgeAI-hackathon/presentation/claimguard-pitch-offline.html"
builder_path = "/home/aliz/Documents/Codes/forgeAI-hackathon/build_pitch.py"

with open(online_path, "w", encoding="utf-8") as f:
    f.write(html_content)

with open(offline_path, "w", encoding="utf-8") as f:
    f.write(html_content)

with open(builder_path, "w", encoding="utf-8") as f:
    f.write(f'''#!/usr/bin/env python3
# ClaimGuard x PRISM Pitch Deck Builder
# Autonomous Judge Pitch Deck with ~15B Class Model & Low Density Editorial Simplicity

html_content = r\'\'\'{html_content}\'\'\'

with open("{online_path}", "w", encoding="utf-8") as f:
    f.write(html_content)

with open("{offline_path}", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Successfully rebuilt presentation/claimguard-pitch.html and presentation/claimguard-pitch-offline.html!")
''')

print("Successfully written simplified, low-density slide decks to disk!")
