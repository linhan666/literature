---
name: research-paper-interpreter
description: Deeply interpret research papers across machine learning, deep learning, AI agents, structural biology, AIDD, CADD, molecular generation, protein structure prediction, virtual screening, molecular dynamics, and related computational research. Use when the user asks to explain, analyze, review, reproduce, compare, critique, or derive research ideas from a paper. Focus on research question, technical mechanism, evidence, experiments, innovation, limitations, reproducibility, code, latest related work, and actionable extensions rather than section-by-section translation.
---

# Research Paper Interpreter

Interpret research papers as **technical research objects**, not as text to be translated or mechanically summarized.

The goal is to answer:

> **What exactly did this work do, why was it designed this way, what evidence supports it, what is genuinely new, what remains weak or unresolved, how reproducible is it, and how can it become the starting point for a better study?**

## Core principles

1. **Do not perform paragraph-by-paragraph translation.** Reconstruct the scientific logic of the work.
2. Separate all substantive statements into three evidence classes when relevant:
   - **【Paper】** directly stated, implemented, or demonstrated in the target paper.
   - **【External evidence】** supported by independently retrieved literature, code, benchmarks, databases, or documentation.
   - **【Analysis】** synthesis, critique, inference, or proposed extension.
3. Never present an inference as a claim made by the paper. If information is absent, explicitly state **“not specified in the paper”**.
4. For innovation claims, current-state judgments, method comparisons, research recommendations, or statements extending beyond the paper, **independently check the latest literature when web/retrieval tools are available**. Do not rely only on the paper's reference list or model memory.
5. If official code is available and the task concerns implementation, architecture, reproducibility, or modification, analyze **both paper and code**. Note discrepancies explicitly.
6. Prefer a small number of major sections. Use cohesive technical narrative, compact tables, and lower-level subsections rather than excessive top-level headings.
7. Explain **why** each design exists, not only **what** it does.
8. Distinguish benchmark improvement from actual scientific or practical value.

---

# Execution workflow

## Step 1 — Establish the paper's research contract

Before diving into details, identify:

- scientific problem;
- research object and application scenario;
- input and output;
- claimed bottleneck in prior work;
- main hypothesis or design thesis;
- headline contribution.

Summarize this in 1–3 sentences, then state the paper as an explicit mapping:

**Input → Core transformation/model → Output → Intended use**

If the paper contains multiple tasks, separate them.

## Step 2 — Reconstruct the complete method before discussing details

Explain the end-to-end data flow first.

For a model-centric paper, default to:

**Input → Representation/Encoder → Core module → Interaction/Fusion → Prediction/Generation head → Output**

For an agent paper, default to:

**User/Task input → Planning/Decomposition → Tool or model selection → Execution → Memory/State → Verification/Reflection → Final output**

For structural biology / AIDD / CADD, default to:

**Target/structure/data → preprocessing or conformational treatment → modeling/sampling/generation/docking → scoring/filtering → computational or experimental validation**

State which components are inherited from prior work, modified, newly introduced, or merely configured.

## Step 3 — Decompose only the technically important modules

For each key module, answer:

- **Input**
- **Output**
- **Algorithm/model**
- **Actual computation**
- **Why this module is needed**
- **Why this design was chosen**
- **Difference from conventional alternatives**
- **Whether it is trained or frozen**
- **Loss/objective**
- **How it is used during inference**

For equations, explain in this order:

**variables → computation → design purpose → behavioral consequence**

Do not merely restate mathematical notation.

## Step 4 — Audit the data and supervision

Determine:

- source and version of datasets;
- sample counts and data modalities;
- labels and how they were obtained;
- inclusion/exclusion and cleaning rules;
- train/validation/test split strategy;
- scaffold, sequence, structure, cluster, temporal, target, or random split;
- data leakage risks;
- positive/negative definitions and class imbalance;
- augmentation, pretraining, fine-tuning, curriculum, distillation, or self-supervision;
- which data affect training versus validation versus final external testing;
- training hyperparameters and compute resources when available.

Do not treat an evaluation set as independent if its construction leaks information from training.

## Step 5 — Interpret experiments as hypothesis tests

For every important experiment, use the logic:

**Hypothesis → Experimental design → Comparator/baseline → Metric → Result → What the result actually supports → What it does not prove**

Inspect especially:

- main benchmark;
- baseline fairness;
- ablations;
- robustness and sensitivity analyses;
- generalization / OOD tests;
- external validation;
- case studies;
- wet-lab or structural validation;
- multi-seed/statistical significance;
- calibration and uncertainty when relevant.

Explicitly judge whether the experiments genuinely support each core claim.

## Step 6 — Extract the real results

Separate:

### Directly demonstrated
Results numerically or experimentally supported by the paper.

### Author interpretation
Mechanistic explanations or broader claims proposed by the authors.

### Remaining uncertainty
Claims for which the presented evidence is incomplete, indirect, or confounded.

Prioritize the 3–5 findings that matter most scientifically. Mention when improvements are numerically small, depend on a narrow benchmark, or disappear under certain settings.

## Step 7 — Assess innovation without copying the contribution list

For each substantive innovation, describe:

- **Previous practice** — what prior work normally did;
- **This paper** — what changed concretely;
- **Innovation locus** — new task definition, data, representation, architecture, module, objective, training strategy, inference strategy, evaluation framework, or engineering integration;
- **Innovation level** — choose one of:
  - new paradigm;
  - core algorithmic innovation;
  - important module-level innovation;
  - engineering/system integration;
  - application/domain transfer.

The label must be justified by evidence, not by the authors' wording.

## Step 8 — Identify limitations and failure modes

Separate:

### Author-acknowledged limitations
Only what the paper itself acknowledges.

### Additional technical limitations
Analyze, as applicable:

- dataset bias and coverage;
- data leakage;
- weak or circular labels;
- inappropriate negative samples;
- benchmark overfitting;
- unfair baselines or tuning budgets;
- distribution shift;
- limited target/scaffold/species/structure coverage;
- compute cost and scaling;
- uncertainty/calibration;
- interpretability;
- biological or physical plausibility;
- insufficient structural or experimental validation;
- reproducibility gaps;
- cherry-picking or favorable-case selection;
- mismatch between training objective and real deployment objective.

Do not manufacture weaknesses without evidence; explain the mechanism by which each limitation could matter.

## Step 9 — Audit code and reproducibility when code exists

Identify:

- official repository and release status;
- license if relevant;
- repository structure;
- model-definition files;
- data preprocessing pipeline;
- training entry point;
- inference/evaluation entry point;
- configs;
- checkpoints;
- environment/dependencies;
- external databases/services;
- missing scripts/data/weights;
- approximate hardware requirements;
- whether headline results appear reproducible from the released materials.

Compare paper description with implementation. Call out mismatches in architecture, default parameters, preprocessing, evaluation, or hidden dependencies.

## Step 10 — Place the paper in the current research landscape

When external search is available, independently retrieve relevant work rather than relying on the target paper's bibliography alone.

Cover only the most relevant chain:

**direct predecessors → contemporary competitors → subsequent improvements → current leading methodological directions**

For each externally sourced claim, provide a citation/link when the environment supports it.

Particularly verify:

- whether the claimed novelty already appeared elsewhere;
- whether newer work has replaced or extended the approach;
- whether later studies reproduced or contradicted the result;
- whether code or benchmarks changed after publication.

## Step 11 — Convert understanding into research directions

Do not end with generic statements such as “this can be applied to other tasks.”

Organize extensions into four classes when useful:

- **Directly reusable modules** — components that can be transferred with little modification;
- **Modules worth modifying** — current weakness + proposed architectural/algorithmic change;
- **Modules worth replacing** — newer or more suitable alternatives;
- **New modules worth adding** — missing capability and why it matters.

For 2–5 serious follow-up project ideas, specify:

- scientific question;
- limitation of the original method;
- exact component to change;
- proposed new model/module/algorithm;
- required data;
- training strategy;
- critical experiments;
- baselines;
- success criteria;
- what result would falsify the proposed idea.

Prefer **model/module modification or new module design** over merely concatenating existing tools into a workflow when the research objective is methodological innovation.

---

# Domain adapters

Use only the adapter(s) relevant to the paper.

## Machine learning / deep learning

Focus on:

- representation learning;
- architecture and tensor/data flow;
- supervision and objective functions;
- inductive bias;
- split strategy and leakage;
- baseline parity;
- ablation validity;
- scaling and compute;
- calibration, uncertainty, and OOD generalization;
- reproducibility from code.

## Agent / LLM systems

Focus on:

- harness vs agent logic;
- planner/controller design;
- tool interfaces and permissions;
- state/memory representation;
- reflection, verifier, critic, or judge loops;
- orchestration and failure recovery;
- benchmark task construction;
- execution success vs answer quality;
- cost, latency, tool calls, token usage;
- reproducibility and nondeterminism;
- whether evaluation measures the **agent** rather than only downstream model quality.

Distinguish improvements caused by a stronger base model from improvements caused by the agent architecture.

## Structural biology

Focus on:

- experimental system and construct design;
- structure determination method and resolution/quality metrics;
- conformational state assignment;
- ligand/protein/cofactor context;
- residue-level interactions;
- structural comparison and mechanistic interpretation;
- mutagenesis, functional assay, cryo-EM/X-ray/NMR evidence;
- whether claimed mechanism is directly observed or inferred;
- numbering schemes and mapping when relevant.

## AIDD / CADD / molecular modeling

Focus on:

- molecular and target representation;
- bioactivity labels and assay heterogeneity;
- ligand/scaffold/target splits;
- docking pose generation vs rescoring;
- receptor flexibility;
- protein-ligand interaction modeling;
- 2D vs 3D inductive bias;
- molecular generation constraints;
- affinity/activity/function distinction;
- virtual screening enrichment and early-recognition metrics;
- prospective vs retrospective validation;
- MD/free-energy/physics-based validation;
- experimental confirmation.

Never equate predicted binding affinity with functional agonism/antagonism unless the study provides evidence linking them.

---

# Default output structure

Use this structure unless the user requests another format. Keep the number of major headings small.

## 1. Core question and one-sentence positioning
Explain problem, input/output, bottleneck, and headline solution.

## 2. Method and mechanism
First give the end-to-end workflow, then deeply explain only the key modules, equations, and design choices.

## 3. Data, training, and experimental evidence
Combine dataset audit, split strategy, training setup, baselines, metrics, main experiments, ablations, and what each experiment proves.

## 4. Innovation, limitations, reproducibility, and current landscape
Separate paper claims, external evidence, and analysis. Include code-level findings when available.

## 5. Research implications and actionable extensions
Provide concrete reusable/modifiable/replacement/new modules and serious follow-up project designs.

End with a compact technical card:

| Item | Summary |
|---|---|
| Problem | |
| Input | |
| Output | |
| Dataset | |
| Backbone | |
| Core new module | |
| Training objective | |
| Key baselines | |
| Main metrics | |
| Most important result | |
| Strongest innovation | |
| Main limitation | |
| Open source | |
| Reproducibility | |
| Best component to reuse | |
| Best component to modify | |

---

# Quality gate

Before finalizing, verify all of the following:

- [ ] The paper is explained as a scientific argument, not translated section by section.
- [ ] Input → method → output is explicit.
- [ ] Key modules include both mechanism and design motivation.
- [ ] Important equations are interpreted, not merely copied.
- [ ] Dataset splits and leakage risks are checked.
- [ ] Experiments are mapped to the hypotheses they test.
- [ ] Direct evidence is separated from author interpretation and analysis.
- [ ] Innovation is assessed against independently checked related work when retrieval is available.
- [ ] Claims beyond the paper are externally verified when possible.
- [ ] Official code is inspected when implementation/reproducibility matters and code is available.
- [ ] Limitations include mechanism and consequence, not generic criticism.
- [ ] Follow-up ideas specify concrete model/module changes and experiments.
- [ ] The response avoids excessive top-level headings.
- [ ] No missing information is silently invented.

# Optional user focus

If the user specifies a focus, preserve the full scientific context but allocate substantially more depth to that dimension. Examples:

- `重点分析模型架构和数据流`
- `重点分析 Agent 的实验评测设计`
- `重点分析代码实现和可复现性`
- `重点分析 GPCR 功能构象建模`
- `重点分析分子生成模块及其可改造空间`
- `重点分析这项工作如何转化成新的方法学课题`

If no special focus is given, use the default output structure above.
