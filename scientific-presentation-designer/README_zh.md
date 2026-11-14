# Scientific Presentation Designer v1.0 — Codex 科研 PPT Skill

这是一个可直接放入 Codex 的本地 Skill：将实验报告、实验结果、指标 CSV/JSON、科研图像转换为**设计过的、可编辑的、证据可追溯的**科研演示 PPTX。不是通用的一键套模板工具。

## 1. 安装到 Codex

解压得到 `scientific-presentation-designer/` 文件夹。任选一种方式：

**项目级（最推荐）**：将完整文件夹放到项目根目录的 `.agents/skills/` 下，得到：

```text
my-research-project/
  .agents/
    skills/
      scientific-presentation-designer/
        SKILL.md
        scripts/
        references/
        examples/
        requirements.txt
```

**用户级**：Windows 通常放到 `C:\Users\<用户名>\.agents\skills\scientific-presentation-designer\`；macOS / Linux 放到 `~/.agents/skills/scientific-presentation-designer/`。

Windows PowerShell（在 ZIP 文件所在目录运行；此命令安装到个人级目录）：

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills" | Out-Null
Expand-Archive -Path .\scientific-presentation-designer-v1.0.zip -DestinationPath "$HOME\.agents\skills" -Force
py -m pip install python-pptx Pillow PyMuPDF
```

若 Codex 未自动发现，请重启 Codex。然后输入 `$scientific-presentation-designer` 显式调用。

## 2. 第一次在真实项目中运行

在 Codex 中打开已有实验项目，按你的目录修改：

```text
$scientific-presentation-designer
请读取 ./report.md、./results/、./figures/，制作一份 12 分钟中文组会汇报，目标是 10–12 页。
严格基于原始指标与真实图片，先建立 evidence_ledger.csv 和 slide_plan.json。
采用 lab-light 主题、16:9、清晰的可编辑图表和科研叙事。
每页渲染、逐页视觉审查并修改，输出 presentation/research_deck.pptx 和预览。
```

更完整的会议/组会/答辩提示词见 `references/codex_prompts.md`。

## 3. 一个可复现的离线示例

安装 Python 依赖后，在 Skill 根目录运行：

```bash
python scripts/build_deck.py --plan examples/example_plan.json --out demo.pptx
python scripts/render_deck.py demo.pptx --outdir demo_preview
python scripts/audit_deck.py demo.pptx --out demo_qa.json
```

此 Demo 的所有实验数值均为**合成示例数据**，绝非真实研究结果。演示如何组织科研叙事、可编辑的图表/文字，以及版式风格。`render_deck.py` 需要 LibreOffice 可执行程序；PowerPoint 也可手动导出 PDF 再视觉检查。

## 4. 设计原则与边界

Skill 对视觉质量的要求：不是“生成了 PPTX 就算完成”，而是**证据审计 → 故事板 → 信息设计 → 原生 PPT 图形 → 全页渲染 → 视觉返修**。它无法凭空知道没有上传的实验结果，也不能代替作者审核科研结论。自动结构检查不能等价于人工或模型对渲染图的视觉检查。

生成器支持 cover、section、cards、kpis、pipeline、bar_chart、line_chart、metric_table、comparison、image_panel、findings、roadmap、closing 等版型。其他复杂科研图（例如蛋白-配体 3D 构象、化学结构、复杂混合图）优先使用实验中真实导出的高质量图像，不使用模型凭想象重绘。Codex 可以针对实际内容扩展 `scripts/build_deck.py`，不应被固定模板限制。

## 5. 文件组成

- `SKILL.md`：Codex 主工作流程。
- `references/`：叙事、视觉系统、证据边界、质量检查、启动提示词。
- `scripts/build_deck.py`：从结构化 JSON 生成可编辑 PPTX 的示范引擎。
- `scripts/render_deck.py`：渲染全部页面、生成联系表。
- `scripts/audit_deck.py`：基本结构、几何和字体风险审计。
- `examples/example_plan.json`：完整合成示例。
- `demo_scientific_report.pptx`：随安装包提供的设计样稿（合成数据）。

Windows 上若安装了 Microsoft PowerPoint 但未安装 LibreOffice，自动渲染脚本也支持 PowerPoint COM 后备方案；可按需执行 `py -m pip install pywin32`。没有可用渲染器时，必须手动用 PowerPoint 导出并检查每一页，不能把静态检查当成视觉质量合格。

最方便的启动提示词独立存放于根目录 `CODEX_START_SCIENTIFIC_PPT.md`。
