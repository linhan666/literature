# QA gates (do not claim tests not run)

1. **Evidence**: named sources exist; DOI/identity status is documented; claim IDs resolve; the exact original passage/figure is recorded; interpretation/source-reported/author-proposed are not visually conflated; no invented paper list or counts.
2. **Comparability**: reported metrics share endpoints, splits, data, model access and study budgets OR noncomparability is visibly disclosed; 'higher' isn't automatically better outside matched context.
3. **Graphics**: arrows have meaning; no false inheritance; proposed taxonomy is marked; figures are original/adapted/reproduced with rights tracked; no attention hotspot = proven binding-site claim.
4. **Artifact**: valid PPTX, slide count matches plan, editable native text/shapes/diagram elements wherever practical, original images remain intact; no missing paths.
5. **Structural QA**: inspect out-of-slide objects, text density, tiny fonts, repeated titles, missing labels, truncated footers; script checks are warnings, not certificates.
6. **Visual QA**: render all slides; inspect contact sheet and all full-resolution PNGs; check source legend, CJK glyphs, punctuation, line breaks, arrow landing, cropped captions, box alignment, table readability and color meaning. If an image can't be inspected, say visual inspection was not completed.
7. **Delivery**: `review_presentation.pptx`, `review_slide_plan.json`, `sources.csv`, `claims.csv`, `figure_manifest.csv`, `speaker_notes.md`, `qa_report.json`, `preview/contact_sheet.png`, `open_issues.md`.

Suggested status footer: `Source checked / Derived inference / Author proposal / Unresolved`. For demo say `DEMO — content not source verified` visibly.
