# Research Idea Paper Potential Skill / 研究想法与论文潜力评估 Skill

[English](#english) | [简体中文](#简体中文)

<a id="english"></a>

## English

### Purpose

This Agent Skill evaluates whether a research idea can support:

1. a **defensible research paper**; and
2. a **high-quality research paper**, if the work succeeds.

It also has a separate module for **Scientific Agent / AI-for-Science** ideas. Use it for early-stage idea triage, proposal refinement, project go/no-go decisions, paper positioning, and reviewer-style stress testing.

The evaluator follows this chain:

`important question -> authentic knowledge gap -> falsifiable claim -> discriminating evidence -> defensible conclusion`

Engineering complexity, benchmark gains, or an “A applied to B” combination do not count as scientific contribution by themselves.

### How to use

1. Add the complete `research-idea-paper-potential` folder to an AI environment that supports Agent Skills. Keep `SKILL.md`, `references/`, `assets/`, `scripts/`, and the other package files together.
2. Describe the idea and what you want to decide. Incomplete ideas are accepted; unknown facts should be identified rather than invented.
3. Choose a focus by asking for an initial triage, strict reviewer analysis, comparison of several ideas, or the Scientific Agent module.

For Claude Code, from the repository root:

```bash
# Global installation
cp -r research-idea-paper-potential ~/.claude/skills/

# Project-only installation
mkdir -p .claude/skills
cp -r research-idea-paper-potential .claude/skills/
```

Example prompts:

**Initial triage**

```text
Use the research-idea-paper-potential skill to assess this idea.
Give a provisional verdict, identify the biggest unknowns, and propose the
smallest decisive evidence package.
<describe the idea>
```

**Strict novelty and reviewer analysis**

```text
使用 research-idea-paper-potential 评估下面的研究想法。
请检索并核验最接近的已有工作，标明检索范围和证据依据，
然后进行严格的审稿人攻击。
<描述研究想法>
```

**Compare ideas**

```text
Compare these ideas with the research-idea-paper-potential skill.
Use the same criteria for each, explain uncertainty, and recommend which
idea to investigate first.
<idea A>
<idea B>
<idea C>
```

**Scientific Agent idea**

```text
Evaluate this Scientific Agent idea. Focus on Agent necessity,
scientific autonomy, and independently validated discovery value.
Compare it against a fixed workflow with the same tools and budget.
<describe the idea>
```

### What to provide

More detail improves the evaluation, but none of these fields is required to begin:

- problem and why it matters;
- what is unknown or inadequate;
- proposed hypothesis or central claim;
- closest prior work you know;
- proposed method and decisive experiments;
- available data, tools, samples, compute, expertise, time, and budget;
- intended field, audience, or venue;
- for an Agent idea, which scientific decisions the Agent would make and how it adapts to evidence.

A one-sentence idea is enough for a provisional first pass. The report should then mark unknowns and state what evidence would raise confidence.

### What the report contains

- normalized problem, gap, claim, method, evidence, and payoff;
- 11 core dimensions scored from 0 to 5, with rationale, confidence, and evidence basis;
- **Paperability Score /100** and **High-Quality Potential Score /100**;
- fatal-flaw gates and a Go / Conditional Go / Reframe / No-Go recommendation;
- at least three reviewer attacks and the strongest alternative explanation;
- a prioritized minimum decisive evidence package and development path;
- for Agent ideas, separate **Agent necessity /8**, **Scientific autonomy /10**, and **Scientific discovery value /12** scores.

The two 100-point scores are structured decision aids, **not calibrated probabilities**. A fatal flaw can override a high score. Novelty or knowledge-gap judgments must be labeled provisional when current prior art cannot be checked.

### Package layout

```text
research-idea-paper-potential/
├── SKILL.md
├── README.md
├── MANIFEST.md
├── .gitattributes
├── FILE_CHECKSUMS.txt
├── references/   # Rubrics, scoring model, evidence levels, fatal flaws, reviewer attacks
├── assets/       # Report template, idea intake template, JSON schema
├── examples/     # Synthetic calibration examples
├── evals/        # Behavioral cases and expected behaviors
└── scripts/      # Dependency-free score calculator
```

### Design basis

The package follows the Agent Skills pattern: a directory anchored by `SKILL.md` front matter, with optional references, scripts, assets, examples, and evaluation materials.

- [OpenAI Skills guide](https://developers.openai.com/api/docs/guides/tools-skills)
- [OpenAI plugin Skills concept](https://developers.openai.com/plugins/concepts/skills)
- [Building skills](https://developers.openai.com/plugins/build/skills)

### Version

`1.0.2`

---

<a id="简体中文"></a>

## 简体中文

### 用途

这个 Agent Skill 用来评估一个研究想法是否有潜力形成：

1. **可辩护的研究论文**；以及
2. 在研究顺利完成时，是否具备成为**高质量研究论文**的潜力。

它还包含面向 **Scientific Agent / AI for Science** 研究的独立评估模块。适用于早期选题筛查、项目申请书完善、项目立项或停止决策、论文定位和审稿人视角压力测试。

核心判断链为：

`重要问题 -> 真实知识空白 -> 可证伪主张 -> 有区分力的证据 -> 可辩护结论`

工程复杂度、基准指标提升，或简单组合“方法 A 用于领域 B”，本身不等于科学贡献。

### 使用方法

1. 将完整的 `research-idea-paper-potential` 文件夹加入支持 Agent Skills 的 AI 环境。请保留 `SKILL.md`、`references/`、`assets/`、`scripts/` 和其他配套文件的相对结构。
2. 描述研究想法以及你希望据此做出的判断。可以从不完整的想法开始；缺失的信息应标为未知，不应凭空补齐。
3. 指定评估重点：初步筛查、严格审稿分析、多想法比较，或 Scientific Agent 专项评估。

在 Claude Code 中，可在仓库根目录执行：

```bash
# 全局安装
cp -r research-idea-paper-potential ~/.claude/skills/

# 仅当前项目安装
mkdir -p .claude/skills
cp -r research-idea-paper-potential .claude/skills/
```

调用示例：

**初步筛查**

```text
使用 research-idea-paper-potential skill 评估这个想法。
给出初步结论，指出最大的未知因素，并提出最小决定性证据包。
<描述研究想法>
```

**严格核查新颖性并进行审稿人攻击**

```text
Use research-idea-paper-potential to evaluate this research idea.
Search for and verify the closest prior work, state the search scope and evidence,
then perform a strict reviewer-style attack.
<describe the research idea>
```

**比较多个想法**

```text
请用 research-idea-paper-potential 按相同标准比较下面几个想法，
解释每个判断的不确定性，并建议优先验证哪个想法。
<想法 A>
<想法 B>
<想法 C>
```

**Scientific Agent 想法**

```text
Evaluate this Scientific Agent idea. Focus on Agent necessity,
scientific autonomy, and independently validated discovery value.
Compare it against a fixed workflow using the same tools and budget.
<describe the idea>
```

### 建议提供的信息

信息越完整，判断越准确；但开始评估不要求填完所有内容：

- 研究问题及其重要性；
- 当前未知、证据不足或尚未解决的部分；
- 研究假设或核心主张；
- 你已知的最接近的已有工作；
- 计划使用的方法和决定性实验；
- 可用的数据、工具、样本、算力、专业人员、时间和预算；
- 目标领域、读者或期刊；
- 对 Agent 想法，说明 Agent 会做哪些科学决策，以及它如何根据证据调整策略。

只提供一句话也可以先做初步评估。报告应明确列出未知信息，以及提高判断置信度所需的证据。

### 评估报告内容

- 规范化后的问题、知识空白、主张、方法、证据和预期价值；
- 11 个核心维度的 0–5 分评价，并说明理由、置信度和证据依据；
- **论文可辩护性评分 /100** 与 **高质量论文潜力评分 /100**；
- 致命缺陷门槛及 Go / Conditional Go / Reframe / No-Go 建议；
- 至少三个审稿人可能提出的质疑，以及最强替代解释；
- 按优先级排列的最小决定性证据包和后续研究路径；
- 对 Agent 想法，另行报告 **Agent 必要性 /8**、**科学自主性 /10** 和 **科学发现价值 /12**。

两个百分制评分是结构化决策辅助，**不是经过校准的概率**。致命缺陷可以推翻高分。如果无法核查最新的相关研究，关于新颖性和知识空白的判断必须标为暂定结论。

### 文件结构

```text
research-idea-paper-potential/
├── SKILL.md
├── README.md
├── MANIFEST.md
├── .gitattributes
├── FILE_CHECKSUMS.txt
├── references/   # 评分标准、评分模型、证据等级、致命缺陷和审稿人质疑
├── assets/       # 报告模板、想法信息模板和 JSON Schema
├── examples/     # 用于校准的合成示例
├── evals/        # 行为测试案例和预期表现
└── scripts/      # 无第三方依赖的计分脚本
```

### 设计依据

本目录采用 Agent Skills 文件结构：以包含 front matter 的 `SKILL.md` 为入口，并可配套参考资料、脚本、模板、示例和评估材料。

- [OpenAI Skills 指南](https://developers.openai.com/api/docs/guides/tools-skills)
- [OpenAI 插件中的 Skills 概念](https://developers.openai.com/plugins/concepts/skills)
- [构建 Skills](https://developers.openai.com/plugins/build/skills)

### 版本

`1.0.2`
