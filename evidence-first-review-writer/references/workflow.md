# Review-mode selection and execution contract

## Decision matrix

| Mode | Core purpose | Method expectations | Permissible claims | Reporting guide |
| --- | --- | --- | --- | --- |
| Narrative-critical (default) | Explain how a field works, compare paradigms, challenge assumptions, propose testable agenda | Transparent, bounded search and source appraisal; no assertion of exhaustive identification | A justified, explicitly scoped synthesis; no comprehensive-exhaustiveness claim | SANRA may assist quality assessment |
| Systematic | Answer a clearly bounded question through reproducible eligibility/selection/appraisal | Pre-specified inclusion/exclusion; search platform details; dual eligibility process or disclosed limitation; report/study accounting; appropriate risk-of-bias | Findings bounded by actual searches, screened population and quality | PRISMA 2020 + PRISMA-S; domain-specific extensions when relevant |
| Scoping | Map breadth/nature of research and gaps | Defined question/context, protocol if available, systematic evidence mapping, explicit screening and extraction | Distribution, taxonomy, unexamined contexts, research gaps; not necessarily effect estimates | PRISMA-ScR; PRISMA-S where appropriate |

A systematic review is a **methodological claim**, not a synonym for thorough writing. PRISMA is a reporting guideline, not proof a study was performed well. Narrative reviews may include a transparent reproducible search yet need not claim systematic-review status. Revisions to existing published reviews require checking copyright, priority and overlap with prior reviews.

## Four goals to articulate in `review_brief.md`

1. **Question** — e.g., how explicitly learned drug–target interactions correspond to actual binding geometry.
2. **Contribution** — e.g., new 2D taxonomy (interaction representation × validation evidence) and recommendations for benchmark design.
3. **Audience** — computational pharmacology, ML methods, structural biology, interdisciplinary readers.
4. **Exclusions** — e.g., sequence-only target encoding permitted, but prohibit structure requiring verified holo geometry in one comparison group; exact scope is the author's choice.

## End-to-end stage gates

| Gate | Mandatory evidence of completion | Failure mode |
| --- | --- | --- |
| G0 Scope | Brief, type, boundaries, stated novelty | Topic too broad; review type mislabel |
| G1 Search | Executed queries, dates and platforms; record IDs | Fictional hit counts; unlogged citation chasing |
| G2 Screen | Eligibility reasons, stable IDs, duplicate map | Exclusion without reasons; report counted as study |
| G3 Extract | Citation identity, specific support, provenance locator, limitations | Abstract extrapolation; unsupported benchmark numbers |
| G4 Synthesize | Orthogonal taxonomy, comparative tables, disagreement map | List of paper summaries with no critique |
| G5 Draft | Argument-driven English sections, support markers | Generic prose, overclaims, invented citations |
| G6 Audit | Script output, human evidence checks, applicable reporting guide | Treating DOI match as scientific verification |
| G7 Release | Human-approved sources, journal style/ethics/conflicts/AI disclosure | Unverified references, mislabeled systematic review |

Never silently skip a gate: label as pending, partially completed, not applicable, or completed with artifact paths. Do not create fabricated records as if actual searches were performed.

## Screening decision conventions

Per canonical record after deduplication:

- `title_abstract_decision`: `include`, `exclude`, or `pending`.
- `full_text_decision`: `include`, `exclude`, `not_retrieved`, `pending`, `not_applicable`.
- `exclusion_reason`: required for `full_text_decision=exclude`.

The PRISMA helper counts reports and uniquely keyed studies separately. When `study_id` is missing it reports a warning; one row per record must not be presented as number of unique studies without validation.

## Research-to-draft discipline

Maintain a `claim-evidence-gap` triage:

1. **Supported** — actual text/figure/table confirms precisely scoped claim, accounting for limitations.
2. **Partially supported** — retain narrowed wording or qualification and assign a verification task.
3. **Conflicting** — report both and explain potential effect modifiers.
4. **Unsupported/unknown** — do not publish as fact; make a question/hypothesis or remove.

Explicitly seek papers contradicting the emerging consensus. Update tables and the narrative together when new papers arrive; audit stale classification after a version update.

## Academic writing workflow in practice

Draft the argument as 5–10 section claims before writing prose. Create tables/figures early to reveal empty evidence categories. Use topic sentences that answer a comparative question, not a paper-specific summary. Highlight causal mechanisms only where experiment/analysis support causality. Close each major section with conditions of validity and open tests. Use a testable future agenda: dataset, intervention, comparator, endpoint, confounders, expected failure if hypothesis wrong.
