---
name: research-idea-paper-potential
description: Evaluate whether a research idea can become a defensible research paper or a high-quality research paper. Use for research idea triage, project go/no-go decisions, paper-positioning analysis, reviewer-style stress tests, and Scientific Agent ideas requiring Agent necessity, Scientific autonomy, and Scientific discovery value assessment.
---

# Research Idea Paper Potential

Evaluate ideas as research claims, not as feature lists or implementation plans.

## Core principle

A research-worthy idea must support a clear chain:

`important question -> authentic knowledge gap -> falsifiable claim -> discriminating evidence -> defensible conclusion`

A high-quality paper additionally needs unusually strong significance, novelty, explanatory depth, evidence, and reach.

For Scientific Agent ideas, separately evaluate:

`Agent necessity -> Scientific autonomy -> Scientific discovery value`

Do not let engineering complexity substitute for scientific contribution.

## Inputs

Accept incomplete ideas. Extract what is known and mark missing items as unknown instead of inventing them.

Useful inputs include:
- problem or research question;
- proposed hypothesis or central claim;
- target domain and intended audience/venue;
- related work already known;
- proposed method/system;
- data, experiments, benchmarks, controls, or wet-lab validation;
- resources, time, compute, samples, collaborators, or equipment;
- for Agent ideas: decisions delegated to the agent, tools available, adaptive loops, and expected discoveries.

If the user provides only a short idea, perform a provisional evaluation and explicitly list the evidence needed to raise confidence.

## Evidence policy

Never assert novelty, an open knowledge gap, or state-of-the-art status from intuition alone.

When literature/web/database access is available and the decision materially depends on current prior art:
1. verify the closest prior work;
2. search both direct and adjacent formulations of the idea;
3. distinguish peer-reviewed work, preprints, benchmarks, software systems, and relevant patents when appropriate;
4. record whether each major judgment is verified, partially verified, or provisional.

When external verification is unavailable, label novelty and gap judgments as provisional.

## Workflow

### 1. Normalize the idea

Rewrite the idea internally into six fields:
1. **Problem** — what important problem is being solved?
2. **Gap** — what is currently unknown, inadequate, contradictory, or unvalidated?
3. **Claim** — complete: `We hypothesize/demonstrate that ______.`
4. **Intervention or method** — what changes relative to prior work?
5. **Evidence** — what observations could support or refute the claim?
6. **Payoff** — if successful, what knowledge, capability, or decision changes?

Do not confuse "what we build" with "what we demonstrate".

### 2. Determine research shape before scoring

Classify the current idea as one of:
- **Not yet research-shaped** — mainly a topic, feature list, application, or implementation plan;
- **Research-shaped but weakly supported** — a claim exists but gap/evidence is uncertain;
- **Defensible research candidate** — a falsifiable claim and credible evidence path exist;
- **Strong paper candidate** — multiple dimensions are strong and major reviewer objections are addressable;
- **High-quality paper candidate** — significance, novelty, evidence, explanatory depth, and reach are jointly strong;
- **Exceptional but high-risk** — potential impact is very high but feasibility/evidence risk is substantial.

### 3. Score the core dimensions

Read `references/core-rubric.md`.

Score every dimension from 0 to 5 and provide a one-sentence rationale plus confidence:
- Problem importance
- Knowledge gap authenticity and clarity
- Novelty
- Scientific claim strength and falsifiability
- Mechanistic or conceptual insight
- Evidence strength and claim-evidence alignment
- Alternative-explanation discrimination and controls
- Generalizability / external validity
- Feasibility
- Reproducibility / robustness
- Narrative coherence / contribution clarity

Do not use a high average to hide a critical weakness.

### 4. Compute two distinct headline scores

Use `references/scoring-model.md`.

Report:
- **Paperability Score /100** — likelihood that the idea can become a defensible research paper with the proposed evidence path.
- **High-Quality Potential Score /100** — ceiling for becoming a strong/important research paper if executed well.

These scores answer different questions. Never collapse them into a single number.

If desired, use `scripts/score_idea.py` with a JSON file following `assets/evaluation-schema.json`.

### 5. Run fatal-flaw gates

Read `references/fatal-flaws.md`.

A fatal flaw overrides the total score. For each triggered gate, state:
- why it is fatal or positioning-limiting;
- what evidence or redesign would remove it;
- whether the idea should be **Go**, **Conditional Go**, **Reframe**, or **No-Go**.

### 6. For Agent or autonomous-science ideas, run the Agent module

Read `references/agent-specific-rubric.md`.

Score separately:
- **Agent necessity /8**
- **Scientific autonomy /10**
- **Scientific discovery value /12**

Also answer the three mandatory questions:
1. `Why does this require an agent rather than a static workflow, script, RAG pipeline, or AutoML system?`
2. `Which scientific decisions are made by the agent rather than predefined by researchers?`
3. `What new scientific knowledge can be generated and independently validated?`

If Agent necessity is weak, recommend positioning as a workflow/system paper rather than inflating the Agent claim.
If autonomy is weak, do not call the system an autonomous scientist.
If discovery value is weak, position the contribution as an Agent method, evaluation, or benchmark paper rather than a scientific-discovery paper.

### 7. Perform a reviewer attack

Read `references/reviewer-attack.md`.

Identify at least the three strongest plausible reviewer attacks. For each, provide:
- attack;
- why a reviewer would care;
- experiment/analysis needed to answer it;
- residual risk after the fix.

Always include the strongest alternative explanation for the expected result.

### 8. Define the minimum decisive evidence package

Do not recommend "more experiments" generically. Specify the smallest evidence set that would make the central claim defensible.

Separate:
- **must-have evidence**;
- **high-value strengthening evidence**;
- **nice-to-have evidence**.

Prioritize experiments by information gain: prefer tests that discriminate between competing explanations.

### 9. Give a development path

End with concrete actions:
- what to verify first;
- what to pilot before committing major resources;
- what would cause a pivot or stop;
- the strongest paper positioning currently justified;
- what would need to become true for a high-quality-paper positioning.

## Output contract

Use `assets/report-template.md` unless the user requests another format.

The final report must contain:
1. Executive verdict;
2. Normalized research question, gap, claim, and payoff;
3. Core dimension table with scores, confidence, and evidence basis;
4. Paperability Score and High-Quality Potential Score;
5. Fatal flaws / gating risks;
6. Agent-specific module when applicable;
7. Reviewer attack;
8. Minimum decisive evidence package;
9. Go / Conditional Go / Reframe / No-Go recommendation;
10. Highest defensible paper positioning now and the conditions required to raise it.

## Calibration rules

- A new combination of existing modules is not automatically novel.
- "First to apply X to Y" is usually application novelty unless it reveals a new phenomenon, mechanism, capability, or principle.
- Benchmark gains without a causal or methodological explanation should not receive high mechanistic/conceptual scores.
- One dataset, one target, or one case study cannot justify a broad principle without external validation.
- More experiments do not compensate for a weak central claim.
- A sophisticated system with no discriminating experiment is not a strong scientific paper.
- Negative results can still support a good paper if they resolve an important uncertainty with rigorous evidence.
- Feasibility constrains paperability; it does not by itself determine scientific importance.
- For Agent systems, automation is not the same as scientific autonomy.

## Final self-check

Before completing the evaluation, verify:
- Is the central claim explicit and falsifiable?
- Is the alleged gap actually verified or clearly labeled provisional?
- Does each proposed experiment have an epistemic role?
- Can the evidence distinguish the claim from the strongest alternative explanation?
- Are the score and verdict consistent with any fatal flaws?
- Are paperability and quality ceiling separated?
- For Agent ideas, is the Agent actually necessary and scientifically autonomous?
- Does the proposed contribution produce new knowledge, not merely a more complex workflow?
