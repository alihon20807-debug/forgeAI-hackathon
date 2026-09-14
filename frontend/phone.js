/**
 * ClaimGuard Mobile Phone Call Controller
 * Native-feeling voice call UI with ASR, TTS, and Commit Window feedback.
 */

document.addEventListener("DOMContentLoaded", () => {
  const SESSION_ID = "live-demo";
  let turnId = 1;
  let callSeconds = 0;
  let callTimerInterval = null;
  let isRecording = false;
  let speakerEnabled = true;

  // DOM Elements
  const callTimer = document.getElementById("call-timer");
  const conversationStream = document.getElementById("conversation-stream");
  const pttBtn = document.getElementById("ptt-btn");
  const pttHint = document.getElementById("ptt-hint");
  const transcribingStatus = document.getElementById("transcribing-status");
  const enforcementHud = document.getElementById("enforcement-hud");
  const hudIcon = document.getElementById("hud-icon");
  const hudText = document.getElementById("hud-text");
  const btnToggleSpeaker = document.getElementById("btn-toggle-speaker");
  const btnToggleText = document.getElementById("btn-toggle-text");
  const btnResetCall = document.getElementById("btn-reset-call");
  const textDrawer = document.getElementById("text-drawer");
  const textInput = document.getElementById("text-input");
  const textSendBtn = document.getElementById("text-send-btn");
  const micCanvas = document.getElementById("mic-canvas");
  const micCtx = micCanvas ? micCanvas.getContext("2d") : null;
  const demoPills = document.querySelectorAll(".pill-btn");

  // =========================================================================
  // 1. Call Timer
  // =========================================================================
  function startTimer() {
    if (callTimerInterval) clearInterval(callTimerInterval);
    callSeconds = 0;
    callTimerInterval = setInterval(() => {
      callSeconds++;
      const mins = String(Math.floor(callSeconds / 60)).padStart(2, "0");
      const secs = String(callSeconds % 60).padStart(2, "0");
      callTimer.textContent = `${mins}:${secs}`;
    }, 1000);
  }
  startTimer();

  // =========================================================================
  // 2. Audio Waveform Visualizer
  // =========================================================================
  let wavePhase = 0;
  function renderWaveform() {
    if (!micCanvas || !micCtx) return;
    const w = micCanvas.width;
    const h = micCanvas.height;
    micCtx.clearRect(0, 0, w, h);

    const bars = 28;
    const barWidth = w / bars - 2;
    const centerY = h / 2;

    micCtx.fillStyle = isRecording ? "#E11D48" : "#059669";

    for (let i = 0; i < bars; i++) {
      let amp = 2;
      if (isRecording) {
        amp = Math.sin(i * 0.4 + wavePhase) * 12 + Math.cos(i * 0.8 - wavePhase) * 6 + 6;
      } else if (window.speechSynthesis && window.speechSynthesis.speaking) {
        amp = Math.sin(i * 0.3 + wavePhase) * 8 + 4;
      }
      amp = Math.max(2, Math.min(amp, h / 2 - 2));
      const x = i * (barWidth + 2);
      const y = centerY - amp;
      micCtx.beginPath();
      micCtx.roundRect(x, y, barWidth, amp * 2, 2);
      micCtx.fill();
    }

    wavePhase += isRecording ? 0.28 : 0.05;
    requestAnimationFrame(renderWaveform);
  }
  renderWaveform();

  // =========================================================================
  // 3. Text-to-Speech (Agent Voice Out)
  // =========================================================================
  function speakAgentReply(text) {
    if (!speakerEnabled || !("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel(); // Stop any pending speech

    // Clean out tags like [CARD REDACTED] for clean spoken delivery
    const cleanSpeech = text
      .replace(/\[CARD REDACTED\]/gi, "Card number redacted")
      .replace(/\[AADHAAR REDACTED\]/gi, "Aadhaar number redacted")
      .replace(/₹/g, "rupees ");

    const utterance = new SpeechSynthesisUtterance(cleanSpeech);
    utterance.rate = 1.05;
    utterance.pitch = 1.0;

    // Pick Indian English voice or Hindi voice if available
    const voices = window.speechSynthesis.getVoices();
    const preferredVoice = voices.find(v => v.lang.includes("en-IN") || v.lang.includes("hi-IN") || v.name.includes("India"));
    if (preferredVoice) {
      utterance.voice = preferredVoice;
    }

    window.speechSynthesis.speak(utterance);
  }

  // Pre-load voices
  if ("speechSynthesis" in window) {
    window.speechSynthesis.onvoiceschanged = () => {
      window.speechSynthesis.getVoices();
    };
  }

  // =========================================================================
  // 4. Message Bubble Helpers
  // =========================================================================
  function appendMessage(role, text, redactedList = []) {
    const bubble = document.createElement("div");
    bubble.className = `msg-bubble ${role}`;

    const sender = document.createElement("div");
    sender.className = "bubble-sender";
    sender.textContent = role === "agent" ? "ClaimGuard AI" : "Caller (You)";
    bubble.appendChild(sender);

    const body = document.createElement("div");
    body.className = "bubble-text";

    // Format redaction tags with visual badges
    let formatted = text
      .replace(/\[CARD REDACTED\]/g, '<span class="redaction-badge">🔒 Card Redacted (Luhn)</span>')
      .replace(/\[AADHAAR REDACTED\]/g, '<span class="redaction-badge">🔒 Aadhaar Redacted (Verhoeff)</span>')
      .replace(/\[PHONE REDACTED\]/g, '<span class="redaction-badge">🔒 Phone Redacted</span>');

    body.innerHTML = formatted;
    bubble.appendChild(body);

    conversationStream.appendChild(bubble);
    conversationStream.scrollTop = conversationStream.scrollHeight;
  }

  // =========================================================================
  // 5. Backend Turn Submission
  // =========================================================================
  async function processTurn(rawText) {
    if (!rawText.trim()) return;

    transcribingStatus.textContent = "Processing ClaimGuard Enforcement...";
    pttBtn.disabled = true;

    // Show temporary caller bubble immediately
    appendMessage("caller", rawText);

    try {
      const resp = await fetch("/api/call/turn", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: SESSION_ID,
          turn_id: turnId++,
          caller_id: "caller_mobile",
          raw_transcript: rawText,
          masked_transcript: rawText, // Backend PII shield will sanitize if raw
          agent_version: "v2",
        }),
      });

      if (!resp.ok) throw new Error(`Turn failed: ${resp.status}`);

      const data = await resp.json();

      // Show Agent Response
      appendMessage("agent", data.agent_response);
      speakAgentReply(data.agent_response);

      // Update Enforcement HUD based on state machine transitions
      updateEnforcementHud(data);

      transcribingStatus.textContent = "Hold mic to speak or tap a prompt";
    } catch (err) {
      console.error(err);
      transcribingStatus.textContent = "Turn error. Is server running on port 8000?";
    } finally {
      pttBtn.disabled = false;
    }
  }

  function updateEnforcementHud(data) {
    const transitions = data.state_machine?.transitions || [];
    const claim = data.current_claim;

    // Check for Abort / Freeze
    const abortTrans = transitions.find(t => t.to_state === "ABORTED");
    const freezeTrans = transitions.find(t => t.to_state === "FROZEN");
    const commitTrans = transitions.find(t => t.to_state === "COMMITTED");

    enforcementHud.className = "enforcement-hud";

    if (abortTrans) {
      enforcementHud.classList.add("aborted");
      hudIcon.textContent = "🛑";
      hudText.textContent = `Dispatch Revoked & Aborted (${abortTrans.action_id || "tow"})`;
    } else if (freezeTrans) {
      enforcementHud.classList.add("frozen");
      hudIcon.textContent = "❄️";
      hudText.textContent = "Commit Window: Intent Frozen (Resolving...)";
    } else if (commitTrans) {
      hudIcon.textContent = "✅";
      hudText.textContent = "Dispatch Committed to NH48 Garage";
    } else if (claim && claim.claim_id && claim.claim_id !== "NONE") {
      hudIcon.textContent = "📋";
      hudText.textContent = `Claim ${claim.claim_id} Active · Deductible ₹${claim.deductible_inr || 1500} Locked`;
    } else {
      hudIcon.textContent = "🛡️";
      hudText.textContent = "Policy NH-8821 Active · Deductible ₹1,500";
    }
  }

  // =========================================================================
  // 6. Voice Recording (MediaRecorder + Whisper / Speech API)
  // =========================================================================
  let mediaRecorder = null;
  let audioChunks = [];
  let speechRecognizer = null;

  // Initialize Web Speech API if supported
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    speechRecognizer = new SpeechRecognition();
    speechRecognizer.continuous = false;
    speechRecognizer.interimResults = false;
    speechRecognizer.lang = "en-IN"; // English-India / code-mixed friendly
  }

  async function startRecording() {
    if (isRecording) return;
    isRecording = true;
    pttBtn.classList.add("recording");
    pttHint.textContent = "LISTENING...";
    transcribingStatus.textContent = "Listening to your voice...";

    audioChunks = [];

    // 1. Try browser Speech Recognition
    if (speechRecognizer) {
      try {
        speechRecognizer.start();
        speechRecognizer.onresult = (e) => {
          const spoken = e.results[0][0].transcript;
          if (spoken) processTurn(spoken);
        };
        speechRecognizer.onerror = (e) => {
          console.warn("Speech recognition error:", e.error);
        };
      } catch (err) {
        console.warn("SpeechRecognizer already active or blocked:", err);
      }
    }

    // 2. Try MediaRecorder for raw Whisper upload
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = (e) => {
          if (e.data && e.data.size > 0) audioChunks.push(e.data);
        };
        mediaRecorder.start();
      } catch (err) {
        console.warn("Mic access blocked or insecure origin:", err);
        transcribingStatus.textContent = "Mic blocked on HTTP. Tap quick prompts below or use HTTPS tunnel.";
      }
    }
  }

  async function stopRecording() {
    if (!isRecording) return;
    isRecording = false;
    pttBtn.classList.remove("recording");
    pttHint.textContent = "HOLD TO SPEAK";

    if (speechRecognizer) {
      try { speechRecognizer.stop(); } catch (e) {}
    }

    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.onstop = async () => {
        // If we have valid audio chunks, send to Whisper ASR
        if (audioChunks.length > 0) {
          const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
          try {
            transcribingStatus.textContent = "Transcribing with Whisper (Indic bias)...";
            const formData = new FormData();
            formData.append("file", audioBlob, "call_turn.wav");
            formData.append("session_id", SESSION_ID);
            const trRes = await fetch("/api/voice/transcribe", { method: "POST", body: formData });
            if (trRes.ok) {
              const trData = await trRes.json();
              if (trData.raw_transcript) {
                processTurn(trData.raw_transcript);
                return;
              }
            }
          } catch (e) {
            console.warn("ASR server error:", e);
          }
        }
      };
      mediaRecorder.stop();
      if (mediaRecorder.stream) {
        mediaRecorder.stream.getTracks().forEach(t => t.stop());
      }
    }
  }

  // PTT Touch & Mouse Handlers
  pttBtn.addEventListener("mousedown", startRecording);
  pttBtn.addEventListener("mouseup", stopRecording);
  pttBtn.addEventListener("mouseleave", () => { if (isRecording) stopRecording(); });

  pttBtn.addEventListener("touchstart", (e) => {
    e.preventDefault();
    startRecording();
  });
  pttBtn.addEventListener("touchend", (e) => {
    e.preventDefault();
    stopRecording();
  });

  // Tap-to-Talk Toggle fallback
  pttBtn.addEventListener("click", () => {
    // If not holding, quick tap toggles recording state
  });

  // =========================================================================
  // 7. Demo Script One-Tap Pills
  // =========================================================================
  demoPills.forEach(pill => {
    pill.addEventListener("click", () => {
      const text = pill.getAttribute("data-text");
      if (text) {
        processTurn(text);
      }
    });
  });

  // =========================================================================
  // 8. Control Actions: Speaker, Keyboard, Reset
  // =========================================================================
  btnToggleSpeaker.addEventListener("click", () => {
    speakerEnabled = !speakerEnabled;
    btnToggleSpeaker.classList.toggle("active", speakerEnabled);
    if (!speakerEnabled && "speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
  });
  btnToggleSpeaker.classList.add("active"); // default ON

  btnToggleText.addEventListener("click", () => {
    textDrawer.classList.toggle("hidden");
    if (!textDrawer.classList.contains("hidden")) {
      textInput.focus();
    }
  });

  textSendBtn.addEventListener("click", () => {
    const val = textInput.value.trim();
    if (val) {
      processTurn(val);
      textInput.value = "";
      textDrawer.classList.add("hidden");
    }
  });

  textInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      textSendBtn.click();
    }
  });

  btnResetCall.addEventListener("click", async () => {
    if (!confirm("Reset demo session and clear all active claims?")) return;
    try {
      await fetch(`/api/session/reset?session_id=${SESSION_ID}`, { method: "POST" });
      turnId = 1;
      startTimer();
      conversationStream.innerHTML = `
        <div class="msg-bubble agent">
          <div class="bubble-sender">ClaimGuard AI</div>
          <div class="bubble-text">Namaste. ClaimGuard Roadside Assistance helpline par aapka swagat hai. How can I help you today?</div>
        </div>
      `;
      enforcementHud.className = "enforcement-hud";
      hudIcon.textContent = "⚡";
      hudText.textContent = "Policy NH-8821 Active · Deductible ₹1,500";
      transcribingStatus.textContent = "Session reset cleanly for demo";
    } catch (e) {
      console.error(e);
    }
  });
});
