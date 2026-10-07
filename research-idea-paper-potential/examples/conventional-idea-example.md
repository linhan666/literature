# Example — Conventional Research Idea

> **Note:** This is a synthetic example used to calibrate the rubric.

## Raw idea

Use a Transformer to predict ligand activity for one GPCR target and compare it with random forest and XGBoost.

## Initial diagnosis

This is research-shaped only weakly. It contains a method and benchmark but no clear knowledge gap or strong claim.

## Possible weak claim

> A Transformer predicts activity better than classical machine-learning models on this dataset.

This may be publishable if rigorously tested, but its quality ceiling is limited because:
- the problem importance is not yet established;
- novelty may be low;
- one target gives limited generalizability;
- metric gain may be caused by split choice or tuning;
- there is little conceptual insight.

## Stronger reframing

Suppose prior work shows a reproducible failure under scaffold-disjoint, low-data settings. Then the research question could become:

> Can receptor-family priors improve ligand activity prediction under scaffold-disjoint low-data conditions for understudied GPCRs?

Possible central claim:

> Hierarchical receptor-family priors improve scaffold-disjoint generalization under low-data conditions relative to target-only and ligand-only baselines.

Now the paper has:
- a specific failure mode;
- a stronger gap;
- a falsifiable claim;
- a matched baseline strategy;
- potential generalization beyond one target.

## Decisive evidence

Must-have:
- scaffold-disjoint split;
- equal-tuning baselines;
- multiple targets/families or leave-target-out evaluation;
- ablation of family prior;
- uncertainty across seeds/splits.

High-value:
- prospective screening or external dataset;
- analysis showing when the prior helps and when it fails.
