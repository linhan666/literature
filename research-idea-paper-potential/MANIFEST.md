# Manifest

## Core
- `SKILL.md` — executable skill instructions and output contract.
- `.gitattributes` — keep package text files LF-normalized across platforms for stable checksums.
- `README.md` — repository overview, usage, and design basis.

## References
- `references/core-rubric.md` — 11-dimension 0–5 scoring rubric.
- `references/scoring-model.md` — Paperability and High-Quality Potential weighting.
- `references/fatal-flaws.md` — fatal-flaw and positioning gates.
- `references/agent-specific-rubric.md` — Agent necessity, Scientific autonomy, Scientific discovery value.
- `references/reviewer-attack.md` — adversarial reviewer protocol.
- `references/evidence-levels.md` — evidence and confidence labels.

## Assets
- `assets/report-template.md` — standard final report structure.
- `assets/idea-intake-template.md` — optional structured idea intake.
- `assets/evaluation-schema.json` — machine-readable score schema.

## Examples
- `examples/scientific-agent-example.md` — synthetic Scientific Agent calibration example.
- `examples/conventional-idea-example.md` — synthetic conventional research-idea example.

## Evals
- `evals/test-cases.md` — behavioral test cases.
- `evals/expected-behaviors.md` — expected and prohibited behaviors.
- `evals/sample-evaluation.json` — sample input for the scoring script.

## Scripts
- `scripts/score_idea.py` — dependency-free score calculator.

## Validation artifacts
- `evals/sample-score-output.json` — expected calculator output for the sample input.
- `FILE_CHECKSUMS.txt` — SHA-256 checksums for payload files at packaging time; the checksum file itself is excluded.
