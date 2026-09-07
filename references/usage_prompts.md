# Usage Prompts

## Start with production planning

```text
请使用 $scholar-ppt-cn，参考模板和材料，先生成生产规划表。
规划表需要包含：页码、标题、叙事段落、页面任务、使用素材、图件形态、核心信息、布局意图/候选结构、密度、素材处理建议和风险。不要在规划表中锁定 family、variant 或 archetype ID；这些在后续蓝图阶段确定。
```

## Let the skill confirm a complex production path first

```text
这是一个复杂制作任务。请先用普通话回显：目标与范围、材料和证据、模板如何使用、将采用的制作路径、下一处停点、交付物和关键假设；如果有会改变结果的歧义，先等我确认，再开始生成或渲染。
```

## Make samples after planning

```text
按确认的生产规划表，先做 5–8 页视觉样板，不要生成 PPT。
```

## Direct editable PPT

```text
按确认的生产规划表，不要生图，直接参考模板生成可编辑 PPT。
```

## Rebuild a flattened slide image into an editable PPTX

```text
请把我提供的 PPT 图片 / 截图重建成视觉尽量接近、但具有实际意义可编辑性的 PPTX。页面标题、正文、页脚、色块、线条和页面级结构请优先做成原生 PowerPoint 对象；完整科研图、截图和复杂视觉素材默认作为独立图片保留，不要把整页截图铺成背景。请先按图片重建规则判断对象颗粒度，再生成 PPTX、渲染对比并运行最终 QA。
```

## Rebuild with mixed editability boundaries

```text
请把这页图片重建成可编辑 PPTX。默认采用 SMART：页面层文字和结构可编辑，完整视觉资产整体保留。指定区域“不要拆”，指定区域“内部也尽量可编辑”，只处理我点名的区域；不要猜测图片中的数据、事实或机制关系。
```

## Preserve a complete asset

```text
这块内容作为一张完整视觉素材保留，只需要能移动、缩放、裁切、替换和删除；不要 OCR 后重排内部文字，也不要重画内部图例和线条。
```

## Deep-edit a reliable region

```text
这块图内部也要尽量可编辑。请只在文字、形状、连接线、表格或图示结构能够可靠核对时拆解；没有原始数据或来源支持的部分保留为独立图片，不要为了增加对象数量而猜测。
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
请使用 $scholar-ppt-cn，沿用 v3.3.1 的生产规划表和 mockup family + variants 流程制作可编辑 PPTX。科研图保持原始比例和必要标注，字号沿用 v3.3.1 口径，不设置统一点数阻断或角色字号表；mockup 路线按渲染后的相对视觉比例对齐字号。完成后渲染全稿、检查 montage，并运行最终 PPTX QA。
```

## Full-deck per-slide image-model route

```text
请使用完整逐页生图路线。先按生产规划表和 mockup family + variants 制作 2 页 pilot；我确认后，剩余每一页都分别调用生图模型生成一张独立的完整 16:9 slide mockup。禁止四宫格、九宫格、contact sheet、总览图或一张图放多页。全套独立视觉稿确认后，再逐页重建为可编辑 PPTX，并完成渲染和 QA。
```

## Continue Route C after approved samples

```text
这几页 pilot 已确认。不要直接用模板扩展；请继续走完整逐页生图路线，把剩余每一页分别生成独立 slide mockup。每批 2–3 页。每次生图都重新注入 Skill 的固定约束，禁止商业课件图标和禁用栏目标签；机制图只能使用已核对的来源节点和关系，不得增加无来源科学内容。每批逐页验收，失败页重生后再继续。全部样板确认后再重建可编辑 PPTX。
```

## Rebuild approved mockups without decoration carry-over

```text
按已确认样板重建可编辑 PPTX。继承构图、图文比例、层级、配色、对齐和留白，但不要继承灯泡、书本、显微镜、烧瓶、靶心、emoji 等商业课件图标，也不要保留“读图要点、关键认识、综合判断、支持证据、注意事项、证据观察、预期输出、本文切口”等栏目标签。来源支持的机制图按已核对的节点和关系重建为可编辑对象；推断、假说或跨文献综合需要明确标注并确认。
```
