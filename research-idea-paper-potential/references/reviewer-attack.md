# Reviewer Attack Protocol

The evaluator should act as a skeptical but fair reviewer after the initial scoring.

## Seven mandatory attack questions

1. **Why does this problem matter?**
   - If solved, who changes what decision or belief?

2. **What exactly is unknown?**
   - Is the gap specific, verified, and not already solved under another name?

3. **What is genuinely new?**
   - Is novelty only "A + B + C" or first application?

4. **What is the central claim?**
   - Can it be written as `We demonstrate that ______`?

5. **What observation would prove the claim wrong?**
   - If none exists, the claim is not sufficiently scientific.

6. **What is the strongest alternative explanation?**
   - Identify the explanation most likely to survive current controls.

7. **If everything works, what changes?**
   - Another implementation, or a new mechanism/method/capability/principle?

## Reviewer-attack table

For at least three attacks, output:

| Attack | Why it matters | Decisive response | Residual risk |
|---|---|---|---|
| ... | ... | ... | Low/Medium/High |

## Common attacks by paper type

### AI / ML
- unfair baseline tuning;
- more compute/data/parameters rather than method effect;
- leakage or invalid split;
- metric improvement too small or unstable;
- no out-of-distribution/generalization evidence;
- ablation does not isolate the claimed mechanism;
- benchmark saturation or cherry-picking.

### Computational drug discovery
- docking score treated as binding evidence;
- insufficient receptor/ligand state coverage;
- rescoring methods are correlated rather than independent evidence;
- no prospective or experimental validation;
- target relevance is associative rather than causal;
- off-target explanation not addressed;
- MD stability is overinterpreted as affinity or mechanism.

### Wet-lab / mechanistic biology
- phenotype is not target-dependent;
- missing rescue or perturbation evidence;
- concentration/exposure not physiologically relevant;
- cell-line result does not generalize;
- pathway readout is downstream correlation rather than mechanism;
- effect could be toxicity or nonspecific stress.

### Scientific Agent
- fixed workflow could do the same thing;
- Agent success is due to tool access or token/compute budget;
- autonomy is claimed but decisions are researcher-authored;
- retrieved knowledge is mislabeled as discovery;
- no counterfactual showing Agent decisions improve scientific outcome;
- no prospective task where the plan cannot be known in advance.
