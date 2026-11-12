# Changelog

## 1.1.0 — 2026-11-12

- Added a **10–12 substantive exchange default target**, with early exit and open-ended expansion permitted.
- Defined explicit **P1–P4 phase gates** with 15 qualitative coverage dimensions (`absent`, `proposed`, `examined`); P5 remains author-controlled export.
- Added **self-reported saturation heuristic** for three consecutive no-novelty rounds; it never proves academic completion.
- Added **justified +3-round extensions** for unresolved high-priority disputes or quality gates.
- Added **final author review** and strict non-automatic export instructions.
- Added `scripts/dialogue_tracker.py` with `init`, `record`, `coverage`, `issue`, `resolve`, `extend`, and `status` commands.
- Added tracker regression tests, long-form adaptive dialogue reference, updated ChatGPT/Codex starter prompts, and handoff process annotations.
- Kept the canonical `review-dialogue-handoff/v1` schema and all 14 sections for downstream compatibility.
- The deterministic tests validate code behavior only, **not** actual research quality or transcript-based user consent.

## 1.0.0 — 2026-11-11

- Initial multi-turn scientific review discussion Skill, 14-section handoff, provenance states, structural validator/exporter, prompts, and biomedical research lenses.
