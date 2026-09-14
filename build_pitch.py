#!/usr/bin/env python3
"""DEPRECATED — do not run this script.

This used to generate presentation/claimguard-pitch.html and
presentation/claimguard-pitch-offline.html from a hardcoded string, with
numbers that were never sourced from evals/results/*.json (an invented
"48-scenario benchmark", an invented "31%"/"~15B" quote, an invented
"₹250 CR DPDP Penalty" figure, and more). It also rewrote itself on every
run, so the fabricated content kept regenerating.

The current deck (presentation/claimguard-pitch.html and its offline
twin) has since been hand-corrected to match the real, honestly-measured
numbers in evals/results/eval_*_all.json — see docs/REMAINING_STEPS_PLAN.md
for how those numbers were produced. Running this script would silently
overwrite that correction and reintroduce fabricated statistics.

If the deck needs to be regenerated, edit presentation/claimguard-pitch.html
and presentation/claimguard-pitch-offline.html directly, following
docs/presentation/Slides-Plan.md, and re-check every number against
evals/results/*.json before publishing. Do not resurrect this script.
"""

if __name__ == "__main__":
    raise SystemExit(
        "build_pitch.py is deprecated and does nothing. "
        "See the module docstring for why, and edit the presentation/ HTML files directly instead."
    )
