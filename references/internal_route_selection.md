# Internal Route Selection

Do not expose route selection to the user unless requested.

## Route A: plan -> image-model samples

Use when the user asks for:
- visual samples;
- mockups;
- style exploration;
- image-model output;
- "先做样板";
- "先看看效果".

## Route B: plan -> template-direct editable route

Use when the user asks for:
- no image generation;
- direct editable PPT;
- strict template use;
- fast production;
- official template compliance;
- highly stable / low-variation output.

Both routes start from the production planning table.

## Route C: plan -> full-deck per-slide image-model design -> editable reconstruction

Use only when the user explicitly requests:
- every slide to be designed by the image model;
- a full set of independent slide mockups before PPTX reconstruction;
- all remaining slides to be generated one by one as visual mockups;
- full-deck image-model design rather than normal expansion from representative samples.

Do not infer Route C from generic requests such as "完成全稿", "继续做完整 PPT", or "按样板扩展".

Route C chain:

production planning table -> mockup family + variants blueprint -> 1-2 pilot pages -> approval -> one independent full-slide image for every slide in batches -> montage review -> editable reconstruction -> QA.

The one-slide-per-image rule remains mandatory. Never generate a storyboard sheet, contact sheet, grid, or multi-slide overview as the source mockup set.
