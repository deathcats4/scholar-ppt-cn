# Source PPTX Continuation Rules

Use these rules when the user wants a new or expanded academic deck to remain visibly inside the same editable PPTX system rather than merely resemble it.

## Separation of authority

Keep three responsibilities separate:

- The new paper, report, thesis, figures, and user brief determine the scientific narrative, section structure, claims, and evidence.
- The scholar-ppt-cn planning and layout logic determines body composition from the communication task, evidence relationships, source-asset geometry, information density, and deck rhythm.
- The source PPTX and its extracted Template DNA determine the visual identity: canvas, theme where useful, backgrounds, exact colors, fonts, recurring decoration, title treatment, section marks, footer/page-number styling, and other reusable visual assets.

Do not let the source deck's old table of contents, research topic, slide sequence, result-page layout, discussion-page layout, data-page layout, microscopy layout, body-text geometry, image count, image slots, or page-specific arrangements determine the new deck unless the user explicitly asks to preserve or reuse a named page layout.

This remains true when the source deck and the new material are from the same academic discipline. Discipline similarity may help with terminology, familiar visual components, and evidence presentation conventions, but it does not authorize copying the old scientific structure or body layouts.

## Use Template DNA and native assets together

Extract Template DNA from the source PPTX to capture the visual system used for both reused and newly designed slides.

Also inspect and reuse native editable assets whenever possible:

- Theme, Slide Master, Layout, and background relationships that carry visual identity;
- recurring title treatments;
- fixed lines, bars, blocks, logos, section marks, and page numbers;
- recurring background shapes or images;
- exact font families, weights, and colors;
- footer/header treatments;
- reusable separators, labels, caption styling, and small decorative components.

Do not reduce an editable source deck to a generic summary such as `blue academic` when its real visual assets are available. Do not redraw a recognizable source visual asset merely to approximate it when it can be reused directly.

Template DNA is still required because new content layouts may need new shapes or components that do not exist as ready-made source objects. Those new elements should be designed by scholar-ppt-cn and styled consistently with the extracted DNA.

## Decks without a meaningful custom master

A personal or manually assembled PPTX may place most of its visual identity on ordinary slides rather than in Slide Master. An empty or generic master does not mean the deck has no reusable visual system.

Inspect representative slides across the deck and identify recurring identity-bearing objects. Build a reusable visual shell from these stable assets without treating the old scientific body layout as the template.

Cloning a source slide is allowed as a technical extraction method, but do not keep its old body geometry merely because cloning was convenient.

## Source text and stable template wording

Do not apply a blanket rule that every source string must be deleted.

Preserve or reuse text that remains naturally valid after the research topic changes, including stable template wording or page-role text such as:

- institutional or brand identity;
- `Part.01`-style section markers when they are part of the deck identity;
- generic section labels such as `目录`, `总结`, or `谢谢` when appropriate to the new deck;
- closing phrases such as requests for comments when they naturally belong to the source template;
- date fields as formatting structures, with the date updated when needed;
- fixed header/footer wording that is genuinely part of the template;
- attribution/license text that must remain.

Replace text that belongs specifically to the old research project, including:

- old project titles and topic-specific section wording;
- old authors or team names unless the user asks to retain them;
- old body text, hypotheses, results, discussion claims, and conclusions;
- old sample IDs, method combinations, and topic-specific labels when they do not apply;
- old figure captions, source citations, literature references, and topic-specific annotations.

A useful test is: if the research topic changed, would this wording still naturally belong in the same presentation system? If yes, it may be retained or updated. If not, replace it.

Do not expose workflow provenance such as `视觉底稿`, `source deck`, `user-supplied reference PPT`, Template DNA notes, route names, or production commentary as visible slide text merely to document how the deck was generated.

## Scientific structure and autonomous body layout

Plan the new deck from the new sources before assigning body layouts. Use the narrative preset, evidence index, production planning table, and family/variant blueprint.

For each new content slide:

1. determine the scientific communication task and core message;
2. identify the actual evidence assets and their geometry;
3. let scholar-ppt-cn select or design the body layout from the new content requirements;
4. apply the source deck's visual identity through native assets and Template DNA;
5. insert the new content and evidence.

By default, do not inspect old result, discussion, data, microscopy, or other scientific content pages for layout ideas. The layout engine should retain its autonomy.

If the user explicitly says that a named source page should be used as the layout reference, or asks for in-place replacement, that page geometry may be reused for the specified scope.

Stable non-content frame pages such as cover, table of contents, section-divider, and closing pages may retain their source structure when it remains naturally applicable because these pages can be part of the template identity rather than old scientific evidence layout.

Do not preserve empty image slots or old body structures when the new content does not require them. If the new slide contains one large scientific figure, give it the area required by the evidence. If it contains multiple microscopy panels, design an appropriate multi-panel evidence page even when the old source deck used a different structure.

## Strict preservation

Apply exact source-page structure, object positions, or in-place replacement only when the user explicitly requests strict layout preservation, original object positions, or direct replacement inside named source slides.

Strict geometry does not authorize carrying unrelated old research content into the new deck.

## Verification

Before delivery:

1. Render the final deck and compare it visually with the source deck.
2. Verify that recognizable native visual assets remain native rather than approximately redrawn when reuse was possible.
3. Verify that new slides follow the extracted visual DNA even when their body layouts were newly designed.
4. Verify that the new scientific structure is traceable to the new source material rather than the old source-deck section sequence.
5. Check that old project-specific text, figures, captions, citations, data, conclusions, and workflow provenance did not leak into the new deck.
6. Check that stable template wording retained from the source still makes sense in the new presentation.
7. Check that newly inserted scientific evidence remains readable and undistorted.
8. Reject stranded text, missing evidence areas, empty inherited image slots, or old body geometry that does not fit the new content.
9. Confirm that the result looks like the same PPT visual system while preserving AI autonomy over scientific body layouts.
10. Run the applicable PPTX QA checks and revise delivery-blocking defects.
