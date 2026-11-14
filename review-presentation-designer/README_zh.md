# Review Presentation Designer v1.0

面向 Codex 的**科学综述 PPT 设计与审查 Skill**。与实验型 Scientific Presentation Designer 并列安装，互不覆盖。

## 定位

- 适用：Narrative-Critical Review / Technical Survey / Scoping Review / 有真实研究协议的 Systematic Review，适用于组会文献综述、学位论文背景、领域方法综述和会议报告。
- 输入：手稿（md/docx/pdf）、真实引用库（bib/ris）、evidence.csv、claims.csv、分类框架、图表及先前已提取的文献笔记。
- 输出：带来源映射的、可编辑的 PowerPoint 幻灯片；来源—论断台账；视觉预览及审计报告。
- 重点：科学叙事、方法分类/机制比较、并列评价轴、技术演化、多论文比较的条件可比性、矛盾证据、研究空白。**不擅自编造文献条目、发表年份、实验结果、技术继承或 PRISMA 统计。**

## 安装

解压安装包，把 `review-presentation-designer` 文件夹复制到项目根目录的 `.agents/skills/` 下；全局可复制到 `~/.agents/skills/`。确保文件为 `.agents/skills/review-presentation-designer/SKILL.md`。

准备 Python 环境（推荐独立虚拟环境），然后：

```bash
python -m pip install -r .agents/skills/review-presentation-designer/requirements.txt
```

Render 需要 LibreOffice（Linux/macOS）或带 Microsoft PowerPoint + pywin32 的 Windows。没有软件时必须注明未执行渲染。

## Codex 使用

```text
$review-presentation-designer

读取 manuscript_final.md、references.bib、evidence.csv、claims.csv 及 figures/。
做一份 15 分钟中文 Narrative-Critical Review 学术汇报。
以核心论点与方法比较组织讲述，不要按稿件章节逐页搬运。
明确区分 source-reported / author-proposed / inference / unresolved。
绘制可编辑分类、机制、可比性、证据链与技术演化图。
提供真实引文溯源和每页讲稿，渲染检查并修复。
缺失原文证据不能自行补造。
```

详见 `CODEX_START_REVIEW_PPT.md` 和 `references/prompts.md`。

## 直接测试配套生成器

```bash
python scripts/build_review_deck.py --plan examples/demo_review_plan.json --out demo_review_talk.pptx
python scripts/render_review_deck.py demo_review_talk.pptx --outdir examples/preview
python scripts/audit_review_deck.py demo_review_talk.pptx --plan examples/demo_review_plan.json --out examples/demo_qa.json
```

演示稿仅展示版式、信息组织与矢量绘图能力：每页都带 DEMO 声明，没有经过原始文献核验。务必替换演示素材及所有占位符，再用于实际学术汇报。

## 结构

- `SKILL.md`: 必遵守的证据优先工作流。
- `references/`: 综述类型、证据契约、专业视觉、图示语义、计划输入格式、验收与 prompts。
- `scripts/`: plan 证据检查、PPTX 编译、逐页渲染和静态 QA。
- `examples/`: 已可执行的 DEMO JSON、样稿、预览、验证报告。
- `agents/openai.yaml`: Skill UI 元数据。

## 能力边界

生成器是通用的可编辑科研综述视觉骨架；高度复杂的化学结构、多层 DAG、机制公式，仍需 Codex 按科学原义定制布局。静态检查不能保证稿件科学正确，也不能代替人工逐页审阅，或认定来源已经独立复现。
