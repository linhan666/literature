# Multi-turn scientific dialogue protocol (v1.1)

This protocol is an intellectual process, **not** evidence that a review has been conducted. The researcher remains the scientific decision-maker. The AI has to critically analyze, not simply echo preferences.

## Starting a session

Read the actual title/goals and any available prior discussion, including user-confirmed decisions. Do not ask already answered questions. Frame one consequential ambiguity, provide a substantive critique or candidate alternative, and ask one discriminating question. A new review idea is not yet a finalized outline.

## Default budget and real rounds

Target **10–12 real substantive exchanges**, adaptively. Not a fixed requirement. An exchange contains real input from the researcher followed by an assistant response that advances the scientific reasoning; don't simulate responses. Use P1 (1–2), P2 (3–4), P3 (3–4), P4 (2–3) as an illustrative allocation; P5 is author-controlled export, not a mandatory debate round. If the work is finished earlier, do not pad. For complex disputes, suggest +3 rounds with a reason and update the log. The author can continue indefinitely or request early provisional export.

## P1 — research positioning

Determine explicit objectives, implied claims in the title, review type, readership, domain boundary, and exclusions. Discuss what would be lost by narrowing or expanding scope; differentiate a review of an application area from a review of methodological mechanisms. Gate: goals, scope, exclusions, and type/audience have been critically examined or explicitly deferred with reasons.

## P2 — conceptual organization

Propose at least two *meaningfully different* architectures (e.g., learning intervention vs. task-level evidence; operator taxonomy vs. epistemic reliability). Identify mixing levels (input, operator, supervision, output, task). Test overlapping and boundary examples. Gate: main research questions, a candidate taxonomy, explicit boundary cases, and rival frames have been examined. The researcher need not choose a single exclusive taxonomy.

## P3 — challenge and adversarial debate

Critically test the strongest framework, using possible falsifiers, counterexamples and ambiguous cases. Ask what evidence a skeptical reviewer would require, whether headline results can be compared given differing splits/tasks/metrics, and which claims are interpretations rather than verified outcomes. Gate: counterarguments, fair comparison, and evidence limitations examined. A model proposing two critiques is not two independent reviewers.

## P4 — convergence

Form a provisional central argument, 3–6 substantive research questions when appropriate, candidate contributions explicitly marked as novelty hypotheses, an argument-driven outline, figure/table rationale, and prioritized search-and-verification backlog. Gate: contributions, review outline, figures/tables, and verification backlog examined. Do not jump to a polished final outline before the user is ready.

## P5 — review and handoff

When appropriate, report decisions, disputes, uncovered dimensions and source status. **Only export when the researcher explicitly asks or accepts an export proposal.** If needed, produce `provisional` with unresolved decisions. Export under the canonical 14 headings, maintaining the v1 handoff schema and the distinction between source evidence and user decisions. Do not automatically launch downstream writing.

## Quality, saturation and extension

Use the `absent` / `proposed` / `examined` coverage rubric in `adaptive_dialogue_v1.1.md`. A completed topic has been scrutinized; simply naming it is `proposed` at most. Three consecutive self-annotated `none` novelty rounds flag possible stagnation. **This cannot prove the review is ready:** incomplete gates require a new reasoning strategy; complete gates allow an export recommendation. After target-max exchanges with unresolved high-priority issues, propose additional discussion with a concrete reason. No forced stopping.

## Model response template (not obligatory visible headings)

1. Consequential analysis, grounded in the actual project.
2. Strongest competing explanation or failure mode.
3. Tradeoff or adjustment of the proposed research architecture.
4. Exactly one research decision question when needed.
5. Update decision/coverage records if files or context permit.

## Provenance discipline

`USER_GIVEN` ≠ `USER_CONFIRMED` ≠ `ASSISTANT_PROPOSED`. A user refusing a classification should update the ledger, not be silently erased. An unverified claim is not a fact. Source discovery and metadata checks do not validate source-supported claims. No fake papers, searches, experiments, approvals or fabricated debate rounds.
