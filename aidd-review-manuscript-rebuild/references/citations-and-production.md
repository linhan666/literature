# Citations, bibliography, originals and production

## Bibliographic identities and editorial provenance

Use existing `references.bib`, citation keys and bibliography databases where available. Never generate a new DOI by guesswork. Match primary source identities by actual title/authors/year/venue/DOI; distinguish preprint versions from peer-reviewed records. Identify two same-named works by authors and technical operations, not by branding alone. Where references conflict, record evidence and keep the manuscript cautious.

Citations have **two checks**:
1. *Mechanical*: in-text citation key resolves to a bibliography entry, figure paths exist, unfilled placeholders are visible, duplicate keys are avoided.
2. *Scientific*: the cited source actually supports the exact proposition, population, measured endpoint and interpretation; original pages/figures/code actually inspected at a defensible scope.

Passing (1) never implies passing (2). Citation counts and density do not measure source accuracy. A DOI resolving to the correct paper is not enough to claim method verification.

## References and edits

- Add sources only after obtaining reliable metadata; record exact origin and access date when necessary. Externally downloaded bibliographic metadata may still contain errors.
- Never “fix” a paper's actual reported results solely using another review's summary. Verify originals for pivotal disputes.
- Follow journal rules for numbered vs author–year, preprint references, datasets, code and AI-use disclosures when actually specified and current. No venue specified → leave flexible.
- After moving a paragraph, carry only citations that still support its revised claims. Record rejected/refined propositions for author review when they are consequential.
- Source and exemplar PDFs are not distributed as part of the generated manuscript package unless rights and user request permit. The user's original files stay untouched; outputs go into a separate folder.

## Optional static check

From a Python environment:

```bash
python scripts/review_lint.py --manuscript review_rebuild/manuscript.md \
  --bib review_rebuild/references.bib \
  --report review_rebuild/lint_report.json
```

Optional supported checks: Markdown/LaTeX citation keys, BibTeX entry identifiers, relative local figure paths, duplicate BibTeX keys and clearly marked placeholders. Use `--help` to see options. Script does not search the web, verify DOI metadata, interpret scientific claims, compile TeX, check peer review or validate the review genre. It supports `.md` and `.tex` inputs. Do not feed its JSON output to the manuscript as if it were a scientific conclusion.

## Export checklist

- Reopen the actual generated manuscript and (if requested/available) compiled PDF/DOCX rendering. Check sections, table/figure placement, retained captions, page breaks, broken refs and the abstract/conclusion relationship.
- Inspect real figures at actual submission width; do not confuse vector validity with readable design.
- Check citations and numerical statements after every major rearrangement.
- Only claim a format is produced when the exact file exists and is accessible.
- Mark `DONE`, `NOT_RUN`, `UNAVAILABLE`, `BLOCKED` with exact evidence. Compiled PDF not produced → do not include a guessed PDF link.

## Originality and permissions

Use reviews as **calibration examples**. Transfer generalized reader-oriented operations, not copied diagrams, phrases, structure or bulk paraphrases. Do not conceal authorship or create misleading search methodology or reviewer records. Manuscript review is not a substitute for author responsibility and target journal requirements.
