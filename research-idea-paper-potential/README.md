# Research Idea Paper Potential Skill

A reusable Agent Skill for judging whether an idea has the potential to become:

1. a **defensible research paper**, and/or
2. a **high-quality research paper**.

It also contains a dedicated module for **Scientific Agent / AI-for-Science** ideas:

- `Agent necessity`
- `Scientific autonomy`
- `Scientific discovery value`

The skill is designed for early-stage research triage, proposal refinement, project Go/No-Go decisions, paper positioning, and reviewer-style stress testing.

## Why this skill exists

Research ideas are often overestimated because they are:

- new implementations rather than new knowledge;
- complex systems without a strong scientific claim;
- benchmark improvements with weak explanatory value;
- "first application" papers without a meaningful knowledge gap;
- Agent workflows whose decisions are actually predefined;
- ambitious projects whose decisive experiment is infeasible.

This skill forces the evaluator to separate **paperability** from **quality ceiling**, and to treat fatal flaws as gates rather than averaging them away.

## Repository structure

```text
research-idea-paper-potential/
├── SKILL.md
├── README.md
├── MANIFEST.md
├── references/
│   ├── core-rubric.md
│   ├── scoring-model.md
│   ├── fatal-flaws.md
│   ├── agent-specific-rubric.md
│   ├── reviewer-attack.md
│   └── evidence-levels.md
├── assets/
│   ├── report-template.md
│   ├── idea-intake-template.md
│   └── evaluation-schema.json
├── examples/
│   ├── scientific-agent-example.md
│   └── conventional-idea-example.md
├── evals/
│   ├── test-cases.md
│   └── expected-behaviors.md
└── scripts/
    └── score_idea.py
```

## Installation / use

This repository follows the Agent Skills pattern: a skill is a directory anchored by a `SKILL.md` manifest plus optional references, assets, and scripts.

Typical use:

```text
Use the research-idea-paper-potential skill to evaluate this idea:
<your idea>
```

You can also ask for a specific mode:

```text
Use the skill in strict reviewer mode. Verify novelty and related work before scoring.
```

```text
Use the skill to compare these three ideas and rank them for paper potential.
```

```text
Evaluate this Scientific Agent idea. Pay special attention to Agent necessity,
Scientific autonomy, and Scientific discovery value.
```

## Headline outputs

The skill reports two core scores rather than one:

- **Paperability Score /100** — can this idea realistically become a defensible research paper?
- **High-Quality Potential Score /100** — if executed well, how high is the scientific ceiling?

For Agent ideas, it additionally reports:

- **Agent necessity /8**
- **Scientific autonomy /10**
- **Scientific discovery value /12**

The Agent score is reported separately instead of being blindly added to the core score.

## Recommended evaluation philosophy

The central model is:

```text
important question
    -> authentic gap
    -> falsifiable claim
    -> discriminating evidence
    -> defensible conclusion
```

For high-quality work:

```text
paperability
    x significance
    x novelty
    x explanatory depth
    x evidence strength
    x reach/generalizability
```

For Scientific Agent work:

```text
Agent necessity
    -> Scientific autonomy
    -> Scientific discovery value
```

## Current-information requirement

Novelty and knowledge-gap claims should be externally verified whenever current literature/database access is available. If verification is unavailable, the skill must label those judgments as provisional rather than presenting them as facts.

## Design basis

The packaging follows the current Agent Skills structure documented by OpenAI: a directory containing `SKILL.md` with YAML front matter and optional supporting files such as references, scripts, and assets.

Useful official references:

- OpenAI Skills guide: https://developers.openai.com/api/docs/guides/tools-skills
- OpenAI plugin Skills concept: https://developers.openai.com/plugins/concepts/skills
- OpenAI guide to building skills: https://developers.openai.com/plugins/build/skills
- OpenAI Academy — Using skills: https://openai.com/academy/skills/

## Version

`1.0.2`

This version emphasizes scientific claim quality, claim-evidence alignment, reviewer resistance, and Agent-specific scientific contribution.
