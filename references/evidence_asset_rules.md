# Scientific Figure and Evidence Rules

## Select Before Layout

Not every source-paper figure belongs in the deck. Every figure must answer a clear presentation question. Evidence that does not advance the argument should be removed or left unused.

## Preserve Full Context by Default

Scientific figures default to:

- use the clearest available source image;
- preserve original aspect ratio and context;
- sit directly on the slide without extra borders, outlines, cards, white plates, rounded containers, or shadows;
- keep axes, legends, units, scale bars, panel labels, table headers, and explanatory context visible;
- avoid decorative masks;
- distinguish multiple figures through whitespace, alignment, numbering, and concise captions instead of putting every figure in a frame;
- avoid automatic "highlight region" cropping.

Multi-panel figures, dense image grids, dense charts, long tables, and mechanisms may require panel-level explanation, cross-slide explanation, or `overview+detail`. When using derived assets or existing detail images:

- record the handling mode and rationale in the slide plan or work record;
- do not obscure axes, legends, units, scale bars, panel labels, table headers, color bars, sample or variable abbreviations, experimental conditions, or explanatory context;
- label the slide caption clearly, such as `Fig. 2A`, `Fig. 5A-B`, or "Fig. 5 shown across multiple slides";
- keep original figure paths, derived asset paths, user-provided detail paths, and review status in `project.json` or the work record.

High-risk splitting, cross-slide explanation, or replacement of core evidence must be confirmed or clearly disclosed. Derived assets must not silently replace original evidence.

A source-grounded simplified mechanism diagram may accompany an original mechanism figure or source-supported text when it improves explanation. Keep every node and relationship traceable, preserve the original evidence, and label cross-source synthesis, inference, or a proposed hypothesis before asking the user to confirm it.

Do not treat local crops generated from a full figure as a default capability. If a full figure is dense or poorly proportioned, prefer full preservation, cross-slide explanation, existing independent panels, higher-resolution requests or omission.

## When There Are Too Many or Too-Small Figures

Use this order:

1. remove unnecessary figures;
2. reduce explanatory structure;
3. enlarge the key figure;
4. split different evidence across slides;
5. use `overview+detail`, `split`, or `cross-slide` for dense but core figures;
6. omit secondary evidence that does not justify a readable slide.

Do not shrink many figures into unreadable thumbnails merely to show that the source paper contains them.

## Use Only Necessary Scientific Annotations

Do not add reading tutorials beside figures, such as instructions about where to look or what a color means. The slide should become clear through composition and evidence selection.

Add short annotations only when they clarify scientific objects or relationships, such as sample groups, reaction directions, key stages, or statistical intervals. Annotations must come from actual visual review, not guesses from titles or captions. They must not obscure data or invent trends absent from the source.

## Visual Review Status

Before using a figure, record the inspection status:

- `vision-reviewed`: opened and visually inspected;
- `metadata-reviewed`: only dimensions, page number, or metadata reviewed;
- `caption-inferred`: inferred only from caption;
- `user-described`: based on the user's description;
- `not-reviewed`: not yet inspected.

Only `vision-reviewed` figures can receive annotations based on internal position or visual structure.


## Handling Modes

Use these values in the production planning table:

- `preserve`: keep the full figure.
- `overview+detail`: keep a full overview and pair it with an existing paper panel or user-provided detail.
- `split`: explain independent panels separately while preserving labels and context.
- `cross-slide`: spread one complex core figure across multiple main-deck slides.
- `not-use`: omit evidence that is irrelevant, unreadable, duplicative, or misleading.
- `request-higher-resolution`: request a clearer source when a key figure cannot be presented faithfully.

Do not create appendix slides as an automatic evidence-handling strategy. If content cannot justify a readable main-deck slide, omit it or ask the user whether the narrative should be expanded.
