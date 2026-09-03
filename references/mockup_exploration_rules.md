# Mockup Exploration Rules

Image-model samples should follow the production planning table and the selected mockup family/variant.

A valid mockup is a complete 16:9 slide, not a standalone illustration.

## One slide per image

Each generated mockup image must contain exactly one complete, front-facing 16:9 slide that fills the image canvas.

Do not generate:
- four-grid, nine-grid, or other multi-slide grids;
- contact sheets, storyboard sheets, presentation overviews, or slide-thumbnail collections;
- several layout alternatives inside one image;
- laptop, monitor, phone, projector, desk, frame, or perspective mockups around the slide;
- a slide shown at an angle, with margins that imitate a gallery, or as one panel inside a larger composition.

When several pages are requested, generate them as separate image outputs or separate generation calls. A montage may be assembled only after the independent full-slide images exist; it is a review artifact, not an image-model slide mockup.

A multi-slide grid is a failed output. Discard and regenerate it as independent full-slide images; do not crop grid cells and treat them as approved samples.

Make composition decisions inside the selected archetype family while preserving:
- narrative purpose;
- source asset identity;
- evidence integrity;
- Template DNA;
- readability.

## Persistent per-call constraints

Insert the mandatory per-call constraint block from `image_generation_efficiency_rules.md` into every image-generation call, including retries and Route C batches.

## Scientific-content boundary

The image model designs page composition and may visualize a verified mechanism blueprint; it does not decide scientific content.

- Allow a simplified mechanism, pathway, workflow, or conceptual diagram when every node, process, arrow, condition, and conclusion is supplied from the source material.
- Do not invent, complete, or alter causal relationships, quantitative trends, scientific structures, or experimental conditions.
- Do not redraw a scientific data figure from memory or create a plausible-looking replacement for missing evidence.
- Use real supplied evidence when available. Otherwise use a neutral evidence placeholder with no fabricated data, labels, micrographs, curves, or mechanism details.
- If the source contains a mechanism figure, preserve that real figure as evidence. A source-grounded simplified explanation may accompany it without replacing it.
- Cross-source synthesis, inference, or a proposed hypothesis must be clearly labeled and confirmed by the user before final delivery.
- Ordinary arrows are allowed for reading order and for relationships already verified in the source material.

## Academic visual restraint

Default to real evidence, typography, whitespace, alignment, restrained dividers, and source-supported arrows.

Do not add generic decorative icons or commercial-infographic devices, including light bulbs, books, document icons, people silhouettes, globes, eyes, targets, trophies, puzzle pieces, gears, check marks, exclamation badges, microscope silhouettes, laboratory-flask icons, hammers, emoji, cartoons, or 3D icons.

Cards, gradients, dashed boxes, badges, icon matrices, ribbons, rounded containers, shadows, and conclusion strips may follow the user template, Template DNA, the selected family/variant, or the page composition. Keep their geometry, spacing, and visual treatment coherent across the deck.

Preserve image aspect ratio. Fit images into containers with deliberate alignment, coordinated backgrounds, and balanced padding. Do not leave accidental blank strips, thin exposed gaps, or visibly uneven padding. Preserve the complete context of scientific evidence; crop decorative photos only when the composition requires it.

For literature reports and journal-club decks, do not use presentation labels such as:
- 读图要点;
- 读图结论;
- 关键认识;
- 综合判断;
- 支持证据;
- 注意事项;
- 证据观察;
- 预期输出;
- 本文切口;
- 证据页 1/2 or 2/2;
- 基于论文证据的结构化归纳.

“核心问题” and “结论” remain valid headings. Rewrite other supported content as direct academic statements without an extra editorial label.

## Mockup typography

Raster mockup text is a visual approximation, not a reliable font installation or point-size specification.

- Request a restrained modern Chinese sans-serif appearance visually close to Microsoft YaHei.
- Avoid handwritten, calligraphic, decorative, outlined, shadowed, distorted, or artificially condensed text.
- Use the mockup to judge hierarchy, density, and relative scale only.
- Set actual Microsoft YaHei and final point sizes during editable reconstruction.

Mockup text is provisional and must be checked before final PPT delivery.
