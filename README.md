# literature — 文献管理工具集

面向科研场景的一站式文献工具集，包含两部分：

1. **文献智能管理系统**（桌面应用）—— PDF 文献入库、元数据自动解析、AI 深度分析与课题建议生成；
2. **Claude 文献阅读 Skills** —— 两个可安装的 skill，分别用于深度解读**研究型论文**和**综述型论文**。

领域背景：结构生物学（Structural Biology）/ 计算机辅助药物设计（CADD）/ AIDD / 细胞生物学 / 机器学习交叉方向。

## 项目结构

```
literature/
├── research-paper-interpreter/   # Skill 1：研究型论文深度解读
│   └── SKILL.md
├── review-paper-interpreter/     # Skill 2：综述型论文系统解读
│   └── SKILL.md
├── main.py                       # 文献管理系统 v1（初版）
├── main_v4.py                    # 文献管理系统 v4（功能完整版，推荐）
├── main_v4_clean.py              # v4 精简版（用于 PyInstaller 打包）
├── requirements.txt              # Python 依赖
└── .github/
    └── workflows/
        └── build-macos.yml       # macOS 应用自动打包
```

---

## Skills：AI 文献阅读助手

两个 skill 都遵循同一套核心原则：**不做逐段翻译或机械总结**，而是把论文当作"科研对象"来重建其科学逻辑，并明确区分三类信息——`Paper`（论文原文陈述）、`External evidence`（联网核验的外部证据）、`Synthesis`（综合分析）。允许联网时会主动检索最新文献、预印本和官方代码仓库进行核验。

两者的区别在于论文类型不同、解读目标不同：

| | research-paper-interpreter | review-paper-interpreter |
|---|---|---|
| **适用论文类型** | 原始研究论文（Research Article） | 综述 / Survey / Perspective / Roadmap |
| **核心目标** | 还原"这项工作做了什么、为什么这样设计、证据是什么" | 重建"这个领域如何被组织、方法如何演化、空白在哪里" |
| **典型输出** | 方法机制拆解、实验证据审计、创新性评估、代码与可复现性分析、可执行的后续研究设计 | 领域分类谱系表、技术演进脉络、代表工作剖析、领域共识与瓶颈、研究空白与选题启发 |
| **典型触发语** | "解读这篇论文"、"分析它的模型架构和实验"、"评估可复现性" | "解读这篇综述"、"梳理方法演化和研究空白"、"结合最新文献评估这篇 Survey 的 future directions" |

### research-paper-interpreter（研究型论文解读）

把研究论文解读为**技术研究对象**，回答：这项工作到底做了什么、为什么这样设计、证据是否支撑结论、真正的新意在哪里、弱点是什么、可复现性如何、如何以它为起点做出更好的研究。

- 11 步工作流：确立研究契约 → 端到端方法重建 → 关键模块拆解 → 数据与监督审计 → 实验即假设检验 → 结果分层提取 → 创新性定位 → 局限与失效模式 → 代码审计 → 研究版图定位 → 转化为研究方向
- 支持模型 / Agent / 结构生物学 / AIDD·CADD 四类领域适配器
- 有官方代码时会同时分析论文与代码实现，指出不一致之处

### review-paper-interpreter（综述型论文系统解读）

把综述解读为**领域知识地图**，重点不是复述目录，而是从综述中恢复知识结构、方法谱系、技术演进、代表工作、领域共识、核心难题与可执行启发。

- 7 步工作流：确认综述定位 → 重建领域分类体系 → 提取代表性方法 → 判断领域共识与瓶颈 → 提取研究空白 → 联网更新综述时效性 → 转化为科研价值
- 会针对综述发表后的进展做**时效核验**：哪些预测已实现、哪些空白已被填补、原分类框架是否仍然适用
- 输出"优先精读清单 + 关键研究空白 + 可执行启发"，直接服务于选题

### 安装与使用

将对应 skill 文件夹复制到 Claude Code 的 skills 目录即可：

```bash
# 全局安装（所有项目可用）
cp -r research-paper-interpreter ~/.claude/skills/
cp -r review-paper-interpreter  ~/.claude/skills/

# 或仅当前项目安装
mkdir -p .claude/skills
cp -r research-paper-interpreter .claude/skills/
cp -r review-paper-interpreter  .claude/skills/
```

安装后在 Claude Code 中直接说"帮我解读这篇论文 / 这篇综述"即可自动触发，或用"使用 research-paper-interpreter 解读这篇论文"显式调用。也可以指定聚焦方向，例如：

- `重点分析模型架构和数据流`
- `重点分析代码实现和可复现性`
- `重点分析 GPCR 功能构象建模`
- `结合最新文献重新评估这篇综述的 future directions`

---

## 文献智能管理系统（桌面应用）

基于 Python + SQLite + PyMuPDF 的本地文献管理工具，内置 DeepSeek 等 OpenAI 兼容大模型接口，实现文献的自动解析与智能分析。

### 版本说明

| 文件 | 说明 |
|---|---|
| `main.py` | **v1 初版**：纯 Tkinter 界面，AIDD 方向分类体系（药物筛选、分子生成、蛋白/分子语言模型等），SQLite 存储，DeepSeek API 分析 |
| `main_v4.py` | **v4 完整版（推荐）**：CustomTkinter 现代化界面，面向结构生物学 × CADD × 细胞生物学交叉领域，功能最全 |
| `main_v4_clean.py` | **v4 精简版**：纯 Tkinter 实现，依赖更少，作为 PyInstaller 打包入口 |

### 主要功能

- **文献入库**：批量导入 PDF，自动提取标题、摘要、关键词、DOI、作者、年份；DOI 自动 CrossRef 元数据查询；智能去重
- **分类与标签**：自定义分类体系 + 标签系统，中文拼音排序
- **AI 单篇分析**：调用大模型对入库文献进行方法、创新点等结构化提取
- **AI 课题建议**：勾选多篇文献，自动分析领域分歧并生成跨领域研究课题建议（可导出 Markdown 报告）
- **统计分析**：按分类、年份、期刊等维度的文献库统计
- **模型管理**：内置模型配置管理界面，支持自定义 OpenAI 兼容 API 端点（base_url + api_key）

### 运行

```bash
pip install -r requirements.txt
python main_v4.py
```

大模型功能需要配置 API Key（默认使用 DeepSeek，二选一）：

```bash
export DEEPSEEK_API_KEY="你的key"   # 或在应用内"模型管理"界面配置
```

首次运行会在程序目录创建 `literature.db`（SQLite 数据库）和 `pdfs/`（PDF 存储目录）。

### macOS 打包

`.github/workflows/build-macos.yml` 提供手动触发（workflow_dispatch）的 PyInstaller 打包，产物为兼容 macOS 10.14+ 的 Intel `.app`（通过 Rosetta 构建），在 Actions 页面手动运行后即可从 Artifacts 下载 `literature-macos.zip`。
