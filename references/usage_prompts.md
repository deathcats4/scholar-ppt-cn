# Usage Prompts

## Start with production planning

```text
请使用 $scholar-ppt-cn，参考模板和材料，先生成生产规划表。
规划表需要包含：页码、标题、叙事段落、页面任务、使用素材、图件形态、核心信息、版式 archetype、密度、素材处理建议和风险。
```

## Make samples after planning

```text
按确认的生产规划表，先做 5–8 页视觉样板，不要生成 PPT。
```

## Direct editable PPT

```text
按确认的生产规划表，不要生图，直接参考模板生成可编辑 PPT。
```

## Expand from approved samples

```text
这几页样板确认，按这个风格扩展成完整可编辑 PPT。
```

## Revise

```text
第 X 页图太小 / 字体不对 / 内容有误，请修一下。
```


## Build mockup family + variants after planning

```text
在生成图片或 PPT 之前，请基于刚才的生产规划表，先生成 mockup family + variants。
请输出：Template DNA 再确认、mockup family 总表、每个 family 的 variants、完整页码到 family/variant 的映射、建议优先生成的 5–8 个样板页。
不要生成图片，不要生成 PPT。
```

## Generate samples from confirmed mockup family

```text
我确认这个 mockup family + variants。
请按其中建议的代表页，逐页生成完整 16:9 slide mockup 样板图。每张图片只能包含一张正视、铺满画布的完整幻灯片；禁止四宫格、九宫格、多页缩略图、总览图、设备展示框或一图多方案。
只生成样板图，不生成 PPTX。
```


## Direct full production with v3.4 quality checks

```text
请使用 $scholar-ppt-cn，沿用 v3.3.1 的生产规划表和 mockup family + variants 流程制作可编辑 PPTX。科研图保持原始比例和必要标注，正文字号沿用 v3.3.1 口径，不设置统一点数阻断；正文过小、拥挤或自动缩字时作为可读性问题复核。完成后渲染全稿、检查 montage，并运行最终 PPTX QA。
```

## Full-deck per-slide image-model route

```text
请使用完整逐页生图路线。先按生产规划表和 mockup family + variants 制作 2 页 pilot；我确认后，剩余每一页都分别调用生图模型生成一张独立的完整 16:9 slide mockup。禁止四宫格、九宫格、contact sheet、总览图或一张图放多页。全套独立视觉稿确认后，再逐页重建为可编辑 PPTX，并完成渲染和 QA。
```

## Continue Route C after approved samples

```text
这几页 pilot 已确认。不要直接用模板扩展；请继续走完整逐页生图路线，把剩余每一页分别生成独立 slide mockup。每批 2–3 页。每次生图都重新注入 Skill 的固定约束，禁止商业课件图标、禁用栏目标签和模型自制机制图；每批逐页验收，失败页重生后再继续。全部样板确认后再重建可编辑 PPTX。
```

## Rebuild approved mockups without decoration carry-over

```text
按已确认样板重建可编辑 PPTX。继承构图、图文比例、层级、配色、对齐和留白，但不要继承灯泡、书本、显微镜、烧瓶、靶心、emoji 等商业课件图标，也不要保留“读图要点、关键认识、综合判断、支持证据、注意事项、证据观察、预期输出、本文切口”等栏目标签。不要重建生图模型自制的简单机制图；普通阅读箭头和来源已确认的关系箭头可以保留。
```
