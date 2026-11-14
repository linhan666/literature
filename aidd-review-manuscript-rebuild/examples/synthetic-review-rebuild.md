# Synthetic worked example — NOT real literature evidence

All labels, citations, studies, and reported comparisons below are fictional schematic placeholders. **Never include Study-A, Study-B, or the described results in an actual manuscript.** This example illustrates review-architecture improvement only.

## Input diagnosis: a descriptive catalog

> Study-A used a drug–protein attention matrix. Study-B used a different attention layer. Study-C applied pretrained features. Several studies reported gains, showing that attention improves interaction prediction.

Problems: three paper summaries do not define what is being compared; source versions/endpoints/splits are unspecified; “attention improves prediction” improperly attributes multi-variable differences to one module.

## Taxonomy repair (author-proposed, not an established standard)

Define **operation** and **evaluation** as orthogonal axes:

- Operation: does the weight pool a joint pair-feature, transfer a partner value, or reweight already encoded features? Hybrid states allowed; no operator category implied to be a biological binding mode.
- Evaluation: predictive pair labels, dependence on partner identity, agreement with contacts, or experimental mechanism. Evidence on one axis does not automatically prove another.

### Core claim table (fictional placeholders only)

| Placeholder | Source evidence that would be needed | What the review may say after checking | Unresolved |
|---|---|---|---|
| Study-A | Original Methods equation and implementation | “The published module weights joint pair-features” if equation warrants it | Whether source code matches the manuscript |
| Study-B | Original attention Q/K/V flow | “The module transfers values across modalities” if implementation warrants it | Hybrid role and training regime |
| Study-C | Exact pretrained checkpoint and evaluation | “External representation is a confounder in operator comparisons” if actual setup uses it | Comparable split/labels |

## Revised passage blueprint (not a ready-to-cite paragraph)

> The review first distinguishes **the computational role of an attention weight** from the predictive task for which it is trained. In Study-A, [verify the mechanism from the original Methods]; Study-B instead [verify the mechanism and mixed cases]. This makes the two designs comparable as *operators*, but not yet as claims of predictive superiority: [check split, pretraining and other unmatched variables]. Study-C illustrates [a source-verified representation confounder]. A matched operator-swap study, holding encoders and data constant, would test the attribution more directly.

This is **better structured**, but it is deliberately incomplete until cited originals are inspected. It demonstrates restraint instead of inventing sources.

## Figure brief

- Type: `AUTHOR-PROPOSED` two-axis matrix (operator × evaluated claim).
- Visual: rows for operator functions, columns for evidence questions, no causal arrows between axes.
- Caption qualifier: “Proposed organizational scheme; not a measured comparison or independently validated taxonomy.”
- Data-free: no sample counts, leaderboards or invented proportions.

## Comparison pass

- Reader can articulate the distinction between an operator and an evaluation claim: improved.
- Real source support: `NOT_RUN` (fictional inputs).
- Published lineage or code confirmation: `NOT_RUN`.
- Ready for inclusion in real manuscript: **NO**; real citation and methods verification required.
