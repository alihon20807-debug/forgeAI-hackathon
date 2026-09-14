# ForgeAI Hackathon — Project Notes for Anyone (Human or Agent) Working Here

## Canonical plan
`Overall-plan.md` at the repo root is the sole, authoritative project plan. There is no other plan file — an earlier draft (`PLAN.md`) was folded into it and deleted; don't recreate a second plan document.

## PRISM is the central highlight — not a bolted-on feature
This project exists to demo PRISM, using ClaimGuard as the vehicle, not the other way round. 40% of the judging rubric (PRISM Evaluation & Diagnosis + Measured AI Improvement) is directly PRISM-dependent. Every future edit to the plan, the deck, or the pitch should keep PRISM load-bearing and visible throughout — in the architecture, the evaluation loop, and the demo — not confined to one slide or one paragraph.

## Language framing rule for presentation materials
Written pitch materials (slides, docs, one-pagers) must be **primarily in English**. Frame the product's multilingual capability as **native-language support** in general (Hindi and other Indian languages), not as "Hinglish."

Hinglish reads as unprofessional in written pitch material. Use it sparingly: **one illustrative example call transcript**, clearly marked as an example, not the framing device for the whole pitch. The spoken live demo can still be a natural code-mixed call — that's realistic — but headings, bullets, and narration text stay in clean English.

## Process rule
Do not turn a plan into a built deliverable (deck, code, submission) without the user explicitly confirming that specific plan first. "We discussed this earlier" is not confirmation.

## Documentation policy — architecture and implementation notes live in markdown
Project architecture, implementation notes, and "what's actually built" status must be written down in markdown files, not left implicit in code or in a built HTML deck. A built artifact (`presentation/claimguard-pitch.html` and its offline twin, or any future rendered output) is a publish target, not a source of project information — do not read it to figure out what the project does or what's decided. Read `Overall-plan.md` (and other project markdown, e.g. `REMAINING_STEPS_PLAN.md`, `HANDOVER.md`) instead. If a fact needed for future work isn't captured in markdown yet, write it down in a focused new markdown file (e.g. `architecture.md`) rather than re-deriving it from code or HTML on every future pass — this is meant to be a one-time investment, not repeated effort each session.
