# Review genre, scope and methodological truthfulness

## Diagnose by actual conduct, not the title

| Genre | Central promise | Legitimate reconstruction | Do not imply without evidence |
|---|---|---|---|
| Narrative-critical review | Selective but transparent argument and critical integration of literature | Strong thesis, disclosed scope/selection logic, comparisons, contradictions, practical implications | Exhaustive literature coverage, preregistered inclusion, formal risk-of-bias assessment, complete PRISMA flow |
| Technical survey | Operational mapping/comparison of methods and implementation choices | Definitional precision, architecture/evidence tables, source-version/code distinctions, evaluation taxonomy | Code inspections or benchmark reruns not conducted; universal ranking across datasets |
| Scoping review | Map the extent, characteristics, and gaps of a defined evidence corpus | Clarify PCC/questions, eligibility, sources, screening, extraction/charting, reporting per applicable PRISMA-ScR items | Full eligibility screening, totals or reviewer independence without actual logs |
| Systematic review | Reproducible, pre-specified or transparently documented methodology to answer a focused question | Improve methods reporting, evidence synthesis, risk-of-bias accounts, PRISMA 2020 / PRISMA-S matching where applicable | Protocol registration, search dates, deduplication, double screening, bias ratings or meta-analysis invented after writing |
| Perspective / conceptual review | Defended position, future agenda, or framework | Distinguish established evidence, inference and proposal; label speculative diagrams | Claim opinion/taxonomy is consensus or independently validated |
| Hybrid | Distinct components of the above that were actually carried out | Identify which sections have which evidence standard | Apply one genre's methodological badge to the whole paper without justification |

**Select actual genre before rebuilding the abstract.** If genre is internally inconsistent, preserve substantive intent, revise label conservatively, and document the rationale. An author's “systematic overview” phrase does not prove a systematic review was conducted. Don't downgrade real completed systematic work merely to avoid checking it.

## Genre-specific checklists, correctly scoped

- **Narrative / narrative-critical**: SANRA (Baethge et al., 2019) is a six-item narrative-review appraisal scale covering importance/aims, literature search, references, scientific reasoning, and relevant endpoint data. It does **not** certify a review or replace text/figure evaluation. Use qualitatively if helpful; no made-up score.
- **Systematic**: PRISMA 2020 governs reporting items for systematic reviews, including search/screen/synthesis transparency. It does **not** make an undocumented literature search real. Apply only to the review steps actually executed; list absent ones.
- **Scoping**: PRISMA-ScR provides a reporting extension for scoping reviews; use when this genre and its conduct are evidenced.
- **Search reporting**: PRISMA-S adds detail for method-driven literature searches; use when the review includes such a search, never as a basis for invented strategies or counts.
- **Technical surveys**: no single default PRISMA claim. Verify source methods, exact computational operations, tasks, benchmark regimes, and independence of evidence.

Journal instructions are a separate constraint: get target journal/year instructions if actually specified and available. Keep abstract types, word limits and citation formats conditional otherwise.

## Core scope questions

Write a compact contract, not a speculative systematic protocol:

1. What *question* is this review trying to answer, and for whom?
2. Which AIDD domains and output types are **in** and **out** (e.g. small-molecule vs peptides, sequence vs 3D, property prediction vs binding vs functional response)?
3. Is the contribution a **taxonomy**, an **evidence-based comparison**, a **historical map**, a **critical interpretation**, or a **proposal**? Multiple roles are acceptable, but distinguish them.
4. Is the literature survey selective, comprehensive, searched systematically, or uncertain? What provenance proves the description?
5. Which decisions have already been explicitly approved by the author and should not be silently overwritten?
6. Which caveats (study period, model versions, available modalities, datasets) must follow claims throughout the text?

## Frequent genre errors

- “We systematically screened 184 studies” when only a list of citations is available → remove or mark as unsubstantiated; do not create a fake flow diagram.
- “The first comprehensive review” without a defensible defined scope and recent landscape check → avoid unsupported priority claims.
- Describing every paper chronologically → reconstruct by conceptual question; chronology only for source-documented evolutions.
- One large Methods section in a narrative review imitating an original computational paper → adapt to review function; don't force IMRaD.
- Treating review-classification counts as research prevalence when extraction was incomplete → state selection bounds or avoid charting prevalence.

## References

- SANRA: https://doi.org/10.1186/s41073-019-0064-8
- PRISMA 2020: https://www.prisma-statement.org/prisma-2020
- PRISMA-ScR: https://www.prisma-statement.org/scoping
- PRISMA-S: https://www.prisma-statement.org/prisma-search

These are reporting/appraisal resources, not proof that any specific manuscript followed them.
