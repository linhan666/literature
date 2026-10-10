---
name: research-idea-concretizer
version: 1.0.0
description: Systematically transforms a vague research seed into multiple distinct, mature, falsifiable, and implementation-ready candidate research ideas.
category: research-planning
license: unspecified
entrypoint: SKILL.md
outputs:
  - structured idea portfolio
  - minimum researchable ideas
  - assumption and evidence map
  - orthogonality analysis
  - uncertainty register
  - downstream evaluation handoff
tags:
  - research-idea-generation
  - idea-concretization
  - scientific-method
  - research-planning
  - hypothesis-generation
  - agentic-science
---

# Research Idea Concretizer

## 1. Mission

Transform one vague, underspecified, or prematurely broad research seed into a **portfolio of multiple mature candidate research ideas** that are:

- conceptually distinct rather than superficial renamings;
- stated as explicit research problems rather than topics;
- grounded in an identifiable gap or unresolved bottleneck;
- associated with a falsifiable hypothesis or testable claim;
- paired with an implementable intervention or study design;
- evaluable using explicit evidence, baselines, and success/failure criteria;
- honest about assumptions, unknowns, and evidence gaps;
- ready to pass to a downstream idea-evaluation skill.

This skill is an **idea concretization and diversification skill**, not a final paper-worthiness judge. It may perform lightweight triage to remove incoherent, duplicate, or non-researchable candidates, but it must not collapse the portfolio prematurely to a single “best” idea.

---

## 2. Core principle

A vague seed is not yet a research idea.

Use the hierarchy:

**Topic → Direction → Candidate Idea → Minimum Researchable Idea (MRI) → Evaluated Research Program**

A candidate reaches MRI status only when the following tuple is explicit:

\[
I=(P,G,H,M,E,C)
\]

where:

- **P — Problem:** the concrete problem or scientific question;
- **G — Gap:** what is unresolved, inadequate, inaccessible, or untested;
- **H — Hypothesis:** a falsifiable expectation or claim;
- **M — Method / Intervention:** what will be built, changed, compared, or tested;
- **E — Evaluation:** how the claim will be tested and against what;
- **C — Contribution:** what new capability, evidence, mechanism, or knowledge would exist if successful.

No candidate may be labeled “mature” if any of these six fields remains materially undefined.

---

## 3. When to use this skill

Use when the input resembles:

- “I have an idea around X + Y.”
- “Could this technology be used for Z?”
- “I want to do something with Agent + drug discovery.”
- “This paper/model seems interesting; what research directions can grow from it?”
- “I have a broad target but no concrete research question yet.”
- “Generate several non-overlapping research ideas from this seed.”

Do **not** use as the primary skill when:

- the user already has a fully specified hypothesis, method, benchmark, and contribution and only needs execution planning;
- the user asks only for literature review, implementation, coding, or experimental protocol;
- the task is to rank already mature ideas — use a dedicated idea-evaluation skill instead.

---

## 4. Operating modes

### 4.1 Evidence-backed mode

Use when web, literature, databases, repository inspection, or connected sources are available and the user permits them.

Requirements:

1. Distinguish **seed-derived assumptions** from **externally verified facts**.
2. Do not claim a literature gap merely because it sounds plausible.
3. For novelty-sensitive claims, search specifically for semantic neighbors, not only exact keywords.
4. Record collisions, near-collisions, and unresolved uncertainty.
5. If evidence is incomplete, downgrade wording from “gap” to “candidate gap” or “unverified gap.”

### 4.2 Offline mode

Use when external verification is unavailable or not requested.

Requirements:

1. Generate candidates from the seed and known constraints.
2. Label novelty and literature-gap statements as provisional.
3. Produce a **verification queue** listing exactly what should later be checked.
4. Never present absence of knowledge as evidence of novelty.

---

## 5. Non-negotiable scientific constraints

The skill MUST:

- separate problem formulation from solution selection;
- generate multiple alternatives before ranking;
- distinguish scientific novelty from engineering integration;
- distinguish a new benchmark from a new method;
- distinguish “uses an Agent” from “requires agentic decision-making”;
- state what evidence would falsify each core hypothesis;
- include plausible baselines and alternative explanations;
- expose hidden assumptions and dependencies;
- remove candidates that differ only by model name, dataset name, target class, or tool branding unless the change alters the research question;
- preserve high-risk/high-reward candidates rather than filtering only for feasibility.

The skill MUST NOT:

- invent literature support;
- assert “no one has done this” without evidence;
- turn every idea into an LLM/Agent idea merely because an Agent is available;
- equate workflow complexity with scientific contribution;
- optimize only for benchmark score without articulating a scientific question;
- treat implementation detail as the research gap;
- overfit the output to the first interpretation of an ambiguous seed.

---

## 6. End-to-end workflow

The workflow has two macro-phases:

1. **Space Expansion** — maximize plausible interpretations and idea diversity.
2. **Idea Specification** — convert promising branches into MRIs.

Do not evaluate aggressively during Space Expansion. Evaluation too early causes premature convergence.

### Stage 0 — Normalize the seed

Extract:

- literal seed statement;
- user motivation, if stated;
- domain and intended research setting;
- hard constraints;
- assumed assets (data, models, structures, instruments, compute, wet-lab access, etc.);
- desired level of ambition;
- whether the user wants methodological novelty, scientific discovery, system-building, or a mixture.

Then rewrite the seed in one neutral sentence without adding novelty claims.

**Output:** `Normalized Seed` + `Known Constraints` + `Unknowns`.

### Stage 1 — Determine current abstraction level

Classify the seed as one of:

- **Topic:** e.g. “AI + GPCR.”
- **Direction:** e.g. “AI for GPCR virtual screening.”
- **Proto-idea:** e.g. “Use an Agent to select receptor conformations for GPCR screening.”
- **Near-MRI:** most fields exist but gaps or evaluation remain underspecified.

State what is missing before expansion.

### Stage 2 — Build the problem space

Decompose the domain into problem families and bottlenecks.

For each family, identify:

- the decision being made;
- the object being acted on;
- current failure modes;
- required evidence;
- downstream consequence of a wrong decision.

Prefer bottlenecks that are causal or decision-critical rather than cosmetic.

**Example decomposition dimensions:**

- target discovery;
- target validation;
- structure/state selection;
- binding-site discovery;
- virtual screening;
- hit triage;
- molecular generation;
- lead optimization;
- ADMET;
- synthesis planning;
- experimental design;
- literature mining.

These examples are domain-dependent, not mandatory.

### Stage 3 — Build the capability space

Describe the actual capabilities of the proposed technology, method, model, dataset, or Agent.

Separate:

- **native capability** — what the component itself can do;
- **orchestrated capability** — what becomes possible only when connected to tools/data;
- **speculative capability** — plausible but not yet demonstrated.

For AI/Agent systems, include when applicable:

- retrieval;
- reasoning;
- planning;
- code execution;
- model/tool selection;
- uncertainty estimation;
- iterative decision revision;
- autonomous experimentation;
- multimodal evidence integration.

Do not infer a capability from a model name alone.

### Stage 4 — Expand across six primary axes

Construct candidates from combinations of:

1. **Problem** — what bottleneck/question is addressed?
2. **Object** — what entity/system/population is acted on?
3. **Intervention** — what method or mechanism changes the situation?
4. **Autonomy / Decision locus** — what decisions are static, model-predicted, human-made, or autonomously selected?
5. **Evidence** — what information sources drive the decision?
6. **Evaluation** — what can prove or disprove the claimed advantage?

Optional axes, used only when they materially diversify the scientific question:

- scale;
- uncertainty regime;
- prospective vs retrospective validation;
- data-rich vs data-poor regime;
- single-task vs multi-task;
- mechanistic vs predictive objective;
- discovery vs engineering objective.

Generate an **idea fragment pool** before constructing mature candidates.

Target: normally 12–30 fragments for a moderately broad seed; fewer for narrow seeds.

### Stage 5 — Construct candidate ideas

Combine fragments into coherent candidate concepts.

Each candidate should initially be expressed as:

> **Because [candidate gap], test whether [intervention] can improve/enable/reveal [problem] for [object] using [evidence], evaluated by [evaluation].**

Reject combinations that are internally incompatible.

Target: normally 6–12 candidate ideas before clustering.

### Stage 6 — Generate adjacent ideas systematically

For each strong candidate, perform controlled transformations:

1. **Object shift** — change the scientific object while preserving the question.
2. **Task shift** — change the task while preserving the core mechanism.
3. **Bottleneck shift** — move to another causal bottleneck.
4. **Intelligence shift** — prediction → reasoning → planning → selection → discovery.
5. **Autonomy shift** — fixed workflow → adaptive workflow → autonomous decision loop.
6. **Evidence shift** — single-source → multimodal → experiment-coupled evidence.
7. **Scientific-question shift** — performance optimization → mechanism/discovery question.

Do not keep a transformed candidate unless the central research claim genuinely changes.

### Stage 7 — Cluster and orthogonalize

Cluster candidates by their **central scientific question**, not by wording.

Two candidates are likely duplicates if they share all of the following:

- same bottleneck;
- same causal claim;
- same decision locus;
- same evaluation logic;
- same expected contribution.

Changing only the model, target, dataset, software package, or implementation stack does not establish orthogonality.

For each retained candidate, state a one-line **orthogonality rationale**:

> “Distinct from Candidate B because this idea tests X, whereas B tests Y.”

Target: retain 3–8 genuinely distinct candidates.

### Stage 8 — Convert each retained candidate to MRI

For every retained candidate, fill the complete MRI record:

#### A. Research problem
A precise, bounded problem statement.

#### B. Candidate gap
What is inadequate or unknown. Mark as `verified`, `partially verified`, or `unverified`.

#### C. Core hypothesis
A falsifiable claim with direction when appropriate.

#### D. Mechanistic rationale
Why the intervention could plausibly cause the expected outcome.

#### E. Proposed method / intervention
Describe only enough to define the research logic. Avoid premature implementation lock-in unless essential.

#### F. Evidence inputs
Data, literature, models, structures, experimental readouts, tools, or observations required.

#### G. Baselines / comparators
At least one credible comparator. Prefer multiple comparator classes when needed:

- current standard practice;
- fixed workflow;
- expert/manual decision;
- simpler non-agentic model;
- ablation;
- random/naive heuristic where informative.

#### H. Evaluation design
Include:

- primary metric(s);
- success criterion;
- failure criterion;
- internal validation;
- external/prospective validation if applicable;
- statistical or repeated-run considerations where applicable.

#### I. Falsification condition
Explicitly state what result would make the core hypothesis unsupported.

#### J. Expected contribution
Choose one or more:

- new method;
- new scientific evidence;
- new mechanism;
- new benchmark/evaluation framework;
- new dataset/resource;
- new autonomous capability;
- new negative result that resolves uncertainty.

#### K. Critical assumptions
List assumptions without which the idea collapses.

#### L. Main risks
Technical, scientific, data, validation, or scope risks.

#### M. Verification queue
Facts that must be externally checked before claiming novelty or feasibility.

### Stage 9 — Lightweight maturity gate

This gate is not a full idea-evaluation rubric. It asks only whether the candidate is sufficiently specified to pass downstream.

A candidate passes only if all are true:

- Problem is specific.
- Gap is explicit and its verification status is labeled.
- Hypothesis is falsifiable.
- Method addresses the gap rather than merely adding complexity.
- Evaluation can distinguish success from failure.
- At least one credible baseline exists.
- Contribution is identifiable.
- Critical assumptions are visible.
- Candidate is non-duplicate relative to the retained portfolio.

Candidates that fail should be revised once. If still unresolved, place them in `Deferred / Needs Evidence` rather than silently dropping them.

### Stage 10 — Construct the portfolio

Unless the user requests a different strategy, organize mature candidates into a balanced portfolio:

- **Conservative:** high feasibility, narrower novelty, strong testability.
- **Balanced:** meaningful novelty with manageable technical risk.
- **Ambitious:** larger conceptual advance requiring more components/evidence.
- **High-risk / high-reward:** potentially transformative but dependent on uncertain assumptions.

A single candidate may occupy only one primary portfolio role.

### Stage 11 — Handoff to idea evaluation

End with a downstream-ready summary containing:

- candidate IDs;
- one-sentence claims;
- maturity status;
- unresolved novelty checks;
- strongest discriminating dimension among candidates;
- recommended order for formal evaluation.

Do **not** declare a winner unless explicitly asked to perform evaluation as a second task.

---

## 7. Special handling for Agent / LLM research ideas

Agent-related seeds require additional safeguards because many “Agent” ideas are actually static workflows with an LLM wrapper.

For every Agent candidate, explicitly fill:

### 7.1 Non-static decision
What decision cannot be cleanly predefined by a fixed workflow without substantial loss of capability?

### 7.2 State-dependent adaptation
What new evidence or intermediate result can cause the Agent to change its next action?

### 7.3 Action space
What real alternatives can the Agent choose among?

### 7.4 Scientific autonomy
Which scientific decisions are delegated to the Agent rather than merely executed by it?

### 7.5 Agent necessity test
Ask:

> If the Agent were replaced by a fixed rule-based or predetermined pipeline, would the central scientific claim still hold?

If yes, the idea may be a workflow paper rather than an Agent paper. Do not discard it; relabel it accurately.

### 7.6 Agent contribution vs model contribution
Separate:

- quality of the underlying predictor/model;
- quality of planning/orchestration;
- value of adaptive decisions;
- value of tool use;
- value of evidence integration.

Evaluation must not attribute predictor gains to agentic reasoning without ablation.

---

## 8. Novelty and literature-collision protocol

When evidence-backed mode is available, perform a collision check for each MRI.

Search at three semantic levels:

1. **Exact collision:** same task + same mechanism + same object + same contribution.
2. **Near collision:** same central claim but different implementation/object.
3. **Conceptual ancestor:** prior work establishing most of the idea’s logic.

For each candidate, assign one status:

- `No obvious collision found` — not proof of novelty;
- `Near-neighbor exists`;
- `Strong collision risk`;
- `Novelty unresolved`.

Never use “novel” as a binary factual claim unless the search scope is adequate and the wording remains appropriately cautious.

If collision occurs, transform the idea by changing the **scientific question**, not merely by swapping a model or dataset.

---

## 9. Evidence discipline

Every important statement should be classified conceptually as one of:

- `User-provided fact`
- `Verified external fact`
- `Reasoned inference`
- `Speculative hypothesis`
- `Unknown / requires verification`

The final output does not need to repeat these labels on every sentence, but the distinction must govern wording.

Use:

- “Evidence indicates…” for verified facts;
- “This suggests…” for inference;
- “We hypothesize…” for testable speculation;
- “This requires verification…” for unresolved claims.

---

## 10. Quality controls

Before finalizing, run these checks.

### 10.1 Topic-to-idea check
Could the candidate still be described as only “X + Y”? If yes, it is too broad.

### 10.2 Solution-first check
Did the candidate begin from a favored model and invent a problem afterward? If yes, reformulate from the problem.

### 10.3 Static-workflow check
For an Agent idea, is the workflow fully predetermined? If yes, remove or downgrade the Agent framing.

### 10.4 Benchmark-only check
Is the entire contribution “higher metric on benchmark X”? If yes, identify the scientific or methodological claim behind the gain.

### 10.5 Falsifiability check
Can a plausible experimental result make the hypothesis unsupported? If not, rewrite the hypothesis.

### 10.6 Baseline check
Would a simpler method plausibly solve the same task? If yes, include it.

### 10.7 Orthogonality check
Do two ideas differ only by object/model/dataset? If yes, merge or transform.

### 10.8 Contribution check
If successful, what new thing becomes known or possible? If no clear answer, the candidate is immature.

### 10.9 Evidence-gap check
Are novelty or feasibility claims resting on unverified assumptions? If yes, record them in the verification queue.

### 10.10 Scope check
Can the idea be tested within a bounded study? If not, split into sub-ideas.

---

## 11. Default output format

Use the following structure unless the user requests another format.

### 1. Normalized seed
- Seed
- Current abstraction level
- Known constraints
- Key unknowns

### 2. Expansion map
- Problem space
- Capability space
- Six-axis decomposition
- Major idea fragments

### 3. Candidate landscape
A compact table of 6–12 pre-cluster candidates.

### 4. Orthogonalized mature candidates
For each retained candidate:

- ID and short title
- One-sentence claim
- Problem
- Gap + verification status
- Hypothesis
- Mechanistic rationale
- Method
- Evidence inputs
- Baselines
- Evaluation
- Falsification condition
- Contribution
- Critical assumptions
- Main risks
- Verification queue
- Orthogonality rationale

### 5. Portfolio view
Map retained candidates to:

- Conservative
- Balanced
- Ambitious
- High-risk/high-reward

### 6. Deferred / needs evidence
Keep promising but immature branches visible.

### 7. Handoff to idea evaluation
List the candidates ready for formal scoring/ranking.

---

## 12. Compact response mode

If the user requests a concise result, retain scientific structure but compress to:

1. seed interpretation;
2. 3–5 mature ideas;
3. for each: `Problem → Gap → Hypothesis → Method → Evaluation → Contribution`;
4. one orthogonality note;
5. verification queue.

Do not omit falsifiability merely to shorten the response.

---

## 13. Failure modes and recovery

### Failure: seed is too vague
Do not ask the user to fully define it. Produce multiple interpretations and label them.

### Failure: too many candidates
Cluster by scientific question, then retain the most orthogonal representatives.

### Failure: candidates converge on one solution family
Force adjacent-idea transformations, especially bottleneck shift and scientific-question shift.

### Failure: everything becomes an Agent
Re-run from problem space with `Agent` removed, then reintroduce it only where adaptive scientific decision-making is necessary.

### Failure: literature collision invalidates novelty
Preserve the problem, change the causal claim or unresolved bottleneck; do not simply swap model names.

### Failure: no credible evaluation exists
Demote candidate maturity and add an evaluation-design task to the verification queue.

### Failure: wet-lab or expensive validation dominates feasibility
Create paired variants: computationally bounded proof-of-concept and full prospective validation.

---

## 14. Completion criteria

The skill is complete only when it has produced:

- one normalized seed;
- one explicit problem/capability decomposition;
- a candidate landscape;
- 3–8 orthogonal mature or near-mature candidates where the seed permits;
- complete MRI records for retained candidates;
- explicit falsification conditions;
- a verification queue;
- a balanced portfolio view;
- a downstream idea-evaluation handoff.

If the seed genuinely supports fewer than three defensible ideas, state that rather than fabricating diversity.
