**Read `DECK-CONTENT.md` for what's in the deck — never the HTML.** `claimguard-pitch.html` / `claimguard-pitch-offline.html` / `claimguard-pitch.pdf` are gitignored build outputs now, not tracked in git and not something to open to find out what the deck says. They still exist locally and are what actually gets shown to judges — just build/edit them directly, and update `DECK-CONTENT.md` to match afterward.

`Slides-Plan.md` is the original build spec (historical — written before the deck existed). `DECK-CONTENT.md` is the current, accurate record of what's actually in the built deck right now, including a "Known issues" list of things that still need fixing before presenting (a stale "~15B" model reference, an internal 48-vs-60 count mismatch, an unmeasured "5-second" timing claim, and some future-scope sectors phrased as present-tense capability).

The old `claimguard-deck.html`/`-offline.html` draft (superseded before `claimguard-pitch.*` existed) has been deleted, not just flagged — it's not coming back.

`build_pitch.py` (repo root) is deprecated and intentionally disabled — see its docstring. Do not run it.
