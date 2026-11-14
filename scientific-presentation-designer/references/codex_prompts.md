# Copy-ready Codex prompts (Chinese)

## A. From experiment report to lab meeting

```text
$scientific-presentation-designer

请读取当前项目下的实验报告（Markdown/Word）、results/ 中的原始指标 CSV/JSON、figures/ 中的真实科研图，制作一份 12 分钟中文组会汇报 PPT，约 10–12 页。

必须先完成实验事实抽取和 evidence_ledger.csv，再给出 slide_plan.json，随后生成可编辑 PPTX。叙事重点是研究问题、实验设计与数据划分、模型方法、核心结果、消融/稳健性、失败案例、局限与下一步实验。尽量用 1 张核心图承载 1 页结论，不要将 Markdown 段落直接塞到 PPT。

视觉风格：高水平科研组会，16:9、简洁白底、藏蓝/青绿配色、强信息层级；重要比较必须重绘为规范的可编辑图表，真实科研结构图原样使用。

严禁编造缺失指标或显著性。生成后将每页渲染为 PNG，逐页检查并修复文字溢出、图表过密、标签过小等问题。输出 PPTX、预览、图文溯源和 QA 报告。
```

## B. Redesign an existing ugly deck

```text
$scientific-presentation-designer

请重新设计 ./slides/original.pptx，保留原始研究结论、数据、方程、结构图和引用，不允许改变科学含义。先从原 PPT 提取逐页核心信息与证据，再重排科学叙事与版式（不是只更换主题配色）。

目标风格为专业学术会议 PPT：版式有节奏，文字简洁，图表清晰，16:9，大字号，高对比。生成可编辑的 updated.pptx。每页渲染检查、修复，并写明内容是否调整以及仍需作者核对的事项。
```

## C. Conference version in English

```text
$scientific-presentation-designer

基于已完成的实验报告和真实结果，生成英文 8 分钟会议汇报 PPT。强调科学动机、创新点、最强且可验证的核心结果、严谨对照和 limitations；复杂技术细节放 appendix。请按英文科技演示标准控制文字密度和图形精度，并输出 .pptx、slide plan、speaker notes、证据审计与全页渲染预览。
```

## D. Thesis defense

```text
$scientific-presentation-designer

将 dissertation/ 下的章节成果整理为 20 分钟中文答辩 PPT。注意多项工作之间的研究问题关系、可复现性、消融与负面结果。每项工作至少有一页核心定量结果、一页方法示意和一页局限。首页、章节分隔、结果图、总结页要保持统一视觉系统。生成 PPTX 后进行逐页可视检查。
```
