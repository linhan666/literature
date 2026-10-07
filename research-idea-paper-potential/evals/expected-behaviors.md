# Expected Skill Behaviors

A high-quality implementation of this skill should satisfy these checks.

## Triggering / scope

- Uses the skill for idea triage, paper-potential judgment, proposal stress testing, and Scientific Agent evaluation.
- Does not require the idea to already be fully specified.

## Reasoning quality

- Separates scientific claim from system description.
- Separates paperability from high-quality-paper ceiling.
- Treats novelty and knowledge gap as evidence-dependent.
- Explicitly considers alternative explanations.
- Uses fatal flaws as gates instead of averaging them away.
- Distinguishes application novelty from conceptual/methodological/mechanistic novelty.
- Distinguishes automation from scientific autonomy.
- Distinguishes retrieval/synthesis from scientific discovery.

## Output quality

- Produces a normalized problem-gap-claim-evidence-payoff chain.
- Gives dimension scores with rationales and confidence.
- Includes at least three reviewer attacks.
- Specifies a minimum decisive evidence package.
- Ends with Go / Conditional Go / Reframe / No-Go.
- States what the project can and cannot claim at its current evidence level.

## Anti-patterns

The skill should not:
- call every new application novel;
- infer novelty from memory when current search is available;
- call a fixed tool chain an autonomous Agent;
- infer mechanism from correlation alone;
- infer binding from docking score alone;
- infer generality from one case;
- recommend indiscriminate extra experiments;
- hide missing evidence behind a precise numeric score.
