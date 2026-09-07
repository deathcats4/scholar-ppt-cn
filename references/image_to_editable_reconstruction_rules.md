# Image-to-Editable PPTX Reconstruction

Use this reference when the input is a flattened slide image rather than an editable source deck. Typical inputs include PPT screenshots, PNG/JPG pages, rendered PDF pages, AI-generated slide mockups, web captures, and completed designs whose source PPTX is unavailable.

The objective is **meaningful editability**: recover the page structure that a person will actually need to maintain while preserving visual fidelity and semantic integrity. Do not equate a larger PowerPoint object count with a better reconstruction.

If an editable source PPTX is available and the user wants to continue that deck, use source-deck continuation instead. Do not reverse-engineer a screenshot when the native source is authoritative.

## Authority and boundaries

Use each input for the authority it can reliably provide:

- The reference image is authoritative for page proportion, composition, hierarchy, geometry, alignment, color relationships, whitespace, crop, and visual rhythm.
- User-provided text, source documents, original figures, data, SVG/PDF assets, logos, and brand rules are authoritative for content and factual meaning.
- Raster text in a screenshot or AI-generated mockup is provisional. Use OCR or visual reading as an aid, then verify it against the supplied content. Do not reproduce obvious AI text artifacts.
- A complete source figure is an evidence asset, not an invitation to invent a new chart or mechanism. Follow `evidence_asset_rules.md` and the scientific-content constraints in `SKILL.md`.
- When the source is too small or unreadable to recover a fact, preserve the visual asset or request a higher-resolution source. Do not guess.

The image-reconstruction path may be used for one slide or a full set. For a new deck or multi-slide production, use the production-path summary before the PPTX write. A named single-slide repair may remain within the localized revision boundary when it does not expand into redesign.

## Reconstruction workflow

Follow this sequence before claiming that an image has been converted:

1. **Inspect the whole page.** Determine canvas ratio, background, outer margins, title zone, content regions, columns, alignment axes, reading order, visual center, and foreground/background order. Do not begin with mechanical OCR or pixel tracing.
2. **Inventory the objects.** Classify every visible region as a page-level element, atomic visual asset, structured editable object, or source-dependent object. Record its bounding box, z-order, role, source, and confidence.
3. **Assign editability policy.** Use the default SMART policy unless the user clearly requests another boundary. Policies may differ on the same slide.
4. **Recover content from the best source.** Use supplied wording and data as truth. Use the image to determine placement, scale, hierarchy, line count, and visual treatment.
5. **Build a reconstruction blueprint.** Resolve object geometry and style before writing the PPTX. A useful internal representation is:

   ```json
   {
     "slide": {"width": 13.333, "height": 7.5, "unit": "in"},
     "elements": [
       {
         "id": "title-1",
         "kind": "text",
         "bbox": [0.72, 0.42, 7.4, 0.48],
         "z": 20,
         "policy": "smart",
         "source": "user-text",
         "confidence": 0.96,
         "style": {"fontFace": "Microsoft YaHei", "fontSize": 24}
       }
     ]
   }
   ```

   Coordinates should be stable slide coordinates, not an accumulation of image-pixel guesses. When starting from pixels, map them proportionally: `x = x_px / image_width * slide_width`, and likewise for `y`, `width`, and `height`.
6. **Rebuild native objects.** Use PptxGenJS 4.0.1 for new decks, or the writer required by source-deck continuation. Keep page-level structure editable and preserve atomic assets as independent images. For compound objects and node-connected arrows, follow `editable_object_structure_rules.md` before rendering the final candidate.
7. **Render and compare.** Render every slide and compare it side by side with the reference at matching canvas dimensions. Inspect individual text and image regions as well as the montage; correct font scale, wrapping, geometry, crop and layering against the source. Verify the planned native text and preserved assets separately, exercise a representative compound object, then run deterministic PPTX QA and hash verification.

## Editability policies

Do not make the user learn internal policy names. Infer the policy from natural language and material risk.

### SMART (default)

Prioritize page-level native objects, then preserve a complete visual asset when its internal structure is coupled, low-value to edit, or not reliably recoverable. Increase native object coverage only when it improves future maintenance without harming fidelity.

### PRESERVE

Use when the user says that an image or region should remain whole, should not be split, or only needs to be moved, scaled, cropped, replaced, or deleted. Do not OCR and rearrange its internal labels, redraw its legend, or recreate its internal lines.

### DEEP EDIT

Use when the user explicitly wants the inside of a region editable or when a reliable structured source makes that valuable. Rebuild text, shapes, connectors, legends, tables, simple charts, or diagrams only when their structure and meaning can be verified. Deep edit never permits guessing.

### SELECTIVE EDIT

Use when the user names a specific title, number, label, or sub-region to change. Change only that region and keep the surrounding asset intact. A request to edit one number is not permission to decompose the whole figure.

Mixed policies are allowed: one slide may contain SMART page elements, a PRESERVE figure, a DEEP EDIT diagram, and a SELECTIVE EDIT label.

## Object decisions

### Page-level elements: rebuild natively

When reliably identifiable, rebuild these as editable PowerPoint objects:

- title, subtitle, body text, captions, source notes, page numbers, headers, and footers;
- page-level color blocks, borders, dividers, columns, labels, conclusion strips, and containers;
- simple lines, arrows, callouts, highlights, and reading-order connectors;
- verified diagrams whose nodes, relationships, conditions, labels, and conclusions are supported by source material.

Use meaningful text boxes and logical groups. A numbered circle includes its number; a panel tab includes its background and text. Preserve separately replaceable evidence images. Follow `editable_object_structure_rules.md` for grouping and native connection bindings; object naming alone does not make components move together.

### Atomic visual assets: preserve as independent images by default

Treat a region as a complete asset when it is a semantically closed visual unit, even if it contains internal text, labels, curves, legends, panels, annotations, or multiple sub-images. It should remain independently movable, scalable, replaceable, crop-able, and removable. Typical examples are:

- scientific figures and multi-panel evidence;
- screenshots, maps, microscopy panels, finished infographics, and complex illustrations;
- charts whose data is unavailable;
- diagrams whose internal semantics cannot be verified from the image alone.

Do not use the full-slide screenshot as the final background. Crop or reuse complete sub-assets only when the crop boundary is clear and does not leave unrelated page elements embedded.

### Structured editable objects: rebuild only with reliable structure

Tables, simple diagrams, flowcharts, connectors, and native charts may be rebuilt when row/column structure, labels, geometry, and relationships are readable and supported. Use original data for charts whenever possible. If only a raster chart is available, preserve it rather than reverse-engineering exact values from pixels.

### Source-dependent objects: defer without the source

Data visualizations, scientific mechanisms, logos, branded marks, and specialized diagrams may depend on source data, vector artwork, or a verified blueprint. Without that source, preserve the object as an image and disclose the limitation. Do not create a plausible replacement.

## Text, fonts, and geometry

- Recover page-level text as real text whenever it is reliable. Prefer supplied text over OCR.
- Preserve meaning, punctuation, numbers, units, and source labels. Do not invent or silently correct uncertain facts.
- Treat the reference font appearance as a relative target, not a guaranteed font name or point size. Use the active template system; otherwise use Microsoft YaHei for editable Chinese and mixed CJK/Latin text.
- Match visual scale through text-box geometry, line breaks, weight, line spacing, and rendered comparison. Do not blindly copy raster pixels into a point size or use automatic shrinking as the default fix.
- Restore the layout system, not anti-aliasing noise. Normalize colors that clearly share a design role, align elements that are visibly intended to align, and keep a coherent palette.
- Preserve z-order: background, containers, assets, annotations, and text must have the intended stacking relationship.

## Images, crops, and source assets

- Prefer an uploaded original or higher-resolution asset over a crop from the screenshot.
- Preserve aspect ratio and necessary scientific context. Recreate crop, mask, border, and shadow behavior with a deliberate image container.
- Keep each preserved asset independently selectable so it can be replaced later.
- A source image can be editable as an object (move, resize, crop, replace) without making every internal pixel editable. State that distinction in the delivery note when it matters.

## Scientific and factual safeguards

- Do not redraw a scientific data figure from memory or from a visually plausible interpretation.
- Do not infer exact chart values, trends, statistics, experimental conditions, or mechanism causality from pixels alone.
- Preserve axes, legends, units, scale bars, panel labels, color bars, conditions, and necessary notes.
- Reconstruct a mechanism diagram only from a verified source-grounded blueprint. Preserve the original mechanism figure as evidence when one exists.
- Clearly label and obtain confirmation for cross-source synthesis, inference, or proposed hypotheses before final delivery.

## False-editability guard

Never satisfy the task by:

- placing the complete reference image as a full-slide background;
- placing a full-slide screenshot underneath a few overlaid text boxes and calling the page editable;
- splitting a coupled visual asset into meaningless fragments merely to increase object count;
- guessing data or text to make a chart or diagram appear native;
- copying commercial icons, emoji, or decorative fragments from the raster image into editable objects.

If a region cannot be reliably reconstructed, keep it as a clearly bounded independent asset and preserve its semantic integrity.

## Acceptance checks

After reconstruction, check all of the following against the reference and the supplied sources:

### Visual fidelity

- canvas ratio, margins, main geometry, alignment, image/text proportion, hierarchy, palette, crop, whitespace, and z-order;
- font substitution, wrapping, line count, weight, and rendered scale;
- no stretched images, accidental gaps, overlap, clipping, or unexpected blank strips.

### Content accuracy

- no missing or invented text, numbers, labels, units, citations, facts, or relationships;
- no raster OCR artifacts copied as authoritative content;
- original figures and required context remain intact.

### Editability and maintenance

- page-level text and structure can be edited directly;
- numbered nodes and labels move with their constituent text; node-connected arrows carry native endpoint bindings, with actual application behavior distinguished from XML-only inspection;
- preserved assets can be selected, moved, replaced, cropped, or deleted;
- requested DEEP EDIT regions are appropriately structured;
- PRESERVE regions remain whole;
- SELECTIVE EDIT changes stay within the requested boundary;
- no full-slide screenshot is masquerading as a reconstructed deck.

A large-image warning still needs review when native text is present. Compare the flagged region with the input and its assigned policy: a legitimate preserved scientific figure may occupy most of a page, while a page screenshot with text overlays does not fulfill reconstruction. Static QA passing is not proof that required regions are editable.

Deliver the editable `.pptx`, rendered previews when available, `qa-report.json`, and a concise note listing preserved complete assets, source-dependent regions, unresolved text/data, and skipped checks. If the required vision, writer, renderer, or QA tool is unavailable, provide the strongest available reconstruction blueprint and state exactly what was not executed.
