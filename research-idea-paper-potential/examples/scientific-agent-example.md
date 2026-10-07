# Example — Scientific Agent Idea

> **Note:** This is a synthetic calibration example, not a claim about any specific published system.

## Raw idea

Build an Agent that receives a disease and compound, searches literature, proposes candidate targets/mechanisms, chooses which computational analyses to run, updates hypotheses after contradictory evidence, and recommends the next validation experiment.

## Weak framing

> We built an Agent integrating literature search, docking, MD, and pathway analysis.

This mainly describes architecture.

## Stronger research framing

> We hypothesize that adaptive evidence acquisition and hypothesis revision enable more reliable mechanism identification than fixed target-to-validation workflows under heterogeneous and incomplete biomedical evidence.

This creates a falsifiable comparison:

`adaptive Agent vs fixed workflow under matched tools and budget`

## Agent-specific reasoning

### Agent necessity

Potentially high **only if** cases require different evidence paths and the Agent must decide what information to acquire next.

If every case always follows:

`search -> extract target -> dock -> MD -> report`

necessity is low.

### Scientific autonomy

High autonomy requires decisions such as:
- generate competing hypotheses;
- choose evidence sources based on uncertainty;
- decide whether structural modeling is relevant;
- design a discriminating next experiment;
- revise or abandon a hypothesis after contradictory evidence.

### Scientific discovery value

Retrieving known disease-target associations is not discovery.

Discovery value becomes stronger if the system:
1. prospectively proposes a non-obvious mechanism;
2. that mechanism is absent from the input knowledge path used to generate it;
3. an independent computational or wet-lab experiment validates it.

## Critical baselines

- same tools + fixed deterministic workflow;
- same tools + LLM but fixed plan;
- Agent with adaptation disabled;
- expert-designed evidence path;
- equal-compute/equal-query-budget comparison.

## Reviewer attack

The strongest attack is likely:

> The Agent appears better only because it uses more searches/tools/compute, not because adaptive scientific reasoning is useful.

The decisive response is a matched-budget study where only adaptive decision-making differs.
