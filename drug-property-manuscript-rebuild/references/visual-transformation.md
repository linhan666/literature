# Visual transformation: learn information organization, not decoration

## First distinguish four jobs

- Concept diagram: makes an idea or contrast understandable; clearly illustrative, not an empirical plot.
- Architecture diagram: describes verified computation, inputs, operations, training/inference boundaries.
- Quantitative figure: represents actual measurements with reproducible encodings.
- Table: supports precise lookup and comparisons under explicitly stated regimes.

A single artwork need not do all four jobs. Do not add panels because an exemplar has panels. One well-designed panel can be the right result.

## Build a display specification from evidence

For every display record the reader's question, a bounded takeaway, source data/code, retained adverse evidence, major objects, relationships, information hierarchy, final-width assumption, caption duties, and editable output format. Cite the transfer card that motivates a choice, or mark it as a local design proposal.

For architecture, verify the edge list and the meaning of each operation before drawing. Current source code does not by itself establish historical run configuration. Avoid unsupported dimensions, freezing claims, conventional-attention substitutions, or invented chemical contacts.

## Design the reading path

Use reference images to examine which information is primary, secondary, and deferred. Ask which operation deserves the most area. Give standard peripheral stages enough context without drowning the distinctive operation. Expanded views, alignment links, and repeated symbols should explain a relationship, not merely add visual complexity.

Use meaningful visual objects when they clarify the actual computation: graphs for graph inputs, token strips for token sequences, aligned entities for real alignment, and a clearly specified interaction representation for an actual interaction. Do not use an attention heatmap to imply physical contacts. Rectangles are acceptable for abstraction, but a list of named rectangles is not enough when the central operation remains unexplained.

Choose direction, grouping, spacing, line conventions, type hierarchy, and color semantics coherently. Do not impose a universal 16:9 canvas. Size for the actual manuscript slot. Original arrangements are required; do not trace a published composition and substitute labels.

Before polishing, consider two information organizations when the key design is unresolved. Keep the scientific content the same. Select on explanatory function, not on which has more decoration.

## Quantitative figures

Use authoritative results and saved plotting inputs/code. Choose the plot according to the comparison: complete scores, paired changes, error distributions, or measured tradeoffs. A delta display can explain an ablation while a table retains full values; it cannot conceal contrary results. Do not replace required lookup information with a decorative chart.

Do not invent curves from AUCs, distributions from means, or error bars without a defined source. Distinguish seed, fold, molecule, target, and scaffold uncertainty. Preserve units, scales, metric direction, and sample identity. Keep comparable scales comparable. Avoid misleading area, 3D effects, and undisclosed axis changes.

Color is not the only encoding: provide suitable labels, line styles, markers, or grouping. Inspect readability at the intended size. An original, well-formed SVG is not necessarily a well-designed scientific figure.

## Tables

Choose rows and columns according to the comparison the reader must make. Group by actual regime or model family only when this clarifies interpretation. Show units, metric direction, split or population, uncertainty definition, and missing-value semantics. Use a table note for shared details instead of repeating long text in every cell.

Balance scanability and detail. Align numbers, apply sensible precision, and keep comparable columns adjacent. Bold values only within genuinely comparable groups under a stated rule. Do not average incomparable metrics or hide unfavorable datasets to simplify a table. Sparse rules are a presentation option, not proof of quality.

## Captions and page integration

A caption should identify what is shown, explain symbols/panels and relevant conditions, and support an appropriately bounded takeaway. Statistical details must remain findable, but do not duplicate an entire Methods section. The associated paragraph interprets the important finding instead of narrating every visual object or cell.

Inspect the rendered figure/table with its actual caption and nearby text. Check clipping, crowded labels, tiny legends, whitespace, consistent notation, float placement, and whether page-level reading order works. Assess the visual at its true size, not only as a zoomed screenshot.

Record both semantic changes and appearance changes. “Reduced crossing arrows and expanded the verified alignment operation” is actionable; “made it look Nature-style” is not.

## Tool and verification limits

Use only available, authorized tools. Prefer reproducible numeric figures and editable scientific diagrams. Image generation may assist authorized conceptual artwork; it is not an authority for model facts or data. Disclose raster-only output. Never claim to have rendered or viewed a file that was not rendered or viewed.

When no visual inspection is possible, deliver the editable specification/source and set `VISUAL_REVIEW_NOT_RUN`. Do not pass a visual-quality gate using only source-code lint.
