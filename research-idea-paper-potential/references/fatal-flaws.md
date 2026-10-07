# Fatal Flaws and Gating Risks

A fatal flaw is a problem that should not be averaged away by strong scores elsewhere.

## F1 — No authentic research gap

The idea is only a topic, engineering build, or exact combination that has no meaningful unresolved scientific/technical question.

**Repair:** define the unresolved uncertainty or failure mode and verify it against prior work.

## F2 — No central scientific claim

The project can list tasks but cannot state a falsifiable conclusion of the form:

`We demonstrate that ______.`

**Repair:** reformulate around a claim and define what observation would falsify it.

## F3 — Claim is not falsifiable or is circular

Examples:
- "the system is intelligent because it behaves intelligently";
- success criteria are defined after seeing results;
- the hypothesis cannot lose.

**Repair:** predefine measurable outcomes and failure conditions.

## F4 — Evidence cannot distinguish the claim from alternatives

Examples:
- performance gain may be due to more compute/data/parameters;
- biological effect may be off-target;
- benchmark gain may be leakage;
- Agent success may come from a fixed workflow rather than autonomous reasoning.

**Repair:** design a discriminating experiment, matched control, perturbation, ablation, rescue, or equivalent.

## F5 — Core decisive study is infeasible

The key evidence depends on inaccessible samples, unavailable data, unrealistic compute, missing expertise, or an unresolvable experimental bottleneck.

**Repair:** obtain pilot access, substitute a valid proxy, narrow the claim, or redesign the project.

## F6 — Success produces no meaningful new knowledge or capability

The best-case outcome is only "we implemented the system" or "metric improved slightly" without a significant methodological, empirical, mechanistic, or conceptual contribution.

**Repair:** identify what changes in scientific understanding or practice if the project succeeds.

## F7 — Prior art collapses the novelty claim

A close prior work already demonstrates the same central claim under comparable conditions.

**Repair:** identify a nontrivial unresolved dimension, change the claim, or stop.

## Positioning-limiting Agent gates

These do not always kill the project, but they can kill the **Agent-paper positioning**.

### A1 — Agent unnecessary

A static workflow, script, RAG pipeline, or ordinary AutoML procedure can solve the task with essentially the same decision structure.

**Action:** position as a workflow/system paper unless a genuine dynamic decision problem is introduced and evaluated.

### A2 — Automation is mislabeled as scientific autonomy

The system executes researcher-defined steps but does not make substantive scientific decisions.

**Action:** reduce autonomy claims or redesign the agent to choose hypotheses, evidence, methods, experiments, or strategy based on observations.

### A3 — Discovery claim is actually retrieval or synthesis

The system retrieves known facts or combines existing evidence but does not produce independently validated new knowledge.

**Action:** position as literature-mining/synthesis methodology, or add a prospective discovery and validation stage.

## Decision labels

- **Go** — no blocking flaw; strongest risks are manageable.
- **Conditional Go** — promising, but one or more gates require early verification before major investment.
- **Reframe** — the work may be publishable, but the current scientific or Agent positioning is not defensible.
- **No-Go** — central gap/claim/feasibility/novelty failure makes the current project a poor research investment.
