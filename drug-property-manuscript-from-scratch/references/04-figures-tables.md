# 04 — Existing images, quantitative figures, tables, and captions

## Start from what is supplied

An existing figure is an input asset, not a requirement to redraw. Inspect its actual pixels or rendered vector output together with its caption and any associated data/code. Record path/version, author/source, display type, available editable source/raw values, legibility, purpose, and supported claims. Do not overwrite it.

Use [the figure register](../assets/figure-register.csv) or a compact table. Assign a substantive decision: `REUSE`, `RECAPTION`, `REFORMAT_FROM_SOURCE`, `REDRAW_FROM_DATA`, `REDESIGN_FROM_VERIFIED_SPEC`, `MOVE_TO_SUPPLEMENT`, or `UNRESOLVED`. Explain any removal; never remove unfavorable evidence simply to simplify the story.

## Capabilities and provenance matrix

| Available material | Permitted work | Do not claim |
|---|---|---|
| Plot script + identified input data | Reproduce/redesign within authorization; retain script, inputs, exports | That reproduction proves scientific validity |
| Exact summary table only | Create a comparison table or compatible summary plot | Individual predictions, curves, or unreported variation |
| Readable plot image with labeled values | Reuse; transcribe exact printed values with `IMAGE_READ` status; improve caption | Raw-data validation, hidden precision, or reconstructed replicates |
| Plot with unlabeled marks only | Describe clearly visible qualitative patterns with limitations; recover data if possible | Exact bar heights/curve coordinates as authoritative values |
| Editable architecture plus method sources | Check components/edges and redesign hierarchy | That the drawing itself proves the model was trained |
| Architecture image only | Reuse as an author-supplied schematic; describe visible high-level flow conditionally | Hidden loss, checkpoint, tensor dimensions, trainability, or implementation |
| Scientific image such as assay or microscopy | Preserve scientific content; describe the supplied measurement context | Pixel retouching or altered evidence to improve the paper |
| No available vision/rendering | Deliver editable source or faithful asset reuse; mark review unavailable | Having seen the figure or verified its visual quality |

A bitmap embedded in SVG/PDF is still raster content, not fully editable vector artwork. Do not label a raster export as a vector source. Do not upscale or vectorize an image and claim new scientific detail. Curve digitization, when specifically authorized, is approximate recovered data with error and provenance, not the original experiment; it is not the default path.

## Build a visual argument

For each display decide: reader question; one main observation or technical message; source/evidence IDs; main-text or supplement role; unique information beyond prose/other displays; required caption facts; and final reading size. Reorder according to the paper’s argument rather than file numbering or the author’s experiment chronology.

Learn role-matched visual decisions from actual exemplar pages through transfer cards. A figure count, color palette, 16:9 canvas, or “Nature-like” appearance is not a specification. A single-column or multi-panel design must fit the actual content and venue, not an assumed layout.

## Architecture and conceptual diagrams

Build a component/edge specification from verified method descriptions or actual code as available. Identify inputs/outputs, operations, model branches, training-only paths, and optional parts. If the supplied method is author-reported, retain that evidence level.

Allocate space according to explanatory importance. A standard encoder can be compact; a claimed new interaction often needs more than a label. Use a local expansion only when its operations are known. Do not turn alternative heads into simultaneous outputs, parallel experiments into sequential upgrades, or a custom interaction block into conventional attention.

For a requested redesign, use an appropriate editable source such as SVG, draw.io, or TikZ/Graphviz where supported. Maintain clear edge semantics and stable notation. Inspect source and rendered output. Image generation, when explicitly authorized and available, may assist conceptual art, but cannot authenticate exact architecture or replace numerical plotting. Do not send unpublished structure or results to an external service without permission.

## Quantitative figures

Use real data and saved, reproducible plotting code; obey the host’s plotting requirements. Identify the exact input table, transformations, metric/class/split, and command. Preserve meaningful uncertainty, missing values, and unfavorable cases. Export vector or raster formats suitable for the verified venue; retain an inspectable preview.

ROC/PR curves require suitable underlying labels/scores or a faithfully reused existing curve—not one aggregate AUC. Error bars require their real definition and supporting values; do not estimate SD from a mean, infer n from the number of bars, or label bootstrap test uncertainty as retraining variability.

Use consistent axes for comparable panels, disclose transformations/truncation, and avoid misleading area encodings or decorative 3-D effects. Bars normally need a zero baseline; exceptions require explicit justification. Ensure accessible distinctions through markers/line styles as well as color. Inspect at actual final reading size, not only enlarged on screen.

## Tables

Build from identified values with metric direction, units, evaluation context, baseline provenance, aggregation/uncertainty, and missing-value meanings. Preserve original precision internally; display sensible precision. Literature-reported results under different protocols belong in clearly separated contexts, not an unqualified common ranking.

Group rows/columns by the scientific comparison. Avoid bolding incomparable values. Boldface is a ranking convention, not significance. Preserve footnotes needed to interpret frozen features, additional pretraining, or incomparable splits. Do not duplicate an entire main table as a bar chart unless the second representation answers a different question.

## Captions and integration

Write actual captions. Include what is shown, panel/legend meanings, task/dataset/split when known, metric/unit/direction, comparison basis, and uncertainty/n definitions when applicable. Explain a bounded takeaway without inventing missing methods. Localize unknown essential items in working markers.

Place text references at the point where a display answers a question. Prose should explain the comparison, not read every label aloud. Captions should be sufficiently self-contained but cannot rescue an incomprehensible layout or carry essential unsupported science. Synchronize numbers and terminology across caption, table, plot, Results, and Abstract.

For each artifact, report separately whether data were available, source was editable, redraw was executed, render was inspected, and claims were source-matched. A readable reused image can be useful even when raw data are unavailable; disclose that limitation rather than forcing a fake redraw.
