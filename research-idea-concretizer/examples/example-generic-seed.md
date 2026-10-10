# Example — Generic Vague Seed

## Seed

“Use a new model X in domain Y.”

## Bad concretization

“Fine-tune model X on dataset Y1 and compare accuracy.”

Why insufficient:

- starts from the solution;
- does not identify a meaningful gap;
- may only be a model/dataset swap;
- scientific contribution is unclear.

## Better expansion

1. Identify the dominant bottlenecks in domain Y.
2. Map which capabilities of model X are actually relevant.
3. Generate candidate pairings between bottlenecks and capabilities.
4. Construct distinct hypotheses.
5. Define evaluations that could falsify those hypotheses.
6. Preserve candidates that differ in scientific question, not only implementation.

## Example MRI skeleton

**Problem:** A specific decision in Y fails under condition Z.

**Gap:** Existing methods lack capability Q under Z.

**Hypothesis:** Capability Q from model X will improve/reveal outcome R under Z.

**Method:** Apply or adapt X so that Q directly acts on the bottleneck.

**Evaluation:** Compare against current standard, simpler alternative, and relevant ablation.

**Falsification:** No consistent gain or the gain disappears when Q is ablated.

**Contribution:** Evidence that Q is or is not necessary for the target problem.
