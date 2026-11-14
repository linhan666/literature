# Taxonomy, comparability and critical synthesis

## Rebuild the intellectual architecture, not just the headings

For the review's actual central question, identify:

- **Unit of analysis:** full published model; particular interaction module; specific assay/result; trained checkpoint; application workflow; intervention; paper (these must not be conflated).
- **Classification dimensions:** functional role, mechanistic operation, input representation, granularity/resolution, supervision, training regime, task, evaluation, evidence level, system integration, chronology, where relevant.
- **Operational rules:** positive criteria, explicit negative criteria, hybrid/ambiguous states, supporting source locator, and counterexamples.
- **Relationship of dimensions:** mutually exclusive **within** one axis if justified, nested parent–child, or orthogonal and overlapping across axes. Do not impose disjoint classes on mixed methods by default.
- **Coverage audit:** apply the rules to a handful of representative, boundary and negative cases from the actual cited corpus; revise the rule if the evidence contradicts its definition.

Suggested coding statuses: `PRIMARY`, `SECONDARY`, `CO_PRIMARY`, `HYBRID`, `INAPPLICABLE`, `UNDETERMINED`, as appropriate. These are **author conventions**, not validated truths. Keep the status visible when decisions are ambiguous. Provide a published-paper-to-taxonomy map only when the corresponding mechanisms have been read/verified sufficiently.

### Three common classification mistakes

1. **Input vs function:** “3D GNN” specifies representation/architecture, not necessarily the functional role of cross-modal attention.
2. **Architecture vs evidence:** a model can use residue–atom attention while having no evidence that the weights correspond to experimental residue contacts.
3. **Time vs lineage:** chronological proximity and name similarity are not sufficient to establish a technical dependence edge.

For overlapping categories, show an incidence matrix or multi-tag table instead of forcing a false partition. An incidence count is not a corpus-prevalence estimate unless the corpus and coding process are defensible.

## The comparison contract

Each comparison must say what is being compared *for which claim*. A practical matrix:

| Dimension | Question to record | If unmatched |
|---|---|---|
| Task/endpoint | Binary DTI, DTA regression, functional response, pose, generative decision? | No simple metric-to-metric ranking |
| Data/split | Dataset version, assay labels, negatives, duplicates, target/scaffold/temporal holdouts? | Generalization claims become conditional |
| Inputs | SMILES, sequence, graph, structure, pocket, external labels, pretrained model? | “Architecture gain” not isolated |
| Intervention | Full pipeline, single swapped operator, retrained baseline, ablation? | Attribution to one module unsupported |
| Evaluation object | Drug–target pair vs atom–residue contact vs scaffold/target or experiment? | Outcome means differ |
| Measurement | Metric, threshold, unit, uncertainty, sample selection? | Magnitudes may not be comparable |
| Validation | Internal benchmark, external set, independent rerun, experiment? | Do not collapse evidence levels |

Decision states, always accompanied by a reason:
- `COMPARABLE_FOR_CLAIM` — sufficiently matched **for the stated narrow claim**.
- `CONDITIONAL` — useful qualitative comparison, confounders disclosed.
- `NOT_COMPARABLE` — incompatible task/protocol or evidence object.
- `NOT_VERIFIED` — critical protocol facts unavailable.

Do not silently transform `CONDITIONAL` into a general ranking. It is often reasonable to compare *architectural distinctions* even when reported AUROCs cannot be compared. Explicitly name the comparison type.

## From list of papers to argument

A literature catalog describes: “A used X; B used Y; C used Z.”

A critical synthesis asks:
1. **What common design pressure/problem connects A, B and C?**
2. **Which mechanism differs in operation, not just name?**
3. **Which comparisons are supported by matched evidence?**
4. **What contradictory results, alternative explanations, or blind spots persist?**
5. **What experiment, data curation or reporting standard would discriminate explanations?**

Use a section-function progression that can vary by topic:

`Problem and selection boundary → operational dimensions → families/contrasts → what evidence actually establishes → incompatible findings → threats to comparison → actionable research questions.`

This is a compositional aid, not a fixed table of contents. Avoid filling identical subsections for every architecture at the cost of analysis.

## Claims and negative evidence

- “Paper A reports improvement over its own baseline” ≠ “A outperforms paper B.”
- “Contact-focused attention visualization is available” ≠ “Attention identifies true protein–ligand contacts.”
- “Multiple results are consistent” ≠ independent replication if data, checkpoints or evaluation protocols overlap.
- A proposed framework may clarify intellectual structure without having predictive/diagnostic validation.
- The absence of matching benchmark evidence is an **evidence gap**, not a finding that a method fails.

When tests could in principle settle a dispute, specify: the hypothesis, controlled variable(s), held-constant factors, predicted distinguishing observations, and feasibility limits. Do not report the proposed test as completed.

## Deliverable mapping example (schema, not a real study)

`Section claim → coded source rows → conflicts/negative evidence → selected figure/table → bounded conclusion → unresolved tests`

An author-proposed taxonomy belongs in a conceptual diagram/table with explicit author-proposal status. Empirical comparisons belong in fact-sourced tables with columns for conditions and validation. If one display mixes the two, distinguish them visually and in captions.
