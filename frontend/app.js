/**
 * ClaimGuard × PRISM — Live Supervisor Console (L6)
 * Push-to-Talk, Waveform Visualizer, Dynamic PII Badging, and Commit Window Transitions.
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const waveformCanvas = document.getElementById("waveform-canvas");
  const waveformCtx = waveformCanvas ? waveformCanvas.getContext("2d") : null;
  const waveformOverlay = document.getElementById("waveform-overlay");
  const pttButton = document.getElementById("ptt-button");
  const scenarioSelect = document.getElementById("scenario-select");
  const simulateBtn = document.getElementById("simulate-turn-btn");
  const transcriptDisplay = document.getElementById("transcript-display");
  const redactionAuditStrip = document.getElementById("redaction-audit-strip");
  const agentResponseText = document.getElementById("agent-response-text");
  const vetoStatusPill = document.getElementById("veto-status-pill");
  const mockModeToggle = document.getElementById("mock-mode-toggle");
  const btnShowMasked = document.getElementById("btn-show-masked");
  const btnShowDiff = document.getElementById("btn-show-diff");

  // State Column Lists
  const listHeld = document.getElementById("list-held");
  const listFrozen = document.getElementById("list-frozen");
  const listCommitted = document.getElementById("list-committed");
  const listAborted = document.getElementById("list-aborted");

  // Counters
  const countHeld = document.getElementById("count-held");
  const countFrozen = document.getElementById("count-frozen");
  const countCommitted = document.getElementById("count-committed");
  const countAborted = document.getElementById("count-aborted");

  // System of Record
  const recDispatchStatus = document.getElementById("rec-dispatch-status");
  const telemetryStream = document.getElementById("telemetry-stream");
  const spanCountBadge = document.getElementById("span-count-badge");

  let isRecording = false;
  let totalSpansLogged = 0;
  let currentScenarioData = null;
  let currentViewMode = "masked"; // 'masked' or 'diff'

  // =========================================================================
  // 1. Ambient Waveform Visualizer
  // =========================================================================
  let wavePhase = 0;
  function drawWaveform() {
    if (!waveformCanvas || !waveformCtx) return;

    const width = waveformCanvas.width;
    const height = waveformCanvas.height;
    waveformCtx.clearRect(0, 0, width, height);

    const centerY = height / 2;
    const bars = 48;
    const barWidth = width / bars - 2;

    waveformCtx.fillStyle = isRecording ? "#DC2626" : "#8E8478";

    for (let i = 0; i < bars; i++) {
      const x = i * (barWidth + 2);
      let amplitude = 4;

      if (isRecording) {
        // High energetic speech wave
        amplitude = Math.sin(i * 0.3 + wavePhase) * 22 + Math.cos(i * 0.7 - wavePhase) * 14 + 12;
        amplitude = Math.max(6, Math.min(amplitude, height - 10));
      } else {
        // Calm ambient line
        amplitude = Math.sin(i * 0.15 + wavePhase * 0.5) * 4 + 4;
      }

      const barHeight = Math.abs(amplitude);
      const y = centerY - barHeight / 2;

      // Draw rounded bar
      waveformCtx.beginPath();
      waveformCtx.roundRect(x, y, barWidth, barHeight, 2);
      waveformCtx.fill();
    }

    wavePhase += isRecording ? 0.25 : 0.04;
    requestAnimationFrame(drawWaveform);
  }
  drawWaveform();

  // =========================================================================
  // 2. Push-to-Talk (PTT) Controllers
  // =========================================================================
  function startRecording() {
    if (isRecording) return;
    isRecording = true;
    pttButton.classList.add("recording");
    waveformOverlay.textContent = "● Recording Live Voice (Hindi-first bias active)...";
    waveformOverlay.style.color = "#DC2626";
  }

  function stopRecording() {
    if (!isRecording) return;
    isRecording = false;
    pttButton.classList.remove("recording");
    waveformOverlay.textContent = "Processing ASR & Pre-LLM PII Scrubber...";
    waveformOverlay.style.color = "#1B5E4B";

    setTimeout(() => {
      executeSelectedScenario();
      waveformOverlay.textContent = "Press Spacebar or Hold PTT to Speak";
      waveformOverlay.style.color = "#8E8478";
    }, 450);
  }

  // Mouse / Touch handlers for PTT button
  pttButton.addEventListener("mousedown", startRecording);
  pttButton.addEventListener("mouseup", stopRecording);
  pttButton.addEventListener("mouseleave", () => {
    if (isRecording) stopRecording();
  });

  pttButton.addEventListener("touchstart", (e) => {
    e.preventDefault();
    startRecording();
  });
  pttButton.addEventListener("touchend", (e) => {
    e.preventDefault();
    stopRecording();
  });

  // Spacebar PTT shortcut
  window.addEventListener("keydown", (e) => {
    if (e.code === "Space" && !e.repeat && document.activeElement.tagName !== "INPUT") {
      e.preventDefault();
      startRecording();
    }
  });

  window.addEventListener("keyup", (e) => {
    if (e.code === "Space" && document.activeElement.tagName !== "INPUT") {
      e.preventDefault();
      stopRecording();
    }
  });

  simulateBtn.addEventListener("click", () => {
    executeSelectedScenario();
  });

  // View Mode Toggles (Masked vs PII Diff)
  btnShowMasked.addEventListener("click", () => {
    currentViewMode = "masked";
    btnShowMasked.classList.add("active");
    btnShowDiff.classList.remove("active");
    renderTranscript();
  });

  btnShowDiff.addEventListener("click", () => {
    currentViewMode = "diff";
    btnShowDiff.classList.add("active");
    btnShowMasked.classList.remove("active");
    renderTranscript();
  });

  // =========================================================================
  // 3. Scenario Execution & State Machine Orchestration
  // =========================================================================
  function executeSelectedScenario() {
    const scenarioKey = scenarioSelect.value;
    const scenario = REPLAY_SCENARIOS[scenarioKey];
    if (!scenario) return;

    currentScenarioData = scenario;
    renderTranscript();
    renderRedactionAudit(scenario.redacted_pii);

    // Agent Outbound Response
    agentResponseText.textContent = scenario.agent_response;
    if (scenario.veto_status.includes("Veto")) {
      vetoStatusPill.className = "veto-status-pill vetoed";
      vetoStatusPill.textContent = "Outbound Veto: Intercepted Concession";
    } else {
      vetoStatusPill.className = "veto-status-pill passed";
      vetoStatusPill.textContent = "Outbound Veto: Clean";
    }

    // Update System of Record
    recDispatchStatus.textContent = scenario.claim_state.dispatch_status;

    // Run Animated State Machine Transitions
    animateStateTransitions(scenario.state_transitions);

    // Emit Telemetry Spans
    emitTelemetrySpans(scenario.spans);
  }

  function renderTranscript() {
    if (!currentScenarioData) return;

    if (currentViewMode === "masked") {
      let formatted = escapeHtml(currentScenarioData.raw_transcript);

      // Replace with styled badges
      currentScenarioData.redacted_pii.forEach((item) => {
        const token = item.type === "CARD_NUMBER" 
          ? `<span class="pii-badge card">🔒 [CARD REDACTED · Luhn Pass]</span>`
          : item.type === "AADHAAR_NUMBER"
          ? `<span class="pii-badge aadhaar">🔒 [AADHAAR REDACTED · Verhoeff Pass]</span>`
          : `<span class="pii-badge phone">🔒 [PHONE REDACTED]</span>`;

        formatted = formatted.replace(item.matched, token);
      });

      transcriptDisplay.innerHTML = formatted;
    } else {
      // Diff View highlighting stripped PII in red
      let formatted = escapeHtml(currentScenarioData.raw_transcript);
      currentScenarioData.redacted_pii.forEach((item) => {
        const diffHighlight = `<span style="background: #FEE2E2; border: 1px dashed #DC2626; color: #DC2626; text-decoration: line-through; padding: 1px 4px; border-radius: 2px;">${escapeHtml(item.matched)}</span>`;
        formatted = formatted.replace(item.matched, diffHighlight);
      });
      transcriptDisplay.innerHTML = formatted;
    }
  }

  function renderRedactionAudit(redactedList) {
    redactionAuditStrip.innerHTML = "";
    if (!redactedList || redactedList.length === 0) {
      redactionAuditStrip.innerHTML = `<span class="audit-badge idle">No sensitive identifiers in active buffer</span>`;
      return;
    }

    redactedList.forEach((item) => {
      const badge = document.createElement("span");
      badge.className = "audit-badge verified";
      if (item.type === "CARD_NUMBER") {
        badge.innerHTML = `✓ Card Redacted: Luhn Checksum <strong>VALID</strong> (${escapeHtml(item.matched)})`;
      } else if (item.type === "AADHAAR_NUMBER") {
        badge.innerHTML = `✓ Aadhaar Redacted: Verhoeff D5 Checksum <strong>VALID</strong> (${escapeHtml(item.matched)})`;
      } else {
        badge.innerHTML = `✓ Phone Redacted: 10-Digit Mobile Masked (${escapeHtml(item.matched)})`;
      }
      redactionAuditStrip.appendChild(badge);
    });
  }

  // =========================================================================
  // 4. Commit Window Kanban Animation
  // =========================================================================
  function clearAllColumns() {
    listHeld.innerHTML = "";
    listFrozen.innerHTML = "";
    listCommitted.innerHTML = "";
    listAborted.innerHTML = "";
    updateColumnCounts();
  }

  function updateColumnCounts() {
    countHeld.textContent = listHeld.children.length;
    countFrozen.textContent = listFrozen.children.length;
    countCommitted.textContent = listCommitted.children.length;
    countAborted.textContent = listAborted.children.length;
  }

  function createActionCard(actionId, actionType, reason, timestamp) {
    const card = document.createElement("div");
    card.className = "action-card";
    card.id = `card-${actionId}`;
    card.innerHTML = `
      <div class="action-card-header">
        <span class="action-type">${actionType}</span>
        <span class="action-time">${timestamp || new Date().toLocaleTimeString()}</span>
      </div>
      <div class="action-reason">${reason}</div>
      <div class="action-meta-badge">${actionId}</div>
    `;
    return card;
  }

  function animateStateTransitions(transitions) {
    clearAllColumns();
    if (!transitions || transitions.length === 0) return;

    transitions.forEach((trans, index) => {
      const delay = index * 400; // Realistic perception delay
      setTimeout(() => {
        // Remove existing instance of this card from previous columns
        const existingCard = document.getElementById(`card-${trans.action_id}`);
        if (existingCard) {
          existingCard.remove();
        }

        const newCard = createActionCard(
          trans.action_id,
          trans.action_type,
          trans.reason,
          trans.timestamp
        );

        if (trans.to_state === "HELD") {
          listHeld.appendChild(newCard);
        } else if (trans.to_state === "FROZEN") {
          listFrozen.appendChild(newCard);
        } else if (trans.to_state === "COMMITTED") {
          listCommitted.appendChild(newCard);
        } else if (trans.to_state === "ABORTED") {
          listAborted.appendChild(newCard);
        }

        updateColumnCounts();
      }, delay);
    });
  }

  // =========================================================================
  // 5. PRISM Telemetry Span Stream
  // =========================================================================
  function emitTelemetrySpans(spans) {
    if (!spans || spans.length === 0) return;

    if (telemetryStream.querySelector(".stream-placeholder")) {
      telemetryStream.innerHTML = "";
    }

    spans.forEach((s) => {
      totalSpansLogged++;
      spanCountBadge.textContent = `${totalSpansLogged} Spans`;

      const entry = document.createElement("div");
      entry.className = "span-log-entry";
      entry.innerHTML = `
        <div class="span-log-top">
          <span class="span-log-name">${s.name}</span>
          <span class="span-duration">${s.duration}</span>
        </div>
        <div class="span-log-attrs">${s.attrs}</div>
      `;

      telemetryStream.prepend(entry);
    });
  }

  function escapeHtml(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Trigger initial default scenario on load
  setTimeout(() => {
    executeSelectedScenario();
  }, 200);
});
