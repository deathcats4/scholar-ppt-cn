---
name: scholar-ppt-cn
description: >-
  Use this skill when a user wants to create, restyle, or rebuild a Chinese
  academic PowerPoint from papers, theses, reports, figures, notes, reference
  templates, screenshots, or visual mockups. This v3.4 release preserves the
  v3.3.1 production workflow: production planning table, mockup family +
  variants blueprint, image-model full-slide samples, an optional full-deck per-slide image-model
  design route, or template-direct editable PPTX, followed by approved-mockup
  reconstruction and montage QA. It adds stronger
  scientific-figure handling, role-based Chinese typography,
  v3.3.1-aligned body-size review policy, PptxGenJS as the
  default preferred new-deck writer, and deterministic final PPTX QA.
metadata:
  version: 3.4.0
  summary: v3.3.1 workflow with persistent per-call image-model constraints, restrained literature-report labels, editable-reconstruction icon filtering, and v3.4 scientific-figure, typography, PptxGenJS, and deterministic QA improvements.
---

# Scholar PPT CN Skill

## User-facing principle

Keep the user interface simple.

The user may say:

- "参考模板和材料，先做规划表。"
- "按规划表先做 5–8 页视觉样板，不要生成 PPT。"
- "整套每一页都先逐页生图，全部确认后再重建 PPTX。"
- "这几页样板确认，按这个风格扩展成完整可编辑 PPT。"
- "不要生图，直接参考模板生成可编辑 PPT。"
- "第 X 页图太小 / 字体不对 / 内容有误，修一下。"

Do not ask the user to understand internal route names, archetype names, or QA gates unless they ask.

## Bundled reference template

If the user does not provide a separate template and wants a ready visual reference, use `assets/templates/scholar-ppt-cn-reference-template.pptx` as the default academic PPT template. Treat it as a reference template for Template DNA extraction, layout rhythm, typography, color system, and reusable page structures.
Its example text sizes and font weights are not delivery requirements. Body font-size requirements follow v3.3.1: do not enforce a universal body-point floor.

## Runtime compatibility

Use whichever file, PPTX-writing, rendering, vision, image-generation, and inspection tools are available in the current environment.

When file and tool access is available, read the relevant source files, create output files on disk, render or inspect previews when possible, revise problems before delivery, and return file paths plus a short QA note.

When PPTX generation, rendering, or image inspection tools are unavailable, do not pretend those checks were performed. Provide the planning table, blueprint, prompts, or implementation instructions that are possible, and clearly say which QA steps still need to be performed after export.

## Main workflow

The default workflow is:

1. **Infer report type and narrative preset.**
2. **Extract Template DNA.**
3. **Build a production planning table.**
4. **Build a mockup family + variants blueprint.**
5. **Generate representative samples, a full set of independent per-slide mockups, or editable PPTX according to the selected route.**
6. **If mockups are approved, lock the visual system and reconstruct or expand as editable slides.**
7. **Render preview, QA, and revise.**

## Reference loading map

Load reference files as needed instead of relying only on this main file.

- For narrative selection, read `references/hidden_narrative_presets.md`.
- For production planning, read `references/production_planning_table_rules.md`, `references/evidence_index_rules.md`, `references/source_asset_geometry_rules.md`, and `references/fallback_layout_archetype_library.md`.
- For Template DNA extraction, read `references/template_dna_rules.md`.
- For mockup family + variants, read `references/mockup_family_variant_blueprint_rules.md`.
- For image-model sample pages, read `references/image_generation_efficiency_rules.md`, `references/mockup_exploration_rules.md`, `references/evidence_asset_rules.md`, and `references/visible_text_filter_rules.md`.
- For the optional full-deck per-slide image-model route, also read `references/full_deck_image_model_route_rules.md`.
- For editable PPTX construction, read `references/editable_reconstruction_rules.md`, `references/cjk_typography_rules.md`, `references/layout_repetition_control.md`, `references/evidence_asset_rules.md`, and `references/pptxgenjs_execution_rules.md`.
- For expansion from approved mockups, read `references/locked_visual_system_rules.md` and `references/mockup_derived_archetype_rules.md`.
- For final checking, read `references/comparative_montage_qa.md` and `references/pptx_qa_rules.md`.

## Production planning table

The production planning table is now the central pre-generation artifact.

It is not merely a content outline. It must connect:

- narrative order;
- slide task;
- source assets;
- source-asset geometry;
- core message;
- internal layout archetype;
- density;
- asset-handling instructions;
- risk/QA notes.

Required columns:

1. slide number;
2. slide title;
3. narrative section;
4. communication task;
5. source asset(s);
6. source-asset geometry;
7. core message;
8. selected layout archetype ID;
9. density level: low / medium / high;
10. asset handling: preserve / overview+detail / split / cross-slide / not-use / request-higher-resolution;
11. notes and risk: fact check, readability, translation, missing asset, etc.

The planning table may be shown to the user for confirmation. Keep it readable and concise. Do not overload it with implementation jargon.

## Mockup family + variants blueprint

After the production planning table and before generating images or PPTX, create a mockup family + variants blueprint.

This stage is the visual-system bridge between planning and generation.

It is not a final PPT and not an image-generation step. It defines reusable visual families and variant options so the deck is stable but not monotonous.

The blueprint must include:

1. **Template DNA reconfirmation**
   - 16:9 canvas;
   - page tone;
   - primary/accent colors;
   - background style;
   - title system;
   - header/footer/page-number behavior;
   - caption/source-note style;
   - card/border/ribbon/divider language;
   - figure/text ratio and page density;
   - typography policy.

2. **Mockup family summary table**
   - Family ID, such as MF-01;
   - family name;
   - applicable narrative sections;
   - applicable communication tasks;
   - applicable source-asset geometries;
   - mapped slide numbers;
   - visual keywords;
   - main risks.

3. **Variants for each family**
   - each family needs at least 3 variants;
   - high-frequency families need 4-6 variants;
   - each variant needs Variant ID, layout name, applicable source-asset geometry, structure, mapped slide numbers, suitable scenario, and forbidden misuse.

4. **Slide-to-family/variant mapping**
   - every planned slide must map to a family and recommended variant;
   - include backup variant and reason for choice;
   - include readability risks.

5. **Representative sample selection**
   - choose 5-8 slides that best test the system;
   - cover cover/report map, large evidence figure, multi-panel evidence, chart interpretation, mechanism/discussion, and conclusion when applicable.

This stage intentionally preserves the successful stability of earlier mockup-family workflows, while adding variants to prevent monotony.

Family is a visual system unit. Variant is a concrete layout option. Neither should be treated as a rigid stencil.


## Hidden narrative presets

Narrative presets control story order. They do not control page geometry.

### Literature report / journal club preset

Use when the user provides a paper/article or asks for 文献汇报, 文献精读, journal club, paper reading, or a paper-based group presentation.

Default narrative order:

1. Cover
2. Report map / overview
3. Background / introduction
4. Research gap / question
5. Objectives / contribution
6. Study area / materials / data / methods, as appropriate
7. Results / evidence chain
8. Discussion / mechanism / interpretation
9. Conclusions
10. Closing

Typical default scale:

- 10–15 min: about 14–18 slides;
- complex paper: around 18–24 slides;
- user-specified count overrides defaults.

### Thesis / defense preset

Use when the user provides a thesis/dissertation, thesis directory, abstract, defense draft, or asks for degree defense / 答辩.

Default narrative order:

1. Cover
2. Outline / agenda
3. Background and significance
4. Research status
5. Research gap / scientific or practical question
6. Objectives, contents, and contributions
7. Technical route / data / methods / workload, as appropriate
8. Main chapters or main results in source order
9. Integrated discussion / mechanism / system view
10. Conclusions and outlook
11. Acknowledgements / closing

### Research progress preset

Use for project progress meetings, group meetings, or recurring research updates that are not single-paper reports.

Default narrative order:

1. Cover
2. Progress overview
3. Research question / objective
4. Completed work
5. Key results
6. Current problems
7. Next steps
8. Discussion / help needed
9. Closing

### General topical presentation preset

Use for general course, topic, or professional presentations.

Default narrative order:

1. Cover
2. Context
3. Problem
4. Main content 1
5. Main content 2
6. Main content 3
7. Summary
8. Closing

### User structure override

If the user provides an explicit outline, table of contents, or preferred order, follow the user-provided structure over hidden presets.

## Template DNA

The reference/template deck teaches visual identity, not exact page geometry.

Extract:

- header / branding behavior;
- title hierarchy;
- footer and page number;
- palette;
- caption/source-note style;
- spacing rhythm;
- page density;
- source-material/text balance;
- component language;
- typography roles;
- border, divider, ribbon, card, and emphasis styles.

Default adherence: guided-creative.

Use strict adherence only if the user explicitly says the template is official or must be followed closely.

## Internal route selection

The route is chosen internally.

### Route A: plan -> image-model samples

Use when the user asks for visual samples, mockups, style directions, or wants to see the effect first.

Chain:

Production planning table -> mockup family + variants blueprint -> Template DNA -> image-model full-slide mockup variants -> user approval -> locked visual system -> mockup-derived archetypes -> editable reconstruction.

### Route B: plan -> template-direct editable PPTX

Use when the user asks to skip image generation, use a strict template, produce quickly, or directly generate editable PPTX.

Chain:

Production planning table -> mockup family + variants blueprint -> Template DNA -> detailed layout archetype library -> Template-DNA parameterization -> PptxGenJS editable PPTX -> QA.

Template DNA alone is not enough for Route B. The detailed layout archetype library must be used.

### Route C: plan -> full-deck per-slide image-model design -> editable reconstruction

Use only when the user explicitly asks for every slide, the whole deck, or all remaining slides to be designed by the image model before editable reconstruction.

Valid requests include:

- "整套 PPT 每一页都先用生图模型设计";
- "全稿逐页生成独立视觉稿，再重建成可编辑 PPT";
- "剩余页面也全部逐页生图，不要直接按样板扩展";
- "先完成全套独立 slide mockup，再制作 PPTX".

Do not activate Route C merely because the user says "完成全稿", "按样板扩展", or "做完整 PPT". Those requests remain Route A expansion unless the user explicitly requests image-model design for every page.

Chain:

Production planning table -> mockup family + variants blueprint -> 1-2 independent pilot mockups -> user approval -> independent full-slide mockup for every planned slide in batches -> full-deck mockup montage review -> locked visual system -> slide-by-slide editable reconstruction -> rendered QA.

Route C still obeys the one-slide-per-image rule. "Full-deck" means one separate generated image per slide, never one storyboard sheet, grid, contact sheet, or presentation overview generated by the image model.

## Image model role

The image model is the visual designer for full-slide mockups, not the author of scientific content.

Each mockup image must contain exactly one complete, front-facing 16:9 slide filling the canvas. Four-grid, nine-grid, contact-sheet, storyboard-sheet, presentation-overview, multi-thumbnail, multi-alternative, device-frame, gallery, or perspective outputs are invalid. Generate multiple requested pages as separate images or separate calls. A montage may be assembled only after independent full-slide mockups exist. Do not crop cells from a generated grid and treat them as approved samples.

It should follow the production planning table and mockup family + variants blueprint, but may make composition decisions inside the selected family/variant boundaries.

It may decide:

- source-material scale and dominance;
- composition direction;
- interpretation-zone placement;
- caption/source-note placement;
- visual rhythm;
- variation across mockups;
- when to use left-image/right-text, top-image/bottom-text, evidence wall, comparison, or open-space layouts.

It may adapt layout according to content. It may use left-image/right-text when that is genuinely the best solution. It must not use the same skeleton lazily for the whole deck.

The image model must not invent, complete, redraw, or simplify scientific mechanisms, reaction pathways, experimental workflows, causal arrows, quantitative trends, mineral or biological structures, or other scientific claims. This includes so-called “simple mechanism diagrams”. If the source already contains a mechanism figure, use the real source figure as an evidence asset; do not ask the image model to reinterpret or redraw it. A newly drawn editable mechanism diagram is allowed only after an explicit user request and verification of every node and relationship against the source material. Ordinary arrows remain allowed for reading order or source-supported relationships.

Default academic visual language should rely on real evidence, typography, alignment, whitespace, restrained rules, and source-supported arrows. Do not add commercial-infographic or training-course decoration such as light bulbs, books, document icons, people silhouettes, globes, eyes, targets, trophies, puzzle pieces, gears, check marks, exclamation badges, microscope silhouettes, laboratory-flask icons, hammers, emoji, cartoons, or 3D icons. This restriction applies even when similar decoration appeared in an earlier generated mockup.

For literature reports and journal-club decks, do not create presentation labels merely to fill the composition, including “读图要点”, “读图结论”, “关键认识”, “综合判断”, “支持证据”, “注意事项”, “证据观察”, “预期输出”, “本文切口”, “证据页 1/2”, or “基于论文证据的结构化归纳”. “核心问题” and “结论” remain valid academic headings. Express other supported content directly as normal academic statements.

Do not rely on earlier conversation context to preserve these constraints. The mandatory per-call constraint block in `references/image_generation_efficiency_rules.md` must be inserted into every image-generation call, including pilot pages, later batches, retries, and Route C continuation calls.

Raster mockup typography is only a visual approximation. Ask for a restrained modern Chinese sans-serif style visually close to Microsoft YaHei, without decorative, handwritten, outlined, shadowed, or artificially condensed lettering. Do not treat the apparent mockup text size as a real PowerPoint point size. Final editable reconstruction must set the actual font and readability policy.

Image-model text is provisional and must be checked before final delivery.

## Image generation efficiency

Full-slide academic mockups are expensive to generate. When using image generation, follow `references/image_generation_efficiency_rules.md`.

Default sample generation should be staged:

1. generate 1-2 pilot mockups first to test the visual system;
2. revise the prompt or blueprint if the pilot adds unwanted template labels, unreadable figure areas, repeated skeletons, or more than one slide inside one generated image;
3. continue in small batches of 2-3 pages;
4. stop between batches when user approval or a visual correction would save time.

Do not attempt 5-8 complex full-slide mockups in one uninterrupted generation step unless the user explicitly requests a long wait. If the user asks for many pages, split them into batches and tell the user the batch plan.

For visual-system approval, prefer fewer high-value representative pages over many redundant pages.

For Route C, approval of the pilot pages starts full-deck per-slide generation. Generate remaining slides as separate full-slide images in small batches. Re-inject the mandatory per-call constraint block for every page or batch, then check each generated page for scientific-content invention, prohibited commercial icons, prohibited literature-report labels, multi-slide grids, and visual drift. A failed page must be regenerated before the next batch. Do not silently switch from Route C to template-direct expansion.

## Locked visual system

Once the user approves mockups, enter locked visual system internally.

Approved mockups become the valid visual source for reconstruction and expansion. Approval normally covers composition, image/text proportion, hierarchy, palette, alignment, whitespace, and page rhythm. It does not automatically approve generic commercial icons, emoji, decorative symbols, prohibited literature-report labels, image-model-created mechanism graphics, or scientific content that cannot be traced to the source.

Expansion must preserve:

- header behavior;
- title hierarchy;
- typography rules;
- color palette;
- border and line style;
- emphasis style;
- source-material treatment;
- caption/source-note style;
- footer and page number;
- approximate density and whitespace rhythm.

Locked visual system is not a fixed stencil. New slides may adapt composition inside the approved system.

## Mockup-derived archetype library

When approved mockups exist, they override the built-in fallback layout library.

After approval, internally derive archetypes from approved mockups.

Each archetype should record:

- source approved mockup ID;
- communication purpose;
- fixed visual elements;
- adaptable elements;
- source-material region behavior;
- interpretation-region behavior;
- caption/source-note behavior;
- footer/page-number behavior;
- density range;
- suitable content types;
- forbidden misuse.

## Detailed layout archetype library

The internal detailed archetype library is used for:

- production planning table archetype selection;
- mockup family + variants construction;
- template-direct editable PPTX;
- fallback pages when no approved mockup exists.

It is not a user-facing list by default.

Select archetypes by matching:

- narrative section;
- slide task;
- source asset type;
- source-asset geometry;
- information density;
- neighboring slide rhythm;
- template constraints.

## Source-asset geometry matching

Before choosing an archetype, classify each primary source asset:

- wide figure;
- tall figure;
- square / near-square figure;
- dense multi-panel figure;
- photo / microscopy / image evidence;
- chart / graph;
- table;
- process / mechanism diagram;
- map / spatial figure;
- screenshot / UI / document excerpt;
- no primary source asset.

Do not force all evidence into a single left-image/right-text structure.

## Evidence index

Internally classify source materials before production planning.

Useful fields:

- asset ID / figure number / table number;
- source section;
- content summary;
- clarity;
- relevance to the narrative;
- main evidence / optional support / likely unused;
- whether a higher-resolution version is needed.

Main evidence assets should be clear and large enough for presentation. If a key source asset is unreadable, request a better version rather than hiding the issue.

## Visible text filter

Do not place internal workflow language into the final PPT, including Template DNA, production planning, archetype, mockup-derived, QA, route, prompt, or implementation labels.

For literature reports and journal-club decks, also omit editorial framing labels such as “读图要点”, “读图结论”, “关键认识”, “综合判断”, “支持证据”, “注意事项”, “证据观察”, “预期输出”, “本文切口”, “证据页 1/2”, and “基于论文证据的结构化归纳”. “核心问题” and “结论” remain allowed. Keep the supported content and write it directly without the extra label.

Do not expose model self-reference, placeholder instructions, or generic “提示：/注意：” wrappers unless a genuine source- or user-required warning exists. Follow `references/visible_text_filter_rules.md`.

## Editable reconstruction

The final PPTX should be editable.

Use editable objects for:

- titles;
- body text;
- captions;
- source notes;
- page numbers;
- footer/header elements;
- lines;
- boxes;
- arrows;
- callouts;
- verified diagrams explicitly supported by source material.

Insert source figures, tables, screenshots, and other evidence assets as image objects unless the user explicitly requests redrawing.

Editable reconstruction inherits the approved mockup's composition, hierarchy, palette, alignment, whitespace, and evidence placement. It must not copy prohibited commercial icons, emoji, decorative symbols, prohibited literature-report labels, or image-model-created scientific diagrams. This rule applies whether those elements appear as Unicode text, emoji, icon fonts, PowerPoint shapes, SVG, PNG, or cropped parts of the mockup.

Do not paste a full-slide mockup image as the final PPT slide background.

## CJK typography and projection readability

For decks containing editable Chinese text, follow `references/cjk_typography_rules.md`.

Default behavior when the user does not provide a conflicting official template:

- editable Chinese and mixed CJK/Latin text uses Microsoft YaHei / 微软雅黑;
- mixed Chinese/Latin text remains in Microsoft YaHei for stable baseline and wrapping;
- independent English titles or journal names may use Times New Roman when there is a design reason;
- cover titles, slide titles, section titles, key conclusions, and genuine emphasis may be bold;
- body text, captions, sources, page numbers, and auxiliary explanations normally use regular weight;
- do not make all Chinese text bold.

For body font size, follow v3.3.1 behavior: do not enforce a universal 16 pt floor, 18-20 pt target, or body-size delivery blocker. Use the template, approved mockups, content density, and rendered readability to choose body sizes. If body text looks too small, clipped, or crowded, report it as a readability issue and revise when it materially harms the presentation.

Avoid using shrink-to-fit, PptxGenJS `fit: "shrink"`, OOXML `<a:normAutofit>`, or another automatic size reduction as the default way to solve crowding. When text does not fit, prefer removing repetition, shortening wording, expanding the text area, reducing secondary elements, redistributing content, or splitting the slide. If automatic shrinking is inherited from a template or existing deck, disclose it as a readability review item rather than a deterministic delivery blocker.

## Scientific figure and evidence handling

Source materials are evidence assets. Follow `references/evidence_asset_rules.md`.

Default behavior:

- preserve scientific figures as image objects when fidelity matters;
- do not redraw or modify data with AI unless the user explicitly requests it;
- use the clearest available source;
- preserve original aspect ratio and full context;
- keep axes, legends, units, scale bars, panel labels, table headers, color bars, conditions, and explanatory notes visible;
- avoid decorative masks, white figure cards, rounded containers, shadows, and automatic highlight-region cropping;
- use `preserve`, `overview+detail`, `split`, `cross-slide`, `not-use`, or `request-higher-resolution` according to scientific readability;
- use only existing paper panels or user-provided detail images for `overview+detail` by default;
- only figures that were actually visually reviewed may receive position-based arrows, boxes, or annotations;
- do not create appendix slides as an automatic evidence-handling strategy.

When figures are too dense, prefer full-figure preservation, cross-slide explanation, existing independent panels, a higher-resolution request, or omission. Do not shrink many figures into unreadable thumbnails. High-risk splitting or replacement of core evidence must be confirmed or clearly disclosed.

## PPTX implementation

For new editable PPTX generation, default to PptxGenJS 4.0.1 as the preferred writer and follow `references/pptxgenjs_execution_rules.md`. PptxGenJS is the writer, not the designer.

The v3.3.1 design authority remains unchanged:

- Template DNA controls visual identity;
- the detailed layout archetype library and mockup family variants control page structure;
- approved mockups override fallback layouts.

Do not choose left-image/right-text, three cards, fixed columns, white figure plates, or identical title/content skeletons merely because they are easy to code. Keep titles, body text, captions, sources, page numbers, simple shapes, lines, arrows, and callouts editable. Do not flatten a full slide into an image and call it editable.

Use another tool when PptxGenJS is unavailable or when in-place preservation of a complex existing PPTX is better served by another writer. The default fallback is python-pptx.

## Layout repetition control

For direct editable generation and long-deck expansion:

- do not use the same visible skeleton for more than two consecutive content slides unless the source material requires it;
- if one slide task appears many times, rotate among compatible archetypes;
- preserve visual identity through Template DNA, not by repeating one geometry;
- allow left-image/right-text when appropriate, but treat repeated lazy use as a QA failure.

## Comparative montage QA

For expanded decks, QA must compare:

- approved mockup overview when samples exist;
- expanded PPT preview overview.

For direct editable generation, inspect the full preview montage.

Check:

- title hierarchy consistency;
- header/footer/page-number consistency;
- source-material placement logic;
- caption/source-note consistency;
- color and border consistency;
- density similarity;
- typography compliance;
- repeated skeletons;
- sudden new visual language;
- text overflow or clipping;
- source asset readability;
- narrative preset coverage;
- planning table coverage.

If the deck no longer reads as one visual system, revise before delivery.

## PPTX QA

When file and rendering tools are available, follow `references/pptx_qa_rules.md`.

Minimum PPTX delivery contract for editable PPTX tasks:

1. create the editable `.pptx` as a real file;
2. render all slides and inspect a montage when a renderer is available;
3. check template/mockup consistency, repeated skeletons, text overflow, scientific figure readability, and internal workflow text;
4. run deterministic static QA against the final PPTX;
5. treat body text size, body auto-shrink, and very dense text as readability review items rather than deterministic delivery blockers;
6. revise, re-render, and rerun QA after any fix;
7. verify that the QA report hash matches the delivered PPTX bytes.

Bundled commands include:

```text
python scripts/preflight.py --output preflight.json
python scripts/render_preview.py deck.pptx --output-dir previews --montage montage.png
python scripts/qa_pptx.py deck.pptx --profile group-meeting --report qa-report.json
python scripts/export_qa_note.py qa-report.json qa-note.md
python scripts/verify_final_qa.py deck.pptx qa-report.json --require-profile group-meeting
```

If a check cannot run because a required renderer or dependency is unavailable, state that limitation and perform the strongest available substitute.

## Delivery

For planning stage, deliver the production planning table. Then deliver the mockup family + variants blueprint before generating images or PPTX.

For Route A sample stage, deliver the representative full-slide mockup images and stop.

For Route C mockup stage, deliver the independent full-slide mockup set plus a review montage and stop for approval before editable reconstruction, unless the user explicitly authorized uninterrupted completion.

For direct editable PPTX or reconstructed/expanded editable PPTX, deliver:

- editable `.pptx`;
- preview montage when rendering is available;
- `qa-report.json`;
- brief QA note;
- mention any fallback pages, missing high-resolution assets, skipped checks, or content that needs source verification.

Keep the final response short and practical.
