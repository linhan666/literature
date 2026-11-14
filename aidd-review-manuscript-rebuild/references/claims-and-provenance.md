# Claims, citations and original-source provenance

## Claim-to-source is a proposition-level link

Bibliographic existence is not support for the attached sentence. Distinguish:

1. **Identity**: is this the exact work/version intended? Record title, author, venue/preprint status, year, DOI or canonical URL, code/data version where relevant.
2. **Location**: where does the supporting evidence occur? Methods subsection, equation, figure, supplement, table, repository code lines or run artifacts; prefer stable exact locators.
3. **Assertion**: what does the original study actually say/show? Do not paraphrase beyond accessible content.
4. **Inference**: which part is the review author's interpretation, and does it follow from the evidence and its limitations?
5. **Strength**: source-reported / independently replicated / directly experimentally tested / inferred / hypothesis / unknown.

Avoid blanket “verified” labels if only metadata and abstracts were checked. Use a source-access column: `FULL_TEXT`, `SECTION_ONLY`, `ABSTRACT_ONLY`, `METADATA_ONLY`, `CODE_READ`, `NOT_ACCESSED`. A code repository alone does not show that its current version generated the paper's reported experiments.

## Minimal claim ledger (reuse existing files)

Create rows only for claims whose verification changes the article:

`claim_id | output_section | claim_text | claim_type | source_key | exact_locator | accessible_scope | support_status | discrepancy | editorial_action`

Suggested `support_status`:
- `DIRECT`: accessed original supports the bounded claim;
- `QUALIFIED`: access supports only a narrower statement;
- `CONFLICTED`: sources or versions disagree;
- `UNSUPPORTED`: accessed source does not substantiate claim;
- `UNVERIFIED`: could not check at requisite depth.

`DIRECT` does **not** mean independent scientific replication. `SOURCE_REPORTED` means what the source reports, not verified reality.

## High-priority verification

Do this before writing stronger synthesis:
- Claimed first/only/novel, “state of the art,” general superiority, real-world or mechanistic success.
- Core architecture, mathematical operation, attention/interaction semantics, trained objective, and feature provenance.
- Quantitative benefit, dataset, endpoint, drug/target split, sample size, test set, statistical uncertainty.
- Experimental confirmation vs simulation, retrospective docking vs prospective wet-lab, binding vs functional signaling.
- Technical inheritance, shared model names, distinct authors/groups or date/version ambiguities.
- Negative evidence, retractions, errata, competing results, leakage criticisms, undisclosed pretraining.
- Source-pool counts, included-study numbers, PRISMA diagram, taxonomy frequencies, if claimed.

Start with available original material; retrieve additional originals only when relevant tools and permissions allow. Ask the user only about material that cannot be retrieved and materially blocks the task; continue supported sections.

## Repair rules

- Wrong DOI / split work identity: correct only after independent bibliographic confirmation; preserve record of correction.
- A claim stronger than a source: narrow to the source's actual endpoint, unit, population and evaluation regime; or remove.
- Conflicting findings: retain disagreement, identify likely causes as hypotheses until substantiated; do not smooth over the contradiction.
- Missing primary source, but only another review cites it: use an explicitly secondary attribution *if permitted by the article* or mark unverified; do not pretend first-hand verification.
- Model-family similarities not linked by cited inheritance: use “shares a broad conceptual feature” if supported, not “was derived from.”
- Unverifiable date/order: avoid precise origin/priority assertions.
- No real evidence for a proposed framework: label `AUTHOR-PROPOSED; NOT INDEPENDENTLY VALIDATED` (or an equivalent concise author-approved formulation), not “accepted standard.”

## Review sentences that preserve provenance

- “In the authors' reported experiments, ...” (single primary source evidence).
- “Across studies meeting [explicit selection condition], the reported results suggest ...; however, ...” (bounded synthesis).
- “We use the following **operational** definition ...” (review-authored classification).
- “This comparison cannot isolate the effect of [operator] because [data/training difference].” (qualified attribution).
- “Whether [hypothesis] transfers across [condition] remains untested in the cited evidence.” (open question, not claim of universal absence).

Citations follow the specific proposition they support, not the paragraph as a decorative group. Recheck after reordering and rewriting. Do not invent unseen paper text or fill bibliographic fields based only on a plausible title.
