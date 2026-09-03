# Internal Route Selection

Do not expose route selection to the user unless requested.

Template handling and production route are independent decisions.

## Visual-reference handling

When a visual template/reference is used for a new deck or broad redesign, extract Template DNA as the visual-consistency layer before production planning.

If the user wants an editable PPTX to remain the same PPT system, also use source-deck continuation:

- reuse native Theme/Master/backgrounds and recurring editable visual assets;
- use Template DNA to keep newly designed elements visually consistent;
- do not use old scientific content-page layouts as default layout candidates.

If the user wants only a similar/reference style, or provides screenshots/non-editable references, use Template DNA without native source-deck continuation.

Strict geometry is a separate modifier. Preserve a source page layout only when the user explicitly asks for strict/in-place preservation or identifies a named page whose layout should be reused.

## Shared new-deck prefix

For new decks and broad redesigns with a visual reference:

narrative preset -> Template DNA -> evidence/source-asset analysis -> production planning table -> mockup family + variants blueprint.

For editable source-deck continuation, add native visual-asset inspection and reuse to that prefix; do not replace the prefix with old-page layout matching.

## Route A: representative visual samples

Use when the user asks for visual samples, mockups, style exploration, image-model output, `先做样板`, or `先看看效果`.

After the shared prefix:

- generate 1–2 representative full-slide samples first;
- use the assigned family and variant for each page;
- preserve native source visual assets when continuation is active;
- use Template DNA for any newly designed visual elements;
- stop for approval unless the user authorizes uninterrupted completion.

Route A does not imply that old template page layouts should be copied.

## Route B: direct editable PPTX

Use when the user asks for no image generation, direct editable PPTX, source-deck continuation, official-template compliance, fast production, or stable low-variation output.

After the shared prefix:

AI-selected layout archetypes -> visual-system application -> editable PPTX -> render -> QA -> revision.

- The new scientific sources determine the deck structure.
- scholar-ppt-cn determines content-slide body composition and establishes the deck's working layout families.
- Template DNA determines visual consistency.
- When source-deck continuation is active, native source assets are reused directly where possible.
- Old scientific content-page layouts do not participate by default, even when the source deck and new paper are from the same discipline.
- Cover, TOC, section-divider, and closing structures may remain when they are stable parts of the template identity and remain appropriate.
- A named old page layout may be reused only when the user explicitly requests it.

## Route C: full-deck per-slide image-model design

Use only when the user explicitly requests every slide to be designed by the image model before editable reconstruction.

Continue after the shared prefix with:

1–2 pilot pages -> approval -> one independent full-slide image for every slide in batches -> montage review -> editable reconstruction -> QA.

If source-deck continuation is active, preserve native visual identity and Template DNA during mockup/reconstruction. Do not use old scientific content-page layouts unless the user explicitly requests them.

The one-slide-per-image rule remains mandatory. Never generate a storyboard sheet, contact sheet, grid, or multi-slide overview as the source mockup set.
