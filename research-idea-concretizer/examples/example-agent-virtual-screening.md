# Example — Agent + Virtual Screening

## Seed

“Build an Agent for GPCR virtual screening.”

## Abstraction level

Direction, not yet a research idea.

## Example problem-space branches

- receptor conformation selection;
- docking-engine/protocol selection;
- adaptive rescoring;
- uncertainty-driven hit triage;
- evidence-guided termination or escalation of computation.

## Example orthogonal candidates

### C1 — Evidence-guided receptor-state selection

**Problem:** GPCR screening performance depends strongly on receptor state/conformation, yet structure selection is often fixed before screening.

**Candidate gap:** Target-specific structure selection may require integrating ligand, structural, and pharmacological evidence rather than applying one static choice rule.

**Hypothesis:** An adaptive evidence-integration system can select receptor conformations that yield better retrospective enrichment than fixed single-structure or naive ensemble baselines.

**Method:** Retrieve candidate receptor structures, integrate structural and literature evidence, run bounded retrospective docking, inspect enrichment and pocket constraints, then choose a receptor or small ensemble.

**Evaluation:** Compare against predefined crystal structure, AlphaFold/static model where relevant, random structure choice, all-structure ensemble, and expert selection.

**Falsification:** The adaptive selector does not reproducibly outperform strong fixed/expert baselines or its decisions fail to transfer across held-out targets.

**Contribution:** A validated scientific decision policy for receptor-state selection.

**Agent necessity:** Potentially high if evidence and intermediate enrichment results can trigger different next actions.

### C2 — Adaptive computational-budget allocation

**Problem:** Expensive rescoring/MD is often applied using fixed cutoffs.

**Hypothesis:** Uncertainty-aware escalation can allocate expensive computation only to ambiguous compounds without sacrificing hit recovery.

**Central distinction from C1:** C1 studies receptor-state selection; C2 studies resource allocation under uncertainty.

### C3 — Autonomous screening-pipeline composition

**Problem:** Different targets may favor different docking/rescoring chains.

**Hypothesis:** A system that selects and revises the computational pipeline based on target/data characteristics and validation feedback can outperform a universal pipeline.

**Central distinction from C1/C2:** The research object is pipeline composition, not receptor state or budget allocation.

### C4 — Scientific discovery of target regimes

**Problem:** It is unclear which target properties predict when multi-conformation screening is actually necessary.

**Hypothesis:** Cross-target analysis can discover structural or pharmacological features that predict benefit from multi-conformation screening.

**Central distinction:** This is a discovery question, not primarily an automation-performance question.
