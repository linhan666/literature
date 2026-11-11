# Critical reasoning, taxonomy and novelty checks

## Unit of analysis before categorization

Do not classify a model family until the unit is defined. Separate:

- **Scientific phenomenon:** what is being explained (e.g. binding, efficacy, conformational change).
- **Task:** classification, regression, retrieval, ranking, co-folding, conditional generation, etc.
- **Input representation:** sequence, graph, 3D, residue contact map, assay metadata.
- **Interaction mechanism:** concatenation, dot-product attention, co-attention, bilinear maps, tensor products, equivariant message passing.
- **Learning signal:** affinity labels, contact supervision, docking/structure targets, distillation, self-supervision, contrastive.
- **Predicted output:** scalar activity, affinity, contact probability, pose, state, novel molecule.
- **Evidence of validity:** metric, benchmark split, external set, perturbation, contact precision, causal test, calibration.

An apparently plausible taxonomy may blend elements from these layers. Say explicitly when they are *orthogonal facets* rather than sibling classes.

## Taxonomy tests

1. **Definitional clarity** — each proposed category has an inclusion rule and a nearest excluded example.
2. **Same-level test** — categories on a single branch share the same ontological layer.
3. **Coverage test** — important examples that cannot be placed should be listed; do not force-fit them.
4. **Overlap test** — nonexclusive categories are permitted when their intersections are explicit and useful.
5. **Granularity test** — a parent category is not listed as a sibling of its child unless scope is redefined.
6. **Empirical discriminability** — a reader can decide membership from model methods; avoid categories based solely on intended results.
7. **Counterfactual stress test** — what single proposed method would break the taxonomy?
8. **Dependency test** — identify categories whose existence depends on unverified assumptions.

Prefer multi-axis charts, facet tables or layered schematics over one giant mutually exclusive hierarchy when methods intentionally combine modules.

## Criticism with alternatives

Every significant critique should carry:

1. A precise target statement or assumption.
2. Why it may fail (definition, leakage, causality, selection bias, confounder, unsupported generalization).
3. A counterexample or thought experiment **identified as such** (never fabricated empirical result).
4. A repair (narrow the claim, separate dimensions, design an experiment, look for counterevidence).
5. A verification task and what evidence would settle it.

Do not critique for its own sake. If a user favors an approach and it is robust, explain why; do not force an adversarial stance where the evidence does not warrant it.

## Scientific novelty: five levels

- **Coverage** — newer literature or an underreviewed subdomain.
- **Organization** — a genuinely useful reclassification with explicit rules.
- **Comparison** — a fair, previously missing contrast of assumptions, datasets, evaluation, tradeoffs.
- **Interpretation** — synthesis that explains contradictory results or conditions of success/failure.
- **Agenda** — a falsifiable research program, evaluation protocol, benchmark proposal, or decision framework.

Never label any of these `novel/first/comprehensive` without comparing the most relevant previous reviews using real evidence. In the dialogue call it **candidate contribution** and list competing reviews to search for.

## Logic for a conceptual narrative review

Instead of `Method A — Method B — Method C`, prefer:

- Which scientific question is worth answering, and why now?
- Which assumptions distinguish candidate paradigms?
- Which constraints determine when each works?
- What published evidence **would be needed** to validate the comparison?
- What literature contradictions and failure modes should be investigated?
- Which evidence-backed (not merely speculative) conclusion can ultimately be drawn?

Generate an outline in argument statements, not a list of tool names. Proposed figure/table captions should answer a clear question.

## Red-team questions

- Are we confusing model predictive relevance with physical mechanism?
- Does a high AUROC demonstrate generalization across unseen targets?
- Is a latent attention map equivalent to verified ligand–residue contacts?
- Are a docking score and calibrated affinity estimate equivalent endpoints?
- Does an assay labeled “agonist” reveal biased signaling pathway or only one observed phenotype?
- Is synthetic accessibility score equivalent to a demonstrable building-block/reaction route?
- Is two models' reported SOTA comparable if their datasets, splits and baselines differ?

These are examples of **questions**, not claims about any particular paper. Do not presume a user's review is biomedical AI; for other domains generalize the tests.

## Evidence backlog construction

Mark candidate assertions as:

- `CONCEPTUAL_PROPOSAL` — author's framework, not bibliographic fact.
- `CHECK_EXISTENCE` — named paper/model/database may be real but has not been validated.
- `CHECK_METHOD` — need Methods section evidence for how approach works.
- `CHECK_RESULT` — need Results/Table/benchmark and conditions.
- `CHECK_CONTRADICTION` — find counterexamples/negative studies.
- `CHECK_NOVELTY` — search earlier reviews/frameworks.
- `CHECK_COMPARABILITY` — verify dataset, label, split, comparator, metric, compute.

Prioritize by importance to central thesis, risk of being wrong, and influence on outline. Do not manufacture precise search hit counts or citations.
