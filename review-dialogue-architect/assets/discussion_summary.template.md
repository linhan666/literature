---
schema: review-dialogue-handoff/v1
stage: provisional
working_title: "{{WORKING_TITLE}}"
dialogue_language: zh-CN
review_type: narrative-critical
literature_status: not-searched
---

# Review Dialogue Summary — {{WORKING_TITLE}}

> **Artifact status:** PROVISIONAL. This document summarizes a research dialogue, not a verified literature review. All proposed novelty claims, paper identities, and experimental assertions require independent checking before being used as manuscript evidence.

**Executive handoff (5–10 lines):**
- User's original aim: [SUMMARIZE FAITHFULLY; NO INVENTED USER REQUIREMENTS]
- Recommended intellectual thesis: [ASSISTANT_PROPOSED unless user confirmed]
- Key boundary: [USER_GIVEN / USER_CONFIRMED / OPEN]
- Candidate contribution: [NOVELTY HYPOTHESIS; CHECK_NOVELTY]
- Most important unresolved point: [OPEN, or "None identified yet"]
- First downstream step: verify scope and novelty against actual relevant reviews; do not start polished prose.

## 1. Topic and original research goals

**Working title:** {{WORKING_TITLE}}

**User's original goals (faithful, not inferred):**

- `USER_GIVEN`: [ORIGINAL AIM]

**Interpretation proposed during discussion:**

- `ASSISTANT_PROPOSED`: [INTERPRETATION AND REASON]

## 2. Scope, exclusions, review type and audience

- Review type: [PROVISIONAL MODE AND WHY]
- Included topics and rationale: [TOPICS]
- Excluded topics and rationale: [TOPICS]
- Intended readers: [AUDIENCE]
- Temporal/disciplinary/geographic boundaries: [IF UNSPECIFIED, SAY SO]
- Scope-changing uncertainties: [OPEN POINTS]

## 3. Central thesis and research questions

**Proposed central thesis (not yet proven):** [THESIS]

| ID | Question | Role in the review | Decision status |
| --- | --- | --- | --- |
| RQ1 | [A CONCEPTUAL QUESTION] | [WHY IT MATTERS] | ASSISTANT_PROPOSED |
| RQ2 | [A COMPARISON QUESTION] | [WHY IT MATTERS] | OPEN |

## 4. Concept map and proposed taxonomy

**Ontological layers being separated:** [PROBLEM / INPUT / OPERATOR / SUPERVISION / OUTPUT / VALIDATION, AS RELEVANT]

**Taxonomy A — candidate:** [AXES, CATEGORY DEFINITIONS, EXAMPLES, EXCLUSIONS]

**Stress test:** [OVERLAPS, BORDERLINE CASES, UNCOVERED METHODS, GRANULARITY]

**Taxonomy status:** [USER_CONFIRMED / ASSISTANT_PROPOSED / OPEN]; validity awaits source mapping.

## 5. Competing frameworks and critical debate

| Option / claim | Strongest rationale | Counterargument or risk | Proposed resolution | Status |
| --- | --- | --- | --- | --- |
| Framework A | [ARGUMENT] | [SERIOUS CRITICISM] | [EVIDENCE OR DECISION NEEDED] | ASSISTANT_PROPOSED |
| Framework B | [ARGUMENT] | [SERIOUS CRITICISM] | [EVIDENCE OR DECISION NEEDED] | OPEN |

## 6. Comparative evaluation dimensions

Define the actual evaluation axes and why a naive across-paper number comparison may be invalid. Include comparability requirements before collecting models. Do not fabricate benchmark outcomes.

| Dimension | Definition | What must be held comparable | Verification need |
| --- | --- | --- | --- |
| [TASK] | [DEFINITION] | [ASSAY/LABEL/SPLIT/ETC.] | CHECK_COMPARABILITY |

## 7. Candidate scholarly contributions

| ID | Proposed original contribution | Why it could matter | Risk of overlap with prior reviews | Evidence needed |
| --- | --- | --- | --- | --- |
| N1 | [CONTRIBUTION HYPOTHESIS] | [VALUE] | [TO INVESTIGATE] | CHECK_NOVELTY |

Distinguish a better organization from a genuinely new empirical result, and do not claim to be first without external validation.

## 8. Proposed English review outline

Provide 5–9 argument-driven sections with **what each section needs to demonstrate**, not merely a list of author/model names.

1. **[Section title]** — claim/argument: ...; evidence needed: ...
2. **[Section title]** — claim/argument: ...; evidence needed: ...
3. **[Section title]** — claim/argument: ...; evidence needed: ...

## 9. Planned figures and tables

| ID | Type | Question it answers | Required underlying evidence | Status |
| --- | --- | --- | --- | --- |
| F1 | Conceptual taxonomy | [QUESTION] | Concept definitions + model placement verification | PROPOSED |
| T1 | Comparison matrix | [QUESTION] | Real source-verified model characteristics | PROPOSED |

## 10. Candidate sources and evidence status

> A paper mentioned in conversation is a candidate, not an authenticated citation. If none was actually supplied or discovered, write "No sources recorded; literature search not performed." Do not fill this table with made-up papers.

| ID | Source title / URL / DOI exactly as supplied or observed | Where it came from | Evidence state | Specific claim to check |
| --- | --- | --- | --- | --- |
| [IF ANY] | [LITERAL SOURCE OR NONE] | USER_GIVEN / ACTUAL SEARCH | BACKGROUND_UNVERIFIED / SOURCE_LOCATED / SOURCE_CHECKED | [CLAIM] |

## 11. Claim-verification backlog and search seeds

| Priority | ID | Claim or open empirical question | Failure if false | Evidence required | Search seed, NOT RUN |
| --- | --- | --- | --- | --- | --- |
| P0 | C01 | [CLAIM] | [HOW THESIS WOULD CHANGE] | CHECK_NOVELTY / CHECK_METHOD / CHECK_RESULT / CHECK_CONTRADICTION | [SEARCH TERMS] |
| P1 | C02 | [CLAIM] | [IMPACT] | [SOURCE/FIGURE/TABLE NEEDED] | [SEARCH TERMS] |

**Actual searches executed in this dialogue:** None unless separately documented with platform, exact query, date and observed result; otherwise explicitly state `NOT RUN`.

## 12. Decision ledger and change history

| Decision ID | Issue | Current choice or proposal | Who decided it / evidence | Alternatives or reversal |
| --- | --- | --- | --- | --- |
| D01 | [ISSUE] | [CHOICE] | USER_GIVEN / USER_CONFIRMED / ASSISTANT_PROPOSED / OPEN | [ALTERNATIVE] |

**Recorded reversals:** [ACTUAL USER CORRECTIONS WITH PREVIOUS AND UPDATED DECISIONS, OR NONE].

## 13. Open questions and prioritized next steps

**Unresolved decisions:** [OPEN, with consequence and recommended way to decide. Do not present as confirmed.]

**What would invalidate the current architecture:** [SOURCES / RESULTS / COUNTEREXAMPLES / CONCEPTUAL ISSUES].

**Prioritized next steps for the downstream review:**
1. Verify prior review coverage / proposed novelty.
2. Test and refine taxonomy against original methods papers and boundary cases.
3. Resolve high-risk claims in Section 11 before writing them as factual statements.
4. Prepare reproducible search, screening and evidence matrix appropriate to review type.

## 14. Downstream handoff brief (English)

**Topic:** [TITLE]

**Author's research objective:** [FAITHFUL SUMMARY]

**Proposed review type and audience:** [MODE, AUDIENCE]

**Scope and exclusions:** [CONSTRAINTS]

**Provisional central argument:** [THESIS / NOT PROVEN]

**Intellectual architecture:** [SECTION LOGIC + TAXONOMY]

**Decisions verified with the user:** [ONLY REAL CONFIRMATIONS, OR "None yet"]

**Assumptions and potential controversies:** [UNRESOLVED]

**Source status:** [NOT SEARCHED / DISCOVERY ONLY / PARTIALLY CHECKED]

**First actions for evidence-first-review-writer:** [PRIORITIZED VERIFICATION AND SEARCH STRATEGY. DO NOT WRITE UNSUPPORTED FACTS.]
