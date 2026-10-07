# Evidence and Confidence Levels

Use evidence labels to prevent unsupported precision.

## Evidence basis

- **E0 — Speculative:** intuition or analogy only.
- **E1 — Plausibility:** supported by basic theory or isolated examples.
- **E2 — Prior-art supported:** relevant literature/benchmarks establish the premise, but not the specific claim.
- **E3 — Direct preliminary evidence:** pilot experiments, internal benchmarks, or direct feasibility tests support the claim.
- **E4 — Independent decisive evidence:** external/prospective validation, independent replication, or equivalent high-strength confirmation.

Each major dimension should note the strongest evidence level supporting its score.

## Confidence

- **Low:** important facts unresolved; score may shift by >=2/5 after verification.
- **Moderate:** main premise is supported, but one important uncertainty remains.
- **High:** closest prior work, feasibility, and decisive tests are well characterized.

## Unknowns

Do not convert missing information into an average score by default.

Mark it as:

`Unknown -> evidence needed -> likely score range`

Example:

`Novelty: Unknown; requires a targeted search of 2024–2026 autonomous molecular-design agents. Likely 2–4/5 depending on whether adaptive reward construction has already been demonstrated.`
