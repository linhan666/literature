# Codex launch prompt — FULL review reconstruction

Copy this prompt into Codex **after installing** this skill, and replace the bracketed paths. This is a prompt template, not an executed manuscript edit.

```text
$aidd-review-manuscript-rebuild

任务：重构我的既有 AIDD 英文综述，模式 FULL。目标是批判性综合、证据与引用可靠性、
分类体系的操作性、段落论证质量，以及实际图表和文章输出，不是普通润色。

输入：
- 英文综述：[manuscript file path]
- 文献 BibTeX：[references.bib path or NONE]
- 原始论文/引用核验材料：[source PDF folder or links or NONE]
- 证据与结论表：[evidence.csv / claims.csv path or NONE]
- 已确认的讨论总结/边界：[discussion_summary.md / topic.md or NONE]
- 现有可编辑图表：[figures/tables folder or NONE]
- 认可的真实综述范文：[reference review papers or NONE]

体裁：[Narrative-Critical Review / Technical Survey / Scoping Review /
       Systematic Review / auto-diagnose from actual material]
投稿期刊：[name or unspecified]
需要的最终格式：[.md, .docx, .tex, PDF if available]

约束：
1. 首先阅读实际初稿和已有核验资产，保护作者已经确认的分类和事实。
2. 核对核心原始文献所报告的机制、结果、版本和引用身份；缺证据就标记，不猜。
3. 对不同研究开展条件可比性判定，禁止基于不匹配指标制作无依据排名。
4. 区分 SOURCE_REPORTED、REVIEW_SYNTHESIS、AUTHOR_PROPOSED、HYPOTHESIS、UNVERIFIED。
5. 重组全文论证，删除重复描述，增加必要的真正批判性比较和限制条件。
6. 先做真实内部样章校准，再继续完成全文；不在样章后无故停下等批准。
7. 按需制作科学准确、可编辑并尽可能实际渲染检查的综述概念图和比较表。
8. 引用改写后逐项核对；不虚构 PRISMA 检索、文献、代码审计、实验或统计结果。
9. 在独立 review_rebuild/ 输出实际完成的英文终稿、引用、图表与必要报告，
   保留输入原始文件。报告 NOT_RUN 与证据缺口，不保证投稿录用。
10. 正文和图表英文，给我的修改说明中文。
```
