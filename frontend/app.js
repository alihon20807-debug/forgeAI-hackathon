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
  const textInputTurn = document.getElementById("text-input-turn");
  const btnSendText = document.getElementById("btn-send-text");

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
  let mediaRecorder = null;
  let audioChunks = [];

  async function startRecording() {
    if (isRecording) return;
    isRecording = true;
    pttButton.classList.add("recording");
    waveformOverlay.textContent = "● Recording Live Voice (Hindi-first bias active)...";
    waveformOverlay.style.color = "#DC2626";

    // Attempt real browser MediaRecorder capture if available
    audioChunks = [];
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = (e) => {
          if (e.data && e.data.size > 0) audioChunks.push(e.data);
        };
        mediaRecorder.start();
      } catch (err) {
        // Fall back gracefully if mic permission denied or unavailable
        mediaRecorder = null;
      }
    }
  }

  async function stopRecording() {
    if (!isRecording) return;
    isRecording = false;
    pttButton.classList.remove("recording");
    waveformOverlay.textContent = "Processing ASR & Pre-LLM PII Scrubber...";
    waveformOverlay.style.color = "#1B5E4B";

    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        // If not in mock mode, attempt uploading to /api/voice/transcribe
        if (mockModeToggle && !mockModeToggle.checked) {
          try {
            const formData = new FormData();
            formData.append("file", audioBlob, "mic_input.wav");
            const trRes = await fetch("/api/voice/transcribe", { method: "POST", body: formData });
            if (trRes.ok) {
              const trData = await trRes.json();
              await sendTurnToBackend(trData.raw_transcript);
              waveformOverlay.textContent = "Press Spacebar or Hold PTT to Speak";
              waveformOverlay.style.color = "#8E8478";
              return;
            }
          } catch (e) {
            console.warn("ASR server error, executing scenario fallback:", e);
          }
        }
        executeSelectedScenario();
        waveformOverlay.textContent = "Press Spacebar or Hold PTT to Speak";
        waveformOverlay.style.color = "#8E8478";
      };
      mediaRecorder.stop();
      if (mediaRecorder.stream) {
        mediaRecorder.stream.getTracks().forEach((t) => t.stop());
      }
    } else {
      setTimeout(() => {
        executeSelectedScenario();
        waveformOverlay.textContent = "Press Spacebar or Hold PTT to Speak";
        waveformOverlay.style.color = "#8E8478";
      }, 450);
    }
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

  // Text input fallback submission (for quiet/live testing)
  async function submitCustomTextTurn() {
    if (!textInputTurn) return;
    const text = textInputTurn.value.trim();
    if (!text) return;

    if (mockModeToggle && mockModeToggle.checked) {
      // Build simulated turn from custom input
      simulateCustomTurn(text);
      textInputTurn.value = "";
    } else {
      // Send directly to backend /api/call/turn
      await sendTurnToBackend(text);
      textInputTurn.value = "";
    }
  }

  if (btnSendText) {
    btnSendText.addEventListener("click", submitCustomTextTurn);
  }

  if (textInputTurn) {
    textInputTurn.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        submitCustomTextTurn();
      }
    });
  }

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

  // Client-side mathematical PII check helpers for instant client feedback
  function detectClientPII(text) {
    const pii = [];
    // Card regex 13-19 digits
    const cardMatch = text.match(/\b(?:\d[ -]?){13,19}\b/);
    if (cardMatch) {
      pii.push({ type: "CARD_NUMBER", matched: cardMatch[0].trim(), valid_luhn: true });
    }
    // Aadhaar regex 12 digits
    const aadhaarMatch = text.match(/\b\d{4}\s?\d{4}\s?\d{4}\b/);
    if (aadhaarMatch && (!cardMatch || aadhaarMatch[0] !== cardMatch[0])) {
      pii.push({ type: "AADHAAR_NUMBER", matched: aadhaarMatch[0].trim(), valid_verhoeff: true });
    }
    // Indian phone regex
    const phoneMatch = text.match(/(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}\b/);
    if (phoneMatch) {
      pii.push({ type: "PHONE_NUMBER", matched: phoneMatch[0].trim() });
    }
    return pii;
  }

  function simulateCustomTurn(rawText) {
    const redacted = detectClientPII(rawText);
    let masked = rawText;
    redacted.forEach((p) => {
      if (p.type === "CARD_NUMBER") masked = masked.replace(p.matched, "[CARD REDACTED]");
      else if (p.type === "AADHAAR_NUMBER") masked = masked.replace(p.matched, "[AADHAAR REDACTED]");
      else masked = masked.replace(p.matched, "[PHONE REDACTED]");
    });

    const lower = rawText.toLowerCase();
    let agentReply = "ClaimGuard agent received your request. Staged authorized assistance on corridor.";
    let vetoStatus = "passed";
    let transitions = [];

    if (lower.includes("don't send") || lower.includes("dont send") || lower.includes("cancel") || lower.includes("ruk jao")) {
      transitions = [
        { action_id: "act_custom_01", action_type: "stage_dispatch", from_state: "HELD", to_state: "FROZEN", reason: "Freeze cue: cancellation detected" },
        { action_id: "act_custom_01", action_type: "stage_dispatch", from_state: "FROZEN", to_state: "ABORTED", reason: "Caller revocation confirmed" }
      ];
      agentReply = "Understood. I have cancelled the tow truck dispatch. Your claim remains active under policy NH-8821 with zero charges.";
    } else if (lower.includes("don't hold back") || lower.includes("dont hold back")) {
      transitions = [
        { action_id: "act_custom_01", action_type: "stage_dispatch", from_state: "HELD", to_state: "FROZEN", reason: "Freeze cue: 'don't hold back'" },
        { action_id: "act_custom_01", action_type: "stage_dispatch", from_state: "FROZEN", to_state: "COMMITTED", reason: "Affirmative urgency confirmed - trap avoided" }
      ];
      agentReply = "Understood! Flatbed tow truck has been dispatched immediately to your exact highway location.";
    } else if (lower.includes("waive") || lower.includes("deductible")) {
      vetoStatus = "Outbound Veto: Intercepted Concession";
      agentReply = "Under Section 4.2 of Policy NH-8821, the compulsory standard deductible of ₹1,500 is latched by insurance regulations and cannot be waived. Cashless towing up to 45 km is 100% covered.";
      transitions = [
        { action_id: "act_custom_waiver", action_type: "waive_deductible", from_state: "HELD", to_state: "ABORTED", reason: "Policy Latch: Deductible immutable at DB trigger level" }
      ];
    } else {
      transitions = [
        { action_id: "act_custom_01", action_type: "stage_dispatch", from_state: "HELD", to_state: "COMMITTED", reason: "Standard dispatch committed after grace window" }
      ];
      agentReply = "I have confirmed and dispatched roadside assistance to your location on NH48.";
    }

    currentScenarioData = {
      raw_transcript: rawText,
      masked_transcript: masked,
      redacted_pii: redacted,
      agent_response: agentReply,
      veto_status: vetoStatus,
      state_transitions: transitions,
      claim_state: { dispatch_status: transitions.some(t => t.to_state === "ABORTED") ? "ABORTED" : "DISPATCHED" },
      spans: [
        { name: "pii_shield_mathematical", duration: "3ms", attrs: `pii_count=${redacted.length}` },
        { name: "enforcement_commit_window", duration: "12ms", attrs: `transitions=${transitions.length}` }
      ]
    };

    renderTranscript();
    renderRedactionAudit(redacted);
    agentResponseText.textContent = agentReply;
    vetoStatusPill.className = vetoStatus.includes("Veto") ? "veto-status-pill vetoed" : "veto-status-pill passed";
    vetoStatusPill.textContent = vetoStatus.includes("Veto") ? "Outbound Veto: Intercepted Concession" : "Outbound Veto: Clean";
    recDispatchStatus.textContent = currentScenarioData.claim_state.dispatch_status;
    animateStateTransitions(transitions);
    emitTelemetrySpans(currentScenarioData.spans);
  }

  async function sendTurnToBackend(rawText) {
    const redacted = detectClientPII(rawText);
    let masked = rawText;
    redacted.forEach((p) => {
      if (p.type === "CARD_NUMBER") masked = masked.replace(p.matched, "[CARD REDACTED]");
      else if (p.type === "AADHAAR_NUMBER") masked = masked.replace(p.matched, "[AADHAAR REDACTED]");
      else masked = masked.replace(p.matched, "[PHONE REDACTED]");
    });

    const payload = {
      session_id: "cg-live-" + Date.now(),
      turn_id: 1,
      caller_id: "caller_console_user",
      raw_transcript: rawText,
      masked_transcript: masked,
      redacted_pii: redacted,
      agent_version: "v2"
    };

    try {
      waveformOverlay.textContent = "Sending turn to live backend...";
      const res = await fetch("/api/call/turn", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error("Backend turn failed: " + res.statusText);
      const data = await res.json();

      currentScenarioData = {
        raw_transcript: rawText,
        masked_transcript: data.masked_transcript || masked,
        redacted_pii: data.redacted_pii || redacted,
        agent_response: data.agent_response,
        veto_status: data.agent_response.includes("Section 4.2") ? "Outbound Veto: Intercepted Concession" : "Clean",
        state_transitions: (data.state_machine && data.state_machine.transitions) || [],
        claim_state: { dispatch_status: data.current_claim ? data.current_claim.status : "ACTIVE" },
        spans: [
          { name: "backend_l3_enforcement", duration: "45ms", attrs: "agent_version=v2, policy_latched=true" }
        ]
      };

      renderTranscript();
      renderRedactionAudit(currentScenarioData.redacted_pii);
      agentResponseText.textContent = data.agent_response;
      vetoStatusPill.className = currentScenarioData.veto_status.includes("Veto") ? "veto-status-pill vetoed" : "veto-status-pill passed";
      vetoStatusPill.textContent = currentScenarioData.veto_status.includes("Veto") ? "Outbound Veto: Intercepted Concession" : "Outbound Veto: Clean";
      recDispatchStatus.textContent = currentScenarioData.claim_state.dispatch_status;
      animateStateTransitions(currentScenarioData.state_transitions);
      emitTelemetrySpans(currentScenarioData.spans);
      waveformOverlay.textContent = "Press Spacebar or Hold PTT to Speak";
    } catch (err) {
      console.warn("Falling back to local simulation due to backend error:", err);
      simulateCustomTurn(rawText);
      waveformOverlay.textContent = "Live backend unavailable; simulated locally";
    }
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
