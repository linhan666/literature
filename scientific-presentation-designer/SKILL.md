---
name: scientific-presentation-designer
description: Turn scientific experiment outputs, benchmark CSVs, figures, and Markdown/Word research reports into visually polished, editable PowerPoint decks for lab meetings, project reviews, thesis defenses, and conferences. Use when Codex is asked to make, redesign, or improve research PPT/PPTX slides; includes evidence-led storyboarding, professional scientific layouts, native charts, slide rendering, and visual QA.
---

# Scientific Presentation Designer

Produce a **credible scientific argument presented as a designed slide deck**, not an automatically paginated report. Default to Chinese-language lab-meeting slides if the user writes Chinese; support English and bilingual decks. Deliver a real `.pptx`, an export/preview when feasible, and a source-to-slide audit trail.

## Mandatory workflow

### 1. Audit the inputs

Read the files the user actually supplies (experiment report, Markdown, CSV/JSON, metrics, figures, source code). Inventory them before writing slides. Identify research question, evaluation design, datasets/splits, baselines, metrics, results, negative findings, limitations, and proposed next steps. Do not infer that an artifact exists because the report mentions it. Prefer exact statistics from tables or machine-readable outputs to prose summaries. If reported values conflict, flag the conflict and avoid choosing one silently.

Build a `presentation/evidence_ledger.csv` with columns `id,claim_or_figure,source_path,source_location,exact_value,units,split_or_condition,verification_status,slide_ids,notes`. Use `verified`, `ambiguous`, or `unsupported`, where verified means checked against the provided source, **not** independently replicated. Mark original plotted figures as reused, and derived charts as recalculated.

### 2. Design the scientific narrative BEFORE creating slides

Write `presentation/slide_plan.json` from the provided report. First decide audience (PI/group meeting, paper presentation, defense, conference, stakeholder), duration, language, and expected detail. If unspecified: 10-12 slides / 12-15 minutes / technical lab meeting / follow input language. Allocate slides to a compelling progression: question → gap/hypothesis → data/protocol → method → central quantitative result → robustness/ablations → failure cases → limitations → actionable next experiments. Never auto-create one slide per section or paste report paragraphs verbatim.

Each content slide requires: an **assertive headline** (what the evidence says, not a generic heading), one primary visual, one supporting message, and its source identifier(s). Rewrite technical prose into concise claims but do not strengthen the scientific conclusion. See `references/storyboard.md` and `references/evidence_guardrails.md`.

### 3. Apply a visual system, not random decoration

Read `references/design_system.md` and `references/archetypes.md`. Default to `lab-light`: white canvas, navy typography, restrained teal emphasis, amber for comparison, lavender for secondary methods, consistent grid. Typical titles 29-35 pt, body 18-23 pt, plot labels 13-17 pt, source notes 9-11 pt. 16:9; use at least 0.55 in outer margins. Use **one message per slide** and a visual hierarchy. Tables must be pruned, charts labeled, figures high resolution. Never rely on a dark full-slide background for every page; alternate intentional section breaks with clean light content pages.

Scientific guidelines: use the same colors for a given model/dataset throughout; keep baselines neutral and the proposed approach teal; use direct labels, exact units, split names, and N where meaningful. Never use visual area/length to imply unmeasured performance. Preserve chemical structures, 3D geometry, equations, legends, and scientific plots without content-altering redrawing.

### 4. Generate editable PowerPoint

Prefer native PowerPoint objects for text, geometric diagrams, cards, tables, and straightforward charts. Use raster/vector images for original research figures; do not replace them with AI art. If your environment supports PptxGenJS, you may use it with equivalent standards. A bundled Python reference renderer is available:

```bash
python -m pip install -r <SKILL_DIR>/requirements.txt
python <SKILL_DIR>/scripts/build_deck.py --plan presentation/slide_plan.json --out presentation/research_deck.pptx
```

The example plan in `examples/example_plan.json` demonstrates supported layouts. This renderer is a **starting scaffold, not a ceiling**: customize layout/typography/plots in code to fit real experiments. Do not shoehorn unusual scientific figures into an inappropriate template. Use only existing files in `image_panel` slides; missing figure paths are a hard failure.

### 5. Render EVERY slide and repair

Visual QA is mandatory, not optional. Run:

```bash
python <SKILL_DIR>/scripts/render_deck.py presentation/research_deck.pptx --outdir presentation/preview
python <SKILL_DIR>/scripts/audit_deck.py presentation/research_deck.pptx --out presentation/qa_report.json
```

Inspect `presentation/preview/contact_sheet.png` and each full-size PNG. If you can inspect images, **actually inspect them**. Correct overflowing labels, tiny text, plot collisions, unwanted image cropping, unreadable legends, color misuse, missing source notes, ragged alignment, and repetitive layouts. Render again after material changes. If a renderer is unavailable, state that visual QA was not performed: do not claim it passed. See `references/qa.md`.

### 6. Deliver the presentation package

Output at minimum:

- `research_deck.pptx` — editable final deck.
- `slide_plan.json` — ordered message, slide type, content, source IDs.
- `evidence_ledger.csv` — where every quantitative claim/figure came from.
- `qa_report.json` and `preview/contact_sheet.png` — if tools were available.
- `presentation_notes.md` — talking points, assumptions, issues requiring human review.

For any missing evidence, present a neutral limitation or exclude the ungrounded result. Clearly indicate which data are illustrative vs measured. If the source material is insufficient, produce the best possible honest deck from the available material rather than inventing figures or statistical significance.

## Specific failure modes to avoid

- PowerPoint as a Word document: no 80-word paragraphs, no 12-line bullets, no default gradient SmartArt.
- One repeated template for every slide, random emoji icons, generic stock lab photos, neon palettes, 3D decorative charts, or meaningless hero images.
- Claims that an increase is significant without a statistical test; conflating AUROC with AUPRC; unexplained changes in evaluation split/denominator; making up sample size, p-values, CIs, timestamps, or data lineage.
- Ranking models on inconsistent datasets, endpoints, or metrics as though the runs were matched.
- Omitting negative results, limitations, or next experiments from research talks.
- Overwriting source figures or raw result files.
- Describing generated slides as visually inspected when no slide-by-slide render inspection happened.

## References, when needed

- `references/storyboard.md`: scientific talk sequencing and slide budget.
- `references/design_system.md`: typography, grid, palette, charts.
- `references/archetypes.md`: visual layout catalog, intended use, anti-patterns.
- `references/evidence_guardrails.md`: source traceability, honest comparisons.
- `references/qa.md`: acceptance gates and iterative QA.
- `references/codex_prompts.md`: Chinese launch prompts for the user.
