# 05 — Pilot comparison, full-paper review, and handoff

## The first-draft comparison differs from rebuilding

There may be no previous manuscript. Compare against two things separately:

1. **Source propositions and artifacts:** Did the draft preserve facts, uncertainty, negative findings, and the author’s intended scope without inventing details?
2. **Same-function exemplar passages/displays:** Did the draft implement specific useful presentation choices, and which gaps remain?

Do not manufacture a bad “before” manuscript and use its defeat as evidence of skill effectiveness. Literal translation of notes can illustrate a failure mode only when clearly labeled; it is not automatically a fair baseline.

## Calibrate a real pilot

Choose a small representative sample supported by the materials. Draft actual paragraphs and captions and produce/reuse actual display files. A request for a figure requires a real available figure or honest specification, not a claim of completion attached to recommendations.

Read the selected exemplar passages or inspect the display again when needed. Record a table: `output location → intended transfer → observed remaining gap → factual constraint → concrete revision → inspection status`.

A useful critique says: “The paragraph lists all six results before stating the general pattern, so the reader must infer the comparison; move the bounded conclusion first and keep two representative contrasts plus the exception.” An unhelpful critique says: “Make this more academic, concise, and top-tier.”

Revise substance and hierarchy before cosmetic wording. When a proposed choice fails, change the information organization or reference—not merely the adjectives. Two rounds are a default resource budget, not a scientific guarantee.

In full mode, continue into the paper after internal calibration unless the user requested approval gates. In pilot-only mode, stop after delivering the pilot and comparison. Only real user feedback establishes `AUTHOR_APPROVED_WITHIN_SCOPE`.

## Full-paper passes

### Semantic fidelity

Check normalized Chinese propositions against major English assertions. Preserve “not yet,” “possibly,” “only on these datasets,” and negative results. Track additions and omissions. Confirm that intent/hypothesis/plan did not become a measured fact. A shortened paragraph must not strengthen the claim.

### Scientific and numerical scope

Check the actual task, method identity, label units, comparison protocol, sample unit, and uncertainty meaning. Reconcile numbers with their sources rather than only checking agreement between copied tables and text. Use [06-domain-guardrails](06-domain-guardrails.md) selectively.

### Reader progression

Reverse-outline the written manuscript, not only the plan. Can the reader identify the question, technical response, empirical test, result, and limit? Do successive Results subsections answer different questions? Are technical explanations connected to what is actually evaluated? Remove repetitive motivation and redundant display narration.

### Concrete reference transfer

For each selected card, locate the actual implementation. Mark `IMPLEMENTED`, `PARTIAL`, `NOT_APPLICABLE`, or `NOT_CHECKED`, with a brief reason. These are editorial observations, not a validated quality score. Do not count cards as if more cards meant better writing.

### Visual integration

Inspect actual figures and relevant rendered pages at final size when supported. Check labels, legends, units, consistency, overflow, blurred raster assets, white space, figure ordering, caption placement, and manuscript width. Mark unavailable visual checks honestly.

### Citations and venue

Verify bibliographic identity and claim support independently. Prefer primary literature and current official venue guidance. Record exact version and access date; abstract-only checks cannot support detailed claims. Keep unverified references as explicit working issues rather than fake BibTeX entries.

For a named venue/year/track, check page budget, template, anonymity, supplemental policy, citation/figure requirements, and AI-use/disclosure rules from official sources. Never invent author names, affiliations, ethics approvals, data availability, code-release links, contributions, funding, or conflicts of interest. These sections can remain explicit author-required fields in a working draft.

### Artifact execution

Compile/render only with real tools and applicable permission. Check compiler logs, undefined citations/references, missing images, and the output itself. Successful compilation alone is not visual approval, scientific validation, or submission readiness. No compiler means no claim of a compiled PDF; deliver editable sources and report `NOT_RUN`/`UNAVAILABLE`.

## Issues and bounded delivery

Classify severity by consequence (`BLOCKER`, `MAJOR`, `MINOR`) and action (`EDITORIAL`, `SOURCE_RECOVERY`, `REAGGREGATION`, `POST_HOC_ANALYSIS`, `NEW_EXPERIMENT`). An unsupported central conclusion is a blocker for that conclusion, not a reason to hide all other useful work. Make safe editorial changes and deliver the current manuscript with localized unresolved gaps.

Keep evidence, reference access, artifact completeness, and author approval as separate statuses. A complete working draft can still have disclosed missing details; it cannot be presented as submission-ready. Report exactly which files were read, values recomputed, images viewed, and outputs rendered.

## Evaluating whether this skill works

The included behavioral cases are proposed tests, not evidence that the skill works. For real evaluation, use identical frozen notes/data/figures, model/tool access, output scope, and effort budgets for a baseline workflow and this one. Compare actual artifacts blind and counterbalanced with appropriate readers when feasible. Assess factual errors separately from communication and preference. A review role played by the same model is not an independent reviewer.

## Handoff without starting over

Deliver one primary editable manuscript plus actual completed display/table assets, source registers, and a compact change/gap report. Use [the handoff template](../assets/handoff.md) when continuing or moving to another workflow.

A later `drug-property-manuscript-rebuild` run may use the new draft as its input, with the same locked evidence, cards, terminology, feedback, and raw assets. Do not automatically invoke it, duplicate all intake work, or require installation of that skill to finish this one. Explicit author changes should propagate to every affected section/display; preserve version history and never silently overwrite original research files.
