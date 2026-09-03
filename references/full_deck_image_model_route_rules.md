# Full-Deck Per-Slide Image-Model Route Rules

Activate this high-cost route only for an explicit user request for per-slide image-model design across the whole deck.

## Activation

Activate only after an explicit user request that every slide, the whole deck, or all remaining slides be designed by the image model before editable reconstruction.

Generic requests to finish the deck or expand from approved samples do not activate this route.

## Workflow

1. Infer the report type and narrative preset, while preserving any user-provided structure.
2. Extract Template DNA from the user template or selected reference template.
3. Finish the production planning table.
4. Finish the mockup family + variants blueprint and map every slide.
5. Generate 1-2 independent pilot slide mockups.
6. Obtain approval or a clearly stated instruction to continue without another stop.
7. Generate one separate full-slide image for every remaining planned slide, in batches of 2-3 by default. Insert the mandatory per-call constraint block from `image_generation_efficiency_rules.md` into every page or batch request.
8. After each batch, inspect every page separately. Reject and regenerate pages that contain multi-slide grids, invented scientific content, prohibited commercial icons, prohibited literature-report labels, illegible evidence regions, or visual drift. Do not continue to the next batch while a failed page remains.
9. Assemble a montage only from the already generated independent slide images.
10. Review the complete mockup set for narrative coverage, family/variant coverage, repetition, and cross-slide rhythm.
11. Reconstruct every slide with real project content and editable PPT objects.
12. Render and run final PPTX QA.

## Output format

Generate one independent image per slide. Reject:

- one four-grid or nine-grid image;
- one contact sheet;
- one storyboard sheet;
- one presentation overview;
- several slide thumbnails in one image;
- several alternatives in one image.

Do not crop cells from a grid and treat them as individual mockups.

## Scientific and visual constraints

All rules in `mockup_exploration_rules.md`, `evidence_asset_rules.md`, and `visible_text_filter_rules.md` apply to every generated page.

The image model may design composition and visualize a supplied source-grounded mechanism blueprint. It must not invent or alter mechanisms, data, evidence, or explanatory relationships. Use verified real evidence or neutral placeholders. If the source contains a mechanism figure, preserve it as evidence; a traceable simplified explanation may accompany it. Clearly label cross-source synthesis, inference, or a proposed hypothesis and obtain user confirmation before final delivery.

## Approval scope

Lock composition, hierarchy, image/text ratio, palette, alignment, whitespace, and page rhythm from the approved pilot pages or full mockup set. Exclude commercial icons, emoji, decorative symbols, prohibited literature-report labels, and scientific claims that cannot be traced to source material. Verify mechanism graphics against the supplied blueprint before reconstruction.

## Approval and continuation

By default, stop after the pilot and again after the full independent mockup set. Continue directly through editable reconstruction only when the user explicitly asks for uninterrupted completion.
