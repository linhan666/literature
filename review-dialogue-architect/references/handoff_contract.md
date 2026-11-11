# Canonical handoff to evidence-first-review-writer

## Exact deliverable

The primary output is `input/discussion_summary.md` (UTF-8 Markdown). It must be **self-contained**: a separate assistant without the original chat can reconstruct the review's scientific intent, candidate framework, open alternatives, and validation requirements. Do not rely on unshared private model context, a link to a chat, a hidden attachment or unspecified paths.

This is an **idea and decision artifact**, **not** a verified source review, manuscript draft, a PRISMA report, or a literature-search record. The downstream `evidence-first-review-writer` is responsible for checking bibliography and scientific evidence, revising the proposed taxonomy in response to findings, and writing the English paper.

## YAML header (simple static fields)

```yaml
---
schema: review-dialogue-handoff/v1
stage: provisional                   # provisional | dialogue-complete
working_title: "Specific review working title"
dialogue_language: zh-CN             # or en, etc.
review_type: narrative-critical      # or systematic, scoping, undecided
literature_status: not-searched      # not-searched | discovery-only | partially-checked
---
```

- `provisional` = useful draft, but final choices or dialogue not yet established.
- `dialogue-complete` = sufficient **actual** dialogue/author decisions to hand off; never means all sources were checked.
- `not-searched` = no real source lookup happened here.
- `discovery-only` = actual lookup was performed, yet no claim was checked against source text.
- `partially-checked` = at least one actual source excerpt/method/result was checked for a specified claim; it does **not** mean all claims were verified.
- Never claim any search status from recalled model knowledge or metadata alone.

## Canonical headings

Use `assets/discussion_summary.template.md`. The validator checks the existence of these headings (numbers and names exact) but not intellectual quality.

1. `## 1. Topic and original research goals`
2. `## 2. Scope, exclusions, review type and audience`
3. `## 3. Central thesis and research questions`
4. `## 4. Concept map and proposed taxonomy`
5. `## 5. Competing frameworks and critical debate`
6. `## 6. Comparative evaluation dimensions`
7. `## 7. Candidate scholarly contributions`
8. `## 8. Proposed English review outline`
9. `## 9. Planned figures and tables`
10. `## 10. Candidate sources and evidence status`
11. `## 11. Claim-verification backlog and search seeds`
12. `## 12. Decision ledger and change history`
13. `## 13. Open questions and prioritized next steps`
14. `## 14. Downstream handoff brief (English)`

An executive handoff summary immediately after frontmatter is recommended. Follow it with sections 1–14. Keep `[TO VERIFY]` in meaningful content where needed; do not leave template placeholders (e.g. `{{TOPIC}}`) in exported files.

## Required distinctions

### Decision attribution

Use literal provenance tags in decision tables or prose:

| Status | Meaning | Example |
|---|---|---|
| `USER_GIVEN` | Explicit initial input | “User requires a sequence-only scope.” |
| `USER_CONFIRMED` | Actual user agreement | “User confirmed only explicit cross-modal interactions.” |
| `ASSISTANT_PROPOSED` | Plausible proposal, not accepted | “Recommend taxonomy using 2 axes.” |
| `OPEN` | Requires selection or evidence | “How to handle hybrid architectures?” |
| `DISPUTED` | Alternatives with arguments | “Operator-centric vs evidence-centric review.” |

Silence is never `USER_CONFIRMED`; quote or reference the actual user turn in a way available in this document. Do not fake user turns.

### Evidence state

Use separate evidence tags for factual claims:

- `BACKGROUND_UNVERIFIED`: from general knowledge or model analysis, not checked against actual source.
- `SOURCE_LOCATED`: real discoverable bibliographic item or URL, claim support not checked.
- `SOURCE_CHECKED`: source text and specific claim directly compared, with actual DOI/URL and page/section/table locator.

The phrase “source checked” is never justified by DOI/title matching alone. If `literature_status: not-searched`, cite no supposedly executed search or retrieved counts. Sources supplied by the user are not automatically verified; trace them as `USER_GIVEN` + `BACKGROUND_UNVERIFIED` or `SOURCE_LOCATED` if the record can be identified.

### Candidate claims and search seeds

Provide a prioritized table with IDs (`C01`, `C02`...), statement/question, status, why it matters, what precise evidence could support/refute it, and suggested search terms/platforms. Separate *existence of a paper* from *support for a scientific claim*. Search seeds are **plans**, not executed queries; label them `PROPOSED QUERY / NOT RUN` unless actually executed.

### Candidate contributions

Recommend intellectual additions that are meaningful even if the original title is vague: new taxonomy, methodological distinction, reporting framework, problem-conditioned comparison, research agenda. Every proposed novelty claim requires `CHECK_NOVELTY` before finalization. Do not promise novelty or publication success.

## Compatible user-facing files

Recommended project layout:

```text
project/
├── .agents/skills/
│   ├── review-dialogue-architect/
│   └── evidence-first-review-writer/
├── input/
│   ├── topic.md
│   ├── initial_goals.md
│   └── discussion_summary.md          # produced after dialogue
├── notes/
│   └── session_state.md                # optional, draft turns and decisions
├── drafts/
│   └── discussion_summary.md          # work-in-progress; export at checkpoint
└── review-workspace/                  # downstream outputs
```

The downstream Skill's original instructions accept the author's topic, scope, and optional research summary; this handoff simply provides a richer input. Do not modify the downstream Skill to silently accept invented literature or to auto-endorse the upstream taxonomy.

## Export procedure

1. Accumulate conclusions, alternatives and attributions **from real available dialogue**.
2. Fill mandatory template sections; adapt substantive content to the field.
3. Set correct stage and literature status.
4. If filesystem is available, optionally run:

```bash
python scripts/handoff.py validate --file drafts/discussion_summary.md
python scripts/handoff.py export --project .
```

5. If `stage: provisional`, the export command blocks by default; user can explicitly use `--allow-provisional` to export with clear warning.
6. The script can validate headings, basic metadata, placeholder absence and consistent status values; it cannot judge scientific quality or verify user confirmation, literature or plagiarism.
7. Hand the exported `input/discussion_summary.md` and optional `input/topic.md` to the next Skill. Advise the next Skill to first perform **scope/novelty checking** and **claim-by-claim verification**, not to copy the summary into the English manuscript.

## Quality rubric (human/agent review; not mechanically certified)

Score each 0=missing, 1=partial, 2=adequate; report gaps, not an unsupported overall percentage:

1. Accurate reproduction of user goals and exclusions.
2. Clear problem framing and conceptual boundaries.
3. Nontrivial intellectual advances beyond paraphrase.
4. Alternative organizing frameworks explicitly compared.
5. Taxonomy layer and overlap tested.
6. Critique includes concrete failure/counterexamples or falsifiable checks.
7. Candidate contributions distinguish novelty hypothesis from demonstrated novelty.
8. Comparisons respect task/dataset/metric differences.
9. Decision attribution and reversals are traceable.
10. Factual assertions separated from speculation and source verification.
11. Outline follows a coherent argument and supports future tables/figures.
12. Verification backlog is prioritized and actionable.

A structurally valid Markdown may still fail many of these substantive criteria. Audit scientifically before export when possible.
