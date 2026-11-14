# AIDD Review Manuscript Rebuild — v1.0.0

**面向 AI for Drug Discovery（AIDD）英文综述的“既有手稿重构”Skill**。可与上传的研究型论文 Skill `drug-property-manuscript-rebuild v2.0.0` 并行安装，名称不同，不会直接覆盖。它不是简单的文章润色器，也不是把研究论文 Results 换成 Literature Review 标题的改造版。

## 1. 为什么单独开发

现有研究型论文重构的关键证据是研究者自己已经完成的实验：模型、数据、运行配置、结果和图表。综述的核心证据则是**被引用的原始工作**及其可比较性；核心写作任务是提出清晰的分析问题、定义分类体系、辨别证据层级、揭示真正的研究争议，再形成有边界的综合判断。

新 Skill 沿用“读取真实初稿 → 真实范文拆解 → 具体迁移卡 → 校准小样 → 实际全文重构 → 对照验收”的合理流程，但改造为以下综述专属模块：

| 能力 | 具体作用 |
|---|---|
| 体裁识别 | 不把 Narrative-Critical Review 假称系统综述；可处理 Technical Survey、Scoping、Systematic、Perspective |
| 文献与论断证据追踪 | 区分源论文报告、综述综合、作者提出的分类/框架和未经验证的假设 |
| 分类体系重建 | 定义操作性类别、边界条件、重叠与正反例，检验类别是否真的支持原文论证 |
| 可比性判断 | 检查任务、标签、数据版本、划分、预训练、评价单位、指标、实验验证等 |
| 真正的批判性综合 | 从逐篇介绍转换成机制差异、冲突证据、条件适用性和可检验研究空白 |
| 综述概念图和表格 | 方法分类图、机制图、证据框架、演化时间线、比较矩阵、决策图 |
| 完整论文重构 | 实际生成修改后的英文稿件、引用、图表及缺口报告，而非只给大纲 |

尤其适用于 **DTI/DTA、分子属性预测、GPCR 计算研究、结构预测与共折叠、药物分子生成、主动学习、分子表征模型、AI 筛选、肽类药物计算**等方向。领域边界是工作流程的审核项，而不是限定只能研究这些主题。

## 2. 安装 Codex

解压 ZIP，保持其顶层目录结构，并将完整文件夹复制到项目：

```text
<your-project>/.agents/skills/aidd-review-manuscript-rebuild/
    SKILL.md
    references/
    assets/
    examples/
    scripts/
    tests/
    README.zh-CN.md
    ...
```

也可放在用户级的 `~/.agents/skills/aidd-review-manuscript-rebuild/`，以便多个项目共享。Codex 可在项目内使用 `$aidd-review-manuscript-rebuild` 显式调用。`SKILL.md` 和 `references/` 必须一起保留；只是复制单个 SKILL.md 会丢失关键分阶段指导。若 Skill 没有出现，请检查位置并重启 Codex。关于当前技能格式与目录的官方依据见 `SOURCES.md`。

这是一个**独立的本地 Skill ZIP**，不是已经通过某个插件目录上架的插件；没有对你的本机 Codex 执行安装，也不会自动联网或向第三方上传未公开论文。

## 3. 可直接复制的完整重构启动 Prompt

```text
$aidd-review-manuscript-rebuild

请使用本 Skill 对我已完成的 AIDD 英文综述论文进行真正的全文重构，
不是普通语法润色，也不是从零编写另一篇综述。

论文类型：Narrative-Critical Review / Technical Survey
（如手稿事实与此不符，请指出并采用能被现有材料支持的体裁，不要编造检索或筛选过程）。
目标期刊：未定；采用通用英文科学综述规范，不擅自填入版式限制。

输入材料位于：
- 初稿：[路径，.docx/.md/.tex/.pdf]
- references.bib：[路径；如有]
- evidence.csv / claims.csv / discussion_summary.md / topic.md：[路径；如有]
- 关键原始文献 PDF 或可访问链接：[路径；如有]
- 现有图、表、框架定义及其他作者决策：[路径；如有]
- 已认可的综述范文：[路径；如无则在可用工具下检索匹配的综述]

要求：
1. 完整读取初稿，理解原文主题、研究边界、已确认分类体系与核心观点。
2. 识别结构、证据、方法分类、批判性分析、图表和引用方面的具体问题。
3. 核对重要文献与核心论断：文章身份、版本、Methods、图表、结论是否确实支持正文。
4. 不把相关性、跨论文性能分数或技术时间顺序误写为因果优势或技术继承。
5. 用真实优秀综述进行结构/表达/图表迁移；不得复制原文和已发表图像。
6. 重建 Introduction、主体章节、比较分析、争议和 Outlook，使其具有真正批判性。
7. 设计并实际制作必要的概念图和比较矩阵，区分原文报告与作者提出的框架。
8. 保留已获支持的科学内容和重要反面证据；未经核验的事实须降级措辞或列入缺口。
9. 先做内部校准小样，再完成全文；除非我明确要求，不要在小样后等待确认。
10. 保留全部原始文件，在独立输出目录交付真正修改后的完整英文稿件、
    引用文件、图表源文件/导出图、quality_report.md 和 unresolved_issues.md。
11. 实际执行哪些检查就如实报告哪些；不得虚构审稿通过、实验验证或 PRISMA 合规。

英文用于正文与图表；中文用于修改说明和质量报告。
本轮模式：FULL。
```

建议在输入文件有 `evidence.csv/claims.csv` 时**复用而非重新创建并丢弃**现有证据体系。若你此前使用 `Review Dialogue Architect` 和 `evidence-first-review-writer`，可以把它们的 `discussion_summary.md`、`topic.md`、`manuscript_final.md`、`references.bib` 及核验报告作为上游资产。**新 Skill 专门负责已有综述的后期重构与实际质量提升，不强迫从 Phase 0 重来。**

## 4. 先做小样：用于测试是否符合你的期望

```text
$aidd-review-manuscript-rebuild

我的 AIDD 英文综述初稿及来源材料位于：[路径]。
本轮使用 PILOT 模式，不重写全文。

请先读取全文定位核心科学问题和叙事缺陷，检查关键文献，
选取与我文章体裁匹配的真实综述范文。

交付：
A. 实际重写的 Introduction 片段；
B. 一段从逐篇文献罗列改造成批判性综合的主体正文；
C. 一张实际可编辑的分类/评价图或一张比较矩阵（按真实材料决定）；
D. 原稿→新稿→范文（同功能）的具体对照；
E. 原始来源核查范围、未验证证据清单。
不要只输出修改建议。不得制造数据、伪造引文或虚构已有共识。
```

## 5. 针对你常见综述主题的定制调用示例

**示例 A：TabPFN 在药物发现中的应用与扩展。**

```text
$aidd-review-manuscript-rebuild

以我提供的 TabPFN 药物发现英文综述终稿、references.bib、
evidence/claims 表和已有图表为基础执行 FULL。
作者已确认的分类原则和研究边界位于：[discussion_summary.md 路径]。
审查方法操作类别、TabPFN 的系统角色、应用证据与版本/继承关系。
多种 ChemPFN 若身份不同必须独立核验；不能凭共同名称画技术继承箭头。
保留作者框架未独立验证的限制；重点重建批判性综合和图表。
```

**示例 B：DTI 显式药物–蛋白 Attention 交互范式。**

```text
$aidd-review-manuscript-rebuild

对该技术综述进行 FULL 重构，输入资料：[路径]。
保留已确认的功能角色分类原则；如原文讨论 R1/R2/R3，
核查论文公式/代码是否支持各类别，允许多标签与边界案例。
必须区分预测、配对依赖、特征归因、结构/生物物理证据，
并审查不同模型在数据、划分、监督和预训练方面是否可比。
所画分类图和评价框架均不得暗示其已被独立验证。
```

以上两个示例中的分类选择仅在相应项目**确有确认文件**时适用，不是写入 Skill 的通用预设。

## 6. 不同模式与工作边界

| 模式 | 提交成果 | 适用情况 |
|---|---|---|
| `DIAGNOSE` | 具体问题定位与重构路线 | 暂时不希望改稿 |
| `PILOT` | 实际改写段落+相关图表小样+对照 | 首次试风格 |
| `FULL` | 完整英文新稿、来源修订、图表与报告 | 已有完整手稿 |
| `TARGETED` | 指定章节/分类体系/引用/图表重构 | 聚焦明显短板 |

与研究型 Skill 的关系：**各自独立**。不必先执行原 Skill；原 Skill 的研究型 Methods/Results 重构不能自动替代综述证据综合。综述若包含作者自行完成的实验，也应分别审核实验事实与文献综述部分。

## 7. 可选自动检查（仅静态）

```bash
python scripts/review_lint.py \
  --manuscript review_rebuild/manuscript.md \
  --bib review_rebuild/references.bib \
  --report review_rebuild/lint_report.json
```

可发现部分缺失 BibTeX 键、重复键、缺失的本地图片与 TODO 标记。**不能**验证文献是否真实、DOI 是否正确、原文是否支持论断，也不能编译 DOCX/PDF 或证明综述质量。脚本只接受 `.md` 和 `.tex`。可执行的本地单元测试：

```bash
python -m unittest discover -s tests -v
```

## 8. 包文件说明

- `SKILL.md` — 主流程与阶段路由。
- `references/` — 九个专业模块：体裁、证据核验、AIDD 科学边界、分类与综合、范文迁移、正文、图表、质量验收、引用与成稿。
- `assets/` — 项目约定、章节映射、论断与方法矩阵、图表 Brief 空模板。
- `examples/` — 明确标注为虚构教学用途的“文献罗列→批判性综合”示例。
- `scripts/review_lint.py` — 零外部 Python 包依赖的静态检查辅助脚本。
- `tests/` — 对脚本行为的单元测试，不是对写作 Skill 效果的实证验证。
- `EVAL_CASES.md` — 未来用于真实项目的行为验收场景（未执行）。
- `VALIDATION.md` — 实际完成的安装包与脚本核验、未执行事项。
- `SOURCES.md` — 格式规范和综述报告框架的可核验来源。

## 9. 重要限制

Skill 是指令、模板与脚本的组合，不会微调模型权重，不会自动安装额外软件，也不授予不存在的浏览、审稿、文献订阅或图像生成权限。实际 PDF/DOCX 导出、编辑图表与原文检索取决于 Codex 运行环境及所获授权。优秀范文只是编辑校准依据，不会替你完成文献系统检索或真实科学验证。
