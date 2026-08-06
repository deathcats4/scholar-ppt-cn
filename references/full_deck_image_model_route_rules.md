# Full-Deck Per-Slide Image-Model Route Rules

This is an optional high-cost route. It is never the default.

## Activation

Activate only after an explicit user request that every slide, the whole deck, or all remaining slides be designed by the image model before editable reconstruction.

Generic requests to finish the deck or expand from approved samples do not activate this route.

## Workflow

1. Finish the production planning table.
2. Finish the mockup family + variants blueprint and map every slide.
3. Generate 1-2 independent pilot slide mockups.
4. Obtain approval or a clearly stated instruction to continue without another stop.
5. Generate one separate full-slide image for every remaining planned slide, in batches of 2-3 by default. Re-inject the mandatory per-call constraint block from `image_generation_efficiency_rules.md` into every page or batch request; do not rely on the earlier route prompt or long conversation context.
6. After each batch, inspect every page separately. Reject and regenerate pages that contain multi-slide grids, invented scientific content, prohibited commercial icons, prohibited literature-report labels, illegible evidence regions, or visual drift. Do not continue to the next batch while a failed page remains.
7. Assemble a montage only from the already generated independent slide images.
8. Review the complete mockup set for narrative coverage, family/variant coverage, repetition, and cross-slide rhythm.
9. Reconstruct every slide with real project content and editable PPT objects.
10. Render and run final PPTX QA.

## Output format

Full-deck means one independent generated image per slide. It never means:

- one four-grid or nine-grid image;
- one contact sheet;
- one storyboard sheet;
- one presentation overview;
- several slide thumbnails in one image;
- several alternatives in one image.

Do not crop cells from a grid and treat them as individual mockups.

## Scientific and visual constraints

All rules in `mockup_exploration_rules.md`, `evidence_asset_rules.md`, and `visible_text_filter_rules.md` apply to every generated page.

The image model designs composition only. It must not invent mechanisms, data, evidence, or explanatory relationships, including “simple mechanism diagrams”. Use verified real evidence or neutral placeholders. If the source contains a mechanism figure, use the real source figure rather than asking the image model to redraw it.

## Approval scope

Approval of pilot pages or a full mockup set normally approves composition, hierarchy, image/text ratio, palette, alignment, whitespace, and page rhythm. It does not automatically approve commercial icons, emoji, decorative symbols, prohibited literature-report labels, model-created mechanism graphics, or scientific claims that cannot be traced to source material.

## Approval and continuation

By default, stop after the pilot and again after the full independent mockup set. Continue directly through editable reconstruction only when the user explicitly asks for uninterrupted completion.
