---
name: review-presentation-designer
description: Turn scientific review manuscripts, literature databases, reference libraries, evidence/claim matrices, and conceptual figures into visually refined, editable review-talk PowerPoint decks. Use for narrative-critical reviews, technical surveys, scoping/systematic reviews, journal clubs, literature seminars, and thesis background/related-work presentations. Specializes in taxonomies, mechanism comparisons, multi-track evolution, contradictory evidence, comparability checks, research gaps, and source-traceable diagrams; NOT a substitute for experimental-results presentation workflows.
---

# Review Presentation Designer

Create a **sourced scientific synthesis for an audience**, not an illustrated manuscript or a paper-by-paper list. Target PowerPoint `.pptx` that is genuinely editable. Default: 12–16 slides for a 15–20 minute technical review seminar, in the manuscript's language (use Chinese when asked). Use widescreen 16:9; support author-provided figures without speculative redrawing.

## Required workflow

1. **Inventory originals.** Read the actual manuscript (`.md`, `.docx`, `.pdf`), bibliography (`.bib`, `.ris`, references), `evidence.csv`, `claims.csv`, methods matrix, figures, and discussion notes if present. Do not assume a document named by the author exists. For extracted figures, record source, page, transformations, permission status and whether it is original, adapted, or reproduced. For PDF, inspect relevant page images when figures matter. Never cite a paper only from a language-model memory or a secondary summary while claiming primary verification.
2. **Classify the review and audience.** Read `references/review_modes.md`. Separate narrative-critical, systematic, scoping, and technical-survey conventions. Do not add an invented PRISMA flow, numerical study selection, forest plot, or pooled effect size. Determine the scope, take-home argument, competing models/definitions, criteria for comparison, contradictory findings and evidence gaps.
3. **Establish a claim–source graph.** Produce `presentation/sources.csv`, `presentation/claims.csv`, and `presentation/figure_manifest.csv` using `references/provenance_contract.md`. Distinguish `source_reported`, `independently_verified`, `synthesis_inference`, `author_proposed`, `disputed`, and `unresolved`. `verified_against_source` means *located in source text*, not independent replication. Track DOI/URL, source passage/page, study conditions and known ambiguities. No silent repair of conflicting references.
4. **Write the review argument before slides.** Create `presentation/review_outline.md` and `presentation/review_slide_plan.json`. Do NOT use manuscript subsections or individual papers as automatic slides. Prefer: field question → scope/definitions → proposed taxonomy → how mechanisms differ → what evidence supports which claims → comparability/contradictions → evolution (supported edges only) → gaps and research agenda → synthesis. Choose one message per slide, a meaningful visual form, and claim IDs for each claim. Cite original papers where available; otherwise visibly label the claim as interpretation/proposal/unresolved. Use `references/narrative_and_archetypes.md`.
5. **Make conceptually faithful visuals.** Read `references/design_system.md` and `references/diagram_grammar.md`. Native editable PowerPoint shapes for taxonomies, matrices, comparisons, flow, timelines and conceptual diagrams; preserve scientific notation and semantics. Do not turn attention maps into validated binding contacts, publication sequence into technical inheritance, or a proposed framework into a verified universal standard. Never rank incomparable datasets or evaluation conditions. For borrowed diagrams, prefer author-created abstractions with citations; if reproducing external imagery, handle license/copyright separately.
6. **Validate evidence and build.** The bundled renderer is a useful editable scaffold; customize for the paper rather than shoehorning a complex review into a template. Run:

```bash
python -m pip install -r <SKILL_DIR>/requirements.txt
python <SKILL_DIR>/scripts/validate_review_plan.py --plan presentation/review_slide_plan.json --claims presentation/claims.csv --sources presentation/sources.csv --out presentation/provenance_report.json --strict
python <SKILL_DIR>/scripts/build_review_deck.py --plan presentation/review_slide_plan.json --claims presentation/claims.csv --sources presentation/sources.csv --out presentation/review_presentation.pptx --notes-out presentation/speaker_notes.md
```

The builder accepts `cover`, `big_idea`, `scope`, `taxonomy`, `mechanisms`, `lanes`, `comparability`, `matrix`, `evidence_map`, `timeline`, `debate`, `agenda`, `synthesis`, `figure`, and `closing`. See `references/plan_schema.md` and `examples/demo_review_plan.json`. **Production mode:** cited factual claims must be traceable; unresolved items need visible uncertainty labels; source-free conceptual propositions must state `AUTHOR-PROPOSED`. **Demo mode:** all slides display DEMO disclaimers and must not be passed off as verified research.
7. **Render every slide and inspect.** Run:

```bash
python <SKILL_DIR>/scripts/render_review_deck.py presentation/review_presentation.pptx --outdir presentation/preview
python <SKILL_DIR>/scripts/audit_review_deck.py presentation/review_presentation.pptx --plan presentation/review_slide_plan.json --out presentation/qa_report.json
```

Inspect the contact sheet **and each full-resolution slide**. Repair text clipping, line crossing, impossible timelines, misleading arrows, legend problems, citation illegibility and repeated layouts; rerender after repairs. Neither rendering success nor static QA proves a slide was visually inspected or the evidence verified. See `references/qa_acceptance.md`.
8. **Deliver an auditable package.** Deliver the editable `.pptx`, preview sheet, slide plan, sources/claim ledger, figure manifest, QA report, and `speaker_notes.md` with citations, known uncertainties, and discussion questions. If source files are missing, deliver a clearly labeled draft or evidence-needed outline; never fabricate citations, bibliographic IDs, numerical counts or scientific agreement.

## Review-specific nonnegotiables

- Distinguish a **model mechanism** from a **biological mechanism**, an attention visualization from independently checked structural contact, and performance prediction from scientific explanation.
- Show the **comparability contract** before cross-paper ranking: task/endpoint; dataset/labels/split; available modalities and pretraining; supervision/evaluation object; operator intervention/capacity/training budget. Compare only within matched conditions; otherwise label `conditional` or `not comparable`.
- Figure edges must mean something stated: sourced lineage or dependency (`solid`), author-proposed hypothesis (`dashed`), chronological adjacency (`no arrow`). Distinguish **time** from **technical inheritance**.
- Use evidence codes/legend for `SOURCE-REPORTED`, `INDEPENDENTLY CHECKED`, `AUTHOR-PROPOSED`, `INFERENCE`, `DISPUTED`, `UNRESOLVED`. Treat source identity verified separately from claim supported.
- For systematic/scoping reviews, only present real screening/selection records; avoid retroactively inventing systematic methods for a narrative review.
- Never imply a source's inclusion in an evidence matrix proves that the figure/review conclusion has been independently validated.

## Detailed resources (load only as relevant)

- `references/review_modes.md` — mode choice and guardrails.
- `references/provenance_contract.md` — source/claim/figure ledger and status semantics.
- `references/narrative_and_archetypes.md` — review argument and slide allocation.
- `references/diagram_grammar.md` — meaning-preserving taxonomies, timeline, map, comparison.
- `references/design_system.md` — visual craft and color accessibility.
- `references/plan_schema.md` — JSON schema and plan examples.
- `references/qa_acceptance.md` — evidence, structural and visual acceptance gates.
- `references/prompts.md` — ready-to-use prompts for literature-review manuscripts.
