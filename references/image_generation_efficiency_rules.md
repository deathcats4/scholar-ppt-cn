# Image Generation Efficiency Rules

Use these rules when generating image-model slide mockups.

## Default batching

- First generate 1-2 pilot mockups only.
- Use the pilot to test Template DNA, title system, figure/text ratio, unwanted commercial icons, prohibited labels, and whether placeholder text appears.
- After the pilot is acceptable, continue in batches of 2-3 pages.
- For 5-8 requested sample pages, split into at least two batches.
- For more than 8 sample pages, Route A should normally switch to editable PPTX after representative samples are approved. Route C continues only after explicit activation.

## Page selection

Prioritize pages that test different layout risks:

- cover or report map;
- one large evidence figure page;
- one dense multi-panel figure page;
- one chart or quantitative interpretation page;
- one discussion page using real source evidence;
- one conclusion page.

Avoid generating multiple pages that test the same skeleton unless the user specifically needs alternatives.

## Mandatory per-call constraint block

Insert the following constraints into every image-generation call, including pilot pages, later batches, individual retries, and Route C continuation calls. Adapt only the slide-specific content; keep the restrictions intact.

```text
Generate exactly one complete, front-facing 16:9 academic slide filling the image canvas. Do not generate a grid, contact sheet, storyboard overview, multiple alternatives, device frame, gallery, or perspective presentation.

Follow the approved pilot and the assigned mockup family/variant for composition, hierarchy, palette, alignment, and whitespace. Design this slide only.

Use supplied real scientific evidence or a neutral placeholder. A mechanism diagram may be designed or simplified only from the supplied source-grounded mechanism blueprint. Preserve every verified scientific node, process, arrow, condition, and conclusion; do not add, complete, or alter scientific content. If a source mechanism figure exists, preserve it as evidence; a simplified explanatory diagram may accompany it when every element remains traceable. Cross-source synthesis, inference, or a proposed hypothesis must be visibly labeled and must not be presented as an established result. Ordinary arrows are allowed for reading order or source-verified relationships.

Do not add light bulbs, books, document icons, people, globes, eyes, targets, trophies, puzzle pieces, gears, check marks, exclamation badges, microscope silhouettes, laboratory-flask icons, hammers, emoji, cartoons, 3D icons, or similar commercial-course decoration.

Cards, gradients, dashed boxes, badges, icon matrices, ribbons, rounded containers, shadows, and conclusion strips may follow the approved template or visual system. Preserve image aspect ratio. Fit images into containers with deliberate alignment, coordinated backgrounds, and balanced padding. Do not leave accidental blank strips, thin exposed gaps, or visibly uneven padding. Preserve axes, legends, units, scale bars, panel labels, and required scientific context.

For literature-report slides, do not add the labels 读图要点、读图结论、关键认识、综合判断、支持证据、注意事项、证据观察、预期输出、本文切口、证据页 1/2、基于论文证据的结构化归纳. 核心问题 and 结论 are allowed. State other supported content directly without editorial labels.

Use a restrained modern Chinese sans-serif appearance visually close to Microsoft YaHei. Use raster text to assess hierarchy and density, not exact PowerPoint point sizes.
```

## Slide-specific prompt content

After the mandatory block, add only the information needed for the current slide:

- slide number and title;
- communication task and core message from the production planning table;
- selected mockup family/variant;
- source-asset identity and geometry;
- required evidence placement and readable region;
- source-supported caption or conclusion text;
- source-grounded mechanism blueprint and element-to-source mapping, when used;
- any verified arrows or relationships;
- approved-pilot visual references.

Do not ask one prompt to create many unrelated pages.

## Per-page acceptance gate

Inspect every generated page before continuing. A page fails and must be regenerated when any of the following is present:

1. more than one slide, a grid, thumbnail sheet, device frame, or perspective presentation;
2. a prohibited commercial icon, emoji, cartoon, or decorative symbol;
3. a prohibited literature-report label;
4. an unsupported mechanism node, scientific arrow, number, figure, or conclusion, or an unlabeled inference/hypothesis;
5. unreadable evidence regions, altered source identity, stretched images, accidental blank strips, thin exposed gaps, or visibly uneven container padding;
6. clear drift from the approved pilot's visual system.

Do not proceed to the next batch while a failed page remains. Do not crop a failed grid or manually hide a failed element and then call the mockup approved.

## Approval semantics

When the user approves a mockup, lock its composition, hierarchy, image/text ratio, palette, alignment, whitespace, and page rhythm. Exclude commercial icons, emoji, decorative symbols, prohibited labels, and untraceable scientific claims. Verify source-grounded mechanism graphics against their blueprint before reconstruction.

## Delivery behavior

After each batch, briefly report:

- generated page numbers;
- failed pages and the exact reason for regeneration;
- whether the visual system is stable enough to continue.

If generation becomes slow or reconnect-prone, stop after the current completed batch and continue with the same mandatory constraint block in the next call.
