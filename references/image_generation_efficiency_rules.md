# Image Generation Efficiency Rules

Use these rules when generating image-model slide mockups.

## Why

Full 16:9 academic slide mockups are slow because each page asks the image model to solve composition, typography, template identity, evidence placeholders, and Chinese/English visual hierarchy at once. Long batches increase the chance of timeouts, reconnects, inconsistent style, and wasted generations.

## Default batching

- First generate 1-2 pilot mockups only.
- Use the pilot to test Template DNA, title system, figure/text ratio, and whether unwanted institutional labels or placeholder text appear.
- After the pilot is acceptable, continue in batches of 2-3 pages.
- For 5-8 requested sample pages, split into at least two batches.
- For more than 8 sample pages, recommend switching to editable PPTX generation after representative samples are approved.

## Page selection

Prioritize pages that test different layout risks:

- cover or report map;
- one large evidence figure page;
- one dense multi-panel figure page;
- one chart or quantitative interpretation page;
- one mechanism/discussion page;
- one conclusion page.

Avoid generating multiple pages that test the same skeleton unless the user specifically needs alternatives.

## Prompt strategy

Keep each image prompt focused on one slide page.

Include:

- 16:9 full-slide mockup;
- template tone and palette;
- selected mockup family/variant;
- rough source-asset geometry;
- intended visual hierarchy;
- requirement that evidence figures are readable placeholders and will be replaced by real source assets during editable PPTX reconstruction;
- instruction to avoid fake university names, fake logos, and visible internal workflow terms.

Avoid:

- asking one image prompt to create many unrelated slide pages;
- demanding accurate paper figure content from memory;
- putting final Chinese body text into image mockups when it will later be rebuilt as editable text;
- using image mockups as final PPT backgrounds.

## Delivery behavior

After each batch, briefly report:

- generated page numbers;
- obvious issues to correct in the next batch;
- whether the visual system is stable enough to continue.

If generation becomes slow or reconnect-prone, stop after the current completed batch and offer to continue with the next batch or switch to editable PPTX reconstruction.

