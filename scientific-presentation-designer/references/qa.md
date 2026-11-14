# Slide quality assurance

The gate is **rendered-slide inspection**, not success of the PPTX save operation.

## Mandatory checks

### Evidence

- All numerical results match provided sources, including precision, units, dataset, split, direction.
- Each data-bearing slide has evidence IDs and source trace in `evidence_ledger.csv`.
- No fabricated experimental evidence, baseline, error bar, statistics, or citation.
- Claims about improvement and significance are limited to tested comparisons.

### Story

- A listener can understand the question and decision without reading the underlying report.
- Each slide has one clear conclusion or question.
- Results dominate time; context is concise; limitations are not hidden.
- There is no report paragraph pasted as a slide.

### Visual

- Correct 16:9; all text/figures inside margins; no collision/clipping.
- Actual full-slide PNG render reviewed at 100% for all slides, not just cover/contact sheet.
- Text remains legible at conference scale: body usually >=18 pt, dense figure text >=13 pt; footnotes ~10 pt.
- Model colors and axis scales consistent; labels and legends readable.
- Visual rhythm deliberate; slide variety comes from information type, not ornament.
- No image stretching or low-resolution upscaling; no unexpected black glyphs / tofu squares.

### Technical

- PPTX opens with no repair warning.
- No broken external figure links or missing fonts that corrupt layout.
- Speaker notes, if authored, are not presented as measured evidence.
- Final deck, source ledger, and slide plan are delivered together.

## Iterative review loop

1. Build deck.
2. Render all slides to PNG; make contact sheet.
3. Inspect each slide in addition to contact sheet; record failures by slide ID.
4. Fix original slide-generation source and rebuild, **not** just a single rendered image.
5. Re-render affected slides or whole deck and inspect again.
6. Save `qa_report.json` with warnings + what was actually checked. Distinguish automated checks from visual/manual inspection.

`audit_deck.py` is intentionally conservative: it checks geometry, length/font red flags, source label presence but cannot prove visual quality. A clean JSON audit **is not** a visual-QA pass.

If there is no LibreOffice/PowerPoint renderer in the environment, generate PPTX, run structural audit, and report clearly that visual QA is pending.
