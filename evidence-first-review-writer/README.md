# Evidence-First Review Writer · v1.0.0

**用途**：可复用的英文科研综述 Skill，支持 critical narrative review、systematic review 和 scoping review；特别强化 AI 药物发现、DTI/DTA、GPCR、虚拟筛选和分子生成方法学综述的范式分类、基准公平性和证据追踪。

**状态**：已交付可安装的 Skill 目录和本地工具；**本地 8 个测试通过**，涉及工作空间初始化、去重、数据审计、PRISMA 计数，以及 Europe PMC 与 Crossref 的模拟响应。**未对真实数据库进行在线端到端验收**，也没有在用户实际研究主题上执行文献检索或写出综述。不要把模板视为已完成的科研工作。

## 结构

```text
evidence-first-review-writer/
├── SKILL.md                          # Agent 首先读取的工作流
├── README.md
├── LICENSE
├── references/
│   ├── workflow.md                    # 三类综述、阶段门控
│   ├── search_strategy.md             # 数据库策略和检索日志
│   ├── evidence_schema.md             # 文献、研究、证据、观点的关系
│   ├── biomed_ai_taxonomy.md          # DTI/DTA/GPCR 等专用维度
│   ├── writing_guide.md              # 英文综述文章结构与批判性写作
│   └── reporting_ethics.md           # PRISMA、SANRA、ICMJE 等
├── scripts/
│   ├── reviewkit.py                   # 初始化、去重、结构审计、PRISMA 计数
│   ├── search_epmc.py                 # Europe PMC 真实检索 + 日志（需联网）
│   └── verify_dois.py                 # Crossref 元数据对照（需联网）
├── assets/
│   ├── review_brief.md                # 综述研究问题与贡献模板
│   ├── manuscript.md                  # 英文稿件骨架（不是综述成稿）
│   └── example_research_request.md    # 主题示例
├── tests/test_reviewkit.py           # 合成数据单元测试（无网）
└── evals/evals.json                  # Agent 级行为测试场景（尚未运行）
```

## 安装

解压后确保文件夹名与 SKILL.md 的 `name` 均为 `evidence-first-review-writer`。

**Codex**：将整个文件夹放到当前项目的 `.agents/skills/evidence-first-review-writer/`，或者用户级 `~/.agents/skills/evidence-first-review-writer/`。

**Claude Code**：将整个文件夹放到 `.claude/skills/evidence-first-review-writer/` 或 `~/.claude/skills/evidence-first-review-writer/`。

从新的 Agent 会话使用：

> Use the evidence-first-review-writer skill. Help me prepare a critical English review on explicit drug–protein interaction learning for DTI/DTA. Develop a claim-driven taxonomy, use accessible scholarly sources with logged searches, and build an evidence matrix before writing. Do not invent citations or compare incompatible benchmarks as though directly comparable.

这些目录适用于支持 [Agent Skills](https://agentskills.io) 的主流本地 Agent；实际发现/激活机制取决于宿主软件版本。把目录复制到磁盘 **不等于** 已经为 ChatGPT 对话自动安装这个 Skill。

## 本地 CLI 快速开始

从 Skill 目录运行；Windows 可用 `py` 代替 `python`。

```bash
# 1. 生成一个空的综述工作空间
python scripts/reviewkit.py init --out ./my-review --topic "Interaction learning in DTI/DTA" --type narrative-critical

# 2. 可选：联网检索 Europe PMC，自动记录准确查询式/查询日期/返回条目数
python scripts/search_epmc.py --project ./my-review --query '("drug target interaction" OR "protein ligand") AND (cross-attention OR contact)' --max-results 100

# 3. 浏览 records.csv 和检索结果后去重；手工审核 duplicate_map.csv、冲突文件
python scripts/reviewkit.py dedupe --input ./my-review/records.csv --out ./my-review

# 4. 由作者/Agent 实际筛选、阅读、提取，维护 screening.csv/evidence.csv/claims.csv
#    可选：联网检查 Crossref 元数据；不自动改变 verified 标识
python scripts/verify_dois.py --records ./my-review/records.csv --out ./my-review/doi_report.csv

# 5. 在写作和更新时进行结构审计
python scripts/reviewkit.py audit --project ./my-review --manuscript ./my-review/manuscript.md

# 6. Systematic/scoping 使用：审核了纳排结果、研究 ID 后才计算流图计数
python scripts/reviewkit.py prisma --project ./my-review

# 7. 本地回归测试（不联网）
python -m unittest discover -s tests -v
```

`audit` 发现结构性错误时退出码为 2；`prisma` 在筛选尚未完成或计数不一致时也退出码为 2。CLI **不会**自动验证自然语言科学论断。来源和论断的人工确认是投稿前的必要步骤。

## 设计的 5 个差异化能力

1. **三层验证**：是否存在有效文献身份、是否支持具体论断、证据的可靠程度分别记录。
2. **四级数据结构**：记录（record/report）→ 研究（study）→ 证据（evidence）→ 论断（claim），防止重复计数和引用挂靠。
3. **三种综述分流**：仅对真实做了相应流程的 systematic/scoping review 声称适用报告规范。
4. **AI 药物发现专用 taxonomy**：交互算子、物理监督、靶点泛化、受体状态、筛选效率、合成路径约束等。
5. **确定性审计工具**：自动检测 ID/引文键错误、去重冲突、文献无全文却声称全文证据、PRISMA 计数矛盾。

## 限制与后续扩展

- 当前仅内置 Europe PMC 的 **检索适配器**，并非 PubMed、Web of Science、Scopus、IEEE、arXiv 等全平台自动聚合器。其他来源由当前 Agent 具备的检索工具或合法接入的 MCP 提供；将记录按 CSV 模式保存。
- 尚未内置全文 PDF 解析、PDF 版权判断、真实的两名独立人工审稿人、Zotero 同步、BibTeX 自动生成、DOCX/LaTeX 编译和期刊模板校验。这些应以可授权的外部工具或独立能力实现，而不是让 Skill 假装完成。
- Crossref 匹配只是候选元数据比对，不等于验证文献内容。人工核实后才能填写 `metadata_status=verified`。
- 任何英文综述稿件都须依据实际引用、可得全文、真实的筛选/提取记录和期刊要求继续完成，并由作者承担最终责任。
- 存在超过单个平台索引的文献时必须显式告知检索覆盖缺口。

## 许可

本 Skill 的新写代码和新写指导文档采用随包 MIT License。引用的第三方规范和学术论文的权利仍归其原权利人；本项目未复制或包含第三方 Skill 代码。
