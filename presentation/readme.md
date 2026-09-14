`claimguard-deck.html` and `claimguard-deck-offline.html` are an earlier, superseded draft — do not refer to them for info.

`claimguard-pitch.html` / `claimguard-pitch-offline.html` (+ `claimguard-pitch.pdf`) are the current deck, built to `Slides-Plan.md`. Its Slide 4 numbers are sourced from `evals/results/eval_v0_all.json` / `eval_v1_all.json` / `eval_v2_all.json` — if those files change, re-check the numbers in the deck before presenting it. `claimguard-pitch.pdf` was last exported before the 2026-09-14 honesty-fix pass (see `REMAINING_STEPS_PLAN.md`) and needs re-exporting from the current HTML.

`build_pitch.py` at the repo root is deprecated and intentionally disabled — do not run it. It used to regenerate the deck from a hardcoded string full of numbers that were never sourced from `evals/results/`, and it overwrote itself to keep doing so. See its docstring.
