# Writing a high-value English critical review

## What differentiates a publishable review

A quality review contributes **a conceptual argument**, not just a collection of citations. It should:

1. Define a well-motivated research question or unresolved tension.
2. Present a reproducible or at least transparent literature-scope account proportionate to its review type.
3. Offer a defensible classification system with category decision rules and boundary cases.
4. Compare methods on common dimensions and explicitly distinguish incomparable evidence.
5. Identify recurrent failure modes and why prior assumptions may not hold.
6. End with a prioritized, **testable** research agenda and proposed evaluation criteria.

## Standard English conventions

- Prefer precise verbs: `reported`, `evaluated`, `associated with`, `predicted`, `supported`, `suggests`, `was not established`, `has not been prospectively validated`.
- Avoid unsupported superlatives: `best`, `state of the art`, `first`, `novel`, `significant`, `robust`, `generalizable`, unless the scope and evidence are explicit.
- Avoid “Recent studies have shown” without a date-bound, cited body of evidence.
- Use `however` for genuine logical contrast, not every second sentence.
- Use acronym first expansion (e.g., drug–target interaction [DTI]); harmonize affinity units and endpoints.
- Keep causal claims narrower than correlational observations; predictive success does not verify biophysical mechanism.
- Label predictions from pretrained weights versus observed experimental measurements.
- State modality, dataset, split and metric when reporting numeric gains.

## Useful comparative paragraph pattern

**Problem → design choice A/B → mechanism/assumption → evidence and uncertainty → boundary case → testable implication.**

Illustrative, non-factual paragraph scaffold (replace placeholders with verified evidence):

> Pairwise interaction modules differ in both the granularity of the modeled correspondence and the supervision used to constrain it [citations]. While [method family A] learns token-level alignments, [method family B] predicts atom–residue contacts under [specified definition]. Reported gains cannot be directly attributed to the interaction operator where the models also differ in pretraining data and benchmark splits [verified examples]. A decisive evaluation would hold encoders, data and training budgets constant while measuring [specified contact metric] and [downstream validation metric].

Do not copy this boilerplate into the final paper verbatim; derive prose from actual evidence.

## Outline template for a computational methods review

1. **Title** — argumentative, scoped, not universal.
2. **Abstract** — context, objective, perspective/method, conceptual contributions, major limitations, outlook.
3. **Introduction** — scientific stakes, shortcomings of previous reviews, exact novel contribution, reader roadmap.
4. **Scope and literature approach** — search and selection transparency matched to review type.
5. **Conceptual foundations** — formal task definitions; data assumptions; how performance is actually measured.
6. **Taxonomy** — category definitions, boundaries, examples.
7. **Comparative synthesis** — by central research questions, not by individual paper.
8. **Evaluation and interpretability** — evidence hierarchy, known confounders, failure analyses.
9. **Translational limits** — prospective evidence, throughput/cost, software and dataset availability.
10. **Research agenda** — falsifiable questions with experimental/benchmark designs.
11. **Conclusions, declarations, references**.

## Figure and table discipline

For each proposed exhibit provide a **caption, intended claim, source provenance, classification rule, inclusion rule, and missing data policy**. A review schematic is a conceptual model unless individually sourced. Avoid copying copyrighted figure graphics or data visualization without permission/appropriate license. Data tables should cite source rows and unit conversions; do not mix IC50, EC50, Kd and Ki as if they mean the same thing. Captions should be self-contained.

## Editorial passes

- **Logic pass**: Does each section answer the promised question? Are there bridge claims between sections?
- **Scientific pass**: Are all terms, units, assay endpoints, model roles, split definitions, and evidence levels exact?
- **Evidence pass**: Is each assertion attributable? Is any citation abstract-only? Are contradictions included?
- **Language pass**: Remove repetition, vague lead-ins, redundancy, first-person promotion and generic AI style.
- **Venue pass**: Length, abstracts, citation system, figure permissions, review article category, AI statements.
