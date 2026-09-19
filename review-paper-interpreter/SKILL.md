---
name: review-paper-interpreter
description: Systematically interpret review, survey, perspective, and roadmap papers in machine learning, deep learning, AI agents, structural biology, AIDD, CADD, and adjacent interdisciplinary fields. Use when the user asks to 解读、分析、梳理、总结 or critically assess a review-type paper, especially when the goal is to reconstruct the field taxonomy, method evolution, representative works, open problems, research gaps, and actionable research opportunities rather than merely summarize sections.
---

# Review Paper Interpreter

用于系统解读 **Review / Survey / Perspective / Roadmap** 型科研文献。重点不是逐节复述，而是从综述中恢复该领域的 **知识结构、方法谱系、技术演进、代表工作、领域共识、核心难题、研究空白与可执行启发**。

适用领域包括但不限于：
- Machine Learning / Deep Learning
- AI Agent / LLM Agent / Scientific Agent
- Structural Biology
- AIDD / CADD
- Protein / Molecular Modeling
- Drug Discovery
- 其他交叉科研方向

## Core principles

1. **不要逐段翻译或机械总结。**
2. 优先回答“这个领域是如何被组织起来的”，而不是“文章每一节写了什么”。
3. 区分三类信息：
   - `Paper`：综述作者明确陈述的观点；
   - `External evidence`：通过外部最新资料核验得到的证据；
   - `Synthesis`：基于两者形成的综合分析。
4. 对综述之外的判断、趋势、研究空白和技术现状，若允许联网，必须重新检索最新论文、预印本、代码仓库或官方资料进行验证；不得仅凭模型记忆延伸。
5. 对重要模型、数据集、工具和代表论文，尽可能提供论文与代码链接；无法确认时明确说明。
6. 不堆砌文献。优先解释**方法之间的关系、继承、替代、互补和演化逻辑**。
7. 对尚无充分证据支持的内容，不作确定性推断。
8. 一级标题保持克制；优先使用表格、二级结构和连贯论述，避免碎片化列点。

## Workflow

### Step 1 — Identify the review

首先确认：
- 题目、年份、期刊/会议；
- Review / Survey / Perspective / Roadmap 等类型；
- 核心主题；
- 覆盖的时间范围、研究对象与技术边界；
- 作者试图解决的核心问题；
- 相比已有综述的主要特色。

然后用 **3–5 句话**回答：

> 这篇综述主要回答了什么问题？它建立了怎样的领域框架？

### Step 2 — Reconstruct the field taxonomy

不要沿用文章目录机械复述。重新抽象作者的分类体系，并优先整理为：

| 研究任务 | 方法类别 | 代表方法/模型 | 输入 | 输出 | 核心思想 | 优势 | 局限 |
|---|---|---|---|---|---|---|---|

若存在技术演化关系，进一步重构：

`早期方法 → 中间阶段 → 当前主流 → 新兴方向`

解释每一代方法主要解决上一代的什么问题，又引入了什么新限制。

### Step 3 — Extract representative methods

只选择真正具有代表性的模型、算法、数据集、工具或工作，重点分析：
- 解决的问题；
- 核心架构或算法；
- 输入与输出；
- 训练数据或数据来源；
- 关键创新；
- 与相关方法的差异；
- 优势与局限；
- 是否开源；
- 是否值得复现、修改或迁移。

避免简单罗列论文标题。

### Step 4 — Determine field consensus and bottlenecks

总结当前领域：

**已基本解决 / 部分解决 / 尚未解决** 的问题。

进一步区分瓶颈来源：
- 数据；
- 模型；
- 表征；
- 泛化；
- 计算成本；
- 可解释性；
- 评测设计；
- 实验验证；
- 工程化或真实应用。

特别指出：哪些路线已经成为主流，哪些技术已经成熟，哪些仍存在明显争议或证据不足。

### Step 5 — Extract research gaps and future directions

提取作者明确提出的：
- limitations；
- challenges；
- open questions；
- future directions。

对每个重要研究空白至少回答：
1. 问题是什么？
2. 为什么重要？
3. 为什么现有方法尚未解决？
4. 属于数据、模型、表征、泛化、计算、解释性、实验还是工程问题？

### Step 6 — Update the review with current evidence

如果允许联网，针对综述中的重要判断和未来方向进行最新核验。

优先检索：
- 原始论文或官方项目页；
- 最新 peer-reviewed paper；
- arXiv / bioRxiv 等预印本；
- 官方 GitHub / Hugging Face；
- 官方数据集或 benchmark 页面。

重点回答：
- 哪些预测后来已经实现？
- 哪些问题已经出现新的解决方案？
- 哪些研究空白仍然存在？
- 综述发表后出现了哪些重要模型、方法或范式？
- 原综述的分类框架是否仍然适用？

输出时明确标记 `Paper / External evidence / Synthesis`，避免把后续研究错误归因给原综述。

### Step 7 — Translate into research value

结合用户当前科研问题，筛选真正有价值的内容。优先回答：
- 哪些原始论文值得继续精读？
- 哪些代码值得复现？
- 哪些模块值得改造？
- 哪些思想可以迁移到新的模型设计？
- 哪些空白可能形成研究课题？
- 哪些方向已经高度拥挤，不宜作为简单创新点？

如果目标涉及模型创新，优先讨论：

`修改现有模块 / 增加新模块 / 改变条件信息 / 重构训练目标 / 新增监督信号 / 改造表示学习 / 重定义任务`

而不是简单把多个现有模型首尾串成 workflow。

## Default output structure

除非用户指定其他结构，否则按以下结构输出，并避免过多一级标题。

### 1. 文献定位与核心框架
简洁说明综述定位，并给出 3–5 句核心概括。

### 2. 领域方法谱系与代表工作
使用一个核心分类表，随后解释技术演化和关键方法之间的关系。

### 3. 当前共识、瓶颈与研究空白
将“论文观点”和“最新外部证据”分开，并说明哪些问题仍未解决以及原因。

### 4. 对当前研究的启发
重点输出值得精读、复现、改造和形成新课题的方向。

最后附：

**一句话总结：** 该综述最核心的贡献。

**最重要的 3–5 个认识：** 只保留真正影响理解领域的结论。

**优先精读：** 代表论文/模型 + 原因。

**关键研究空白：** 问题 + 未解决原因。

**可执行启发：** 可借鉴 / 可改造 / 可形成研究课题。

## Domain-specific emphasis

根据文献主题动态调整分析重点：

- **ML / DL**：architecture、representation、objective、pretraining、data regime、generalization、benchmark、ablation。
- **Agent**：agent architecture、planning、tool use、memory、reflection、multi-agent coordination、environment、benchmark、success metric、failure mode。
- **Structural Biology**：structure/state representation、conformational ensemble、experimental evidence、resolution、state assignment、structure-function relationship。
- **AIDD / CADD**：task definition、protein/ligand representation、binding/activity/selectivity、dataset leakage、split strategy、docking/generation/scoring、prospective validation。
- **Generative Modeling**：conditioning、representation、generation space、objective、sampling、validity、novelty、diversity、property control、3D compatibility、experimental validation。

## Quality checks

回答前检查：
- 是否误把 Review 当成原始研究论文？
- 是否只是复述目录？
- 是否真正重建了方法分类和演化逻辑？
- 是否区分作者观点与外部最新证据？
- 是否对外部判断进行了检索核验？
- 是否给出了真正代表性的工作而非文献堆砌？
- 是否解释了研究空白“为什么没有被解决”？
- 是否把启发落实到可复现、可改造或可设计的新研究问题？
- 是否避免了过多一级标题与碎片化输出？

## Invocation examples

典型触发请求包括：
- “使用 review-paper-interpreter 解读这篇综述。”
- “系统分析这篇 Survey，并梳理方法演化和研究空白。”
- “不要逐节总结，告诉我这篇 Review 建立了怎样的领域框架。”
- “结合最新文献重新评估这篇综述提出的 future directions。”
- “从这篇 AIDD/Agent/结构生物学综述中找值得我进一步改造的模型和研究课题。”
