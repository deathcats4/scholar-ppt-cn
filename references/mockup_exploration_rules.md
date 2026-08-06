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

The image model may make composition decisions inside the selected archetype family, but it must preserve:
- narrative purpose;
- source asset identity;
- evidence integrity;
- Template DNA;
- readability.

## Persistent per-call constraints

Do not assume that constraints stated earlier in a long conversation will remain active. Every image-generation call, including retries and later Route C batches, must repeat the mandatory per-call constraint block in `image_generation_efficiency_rules.md`.

## Scientific-content boundary

The image model designs the page composition; it does not author scientific content.

- Do not invent or complete mechanisms, reaction pathways, experimental workflows, causal relationships, quantitative trends, or scientific structures.
- Do not generate a “simple mechanism diagram”. Simple-looking nodes and arrows can still create unsupported scientific claims.
- Do not redraw a scientific figure from memory or create a plausible-looking replacement for missing evidence.
- Use real supplied evidence when available. Otherwise use a neutral evidence placeholder with no fabricated data, labels, micrographs, curves, or mechanism details.
- If the source contains a mechanism figure, use that real source figure as an evidence asset. Do not ask the image model to reinterpret or redraw it.
- Ordinary arrows are allowed for reading order and for relationships already verified in the source material.

## Academic visual restraint

Default to real evidence, typography, whitespace, alignment, restrained dividers, and source-supported arrows.

Do not add generic decorative icons or commercial-infographic devices, including light bulbs, books, document icons, people silhouettes, globes, eyes, targets, trophies, puzzle pieces, gears, check marks, exclamation badges, microscope silhouettes, laboratory-flask icons, hammers, emoji, cartoons, or 3D icons.

Do not add decorative cards, gradients, dashed boxes, badges, icon matrices, or colored ribbons merely to fill empty space. Use containers only when they organize genuine categories, comparisons, or process stages. Cards and bottom conclusion strips are not default components and should not recur on every slide.

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
