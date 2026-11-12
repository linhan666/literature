# Adaptive dialogue engine v1.1 — field guide

## Operating contract

A round is one **genuine researcher input plus an assistant response** containing substantive analysis. The target 10–12 rounds is a planning budget only. Do not simulate missing user responses, force a minimum, or artificially lengthen an adequate discussion. Researcher instructions supersede suggested budgets; early export is allowed and marked provisional when appropriate.

## Phase gates and coverage rubric

Each coverage dimension is recorded as:

- `absent` (0): topic has not been addressed.
- `proposed` (1): a candidate formulation was offered but not rigorously challenged.
- `examined` (2): boundaries, tradeoffs, counterexamples, or evidence needs have been analyzed in a substantive turn, even if the final author decision remains open.

The dimensions and phase mapping (the tracker uses these exact names):

| Phase | Coverage dimension | Sufficient substantive examination |
| --- | --- | --- |
| P1 | `research_goals` | Faithfully separate stated aims and inferred aims |
| P1 | `scope` | Discuss inclusion boundaries and what their changes imply |
| P1 | `exclusions` | Name material exclusions or justify none |
| P1 | `review_type_and_audience` | Compare viable review genres and intended readers |
| P2 | `central_questions` | Questions distinguish scientific and editorial problems |
| P2 | `taxonomy` | Explicit categories/axes and definitions tested |
| P2 | `taxonomy_boundaries` | Nonexclusive relationships, overlaps and counterexamples |
| P2 | `competing_frameworks` | At least two truly different architectures compared |
| P3 | `counterarguments` | Serious scientific counterarguments and falsifiers |
| P3 | `fair_comparison` | Task, dataset, split, metric, information access comparability |
| P3 | `claim_evidence_limits` | Empirical findings vs inference vs hypotheses separated |
| P4 | `contributions` | Candidate contributions with novelty verification plan |
| P4 | `review_outline` | Coherent argument sequence, not merely paper list |
| P4 | `figures_and_tables` | Each proposed artifact has an analytical job |
| P4 | `verification_backlog` | Priority, search seeds, counterevidence and audit plan |

**Gate output**: `ready_for_researcher_review` means all dimensions logged `examined`. It is not a quality certificate, not an assertion of user approval, and not a claim that the literature is verified. A critical open dispute blocks a final-review suggestion (not an explicit author-requested provisional export). If a dimension genuinely belongs downstream, log the explicit deferral in the notes and handoff; do not falsely set it to `examined`.

## Adaptive process

At each round:
1. Identify the single most consequential unresolved issue.
2. Do new scientific work: analysis, criticism, counterexample, comparison or revised framework.
3. Ask at most one consequential decision question, unless instructed otherwise.
4. Carry forward genuine decisions and reversals; label sources appropriately.
5. Log the round as `substantial`, `incremental`, or `none` *only from actual content*. Annotate coverage and open/closed critical issues separately.

After 2–3 rounds, check which gate needs work and show a compact status *only if it helps decision-making*. Do not make the conversation an administrative form.

At 10–12 rounds: if all relevant gates have been examined, present candidate convergence and ask whether to review/export; if important gates remain, name them and propose +3 rounds with precise goals. A target is neither a hard stop nor automatic escalation.

If three consecutive recorded rounds were `none`, the tracker flags **possible stagnation**. When gate incomplete, change lenses and challenge a different assumption. When ready, suggest final review. Lack of apparent novelty may reflect poor questioning rather than adequate synthesis.

## Final user-controlled review gate

Before proposing export, check:
- Goals and scope faithfully expressed; key constraints traced to actual user statements.
- Taxonomy boundaries stress-tested and alternatives compared.
- Critical criticisms addressed or explicitly deferred.
- Candidate novelty claims NOT presented as verified discoveries.
- Core decisions user-confirmed where applicable; assistant recommendations not misattributed.
- Evidence verification queue and unresolved issues prioritized.

The final step is the researcher's decision. Never auto-export at round 12 or after a saturation flag. An explicit user request to export always takes priority: export with `provisional` status if epistemic or decision gaps remain.

## Tool semantics and limits

`scripts/dialogue_tracker.py` records researcher/assistant **self-reported annotations** in `notes/dialogue_state.json`. It is not NLP sentiment/similarity inference and cannot validate whether a coverage assertion is true. `handoff.py` checks file structure and metadata, not research sufficiency.

Quick example:

```bash
python .agents/skills/review-dialogue-architect/scripts/dialogue_tracker.py init --project .
python .agents/skills/review-dialogue-architect/scripts/dialogue_tracker.py record --project . --phase P1-positioning --novelty substantial --user-input "Topic and objectives provided" --analysis "Scope ambiguity and candidate distinction discussed"
python .agents/skills/review-dialogue-architect/scripts/dialogue_tracker.py coverage --project . --dimension scope --level examined --note "Discussed which drug-discovery stages to exclude"
python .agents/skills/review-dialogue-architect/scripts/dialogue_tracker.py status --project .
```

An automated check marked `ready_for_researcher_review` is **not** permission to write or submit the review; source verification and scholarly judgment belong downstream.
