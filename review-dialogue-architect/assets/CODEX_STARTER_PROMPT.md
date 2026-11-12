# Codex 启动 Prompt — Review Dialogue Architect v1.1

```text
请使用 $review-dialogue-architect（v1.1）并进入 INTERACTIVE 模式。

读取 input/topic.md 以及实际存在的 prior discussion/session_state 记录。
目标：就我的英文科研综述主题、初步研究目标，开展深入、批判性的真实多轮讨论，形成可交给 evidence-first-review-writer 的结构化研究架构。

默认 10–12 轮实质性用户–助手交流（软预算，不是强制轮数）。
实行 P1 研究定位 → P2 竞争分类框架 → P3 反向质疑 → P4 收敛 → P5 用户批准导出五阶段；每阶段要完成科学层面的质量门控，不能只凭是否提到关键词判断完成。
每轮：先做有实质内容的分析，再问最多一个影响后续构思的关键决策问题，不重复已经回答的问题。

使用 notes/session_state.md 保存真实决策与争议；可选使用 scripts/dialogue_tracker.py 记录实际轮次、15 项覆盖状态、饱和度启发式、关键未解决争议和有理由的延长。

当最近三轮缺少实质性新观点，不要自动生成总结；如果尚有空缺，换批判视角。达到目标预算后尚存重大争议，可以建议 +3 轮；不得强制结束。

只有我明确要求 EXPORT 时才按 assets/discussion_summary.template.md 填写 drafts/discussion_summary.md，并在检查后导出到 input/discussion_summary.md；保留 review-dialogue-handoff/v1、14 个固定二级章节与已确认/未确认的严格区分。若讨论仍未充分，标记 provisional。

不要自动开始论文正文写作，不要伪造数据库检索、引用、用户确认、科研数据或学术创新性结论。

现在只开始第一轮，优先发现本研究最关键的学术定义或范围歧义，提供实质分析并提出一个决策问题。
```
