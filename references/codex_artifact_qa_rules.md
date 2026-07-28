# Codex Artifact QA Rules

Use these rules when the skill runs in Codex or another environment with file and tool access.

## Purpose

Codex should not stop at a prompt, plan, or verbal QA when the user asks for an editable PPTX. It should produce artifacts and verify them as far as the environment allows.

## Artifact contract

For editable PPTX tasks, create:

- the final editable `.pptx`;
- slide preview images or an equivalent rendered preview when possible;
- a preview montage when possible;
- a short QA note listing checks performed and any unresolved limitations.

Use clear output filenames that include the project/topic and stage, such as:

- `planning-table.md`;
- `mockup-family-variants.md`;
- `sample-slide-01.png`;
- `deck-draft.pptx`;
- `deck-preview-montage.png`;
- `qa-note.md`.

## Production behavior

- Prefer editable PowerPoint objects for text, captions, callouts, simple shapes, lines, arrows, and simple diagrams.
- Insert source figures, screenshots, tables, and evidence images as image objects unless the user asks for redrawing.
- Do not use a full-slide mockup image as the final editable slide background.
- Preserve source evidence labels, axes, legends, scale bars, panel labels, table headers, and explanatory notes.
- If a key source asset is too low-resolution to present, ask for a better version or mark the limitation clearly.

## Preview and QA

Before final delivery, inspect the deck through rendered previews or the closest available substitute.

Check:

- whether the PPTX opens/renders;
- title, header, footer, and page-number consistency;
- CJK font and bold compliance for editable Chinese text;
- text overflow, clipping, or accidental overlap;
- source asset readability;
- repeated visible skeletons across consecutive content slides;
- visible internal workflow terms that should not appear in final slides;
- whether the deck still reads as one visual system.

When a problem is fixable, revise the deck before delivery. When it is not fixable with available files or tools, record it in the QA note.

## ChatGPT compatibility

These artifact QA rules are conditional. In environments without file, PPTX, rendering, or image-inspection tools, provide the strongest possible planning or generation guidance and state which checks still need to be completed after export.
