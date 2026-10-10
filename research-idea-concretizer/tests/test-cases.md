# Behavioral Test Cases

These are qualitative tests for evaluating Skill behavior.

## Test 1 — Extremely vague seed

**Input:** “AI + GPCR.”

**Expected behavior:**

- classify as Topic;
- expand problem and capability space;
- generate several distinct directions;
- do not claim novelty;
- produce 3–8 MRIs only after clustering.

**Failure:** outputs one arbitrary idea immediately.

## Test 2 — Model-first seed

**Input:** “Use Model Z for molecular generation.”

**Expected behavior:**

- identify solution-first framing;
- ask what bottleneck/capability match exists through decomposition, without requiring user clarification;
- create candidates tied to different scientific questions.

**Failure:** “Fine-tune Model Z and benchmark it” as the only idea.

## Test 3 — Fake Agent idea

**Input:** “Create an Agent that always runs docking, MM/GBSA, then MD.”

**Expected behavior:**

- identify the pipeline as static;
- label Agent necessity low unless state-dependent decisions are added;
- preserve workflow-paper interpretation if scientifically valid.

**Failure:** praises it as an autonomous Agent without analysis.

## Test 4 — Duplicate ideas

**Input:** Generate ideas for a screening Agent.

**Candidate fragments:**
- choose AutoDock Vina;
- choose Glide;
- choose GOLD.

**Expected behavior:** merge under “docking-engine/protocol selection” unless different engine families imply a different scientific hypothesis.

## Test 5 — Unverified novelty

**Input:** “No one has ever used multimodal evidence for target selection.”

**Expected behavior:** treat as a user assertion that requires verification; do not repeat as fact.

## Test 6 — No obvious evaluation

**Input:** “Use an LLM to discover unknown mechanisms.”

**Expected behavior:** keep as near-mature/deferred until an evaluation/falsification design is specified.

## Test 7 — High-risk idea preservation

**Input:** broad seed with one feasible engineering idea and one transformative but uncertain discovery idea.

**Expected behavior:** retain both in different portfolio roles rather than filtering only for feasibility.

## Test 8 — Literature collision

**Input:** a candidate strongly resembles known prior work.

**Expected behavior:** mark collision risk and transform the central scientific question rather than merely swapping a model.
