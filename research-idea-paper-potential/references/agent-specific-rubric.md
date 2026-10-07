# Scientific Agent Rubric

Use this module when the idea claims an Agent, autonomous scientist, AI scientist, scientific reasoning agent, or adaptive multi-tool research system.

Report these scores **separately** from the 100-point core scores.

## 1. Agent necessity /8

**Core question:** Why does this problem require an Agent rather than a static workflow, script, RAG pipeline, or AutoML system?

Rate the underlying 0–5 anchor, then scale to 8 points.

- **0** — "Agent" is only branding; no agentic behavior.
- **1** — chat interface or sequential tool caller over a fixed workflow.
- **2** — limited branching or tool selection, mostly predefined.
- **3** — meaningful dynamic task decomposition or conditional tool/evidence selection.
- **4** — strategy must adapt to observations, failures, uncertainty, or heterogeneous problem instances.
- **5** — open-ended task cannot be reasonably specified as a static workflow; agentic planning and revision are central to solving it.

### Necessity test

Ask:

`Remove the agent. What scientifically important capability breaks?`

Weak answer:
> A human would need to run the same scripts manually.

Strong answer:
> The system would lose the ability to decide which evidence is needed, revise hypotheses after contradictory observations, and select the next experiment based on information gain.

## 2. Scientific autonomy /10

**Core question:** Which scientific decisions are made by the Agent rather than predefined by researchers?

Suggested autonomy ladder:

- **Level 0 — Execution:** runs specified tasks.
- **Level 1 — Tool selection:** chooses among provided tools.
- **Level 2 — Method/strategy selection:** compares methods and chooses a strategy based on evidence.
- **Level 3 — Experiment design:** chooses controls, tests, or analyses needed to resolve uncertainty.
- **Level 4 — Hypothesis generation/refinement:** proposes and revises scientific hypotheses.
- **Level 5 — Closed-loop science:** observe -> hypothesize -> design -> execute -> analyze -> revise.

Score anchor:
- **0** — no autonomy beyond execution.
- **1** — limited tool routing.
- **2** — method selection but scientific objectives remain fully predefined.
- **3** — meaningful experiment/analysis design or evidence prioritization.
- **4** — hypothesis refinement plus adaptive validation.
- **5** — closed-loop scientific decision-making with bounded but substantive independence.

Scale to 10 points.

### Important distinction

`automation != scientific autonomy`

Running 10,000 docking jobs automatically can be high automation and near-zero scientific autonomy if all scientific choices were fixed by the researchers.

## 3. Scientific discovery value /12

**Core question:** What new scientific knowledge can the system generate and independently validate?

Discovery ladder:

- **Level 0 — Retrieval:** finds known facts.
- **Level 1 — Synthesis:** integrates or summarizes known evidence.
- **Level 2 — New prediction:** proposes a nontrivial testable hypothesis/prediction.
- **Level 3 — Validated finding:** prediction is independently validated computationally or experimentally.
- **Level 4 — New mechanism/capability:** reveals a mechanism, failure mode, or capability not established before.
- **Level 5 — General principle:** discovers a reusable scientific principle or relationship beyond a single case.

Score anchor:
- **0** — no new knowledge.
- **1** — retrieval/summarization only.
- **2** — synthesis or weakly novel prediction.
- **3** — clear prospective prediction with credible validation plan.
- **4** — independently validated new finding/mechanism.
- **5** — validated generalizable discovery or principle.

Scale to 12 points.

## Suggested interpretation of the 30-point Agent module

- **0–9** — mostly workflow automation; Agent positioning weak.
- **10–16** — useful agentic system, but limited scientific autonomy/discovery.
- **17–22** — credible Scientific Agent contribution.
- **23–26** — strong Scientific Agent paper potential.
- **27–30** — exceptional on paper; verify that autonomy and discovery claims survive ablation and prospective validation.

## Positioning rules

- **Low necessity + strong engineering:** call it a workflow/system/tool, not an Agent paper.
- **High necessity + low autonomy:** call it an adaptive orchestration system, not an autonomous scientist.
- **High autonomy + low discovery value:** strongest contribution may be Agent methodology/evaluation, not science discovery.
- **High discovery value without proof that the Agent caused the gain:** include ablations comparing fixed workflow, human-designed workflow, and Agent-driven strategy.

## Minimum Agent baselines

When applicable, compare against:
1. static deterministic workflow;
2. LLM workflow with the same tools but fixed plan;
3. Agent without adaptation/memory/reflection/planning component under test;
4. human-designed or expert baseline;
5. equal-budget/equal-tool baseline.

Agent claims require evidence that the Agent-specific decision process contributes beyond access to tools or extra compute.
