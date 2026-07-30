# Visual Reference Pack Rules

Use an approved visual reference pack as a design reference, not as a slide
template or a source of scientific content.

## Priority

1. Preserve a user template's canvas, branding, palette, and typography first.
2. When no user template exists, select one approved visual family for the
   whole deck.
3. If no approved pack is available, continue with neutral design tokens and
   editable layout rules.
4. Never activate a pack whose manifest status is `draft`.

## Authority and timing

Use this order:

1. Planning defines the narrative, slide task, core message, and evidence.
2. Evidence indexing classifies the real source-asset geometry and constraints.
3. The visual family defines identity, hierarchy, density range, annotation
   behavior, and cross-slide rhythm.
4. Reference retrieval supplies a late aesthetic anchor and useful composition
   behaviors.
5. The builder composes the actual page from current content.

Do not retrieve a reference page and then invent or reshape content to fill its
regions. Do not use a reference to decide slide count, narrative order, or
evidence coverage.

## Runtime retrieval

Filter references from JSON metadata before opening images. Match:

- communication role;
- primary asset geometry;
- information density;
- title mode when relevant.

Open only the best 1–3 candidate images. Do not load the whole pack or its
contact sheet during ordinary production. If vision is unavailable, continue
from the JSON metadata and family notes.

Keep one visual family across a deck. Borrow from another family only when the
current family has no suitable composition, and preserve the active deck's
visual identity.

## Interpretation

Learn visual hierarchy, whitespace, evidence dominance, composition,
typographic roles, and page rhythm. Do not copy:

- example titles, labels, conclusions, numbers, charts, or research subjects;
- a reference image's exact geometry when the real content requires another
  composition;
- a pictured font family when it is unavailable locally;
- an image simply because the reference page contains one.

Treat exact columns, panel sizes, image positions, connector paths, decorative
motifs, and title wrapping as non-binding. A selected image is a quality and
design-language reference, not a target wireframe.

Reference images must not be pasted, cropped, or rasterized into the final
slide. Rebuild the page with editable text, shapes, and current-project
evidence. Reusable decorative pixels must be reviewed and packaged separately
as visual assets.

Do not require pixel-level similarity. Adapt to real title length, asset
geometry, and density. Record selected reference IDs and a short reason in
project state when the host schema supports it.

Keep the family's main text and identity colors stable. Introduce a
project-specific orange, green, purple, or other semantic accent only when it
clarifies current evidence or mechanism roles. Use it locally and sparingly; do
not infer a new deck-wide palette from one example reference.

## Pack admission

Only human-approved references enter an active pack. Each approved PNG must:

- use a 16:9 canvas near 1600 x 900;
- contain readable Simplified Chinese with no obvious garbling;
- be credible for a real academic presentation;
- have clear hierarchy and evidence priority;
- be reasonably reconstructable with editable presentation objects;
- include sidecar metadata that states what to learn and what not to copy.

AI-generated example data may appear in a reference image, but the metadata
must mark it as example content and forbid reuse.

Do not require a fixed footer, page number, or visible source zone. Keep source
traceability in project state and show it on slides only when the task needs it.

Do not treat a few approved pages as a complete family. Before using a pack for
an end-to-end single-paper demonstration, cover at least:

- cover;
- research gap;
- research question;
- method design;
- dominant result;
- comparison;
- multi-panel evidence;
- mechanism;
- discussion or outlook;
- conclusion.

Keep the pack in `draft` while this coverage is incomplete. Three independent
references per role are the development target, not a runtime requirement.

## Development workflow

Generate references in small batches:

1. Use a short shared aesthetic baseline plus one page-task prompt.
2. Generate three independent candidates for exploration.
3. Select visually strong candidates by human review.
4. Normalize approved images and generate metadata.
5. Validate the pack before changing its status to `active`.

Store family expansion tasks in versioned JSON and export copy-ready Markdown
from that JSON. Do not independently maintain two prompt sources.

During exploration, do not chain every image to the previous one. After a
direction is approved, use one selected image as a family anchor while asking
for the same identity without copying its exact composition.
