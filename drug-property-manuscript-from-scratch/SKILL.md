---
name: drug-property-manuscript-from-scratch
description: Write a first original-research manuscript on drug-discovery property prediction from Chinese notes, a rough author brief, completed experimental data, and existing figures, without requiring a prior manuscript. Reconstruct the supported study, closely analyze real exemplar papers, and draft original English prose, captions, and tables. Use for notes-to-paper, intent-plus-results-to-paper, or figure-led first drafting; not generic translation, research invention, or primarily rebuilding an existing full draft.
---

# Drug Property Manuscript From Scratch — v1.0.0

## Job and success condition

Turn incomplete writing materials—not incomplete invented science—into a first coherent, evidence-bounded research manuscript for a computer-science conference or computational journal. Accept Chinese rough notes, prose or handwritten notes, an author’s broad intent, experiment tables/logs/predictions, existing figures, and optional code. A polished draft, English outline, code repository, and author-prepared input form are **not prerequisites**.

The main operation is:
**recover what is known → separate intention from observation → identify a defensible paper-level argument → learn concrete presentation choices from real exemplars → plan paragraphs and displays → draft and compare a real pilot → complete the requested paper → verify and hand off.**

“Write like a top journal” is a goal, not a usable specification. Do not stop at a generic outline, literal Chinese-to-English translation, inventory of modules, or a larger audit report. Deliver actual manuscript prose and usable displays within the available evidence. No guarantee of acceptance, novelty, scientific validity, or stylistic parity follows from using this skill.

## Defaults and relation to the rebuild skill

- Use English for manuscript text, captions, table headings, and figure labels; use the user’s language for editorial decisions and unresolved questions, unless instructed otherwise.
- Treat completed experiments as frozen. Read sources, write new text, and format supplied values; do not train, retune, relabel, change splits, or manufacture missing experiments. Reaggregation and data-driven redraws require identifiable inputs and the task’s authorization; new diagnostics remain separately authorized post hoc analysis.
- Preserve originals. Work in a new versioned directory such as `paper_from_scratch/v001/`; reuse an existing active directory only when continuation is intended.
- This is an **independent companion**, not a replacement for or dependency on `drug-property-manuscript-rebuild`. Rough notes belong here. A complete manuscript whose organization is the main problem normally belongs to rebuild. Follow an explicit user choice; do not launch both full workflows or automatically restart in rebuild after finishing.
- Mode `FULL_DRAFT` is the default for a paper request; `PILOT_ONLY`, `BLUEPRINT_ONLY`, and `SECTION_ONLY` apply only when requested. In full mode, calibrate internally and continue without an unsolicited approval pause.
- The skill provides instructions and templates, not a browser, vision model, plotting engine, compiler, or API account. Check real capabilities. Never claim execution, reading, visual inspection, author approval, or external review that did not occur.

## Load modules just before their stage

Resolve these files relative to this skill directory, not the project’s working directory. Keep the whole installed folder.

| Stage | Required reference |
|---|---|
| Recover notes, intent, artifacts, and evidence | [01-intake-evidence](references/01-intake-evidence.md) |
| Select and dissect real papers; create transfer cards | [02-exemplar-transfer](references/02-exemplar-transfer.md) |
| Construct a thesis; draft paragraphs and sections | [03-argument-first-drafting](references/03-argument-first-drafting.md) |
| Inspect/reuse/redesign figures; create tables and captions | [04-figures-tables](references/04-figures-tables.md) |
| Compare, integrate, deliver, or hand off | [05-review-handoff](references/05-review-handoff.md) |
| Make task-specific scientific or quantitative claims | [06-domain-guardrails](references/06-domain-guardrails.md) |

The assets are lightweight optional working templates; reuse equivalent project records. Do not require the user to fill them. The examples are **fictional teaching fixtures**, never manuscript evidence or real exemplar papers.

## 1. Recover the study, not just the notes’ wording

Read authorized project instructions and supplied material before asking questions. Locate files within the authorized workspace; do not require a prescribed input tree. Read the full relevant notes and tables; inspect each candidate figure visually with its available caption. Use the host’s file, document, PDF, and spreadsheet handling rules. Handwriting and embedded labels may remain unresolved; never silently guess them.

Classify the entry route:

| Route | What to do |
|---|---|
| Chinese notes + results/figures | Extract propositions, definitions, intentions, and qualifications; reorganize them rather than translating sentence by sentence. |
| Rough intent + results/figures | Build the study brief from artifacts; test the intended contribution against actual evidence. Do not demand a nonexistent draft. |
| Figures/tables + minimal explanation | Identify display meaning and supported observations; recover task/method details from accessible records. Localize remaining gaps. |
| Mixed or fragmentary materials | Reconcile versions and sources, preserve contradictions, and construct the same brief without privileging the most polished prose. |

Record a compact `study_brief.md`: task and sample unit; inputs/outputs and endpoints; available method detail; completed evaluation; candidate contributions; negative findings; author preferences; venue/year/track if known; allowed work; actual file identities; missing information; and next action. Use a provisional venue-neutral computational article when no venue is specified. Do not invent page limits or a two-column layout.

Separate every consequential item’s **role** (`FACT`, `INTENT`, `HYPOTHESIS`, `INTERPRETATION`, `PLAN`, `PREFERENCE`, `QUESTION`) from its **support status** (`SOURCE_MATCHED`, `AUTHOR_REPORTED`, `DERIVED`, `IMAGE_READ`, `EXTERNAL_VERIFIED`, `UNRESOLVED`, `CONFLICT`). Matching a source means the source says it—not that the experiment is scientifically valid or independently reproduced.

Preserve qualifiers in Chinese notes: “可能,” “尚未,” “未验证,” “数值更高,” and “部分数据集” must not disappear. Keep a bilingual terminology/notation map when needed. Do not import targets, architectures, datasets, or conclusions from a different project or memory.

## 2. Establish evidence sufficiency without blocking all writing

Use claim-specific sources: run-linked configuration/code for the trained method; labeled results and evaluator provenance for values; data/assay records for endpoints; verified primary literature for external claims; the author for intent. A current file or an architecture picture is not proof of a historical run.

Build a small source/claim register only for claims used or disputed. Record source path, location, context, units, split/run, aggregation, uncertainty, and allowed wording as available. Do not insert unknown defaults.

Write supported content now. Localize missing details with explicit working markers such as `[[METHOD_NEEDED:M03]]`, `[[CITATION_NEEDED:C02]]`, or `[[RESULT_CONFLICT:R04]]`, also listed in `verification.md`. Omit unnecessary unsupported claims instead of filling a paper with markers. An unresolved task definition, label meaning, or central result constrains the relevant sections; it does not authorize fabricated Methods or Results.

When only intention exists and no results are available, provide a clearly labeled pre-results writing scaffold and supported background—not a completed empirical paper. When results exist but raw predictions/code do not, draft within the supplied record without pretending independent verification. Ask only for genuinely indispensable unresolved information; continue all unaffected work.

## 3. Learn observable presentation choices from matched exemplars

Read `02-exemplar-transfer.md`. Use user-approved real papers first. If none are supplied and browsing is permitted, find a small role-matched set using nonconfidential task/method terms. Match scientific task, contribution type, audience, evidence richness, and space budget before prestige. Do not automatically use a named example from another skill.

For an overall anchor, inspect the full main text. For local examples, inspect complete paragraphs/sections and context. For figures and tables, inspect the actual page image and caption—not just extracted text. Record paper version, locator, access scope, and what was actually seen. No vision means no verified visual comparison; no full text means no full-paper exemplar claim.

Make transfer cards with:
`exact source location → observed choice → reader function → applicability → concrete local use → non-transferable elements → output check`.

Cover the main requested functions, normally introduction, technical explanation, results reasoning, key figure, and main table. Set a short project style contract from those cards. Generic praise, copying a palette, mimicking paragraph lengths, or copying wording/distinctive figure expression is not valid transfer. An exemplar’s claims, results, study motivation, and validation suite are **not** facts for this study.

## 4. Construct the paper’s argument and reader path

Read `03-argument-first-drafting.md` and the relevant domain guardrails. Start with the author’s intended message as a candidate—not a proven conclusion. From the same frozen facts, consider at most two or three genuinely different framings when useful. Select the most defensible provisional thesis and record why; do not silently replace the author’s research objective.

For each contribution connect:
`precise problem → implemented response → completed comparison → observed pattern → counterevidence/limitations → permitted conclusion`.

Do not invent a historical motivation, unmeasured bottleneck, theoretical guarantee, or missing ablation to make the story elegant. Describe retrospective rationale as rationale, not a preregistered hypothesis. A collection of known modules is not automatically a new principle.

Build a section-level reader path, then paragraph packets with one purpose, a central proposition, evidence IDs, selected local transfer card, required notation, and inference limit. Plan displays jointly: each has a distinct question, source, message, caption needs, and location. Reference choices inform how to communicate the evidence; they do not dictate which evidence must exist.

## 5. Calibrate real first-draft prose and displays

Create a small real pilot within scope: usually an Introduction span, a technical or Results paragraph, and a representative existing/redesigned display with its caption. Add a main table when available and useful. Do not invent inputs to satisfy a fixed pilot checklist.

Compare it against the source propositions (fidelity/completeness) and same-function real exemplars (presentation). **There is no mandatory old draft comparison because none may exist.** Notes’ rough wording is not a quality baseline. Record observable remaining gaps, then revise. Two focused rounds are a default effort budget, not a proven quality threshold.

In `PILOT_ONLY`, deliver the actual pilot and stop. In `FULL_DRAFT`, carry the selected choices into the manuscript without requiring unrequested approval. User approval is recorded only if actually obtained. If no real exemplar is accessible, draft provisionally from general editorial choices and mark calibration unavailable.

## 6. Draft the manuscript, not an expanded template

Before each section, reload its paragraph packets, exact facts, local transfer cards, and terminology. Write original English from the reconstructed meaning, not Chinese syntax or copied exemplar sentences. Avoid uniform paragraph recipes.

A useful authoring order is task formulation/Methods → Results/captions → Discussion/limitations → Introduction/Related Work → Abstract/title. This is not a mandated section order. Follow the requested scope and verified venue requirements.

Methods must describe actual computation and data/evaluation choices at the available level of detail. Results must make judgments from displayed evidence, not narrate every cell. Introduction must connect a supported technical problem to the actual response, not generic drug-discovery importance plus a module list. Related Work must compare verified close work by substantive distinctions. Discussion must retain failures and bounded applicability. Abstract/title must reflect final supported claims.

Maintain figure–text–table complementarity and numerical consistency. Retain readable existing figures when suitable; data-driven redraws require real values and saved sources. Follow `04-figures-tables.md`. A useful caption revision or table reorganization may improve presentation without redrawing every image.

## 7. Review separately for fidelity, communication, and submission

Follow `05-review-handoff.md`. Check: note-to-manuscript semantic fidelity; implemented method versus text/diagram; source-to-number consistency; task/metric/uncertainty meanings; citations; argument progression; concrete exemplar transfer; display readability; and actual rendering/compilation when supported.

An internal review is not independent validation. A self-score, lint pass, compilation success, or style-similarity score is not evidence of top-tier writing. Every material critique should name a location, its consequence for the reader, and a feasible edit. Fix within scope; separate new experiments from editorial repairs.

Verify current official instructions only for the actual venue/year/track, including anonymity and AI-use/disclosure rules. Do not invent an accepted-paper status or claim submission readiness with unresolved facts/citations. If no venue is set, report venue compliance as not assessed.

## 8. Deliver a usable first manuscript and a resumable handoff

For a full draft, deliver actual editable content, not only notes, cards, or a plan. Use one primary manuscript format; a compiled PDF is additional only when actually produced. Include only applicable supporting files:

```text
paper_from_scratch/v001/
  manuscript.md OR manuscript.tex
  study_brief.md                 # includes terminology, decisions, resume state
  evidence.csv                   # or an existing equivalent
  blueprint.md                   # paragraph/display plan
  reference_cards.md             # real-source observations and local choices
  style_contract.md
  comparison.md                  # actual pilot/output comparisons
  figures/                       # reused originals or real sources/exports
  tables/                        # real table data and editable tables
  references.bib                 # when needed and verified
  supplement.md OR supplement.tex # only when warranted
  verification.md
  handoff.md                     # compact and optional until continuation
```

Report independent statuses, not one inflated overall badge:
- Evidence: `AUTHOR_REPORTED`, `MIXED`, or `SOURCE_MATCHED_WITHIN_SCOPE`, with gaps.
- Exemplar calibration: `NOT_RUN`, `TEXT_ONLY`, or `TEXT_AND_VISUAL`, with actual locators.
- Artifact: `PARTIAL_DRAFT`, `COMPLETE_WORKING_DRAFT`, or `COMPILED_WORKING_DRAFT`; an explicit gap remains a gap even in a compiled file.
- Approval: `NOT_REQUESTED`, `PENDING`, or `AUTHOR_APPROVED_WITHIN_SCOPE` only after actual approval.

Offer the existing rebuild workflow only as a later optional handoff after a draft exists. Carry the source/claim register, selected exemplars, approved choices, raw-image paths, and remaining issues forward; do not discard them or force the author to repeat the intake. Neither skill replaces scientific author responsibility.
