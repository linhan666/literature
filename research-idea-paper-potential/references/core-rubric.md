# Core Research-Idea Rubric

Score each dimension from **0 to 5**. Use `U` internally when evidence is insufficient; for computation, a provisional numeric score may be assigned only if clearly marked low-confidence.

## 1. Problem importance

**Question:** If this problem were solved, would the field, scientific understanding, or a meaningful real-world decision change?

- **0** — no identifiable scientific problem.
- **1** — minor convenience or narrow implementation issue.
- **2** — legitimate but low-impact problem.
- **3** — meaningful problem for a subfield or application.
- **4** — major bottleneck, unresolved challenge, or important scientific question.
- **5** — central problem with broad scientific or translational consequences.

High scores require more than "nobody has done this exact thing before."

## 2. Knowledge gap authenticity and clarity

**Question:** What exactly is unknown, inadequate, contradictory, or unvalidated?

Typical gap types:
- knowledge gap;
- performance gap;
- mechanism gap;
- methodological gap;
- evidence gap.

- **0** — no gap; the idea is mainly a topic or implementation.
- **1** — vague claim that prior work is insufficient.
- **2** — plausible gap but weakly documented or already partly solved.
- **3** — specific and supported gap.
- **4** — well-verified important gap with clear boundaries.
- **5** — decisive unresolved gap whose resolution would materially advance the field.

## 3. Novelty

Evaluate the strongest novelty type actually supported:

`application < engineering < methodological < empirical < mechanistic < conceptual`

- **0** — essentially duplicated prior work.
- **1** — cosmetic or parameter-level variation.
- **2** — new application or integration with limited conceptual novelty.
- **3** — meaningful methodological, empirical, or system-level novelty.
- **4** — strong mechanism, method, or problem-formulation novelty.
- **5** — conceptual advance or genuinely field-shifting new capability/principle.

Do not award a high score merely because modules have not previously been combined.

## 4. Scientific claim strength and falsifiability

**Question:** Can the idea be expressed as `We demonstrate that ______`, and can evidence prove it wrong?

- **0** — no scientific claim.
- **1** — descriptive feature list or unfalsifiable aspiration.
- **2** — vague or weakly testable claim.
- **3** — explicit, testable claim with reasonable scope.
- **4** — precise claim tied to decisive tests.
- **5** — strong, discriminating claim with high explanatory or practical consequence.

A claim should describe what is learned, not merely what is built.

## 5. Mechanistic or conceptual insight

**Question:** Does the work explain **why**, **when**, or **under what principle** the result occurs?

- **0** — no insight beyond implementation/output.
- **1** — post-hoc narrative only.
- **2** — limited explanatory analysis.
- **3** — meaningful mechanism, causal evidence, or interpretable principle.
- **4** — strong explanation that connects observations to a generalizable mechanism/concept.
- **5** — new mechanism, theory, or conceptual framework likely to alter how the problem is understood.

For benchmarking papers, this dimension can be satisfied by discovering a robust failure mode or evaluation principle rather than a biological mechanism.

## 6. Evidence strength and claim-evidence alignment

**Question:** Are the proposed observations sufficient for the exact scope of the claim?

- **0** — evidence absent or unrelated.
- **1** — anecdotal demonstration.
- **2** — partial validation with major gaps.
- **3** — adequate evidence for a bounded claim.
- **4** — multiple independent evidence layers with strong alignment.
- **5** — decisive convergent evidence, ideally including prospective or external validation where relevant.

More experiments are not automatically stronger evidence. Each experiment should have an epistemic role.

## 7. Alternative-explanation discrimination and controls

**Question:** Can the design distinguish the proposed explanation from the strongest competing explanation?

- **0** — no controls or alternative hypotheses considered.
- **1** — obvious confounders remain.
- **2** — basic controls but major alternatives unresolved.
- **3** — main confounders addressed.
- **4** — matched baselines/controls/ablations/perturbations discriminate leading alternatives.
- **5** — decisive experiments directly challenge the strongest plausible alternative hypotheses.

Examples include negative/positive controls, ablations, matched compute/data, perturbation, rescue, mutation, blinded validation, or leakage checks.

## 8. Generalizability / external validity

**Question:** How far can the conclusion travel beyond the exact training set, target, cohort, system, or case study?

- **0** — conclusion is not even supported in the studied setting.
- **1** — one narrow demonstration.
- **2** — limited replication within closely related settings.
- **3** — multiple datasets/targets/settings or a deliberately bounded conclusion.
- **4** — strong external validation across meaningful shifts.
- **5** — supports a broader principle across domains/conditions with appropriate boundaries.

Do not infer a general principle from a single case.

## 9. Feasibility

**Question:** Can the decisive study actually be completed with accessible data, tools, expertise, time, and budget?

- **0** — core study is impossible under realistic constraints.
- **1** — major inaccessible dependency.
- **2** — high risk with no credible fallback.
- **3** — feasible with manageable risks.
- **4** — clear execution path with pilot evidence or robust fallbacks.
- **5** — highly executable and well de-risked without trivializing the scientific question.

## 10. Reproducibility / robustness

**Question:** Can the result survive reasonable implementation, sampling, and analysis variation?

- **0** — opaque or irreproducible.
- **1** — major undocumented dependencies.
- **2** — reproducibility plan incomplete.
- **3** — methods, seeds, splits, code/protocols, and statistics are adequately specified.
- **4** — strong robustness analyses and transparent artifacts.
- **5** — independent reproduction, preregistration, multi-site/multi-seed confirmation, or equivalent high-confidence reproducibility.

## 11. Narrative coherence / contribution clarity

**Question:** Do the problem, gap, claim, method, evidence, and conclusion form one coherent paper rather than several disconnected mini-projects?

- **0** — no coherent story.
- **1** — highly fragmented.
- **2** — central story exists but contribution is diffuse.
- **3** — clear central narrative.
- **4** — strong claim-centered structure.
- **5** — exceptionally clean contribution where every major experiment advances the same argument.
