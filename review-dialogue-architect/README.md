# Review Dialogue Architect v1.1.0

**科研英文综述的上游研究对话 Skill｜10–12 轮弹性预算｜阶段质量门控｜研究者决定导出**

这个 Skill 将「拟定综述标题 + 初步研究目标」转化为实际科研讨论，通过反例、竞争框架、批判比较和用户决策记录逐步收敛研究思路。最终交付 `input/discussion_summary.md`，由下游 `evidence-first-review-writer` 负责真实文献检索、证据核验与英文写作。

## v1.1 相比 v1.0 新增什么

| 机制 | v1.1 行为 | 重要边界 |
| --- | --- | --- |
| 讨论预算 | 默认目标 10–12 次真实的用户–助手深入交流，简单主题可提前结束 | 不是强制最少轮数，也不是硬性上限 |
| 阶段质量门控 | P1 研究定位、P2 竞争框架、P3 反向质疑、P4 收敛各有可审查维度 | 脚本仅依赖人工/助手填写的状态，不能证明科学质量 |
| 覆盖追踪 | 15 个维度按 `absent` / `proposed` / `examined` 更新 | `examined` 表示实质讨论过，不等于用户同意或文献证实 |
| 讨论饱和度提示 | 最近 3 轮记录为 `none` 时提醒换思路或审查是否收敛 | 只是记录驱动的启发式检测，不是语义判断模型 |
| 自适应扩展 | 到达目标预算仍有重大争议，可提出 +3 轮等带理由的延长 | 不自动替用户做决定或强行结束 |
| 最终审查门 | 梳理已确认内容、未决项、证据缺口，并请研究者选择是否导出 | **没有明确导出要求时绝不自动生成最终总结** |

除新增可选追踪器外，保持 v1.0 **14 章节 `discussion_summary.md` 格式和 `review-dialogue-handoff/v1` schema** 不变，兼容原有下游 `evidence-first-review-writer`。

## 推荐流程

```text
标题 + 目标
    ↓
P1 研究定位与边界
    ↓ (质量门控：是否实质审查过？)
P2 分类体系和竞争框架
    ↓
P3 批判、反例、证据及可比性
    ↓
P4 学术贡献假设、论证结构、验证清单
    ↓
最终审查：研究者决定继续 / 修订 / 导出
    ↓ (明确要求导出才执行)
input/discussion_summary.md
    ↓
evidence-first-review-writer
```

讨论阶段可以往返循环；10–12 轮只是默认预算。如果用户第 3 轮就要导出，应生成 `provisional` 交接；如果第 12 轮仍有重大争议，解释原因并建议延长。**不能为了完成轮数人为制造问题。**

## 方式 A：在 ChatGPT 网页中直接开始（不需要 Codex）

打开 `assets/CHATGPT_STARTER_PROMPT.md`，复制完整 Prompt 到新对话，再填写综述标题和初步目标。普通 ChatGPT 对话并不会因为你在电脑上解压 ZIP 而自动加载本地 Skill；使用完整 Prompt 或在支持的环境中安装 Skill 才能保证指令可用。

基本启动语句：

> 请按 Review Dialogue Architect v1.1 进入 INTERACTIVE 模式。我的综述标题是 ...，初步目标是 ...。默认采用 10–12 轮的弹性讨论预算，严格阶段门控，每轮做深入批判性分析，只问一个高价值决定性问题。不要提前生成 `discussion_summary.md`，由我决定何时导出。

## 方式 B：在 Codex 安装整个 Skill

将 ZIP 解压得到的 `review-dialogue-architect/` 文件夹放入项目：

```text
Scientific-Review-Project/
├── .agents/
│   └── skills/
│       ├── review-dialogue-architect/
│       │   ├── SKILL.md
│       │   ├── references/
│       │   ├── assets/
│       │   ├── scripts/
│       │   └── tests/
│       └── evidence-first-review-writer/   # 如已安装
├── input/topic.md
├── notes/session_state.md
├── notes/dialogue_state.json               # 可选日志文件
└── drafts/discussion_summary.md            # 实际讨论后填充
```

在 Codex 的项目对话中使用 `$review-dialogue-architect` 调用。若原来已安装 v1.0，建议先备份旧文件夹，然后覆盖安装 v1.1；已有的研究文件与日志请不要覆盖。

## 可选命令（Windows PowerShell）

以下在项目根目录运行；`py -3` 表示 Python 3.10+（若不可用改为 `python`）：

```powershell
py -3 .agents\skills\review-dialogue-architect\scripts\handoff.py init --project .
py -3 .agents\skills\review-dialogue-architect\scripts\dialogue_tracker.py init --project .
```

`input/topic.md` 填写题目和研究目标；之后直接在 Codex/ChatGPT 中进行多轮讨论。无需由用户逐轮手工执行追踪命令；它是有文件/终端能力的代理可选的记录工具。

```powershell
# 检查轮次、阶段门控和争议提醒
py -3 .agents\skills\review-dialogue-architect\scripts\dialogue_tracker.py status --project .

# 当你明确要求 EXPORT 后，填写草稿并执行结构校验
py -3 .agents\skills\review-dialogue-architect\scripts\handoff.py validate --file drafts\discussion_summary.md

# 实质对话已完成且你已要求导出
py -3 .agents\skills\review-dialogue-architect\scripts\handoff.py export --project .

# 若讨论不完整但你明确要求提前交接
py -3 .agents\skills\review-dialogue-architect\scripts\handoff.py export --project . --allow-provisional
```

目标文件已存在时，导出不会默认覆盖；可在审核后选择显式 `--overwrite`。脚本不能核查论文真实性或用户是否真的作过确认，这些只能通过原始对话和外部证据确认。

### 记录一轮实际讨论（可选）

```powershell
py -3 .agents\skills\review-dialogue-architect\scripts\dialogue_tracker.py record --project . --phase P1-positioning --novelty substantial --user-input "实际用户输入概述" --analysis "本轮实际新增的批判分析与取舍"
py -3 .agents\skills\review-dialogue-architect\scripts\dialogue_tracker.py coverage --project . --dimension scope --level examined --note "比较了收窄与扩展研究范围的后果"
py -3 .agents\skills\review-dialogue-architect\scripts\dialogue_tracker.py status --project .
```

如记录重大争议：

```powershell
py -3 .agents\skills\review-dialogue-architect\scripts\dialogue_tracker.py issue --project . --severity critical --description "分类体系混合输入、监督与交互算子层级"
```

如第 12 轮仍未解决：

```powershell
py -3 .agents\skills\review-dialogue-architect\scripts\dialogue_tracker.py extend --project . --rounds 3 --reason "需要继续核查竞争分类方案的边界及反例"
```

## 完整文件清单

```text
review-dialogue-architect/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE
├── agents/openai.yaml
├── references/
│   ├── discussion_protocol.md
│   ├── adaptive_dialogue_v1.1.md
│   ├── critical_reasoning.md
│   ├── biomedical_ai_lenses.md
│   └── handoff_contract.md
├── assets/
│   ├── CHATGPT_STARTER_PROMPT.md
│   ├── CODEX_STARTER_PROMPT.md
│   ├── topic.template.md
│   ├── session_state.template.md
│   ├── discussion_summary.template.md
│   └── sample_provisional_handoff.md
├── scripts/
│   ├── handoff.py
│   └── dialogue_tracker.py
├── tests/
│   ├── test_handoff.py
│   └── test_dialogue_tracker.py
└── evals/evals.json
```

## 测试与限制

在开发容器中使用 Python 标准库运行确定性测试，覆盖模板校验、导出防覆盖、轮次记录、覆盖门控、饱和度提示、争议阻断和扩展记录。**这些是程序测试，不代表已经运行了真实用户的 10–12 轮学术对话，也不代表文献核验完成。** `evals/evals.json` 是尚未执行的行为评测计划。

## 下游衔接

`input/discussion_summary.md` 必须忠实保留 `USER_GIVEN`、`USER_CONFIRMED`、`ASSISTANT_PROPOSED`、`OPEN`、`DISPUTED`，并用来源级别区分 `BACKGROUND_UNVERIFIED`、`SOURCE_LOCATED`、`SOURCE_CHECKED`。下游先确认研究定位与已有综述覆盖，再查论文、建证据矩阵、撰文。所有未经源验证的学术发现、新颖性判断、模型 SOTA 声称均应保留为待验证事项。

本 Skill 原创代码和说明采用 MIT License；各外部参考资源版权归其原作者。
