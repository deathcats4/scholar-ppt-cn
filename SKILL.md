---
name: scholar-ppt-cn
description: >-
  Create, restyle, or rebuild Chinese academic PowerPoint presentations from
  papers, theses, reports, figures, notes, templates, screenshots, or visual
  mockups. Use for presentation planning, Template DNA extraction, slide
  mockups, template-based editable PPTX generation, editable reconstruction,
  rendering, and final QA.
metadata:
  version: 3.4.6
  summary: Chinese academic PPT planning, visual design, editable reconstruction, rendering, and deterministic QA.
---

# Scholar PPT CN Skill

## User-facing operation

Keep the user interface simple. Classify the task and select routes internally.

The user may say:

- "参考模板和材料，先做规划表。"
- "按规划表先做 5–8 页视觉样板，不要生成 PPT。"
- "整套每一页都先逐页生图，全部确认后再重建 PPTX。"
- "这几页样板确认，按这个风格扩展成完整可编辑 PPT。"
- "不要生图，直接参考模板生成可编辑 PPT。"
- "第 X 页图太小 / 字体不对 / 内容有误，修一下。"

Do not ask the user to choose internal route names, archetype IDs, family IDs, variant IDs, or QA gates unless requested.

Follow any user-provided outline, table of contents, slide count, page order, template, font requirement, or delivery format.

## Template and input authority

Use a user-provided template when available.

If the user provides no template, use `assets/templates/scholar-ppt-cn-reference-template.pptx` for production planning, family/variant blueprints, mockups, and PPTX generation. A content-only outline may proceed without Template DNA.

When a visual template or reference is used for a new deck or broad redesign, extract Template DNA before production planning. Template DNA is the visual-consistency layer: it captures the canvas/background behavior, institutional identity, palette, typography roles, title treatment, footer/page-number styling, caption style, recurring lines/blocks/dividers, decorative motifs, and reusable micro-components. It describes how the deck should look; it does not decide the scientific narrative or the body layout of a slide.

If the user wants the new presentation made directly on top of an editable PPTX, says to continue or fill the provided deck, asks for the same PPT system rather than merely a similar style, or otherwise indicates that the source PPTX itself should remain the visual base, also use source-deck continuation. Read `references/source_pptx_continuation_rules.md`.

For source-deck continuation, use Template DNA together with direct native-asset reuse:

- reuse native Theme/Master/Layout/background assets when they carry visual identity;
- inspect ordinary slides when the master is generic and reuse recurring editable visual objects such as title treatments, lines, blocks, section marks, logos, page numbers, and footer/header elements;
- prefer the original editable asset over an approximate redraw when reuse is possible;
- use Template DNA to keep newly designed slides and newly created visual elements consistent with the same PPT system.

If the user wants only a similar/reference style, asks to imitate or restyle from a PPT/PPTX, or provides screenshots or other non-editable visual references, use Template DNA without native source-deck continuation.

By default, the reference deck is visual-system authority, not body-layout authority. The new scientific sources determine the narrative and evidence; scholar-ppt-cn selects or designs body layouts from the communication task, evidence relationships, source-asset geometry, information density, readability, and deck rhythm. Do not inspect or reuse old result-page, discussion-page, data-page, microscopy-page, or other scientific content layouts as default candidates.

Stable frame pages such as cover, table of contents, section-divider, and closing pages may retain their source structure when they are clearly part of the template identity and remain naturally applicable. Preserve a named old page layout or exact object positions only when the user explicitly requests strict/in-place preservation or explicitly says that a particular source page should be used as the layout reference.

Do not apply a blanket rule that every source text string must be deleted. Preserve or update stable template wording that remains natural after the research topic changes, such as institutional identity, `Part.01`-style section markers, generic `目录`/`总结`/`谢谢` labels, appropriate closing phrases, date fields, and fixed header/footer wording. Replace old project-specific titles, authors, body text, sample IDs, data, figures, captions, citations, hypotheses, conclusions, and topic-specific labels. Retain attribution or license text when required.

Treat example text sizes and font weights as visual references. Set final typography from the active visual system, content hierarchy, and rendered readability.

## Runtime compatibility

Use the file, PPTX-writing, rendering, vision, image-generation, and inspection tools available in the current environment.

When file and tool access is available:

- read the relevant source files;
- create real output files;
- render or inspect previews;
- revise identified problems before delivery;
- return file paths and a concise QA note.

When required tools are unavailable:

- perform the strongest available substitute;
- deliver the planning table, blueprint, prompts, or implementation instructions that can be completed;
- report every skipped generation, rendering, inspection, or QA step;
- do not claim an unavailable check passed.

## Progressive reference loading

Read each reference completely when its stage or route becomes active. Do not load references for unrelated routes. Load newly applicable references before continuing when the task scope expands.

### Narrative and planning

- Narrative selection: `references/hidden_narrative_presets.md`
- Template DNA extraction: `references/template_dna_rules.md`
- Source-PPTX continuation: `references/source_pptx_continuation_rules.md`
- Evidence inventory: `references/evidence_index_rules.md`
- Source-asset classification: `references/source_asset_geometry_rules.md`
- Production planning table: `references/production_planning_table_rules.md`
- Internal layout selection and fallback pages: `references/fallback_layout_archetype_library.md`
- Mockup family + variants blueprint: `references/mockup_family_variant_blueprint_rules.md`

### Route selection and image-model work

- New-deck route selection: `references/internal_route_selection.md`
- Image-model batching and mandatory per-call block: `references/image_generation_efficiency_rules.md`
- Full-slide mockup rules: `references/mockup_exploration_rules.md`
- Full-deck per-slide image-model route: `references/full_deck_image_model_route_rules.md`

### Cross-route content controls

- Scientific figures and evidence: `references/evidence_asset_rules.md`
- Visible slide-text filtering: `references/visible_text_filter_rules.md`

### Existing PPTX revision

- Localized and deck-wide mechanical revision: `references/existing_pptx_revision_rules.md`

### Approved-mockup expansion and editable PPTX

- Locked approved visual system: `references/locked_visual_system_rules.md`
- Mockup-derived archetypes: `references/mockup_derived_archetype_rules.md`
- Editable reconstruction: `references/editable_reconstruction_rules.md`
- CJK typography: `references/cjk_typography_rules.md`
- Layout repetition: `references/layout_repetition_control.md`
- PptxGenJS and writer selection: `references/pptxgenjs_execution_rules.md`

### Final checking

- Comparative montage review: `references/comparative_montage_qa.md`
- PPTX package, rendering, revision, and hash QA: `references/pptx_qa_rules.md`

## Task classification

Classify the request before starting production.

### Review or revise an existing PPTX

Use this path for targeted review, correction, restyling, page replacement, typography adjustment, image correction, or content correction in an existing deck.

- Use localized revision for named slides, objects, text, figures, or layout defects.
- Use deck-wide mechanical revision for a user-defined replacement or normalization that preserves narrative structure and slide composition.
- Use broad redesign when the request requires new design decisions, narrative restructuring, substantial content expansion, template-geometry changes, or page-family remapping.
- For localized or deck-wide mechanical revision, read `references/existing_pptx_revision_rules.md` and only the content, typography, evidence, writer, and QA references required by the change.
- Do not require Template DNA, a production planning table, or a family/variant blueprint for localized or deck-wide mechanical revision.
- Build or update Template DNA, the production planning table, and the family/variant blueprint before broad redesign.
- Keep localized and mechanical revisions outside Routes A, B, and C.

### Planning only

Use this path when the user asks for an outline, narrative structure, evidence index, production planning table, or family/variant blueprint without slide generation.

1. Read the source material and selected template.
2. Select the narrative preset while preserving user structure.
3. If a visual template/reference is active, extract Template DNA as the visual-consistency layer. If source-deck continuation is active, also inspect reusable native visual assets. Skip visual-style extraction for a content-only outline.
4. Build the evidence index and classify source-asset geometry.
5. Build the production planning table.
6. Build the mockup family + variants blueprint when requested or before later image/PPTX generation.
7. Deliver the requested planning artifact and stop.

### New deck or large expansion

Read `references/internal_route_selection.md`, then select Route A, B, or C.

New-deck work begins with the narrative preset and visual-reference handling.

When a visual template/reference is active, use:

Narrative preset -> Template DNA -> evidence/source-asset analysis -> production planning table -> mockup family + variants blueprint.

When source-deck continuation is active, add source-PPTX native visual-asset inspection and reuse to this chain. The editable source PPTX supplies reusable visual assets while Template DNA keeps new elements visually consistent. The new sources still determine the scientific narrative, and scholar-ppt-cn retains autonomy over body-layout design.

## Route A: representative image-model samples

Use Route A when the user asks for visual samples, mockups, style exploration, image-model output, “先做样板”, or “先看看效果”.

Continue from the shared narrative -> Template DNA -> planning -> family/variant chain. If source-deck continuation is active, preserve reusable native visual assets in the samples while using Template DNA for any newly designed visual elements. Do not copy old scientific content-page layouts unless the user explicitly requests a named source layout.

- Read the image-model, evidence, and visible-text references before the first image call.
- Generate 1–2 pilot pages first.
- Continue accepted work in batches of 2–3 pages.
- Use the assigned family and variant for each page.
- Deliver representative samples and stop for approval unless the user authorizes uninterrupted completion.

## Route B: template-direct editable PPTX

Use Route B when the user requests no image generation, direct editable PPTX, source-deck continuation, strict template use, fast production, official-template visual compliance, or stable low-variation output.

Use the shared narrative -> Template DNA -> evidence/source-asset analysis -> production planning table -> family/variant blueprint before generation.

For source-deck continuation:

AI-selected body layouts -> native visual-asset reuse + Template-DNA styling -> editable PPTX continuation -> render -> QA -> revision.

- Read `references/source_pptx_continuation_rules.md`.
- Start from a copy of the editable source PPTX or an extracted shell made from it when practical, rather than recreating recognizable visual assets from scratch.
- Prefer native Theme/Master/Layout/background assets when they carry the visual identity.
- When the source deck has a generic or nearly empty master, inspect ordinary slides and directly preserve recurring visual objects, exact colors, fonts, title treatments, lines, blocks, footer/page-number treatment, and other stable visual assets.
- Use Template DNA to keep newly designed slides and newly created components visually consistent with the source deck.
- Preserve stable template wording that remains natural in the new deck; replace old project-specific research text, authors, data, figures, captions, citations, conclusions, sample IDs, and topic-specific labels.
- Do not show workflow/provenance text such as `视觉底稿`, `user-supplied reference PPT`, Template DNA notes, route names, or repeated production `[Sources]` blocks. Keep necessary scientific citations concise and content-facing.
- Unless the user explicitly requests a named source layout or strict geometry, scholar-ppt-cn selects or designs each scientific content-page layout from the new communication task, evidence relationships, figure geometry, density, readability, and deck rhythm. Do not inspect old result, discussion, data, microscopy, or other scientific content pages for layout ideas by default.
- Stable frame pages such as cover, table of contents, section divider, and closing pages may retain their source structure when naturally applicable.

For reference-style generation without native source-deck continuation:

detailed layout archetype selection -> Template-DNA parameterization -> editable PPTX generation -> render -> QA -> revision.

- Use Template DNA for visual-system styling and the detailed fallback archetype library for content-driven composition.
- Without an explicit original-layout request, do not use native reference pages or native full-slide layouts as composition candidates. Select or adapt page structures from the scientific narrative, evidence, source geometry, density, and deck rhythm, then style them with Template DNA.
- Map every slide to a family, variant, and layout archetype before PPTX generation.

Strict adherence applies only when the user explicitly requests preservation of native page structure or object positions. Strict geometry preservation does not preserve demo text, sample data, instructions, old project content, or author credits unless attribution or license terms require them.

Read the editable reconstruction, typography, evidence, layout repetition, writer, montage, and PPTX QA references required by the active policy. Preserve editability for text, lines, shapes, callouts, and verified diagrams.

## Route C: full-deck per-slide image-model design

Use Route C only after an explicit user request for image-model design of every slide, the whole deck, or all remaining slides before editable reconstruction.

Do not activate Route C from “完成全稿”, “按样板扩展”, “继续做完整 PPT”, or another generic completion request.

Continue with:

1–2 independent pilot mockups -> user approval -> one independent full-slide image for every planned slide in batches -> full-deck montage review -> locked visual system -> slide-by-slide editable reconstruction -> rendered QA.

- Read `references/full_deck_image_model_route_rules.md` before the pilot.
- Select the 1–2 pilot pages from the representative coverage set in the family/variant blueprint.
- Generate one separate image per slide.
- Reject storyboard sheets, grids, contact sheets, presentation overviews, device frames, galleries, perspectives, and multiple slide alternatives inside one image.
- Stop after the pilot and after the complete independent mockup set unless the user authorizes uninterrupted completion.
- Do not switch to template-direct expansion without user direction.

## Expansion from approved mockups

Use approved mockups as the active visual source.

1. Read `references/locked_visual_system_rules.md`.
2. Read `references/mockup_derived_archetype_rules.md`.
3. Inspect the existing production planning table and family/variant blueprint.
4. Create or update only the missing planning entries required for new slides.
5. Lock composition, image/text proportion, hierarchy, palette, alignment, whitespace, and page rhythm.
6. Derive reusable archetypes from the approved mockups.
7. Map new slides to compatible archetypes and variants.
8. Read the editable PPTX references and reconstruct with real project content.
9. Compare the expanded montage with the approved mockup montage.

Approved mockups override the fallback layout library for visual-system and composition decisions. Adapt new slide composition inside the approved system.

## Shared scientific-content constraints

Treat source materials as evidence assets.

- Use the clearest available source.
- Preserve original aspect ratio and required context.
- Keep axes, legends, units, scale bars, panel labels, table headers, color bars, conditions, and explanatory notes visible.
- Do not invent, complete, or alter mechanisms, numbers, data, trends, experimental conditions, evidence, or scientific conclusions.
- Do not redraw a scientific data figure from memory or create a plausible replacement for missing evidence.
- Use neutral placeholders without fabricated labels, curves, micrographs, or mechanism details when real evidence is unavailable.
- Build simplified mechanism diagrams only from a verified source-grounded blueprint.
- Preserve an original mechanism figure as evidence when one exists.
- Label cross-source synthesis, inference, and proposed hypotheses and obtain user confirmation before final delivery.
- Add position-based annotations only to figures that were visually inspected.
- Confirm or disclose high-risk splitting, cross-slide explanation, or replacement of core evidence.
- Request a higher-resolution source when key evidence remains unreadable.
- Do not create appendix slides automatically.

Use `preserve`, `overview+detail`, `split`, `cross-slide`, `not-use`, or `request-higher-resolution` according to `references/evidence_asset_rules.md`.

## Shared visual-system constraints

Use the active design authority. Template DNA is the visual-consistency layer whenever a visual reference is active. For source-deck continuation, combine Template DNA with directly reused native source-PPTX visual assets. The new sources and production plan remain authoritative for narrative and evidence, and scholar-ppt-cn remains authoritative for body-layout design unless the user explicitly requests a named source layout or strict geometry.

- Adapt layout to narrative purpose, evidence relationships, source-asset geometry, density, and neighboring-slide rhythm.
- When archetype-based generation is active, rotate compatible archetypes across long decks.
- Do not repeat the same visible skeleton for more than two consecutive content slides unless the source material requires it.
- Allow left-image/right-text when appropriate; reject repeated lazy use across the deck.
- Allow cards, borders, rounded containers, gradients, shadows, ribbons, badges, and conclusion strips when selected by the template or approved visual system.
- Preserve image aspect ratio.
- Fit images with deliberate alignment, coordinated backgrounds, and balanced padding.
- Reject stretched images, accidental blank strips, thin exposed gaps, and visibly uneven padding.
- Resize the container, revise the layout, split the slide, or request a better source when evidence does not fit cleanly.

Do not add or reconstruct generic commercial-course decoration, including generic light-bulb, book, document, people, globe, target, trophy, puzzle, gear, check-mark, warning-badge, microscope, laboratory-flask, hammer, emoji, cartoon, or 3D icon motifs.

Do not expose internal workflow terms, route names, family/variant IDs, placeholder instructions, model self-reference, slide-production commentary, figure-handling/cropping commentary, or prohibited literature-report labels in final slides or mockups. Allow domain terms such as prompt, archetype, or reading order when they are genuine source-supported presentation content. Apply `references/visible_text_filter_rules.md`.

## Image-model constraints

The image model designs full-slide mockups. Scientific content comes from supplied sources and verified blueprints.

- Generate exactly one complete, front-facing 16:9 slide per image.
- Insert the mandatory per-call block from `references/image_generation_efficiency_rules.md` into every pilot, batch, retry, and continuation call.
- Supply the slide task, core message, family/variant, source-asset identity and geometry, readable evidence region, supported text, verified relationships, and approved visual references for the current slide.
- Preserve narrative purpose, source identity, evidence integrity, Template DNA, and readability.
- Use raster text to judge hierarchy, density, line length, and relative scale.
- Treat raster wording, font identity, and apparent point size as provisional.
- Reject and regenerate pages containing grids, unsupported scientific content, prohibited decoration, prohibited labels, unreadable evidence, stretched images, accidental gaps, or visual drift.
- Do not crop cells from a failed grid and treat them as approved samples.
- Do not continue to the next batch while a failed page remains.

The image model may select source-material dominance, composition direction, interpretation-zone placement, caption placement, page rhythm, and a compatible layout inside the assigned family/variant.

## Editable PPTX and typography constraints

The final PPTX must remain editable unless the user requests mockups only.

Keep these elements editable when practical:

- titles and body text;
- captions and source notes;
- page numbers and header/footer elements;
- lines, boxes, arrows, and callouts;
- source-verified simplified diagrams.

Insert source figures, tables, screenshots, and other evidence as image objects unless the user requests a verified redraw. Do not use a full-slide mockup image as the final slide background.

For typography:

- follow an explicit user font requirement;
- preserve the user-template font system when requested;
- otherwise use Microsoft YaHei for editable Chinese and mixed CJK/Latin text;
- use Times New Roman for independent English titles or journal names only when selected by the design;
- select weights from the template, approved mockups, content hierarchy, and rendered readability;
- allow all-bold, regular-weight, and mixed-weight systems when the hierarchy remains coherent;
- do not enforce universal point-size floors, role tables, or body-size delivery blockers;
- do not copy raster pixel size as a PowerPoint point size;
- do not use automatic shrinking as the default solution for crowding;
- resolve crowding through shortening, expanding text areas, removing minor elements, redistribution, layout revision, or slide splitting;
- render and verify font substitution, wrapping, clipping, density, weight, and hierarchy.

For new editable decks, use PptxGenJS 4.0.1 as the preferred writer. Use another writer when required for in-place preservation, complex masters, animations, charts, special objects, unavailable dependencies, or explicit user direction.

## Approval and continuation

Treat approval as authorization for the approved visual composition and system. Continue filtering unsupported scientific content, prohibited decoration, prohibited labels, and unreliable raster text during reconstruction.

- Planning-only work stops after the requested planning artifact.
- Route A stops after representative samples unless continuation is authorized.
- Route C stops after the pilot and after the complete independent mockup set unless uninterrupted completion is authorized.
- Approved-mockup expansion continues inside the locked visual system.
- Targeted repair stays within the affected scope unless the user requests broader redesign.

## QA and delivery

For editable PPTX creation, reconstruction, expansion, or revision:

1. Save the candidate PPTX.
2. Render every slide when a renderer is available.
3. Inspect the full montage and affected slides.
4. Compare against the selected template and approved mockups.
5. Check narrative coverage, planning coverage, hierarchy, repeated skeletons, clipping, evidence readability, image fit, internal workflow text, prohibited decoration, and source verification.
6. Fix identified problems.
7. Re-render after every fix.
8. Run deterministic static QA against the final file.
9. Verify delivery-blocking errors are zero for new decks and broad redesign. For localized or deck-wide mechanical revision, verify that no new delivery-blocking errors were introduced and none remain within the changed scope; disclose pre-existing errors outside that scope.
10. Verify the QA report hash matches the delivered PPTX bytes.

Read `references/comparative_montage_qa.md` before final delivery for new decks, approved-mockup expansion, broad redesign, and multi-slide visual-system changes. Read `references/pptx_qa_rules.md` before every editable PPTX delivery.

Deliver according to the active stage:

- Planning: production planning table and requested blueprint.
- Route A sample stage: representative independent full-slide mockups.
- Route C pilot stage: independent pilot mockups.
- Route C full-mockup stage: independent per-slide mockups and review montage.
- Editable work: final editable `.pptx`, preview montage when available, `qa-report.json`, and a concise QA note.

Mention fallback pages, missing high-resolution assets, unresolved source verification, skipped checks, and tool limitations. Keep the final response short and practical.
