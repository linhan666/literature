# Reporting, authorship, ethics, and release checks

## Norms (consult original, current source)

- **PRISMA 2020** (systematic review reporting): https://www.prisma-statement.org/prisma-2020 ; original statement: doi:10.1136/bmj.n71. The checklist and flow diagrams support transparent reporting; compliance depends on actual methods and disclosure, not a generated diagram.
- **PRISMA-S** (reporting literature searches): Rethlefsen et al. (2021), doi:10.1186/s13643-020-01542-z ; also in JMLA doi:10.5195/jmla.2021.962. Distinguish the specific versions/venues and avoid merging their DOIs into one record.
- **PRISMA-ScR** (scoping reviews): https://www.prisma-statement.org/scoping ; Tricco et al. (2018), doi:10.7326/M18-0850.
- **SANRA** (narrative article appraisal): Baethge, Goldbeck-Wood & Mertens (2019), doi:10.1186/s41073-019-0064-8. Guide to appraisal; not a guarantee of validity.
- **ICMJE recommendations** on AI assistance and author responsibility: https://www.icmje.org/recommendations/browse/roles-and-responsibilities/defining-the-role-of-authors-and-contributors.html . Human authors remain accountable. AI tools are not authors. Disclose use according to journal policy.

Links above are references for methods and ethics, not evidence that a particular review has met them. Confirm publisher instructions at time of submission. Avoid reproducing complete checklists without respecting licensed content; use official material.

## Release checklist

- [ ] Correct review-type label; scope/search methods fully and accurately described.
- [ ] Search queries, platforms, dates, filters, and observed counts preserved if executed.
- [ ] Records vs reports vs studies tracked; duplicate reports reconciled.
- [ ] Full-text claims checked against correct version/section/page/figure/table.
- [ ] Citations verified as bibliographic identities, with preprint and correction status noted.
- [ ] Contradictory evidence and important negative findings included.
- [ ] Performance comparisons avoid invalid cross-dataset or incompatible endpoint claims.
- [ ] Model limitations and generalization boundaries clearly stated.
- [ ] Reused figures and quoted content cleared for publication.
- [ ] Confidential/unpublished research used only under authorization and applicable policies.
- [ ] Human author has approved contribution/interpretation; disclosures, conflicts, funding and AI use addressed.
- [ ] Target journal title, article category, length, formatting, reference style, and reporting requirements confirmed.
- [ ] All local audit errors resolved; warnings explicitly considered and logged.

## AI-use disclosure suggestion (edit to actual work)

> AI-assisted tools were used to support literature discovery organization, drafting assistance, and/or language editing as described in the authors' workflow records. The authors independently verified bibliographic records, scientific claims, interpretations and references, and take full responsibility for the final manuscript.

Do not include an activity not performed. Specific journal policies may require details about tools, dates, prompts, or data confidentiality.

## Confidentiality and provenance

Do not send unpublished manuscripts, patient data, confidential submissions or proprietary datasets to unauthorized search endpoints or external APIs. `verify_dois.py` sends only DOI strings to Crossref when explicitly invoked; no manuscript or abstract text is sent. A script completing does not mean a policy has been satisfied. Do not invent second independent human reviewers or protocol registrations.
