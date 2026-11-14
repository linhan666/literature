# Figures and tables for AIDD reviews: conceptual clarity + provenance

## Select displays by scientific reader task

For every display, specify:
`figure/table ID → question → evidence or author-proposed basis → units/objects → encoding → exact sources → key distinction → legend caveat → output formats`.

Use figures to express *relations*, tables to support comparative retrieval. Neither should reproduce the text in boxes. Keep editable vector/source files where possible (SVG, PPTX, draw.io, Mermaid, TikZ, reproducible plotting script), with exported PDF/PNG only when actually produced. Use the author's venue requirements for size/resolution/fonts when known.

## Useful display families

| Display | What it can legitimately show | Essential constraint |
|---|---|---|
| Taxonomy / ontology | Operational categories, orthogonal axes, composite systems, boundary cases | Label proposed frameworks; explain multi-label coding, do not imply natural biological divisions |
| Method-mechanism schematic | Verified computations, inputs, attention/value flow, training or inference conditions | Cite original architecture; arrows must match actual operation, not conjectured mechanism |
| Comparison matrix | Methods × representation/operation/data/endpoint/split/evidence/limitations | Separate evidence from inference and unavailable metadata; no universal ranks without matching settings |
| Evidence/evaluation framework | Distinct prediction, cross-modal dependence, attribution, structural or functional validation claims | Avoid false sequential certification or one proxy as proof of another |
| Technology evolution / timeline | Verified release chronology, direct extensions, combinations and concurrent branches | Date source and type of edge; no invented inheritance from proximity or shared label |
| Research decision flow | Conditional selection criteria and failure modes | Mark author-proposed decision logic, not an externally validated clinical algorithm |
| Evidence map / counts | Extracted studies by established operational categories | Only with a documented denominator, deduplication and coding process; uncertainty/coverage limits |

A **3-panel proposed taxonomy** can be as valuable as an architecture figure, but do not call it experimentally validated. A **quantitative superiority plot** drawn from incommensurable published studies is misleading even when visually polished.

## Source and author-proposal encoding

Use explicit cues that survive grayscale printing:
- `SOURCE-REPORTED` for content taken from verified originals (with citation in caption/table note).
- `REVIEW SYNTHESIS` for combined interpretation based on named evidence.
- `AUTHOR-PROPOSED / HYPOTHESIS` for new conceptual mappings, dashed inference edges and untested relationships.
- `UNCERTAIN / NOT VERIFIED` for disputed edges or unknown version relationships; omit if no visual justification.

Avoid visually identical solid arrows for a verified data flow and a speculative technical inheritance. Don't fabricate confidence scores, performance delta bars, category proportions or a PRISMA flow. Never use a source's actual chart/layout as an unlicensed tracing template.

## Conceptual diagram composition

- Put the **claim** in the visual title/caption, not “An overview of models.”
- Use at most one primary semantic job per panel; panels may use A/B/C with a shared legend.
- Align the logical direction of edges and distinguish *conditional input*, *operation*, *evidence* and *output*.
- Include atom/residue/token labels only if scientifically correct. Mechanisms like attention scores, attention-weighted values, pairwise feature pooling and physical contacts should not be collapsed into the same arrow.
- Use readable English labels at final column width; light background, restrained colors, non-color encodings, sufficient contrast and purposeful whitespace.
- Show negative or uncertain relationships if central to the review. Do not “repair” conceptual ambiguity with decorative molecule icons.

**Example constraint:** a line from `Method A` to `Method B` in a timeline is a claim of relation. Use it only when an original source demonstrates derivative code/model use; otherwise place them on parallel tracks without an edge.

## Table methodology

- Decide the row unit: paper vs method implementation vs experiment vs dataset; do not silently mix.
- Use columns that directly adjudicate comparison conditions. For example: `Method / interaction role / input modality / endpoint / split + dataset version / supervision / evidence type / primary source / caveat`.
- Explicitly distinguish `NOT_REPORTED`, `NOT_APPLICABLE`, `NOT_CHECKED`, and true negative evidence. Do not use a blank cell for all four.
- Do not average unrelated AUROC, RMSE, affinity, RMSD and hit-rate scores. Put measured cross-study values only within a table where common protocols can be demonstrated, or show them descriptively with a strong non-comparability note.
- Document denominators/selection if reporting percentages or method frequencies. Avoid score heatmaps if color magnifies illusory rankings.
- Use consistent chemical units, split conventions, terminology and reference keys. If an entry combines methods, mark it as hybrid instead of arbitrarily assigning to one class.

## Captions and production review

A meaningful caption contains:
1. What the object depicts and the comparison question.
2. Meaning of shapes, colors, arrows, confidence/edge types and panel labels.
3. Whether it is an author-proposed scheme, source-reported facts, or evidence-based synthesis.
4. Specific citations or source mapping for external methodological content.
5. Qualification that prevents a misleading inference (e.g. *schematic, not to scale* or *not a performance comparison*).

View the actual exported figure and the page where it is placed, including captions. Evaluate label clipping, small type, broken arrows, unexpected wraps, alignment, table width, monochrome readability, and text–display redundancy. If no renderer/vision is available set `VISUAL_REVIEW_NOT_RUN`, not “publication-ready.”

## Figure brief template

`assets/figure-brief-template.md` gives a short reproducible brief. Produce actual files when requested, not only a drawing prompt. Image generation may supply authorized conceptual art but must not be used as evidence of a numerical or structural truth. Verify scientific labels and redraw precise figures using structured/vector tools where feasible.
