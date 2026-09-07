# scholar-ppt-cn

> 把论文、报告、资料，变成一套体面、规范、可编辑的中文学术 PPT。

scholar-ppt-cn 是一个装进 AI 助手（Codex、ChatGPT 等支持 Skills 的智能体）的**学术 PPT 技能包**。你负责提供材料和想法，它负责完成从结构规划到成品交付的整套活儿。

文献汇报、组会 PPT、开题/中期/毕业答辩、研究进展、课程报告……把论文 PDF、提纲、图表或旧 PPT 交给它，可以得到页面文字和结构可编辑、科研图可独立替换的 PPTX 文件。复杂图像内部是否可编辑，取决于原始数据和结构能否可靠恢复。

## 它能为你做什么

**从论文或资料生成全新的 PPT**
- 自动梳理讲述结构：内置文献汇报、答辩、研究进展、通识报告等多种叙事框架，也可完全按你的提纲来
- 从你提供的模板（或内置参考模板）提炼视觉规范：配色、字体、标题层级、页眉页脚、版式节奏
- 直接输出可编辑 PPTX；也可以先出几页整页视觉样板，确认风格后再做全套

**在你的模板 / 旧 PPT 上继续做**
- 直接在已有可编辑 PPTX 上延续制作，复用原模板的主题、版式、页眉页脚等视觉资产
- 换成新课题的新内容，整份保持原模板的视觉体系

**把 PPT 图片重建成可编辑 PPTX**
- 支持 PPT 截图、PNG/JPG 页面、渲染后的 PDF 页、AI 视觉稿和网页截屏
- 页面标题、正文、页脚、色块、线条和页面级结构优先恢复为原生 PowerPoint 对象
- 完整科研图、截图和复杂视觉素材按实际编辑价值整体保留，避免“对象数量很多但无法维护”的假可编辑
- 支持默认智能判断、完整保留、深度拆解和局部拆解等混合编辑颗粒度
- 通过逻辑分组保持编号与底形一起移动；需要连接节点的箭头使用原生连接关系，并检查实际编辑行为

**复杂制作先确认执行路径**

- 新建整套 PPT、按样板扩展或大范围重设计开始前，会先回显范围、模板关系、制作方式、停点和交付物
- 发现会改变结果的歧义时会先等待确认，避免直接启动长时间生成

**修改、订正已有的 PPT**
- 局部修订：改某几页的文字、图片、版式问题
- 整篇统一修订：批量替换术语、统一字体、统一页码与来源标注
- 大范围重设计：换风格、重组叙事结构

**守住学术底线**
- 科研图片原样保留：不重画、不"脑补"，坐标轴、图例、单位、标注都在
- 不会给你塞灯泡、书本、emoji 这类"商务课件风"装饰
- 交付前自动渲染预览、静态质检、逐页检查，报告与成品文件一一对应

## 怎么用

请安装发布包，不要把包含开发文档和评测材料的 Git 工作区直接作为 skill 目录。可以在克隆仓库后生成一个只含运行时文件的目录：

```bash
git clone https://github.com/deathcats4/scholar-ppt-cn.git
powershell -File .\scholar-ppt-cn\scripts\package_skill.ps1 -Destination .\scholar-ppt-cn-runtime
# 将 scholar-ppt-cn-runtime 文件夹改名为 scholar-ppt-cn，放入 Skills 目录
```

发布包只包含 `SKILL.md`、运行时 references/scripts/assets 和接入配置；仓库中的开发说明、测试和评测记录不属于 skill 运行时。

然后直接用大白话提需求，比如：

- "参考这篇论文做一份组会汇报 PPT，先做规划表。"
- "先做 5 页视觉样板看看风格，先不要生成 PPT。"
- "不要生图，直接生成一份可编辑的 PPTX。"
- "把这张 PPT 图片转成视觉接近、结构合理的可编辑 PPTX。"
- "整页截图不要当背景，标题和页面结构要能改；这张科研图整体保留。"
- "在这个旧 PPT 的基础上继续做，换成新课题的内容。"
- "第 6 页的图太小，调大一点；全文把『XX』统一改成『YY』。"

没有自带模板也没关系，技能内置了一套中文学术参考模板（`assets/templates/scholar-ppt-cn-reference-template.pptx`）。

## 可选的本机工具

渲染预览与最终质检会用到 Python、LibreOffice、poppler 和 Node.js。缺工具时技能会如实说明并自动降级——**不会假装检查过**。

```text
python scripts/preflight.py --output preflight.json
python scripts/render_preview.py deck.pptx --output-dir previews --montage montage.png
python scripts/qa_pptx.py deck.pptx --profile group-meeting --report qa-report.json
python scripts/verify_final_qa.py deck.pptx qa-report.json --require-profile group-meeting
```

## 项目结构

```text
scholar-ppt-cn/
├── SKILL.md              技能主说明（智能体从这里读取工作流程）
├── references/           各环节操作规则（叙事、版式、图片、QA 等）
├── scripts/              渲染预览、静态质检等工具脚本
├── assets/templates/     内置中文学术参考模板
└── agents/               智能体接入配置
```

## 版本历史

主要变化见 [CHANGELOG.md](CHANGELOG.md)。当前版本：**3.5.1**。

## License

[MIT](LICENSE)
