# AIDD review domain guardrails: protect meaning before style

These are **questions to audit**, not assumptions that all included studies fail them. Adapt to the domain being reviewed; avoid bloating the manuscript with every pitfall.

## Endpoints and experimental meaning

- `DTI` binary interaction, `DTA` continuous affinity, efficacy/function (`EC50`, `Emax`, antagonism, inverse agonism, pathway bias), drug properties (`ADMET`, physicochemical), protein structure, binding pose, and molecular generation are distinct tasks. Do not transfer conclusions between them without a supported link.
- `Kd`, `Ki`, `IC50`, `EC50`, `pIC50/pKi`, inhibition %, docking scores, and simulated binding free energies are not interchangeable. EC50 depends on functional assay and context; IC50 is assay-dependent; numerical scales/units/directions matter. A lower IC50 and higher pIC50 mean different directions; confirm transform conventions.
- Positive-only/unknown interactions are not automatically verified negatives. Label threshold, censoring, assay, aggregation, stoichiometry and heterogeneous complexes matter. Multi-protein receptors and heteromers are not identical to a single concatenated sequence.
- For GPCRs, ligand binding vs agonism/antagonism, receptor active/inactive structure, biased signaling, G-protein family, and beta-arrestin responses are different claims. Antibody, peptide, mini-protein and small-molecule evidence may not be equivalent.
- For peptides and cyclic peptides, distinguish membrane permeability, oral exposure, protease stability, conformation, noncanonical residues, N-methylation, synthetic tractability and target potency.

## ML and benchmark comparisons

- Define prediction unit (`molecule`, `drug–protein pair`, `protein structure`, `generated candidate`, `assay`, `prospective selection`). Identify targets/families and applicability domain.
- `Random pair`, `scaffold`, `drug-cold`, `target-cold`, `both-cold`, `protein-family holdout` and `temporal` splits measure different extrapolation capabilities. Inspect overlap (duplicates, near-identical molecules, homologous proteins, source assays, pretraining datasets) before claiming generalized transfer.
- AUC-ROC, average precision/PR-AUC, enrichment factor, BEDROC, calibration, accuracy, RMSE, Pearson/Spearman, RMSD and generative validity/novelty each have different meanings; direction and base rate/threshold matter. `AUPRC` definitions may differ across software; nonmatching metrics should not be ranked on one axis.
- Data sources sharing names (e.g. “BindingDB subset,” “DrugBank,” “Davis,” “KIBA”) may have different versions, curation, labels, negatives and splits. Record versions and preprocessing before comparing table cells.
- Comparisons need baseline status (literature-reported vs faithfully reproduced), training labels, pretraining, additional modalities, selected hyperparameters, compute and uncertainty. A model-family comparison with multiple concurrent differences does not isolate the causal value of a particular attention layer or architecture.
- A mean without an uncertainty definition is not a confidence interval. Seed-to-seed SD, fold SD and bootstrap CI are not interchangeable. Report significance only from actual tests.

## Structures, interactions and molecular generation

- Protein–ligand docking, rescoring, MD stability, cofolding confidence, interface contacts, attention maps and experimental target engagement are different evidence types. Predicted pose/contacts alone do not validate binding affinity, functional response, mechanistic action, or efficacy.
- `Active/inactive` states are biological model states, not trivially labelled by docking. Receptor conformational ensembles, environment, membrane context and state-specific pocket changes may limit static-structure interpretations.
- In generative drug design, chemical validity, uniqueness, novelty, diversity, synthetic accessibility proxies, actual synthesizability, docking score and experimental potency are different. A model can maximize a proxy without improving experimental design outcomes.
- Retrospective benchmark gains do not constitute prospective synthesis or wet-lab hit confirmation. Active learning “simulations” from fixed pools are not prospective closed-loop experiments.
- AlphaFold/structure prediction confidence, protein–ligand complex prediction, molecular dynamics and thermodynamics support different scientific propositions.

## Chronology and software lineage

- Published year, online-first date, arXiv version, benchmark date, source-code checkpoint and model release can differ. Use source-documented chronology. Draw an inheritance arrow only if there is documented technical dependence, not just a shared name, similar model term, or publication order.
- Check version-sensitive statements for pretrained models and code, especially when method names are reused by independent groups.
- An author's displayed attention matrix, interaction attribution, or saliency visualization is not automatically a chemically faithful contact map. Verify values, operators, and physical interpretation separately.

## Claim calibration ladder

1. “The study *reported* ... under [conditions].”
2. “Across [matched evidence], a pattern is consistent with ...”
3. “A mechanism is suggested by ... but not directly established.”
4. “The proposed taxonomy/framework organizes ...; it has not been independently validated.”
5. “Evidence is insufficient to determine ...; a matched [evaluation] would test it.”

Use the level the *sources justify*. Avoid both hype and formulaic disclaimers that obscure real achievements.
