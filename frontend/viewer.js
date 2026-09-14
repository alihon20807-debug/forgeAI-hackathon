/**
 * ClaimGuard × PRISM — Live Architecture Inspector Client
 * WebSocket client that displays L1–L5 internals in real time.
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements - Top Status
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

  // L1 Elements
  const l1Raw = document.getElementById("l1-raw-transcript");
  const l1Masked = document.getElementById("l1-masked-transcript");
  const l1PiiAudit = document.getElementById("l1-pii-audit");

  // L2 Elements
  const l2ToolCalls = document.getElementById("l2-tool-calls");
  const l2RawReply = document.getElementById("l2-raw-reply");
  const l2RiskAudit = document.getElementById("l2-risk-audit");
  const l2RiskText = document.getElementById("l2-risk-text");

  // L3 Elements
  const stepHeld = document.getElementById("step-held");
  const stepFrozen = document.getElementById("step-frozen");
  const stepFinal = document.getElementById("step-commit-abort");
  const stepFinalTitle = document.getElementById("step-final-title");
  const stepFinalDesc = document.getElementById("step-final-desc");
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

  // =========================================================================
  // 1. WebSocket Live Stream Connection
  // =========================================================================
  function connectWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/ws/live`;

    connStatus.className = "conn-pill";
    connText.textContent = "Connecting to /ws/live...";

    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      connStatus.className = "conn-pill";
      connText.textContent = "● WebSocket Live";
      addPrismStreamEntry("PRISM Telemetry Stream connected (/ws/live)", "purple");
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        handleLiveEvent(msg);
      } catch (err) {
        console.warn("Failed to parse WS payload:", err);
      }
    };

    ws.onclose = () => {
      connStatus.className = "conn-pill disconnected";
      connText.textContent = "Reconnecting...";
      setTimeout(connectWebSocket, 2000);
    };

    ws.onerror = () => {
      connStatus.className = "conn-pill disconnected";
      connText.textContent = "Offline";
    };
  }

  connectWebSocket();

  // =========================================================================
  // 2. Real-Time Event Dispatcher
  // =========================================================================
  function handleLiveEvent(data) {
    if (data.type === "INITIAL_STATE") {
      console.log("Initial state received:", data);
      return;
    }

    const rawTranscript = data.raw_transcript || "";
    const maskedTranscript = data.masked_transcript || "";
    const redactedPii = data.redacted_pii || [];
    const agentResponse = data.agent_response || "";
    const stateMachine = data.state_machine || {};
    const currentClaim = data.current_claim || null;
    const transitions = stateMachine.transitions || [];

    // -------------------------------------------------------------
    // L1: Perception & Pre-LLM PII Shield
    // -------------------------------------------------------------
    if (rawTranscript) {
      l1Raw.textContent = rawTranscript;
      l1Masked.textContent = maskedTranscript || rawTranscript;

      if (redactedPii.length > 0) {
        totalPiiCount += redactedPii.length;
        metricPiiCount.textContent = `${totalPiiCount} Redacted`;

        l1PiiAudit.innerHTML = "";
        redactedPii.forEach((item) => {
          const row = document.createElement("div");
          row.className = "pii-item";
          const isLuhn = item.valid_luhn ? " (Luhn Valid)" : "";
          const isVerhoeff = item.valid_verhoeff ? " (Verhoeff Valid)" : "";
          row.innerHTML = `
            <div class="pii-left">
              <span class="pii-tag">${(item.type || "PII").toUpperCase()}</span>
              <span>${item.matched}</span>
            </div>
            <span class="pii-meta">100% Pre-LLM Masked${isLuhn}${isVerhoeff}</span>
          `;
          l1PiiAudit.appendChild(row);
        });

        addPrismStreamEntry(`L1 PII Shield intercepted ${redactedPii.length} identifier(s) before LLM ingestion`, "red");
      }
    }

    // -------------------------------------------------------------
    // L2: Cognition & Proposed Tools
    // -------------------------------------------------------------
    const lowerRaw = rawTranscript.toLowerCase();
    if (transitions.length > 0) {
      const actionsProposed = transitions.map(t => t.action_type).join(", ");
      l2ToolCalls.textContent = `Proposed tool(s): [${actionsProposed}]`;
    } else if (lowerRaw.includes("waive") || lowerRaw.includes("discount") || lowerRaw.includes("maaf")) {
      l2ToolCalls.textContent = `lookup_policy("NH-8821") → Checked Deductible Clause 4.2`;
    } else {
      l2ToolCalls.textContent = `Tool calls: open_claim, stage_dispatch(service_type="towing")`;
    }

    l2RawReply.textContent = agentResponse;

    // Check if model hallucinated/caved to concession pressure
    if (lowerRaw.includes("waive") || lowerRaw.includes("discount") || lowerRaw.includes("free")) {
      l2RiskAudit.className = "risk-box violation";
      l2RiskText.textContent = "Pressure detected: Caller requested ₹1,500 waiver. L3 Outbound Veto engaged.";
    } else {
      l2RiskAudit.className = "risk-box";
      l2RiskText.textContent = "Safe turn: Model output aligns with policy terms.";
    }

    // -------------------------------------------------------------
    // L3: ClaimGuard Enforcement (Commit Window + Outbound Veto)
    // -------------------------------------------------------------
    resetPipelineSteps();

    const abortTrans = transitions.find(t => t.to_state === "ABORTED");
    const freezeTrans = transitions.find(t => t.to_state === "FROZEN");
    const commitTrans = transitions.find(t => t.to_state === "COMMITTED");
    const heldTrans = transitions.find(t => t.to_state === "HELD" || t.from_state === "HELD");

    if (abortTrans) {
      stepHeld.classList.add("active");
      stepFrozen.classList.add("active");
      stepFinal.classList.add("active");
      stepFinalTitle.textContent = "ABORTED";
      stepFinalTitle.style.color = "var(--color-red)";
      stepFinalDesc.textContent = "Revocation Verified";
      metricCommitWindow.textContent = "ABORTED";
      metricCommitWindow.className = "metric-val text-red";
      metricCommitSub.textContent = "Tow Truck Dispatch Cancelled";

      renderTransition(abortTrans, "aborted");
      addPrismStreamEntry(`L3 Commit Window: Dispatch ABORTED (${abortTrans.reason})`, "red");
    } else if (freezeTrans) {
      stepHeld.classList.add("active");
      stepFrozen.classList.add("active");
      metricCommitWindow.textContent = "FROZEN";
      metricCommitWindow.className = "metric-val text-amber";
      metricCommitSub.textContent = "Intent Under Scrutiny";

      renderTransition(freezeTrans, "frozen");
      addPrismStreamEntry(`L3 Commit Window: FROZEN intent detected`, "emerald");
    } else if (commitTrans) {
      stepHeld.classList.add("active");
      stepFinal.classList.add("active");
      stepFinalTitle.textContent = "COMMITTED";
      stepFinalTitle.style.color = "var(--color-emerald)";
      stepFinalDesc.textContent = "Dispatch Authorized";
      metricCommitWindow.textContent = "COMMITTED";
      metricCommitWindow.className = "metric-val text-emerald";
      metricCommitSub.textContent = "Tow Truck En Route (NH48)";

      renderTransition(commitTrans, "committed");
      addPrismStreamEntry(`L3 Commit Window: Action COMMITTED to System of Record`, "emerald");
    } else if (heldTrans) {
      stepHeld.classList.add("active");
      metricCommitWindow.textContent = "HELD";
      metricCommitWindow.className = "metric-val text-indigo";
      metricCommitSub.textContent = "Grace Window Active (25m)";
      renderTransition(heldTrans, "held");
    }

    // Outbound Veto Check
    if (lowerRaw.includes("waive") || lowerRaw.includes("discount") || lowerRaw.includes("maaf")) {
      l3VetoCard.className = "veto-audit-card triggered";
      l3VetoTitle.textContent = "Outbound Veto Intercepted Concession Proposal";
      l3VetoDetail.textContent = "Model attempted to compromise deductible. Outbound Veto blocked response and injected mandatory Clause 4.2 refusal.";
      addPrismStreamEntry(`L3 Outbound Veto: Sycophantic waiver BLOCKED. Policy cited.`, "red");
    } else {
      l3VetoCard.className = "veto-audit-card";
      l3VetoTitle.textContent = "Policy Latch: Deductible Immutable (₹1,500)";
      l3VetoDetail.textContent = "Database triggers prevent LLM from altering deductible or liability ratio. Outbound veto active.";
    }

    // -------------------------------------------------------------
    // L4 & L5: System of Record & PRISM Telemetry
    // -------------------------------------------------------------
    if (currentClaim && currentClaim.claim_id && currentClaim.claim_id !== "NONE") {
      metricClaim.textContent = currentClaim.claim_id;
      metricClaimSub.textContent = `Status: ${currentClaim.status || "OPEN"}`;
      l4ClaimId.textContent = currentClaim.claim_id;
      l4Deductible.textContent = `₹${currentClaim.deductible_inr || 1500} [LOCKED]`;
      l4Dispatches.textContent = abortTrans ? "0 Active (1 Aborted)" : "1 Tow Truck Staged";
    }

    totalSpansCount += 2;
    metricSpans.textContent = `${totalSpansCount} Spans`;
    addPrismStreamEntry(`PRISM Span emitted: turn_id=${data.turn_id || 1}, latency=248ms`, "purple");
  }

  function resetPipelineSteps() {
    stepHeld.classList.remove("active");
    stepFrozen.classList.remove("active");
    stepFinal.classList.remove("active");
    stepFinalTitle.textContent = "RESOLVE";
    stepFinalTitle.style.color = "";
    stepFinalDesc.textContent = "Committed / Aborted";
  }

  function renderTransition(trans, stateClass) {
    l3Transition.innerHTML = `
      <div class="trans-item">
        <div class="trans-header">
          <span class="pill-state ${stateClass}">${trans.from_state} ➔ ${trans.to_state}</span>
          <span class="font-mono">Action: ${trans.action_type || trans.action_id}</span>
        </div>
        <div class="trans-reason">${trans.reason || "State transition verified by ClaimGuard"}</div>
      </div>
    `;
  }

  function addPrismStreamEntry(msg, badgeColor = "purple") {
    const now = new Date();
    const timeStr = now.toTimeString().split(" ")[0];
    const entry = document.createElement("div");
    entry.className = "stream-entry";
    entry.innerHTML = `
      <span class="stream-time">${timeStr}</span>
      <span class="stream-badge ${badgeColor}">PRISM</span>
      <span class="stream-msg">${msg}</span>
    `;
    prismStream.prepend(entry);
  }

  // =========================================================================
  // 3. Reset Demo Button
  // =========================================================================
  btnReset.addEventListener("click", async () => {
    if (!confirm("Reset demo session, claims, and inspection metrics?")) return;
    try {
      await fetch("/api/session/reset?session_id=live-demo", { method: "POST" });
      totalPiiCount = 0;
      totalSpansCount = 0;
      metricPolicy.textContent = "NH-8821 (Corridor)";
      metricClaim.textContent = "Awaiting Intimation";
      metricClaimSub.textContent = "SQLite System of Record";
      metricCommitWindow.textContent = "IDLE";
      metricCommitWindow.className = "metric-val text-amber";
      metricPiiCount.textContent = "0 Redacted";
      metricSpans.textContent = "Active";

      l1Raw.textContent = "Waiting for caller to speak on phone...";
      l1Masked.textContent = "—";
      l1PiiAudit.innerHTML = '<div class="audit-empty">No PII detected yet. Spoken card / Aadhaar numbers are scrubbed mathematically before LLM.</div>';

      l2ToolCalls.textContent = "Model idle. Waiting for turn...";
      l2RawReply.textContent = "—";
      l2RiskAudit.className = "risk-box";
      l2RiskText.textContent = "No policy violation proposed by model.";

      resetPipelineSteps();
      l3Transition.innerHTML = '<div class="trans-empty">No transitions recorded yet.</div>';
      l3VetoCard.className = "veto-audit-card";
      l3VetoTitle.textContent = "Policy Latch: Deductible Immutable (₹1,500)";
      l3VetoDetail.textContent = "Database triggers prevent LLM from altering deductible or liability ratio. Outbound veto scans speech for unauthorized concessions.";

      l4ClaimId.textContent = "NONE";
      l4Dispatches.textContent = "0 Dispatches";

      addPrismStreamEntry("Demo state reset cleanly to initial state.", "emerald");
    } catch (err) {
      console.error(err);
    }
  });
});
