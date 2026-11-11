# Codex 启动 Prompt

```text
请使用 $review-dialogue-architect 开启一个科研英文综述的多轮研究讨论。

输入：input/topic.md（里面包括暂定英文标题和初步研究目标；可选此前讨论记录）。

目标：与我共同深化综述的科学问题、范围、分类体系、争议、对比框架和潜在贡献。
请批判性评估我的初步观点；尤其要区分问题定义、模型输入、交互机制、学习监督、预测输出、验证方式等概念层级。

不要立即写英文正文，不要假装已经检索或阅读过尚未访问的论文。
每轮提供实质性分析，提出最多一个最关键的待决问题，并记录真实用户确认和未经确认的建议。
使用 notes/session_state.md 维护会话决策；正式导出前，在 drafts/discussion_summary.md 完整填写模板，运行 scripts/handoff.py validate；经过真实讨论和必要审核后 export 到 input/discussion_summary.md。

先进行第一轮科学问题与框架分析，不要单轮自动模拟完整对话。
```

如果 Codex 未识别 Skill：确认 `SKILL.md` 位于 `.agents/skills/review-dialogue-architect/SKILL.md`，查看 `/skills`，必要时重启 Codex。
