# scholar-ppt-cn

> 把论文、报告、资料，变成一套体面、规范、可编辑的中文学术 PPT。

scholar-ppt-cn 是一个装进 AI 助手（Codex、ChatGPT 等支持 Skills 的智能体）的**学术 PPT 技能包**。你负责提供材料和想法，它负责完成从结构规划到成品交付的整套活儿。

文献汇报、组会 PPT、开题/中期/毕业答辩、研究进展、课程报告……把论文 PDF、提纲、图表或旧 PPT 交给它，就能得到**结构清楚、版式规范、每个字每张图都能直接改**的 PPTX 文件。

## 它能为你做什么

**从论文或资料生成全新的 PPT**
- 自动梳理讲述结构：内置文献汇报、答辩、研究进展、通识报告等多种叙事框架，也可完全按你的提纲来
- 从你提供的模板（或内置参考模板）提炼视觉规范：配色、字体、标题层级、页眉页脚、版式节奏
- 直接输出可编辑 PPTX；也可以先出几页整页视觉样板，确认风格后再做全套

**在你的模板 / 旧 PPT 上继续做**
- 直接在已有可编辑 PPTX 上延续制作，复用原模板的主题、版式、页眉页脚等视觉资产
- 换成新课题的新内容，整份保持原模板的视觉体系

**修改、订正已有的 PPT**
- 局部修订：改某几页的文字、图片、版式问题
- 整篇统一修订：批量替换术语、统一字体、统一页码与来源标注
- 大范围重设计：换风格、重组叙事结构

**守住学术底线**
- 科研图片原样保留：不重画、不"脑补"，坐标轴、图例、单位、标注都在
- 不会给你塞灯泡、书本、emoji 这类"商务课件风"装饰
- 交付前自动渲染预览、静态质检、逐页检查，报告与成品文件一一对应

## 怎么用

把本仓库里的 `scholar-ppt-cn` 文件夹放进你的 AI 助手的 Skills 目录即可，例如：

```bash
git clone https://github.com/deathcats4/scholar-ppt-cn.git
# 将 scholar-ppt-cn 文件夹放入 Skills 目录，例如 ~/.agents/skills/scholar-ppt-cn
```

然后直接用大白话提需求，比如：

- "参考这篇论文做一份组会汇报 PPT，先做规划表。"
- "先做 5 页视觉样板看看风格，先不要生成 PPT。"
- "不要生图，直接生成一份可编辑的 PPTX。"
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

主要变化见 [CHANGELOG.md](CHANGELOG.md)。当前版本：**3.4.6**。

## License

[MIT](LICENSE)
