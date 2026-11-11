# Biomedical / AI drug discovery review extension

This reference is a **proposed comparative framework**, not a claim that the literature itself uses this exact taxonomy. Introduce it as the review authors' analytical framework; cite primary sources for attribution and findings.

## Recommended orthogonal axes

| Axis | Categories or questions | Why it matters |
| --- | --- | --- |
| Downstream goal | DTI binary/multilabel; DTA regression; binding pose; efficacy/functional bias; VS enrichment; de novo molecule generation | Binding, affinity and efficacy are distinct labels |
| Molecular inputs | SMILES; 2D graph; fingerprint; ligand 3D conformer; protein sequence/PLM; sequence-derived contacts; apo/holo structures; receptor state | Defines inference availability and information budget |
| Cross-modal interaction | No explicit pair interaction; late fusion; bilinear/multiplicative; drug-to-protein and protein-to-drug cross-attention; pairwise atom-residue map; graph-based interface; geometric equivariant interactions | Attention weights alone do **not** prove physical contacts or causal interpretability |
| Supervision | Binding assay; affinity endpoint (Kd/Ki/IC50/EC50, with differences); activity class; pose/contact; functional signaling | Assay endpoints are not interchangeable |
| Split / generalization | Random pair; scaffold/cold-drug; cold-target; cold-both; temporal; family/species transfer; external lab validation | Quantifies distribution shift and leakage risk |
| Data reliability | Source database, duplicate assays, label thresholds, negative generation, assay uncertainty, target identity, oligomer/complex representation | Nominal benchmark size is not equivalent to effective independence |
| Scientific trust | Calibration/uncertainty; negative controls; ablation; prospective test; structural validation; independent experimental evidence | Prevents interpretation from resting on attractive visualizations |
| Resource efficiency | Parameters, frozen vs fine-tuned encoders, VRAM, wall time, docking cost per compound, scaling to 10^5–10^7 ligands | Differentiates deployable VS from per-complex structural inference |

## Focus modules

### Explicit drug–protein interaction learning

Separate **attention distribution** from **physical contact prediction** and **mechanistic attribution**:

1. A cross-attention matrix says where information is weighted, not automatically where atoms contact residues.
2. A contact-map head produces a supervised or inferred pairwise contact prediction; evaluate precision/recall at a physical distance definition with ligand pose quality and ground-truth origin documented.
3. Counterfactual perturbations, residue mutagenesis, ligand modifications, and benchmark interventions may offer stronger causal evidence but require careful confounder controls.
4. Report mapping conventions (atom vs token, residue numbering, pocket definition), reference structure, protonation, hydrogen bonding constraints, and whether contacts are unique to agonist or antagonist states.

### GPCR pharmacology and state awareness

Separate binding vs efficacy (agonism/antagonism/inverse agonism) vs pathway bias (G protein, beta-arrestin, Gs/Gi/o/Gq/11) and assay-specific signaling. Distinguish inactive vs active receptor conformations, orthosteric vs allosteric pockets, sequence identity and GPCR family split, and efficacy labels across experimental systems. Do not assume structural class implies signaling outcome.

### DTI/DTA benchmarking

For any headline score record: dataset version; endpoint; unit/log transform; metric; split; random seed/CI; cutoff; model inputs; pretrained encoder overlap; train/test leakage; target overlap; external holdout; full baseline list; compute. Do not compare AUROC/AUPRC (classification) with RMSE/Pearson/C-index (regression) as if one task. AUPRC depends on active prevalence; docking ranking metrics such as EF@1% depend on pool construction.

### Structure-based virtual screening

Separate docking pose generation, rescoring, structure cofolding, affinity estimation, pose ranking, and enrichment. Ask whether a method requires ligand-specific receptor relaxation, a fixed protein template, training on analogous targets, re-docking, or an apo/holo template. Compare throughput and false-positive budgets before claiming screening practicality.

### 3D generative chemistry with synthesizability

Classify how synthesis enters: post-hoc SA/QED proxy, retrosynthetic feasibility check, reaction-template conditioning, building-block composition, direct synthetic-route generation, or constrained RL/search. Explicit BB/reaction routes are substantively different from heuristic SA scores. Distinguish pharmacophore point constraints from specified residue×interaction-type constraints, and evaluate generated pose validity, chemical validity, diversity, activity prediction leakage, route feasibility, and actual synthesis.

## Recommended review exhibits

- **Figure 1**: task and information-flow taxonomy (sequence/SMILES → representations → cross-modal interaction → task → validation).
- **Figure 2**: a matrix mapping interaction operators to hypotheses and available physical supervision.
- **Table 1**: representative methods × inputs × interaction operator × label × dataset × split × metric × limitations.
- **Table 2**: evidence-of-interpretability ladder: visual attention, correlation, physical contact agreement, perturbation sensitivity, prospective mechanistic validation.
- **Table 3**: reproducibility and deployment checklist (licenses, source code, splits, pretraining leakage, runtime, external data).
- **Figure 3**: forward-looking design hypotheses, explicitly separated from observed facts.

When actual benchmark numbers cannot be verified, use `Not reported`, `Not comparable`, or `Verification pending` rather than fabricated rankings.
