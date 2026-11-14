# Comparative quality gates and editorial decisions

## Scientific fidelity and review craft are separate acceptance dimensions

**Source fidelity**: correct work/version/DOI; claim-source match; quantitative and domain accuracy; identifiable original vs review inference vs author proposal; fair comparability; no omitted important contrary results; genre/methods honesty.

**Review craft**: coherent and discriminating review question; meaningful section order; intellectual contribution beyond study inventory; precise taxonomy with boundary cases; reproducible comparison language; captions and tables that do actual work; clear visual and paragraph-level information flow.

An improvement in prose or page design cannot offset a false source claim. A perfect citation ledger alone does not make a critical review readable.

## Pilot and full output review record

For each substantial unit, record:

```text
Output location (section/paragraph or figure/table):
Old-draft defect (location, example):
Same-function exemplar transfer card (if actually read):
Rebuilt text / rendered display evidence:
Source and inference checks actually completed:
Changed claim strength or corrected source identity:
Reader task: what should they now distinguish?
Remaining defect (specific and feasible):
Decision: KEEP / REVISE / REVERT / BLOCKED
Reviewer provenance: internal / author / independent human (only if true)
```

Readers should be able to answer one concrete question: “What are the methods' real differences and under which conditions can their evidence be compared?” A paragraph that requires chasing six citations just to learn the main distinction needs reorganization.

## Quality gates

| Gate | Evidence required | Don't count as completion |
|---|---|---|
| Genre | Documented genre and claims compatible with available search/screening records | Calling the paper systematic in its title |
| Core sources | Accessible original evidence for pivotal arguments and a list of unverified items | A valid-looking DOI or abstract alone |
| Taxonomy | Operational criteria, mixed/boundary cases, proposed status | Pretty colored boxes with unclear classification |
| Comparability | Explicit task/data/split/input/evaluation conditions for cross-study superiority claims | Merely placing scores in adjacent columns |
| Critical synthesis | Actual statements about contrasts, contradictions, limits and decisions | Listing more papers |
| Figures/tables | Editable source, consistent underlying evidence, rendered inspection where available | A successful SVG/PDF export alone |
| References | Referenced keys resolve; author/title/DOI verified for core sources | Static BibTeX syntax lint |
| Production | Read actual export/page layout and verify requested formats | A filename appearing in the folder |
| Final report | Specific modifications + material unresolved evidence gaps + checks actually run | Unsupported “95/100; submission ready” |

## Comparative calibration

Compare original and revised spans *holding scientific content fixed unless a correction is documented*. Compare with the same rhetorical function in review exemplars, not just style prestige. Decide whether claims are clearer, citations more locally appropriate, synthesis more informative and visual relationships more interpretable. Re-evaluate facts after any rewrite.

If assessing the skill's efficacy rather than the manuscript, a true workflow A/B requires the same source set, task, available tools, time budget and output constraints. Blind, counterbalanced human judgment is useful if feasible. An internal same-model critique is not independent validation; success on one review does not establish universal quality.

## Discrepancy / halt policy

- `EVIDENCE_CONFLICT`: fix only if direct source evidence resolves the conflict; otherwise qualify/report.
- `TAXONOMY_FAILURE`: revise the operational rule or mark ambiguous; never relabel source content invisibly.
- `VISUAL_REVIEW_NOT_RUN`: provide editable source/description, disclose not inspected.
- `BIBLIOGRAPHY_UNVERIFIED`: do not claim publication-ready citations.
- `REVIEW_METHODS_NOT_REPRODUCIBLE`: do not fabricate systematic methods; preserve narrative or explicitly report incomplete protocol.

A `FULL` request with adequate evidence should continue through the complete output, not stop at recommendation-only stage. In `PILOT` mode stop after actual sample + comparison. A few focused iterations are useful; endless synonym substitution is not.

## Final status definitions

- `PROVISIONAL`: core source access/genre/figures insufficient for full checks, or major unsupported material remains.
- `EVIDENCE_CHECKED_DRAFT`: specified high-priority claims verified to the scope recorded; NOT all literature automatically checked.
- `AUTHOR_REVIEWED`: the user actually reviewed/approved specified draft choices; no implied independent scientific validation.

Avoid fabricated grading, post-hoc “compliance certificates,” or publication guarantees.
