# Existing PPTX Revision Rules

Use these rules for localized revision and deck-wide mechanical revision of an existing PPTX.

## Scope classification

Use localized revision when the request identifies specific slides, objects, text, figures, formatting, or layout defects.

Use deck-wide mechanical revision when the request defines a repeatable change that preserves narrative structure and slide composition, including:

- literal terminology replacement;
- font-family replacement;
- footer, page-number, or source-note normalization;
- correction of one repeated formatting defect;
- replacement of one recurring asset.

Use broad redesign instead when the request requires:

- narrative sequence or section structure;
- a newly designed or reinterpreted deck-wide visual system;
- template geometry or page-family logic;
- the role or message of many slides;
- the slide count through substantial expansion or restructuring.

Do not expand a localized or mechanical revision into broad redesign without user direction.

## Baseline inspection

- Preserve the input PPTX and write changes to a new output file unless the user explicitly requests overwrite.
- Record the slide count, slide order, canvas size, and target slide numbers before editing.
- Inspect the target slides and the objects affected by the request.
- Identify masters, layouts, themes, transitions, animations, charts, SmartArt, grouped objects, embedded media, hyperlinks, notes, external relationships, and special objects that may be affected.
- Render the target slides before editing when a renderer is available.
- Run baseline static QA before editing when available and record pre-existing errors and warnings.
- Establish the exact requested changes, permitted reflow, and protected content before editing.

## Change boundary

- Modify only the requested targets and the adjacent objects that require reflow to keep the affected slide valid.
- Preserve unrequested text, figures, data, notes, captions, sources, geometry, and object order.
- Preserve unaffected slides without reconstruction.
- Preserve slide count, slide order, canvas size, masters, layouts, themes, headers, footers, branding, notes, and special objects unless the user requests changes to them.
- Do not apply a local style correction to the full deck unless the user requests deck-wide normalization.
- Stop and request direction when a required change would alter the narrative structure, visual system, or protected content beyond the authorized scope.

## Edit method

- Prefer an in-place editing tool that preserves the existing PPTX structure and required PowerPoint features.
- Do not rebuild the full deck for a localized or mechanical revision.
- Modify an existing object when the requested result can be achieved without replacing the slide.
- Replace only the affected object when direct modification is unavailable or unsafe.
- Rebuild only the affected slide when object-level editing cannot produce the requested result.
- Preserve the affected slide's layout relationship, background, branding, headers, footers, z-order, grouping, transitions, animations, and notes when rebuilding is required.
- Stop and request direction before replacement when a protected feature cannot be preserved.
- Keep editable objects editable when practical.
- Do not flatten an affected slide into a full-slide image.
- Use `references/pptxgenjs_execution_rules.md` to select a writer when the current tool cannot preserve required features.

For deck-wide mechanical revision:

- enumerate matching objects before changing them;
- apply replacements only to the object types and text scopes named by the user;
- distinguish editable text from text baked into images;
- inspect exceptions instead of forcing a replacement into incompatible objects;
- preserve intentional local deviations unless the user requests complete normalization.

## Content and layout controls

- Use `references/evidence_asset_rules.md` when modifying scientific figures, tables, screenshots, diagrams, captions, or source notes.
- Preserve source identity, aspect ratio, axes, legends, units, scale bars, labels, and required context.
- Reject stretched images, accidental blank strips, thin exposed gaps, and visibly uneven padding.
- Use `references/cjk_typography_rules.md` when modifying fonts, weights, sizes, wrapping, or text-box geometry.
- Preserve the existing deck's typography system unless the user requests a replacement.
- Do not add unsupported scientific content, decorative icons, internal workflow labels, or new claims while repairing a slide.

## Verification

1. Save the revised PPTX as a new candidate file.
2. Confirm that the package opens and the slide count, order, and canvas size match the baseline unless the user requested changes.
3. Render every changed slide.
4. Compare each changed slide with its baseline and the requested result.
5. Inspect text wrapping, clipping, overlap, object bounds, image fit, figure readability, alignment, and z-order on changed slides.
6. Inspect neighboring slides when the change affects repeated components or visual continuity.
7. Inspect the final full-deck montage when a renderer is available.
8. Check that unrelated slides and protected features remain unchanged.
9. Run the applicable checks from `references/pptx_qa_rules.md` against the final PPTX.
10. Re-render and rerun QA after every correction.
11. Verify that no new delivery-blocking errors were introduced and none remain within the changed scope.
12. Disclose pre-existing errors outside the changed scope without modifying unrelated content.
13. Deliver only when the QA report matches the final PPTX.

Treat any unrequested visual or structural difference as a regression. Restore the baseline behavior. Stop and request direction before delivery when restoration is not possible.

## Delivery

- Deliver the revised editable PPTX.
- List the changed slide numbers and the completed changes.
- Report any replaced objects, rebuilt slides, lost or unsupported features, skipped checks, and tool limitations.
- Do not generate a production planning table, family/variant blueprint, or visual mockup unless the task expands into broad redesign.
