# Research Idea Concretizer | 研究想法具体化

[English](#english) | [简体中文](#简体中文)

<a id="english"></a>

## English

### Purpose

`research-idea-concretizer` turns a vague research seed into a portfolio of distinct, testable candidate ideas. It expands the problem space before clustering ideas and specifying the strongest candidates as **Minimum Researchable Ideas (MRIs)**.

This skill is for concretizing and diversifying ideas. It is not a literature review, a final novelty certification, or a paper-worthiness ranking.

### What it produces

- A neutral restatement of the seed, known constraints, and unknowns.
- Problem-space and capability-space maps, followed by candidate fragments across problem, object, intervention, decision locus, evidence, and evaluation.
- An orthogonalized portfolio, usually with 3–8 retained candidates when the seed supports that many. It may retain fewer rather than inventing diversity.
- An MRI record for each retained candidate: **Problem + Gap + Hypothesis + Method + Evaluation + Contribution**, with baselines, falsification conditions, assumptions, risks, and a verification queue.
- Maturity labels and a handoff for downstream idea evaluation. The skill does not declare a winner unless asked to evaluate the candidates as a separate task.

### Install

Use the complete `research-idea-concretizer/` directory with an AI environment that supports Agent Skills. Keep `SKILL.md`, `schemas/`, `templates/`, `rubrics/`, `references/`, `examples/`, `scripts/`, and the other package files together.

From the repository root, copy the folder into the skills directory configured for your host:

```bash
cp -r research-idea-concretizer <host-skills-directory>/
```

Replace `<host-skills-directory>` with the directory used by your environment, or use that environment’s supported skill-import flow.

### Use

Give the skill a seed and any constraints you already know. A one-sentence seed is enough to begin; do not invent novelty claims or assets that were not provided.

```text
Use research-idea-concretizer to expand this seed into several genuinely distinct research ideas.
Preserve uncertainty, specify falsifiable hypotheses and credible baselines, and defer claims that need evidence.

Seed: [your seed]
Constraints or available resources: [optional]
Evidence mode: [evidence-backed if sources are available and permitted; otherwise offline]
```

The skill can work in either of two modes:

- **Evidence-backed:** use permitted literature, web, repository, or database sources; record the search scope, collisions, and unresolved evidence.
- **Offline:** mark novelty and gap statements as provisional, and provide a verification queue. Lack of a known paper is not evidence of novelty.

### Scientific boundaries

- Candidate gaps may be `verified`, `partially verified`, or `unverified`; do not present an unverified gap as an established fact.
- A mature label means the idea is sufficiently specified for downstream evaluation. It does not certify novelty, feasibility, or likely publication success.
- For Agent ideas, distinguish adaptive scientific decisions from a predetermined workflow, and separate the value of orchestration from the underlying model.
- If the seed supports fewer than three defensible candidates, report that instead of fabricating a larger portfolio.

### Validate a candidate JSON file

The included validator checks JSON structure against the package schema. From the repository root:

```bash
python -m pip install jsonschema
python research-idea-concretizer/scripts/validate_candidate.py research-idea-concretizer/examples/example-candidate.json
```

A `VALID` result confirms schema compliance only; it does not establish scientific quality, novelty, or biological/experimental validity.

### Package contents

- `SKILL.md` — complete workflow and output requirements.
- `schemas/` — machine-readable candidate record schema.
- `templates/` — compact and full report formats.
- `rubrics/` — maturity and orthogonality checks.
- `references/` — design rationale.
- `examples/` and `tests/` — illustrative inputs, outputs, and qualitative behavior cases.
- `scripts/` — JSON Schema validator.

### Version

See `VERSION` and `CHANGELOG.md`.

---

<a id="简体中文"></a>

## 简体中文

### 用途

`research-idea-concretizer` 用于把模糊的研究 seed 扩展成多个彼此有实质区别、可检验的候选 idea。它先展开问题空间，再对候选进行聚类和正交性筛选，并把保留的 idea 具体化为**最小可研究 idea（Minimum Researchable Idea，MRI）**。

这个 skill 负责 idea 的具体化与多样化；它不替代文献综述、最终新颖性认证或论文潜力排名。

### 输出内容

- 对 seed 的中性重述，以及已知约束和未知事项。
- 问题空间与能力空间图谱，并围绕问题、对象、干预、决策位置、证据和评估构造候选片段。
- 一组经过正交性筛选的候选；seed 支持时通常保留 3–8 个。若有依据的候选不足 3 个，会如实报告，不会为了凑数而制造差异。
- 每个保留候选的 MRI 记录：**问题 + 缺口 + 假设 + 方法 + 评估 + 贡献**，并补充基线、证伪条件、关键假设、风险和待核实事项。
- 成熟度标记和供下游 idea 评估使用的交接摘要。除非用户另行要求评估候选，否则 skill 不会直接宣布胜出者。

### 安装

在支持 Agent Skills 的 AI 环境中使用完整的 `research-idea-concretizer/` 目录。请保留 `SKILL.md`、`schemas/`、`templates/`、`rubrics/`、`references/`、`examples/`、`scripts/` 等配套文件。

在仓库根目录执行，将整个文件夹复制到当前环境配置的 skills 目录：

```bash
cp -r research-idea-concretizer <host-skills-directory>/
```

请把 `<host-skills-directory>` 替换为你所用环境的实际目录；也可以使用该环境支持的 skill 导入流程。

### 使用

向 skill 提供一个 seed 和已知约束即可开始；一句话 seed 也可以。不要补造用户未提供的新颖性结论或可用资源。

```text
使用 research-idea-concretizer 把下面的 seed 扩展为多个真正不同的研究 idea。
保留不确定性，为每个 idea 写出可证伪假设和可信基线；需要证据支持的结论先列为待核实事项。

Seed：[填写 seed]
约束或可用资源：[可选]
证据模式：[有许可且来源可用时选择证据支持模式，否则选择离线模式]
```

两种工作模式：

- **证据支持模式：** 在用户许可且来源可用时检索文献、网页、代码仓库或数据库，并记录检索范围、相似工作和未解决的证据问题。
- **离线模式：** 将新颖性和研究缺口标记为暂定判断，并列出后续核查清单。不知道某篇论文，不等于已经证明新颖。

### 科学边界

- 候选缺口可标记为 `verified`、`partially verified` 或 `unverified`；未经核实的缺口不能写成已确立事实。
- “成熟”表示 idea 的定义足以进入下游评估，不代表其新颖性、可行性或发表前景已经得到证明。
- 对 Agent idea，要区分自适应科学决策与预设流程，并把编排带来的价值与底层模型的价值分开评估。
- 如果 seed 只能支持少于 3 个有依据的候选，应如实说明，不要人为扩充组合。

### 校验候选 JSON

随包校验器会按 Schema 检查 JSON 结构。从仓库根目录执行：

```bash
python -m pip install jsonschema
python research-idea-concretizer/scripts/validate_candidate.py research-idea-concretizer/examples/example-candidate.json
```

输出 `VALID` 只表示结构符合 Schema，不代表 idea 的科学质量、新颖性或生物学/实验有效性已经得到验证。

### 文件说明

- `SKILL.md`：完整工作流程与输出要求。
- `schemas/`：候选记录的机器可读 Schema。
- `templates/`：精简版与完整版报告模板。
- `rubrics/`：成熟度和正交性检查标准。
- `references/`：设计依据。
- `examples/` 和 `tests/`：示例输入输出与定性行为用例。
- `scripts/`：JSON Schema 校验器。

### 版本

版本信息见 `VERSION`，更新记录见 `CHANGELOG.md`。