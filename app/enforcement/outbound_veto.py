"""Outbound Veto (ClaimGuard L3 Enforcement).

Thesis: "The LLM proposes; deterministic code disposes."
Before anything is spoken or returned to the caller, the Outbound Veto intercepts
the agent response to guarantee:
1. Grounded Financial Figures: Any rupee figure mentioned MUST exist in the verified
   policy record or retrieved context chunks. Hallucinated numbers are blocked.
2. No Concessions: Spoken concessions ("we will waive the deductible", "no charge for you")
   are vetoed and replaced with an authoritative, grounded policy clause citation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional, Set


@dataclass
class VetoResult:
    passed: bool
    original_text: str
    filtered_text: str
    veto_reasons: List[str] = field(default_factory=list)


# Concession phrases (English and Hindi/Code-mixed)
CONCESSION_PATTERNS = [
    r"\b(?:will|can|shall|i'?ll)\s+(?:waive|waived|remove|drop)\b",
    r"\bwaive\s+(?:the\s+)?(?:deductible|charge|fee|cost)\b",
    r"\bno\s+charge\s+(?:for\s+you|to\s+you|at\s+all)\b",
    r"\bno\s+charge\b",
    r"\bfree\s+of\s+charge\b",
    r"\bwon'?t\s+charge\b",
    r"\bwill\s+not\s+charge\b",
    r"\bdon'?t\s+worry\s+about\s+the\s+deductible\b",
    r"\bzero\s+deductible\b",
    r"\bno\s+cost\s+to\s+you\b",
    r"\bwe\s+will\s+cover\s+everything\b",
    # Hindi / Code-mixed concessions
    r"\bmaaf\s+kar\s+d(?:enge|unga|o)\b",
    r"\bcharge\s+nah?i\s+lagega\b",
    r"\bkoi\s+charge\s+nah?i\b",
    r"\bkoi\s+paisa\s+nah?i\b",
    r"\bpaisa\s+mat\s+dena\b",
    r"\bzero\s+rupay?e\b",
]

# Regex patterns matching Rupee amounts: ₹1500, ₹ 1,500, Rs. 1500, INR 1500, 1500 rupees
RUPEE_EXTRACTION_PATTERN = re.compile(
    r"(?:₹|Rs\.?|INR)\s*([0-9]+(?:,[0-9]+)*)|([0-9]+(?:,[0-9]+)*)\s*(?:rupees|rupaye|rs)",
    re.IGNORECASE,
)


class OutboundVeto:
    """Deterministic Outbound Veto filter."""

    def __init__(
        self,
        default_policy_number: str = "NH-8821",
        default_deductible_inr: int = 1500,
    ) -> None:
        self.default_policy_number = default_policy_number
        self.default_deductible_inr = default_deductible_inr

    @staticmethod
    def extract_rupee_figures(text: str) -> List[int]:
        """Extract all integer rupee amounts from an utterance."""
        figures: List[int] = []
        for match in RUPEE_EXTRACTION_PATTERN.finditer(text):
            val_str = match.group(1) or match.group(2)
            if val_str:
                clean_num = val_str.replace(",", "")
                try:
                    figures.append(int(clean_num))
                except ValueError:
                    pass
        return figures

    def check_concessions(self, text: str) -> List[str]:
        """Detect any forbidden concession phrases."""
        violations = []
        lower_text = text.lower()
        for pat in CONCESSION_PATTERNS:
            if re.search(pat, lower_text):
                violations.append(f"Forbidden concession pattern detected: '{pat}'")
        return violations

    def check_unverified_figures(
        self,
        text: str,
        allowed_figures: Set[int],
    ) -> List[str]:
        """Ensure every ₹ figure in text is explicitly authorized by policy or context."""
        violations = []
        detected_figures = self.extract_rupee_figures(text)
        for fig in detected_figures:
            if fig not in allowed_figures:
                violations.append(
                    f"Phantom rupee amount ₹{fig:,} not found in verified policy or context"
                )
        return violations

    def verify_and_filter(
        self,
        text: str,
        allowed_figures: Optional[Set[int]] = None,
        policy_number: Optional[str] = None,
        deductible_inr: Optional[int] = None,
        context_chunks: Optional[List[str]] = None,
    ) -> VetoResult:
        """Inspect agent response. If vetoed, replace with grounded policy citation."""
        reasons: List[str] = []
        pol_num = policy_number or self.default_policy_number
        deductible = deductible_inr or self.default_deductible_inr

        # 1. Build authoritative allowed figures
        authorized: Set[int] = {
            deductible,
            5000,   # Standard roadside coverage limit
            10000,  # Ambulance rider limit
            80,     # Excess per-km towing rate
            50,     # Standard 50 km towing radius
            0,      # Ambulance zero deductible
        }
        if allowed_figures:
            authorized.update(allowed_figures)

        # Also permit any numbers extracted directly from retrieved RAG context chunks
        if context_chunks:
            for chunk in context_chunks:
                for fig in self.extract_rupee_figures(chunk):
                    authorized.add(fig)

        # 2. Check for concession phrases
        concession_violations = self.check_concessions(text)
        reasons.extend(concession_violations)

        # 3. Check for phantom rupee figures
        figure_violations = self.check_unverified_figures(text, authorized)
        reasons.extend(figure_violations)

        if not reasons:
            return VetoResult(
                passed=True,
                original_text=text,
                filtered_text=text,
                veto_reasons=[],
            )

        # VETO TRIGGERED: Provide deterministic grounded refusal citing policy clause
        grounded_replacement = (
            f"Under Section 4.2 of Policy {pol_num}, standard mandatory deductibles "
            f"of ₹{deductible:,} apply to roadside dispatches along the NH48 corridor "
            f"and cannot be waived by phone representatives. Your dispatch request remains "
            f"active under these standard policy terms."
        )

        return VetoResult(
            passed=False,
            original_text=text,
            filtered_text=grounded_replacement,
            veto_reasons=reasons,
        )
