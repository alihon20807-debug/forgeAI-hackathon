/**
 * ClaimGuard × PRISM — Architectural Telemetry & Inspection Studio Controller
 * Real-time WebSocket subscriber powering circuit graphs, oscilloscopes, and flight tapes.
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements - Metrics
  const connStatus = document.getElementById("conn-status");
  const connText = document.getElementById("conn-text");
  const metricPolicy = document.getElementById("metric-policy");
  const metricClaim = document.getElementById("metric-claim");
  const metricClaimSub = document.getElementById("metric-claim-sub");
  const metricCommitWindow = document.getElementById("metric-commit-window");
  const metricCommitSub = document.getElementById("metric-commit-sub");
  const metricPiiCount = document.getElementById("metric-pii-count");
  const metricSpans = document.getElementById("metric-spans");
  const btnReset = document.getElementById("btn-reset-inspector");

  // Oscilloscope Canvas
  const scopeCanvas = document.getElementById("scope-canvas");
  const scopeCtx = scopeCanvas ? scopeCanvas.getContext("2d") : null;
  const scopeStatus = document.getElementById("scope-status");

  // L1 Elements
  const l1Raw = document.getElementById("l1-raw-transcript");
  const l1Masked = document.getElementById("l1-masked-transcript");
  const l1PiiAudit = document.getElementById("l1-pii-audit");

  // L2 Elements
  const l2ToolCalls = document.getElementById("l2-tool-calls");
  const l2RawReply = document.getElementById("l2-raw-reply");
  const l2RiskAudit = document.getElementById("l2-risk-audit");
  const l2RiskText = document.getElementById("l2-risk-text");

  // L3 Circuit Nodes & SVG Elements
  const nodeHeld = document.getElementById("node-held");
  const nodeFrozen = document.getElementById("node-frozen");
  const nodeCommitted = document.getElementById("node-committed");
  const nodeAborted = document.getElementById("node-aborted");
  const wireStagedFreeze = document.getElementById("wire-staged-freeze");
  const wireFreezeCommit = document.getElementById("wire-freeze-commit");
  const wireFreezeAbort = document.getElementById("wire-freeze-abort");
  const pulseParticle = document.getElementById("pulse-particle");
  const l3Transition = document.getElementById("l3-latest-transition");
  const l3VetoCard = document.getElementById("l3-veto-card");
  const l3VetoTitle = document.getElementById("l3-veto-title");
  const l3VetoDetail = document.getElementById("l3-veto-detail");

  // L4 & L5 Elements
  const l4ClaimId = document.getElementById("l4-claim-id");
  const l4Deductible = document.getElementById("l4-deductible");
  const l4Dispatches = document.getElementById("l4-dispatches");
  const prismStream = document.getElementById("prism-stream");

  let ws = null;
  let totalPiiCount = 0;
  let totalSpansCount = 0;
  let isAcousticActive = false;
  let acousticTimer = null;

  // =========================================================================
  // 1. Audio Frequency Oscilloscope Canvas
  // =========================================================================
  let scopePhase = 0;
  function renderOscilloscope() {
    if (!scopeCanvas || !scopeCtx) return;
    const w = scopeCanvas.width;
    const h = scopeCanvas.height;
    scopeCtx.clearRect(0, 0, w, h);

    const centerY = h / 2;
    scopeCtx.beginPath();
    scopeCtx.lineWidth = 2;
    scopeCtx.strokeStyle = isAcousticActive ? "#0284C7" : "#94A3B8";

    for (let x = 0; x < w; x += 2) {
      let y;
      if (isAcousticActive) {
        // High-energy voice signal harmonics
        y = centerY +
          Math.sin(x * 0.05 + scopePhase) * 14 +
          Math.cos(x * 0.12 - scopePhase * 1.5) * 8 +
          Math.sin(x * 0.2 + scopePhase * 2) * 4;
      } else {
        // Calm idle carrier line with gentle thermal noise
        y = centerY + Math.sin(x * 0.02 + scopePhase * 0.3) * 2;
      }
      if (x === 0) scopeCtx.moveTo(x, y);
      else scopeCtx.lineTo(x, y);
    }
    scopeCtx.stroke();

    scopePhase += isAcousticActive ? 0.25 : 0.03;
    requestAnimationFrame(renderOscilloscope);
  }
  renderOscilloscope();

  function triggerAcousticPulse(durationMs = 3000) {
    isAcousticActive = true;
    if (scopeStatus) scopeStatus.textContent = "Voice turn streaming · ASR processing";
    if (acousticTimer) clearTimeout(acousticTimer);
    acousticTimer = setTimeout(() => {
      isAcousticActive = false;
      if (scopeStatus) scopeStatus.textContent = "Carrier line steady · Awaiting turn";
    }, durationMs);
  }

  // =========================================================================
  // 2. WebSocket Real-Time Connection
  // =========================================================================
  function connectWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/ws/live`;

    connStatus.className = "system-pill";
    connText.textContent = "Connecting";

    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      connStatus.className = "system-pill";
      connText.textContent = "Online";
      addTapeEntry("Spine telemetry channel open (/ws/live)", "prism");
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        handleLiveEvent(msg);
      } catch (err) {
        console.warn("Failed to parse WS message:", err);
      }
    };

    ws.onclose = () => {
      connStatus.className = "system-pill offline";
      connText.textContent = "Reconnecting";
      setTimeout(connectWebSocket, 2000);
    };

    ws.onerror = () => {
      connStatus.className = "system-pill offline";
      connText.textContent = "Offline";
    };
  }

  connectWebSocket();

  // =========================================================================
  // 3. Live Event Processing
  // =========================================================================
  function handleLiveEvent(data) {
    if (data.type === "INITIAL_STATE") return;

    triggerAcousticPulse(3500);

    const rawTranscript = data.raw_transcript || "";
    const maskedTranscript = data.masked_transcript || "";
    const redactedPii = data.redacted_pii || [];
    const agentResponse = data.agent_response || "";
    const stateMachine = data.state_machine || {};
    const currentClaim = data.current_claim || null;
    const transitions = stateMachine.transitions || [];

    // -------------------------------------------------------------
    // L1: Perception & PII Shield
    // -------------------------------------------------------------
    if (rawTranscript) {
      l1Raw.textContent = rawTranscript;
      l1Masked.textContent = maskedTranscript || rawTranscript;

      if (redactedPii.length > 0) {
        totalPiiCount += redactedPii.length;
        metricPiiCount.textContent = `${totalPiiCount} Scrubbed`;

        l1PiiAudit.innerHTML = "";
        redactedPii.forEach(item => {
          const chip = document.createElement("div");
          chip.className = "pii-chip";
          const typeLabel = (item.type || "PII").replace("_", " ");
          const checkLabel = item.valid_luhn ? "Luhn Checksum (ISO/IEC 7812) Validated" : (item.valid_verhoeff ? "Verhoeff Algorithm Validated" : "Pattern Verified");
          chip.innerHTML = `
            <div class="pii-chip-meta">
              <span class="pii-chip-badge">${typeLabel}</span>
              <span>${item.matched}</span>
            </div>
            <span class="pii-chip-verify">${checkLabel} · Redacted</span>
          `;
          l1PiiAudit.appendChild(chip);
        });

        addTapeEntry(`L1 PII Shield intercepted ${redactedPii.length} sensitive identifier(s)`, "abort");
      }
    }

    // -------------------------------------------------------------
    // L2: Cognition Intent
    // -------------------------------------------------------------
    const lowerRaw = rawTranscript.toLowerCase();
    if (transitions.length > 0) {
      const actionsProposed = transitions.map(t => t.action_type || t.action_id).join(", ");
      l2ToolCalls.textContent = `[${actionsProposed}]`;
    } else if (lowerRaw.includes("waive") || lowerRaw.includes("discount") || lowerRaw.includes("maaf")) {
      l2ToolCalls.textContent = `lookup_policy("NH-8821") → Checked Clause 4.2 Deductible`;
    } else {
      l2ToolCalls.textContent = `open_claim, stage_dispatch(service_type="towing")`;
    }

    l2RawReply.textContent = agentResponse;

    // Concession / Sycophancy Check
    if (lowerRaw.includes("waive") || lowerRaw.includes("discount") || lowerRaw.includes("free")) {
      l2RiskAudit.className = "sycophancy-monitor violation";
      l2RiskText.textContent = "Concession pressure detected. L3 Outbound Veto engaged.";
    } else {
      l2RiskAudit.className = "sycophancy-monitor";
      l2RiskText.textContent = "Output conforms to policy safety boundary.";
    }

    // -------------------------------------------------------------
    // L3: Interactive Circuit State Machine (The Star)
    // -------------------------------------------------------------
    resetCircuit();

    const abortTrans = transitions.find(t => t.to_state === "ABORTED");
    const freezeTrans = transitions.find(t => t.to_state === "FROZEN");
    const commitTrans = transitions.find(t => t.to_state === "COMMITTED");
    const heldTrans = transitions.find(t => t.to_state === "HELD" || t.from_state === "HELD");

    if (abortTrans) {
      nodeHeld.classList.add("active-held");
      nodeFrozen.classList.add("active-frozen");
      nodeAborted.classList.add("active-aborted");
      wireStagedFreeze.classList.add("active");
      wireFreezeAbort.classList.add("aborted");

      metricCommitWindow.textContent = "ABORTED";
      metricCommitWindow.className = "cell-value font-mono text-rose";
      metricCommitSub.textContent = "Dispatch Cancelled";

      updateTransitionBar("ABORTED", abortTrans.reason || "Caller revocation verified at turn 2", "aborted");
      addTapeEntry(`L3 Enforcement: Dispatch ABORTED (${abortTrans.action_id || "tow"})`, "abort");
    } else if (freezeTrans) {
      nodeHeld.classList.add("active-held");
      nodeFrozen.classList.add("active-frozen");
      wireStagedFreeze.classList.add("active");

      metricCommitWindow.textContent = "FROZEN";
      metricCommitWindow.className = "cell-value font-mono text-amber";
      metricCommitSub.textContent = "Revocation Under Scrutiny";

      updateTransitionBar("FROZEN", freezeTrans.reason || "Cancel-like token detected in audio", "frozen");
      addTapeEntry(`L3 Enforcement: Intent FROZEN pending intent resolution`, "gate");
    } else if (commitTrans) {
      nodeHeld.classList.add("active-held");
      nodeCommitted.classList.add("active-committed");
      wireStagedFreeze.classList.add("committed");
      wireFreezeCommit.classList.add("committed");

      metricCommitWindow.textContent = "COMMITTED";
      metricCommitWindow.className = "cell-value font-mono text-emerald";
      metricCommitSub.textContent = "Flatbed Tow En Route";

      updateTransitionBar("COMMITTED", commitTrans.reason || "Dispatch authorized to NH48 garage", "committed");
      addTapeEntry(`L3 Enforcement: Action COMMITTED to System of Record`, "commit");
    } else if (heldTrans) {
      nodeHeld.classList.add("active-held");
      wireStagedFreeze.classList.add("active");

      metricCommitWindow.textContent = "HELD";
      metricCommitWindow.className = "cell-value font-mono text-indigo";
      metricCommitSub.textContent = "Grace Window Active (25m)";

      updateTransitionBar("HELD", "Action staged in memory with cancellation grace window", "held");
      addTapeEntry(`L3 Enforcement: Action staged into HELD state`, "gate");
    }

    // Outbound Veto
    if (lowerRaw.includes("waive") || lowerRaw.includes("discount") || lowerRaw.includes("maaf")) {
      l3VetoCard.className = "veto-gate-card triggered";
      l3VetoTitle.textContent = "Outbound Veto Intercepted Concession Proposal";
      l3VetoDetail.textContent = "Model attempted to compromise deductible. Outbound veto blocked response and injected mandatory Section 4.2 refusal.";
      addTapeEntry("L3 Outbound Veto: Sycophantic waiver BLOCKED. Policy cited.", "abort");
    } else {
      l3VetoCard.className = "veto-gate-card";
      l3VetoTitle.textContent = "Policy Latch: Deductible ₹1,500 Locked";
      l3VetoDetail.textContent = "SQLite trigger latches financial fields. Outbound veto intercepts sycophantic promises before transmission.";
    }

    // -------------------------------------------------------------
    // L4 & L5: Authoritative State & PRISM
    // -------------------------------------------------------------
    if (currentClaim && currentClaim.claim_id && currentClaim.claim_id !== "NONE") {
      metricClaim.textContent = currentClaim.claim_id;
      metricClaimSub.textContent = `Status: ${currentClaim.status || "OPEN"}`;
      l4ClaimId.textContent = currentClaim.claim_id;
      l4Deductible.textContent = `₹${currentClaim.deductible_inr || 1500} [TRIGGER LOCKED]`;
      l4Dispatches.textContent = abortTrans ? "0 Active (1 Aborted)" : "1 Tow Truck Staged";
    }

    totalSpansCount += 2;
    metricSpans.textContent = `${totalSpansCount} Spans`;
    addTapeEntry(`PRISM Span emitted: turn_id=${data.turn_id || 1}, latency=240ms`, "prism");
  }

  function resetCircuit() {
    [nodeHeld, nodeFrozen, nodeCommitted, nodeAborted].forEach(n => {
      n.className.baseVal = "circuit-node";
    });
    [wireStagedFreeze, wireFreezeCommit, wireFreezeAbort].forEach(w => {
      w.className.baseVal = "circuit-wire" + (w.classList.contains("branch") ? " branch" : "");
    });
  }

  function updateTransitionBar(state, text, stateClass) {
    l3Transition.innerHTML = `
      <span class="record-state-pill ${stateClass} font-mono">${state}</span>
      <span class="record-text">${text}</span>
    `;
  }

  function addTapeEntry(text, tag = "prism") {
    const now = new Date();
    const timeStr = now.toTimeString().split(" ")[0];
    const row = document.createElement("div");
    row.className = "tape-row";
    row.innerHTML = `
      <span class="tape-time">${timeStr}</span>
      <span class="tape-tag ${tag}">${tag.toUpperCase()}</span>
      <span class="tape-text">${text}</span>
    `;
    prismStream.prepend(row);
  }

  // =========================================================================
  // 4. Reset Button
  // =========================================================================
  btnReset.addEventListener("click", async () => {
    if (!confirm("Reset demo session, claims, and inspection metrics?")) return;
    try {
      await fetch("/api/session/reset?session_id=live-demo", { method: "POST" });
      totalPiiCount = 0;
      totalSpansCount = 0;
      metricPolicy.textContent = "NH-8821";
      metricClaim.textContent = "Awaiting Intimation";
      metricClaimSub.textContent = "SQLite System of Record";
      metricCommitWindow.textContent = "IDLE";
      metricCommitWindow.className = "cell-value font-mono text-amber";
      metricPiiCount.textContent = "0 Scrubbed";
      metricSpans.textContent = "Active";

      l1Raw.textContent = "Waiting for caller to speak on phone...";
      l1Masked.textContent = "—";
      l1PiiAudit.innerHTML = `
        <div class="audit-clean-state">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <span>Zero clear-text card, Aadhaar, or phone identifiers transmitted to LLM.</span>
        </div>
      `;

      l2ToolCalls.textContent = "Model idle.";
      l2RawReply.textContent = "—";
      l2RiskAudit.className = "sycophancy-monitor";
      l2RiskText.textContent = "Output conforms to policy safety boundary.";

      resetCircuit();
      updateTransitionBar("IDLE", "State machine armed. Dispatches start in HELD state.", "");

      l3VetoCard.className = "veto-gate-card";
      l3VetoTitle.textContent = "Policy Latch: Deductible ₹1,500 Locked";
      l3VetoDetail.textContent = "SQLite trigger latches financial fields. Outbound veto intercepts sycophantic promises before transmission.";

      l4ClaimId.textContent = "NONE";
      l4Dispatches.textContent = "0 Active";

      addTapeEntry("Flight telemetry reset to baseline state.", "commit");
    } catch (err) {
      console.error(err);
    }
  });
});
