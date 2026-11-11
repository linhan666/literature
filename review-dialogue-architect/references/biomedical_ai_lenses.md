# Domain lenses for biomedical AI and drug discovery

Use only when topic relates to drug discovery, GPCRs, DTI/DTA, structure prediction, virtual screening, or molecular generation. These are **analysis prompts**, not an obligatory taxonomy nor verified research findings.

## A. Task ontology and target-definition questions

- DTI: active/inactive or binding yes/no? Are labels continuous affinities thresholded, or assays with different biology?
- DTA: Ki/Kd/IC50/EC50/pIC50 are distinct measurements with assay context; do not conflate affinity and functional potency.
- GPCR pharmacology: binding, agonism/antagonism, inverse agonism, partial agonism, biased signaling, coupling preference are not interchangeable.
- Ion channels and heteromeric targets: distinguish a single UniProt chain from subunit composition, stoichiometry, complex identity, and assay context.
- Virtual screening: hit identification and early enrichment differ from direct affinity regression, kinetic prediction, efficacy or synthesizability.

## B. Model architecture and epistemology

Categorize across orthogonal axes:

1. Inputs: SMILES, molecular graph, 3D conformer, protein sequence, pocket graph, ensemble, receptor active/inactive state.
2. Encoders: PLM, GNN, CNN, transformer, equivariant geometric model, tabular descriptors, pretrained frozen weights.
3. Intermolecular interaction: none / late fusion / explicit pairwise maps / co-attention / geometry-aware messages / joint structure inference.
4. Learning and supervision: assay, structure/contact, distillation, weak labels, ranking, multitask, pretraining, causal/perturbation-oriented.
5. Prediction: binding classification, affinity regression, pose prediction, functional efficacy, selectivity, molecule/route generation.
6. Evaluation: random/scaffold/drug/target/pair cold splits, external assay, prospective VS, pose/contact checks, uncertainty/calibration, throughput.

If two named “attention mechanisms” operate at different granularity or are an architectural operator versus a training objective, they may not be sibling categories.

## C. Benchmark validity and interpretations

- State train/validation/test separation and possibility of near-duplicates, target leakage, scaffold bias, kinase-family bias, dataset memorization or pretrained teacher overlap.
- Distinguish AUROC/AUPRC from early enrichment (EF@k%, BEDROC) and regression CI/RMSE/R2; all are task-dependent.
- Confidence scores, attention heatmaps, contact probabilities, structural poses and functional effects answer different questions.
- If a model is described as SOTA, request comparability constraints and external/prospective corroboration.
- Large virtual screening libraries require throughput / compute / docking feasibility; not only predictive metrics.
- Distinguish empirical observations of receptor states from causal pharmacological attribution.

## D. Molecular generation and synthesis

Distinguish 2D chemical validity and heuristic synthetic-accessibility proxies from reaction-valid, building-block-native, route-conditioned generation. Also distinguish local ligand placement, global de novo 3D generation, fragment growing, scaffolding, policy search, Pareto/multiobjective post-training, and constraints evaluated after generation versus enforced during generation.

Ask which component is truly original: generative backbone, conditional controls, physical feedback, route representation, reward optimization, or evaluation design.

## E. How to use these lenses

Choose 3–6 dimensions with direct bearing on the user's aims; don't turn them all into mandatory chapters. Document excluded axes and why. Produce a candidate comparison matrix with *fields* but **no fabricated model scores or study evidence**. Assign verification priorities for the eventual evidence-first-review-writer.

## Recommended comparative matrix (schema only)

| Family/model | Scientific task and labels | Drug/protein input | Explicit interaction mechanism | Physical supervision | Output and uncertainty | Benchmark/split | Claimed advantage (unverified) | Required source/experiment |
|---|---|---|---|---|---|---|---|---|
| [CANDIDATE] | [TO VERIFY] | [TO VERIFY] | [TO VERIFY] | [TO VERIFY] | [TO VERIFY] | [TO VERIFY] | [NOT YET ESTABLISHED] | [METHOD/RESULT] |

Avoid populating row-specific scientific details from memory as if sourced.
