# scholar-ppt-cn

一个用于 ChatGPT / Codex 的中文学术 PPT Skill。

它把“从论文到可编辑组会 PPT”的流程拆成：

1. 生产规划表
2. mockup family + variants
3. image model 样板页
4. 可编辑 PPTX 重建
5. montage QA

## What It Does

`scholar-ppt-cn` is an AI academic PPT workflow skill for Codex / ChatGPT. It helps turn papers, theses, reports, figures, notes, reference templates, screenshots, or visual mockups into planned academic presentations and editable PowerPoint decks.

## Template Download

The repository includes a 5-slide reference PowerPoint template:

[Download scholar-ppt-cn-reference-template.pptx](assets/templates/scholar-ppt-cn-reference-template.pptx)

Use it as the visual reference when creating Chinese academic presentations with this skill.

Core idea:

提纲决定讲述顺序；详细版式库决定页面结构；模板 DNA 决定视觉风格；image model 或 Python 负责生成。

## Workflow

1. Generate a production planning table.
2. Use the table to build a mockup family + variants blueprint.
3. Generate visual samples or direct editable PPT from the blueprint.
4. Approve samples when image-model route is used.
5. Expand or reconstruct an editable PPTX.
6. Preview, QA, and revise.

The planning table is not a rigid old-style outline. It maps each slide to a narrative section, source asset, source-asset geometry, core message, and detailed layout archetype.

For Codex, the skill now treats editable PPTX work as an artifact workflow: generate files, inspect or render previews when possible, run QA, and report any unavailable checks honestly. ChatGPT-style environments can still use the same planning and blueprint workflow, with QA steps performed after export.

## Version

v3.3.1 adds Codex artifact QA rules, explicit reference loading, and image-generation batching for slide mockups. v3.3 added the formal mockup family + variants stage between planning and generation.
