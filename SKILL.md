---
name: scholar-ppt-cn
description: Use this skill when a user wants to create, restyle, or rebuild a Chinese academic PowerPoint from papers, theses, reports, figures, notes, reference templates, screenshots, or visual mockups. The workflow keeps the user interface simple while restoring useful planning. First create a production planning table that maps each slide to narrative section, source asset, source-asset geometry, core message, and detailed layout archetype. Then create a mockup family + variants blueprint that groups planned slides into reusable visual families and assigns concrete variants. Visual samples and editable PPTX are generated only after this family blueprint is established. Template DNA controls visual identity; layout archetypes and mockup family variants control page structure; approved mockups override fallback layouts.
metadata:
  version: 3.3.0-productized-planned-family
  summary: Chinese academic PPT workflow with production planning plus a mockup-family-and-variants stage before generating visual samples or editable PPTX.
---

# Scholar PPT CN Skill

## User-facing principle

Keep the user interface simple.

The user may say:

- "参考模板和材料，先做规划表。"
- "按规划表先做 5–8 页视觉样板，不要生成 PPT。"
- "这几页样板确认，按这个风格扩展成完整可编辑 PPT。"
- "不要生图，直接参考模板生成可编辑 PPT。"
- "第 X 页图太小 / 字体不对 / 内容有误，修一下。"

Do not ask the user to understand internal route names, archetype names, or QA gates unless they ask.

## Main workflow

The default workflow is:

1. **Infer report type and narrative preset.**
2. **Extract Template DNA.**
3. **Build a production planning table.**
4. **Build a mockup family + variants blueprint.**
5. **Generate visual samples or editable PPTX according to the user request.**
6. **If samples are approved, lock the visual system and expand from approved mockups.**
7. **Render preview, QA, and revise.**

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
10. asset handling: preserve / overview+detail / split / request higher resolution;
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

Production planning table -> mockup family + variants blueprint -> Template DNA -> detailed layout archetype library -> Template-DNA parameterization -> editable PPTX -> QA.

Template DNA alone is not enough for Route B. The detailed layout archetype library must be used.

## Image model role

The image model is the visual designer for full-slide mockups.

It should follow the production planning table and mockup family + variants blueprint, but may make composition decisions inside the selected family/variant boundaries.

It may decide:

- source-material scale and dominance;
- composition direction;
- interpretation-zone placement;
- caption/source-note placement;
- visual rhythm;
- variation across mockups;
- when to use left-image/right-text, top-image/bottom-text, central model, evidence wall, comparison, or open-space layouts.

It may adapt layout according to content. It may use left-image/right-text when that is genuinely the best solution. It must not use the same skeleton lazily for the whole deck.

Image-model text is provisional and must be checked before final delivery.

## Locked visual system

Once the user approves mockups, enter locked visual system internally.

Approved mockups become the valid visual source for reconstruction and expansion.

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

Do not place internal workflow language into the final PPT.

Avoid visible slide text such as:

- template DNA;
- minimal brief;
- archetype;
- inheritance map;
- mockup-derived;
- production planning table;
- production note;
- speaker note;
- this slide is for;
- design suggestion;
- QA note;
- page task;
- source gap;
- internal route;
- internal file or workflow label.

If an internal idea must appear, rewrite it as normal presentation content.

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
- simple diagrams.

Insert source figures, tables, screenshots, and other evidence assets as image objects unless the user explicitly requests redrawing.

Do not paste a full-slide mockup image as the final PPT slide background.

## CJK typography hard rule

For decks containing editable Chinese text:

- every editable run containing CJK characters must use Microsoft YaHei / 微软雅黑;
- every editable run containing CJK characters must be set to 加粗 / bold;
- English, numbers, units, and formulas default to Arial when separated into their own runs;
- text inside source images is not modified.

Correct implementation means:

- font family = Microsoft YaHei / 微软雅黑;
- bold = true / 加粗开启.

Do not treat "Microsoft YaHei Bold" as a separate font name.

This rule outranks template-extracted regular body text.

## Evidence asset rules

Source materials are evidence assets.

Default:

- preserve as image objects when fidelity matters;
- no AI redraw unless requested;
- no content modification;
- no cropping of essential labels, axes, legends, scale bars, panel labels, table headers, or explanatory notes;
- use high-resolution originals when available;
- if a key source asset is unreadable, request a better file instead of hiding the problem;
- use overview + detail zoom when a dense figure must be explained on a presentation slide.

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

## Delivery

For planning stage, deliver the production planning table. Then deliver the mockup family + variants blueprint before generating images or PPTX.

For sample stage, deliver full-slide mockup images and stop.

For direct editable PPTX or expanded editable PPTX, deliver:

- editable `.pptx`;
- preview montage;
- brief QA note;
- mention any fallback pages, missing high-resolution assets, or content that needs source verification.

Keep the final response short and practical.
