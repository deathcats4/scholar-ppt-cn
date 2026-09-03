# PptxGenJS Execution Rules

## Tool Choice

Use PptxGenJS as the default preferred writer when creating a new editable PPTX from papers, reports, figures, or slide plans.

Use another tool when:

- Node.js or PptxGenJS is unavailable;
- the task requires in-place modification of an existing PPTX and another tool better preserves masters, animations, complex charts, or special objects;
- the user provides a complex PowerPoint template and asks for high-fidelity continuation;
- the user explicitly specifies another tool;
- the required feature cannot be implemented reliably with PptxGenJS.

When PptxGenJS is unavailable, the default fallback is python-pptx.

## Separate Executor and Designer

Use PptxGenJS to create PowerPoint objects and save the PPTX. Select the design from the production plan, Template DNA, family/variant mapping, and approved mockups.

Select page structures from the research question, communication task, evidence relationships, figure geometry, production plan, family/variant mapping, and approved mockups. Use Template DNA to style those structures, not to supply full-page geometry. Rotate compatible structures across the deck. Route B may use the user template or bundled reference template for canvas, visual identity, theme, recurring decoration, and reusable micro-components; use native full-slide layouts only when the user explicitly requests original-layout preservation. Route A may use approved generated full-slide mockups and user-provided references.

## Default Generation Conventions

- Default canvas is 16:9 unless a user template or explicit user requirement says otherwise.
- Editable Chinese and mixed CJK/Latin text uses `Microsoft YaHei`.
- Select font weights from the user template, Template DNA, approved mockups, content hierarchy, and rendered readability.
- All-bold, regular-weight, and mixed-weight systems are allowed when they form a coherent hierarchy.
- Cards, borders, rounded containers, gradients, and shadows may follow the selected visual system.
- Preserve image aspect ratio and required scientific context.
- Fit images with deliberate alignment, coordinated backgrounds, and balanced padding.
- Reject stretched images, accidental blank strips, thin exposed gaps, and visibly uneven padding.
- Resize the container or revise the layout when an evidence image does not fit cleanly.
- Slide titles, explanations, lines, color blocks, ordinary reading arrows, and source-verified diagrams should remain editable when practical.
- Do not flatten a whole slide into an image and call it editable.
- Do not recreate commercial-course icons or emoji with Unicode text, icon fonts, basic shapes, SVG, or PNG.
- Rebuild source-grounded mechanism diagrams from a verified blueprint; do not trust raster labels or add unsupported nodes and arrows. Preserve a source mechanism figure as evidence when one exists, while allowing a traceable simplified editable explanation to accompany it.
- For literature reports, do not insert the prohibited editorial labels defined in `visible_text_filter_rules.md`.

Define font constants centrally in generator code. Select page geometry from the production plan and visual system:

```js
const FONT_CN = "Microsoft YaHei";
const FONT_LATIN = "Times New Roman";
```

Use font constants consistently. Select size and weight from the text hierarchy and rendered layout.

## Text Sizing

Do not enforce universal point-size floors or role tables. Choose sizes from the user template, approved mockups, content density, and rendered readability.

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

Complete the required rendering and QA steps after every generated file.
