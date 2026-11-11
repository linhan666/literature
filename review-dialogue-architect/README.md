# Review Dialogue Architect (v1.0.0)

**中文说明 | English-ready handoff**

一个专门用于英文科研综述**选题孵化、深度学术讨论、批判性框架构建与结构化交接**的 Agent Skill。输入可以很简短：一条拟定英文标题 + 一段初步目标描述。它通过真实的多轮用户对话建立思考框架，然后把确认过的决定、争论、未核实论断和文献检索任务整理成 `input/discussion_summary.md`，供下游 `evidence-first-review-writer` 使用。

与“整理聊天记录”“直接写综述正文”不同，这个 Skill 要主动提出并检验框架，同时严格区分**用户要求 / 用户确认 / AI 建议 / 未解决 / 文献证据状态**。

## 你能获得什么

- 精确的问题定义、范围/排除条件、预期受众以及综述模式建议。
- 多种分类/叙事架构与对其本体层级、重叠、边界案例的批判性检验。
- 核心科学问题、可能的综述差异化贡献、拟定论证结构、图表设计。
- 高风险论断、反例方向、证据检索计划；所有科学与新颖性断言明确标记待核实。
- **唯一必需的最终文件：`input/discussion_summary.md`**，另含英文 handoff brief 以便下游使用。

## 与 Evidence-First Review Writer 的关系

```text
研究者：英文综述主题/初步目标
      │
      ▼
review-dialogue-architect   ← 本 Skill，多轮讨论/框架构思/反向质疑
      │
      └── input/discussion_summary.md  [经讨论形成的研究方案；可标注 provisional]
      │
      ▼
evidence-first-review-writer  ← 后续 Skill，真实检索/核验/证据综合/撰稿
      │
      └── references, evidence matrix, English manuscript
```

`discussion_summary.md` 不是可直接引用的证据。下游应当先检查已有综述、确认论文存在并逐条验证关键论断；可基于检索结果修正上游框架。

## 使用方式 A：ChatGPT 普通网页对话（无需安装）

打开 [`assets/CHATGPT_STARTER_PROMPT.md`](assets/CHATGPT_STARTER_PROMPT.md)，将其内容粘贴到新的 ChatGPT 对话，附上你的**英文综述主题和初步研究目标**，开启逐轮讨论；讨论成熟时说“导出总结”。若界面允许上传文件，也可上传 `SKILL.md` 与模板，以便模型按完整规范执行。

**重要**：向普通对话上传一个 ZIP 并不等于在账户中安装了一个可自动调用的 Skill。正式的可复用 Skill 通过支持 Skill 的 ChatGPT/Codex 环境加载，或打包成可安装的插件。普通网页对话最稳妥的入口是独立的启动 Prompt。

## 使用方式 B：Codex / 支持本地 Skills 的 ChatGPT

将整个 `review-dialogue-architect/` 文件夹放进项目 `.agents/skills/`；把下游 `evidence-first-review-writer/` 并列放置：

```text
my-scientific-review/
├── .agents/skills/
│   ├── review-dialogue-architect/SKILL.md
│   └── evidence-first-review-writer/SKILL.md
├── input/topic.md
├── notes/session_state.md
├── drafts/discussion_summary.md
└── input/discussion_summary.md            # 导出后出现
```

Codex 中通过 `$review-dialogue-architect` 显式调用，或根据任务描述自动触发；如未识别可用 `/skills` 检查，必要时重新打开会话。对 ChatGPT 的具体安装/调用能力，取决于使用的产品入口及插件权限，不要将本地目录视为自动同步到网页聊天。

### 初始化及导出命令

在你的项目目录内运行（下面的 `SKILL_DIR` 指本 Skill 的实际路径）：

```bash
python SKILL_DIR/scripts/handoff.py init --project .
# 编辑 input/topic.md，并与 Skill 多轮深入讨论；把形成的文本填入 drafts/discussion_summary.md
python SKILL_DIR/scripts/handoff.py validate --file drafts/discussion_summary.md
python SKILL_DIR/scripts/handoff.py export --project .
# 导出到 input/discussion_summary.md
```

没有真实多轮讨论时，`stage: provisional`，默认导出会阻止假装完成；若你明确要先移交不成熟方案：

```bash
python SKILL_DIR/scripts/handoff.py export --project . --allow-provisional
```

如果目标文件已存在，请显式增加 `--overwrite`。命令不会偷偷替换已完成的下游输入文件。

### 下一阶段 Prompt

```text
请使用 $evidence-first-review-writer，阅读 input/topic.md 和
input/discussion_summary.md。首先核实综述定位、已有综述与候选贡献，
逐一检验未验证的科学论断和分类边界。建立真实检索日志、来源与证据矩阵。
不要把上游的 ASSISTANT_PROPOSED 或 BACKGROUND_UNVERIFIED 直接写成事实，
也不要假装已有系统综述流程已经完成。先输出第一阶段研究方案供审核。
```

## 文件说明

```text
review-dialogue-architect/
├── SKILL.md                         主指令（核心必读）
├── README.md                        本指南
├── LICENSE
├── agents/openai.yaml               可选显示元信息
├── references/
│   ├── discussion_protocol.md       多轮讨论策略与终止条件
│   ├── critical_reasoning.md        分类/创新/证据/论证的批判性评估
│   ├── biomedical_ai_lenses.md      药物发现/DTI/DTA/GPCR 专项问题
│   └── handoff_contract.md          下游输入的强约束
├── assets/
│   ├── topic.template.md            输入模板
│   ├── session_state.template.md    对话动态决策记录
│   ├── discussion_summary.template.md  交接文件规范
│   ├── sample_provisional_handoff.md   虚构场景的示例，非文献检索结果
│   ├── CHATGPT_STARTER_PROMPT.md    网页 ChatGPT 可直接粘贴的完整 Prompt
│   └── CODEX_STARTER_PROMPT.md      Codex 初始 Prompt
├── scripts/handoff.py               初始化/结构核查/导出，stdlib
├── tests/test_handoff.py            确定性回归测试
└── evals/evals.json                 行为评测情境，尚需实际 Agent 运行
```

## 重要限制

- `handoff.py` 只核查元数据、章节齐全和模板残留，**不**验证观点是否有学术价值、用户是否真的确认、引文是否准确；这必须依赖实际对话与原始论文核对。
- 例子中的科学性观点是待研究的问题，不是已验证的文献发现。不能用它们替代论文证据。
- Skill 不是文献检索引擎，也不能替代文献数据库、同行审稿、作者的学术判断和投稿要求。
- `dialogue-complete` 只说明讨论与作者决策达到可以交接的阶段，**绝不意味着文献/论断已经核验完成**。

## 建议的真实工作节奏

建议在多轮对话中依次经历范围澄清、分类方案竞争、批判反例、收敛到主线，必要时可往返迭代。没有固定轮数：真正重要的是概念澄清、关键争论是否形成可行动的决策记录，而不是聊天记录长度。

## 设计参考（不是本包的科学证据）

- Agent Skills 官方实践： https://learn.chatgpt.com/docs/build-skills
- OpenAI skill authoring guidance: https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md
- Review methods taxonomy: Grant & Booth (2009), https://doi.org/10.1111/j.1471-1842.2009.00848.x
- SANRA quality assessment of narrative reviews: https://doi.org/10.1186/s41073-019-0064-8

MIT License applies to original code and documents in this package. External resources remain under their own licensing terms.
