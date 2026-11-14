# literature — 文献管理工具集

面向科研场景的一站式文献工具集，包含十部分：

1. **文献智能管理系统**（桌面应用）—— PDF 文献入库、元数据自动解析、AI 深度分析与课题建议生成；
2. **Claude 文献阅读 Skills** —— 两个可安装的 skill，分别用于深度解读**研究型论文**和**综述型论文**；
3. **研究想法具体化 Skill** —— 从模糊 seed 展开多个彼此不同、可检验的候选 idea；
4. **研究想法评估 Skill** —— 从科学问题、创新性、证据和可行性等维度评估候选 idea 的论文潜力；
5. **药物属性预测手稿 Skills** —— 分别从零组织首稿、重建已有手稿，使用真实范文校准写作与图表表达，并遵守实验和证据边界。
6. **综述选题孵化 Skill** —— 通过多轮批判性学术讨论，把拟定标题与初步目标推进为可交接的综述研究框架；
7. **证据优先综述写作 Skill** —— 真实检索、逐条核验、方法学分类与英文综述逐章写作，强制来源—证据—论断三层可溯源；
8. **AIDD 综述手稿重构 Skill** —— 面向已有英文综述，重建证据支持的分类、比较与批判性综合；
9. **科研演示文稿设计 Skill** —— 将真实实验报告、结果和图表转化为可编辑、可追溯的科研汇报 PPT；
10. **科学综述演示文稿设计 Skill** —— 面向文献综述汇报，组织方法谱系、证据比较、矛盾与研究空白。

领域背景：结构生物学（Structural Biology）/ 计算机辅助药物设计（CADD）/ AIDD / 细胞生物学 / 机器学习交叉方向。

## 项目结构

```
literature/
├── research-paper-interpreter/      # Skill 1：研究型论文深度解读
│   └── SKILL.md
├── review-paper-interpreter/       # Skill 2：综述型论文系统解读
│   └── SKILL.md
├── research-idea-concretizer/      # Skill 3：模糊 seed 到候选 idea 具体化
│   ├── SKILL.md
│   ├── README.md
│   ├── .gitattributes
│   ├── CHANGELOG.md
│   ├── MANIFEST.sha256
│   ├── VERSION
│   ├── schemas/
│   ├── templates/
│   ├── rubrics/
│   ├── references/
│   ├── examples/
│   └── scripts/
├── research-idea-paper-potential/  # Skill 4：研究想法与论文潜力评估
│   ├── SKILL.md
│   ├── README.md
│   ├── MANIFEST.md
│   ├── FILE_CHECKSUMS.txt
│   ├── .gitattributes
│   ├── references/
│   ├── assets/
│   ├── examples/
│   ├── evals/
│   └── scripts/
├── aidd-review-manuscript-rebuild/        # 已有 AIDD 英文综述手稿重构
│   ├── SKILL.md、README.zh-CN.md、references/、assets/、examples/、scripts/、tests/
├── drug-property-manuscript-from-scratch/  # 从中文笔稿、研究意图和实验材料组织首稿
│   ├── .gitattributes
│   ├── SKILL.md
│   ├── README.zh-CN.md
│   ├── agents/
│   ├── assets/
│   ├── examples/
│   └── references/
├── drug-property-manuscript-rebuild/       # 基于真实范文重建已有论文手稿
│   ├── .gitattributes
│   ├── SKILL.md
│   ├── README.zh-CN.md
│   ├── assets/
│   ├── examples/
│   └── references/
├── review-dialogue-architect/        # 综述选题孵化与批判性讨论（流水线上游，v1.1）
│   ├── CHANGELOG.md
│   ├── SKILL.md
│   ├── agents/
│   ├── assets/
│   ├── references/
│   ├── scripts/
│   ├── evals/
│   └── tests/
├── evidence-first-review-writer/    # 证据优先的英文综述写作（流水线下游）
│   ├── SKILL.md
│   ├── assets/
│   ├── references/
│   ├── scripts/
│   ├── evals/
│   └── tests/
├── scientific-presentation-designer/ # 真实实验材料到科研汇报 PPT
│   ├── SKILL.md、README_zh.md、agents/、examples/、references/、scripts/
├── review-presentation-designer/     # 文献综述汇报与证据可视化 PPT
│   ├── SKILL.md、README_zh.md、agents/、examples/、references/、scripts/
├── main.py                         # 文献管理系统 v1（初版）
├── main_v4.py                      # 文献管理系统 v4（功能完整版，推荐）
├── main_v4_clean.py                # v4 精简版（用于 PyInstaller 打包）
├── requirements.txt                # Python 依赖
└── .github/
    └── workflows/
        └── build-macos.yml         # macOS 应用自动打包
```

---

## Skills：文献阅读、研究构思、论文写作与科研演示工作流

两个论文解读 skill 都遵循同一套核心原则：**不做逐段翻译或机械总结**，而是把论文当作"科研对象"来重建其科学逻辑，并明确区分三类信息——`Paper`（论文原文陈述）、`External evidence`（联网核验的外部证据）、`Synthesis`（综合分析）。允许联网时会主动检索最新文献、预印本和官方代码仓库进行核验。

两者的区别在于论文类型不同、解读目标不同：

| | research-paper-interpreter | review-paper-interpreter |
|---|---|---|
| **适用论文类型** | 原始研究论文（Research Article） | 综述 / Survey / Perspective / Roadmap |
| **核心目标** | 还原"这项工作做了什么、为什么这样设计、证据是什么" | 重建"这个领域如何被组织、方法如何演化、空白在哪里" |
| **典型输出** | 方法机制拆解、实验证据审计、创新性评估、代码与可复现性分析、可执行的后续研究设计 | 领域分类谱系表、技术演进脉络、代表工作剖析、领域共识与瓶颈、研究空白与选题启发 |
| **典型触发语** | "解读这篇论文"、"分析它的模型架构和实验"、"评估可复现性" | "解读这篇综述"、"梳理方法演化和研究空白"、"结合最新文献评估这篇 Survey 的 future directions" |

研究想法工作流可以串联两个 skill：`research-idea-concretizer` 先从模糊 seed 扩展并正交化多个候选，再由 `research-idea-paper-potential` 评估候选的论文潜力。前者负责具体化与多样化，不替后者选出胜者。

### research-idea-concretizer（模糊 seed 到候选 idea 具体化）

把一个模糊研究 seed 系统地展开为多个彼此不同、可证伪、可评估的候选 idea。

- 先扩展问题空间与能力空间，再按核心科学问题聚类，避免只替换模型或数据集造成伪多样性
- 为每个保留候选明确问题、研究缺口、假设、方法、评估和预期贡献，并补充基线、证伪条件、关键假设、风险与待核实事项
- 对新颖性与研究缺口标注核验状态；未核实的内容不会写成既定事实
- seed 支持时通常保留 3–8 个候选；若有依据的候选更少，就如实说明
- 详细说明见 [research-idea-concretizer/README.md](research-idea-concretizer/README.md)

### research-idea-paper-potential（研究想法与论文潜力评估）

用于早期研究构思筛选和项目决策，区分“是否能形成可辩护论文”与“高质量论文的潜力上限”。

- 以研究问题、知识空白、可证伪主张、判别性证据和可行性为核心
- 使用致命缺陷门槛和审稿人攻击，避免强项平均掩盖阻断性问题
- 对 Scientific Agent 想法单独评估 Agent 必要性、科学自主性和发现价值
- 输出最小决定性证据包、Go / Conditional Go / Reframe / No-Go 建议及当前可辩护的论文定位

### drug-property-manuscript-from-scratch（药物属性预测论文从零成稿）

面向已有实验材料、但还没有完整手稿的研究者，从中文笔稿、研究意图、实验结果和图表中恢复研究事实与证据边界，学习适配的真实范文写法，并完成英文首稿。

- 适用于中文笔稿、零散研究记录、粗略研究意图或以图表为主的材料
- 通过真实范文拆解、迁移卡、段落与图表规划、小样比较，推进到完整工作稿
- 与 [drug-property-manuscript-from-scratch/README.zh-CN.md](drug-property-manuscript-from-scratch/README.zh-CN.md) 配套

### drug-property-manuscript-rebuild（药物属性预测手稿重建 v2）

面向已有完整手稿的重写任务，围绕具体范文拆解、写法迁移、真实小样对照和迭代修订，改善论证、段落组织、图表与表格表达。

- 适用于已有论文初稿，且希望提升论文论证或视觉表达的项目
- 保留已完成实验和原始文件；科学主张以实际证据为边界
- 与 [drug-property-manuscript-rebuild/README.zh-CN.md](drug-property-manuscript-rebuild/README.zh-CN.md) 配套

两个药物手稿 skill 可独立使用；按项目材料的起点选择对应流程。

### aidd-review-manuscript-rebuild（AIDD 英文综述既有手稿重构）

面向已有 AIDD 英文综述的结构、证据、分类体系、跨研究可比性、批判性综合和图表重构。适用于 Narrative-Critical Review、Technical Survey、Scoping Review、Systematic Review 或 Perspective；只有实际完成了相应检索与筛选流程时才报告系统综述方法。

- 将原始来源与论断逐项对应，区分来源报告、作者综合、作者提出框架和未核验内容
- 检查 AIDD 任务、数据、划分、标签、指标与验证层级，避免不成立的跨论文排名
- 通过真实综述范文校准段落与图表表达，并交付可编辑手稿、引用、图表和问题清单
- 与研究型论文重构 Skill `drug-property-manuscript-rebuild` 并行使用；综述手稿使用本 Skill，原始实验研究论文使用研究型重构 Skill
- 详见 [aidd-review-manuscript-rebuild/README.zh-CN.md](aidd-review-manuscript-rebuild/README.zh-CN.md)

### research-paper-interpreter（研究型论文解读）

把研究论文解读为**技术研究对象**，回答：这项工作到底做了什么、为什么这样设计、证据是否支撑结论、真正的新意在哪里、弱点是什么、可复现性如何、如何以它为起点做出更好的研究。

- 11 步工作流：确立研究契约 → 端到端方法重建 → 关键模块拆解 → 数据与监督审计 → 实验即假设检验 → 结果分层提取 → 创新性定位 → 局限与失效模式 → 代码审计 → 研究版图定位 → 转化为研究方向
- 支持模型 / Agent / 结构生物学 / AIDD·CADD 四类领域适配器
- 有官方代码时会同时分析论文与代码实现，指出不一致之处

### review-paper-interpreter（综述型论文系统解读）

把综述解读为**领域知识地图**，重点不是复述目录，而是从综述中恢复知识结构、方法谱系、技术演进、代表工作、领域共识、核心难题与可执行启发。

- 7 步工作流：确认综述定位 → 重建领域分类体系 → 提取代表性方法 → 判断领域共识与瓶颈 → 提取研究空白 → 联网更新综述时效性 → 转化为科研价值
- 会针对综述发表后的进展做**时效核验**：哪些预测已实现、哪些空白已被填补、原分类框架是否仍然适用
- 输出"优先精读清单 + 关键研究空白 + 可执行启发"，直接服务于选题

---

## 综述写作流水线：从选题孵化到证据驱动的英文成稿

`review-dialogue-architect` 与 `evidence-first-review-writer` 是一条前后衔接的流水线，而不是两个可互相替代的工具：

| | review-dialogue-architect | evidence-first-review-writer |
|---|---|---|
| **负责** | 问题表述（problem formulation）、概念推理、批判性对话、交接 | 真实检索、来源筛选、论断核验、证据综合、英文撰稿 |
| **不负责** | 检索文献、核验引文、撰写正文 | 替用户决定研究定位与最终判断 |
| **输入** | 英文拟定标题 + 初步研究目标 | `topic.md` + `discussion_summary.md` + 可选 `existing_papers.bib` |
| **输出** | `input/discussion_summary.md`（14 章节、带溯源标签） | `review_brief.md`、`records.csv`、`evidence.csv`、`claims.csv`、`manuscript.md`、审计报告 |
| **核心约束** | 不把 AI 建议当成用户确认，不虚构讨论 | 不把讨论总结当文献证据，不编造文献、检索数量与 DOI |

关键设计：**ChatGPT 讨论总结属于待核实的研究输入，不是可以直接引用的文献证据**。若把讨论总结直接交给写作 Skill 扩写成正文，其中未经核实的判断、分类和参考文献会原样进入稿件。正确做法是把它转成待研究问题、待检索方向与待核验论断清单。

---

### review-dialogue-architect（综述选题孵化与批判性讨论，v1.1）

把一个拟定英文标题和初步研究目标，通过**多轮真实对话**逐步推进为可交接的研究框架，最终产出 `discussion_summary.md` 交给下游 `evidence-first-review-writer`。它不是一次性生成综述大纲的工具，而是交互式的科研构思与学术讨论 Skill。

- **五种模式**：`interactive`（默认，多轮讨论）、`bootstrap`（暂时无法回答时先给明确标记为 provisional 的框架）、`resume`（接续已有讨论记录，保留既有决定与反转）、`export`（导出交接文件）、`revise`（接受新修正，并作废依赖旧假设的分类节点）
- **默认 10–12 轮实质交换**：一轮指研究者给出真实输入或决策、助手给出有信息量的科学分析；内部推理、工具调用与虚构的“用户回答”都不计入。轮数是目标而非配额——简单题目可以更早收敛，争议大的题目可以到 15–25 轮，研究者任何时候要求导出都应当被接受（未解决部分标 `provisional`）
- **P1–P4 阶段门槛 + P5 作者控制的交接**：定位 → 竞争性框架（至少两套组织方案互相压力测试）→ 批判性评估（反例、证据缺口、评测可比性、审稿人质疑）→ 研究收敛；门槛只有在相关议题被**批判性检验**后才算通过，大纲里出现相关措辞不算，研究者主动延后的问题要如实记录为延后
- **15 个覆盖维度**按 `absent` / `proposed` / `examined` 记录（P1 4 项、P2 4 项、P3 3 项、P4 4 项）；分类体系在被文献证实前一律按假设处理
- **饱和启发式与自适应延长**：若最近三轮*已记录*的交换没有产生实质新见解，不自动结束，而是换视角、引入反例；12 轮后仍有未决高优先级争议或门槛未过时，说明未决项并提出有理由的 +3 轮延长。这个判断只是标注式启发，不是语义上的“研究已充分”证明
- **8 种溯源状态**，并区分决策状态与证据状态：`USER_GIVEN` / `USER_CONFIRMED` / `ASSISTANT_PROPOSED` / `OPEN` / `DISPUTED`，以及 `BACKGROUND_UNVERIFIED` / `SOURCE_LOCATED` / `SOURCE_CHECKED`（只核对元数据不算 `SOURCE_CHECKED`）
- 每轮至少给出一条新推论、实质批评或有信息量的替代方案，并说明它对综述设计的影响；每轮最多只提一个高影响的研究决策问题，已答复的不再追问
- 明确禁止编造用户确认、文献检索结果或实验发现；一个模型扮演多个审稿人只是"一个模型的多种批评"，不是多个独立专家评审
- 完整规则见 [review-dialogue-architect/SKILL.md](review-dialogue-architect/SKILL.md)，版本变更见 [CHANGELOG.md](review-dialogue-architect/CHANGELOG.md)

第一次使用只需要两个输入，不必预先准备文献清单或大纲：

- **输入 A**：拟定的英文综述标题（可以是暂定标题）
- **输入 B**：初步研究目标（允许是尚未整理清楚的思路）

启动提示词：

```text
请使用 $review-dialogue-architect Skill。

综述标题：
<英文题目>

初步研究目标：
<目标，可以写得比较粗略>

请进入 INTERACTIVE 模式：
- 首先分析研究定位和潜在问题。
- 独立提出替代框架与学术质疑。
- 与我逐轮深入讨论。
- 保留已确认和未解决的问题。
- 不要立即生成最终总结或正文。
- 只有当我要求导出时，才输出 discussion_summary.md。
```

讨论过程中的反馈可以像正常科研争论一样直接，例如"我认为按 Attention 类型分类不合理，这些方法可能同时具备多种交互机制，请重新审视分类维度"。Skill 应当据此重做分析，而不是坚持原框架，也不应把先前的建议自动标为用户已认可。

讨论成熟后导出：

```text
请使用 $review-dialogue-architect 的 EXPORT 模式，生成 input/discussion_summary.md：

要求：
- 严格遵循 Skill 规定的 14 章节结构。
- 保留原始目标、已确认决定、被否定方案及原因。
- 区分 USER_CONFIRMED、ASSISTANT_PROPOSED、OPEN、DISPUTED。
- 区分已核验证据与待验证科学假设。
- 包含最终方法学分类、英文大纲和图表规划。
- 包含后续真实文献检索与核验任务。
- 不得编造文献、科研结论或用户确认。
- 输出必须独立于当前对话，能直接供下游 Skill 使用。
- 导出后做完整性检查，不要开始正文写作。
```

导出文件是**研究构思的交接件**，不是已经完成文献验证的综述正文。

可选的本地对话追踪器 `scripts/dialogue_tracker.py`（标准库，只把自报标注写成 JSON，不读对话、不判语义、不替代研究者判断）：

```bash
python scripts/dialogue_tracker.py init   --project ./my-review
python scripts/dialogue_tracker.py record --project ./my-review --phase P2-frameworks --novelty substantial \
    --user-input "<研究者本轮的真实输入>" --analysis "<本轮给出的分析>" --question "<一个关键问题>"
python scripts/dialogue_tracker.py coverage --project ./my-review --dimension taxonomy --level examined
python scripts/dialogue_tracker.py issue    --project ./my-review --severity critical --description "<未决争议>"
python scripts/dialogue_tracker.py resolve  --project ./my-review --id I1 --resolution "<处理结论>"
python scripts/dialogue_tracker.py extend   --project ./my-review --reason "<未决高优先级项>" --rounds 3
python scripts/dialogue_tracker.py status   --project ./my-review
```

它的回归测试只验证代码行为（例如 critical 争议即使覆盖度满也不得出"可以导出"的结论），
**不验证研究质量，也不证明对话中真的获得了作者同意**。

### evidence-first-review-writer（证据优先的英文综述写作）

按 `narrative-critical`（默认）/ `systematic` / `scoping` 三种综述类型，把上游的研究框架推进为可溯源的英文综述。核心是三个必须分开的问题：**(1) 文献是否存在；(2) 文献是否支持这条确切论断；(3) 证据的可信度与适用性如何**——DOI 解析成功只回答了第一条的一部分。

- **三层证据链**：`records.csv`（候选记录，稳定 ID）→ `evidence.csv`（章节/页码/图表、被测论断、数据设置、模型、对照、指标、划分、局限）→ `claims.csv`（每条论断绑定一条或多条证据，必须含反证）
- 检索结果在核对标题/年份/DOI 前一律标 `metadata_status=unverified`；论断在原文核实前一律 `support_status=unknown`；只读到摘要时必须披露
- **不允许**在未实际完成检索、筛选、登记的情况下自称 systematic / scoping / PRISMA-compliant，也不允许编造检索数量、检索日期或"已做双人筛选"
- 保留矛盾结论与负面结果，区分同一数据集下的头对头比较与跨论文数字：划分方式、靶点重叠、数据泄漏、测定端点不同都会让朴素排名失效
- 未真正执行时可用的工具：Europe PMC 检索（`search_epmc.py`）与 Crossref DOI 元数据核对（`verify_dois.py`），两者都是**可选联网**工具，网络失败时不写盘、不假装完成
- 完整规则见 [evidence-first-review-writer/SKILL.md](evidence-first-review-writer/SKILL.md)

六阶段推进，每个阶段都有可检查的产物：

| 阶段 | 交给 Skill 的任务 | 应得到的结果 |
|---|---|---|
| 1. 定位 | 分析标题、讨论总结与已有综述 | `review_brief.md`、创新定位、候选大纲 |
| 2. 文献检索 | 设计并执行多源学术检索 | `records.csv`、`search_log.csv` |
| 3. 文献核验 | 去重、筛选、读取全文、提取证据 | `screening.csv`、`evidence.csv` |
| 4. 分类与综合 | 比较模型、方法与局限，检验分类是否被文献支持 | Taxonomy、比较矩阵、`claims.csv` |
| 5. 英文写作 | 基于已核验证据逐章写作 | `manuscript.md` |
| 6. 审稿修订 | 检查论断、引文、逻辑与格式要求 | 审计报告、修改后的稿件 |

建议的第一阶段提示词（明确要求"先不写正文"）：

```text
请使用 $evidence-first-review-writer Skill，开始一个英文科研综述项目。

输入文件：
1. input/topic.md：综述主题及初步研究目标。
2. input/discussion_summary.md：此前与 ChatGPT 深入讨论后的总结。
3. input/existing_papers.bib：已有参考文献（如果存在）。

基本要求：
- 目标是具有批判性分析的英文科研综述。
- 默认采用 Critical Narrative Review。
- ChatGPT 讨论总结仅作为研究输入，不能直接当作文献证据。
- 不要立即撰写英文正文。

第一阶段：
1. 分析标题、研究边界和综述定位。
2. 提取已有研究思路、方法分类、关键论断和争议点。
3. 标记已核实、待核实、作者提出和存在争议的内容。
4. 检索已有相关综述，分析差异化贡献。
5. 提出分类体系、英文大纲和文献检索计划。
6. 输出 Markdown 文件供审核。

完成第一阶段后停止，不自动进入正文写作。
```

建议人工把关的三个节点：

- **节点 A：研究定位与分类体系** —— 与已有综述相比是否有足够明确的学术贡献；分类轴是否同层级、是否重叠
- **节点 B：核心文献与证据矩阵** —— 覆盖是否合理、证据是否充分、有无明显遗漏与不公平比较
- **节点 C：英文综述完整大纲** —— 章节之间的论证关系、表格与图示设计是否成立

本地辅助命令（标准库即可，在 Skill 目录下运行）：

```bash
python scripts/reviewkit.py init --out ./my-review --topic "<主题>" --type narrative-critical
python scripts/search_epmc.py --project ./my-review --query "<检索式>" --max-results 100   # 需联网
python scripts/reviewkit.py dedupe --input ./my-review/records.csv --out ./my-review
python scripts/reviewkit.py audit  --project ./my-review --manuscript ./my-review/manuscript.md
python scripts/verify_dois.py --records ./my-review/records.csv --out ./my-review/doi_report.csv  # 需联网
```

注意这些脚本的能力边界：`audit` 只校验 ID、模式链接与引用键，不判断科学真伪；`verify_dois` 只核对 Crossref 的题名/年份身份，不证明文献支持某条论断，也不会自动提升元数据核验状态。它们也不是"能自动访问所有学术数据库、读完所有全文并直接投稿"的系统——第二阶段必须真实执行检索，不能由模型凭记忆生成文献清单。

### scientific-presentation-designer（科研汇报 PPT）

把研究报告、CSV/JSON 指标和真实科研图像组织成可编辑 PowerPoint，并保留证据台账与逐页视觉检查流程。适用于组会、项目评审、答辩和会议汇报；附带演示使用合成示例数据。

- 先核对输入材料和定量结论，再规划科学叙事与每页信息
- 优先使用可编辑的 PowerPoint 原生图表、表格和示意图，保留原始科研图像含义
- 渲染并检查每一页，随包提供完整工作流、脚本和 demo
- 详见 [scientific-presentation-designer/README_zh.md](scientific-presentation-designer/README_zh.md) 与 [CODEX_START_SCIENTIFIC_PPT.md](scientific-presentation-designer/CODEX_START_SCIENTIFIC_PPT.md)

### review-presentation-designer（科学综述汇报 PPT）

面向文献综述、技术综述和学位论文背景汇报，围绕问题、方法分类、机制比较、证据冲突和研究空白组织可编辑幻灯片。

- 建立来源—论断台账，区分来源报告、作者提出、推论与未解决问题
- 跨论文比较时明确可比条件，图示中区分时间顺序与技术继承
- 随包 demo 带有合成演示标记，实际汇报前需替换并核验文献材料
- 详见 [review-presentation-designer/README_zh.md](review-presentation-designer/README_zh.md) 与 [CODEX_START_REVIEW_PPT.md](review-presentation-designer/CODEX_START_REVIEW_PPT.md)

### 安装与使用

将对应 skill 文件夹复制到 Claude Code 的 skills 目录即可：

```bash
# 全局安装（所有项目可用）
cp -r research-paper-interpreter ~/.claude/skills/
cp -r review-paper-interpreter  ~/.claude/skills/
cp -r research-idea-concretizer ~/.claude/skills/
cp -r research-idea-paper-potential ~/.claude/skills/
cp -r review-dialogue-architect   ~/.claude/skills/
cp -r evidence-first-review-writer ~/.claude/skills/

# 或仅当前项目安装
mkdir -p .claude/skills
cp -r research-paper-interpreter .claude/skills/
cp -r review-paper-interpreter  .claude/skills/
cp -r research-idea-concretizer .claude/skills/
cp -r research-idea-paper-potential .claude/skills/
cp -r review-dialogue-architect   .claude/skills/
cp -r evidence-first-review-writer .claude/skills/
```

### Codex / DSH 中的 Skills 安装

药物手稿与综述 skill 均按 Codex 的 skill 目录格式提供。安装时保留完整目录，特别是 `references/`、`assets/`、`scripts/` 与 `tests/`：

```bash
# 当前项目
mkdir -p .agents/skills
cp -r drug-property-manuscript-from-scratch .agents/skills/
cp -r drug-property-manuscript-rebuild .agents/skills/
cp -r aidd-review-manuscript-rebuild .agents/skills/
cp -r scientific-presentation-designer .agents/skills/
cp -r review-presentation-designer .agents/skills/
cp -r review-dialogue-architect .agents/skills/
cp -r evidence-first-review-writer .agents/skills/

# 或安装到用户级目录
mkdir -p ~/.agents/skills
cp -r drug-property-manuscript-from-scratch ~/.agents/skills/
cp -r drug-property-manuscript-rebuild ~/.agents/skills/
cp -r aidd-review-manuscript-rebuild ~/.agents/skills/
cp -r scientific-presentation-designer ~/.agents/skills/
cp -r review-presentation-designer ~/.agents/skills/
cp -r review-dialogue-architect ~/.agents/skills/
cp -r evidence-first-review-writer ~/.agents/skills/
```

在 Codex 中可显式调用 `$drug-property-manuscript-from-scratch`、`$drug-property-manuscript-rebuild`、`$aidd-review-manuscript-rebuild`、`$scientific-presentation-designer` 或 `$review-presentation-designer`；各自的 README 说明了适用场景和输入方式。

上述两个综述 skill 也都可直接放进 DSH 的用户级技能目录 `~/.dsh/skills/`（或项目级 `.dsh/skills/`），放入后即出现在会话的技能列表中，无需重启。

安装后在 Claude Code 中可直接描述任务，也可以显式指定 skill。例如可以先说"使用 research-idea-concretizer 把这个模糊 seed 扩展为多个正交候选 idea"，再说"使用 research-idea-paper-potential 评估这些候选的论文潜力"。论文解读也可以指定聚焦方向，例如：

- `重点分析模型架构和数据流`
- `重点分析代码实现和可复现性`
- `重点分析 GPCR 功能构象建模`
- `结合最新文献重新评估这篇综述的 future directions`

---

## 文献智能管理系统（桌面应用）

基于 Python + SQLite + PyMuPDF 的本地文献管理工具，内置 DeepSeek 等 OpenAI 兼容大模型接口，实现文献的自动解析与智能分析。

### 版本说明

| 文件 | 说明 |
|---|---|
| `main.py` | **v1 初版**：纯 Tkinter 界面，AIDD 方向分类体系（药物筛选、分子生成、蛋白/分子语言模型等），SQLite 存储，DeepSeek API 分析 |
| `main_v4.py` | **v4 完整版（推荐）**：CustomTkinter 现代化界面，面向结构生物学 × CADD × 细胞生物学交叉领域，功能最全 |
| `main_v4_clean.py` | **v4 精简版**：纯 Tkinter 实现，依赖更少，作为 PyInstaller 打包入口 |

### 主要功能

- **文献入库**：批量导入 PDF，自动提取标题、摘要、关键词、DOI、作者、年份；DOI 自动 CrossRef 元数据查询；智能去重
- **分类与标签**：自定义分类体系 + 标签系统，中文拼音排序
- **AI 单篇分析**：调用大模型对入库文献进行方法、创新点等结构化提取
- **AI 课题建议**：勾选多篇文献，自动分析领域分歧并生成跨领域研究课题建议（可导出 Markdown 报告）
- **统计分析**：按分类、年份、期刊等维度的文献库统计
- **模型管理**：内置模型配置管理界面，支持自定义 OpenAI 兼容 API 端点（base_url + api_key）

### 运行

```bash
pip install -r requirements.txt
python main_v4.py
```

大模型功能需要配置 API Key（默认使用 DeepSeek，二选一）：

```bash
export DEEPSEEK_API_KEY="你的key"   # 或在应用内"模型管理"界面配置
```

首次运行会在程序目录创建 `literature.db`（SQLite 数据库）和 `pdfs/`（PDF 存储目录）。

### macOS 打包

`.github/workflows/build-macos.yml` 提供手动触发（workflow_dispatch）的 PyInstaller 打包，产物为兼容 macOS 10.14+ 的 Intel `.app`（通过 Rosetta 构建），在 Actions 页面手动运行后即可从 Artifacts 下载 `literature-macos.zip`。
