"""Commit Window State Machine (ClaimGuard L3 Enforcement).

Thesis: "The LLM proposes; deterministic code disposes."
Staging: Every consequential tool call starts in HELD state.
Freeze: Any cancel-like or hesitation keyword in the transcript immediately transitions
        all HELD actions to FROZEN.
Resolve: Analyzes intent (separating true revocations from look-alike traps) to transition
         actions to COMMITTED or ABORTED.
"""

from __future__ import annotations

import re
import time
import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class ActionState(str, Enum):
    HELD = "HELD"
    FROZEN = "FROZEN"
    COMMITTED = "COMMITTED"
    ABORTED = "ABORTED"


@dataclass
class StateTransition:
    action_id: str
    action_type: str
    from_state: str
    to_state: str
    reason: str

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


@dataclass
class HeldAction:
    action_id: str
    session_id: str
    action_type: str  # e.g., 'stage_dispatch', 'open_claim'
    payload: Dict[str, Any]
    state: ActionState = ActionState.HELD
    staged_at: float = field(default_factory=time.time)
    staged_turn: int = 1
    frozen_at: Optional[float] = None
    resolved_at: Optional[float] = None
    reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "session_id": self.session_id,
            "action_type": self.action_type,
            "payload": self.payload,
            "state": self.state.value,
            "staged_at": self.staged_at,
            "staged_turn": self.staged_turn,
            "frozen_at": self.frozen_at,
            "resolved_at": self.resolved_at,
            "reason": self.reason,
        }


# Keywords that trigger immediate safety freeze
FREEZE_PATTERNS = [
    r"\bwait\b",
    r"\bruko\b",
    r"\bcancel\b",
    r"\bstop\b",
    r"\bdon'?t\s+send\b",
    r"\bdo\s+not\s+send\b",
    r"\bmat\s+bhejo\b",
    r"\bhold\s+on\b",
    r"\bhold\s+back\b",
    r"\bnah?i\s+chahi?ye\b",
    r"\brehne\s+d[oe]\b",
    r"\babort\b",
    r"\bnever\s*mind\b",
    r"\brok\s+do\b",
    r"\brok\s+lo\b",
    r"\bthoda\s+ruko\b",
    r"\bwait\s+karo\b",
    r"\bmat\s+bulao\b",
    r"\bno\s+need\b",
    r"\bdo\s+not\s+dispatch\b",
]

# Patterns representing look-alike traps ("don't hold back, send it now")
# Even though "hold back" trips the freeze trigger, the intent is strongly affirmative.
LOOKALIKE_AFFIRM_PATTERNS = [
    r"don'?t\s+hold\s+back[,\s]+send\b",
    r"don'?t\s+hold\s+back",
    r"send\s+it\s+now",
    r"send\s+now",
    r"jaldi\s+bhejo",
    r"turant\s+bhejo",
    r"wait\s+mat\s+karo",
    r"ruko\s+mat",
    r"der\s+mat\s+karo",
    r"without\s+delay",
    r"asap\b",
]

# Patterns representing explicit revocations
REVOCATION_PATTERNS = [
    r"don'?t\s+send",
    r"do\s+not\s+send",
    r"cancel\s+(the\s+)?(tow|dispatch|truck|crane|ambulance|claim|mechanic|assistance)",
    r"cancel\s+karo",
    r"mat\s+bhejo",
    r"abort\s+(the\s+)?(dispatch|tow|action)",
    r"stop\s+(the\s+)?(dispatch|tow|truck|crane|mechanic)",
    r"cousin\s+(just\s+)?showed\s+up",
    r"cousin\s+aa\s+gaya",
    r"friend\s+(just\s+)?(showed\s+up|arrived)",
    r"friend\s+aa\s+gaya",
    r"police\s+patrol",
    r"car\s+started",
    r"gaadi\s+start\s+ho\s+gayi",
    r"theek\s+ho\s+gay[ia]",
    r"nah?i\s+chahi?ye",
    r"rehne\s+d[oe]",
    r"no\s+need",
    r"mechanic\s+fixed",
]


class CommitWindow:
    """Session-scoped or global manager for the ClaimGuard Commit Window."""

    def __init__(self) -> None:
        # session_id -> list of HeldAction
        self._actions: Dict[str, List[HeldAction]] = {}
        # session_id -> list of StateTransition
        self._transitions: Dict[str, List[StateTransition]] = {}

    def stage_action(
        self,
        session_id: str,
        action_type: str,
        payload: Dict[str, Any],
        action_id: Optional[str] = None,
        staged_turn: int = 1,
    ) -> HeldAction:
        """Stage a consequential action into HELD state."""
        aid = action_id or f"act_{action_type[:3]}_{uuid.uuid4().hex[:6]}"
        action = HeldAction(
            action_id=aid,
            session_id=session_id,
            action_type=action_type,
            payload=payload,
            state=ActionState.HELD,
            staged_at=time.time(),
            staged_turn=staged_turn,
        )
        if session_id not in self._actions:
            self._actions[session_id] = []
            self._transitions[session_id] = []

        self._actions[session_id].append(action)
        return action

    def detect_freeze_trigger(self, transcript: str) -> Optional[str]:
        """Detect any cancel, pause, or hesitation keywords in the transcript."""
        text = transcript.lower()
        for pattern in FREEZE_PATTERNS:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return None

    def freeze_all_held(self, session_id: str, trigger_word: str) -> List[StateTransition]:
        """Freeze all currently HELD actions in a session."""
        transitions: List[StateTransition] = []
        actions = self._actions.get(session_id, [])
        for action in actions:
            if action.state == ActionState.HELD:
                action.state = ActionState.FROZEN
                action.frozen_at = time.time()
                action.reason = f"Freeze trigger detected: '{trigger_word}'"
                t = StateTransition(
                    action_id=action.action_id,
                    action_type=action.action_type,
                    from_state=ActionState.HELD.value,
                    to_state=ActionState.FROZEN.value,
                    reason=action.reason,
                )
                transitions.append(t)
                self._transitions[session_id].append(t)
        return transitions

    def resolve_action(
        self,
        session_id: str,
        action_id: str,
        target_state: ActionState,
        reason: str,
    ) -> Optional[StateTransition]:
        """Manually or algorithmically transition an action to COMMITTED or ABORTED."""
        actions = self._actions.get(session_id, [])
        for action in actions:
            if action.action_id == action_id:
                if action.state in (ActionState.COMMITTED, ActionState.ABORTED):
                    return None  # Terminal state
                from_state = action.state.value
                action.state = target_state
                action.resolved_at = time.time()
                action.reason = reason
                t = StateTransition(
                    action_id=action.action_id,
                    action_type=action.action_type,
                    from_state=from_state,
                    to_state=target_state.value,
                    reason=reason,
                )
                self._transitions[session_id].append(t)

                # Sync status with DB if dispatch
                if action.action_type == "stage_dispatch":
                    try:
                        from app.db.database import update_dispatch_status_db
                        update_dispatch_status_db(dispatch_id=action.action_id, status=target_state.value)
                    except Exception:
                        pass

                return t
        return None

    def process_turn_intent(
        self,
        session_id: str,
        transcript: str,
    ) -> Tuple[List[StateTransition], Optional[str]]:
        """Core state resolution logic for a conversational turn.
        
        1. Checks for freeze triggers.
        2. Evaluates whether the utterance represents a look-alike trap vs true revocation.
        3. Returns (transitions_occurred, freeze_trigger_word).
        """
        transitions: List[StateTransition] = []
        trigger = self.detect_freeze_trigger(transcript)

        # If trigger found, first freeze any HELD actions
        if trigger:
            freeze_trans = self.freeze_all_held(session_id, trigger)
            transitions.extend(freeze_trans)

        lower_text = transcript.lower()

        # Step 2: Check for Look-alike Traps ("don't hold back, send it now")
        is_lookalike_affirm = any(re.search(pat, lower_text) for pat in LOOKALIKE_AFFIRM_PATTERNS)
        is_true_revocation = any(re.search(pat, lower_text) for pat in REVOCATION_PATTERNS)

        actions = self._actions.get(session_id, [])
        for action in actions:
            if action.state in (ActionState.FROZEN, ActionState.HELD):
                if is_lookalike_affirm and not is_true_revocation:
                    # Look-alike trap: Caller actually wants the dispatch executed urgently!
                    t = self.resolve_action(
                        session_id=session_id,
                        action_id=action.action_id,
                        target_state=ActionState.COMMITTED,
                        reason="Look-alike affirmation resolved: urgent dispatch confirmed",
                    )
                    if t:
                        transitions.append(t)
                elif is_true_revocation:
                    # True revocation: Caller cancelled the dispatch
                    if action.action_type == "stage_dispatch":
                        t = self.resolve_action(
                            session_id=session_id,
                            action_id=action.action_id,
                            target_state=ActionState.ABORTED,
                            reason=f"Caller revocation verified: '{transcript.strip()}'",
                        )
                        if t:
                            transitions.append(t)
                    else:
                        # Claim record stays open as per Section 6.1 / Cat B invariant
                        t = self.resolve_action(
                            session_id=session_id,
                            action_id=action.action_id,
                            target_state=ActionState.COMMITTED,
                            reason="Claim record preserved active while dispatch aborted",
                        )
                        if t:
                            transitions.append(t)

        return transitions, trigger

    def commit_held_actions(
        self,
        session_id: str,
        reason: str = "Turn completed without revocation",
        min_turn_age: int = 0,
        current_turn: Optional[int] = None,
    ) -> List[StateTransition]:
        """Commit remaining HELD actions whose grace period or turn age has elapsed."""
        transitions: List[StateTransition] = []
        actions = self._actions.get(session_id, [])
        for action in actions:
            if action.state == ActionState.HELD:
                if min_turn_age > 0 and current_turn is not None:
                    if current_turn - action.staged_turn < min_turn_age:
                        continue  # Still in initial proposal grace turn
                t = self.resolve_action(session_id, action.action_id, ActionState.COMMITTED, reason)
                if t:
                    transitions.append(t)
        return transitions

    def get_held_actions(self, session_id: str) -> List[Dict[str, Any]]:
        """Return currently uncommitted (HELD or FROZEN) actions."""
        actions = self._actions.get(session_id, [])
        return [
            a.to_dict()
            for a in actions
            if a.state in (ActionState.HELD, ActionState.FROZEN)
        ]

    def get_all_actions(self, session_id: str) -> List[Dict[str, Any]]:
        return [a.to_dict() for a in self._actions.get(session_id, [])]

    def get_transitions(self, session_id: str) -> List[Dict[str, str]]:
        return [t.to_dict() for t in self._transitions.get(session_id, [])]

    def clear_session(self, session_id: str) -> None:
        self._actions.pop(session_id, None)
        self._transitions.pop(session_id, None)


# Global singleton instance
_GLOBAL_COMMIT_WINDOW = CommitWindow()


def get_commit_window() -> CommitWindow:
    return _GLOBAL_COMMIT_WINDOW
