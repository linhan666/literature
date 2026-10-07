# Scoring Model

Use dimension scores from **0 to 5**.

For a dimension with score `s` and weight `w`:

`weighted contribution = (s / 5) * w`

Report scores to one decimal place. Scores are decision aids, not substitutes for reasoning.

## Paperability Score /100

This score emphasizes whether the idea can become a **defensible research paper**.

| Dimension | Weight |
|---|---:|
| Problem importance | 8 |
| Knowledge gap authenticity and clarity | 10 |
| Novelty | 8 |
| Scientific claim strength and falsifiability | 14 |
| Mechanistic or conceptual insight | 6 |
| Evidence strength and claim-evidence alignment | 15 |
| Alternative-explanation discrimination and controls | 12 |
| Generalizability / external validity | 5 |
| Feasibility | 14 |
| Reproducibility / robustness | 6 |
| Narrative coherence / contribution clarity | 2 |
| **Total** | **100** |

Suggested interpretation before fatal-flaw overrides:

- **<50** — not ready as a research project/paper.
- **50–59** — research-shaped but weak or under-specified.
- **60–69** — plausible paper candidate with significant risks.
- **70–79** — defensible research-paper potential.
- **80–89** — strong paper candidate.
- **90–100** — unusually mature and well-supported; re-check calibration and novelty claims.

## High-Quality Potential Score /100

This score estimates the **scientific ceiling if executed well**.

| Dimension | Weight |
|---|---:|
| Problem importance | 15 |
| Knowledge gap authenticity and clarity | 10 |
| Novelty | 15 |
| Scientific claim strength and falsifiability | 12 |
| Mechanistic or conceptual insight | 12 |
| Evidence strength and claim-evidence alignment | 12 |
| Alternative-explanation discrimination and controls | 8 |
| Generalizability / external validity | 10 |
| Feasibility | 3 |
| Reproducibility / robustness | 2 |
| Narrative coherence / contribution clarity | 1 |
| **Total** | **100** |

Suggested interpretation:

- **<50** — low quality ceiling even if completed.
- **50–64** — likely incremental or niche contribution.
- **65–74** — credible solid-paper ceiling.
- **75–84** — strong high-quality-paper potential.
- **85–92** — very high potential if the evidence survives reviewer attack.
- **>92** — exceptional on paper; aggressively verify prior art, feasibility, and overclaiming.

## Important rule: fatal flaws override scores

A score of 82 does not imply Go if the central claim cannot be tested or the novelty claim is already invalidated by prior work.

Always report:

1. numeric score;
2. confidence in the score;
3. fatal flaws or gates;
4. the strongest reason the score could be wrong.

## Confidence

Use:
- **Low** — mostly idea-level reasoning; important facts unverified.
- **Moderate** — some literature/prior-art or pilot evidence verified.
- **High** — closest prior work, feasibility, and decisive evidence path are well established.

Do not use score precision to imply evidence precision.
