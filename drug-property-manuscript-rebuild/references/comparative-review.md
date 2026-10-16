# Comparative review and calibration

## Compare the same function, not generic prestige

Use a reference Introduction paragraph for the same rhetorical job, a method explanation for the same level of abstraction, and a display serving the same information need. Differences in topic, word budget, figure complexity, or evidence make raw similarity comparisons misleading.

For each selected output unit, record:

```text
Output locator:
Reference card / same-function source locator:
Old-version defect:
Implemented change:
Evidence in the actual revised text or render:
Remaining defect and feasible fix:
Fact integrity: preserved / conflict / unchecked
Decision: keep / revise / revert / insufficient evidence
Reviewer and review mode:
```

A defect must be locatable: e.g., “the first two sentences repeat field-level motivation, while the intended methodological difficulty appears only in sentence six.” Do not write “not sufficiently academic” without a concrete reason.

## Two axes, not one inflated score

**Scientific fidelity.** Numbers, task, implementation, uncertainty, citations, and claim strength remain accurate. A stylistic improvement that introduces a scientific error fails.

**Communicative craft.** Judge argument progression, information selection, technical explanation, prose specificity, visual organization, table scanability, and figure–text complementarity. Compare to relevant reference behavior and reader needs.

Do not create a single “top-tier score,” mandatory adjective count, target sentence length, or unvalidated similarity threshold. Descriptive metrics may locate a problem; they do not certify prose quality. Scores, if the user requests them, require anchored explanations and cannot be treated as acceptance probabilities.

## Reader tasks

For a prose span, ask a reader to identify the actual question, central proposition, evidence, and permissible interpretation. For a diagram, ask them to trace the actual inputs and explain the distinctive computation. For a quantitative display, ask what changed, under what comparison, and how uncertainty is represented.

Prefer real user/editor feedback on the pilot. Model-simulated reader answers are internal checks, not proof of reader comprehension. Do not assume user approval from silence.

## Separate a controlled workflow test from exemplar comparison

To test whether this skill improves writing, keep the same study facts, baseline files, word/page limits, time/tool budget, and model configuration where feasible. Compare the baseline writing workflow and v2 on the same units. Hide version labels from human reviewers, counterbalance order, and record both preference and specific defects.

Repeat across several paragraph/display functions rather than declaring success from one attractive figure. Record factual errors as failures even when a version is preferred. Results from one manuscript are local evidence, not a general benchmark.

Using another published paper as the comparison is useful calibration, not a controlled A/B test: its content and evidence differ. An optional held-out paper provides another reference point, not an objective gold standard. Same-model self-review is not independent review; multiple role prompts are not multiple human experts.

## Revision and stopping

Fix the highest-impact identified defect first. Re-check facts after any scientific wording change. Record whether the target defect was actually removed. If two rounds only produce synonyms, change the organizing decision rather than requesting “more polished” text again.

Respect the user's scope and budget. Stop a calibration-only request after actual pilots and comparisons. For a full-manuscript request, continue through the paper, reporting unresolved limitations instead of silently certifying success.

## Integrated acceptance record

Verify what was truly read, inspected, recalculated, rendered, and compiled. Keep filenames/commands where applicable. `NOT_RUN` is not `PASS`. File integrity or schema tests do not measure writing improvement.

Deliver a concise change report: main improvements, remaining presentation gaps, evidence gaps, and exact validation limits. Do not imply that a successful internal review establishes top-journal quality or publication readiness.
