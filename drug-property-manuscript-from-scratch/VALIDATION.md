# Validation record

Package: `drug-property-manuscript-from-scratch` v1.0.0. Date: **2026-10-16**.

## Repository sync note

When this package was added to the `literature` repository, the README wording was updated to describe the checked-in source directory, `.gitattributes` was added to keep hashes stable across operating systems, and `SHA256SUMS` was refreshed for this repository copy. The 64 checks below record the original package validation; this repository sync did not rerun the behavioral cases or the full packaging checks.

## Checks actually executed

Local Python checks parsed the generated YAML and CSV, checked required files and relative links, inspected text payload and Markdown fences, and verified the fictional example arithmetic. Packaging checks verified the install root, ZIP CRC, file set, bytes, and hash manifest.

**64 static/packaging assertions passed.** See `validation-results.json` for the machine-readable record. Structure/presence assertions do not test agent behavior or scientific validity.

An initial link check encountered the not-yet-generated validation report. Report creation was reordered before the final link recheck; no unresolved link failures remain.

| Check | Result |
|---|---|
| Delimited YAML frontmatter | PASS |
| Required metadata types | PASS |
| Valid name matching folder | PASS |
| Description within size boundary | PASS |
| All required resources exist | PASS |
| No symlinks | PASS |
| Nonempty UTF-8 text files | PASS |
| Text-only nonexecutable payload | PASS |
| No sandbox-specific generated paths | PASS |
| Relative link: README.zh-CN.md -> SOURCES.md | PASS |
| Relative link: README.zh-CN.md -> VALIDATION.md | PASS |
| Markdown fences: README.zh-CN.md | PASS |
| Markdown fences: VALIDATION.md | PASS |
| Relative link: SKILL.md -> references/01-intake-evidence.md | PASS |
| Relative link: SKILL.md -> references/02-exemplar-transfer.md | PASS |
| Relative link: SKILL.md -> references/03-argument-first-drafting.md | PASS |
| Relative link: SKILL.md -> references/04-figures-tables.md | PASS |
| Relative link: SKILL.md -> references/05-review-handoff.md | PASS |
| Relative link: SKILL.md -> references/06-domain-guardrails.md | PASS |
| Markdown fences: SKILL.md | PASS |
| Markdown fences: SOURCES.md | PASS |
| Markdown fences: EVAL_CASES.md | PASS |
| Markdown fences: assets/paragraph-packet.md | PASS |
| Markdown fences: assets/intake.zh-CN.md | PASS |
| Markdown fences: assets/transfer-card.md | PASS |
| Markdown fences: assets/study-brief.md | PASS |
| Markdown fences: assets/handoff.md | PASS |
| Relative link: references/02-exemplar-transfer.md -> ../assets/transfer-card.md | PASS |
| Markdown fences: references/02-exemplar-transfer.md | PASS |
| Markdown fences: references/06-domain-guardrails.md | PASS |
| Relative link: references/03-argument-first-drafting.md -> ../assets/paragraph-packet.md | PASS |
| Markdown fences: references/03-argument-first-drafting.md | PASS |
| Relative link: references/05-review-handoff.md -> 06-domain-guardrails.md | PASS |
| Relative link: references/05-review-handoff.md -> ../assets/handoff.md | PASS |
| Markdown fences: references/05-review-handoff.md | PASS |
| Relative link: references/01-intake-evidence.md -> ../assets/intake.zh-CN.md | PASS |
| Relative link: references/01-intake-evidence.md -> 04-figures-tables.md | PASS |
| Relative link: references/01-intake-evidence.md -> ../assets/evidence-ledger.csv | PASS |
| Markdown fences: references/01-intake-evidence.md | PASS |
| Relative link: references/04-figures-tables.md -> ../assets/figure-register.csv | PASS |
| Markdown fences: references/04-figures-tables.md | PASS |
| Markdown fences: examples/intention-conflict.md | PASS |
| Markdown fences: examples/notes-to-manuscript.md | PASS |
| Codex interface metadata | PASS |
| Explicit-only invocation | PASS |
| Default prompt names this skill | PASS |
| No declared external dependency | PASS |
| CSV header-only template: evidence-ledger.csv | PASS |
| CSV header-only template: figure-register.csv | PASS |
| CSV header-only template: result-register.csv | PASS |
| Fictional labeling: intention-conflict.md | PASS |
| Fictional labeling: notes-to-manuscript.md | PASS |
| Synthetic fixture has 3 numeric rows | PASS |
| Synthetic fixture ordering and arithmetic | PASS |
| 32 distinct proposed behavioral IDs | PASS |
| Behavioral cases explicitly not executed | PASS |
| Full and scoped output modes | PASS |
| No dependency on rebuild skill | PASS |
| ZIP CRC integrity | PASS |
| ZIP has one expected install root | PASS |
| ZIP safe relative paths | PASS |
| ZIP exact unique file set | PASS |
| ZIP bytes match local artifacts | PASS |
| SHA256 manifest coverage and consistency | PASS |

## Not executed

- Installation, discovery, or invocation in the user’s Codex: **NOT_RUN**.
- The 32 proposed cases in EVAL_CASES.md: **0 executed**.
- Writing from the user’s real notes, results, or images: **NOT_RUN**.
- Real-study exemplar analysis, figure generation, and manuscript compilation: **NOT_RUN**.
- Controlled or blind human comparison of writing quality: **NOT_RUN**.

The example documents are invented teaching fixtures. Only their arithmetic and explicit fictional labeling were checked; they are not experimental results or model-behavior tests.

## Integrity

`SHA256SUMS` covers every package file except itself. It checks consistency, not identity, safety, or official approval. This single-skill archive contains no font files, PDFs, publisher images, or executable payload.
