# Sources, provenance and scope

Prepared 2026-11-14. Links below are methodological/documentation sources consulted for this skill's design. They are **not** empirical verification of any particular AIDD manuscript and should not be inserted into a user's review as if they support model-specific claims.

## Codex skill conventions (current online documentation)

1. OpenAI, **Build skills**, https://learn.chatgpt.com/docs/build-skills (accessed 2026-11-14). Basis: skill folder with `SKILL.md` frontmatter `name`/`description`, modular references/scripts, local `.agents/skills/` discovery, `$` explicit invocation in Codex, progressive disclosure. Installation advice can change; use current official documentation when needed.
2. OpenAI, **Customization / Skills**, https://learn.chatgpt.com/docs/customization/overview (accessed 2026-11-14). Basis: role of reusable skills and repository/user scopes.

## Review methodology and genre boundaries

3. Page MJ et al. **The PRISMA 2020 statement: an updated guideline for reporting systematic reviews.** *BMJ* 2021;372:n71. DOI: https://doi.org/10.1136/bmj.n71. Official overview https://www.prisma-statement.org/prisma-2020. Use as **reporting guidance**, not a substitute for performed searching/screening.
4. Tricco AC et al. **PRISMA Extension for Scoping Reviews (PRISMA-ScR): Checklist and Explanation.** *Ann Intern Med* 2018;169:467–473. DOI: https://doi.org/10.7326/M18-0850. Official overview https://www.prisma-statement.org/scoping.
5. Rethlefsen ML et al. **PRISMA-S: an extension to the PRISMA Statement for Reporting Literature Searches in Systematic Reviews.** *Syst Rev* 2021;10:39. DOI: https://doi.org/10.1186/s13643-020-01542-z. Official overview https://www.prisma-statement.org/prisma-search. Search reporting guidance, not a search-quality certificate.
6. Baethge C, Goldbeck-Wood S, Mertens S. **SANRA—a scale for the quality assessment of narrative review articles.** *Research Integrity and Peer Review* 2019;4:5. DOI: https://doi.org/10.1186/s41073-019-0064-8. Supports narrative-review appraisal dimensions; it is not a general prose/figure design scoring system.

## Source skill inspected

7. User-supplied archive: `drug-property-manuscript-rebuild-v2.0.0.zip`, containing `drug-property-manuscript-rebuild/SKILL.md`, `README.zh-CN.md`, modules for exemplar analysis, prose/visual transformation, comparative review and evidence guardrails. Read during this task to retain its useful *workflow principle* while redesigning content for review articles. The original package was **not modified, embedded, or redistributed** in this new ZIP.

## Domain examples and caution

AIDD-specific checks are **questions to verify in each cited original**: biological endpoints, dataset/holdout semantics, negative sets, pretraining and comparator confounding, simulation vs experimental validation, inferred structural contacts vs actual binding, and source-reported technical lineage. These are review audit heuristics, not claims that every AIDD source shares a single failure mode or proof that any review has been validated.
