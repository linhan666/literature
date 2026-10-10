# research-idea-concretizer

A repository-ready Skill for turning a vague scientific seed into multiple distinct, mature, falsifiable research ideas.

## What it does

The Skill implements a two-phase process:

1. **Space Expansion** — expands the seed across problem, object, intervention, autonomy, evidence, and evaluation axes.
2. **Idea Specification** — clusters and orthogonalizes candidates, then converts the retained ideas into **Minimum Researchable Ideas (MRIs)**.

Each MRI explicitly contains:

`Problem + Gap + Hypothesis + Method + Evaluation + Contribution`

and additionally records baselines, falsification conditions, assumptions, risks, evidence needs, and novelty-verification status.

## Repository structure

```text
research-idea-concretizer/
├── SKILL.md
├── README.md
├── VERSION
├── CHANGELOG.md
├── schemas/
│   └── idea_candidate.schema.json
├── templates/
│   ├── full-output-template.md
│   └── compact-output-template.md
├── rubrics/
│   ├── maturity-gate.md
│   └── orthogonality-check.md
├── references/
│   └── methodology-notes.md
├── examples/
│   ├── example-agent-virtual-screening.md
│   └── example-generic-seed.md
├── tests/
│   └── test-cases.md
└── scripts/
    └── validate_candidate.py
```

## Recommended use

Use this Skill **before** a formal research-idea evaluation/ranking Skill.

Recommended pipeline:

```text
Vague Seed
   ↓
research-idea-concretizer
   ↓
3–8 mature or near-mature candidate ideas
   ↓
idea-evaluation skill
   ↓
prioritized research program
```

## Design goals

- prevent premature convergence on the first interpretation;
- distinguish a topic from a researchable idea;
- force falsifiability and credible evaluation;
- preserve multiple levels of ambition;
- avoid superficial “model/dataset swap” novelty;
- rigorously detect when an “Agent” is only a static workflow with an LLM wrapper;
- support both evidence-backed and offline use.

## Version

See `VERSION` and `CHANGELOG.md`.
