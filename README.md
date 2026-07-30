# scholar-ppt-cn

面向多种 Agent/LLM 宿主的中文学术 PPT 工作流 Skill。

它帮助 Agent 从论文、学位论文、报告、图片、表格、笔记、现有 PPTX
或参考模板出发，建立结构化项目状态、规划页面、按需探索视觉方向、生成或指导
生成可编辑 PPTX，并执行确定性的静态 QA。

## 版本状态

当前开发版本为 **v3.4.0-beta.1**。核心工作流已经进入 Beta 测试，视觉参考包、
跨宿主生成一致性及部分内部 Schema 和接口仍会继续调整。现有自然语言用法将
尽量保持兼容，但不保证开发阶段的内部 JSON 和中间文件格式保持不变。

需要继续使用原有工作流的用户，可以选择
[v3.3.1 稳定版](https://github.com/deathcats4/scholar-ppt-cn/releases/tag/v3.3.1)。
该版本及其 Git 标签会继续保留，不会被 v3.4 覆盖。

## 定位

本仓库提供：

- 宿主无关的学术 PPT 工作流规范；
- 统一、版本化的 `project.json`；
- 生产规划 Markdown 导出；
- 环境能力探测；
- 可选的轻量 Python 可编辑 PPTX 回退运行时；
- PPTX ZIP/OOXML 静态 QA；
- 可复现 Skill 打包；
- 自动测试和跨平台 CI。

本仓库不承诺完整的高保真 PPTX 生成引擎。v3.4 Beta 提供一个轻量、确定性的
Python 回退运行时：当当前模型与执行环境需要更确定的输出路径时，它可以根据
`project.json` 生成基础可编辑 PPTX，避免在任务中临时编写大型构建脚本。
严格复用用户母版、复杂图表、动画和高设计完成度页面仍优先交给宿主工具。
Office 渲染、视觉检查和图像生成继续按能力启用和降级。

## 工作方式

用户只需描述目标，不需要选择 Lite/Standard/Full 模式：

```text
读取材料 → project.json → 页面规划 → 模板/版式选择
→ 按需视觉样板 → 可编辑 PPTX → QA → 修订
```

每个步骤是否执行及其原因写入 JSON。图像模型不是必需依赖，也不绑定某个
具体模型。

模板方向、是否先看 3–5 页代表性样板、目标时长等主观选择由 Agent 用简短
问题询问用户。可从材料和环境中确定的事实仍由 Agent 自动发现。代表性样板
可以直接使用模板制作成可编辑页面，不依赖图像生成。

QA 默认对整个 PPTX 做静态检查，再用一次蒙太奇定位异常；只有异常页会被
单独打开和重渲染，不进行耗时的逐页人工检查。

## 常用调用

```text
使用 $scholar-ppt-cn，根据论文先建立项目 JSON 和生产规划，不生成 PPT。
```

```text
使用 $scholar-ppt-cn，不要生成视觉样板，直接参考我的模板制作可编辑 PPTX 并做 QA。
```

```text
使用 $scholar-ppt-cn，修改现有项目的第 4 页和第 7 页，重新导出并检查。
```

## 本地工具

要求 Python 3.11+。项目初始化、Schema 校验、静态 QA、视觉包校验和打包等
核心命令不依赖第三方包：

```text
python scripts/preflight.py --output outputs/preflight.json
python scripts/init_project.py --slug demo --title "示例汇报" --output outputs/demo/project.json
python scripts/validate_project.py path/to/project.json
python scripts/export_planning.py path/to/project.json path/to/planning.md
python scripts/qa_pptx.py path/to/deck.pptx --project path/to/project.json --report path/to/qa-report.json --update-project
python scripts/export_qa_note.py path/to/qa-report.json path/to/qa-note.md
python scripts/validate_visual_references.py --pack assets/visual-reference-packs/blue-academic/pack.json
python scripts/validate_visual_references.py --plan assets/visual-reference-packs/blue-academic/generation/generation-plan.json
python scripts/validate_visual_references.py --family-plan assets/visual-reference-packs/blue-academic/generation/family-expansion-plan.json
python scripts/export_visual_family_prompts.py assets/visual-reference-packs/blue-academic/generation/family-expansion-plan.json assets/visual-reference-packs/blue-academic/generation/FAMILY_EXPANSION_PROMPTS.md
python scripts/lint_skill.py .
python scripts/package_skill.py --version dev
python -m unittest discover -s tests -v
```

需要生成基础可编辑 PPTX 时，可在说明用途并征得用户同意后安装固定版本依赖：

```text
python -m pip install -r requirements-runtime.txt
python scripts/build_deck.py path/to/project.json --base-dir . --report path/to/build-report.json --update-project
```

回退运行时支持封面、章节、陈述、要点、单图、对比、多面板、流程和结论等
语义页面类型，并保留原画布、原始证据图比例和可编辑文字/形状。它不会自动给
封面加图、自动生成来源区、把内部风险提示写进页面，也不会逐像素照抄视觉参考
图。已有生成结果在覆盖前会保存到 `versions/`，随后仍必须运行静态 QA。

缺少 LibreOffice、PDF renderer、中文字体或其他可选能力时，Skill 会说明影响
并询问是否安装；用户拒绝后继续采用可用的降级路径。

## 项目状态

`schemas/project.schema.json` 定义统一状态。JSON 是机器真源，Markdown 是
从 JSON 生成的用户视图。JSON 只保存路径、ID、短摘要、映射、决策和 QA
结果，不嵌入 PDF、图片或全文。

当前 `1.0.0` Schema 随 v3.4 Beta 共同试用，在 v3.4.0 稳定版前仍可能根据
真实运行反馈调整；它不是对旧开发期 JSON 的长期兼容承诺。稳定版如需进行
不兼容修订，将先提供版本迁移支持。

示例见 `tests/fixtures/project-valid.json`。

## 模板

目标内置模板体系包括：

- 简洁理工；
- 深色报告；
- 温和人文。

用户模板始终优先，并保留其原始画布尺寸。无模板时默认 16:9。

仓库现有的 `scholar-ppt-cn-reference-template.pptx` 是待替换的旧开发资产，
新版工作流不再把它作为自动默认模板。三套原创中性模板将在后续阶段制作和
视觉验证。

## 视觉参考包

v3.4 引入与可编辑模板互补的视觉参考包。预生成的高质量页面
图片只用于学习层级、留白、图文关系和页面节奏；最终 PPTX 仍使用真实内容和
可编辑对象重建，不会把整页参考图作为背景。

`assets/visual-reference-packs/blue-academic/` 当前为 `active`，包含 31 张
经过人工筛选的参考图，覆盖封面、研究空白、研究问题、方法设计、单主图结果、
比较、多面板、机制、讨论与展望、结论十类核心页面角色。每类以 3 张作为最低
探索数量，优秀且不重复的候选可以更多。运行时先读取元数据，再只打开匹配的
少量图片；示例图表、数字和结论不得进入最终 PPTX。该参考包已经用于真实论文
的本地端到端验证，后续仍会继续扩展页面角色、内容几何和跨学科覆盖。

这些参考图由生成式 AI 辅助生成并经人工筛选，仅用于视觉与构图参考，不作为
科研证据或最终幻灯片内容。发布包只包含运行所需的图片与元数据，不包含生成
提示词、生成计划和总览图等开发资料。

## 开发状态

当前为 v3.4.0-beta.1 阶段。根目录 `AGENTS.md` 记录已经确认的产品原则、
开发约束和本地迭代方式。Beta 完成真实材料回归、跨平台验证和外部审查后，
再进入 v3.4.0 稳定版本。
