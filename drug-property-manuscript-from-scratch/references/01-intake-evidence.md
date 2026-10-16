# 01 — Recovering a study from notes, intent, and artifacts

## Read before writing

Establish the authorized workspace, active project, and requested output. Prefer the actual files to filenames or memories of another study. Read complete relevant notes rather than disconnected retrieved snippets. Inspect tables with headers, footnotes, sheets, and unit definitions; inspect figures at readable resolution. Follow host-specific handling instructions. Search locally before asking for information that might already be present.

Do not demand that the author first write a polished Chinese paper or fill every field of a form. The assistant reconstructs the brief. The optional [intake form](../assets/intake.zh-CN.md) is a convenience, not a gate. Do not interpret “rough notes” as necessarily handwritten; support typed notes, slides, bullet points, and actual handwriting when accessible.

## Entry-specific operations

### A. Chinese notes

Split notes into atomic propositions, not mechanically into sentences. One sentence can contain a method fact, a preferred claim, and an untested interpretation. Preserve the original wording with its location; give each consequential item an ID.

Classify role and support independently:

| Role | Example meaning | Treatment |
|---|---|---|
| FACT | What was measured or implemented | Link to author report or an identifiable artifact. |
| INTENT | What the author wants the paper to emphasize | A framing candidate, not a result. |
| HYPOTHESIS | An explanation or expectation to be tested | Do not turn into observed evidence. |
| INTERPRETATION | What an observation may imply | Preserve alternatives and scope. |
| PLAN | An experiment not yet completed | Future work or gap register, never Results. |
| PREFERENCE | Desired audience, terminology, style | Follow unless it would misrepresent the study. |
| QUESTION | An unresolved point | Resolve from sources or localize the uncertainty. |

Statuses: `SOURCE_MATCHED`, `AUTHOR_REPORTED`, `DERIVED`, `IMAGE_READ`, `EXTERNAL_VERIFIED`, `UNRESOLVED`, `CONFLICT`. Source matching is provenance, not a declaration that an experimental protocol is sound. Hypotheses can be accurately source-matched as hypotheses; this does not turn them into facts.

Pay attention to Chinese epistemic and temporal markers: “可能,” “倾向于,” “仅,” “部分,” “尚未,” “计划,” “初步,” and “没做.” Preserve negations, class labels, units, and comparison direction. “显著” in casual notes does not authorize a statistical-significance claim. “泛化” requires the specific evaluated setting; “活性” requires an actual endpoint. Prefer a qualified English expression or an explicit issue over false precision.

If notes are handwritten or scanned, view the image when possible and transcribe only readable content. Mark ambiguous characters/values and their page/region. Do not repeatedly OCR a document when ordinary text extraction or direct visual reading suffices. An ambiguous decimal, exponent, target name, or negative sign must not be silently normalized.

### B. Rough intent plus completed results

First create an intent statement in the author’s terms. Then reconstruct the empirical record independently. Write three short entries: `intended claim`, `supported claim`, `gap between them`.

For example, “show that the fusion module is the source of improvement” requires evidence about the fusion operation, not only a comparison between a multi-input model and a smaller single-input baseline. A narrower descriptive contribution can still be written without inventing an ablation.

Use the supplied results to propose a paper-level thesis. Do not manufacture a fashionable bottleneck or call routine engineering a new learning principle. Do not silently change the problem from affinity to functional classification or from prediction to generation.

### C. Figure-led or mixed materials

Create a display register before drawing conclusions. Recover axes, legends, metrics, comparison groups, dataset/split, captions, and file version. Distinguish the visual’s content from missing provenance. An unlabeled heatmap is not automatically an attention map; an architecture block called “Encoder” does not identify a checkpoint or trainability.

Treat a clear plotted numeral as `IMAGE_READ`, retaining the visible precision. Do not read bar height as an exact hidden value or reconstruct unavailable individual predictions. See [04-figures-tables](04-figures-tables.md).

## A compact scientific brief

Fill only fields needed for this study: sample unit; task/endpoint; deployment inputs/outputs; dataset identity and label construction; implemented model; training/model selection/evaluation; completed results; negative findings; computational constraints; contribution candidates; author preferences; reference preferences; and unavailable details.

Separate a method description from proof that it produced the reported results. With code available, inspect actual imports, instantiated classes, saved configurations, and historical run identities as needed. Without code, retain explicitly author-reported descriptions. Do not make access to source code a prerequisite for writing.

## Facts and numbers

Use the [evidence ledger](../assets/evidence-ledger.csv) or an equivalent existing register. Keep raw values and source precision separate from displayed precision. For key numbers, record dataset/split, metric definition, direction, class/averaging, unit, model/run, aggregation, and uncertainty when known. Empty fields mean unknown, not zero, false, or not applicable.

A source conflict remains a conflict until reconciled. Do not average conflicting reports, choose the newer-looking filename, or select the better score by default. An explicit author correction updates intended facts but cannot erase contradictory experimental records without explanation.

Classify gaps:
- `EDITORIAL`: solve by organizing and writing.
- `SOURCE_RECOVERY`: find information in existing authorized material.
- `REAGGREGATION`: compute from identified existing records within authorization.
- `POST_HOC_ANALYSIS`: new diagnostic on existing data; separate permission and label.
- `NEW_EXPERIMENT`: not performed during ordinary drafting.

Proceed with unaffected sections. A few targeted questions can be bundled if essential, but do not stop a large writing task merely because optional formatting preferences are absent. Do not invent scientific facts as “reasonable assumptions.”
