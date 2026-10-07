# Skill Evaluation Test Cases

Use these cases to test whether the skill behaves consistently.

## T1 — Feature-list masquerading as research

**Prompt:**
> I want to build an LLM system with RAG, memory, MCP tools, docking, MD, and a dashboard for drug discovery. Is this a good paper?

**Expected:**
- do not reward component count;
- classify as not yet research-shaped or weakly research-shaped;
- demand problem/gap/claim;
- flag possible F2/F6;
- if called an Agent, evaluate necessity separately.

## T2 — Strong question, infeasible validation

**Prompt:**
> I have a new hypothesis that requires a rare human tissue cohort I cannot access and no valid proxy exists.

**Expected:**
- high potential scientific importance may coexist with low paperability;
- feasibility can trigger F5;
- recommendation should be Conditional Go/Reframe/No-Go depending on alternatives.

## T3 — Incremental metric gain

**Prompt:**
> My model improves AUROC from 0.910 to 0.916 on one random split. Can this be a high-quality paper?

**Expected:**
- attack statistical robustness, split validity, tuning fairness, and scientific meaning;
- quality ceiling should remain limited without stronger novelty/insight/generalization.

## T4 — Evidence-gap paper

**Prompt:**
> Everyone uses LLM Agents for biomedical literature mining, but no benchmark tests whether they recover all known disease-target associations with calibrated completeness and citation accuracy.

**Expected:**
- recognize evidence-gap/benchmark paper potential;
- not require a new model architecture;
- emphasize gold-standard construction, coverage, leakage, and evaluation validity.

## T5 — Fixed Agent workflow

**Prompt:**
> My Agent always searches PubMed, extracts targets, docks them, runs 100 ns MD, then writes a report.

**Expected:**
- low Agent necessity and autonomy;
- recommend workflow/system positioning;
- do not call fixed sequential execution autonomous science.

## T6 — Adaptive scientific Agent

**Prompt:**
> The Agent generates competing hypotheses, chooses the next evidence source to maximize expected information gain, can stop unpromising branches, and designs a prospective validation test.

**Expected:**
- potentially high necessity/autonomy;
- still require matched baselines and validated discovery;
- do not award high discovery score without independent validation.

## T7 — Already-solved idea

**Prompt:**
> I want to be the first to apply method X to Y.

Assume literature search reveals multiple prior studies already did this.

**Expected:**
- trigger F7;
- lower novelty/gap scores;
- propose reframe or No-Go rather than rationalizing novelty.
