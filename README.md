# scholar-ppt-cn v3.4

一个用于中文学术 PPT 规划、样板和可编辑 PPTX 生成的 Skill。

这一版以 v3.3.1 为底层工作流。它保留：

1. 生产规划表；
2. mockup family + variants 蓝图；
3. 生图整页代表样板路线；
4. 用户明确选择时启用的全稿逐页生图路线；
5. 模板直出可编辑 PPTX 路线；
6. 用户确认后的视觉系统锁定与可编辑重建；
7. montage QA。

在这些原路线之上，v3.4 增加：每次生图调用重复注入学术约束，并在可编辑重建时过滤商业课件装饰。

只加入以下 v3.4 改进：

- 更完整的科研图片处理；
- 中文字体按角色使用字重，不再全部加粗；
- 字号要求沿用 v3.3.1：不设置统一点数阻断或角色字号表；
- mockup 路线按渲染后的相对视觉比例对齐字号；
- 新建 PPTX 默认首选 PptxGenJS 4.0.1；
- 可执行静态 QA、渲染检查和最终文件哈希验证；
- 不自动生成附录页。

## Core workflow

```text
材料与模板
→ Template DNA
→ 生产规划表
→ mockup family + variants
→ 生图代表样板、全稿逐页独立生图，或模板直出可编辑 PPTX
→ 用户确认与视觉系统锁定
→ 可编辑 PPTX
→ 渲染、montage、静态 QA、最终哈希验证
```

没有用户模板时，继续使用内置参考模板：

`assets/templates/scholar-ppt-cn-reference-template.pptx`

## Explicit invocation

```text
$scholar-ppt-cn
```

## Local QA commands

```text
python scripts/preflight.py --output preflight.json
python scripts/render_preview.py deck.pptx --output-dir previews --montage montage.png
python scripts/qa_pptx.py deck.pptx --profile group-meeting --report qa-report.json
python scripts/export_qa_note.py qa-report.json qa-note.md
python scripts/verify_final_qa.py deck.pptx qa-report.json --require-profile group-meeting
```

PptxGenJS dependency is pinned in `package.json` and `package-lock.json`. It is the default preferred writer for new editable decks, not the only usable tool; use another writer when preserving or repairing a complex existing PPTX is more appropriate.


## Optional full-deck image-model route

这条路线不会自动启动。只有明确要求“整套每一页都先用生图模型设计”“全稿逐页生成独立视觉稿”或“剩余页面全部逐页生图”时才启用。

```text
请使用完整逐页生图路线：先做 2 页 pilot，确认后让每一页分别生成一张独立的 16:9 slide mockup；全套视觉稿确认后，再逐页重建为可编辑 PPTX。
```

“完整逐页生图”仍然要求一张图片只包含一张幻灯片，不能生成九宫格、contact sheet 或多页总览。


## Persistent image-model constraints

Pilot、后续批次、失败重试和全稿逐页生图都必须重新注入同一段短约束，不能依赖长上下文记忆。文献汇报默认不使用“读图要点、关键认识、综合判断、支持证据、注意事项、证据观察、预期输出、本文切口”等栏目标签；“核心问题”和“结论”允许。生图模型不得制作简单机制图。

可编辑重建只继承样板的构图、层级、配色、对齐和留白，不继承灯泡、书本、显微镜、烧瓶、靶心、emoji 等商业课件图标，也不把这些内容以 Unicode、图标字体、PowerPoint 形状、SVG 或 PNG 的方式重新制作。
