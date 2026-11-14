# Codex 启动 Prompt — Review Presentation Designer v1.0

```text
$review-presentation-designer

项目任务：根据当前项目中的综述性论文及其证据资料，制作一份高质量、可编辑、可溯源的科研综述 PowerPoint 汇报。

默认参数：中文汇报、15–20分钟、约14页（必要时调整）、技术型学术听众、16:9、editorial-light。

【输入调查】
1. 自主查找并读取 manuscript_final.md/.docx/.pdf、references.bib、discussion_summary.md、topic.md、evidence.csv、claims.csv、methods_matrix、figures 等实际存在的文件。
2. 如果关键文件缺失，在 open_issues.md 记录，不得臆测存在。

【证据审查】
3. 按源论文/综述推断/作者提出/待核验/矛盾证据为论断编码，建立 sources.csv、claims.csv 和 figure_manifest.csv。
4. 任何 DOI、引用、年代、具体比较结论必须有原始证据；仅从稿件转述得到的内容标为尚待原文核验。
5. 不能假造文献筛选流程、论文数量、统计显著性、横向性能排序、技术继承箭头或验证过的机制。

【综述叙事】
6. 将论文凝练为：科学问题与综述立场 → 范围与术语 → 分类/技术机制 → 证据维度和比较条件 → 争议/局限 → 研究空白与选题矩阵 → 综合结论。
7. 不要按论文小节机械分成幻灯片；每页一个可辩护的主张，优先机制图、分类树、比较矩阵、多轨演化图和证据图谱。
8. 画出“作者提出但未独立验证”的框架时，在对应幻灯片清晰标明 AUTHOR-PROPOSED。

【设计实现】
9. 使用此 Skill 中的可编辑 PPTX 生成器，必要时扩展布局和专业矢量图。
10. 不要将整页手稿截图贴到 PPT。原始科学图片需要正确来源/引用/授权状态。
11. 生成 speaker_notes.md 和 PowerPoint 内讲者备注，保留完整来源线索、定义和限制。

【检验与交付】
12. 运行 validate_review_plan.py --strict；审查 unresolved 和 comparative claims。
13. 渲染每一张幻灯片，检查全幅 PNG，修复拥挤、溢出、过小字号、箭头含义、来源信息和不一致的分类颜色。
14. 交付 review_presentation.pptx、review_slide_plan.json、来源台账、speaker_notes.md、qa_report.json、preview/contact_sheet.png、open_issues.md。
15. 说明确切执行过哪些审查；禁止把结构检查说成人工审美审查或独立的科学验证。
```

说明：不需要额外附上旧的实验结果 PPT Skill；两个 Skill 可并存。若实际场景同时包含综述和实验结果，可先用本 Skill 形成文献逻辑，再单独以实验型 Skill 设计实验章节。
