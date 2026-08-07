# PptxGenJS Execution Rules

## Tool Choice

Use PptxGenJS as the default preferred writer when creating a new editable PPTX from papers, reports, figures, or slide plans.

Default does not mean mandatory. Use another tool when:

- Node.js or PptxGenJS is unavailable;
- the task requires in-place modification of an existing PPTX and another tool better preserves masters, animations, complex charts, or special objects;
- the user provides a complex PowerPoint template and asks for high-fidelity continuation;
- the user explicitly specifies another tool;
- the required feature cannot be implemented reliably with PptxGenJS.

When PptxGenJS is unavailable, the default fallback is python-pptx.

## Separate Executor and Designer

PptxGenJS creates PowerPoint objects and saves the PPTX. It does not decide slide design.

Do not default to these patterns merely because they are easy to code:

- left image and right text;
- three cards;
- white figure plates;
- identical title/content skeletons on every slide;
- fixed column widths or fixed-coordinate templates.

First understand the research question, evidence relationships, figure geometry, and selected v3.3.1 production route. Then implement the chosen design with PptxGenJS. Route B may use the user template, bundled reference template, and Template DNA. Route A may use approved generated full-slide mockups and user-provided references.

## Default Generation Conventions

- Default canvas is 16:9 unless a user template or explicit user requirement says otherwise.
- Editable Chinese and mixed CJK/Latin text uses `Microsoft YaHei`.
- Slide titles, section titles, key conclusions, and necessary emphasis use `bold: true`.
- Body, captions, sources, and page numbers use regular weight.
- Scientific figures are placed proportionally and normally receive no outer border, outline, white card, or shadow.
- Images must not be stretched to fill a slot.
- Slide titles, explanations, lines, color blocks, ordinary reading arrows, and source-verified diagrams should remain editable when practical.
- Do not flatten a whole slide into an image and call it editable.
- Do not recreate commercial-course icons or emoji with Unicode text, icon fonts, basic shapes, SVG, or PNG.
- Rebuild source-grounded mechanism diagrams from a verified blueprint; do not trust raster labels or add unsupported nodes and arrows. Preserve a source mechanism figure as evidence when one exists, while allowing a traceable simplified editable explanation to accompany it.
- For literature reports, do not insert the prohibited editorial labels defined in `visible_text_filter_rules.md`.

Define font constants centrally in generator code, but do not create a fixed page-geometry template:

```js
const FONT_CN = "Microsoft YaHei";
const FONT_LATIN = "Times New Roman";
```

Font constants ensure consistency; they do not imply identical size or weight.

## Text Sizing

Font-size requirements follow v3.3.1 behavior: do not enforce universal point-size floors or role tables. Choose sizes from the user template, approved mockups, content density, and rendered readability.

For mockup-approved routes, treat the raster mockup as a relative visual target:

- match title/body/caption/source-note hierarchy by proportion and page rhythm;
- avoid copying apparent pixel text as exact PowerPoint point sizes;
- render the editable PPTX and adjust sizes until the visual scale matches the approved mockup;
- prefer changing text amount, box geometry, or slide split before shrinking text away from the approved hierarchy.

Avoid using automatic shrinking as the default solution for body text, research judgments, explanations, and main lists:

- PptxGenJS `fit: "shrink"`;
- OOXML `<a:normAutofit>`;
- any automatic size reduction used to fit text.

When content does not fit, remove repetition, shorten sentences, reduce minor labels, expand the text area, reduce secondary images or labels, redistribute content, split the slide, or remove non-core content.

Recommended guarded helper pattern:

```js
function addBodyText(slide, text, options) {
  if (!options?.fontSize) {
    throw new Error("fontSize must come from the selected template/mockup layout.");
  }
  slide.addText(text, {
    ...options,
    objectName: options.objectName ?? "BODY_text",
    fontFace: "Microsoft YaHei",
    color: options.color ?? "222222",
  });
}
```

Body text should not bypass shared helpers when a deck has a defined typography system. `spAutoFit` is acceptable only when the rendered result still matches the approved hierarchy, does not clip, does not cross slide bounds, and does not overlap other objects.

## Required Post-Generation Steps

1. Save the PPTX.
2. Render all slides when a renderer is available.
3. Inspect the full montage.
4. Fix specific failing slides.
5. Re-render the final PPTX.
6. Run static QA against the final file with the scenario-appropriate profile.
7. Review rendered text scale against the approved mockup or template hierarchy; revise clipped, overcrowded, or out-of-scale slides.
8. Re-render and rerun QA after any fix.
9. Verify `error = 0` and the QA report hash matches the delivered file.

Successful PptxGenJS execution only proves that a file was generated. It does not prove that the slides passed visual review.
