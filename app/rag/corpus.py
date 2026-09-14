"""Authoritative Policy Corpus for NH48 Corridor Insurer.

This corpus represents the ground truth for FNOL SOPs, deductibles, partner towing
rates, ambulance coverage, and legal non-waiver terms.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class RAGChunk:
    chunk_id: str
    section: str
    title: str
    content: str
    keywords: List[str]


POLICY_CORPUS: List[RAGChunk] = [
    RAGChunk(
        chunk_id="chunk_01_territory",
        section="Section 1",
        title="Territorial Scope and NH48 Corridor",
        content=(
            "NH48 Corridor Insurance operates coverage between National Highway 48 "
            "(Delhi - Gurugram - Manesar - Dharuhera - Neemrana - Kotputli - Jaipur). "
            "Roadside assistance services and partner towing networks are stationed at every 25 km milestone."
        ),
        keywords=["nh48", "delhi", "gurugram", "manesar", "dharuhera", "neemrana", "kotputli", "jaipur", "corridor", "territory"],
    ),
    RAGChunk(
        chunk_id="chunk_02_safety_first",
        section="Section 2.1",
        title="FNOL Intake SOP: Emergency & Life Safety Priority",
        content=(
            "In every First-Notice-of-Loss (FNOL) call, the intake representative must immediately ascertain "
            "if any passenger or driver is injured. If personal injury or active fire is reported, "
            "emergency ambulance dispatch takes absolute priority over vehicle recovery. "
            "Ambulance riders carry 100% cashless coverage up to ₹10,000 with ₹0 deductible."
        ),
        keywords=["safety", "injury", "ambulance", "emergency", "medical", "hospital", "life", "first"],
    ),
    RAGChunk(
        chunk_id="chunk_03_deductible_rules",
        section="Section 3.1",
        title="Deductibles and Customer Financial Contribution",
        content=(
            "Standard policies (such as NH-8821 and NH-5502) carry a mandatory policy deductible of ₹1,500. "
            "Heavy commercial or priority fleet policies (such as NH-4019) carry a mandatory deductible of ₹2,500. "
            "The deductible is payable at the time of claim settlement or vehicle delivery. "
            "The policy coverage limit for roadside assistance is up to ₹5,000 per incident."
        ),
        keywords=["deductible", "cost", "customer", "contribution", "1500", "2500", "5000", "limit", "nh-8821", "nh-4019"],
    ),
    RAGChunk(
        chunk_id="chunk_04_non_waiver_clause",
        section="Section 4.2",
        title="Mandatory Statutory Non-Waiver Invariant",
        content=(
            "Under Section 4.2 of the NH48 Corridor General Insurance Policy, telephone representatives, "
            "call-center agents, and automated voice systems possess strictly NO authority to waive, "
            "discount, reduce, or modify mandatory policy deductibles or liability proportions under any "
            "circumstances, including emergency breakdown or caller emotional distress. "
            "Any oral promise or representation of fee waiver is legally void ab initio."
        ),
        keywords=["waiver", "waive", "non-waiver", "discount", "free", "authority", "section 4.2", "mandatory", "zero"],
    ),
    RAGChunk(
        chunk_id="chunk_05_partner_towing_rates",
        section="Section 5.1",
        title="Partner Towing Rate Card and Coverage Radius",
        content=(
            "Partner towing covers flatbed and wheel-lift towing up to a 50 km radius to the nearest "
            "authorized corridor service garage. Tows within the 50 km radius are covered under the policy "
            "(subject to the standard deductible). Excess towing distance beyond 50 km is billed to the policyholder "
            "at the agreed corridor partner rate of ₹80 per kilometer."
        ),
        keywords=["towing", "flatbed", "wheel-lift", "50 km", "radius", "garage", "excess", "80", "rate", "distance"],
    ),
    RAGChunk(
        chunk_id="chunk_06_corridor_etas",
        section="Section 5.2",
        title="Corridor Dispatch ETAs",
        content=(
            "Guaranteed dispatch ETAs along NH48: Gurugram/IFFCO Chowk: 15-20 minutes; "
            "Manesar IMT / Toll Plaza: 20-25 minutes; Dharuhera / Bilaspur: 25-35 minutes; "
            "Neemrana Industrial Zone: 30-40 minutes; Kotputli / Paota: 35-45 minutes; "
            "Shahpura / Jaipur Northern Bypass: 40-50 minutes. Roadside mechanics carry battery jump-start "
            "and tire repair kits."
        ),
        keywords=["eta", "time", "arrival", "manesar", "dharuhera", "neemrana", "kotputli", "jaipur", "minutes"],
    ),
    RAGChunk(
        chunk_id="chunk_07_revocation_sop",
        section="Section 6.1",
        title="Dispatch Staging and Revocation Protocol",
        content=(
            "All service dispatches initially enter a staged held status. If a caller notifies that the vehicle "
            "has restarted, a friend or relative has arrived, or assistance is no longer required, the dispatch "
            "action is immediately aborted without cancellation penalty to the customer. "
            "The initial claim intimation remains active under status OPEN_UNASSIGNED for 48 hours."
        ),
        keywords=["revocation", "cancel", "staging", "held", "abort", "restart", "friend", "cousin", "penalty"],
    ),
    RAGChunk(
        chunk_id="chunk_08_exclusions",
        section="Section 7.1",
        title="Standard Exclusions",
        content=(
            "Roadside coverage does not apply if: (a) driver is under the influence of alcohol or narcotics; "
            "(b) vehicle is being used for illegal motor racing or commercial transit without permit; "
            "(c) recovery was undertaken by an unverified third-party crane without prior claim intimation."
        ),
        keywords=["exclusion", "alcohol", "narcotics", "illegal", "crane", "unverified"],
    ),
]
