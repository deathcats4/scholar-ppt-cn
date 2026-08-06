# Changelog

## 3.4.0

- Released the zip-based v3.4 workflow as the stable `scholar-ppt-cn` skill.
- Preserved the v3.3.1 production flow: production planning table, mockup family + variants, representative image-model samples, optional full-deck per-slide image-model design, template-direct editable PPTX, approved-mockup expansion, and montage QA.
- Added a mandatory short constraint block to every image-generation call, retry, and later Route C batch to reduce long-context drift.
- Added per-page acceptance gates before continuing to the next image batch.
- Defined mockup approval as approval of composition and visual system, not automatic approval of icons, labels, or unsupported scientific content.
- Prohibited commercial-course icons and emoji from editable reconstruction across Unicode, icon fonts, PowerPoint shapes, SVG, PNG, and cropped mockup fragments.
- For literature reports, disallowed editorial labels such as 读图要点、关键认识、综合判断、支持证据、注意事项、证据观察、预期输出、本文切口 while retaining 核心问题 and 结论.
- Prohibited image-model-created simple mechanism diagrams; retained ordinary reading arrows and source-supported relationship arrows.
- Clarified that cards and bottom conclusion strips are selective components, not mandatory deck-wide repetition.
- Narrowed deterministic visible-text QA to internal workflow terms, the user-selected prohibited labels, model self-reference, placeholders, prohibited icon glyphs, and icon fonts.
- Added an explicit, non-default full-deck per-slide image-model route.
- Required explicit user intent before every slide is generated as an independent mockup.
- Kept one slide per generated image; grids and storyboard sheets remain invalid.
- Added pilot approval, batched full-deck generation, complete mockup montage review, and slide-by-slide editable reconstruction.
- Clarified that generic requests to finish or expand the deck do not activate the full-deck image-model route.
- Required exactly one complete front-facing 16:9 slide per image-model mockup.
- Rejected four-grid, nine-grid, contact-sheet, storyboard-sheet, multi-thumbnail, multi-alternative, device-frame, gallery, and perspective outputs.
- Required separate image outputs for multiple pages and prohibited cropping grid cells into approved samples.
- Added academic mockup restraint: image models design page composition but may not invent scientific mechanisms or evidence.
- Disabled generic commercial-infographic icons and production-facing labels by default in image-model samples.
- Clarified that raster mockup typography is provisional; actual Microsoft YaHei and rendered readability policy apply during editable reconstruction.
- Bundled editable reference-template workflow.
- Fallback layout archetype library and Template DNA.
- Expanded scientific-figure handling: preserve, overview+detail, split, cross-slide, not-use, and request-higher-resolution.
- Role-based Microsoft YaHei typography instead of bolding all Chinese text.
- Body font-size requirements follow v3.3.1: no universal body-point floor or body-size delivery blocker.
- Body auto-shrink and `<a:normAutofit>` are reported for readability review rather than treated as delivery-blocking errors.
- PptxGenJS 4.0.1 as the default preferred writer for new decks.
- Deterministic PPTX QA, rendering helper, QA note export, and final-file hash verification.
- Automatic appendix-slide handling is not used.

## 3.3.1

Improved compatibility for file-based generation, preview inspection, and QA.

### Added
- Runtime compatibility rules for environments with or without file and PPTX tooling.
- Explicit reference loading map in `SKILL.md`.
- PPTX QA contract.
- Image-generation batching rules to avoid long, fragile multi-page mockup runs.

### Changed
- Image-model sample generation now defaults to 1-2 pilot pages followed by 2-3 page batches.

## 3.3.0-productized-planned-family

Added a mandatory mockup family + variants blueprint stage between production planning and generation.

### Added
- Template DNA reconfirmation before mockup family construction.
- Mockup family summary table.
- Multiple variants per family.
- Slide-to-family/variant mapping for every planned slide.
- Representative sample selection.
- Dedicated reference: `mockup_family_variant_blueprint_rules.md`.

### Changed
- Image-model samples now follow both the production planning table and the mockup family + variants blueprint.
- Template-direct editable PPTX also uses the family/variant blueprint for visual consistency.
- High-frequency families must define 4-6 variants to reduce repetitive pages.

## 3.2.0-productized-planned-archetype

Restored planning, but redefined it as a production planning table.

### Added
- Production planning table as central pre-generation artifact.
- Planning table fields: narrative section, communication task, source asset, source-asset geometry, core message, layout archetype ID, density, asset handling, risks.
- Hidden narrative presets now include:
  - literature report / journal club;
  - thesis / defense;
  - research progress;
  - general topical presentation.
- Detailed fallback layout archetype library remains required for template-direct generation.
- Image-model samples now follow the planning table while retaining composition freedom inside selected archetypes.

### Clarified
- Planning table is not an old-style rigid slide outline.
- Narrative presets control story order; layout archetypes control structure; Template DNA controls visual identity.
- User-provided outline overrides hidden presets.
