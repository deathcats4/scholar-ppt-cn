# scholar-ppt-cn

面向多种 Agent/LLM 宿主的中文学术 PPT 工作流 Skill。

它帮助 Agent 从论文、学位论文、报告、图片、表格、笔记、现有 PPTX
或参考模板出发，建立结构化项目状态、规划页面、按需探索视觉方向、生成或指导
生成可编辑 PPTX，并执行确定性的静态 QA。

## 定位

本仓库提供：

- 宿主无关的学术 PPT 工作流规范；
- 统一、版本化的 `project.json`；
- 生产规划 Markdown 导出；
- 环境能力探测；
- PPTX ZIP/OOXML 静态 QA；
- 可复现 Skill 打包；
- 自动测试和跨平台 CI。

本仓库暂不提供内置的确定性 PPTX 生成引擎。PPTX 写入、Office 渲染、视觉
检查和图像生成由当前 Agent 宿主的可用工具提供，并可按能力降级。

## 工作方式

用户只需描述目标，不需要选择 Lite/Standard/Full 模式：

```text
读取材料 → project.json → 页面规划 → 模板/版式选择
→ 按需视觉样板 → 可编辑 PPTX → QA → 修订
```

每个步骤是否执行及其原因写入 JSON。图像模型不是必需依赖，也不绑定某个
具体模型。

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

要求 Python 3.11+，核心命令不依赖第三方包：

```text
python scripts/preflight.py --output outputs/preflight.json
python scripts/init_project.py --slug demo --title "示例汇报" --output outputs/demo/project.json
python scripts/validate_project.py path/to/project.json
python scripts/export_planning.py path/to/project.json path/to/planning.md
python scripts/qa_pptx.py path/to/deck.pptx --project path/to/project.json --report path/to/qa-report.json --update-project
python scripts/export_qa_note.py path/to/qa-report.json path/to/qa-note.md
python scripts/lint_skill.py .
python scripts/package_skill.py --version dev
python -m unittest discover -s tests -v
```

缺少 LibreOffice、PDF renderer、中文字体或其他可选能力时，Skill 会说明影响
并询问是否安装；用户拒绝后继续采用可用的降级路径。

## 项目状态

`schemas/project.schema.json` 定义统一状态。JSON 是机器真源，Markdown 是
从 JSON 生成的用户视图。JSON 只保存路径、ID、短摘要、映射、决策和 QA
结果，不嵌入 PDF、图片或全文。

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

## 开发状态

当前为 v3.4 本地重构阶段。根目录 `AGENTS.md` 记录已经确认的产品原则、
开发约束和本地迭代方式。
