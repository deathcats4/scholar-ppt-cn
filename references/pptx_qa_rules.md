# PPTX QA Rules

Use these rules when the environment provides file, PPTX, rendering, or inspection tools. Static QA checks the PPTX package itself, including supported objects nested inside PowerPoint groups; it does not replace visual review, semantic review, template/mockup comparison, or scientific figure readability.

## PPTX Delivery Contract

For editable PPTX tasks, create when the environment supports them:

- the final editable `.pptx`;
- slide previews;
- a preview montage;
- `qa-report.json`;
- a concise QA note.

Do not claim a check passed unless it ran against the final deliverable. Any PPTX modification invalidates the old QA report.

For localized or deck-wide mechanical revision of an existing PPTX, run baseline QA before editing when available. Final QA must introduce no new delivery-blocking errors and leave none unresolved within the changed scope. Report pre-existing errors outside the changed scope without modifying unrelated content.

## Final Revision Loop

1. Save the candidate PPTX.
2. Render every slide when a renderer is available.
3. Inspect the montage.
4. Compare against the approved mockups or the selected template system.
5. Check scientific figure readability and repeated visible skeletons.
6. Fix abnormal slides.
7. Run `scripts/qa_pptx.py` using the appropriate profile.
8. Save again and re-render after any fix.
9. Rerun QA on the new file.
10. Run `scripts/verify_final_qa.py`.
11. For new decks and broad redesign, deliver only when delivery-blocking errors are zero. For localized or deck-wide mechanical revision, deliver only when no new delivery-blocking errors were introduced and none remain within the changed scope.
12. Verify that the QA report hash matches the final PPTX.

## Scenario Profiles

Typical commands:

```text
python scripts/qa_pptx.py deck.pptx --profile group-meeting --report qa-report.json
python scripts/verify_final_qa.py deck.pptx qa-report.json --require-profile group-meeting
```

Available profiles: `group-meeting`, `defense`, `conference`, `classroom`, and `template-preserve`. The first four are strict projection scenarios. Use `template-preserve` only when the user explicitly requires in-place preservation of an existing template typography system.

## Bundled commands

Use the applicable commands:

```text
python scripts/preflight.py --output preflight.json
python scripts/render_preview.py deck.pptx --output-dir previews --montage montage.png
python scripts/qa_pptx.py deck.pptx --profile group-meeting --report qa-report.json
python scripts/export_qa_note.py qa-report.json qa-note.md
python scripts/verify_final_qa.py deck.pptx qa-report.json --require-profile group-meeting
```

## Delivery-Blocking Errors

- invalid ZIP/OOXML;
- missing required parts or broken relationships;
- no slides;
- objects entirely outside the slide;
- visible internal workflow terms;
- visible slide-production, figure-handling, cropping, layout, or design commentary;
- prohibited literature-report labels selected by the user preference profile;
- prohibited commercial icon glyphs in editable text objects;
- project-record slide count or canvas mismatch when a project record is supplied.

## Warnings Requiring Review

- external relationships, macros, ActiveX, or embedded objects;
- partially out-of-bounds objects;
- low effective image resolution;
- possible text-box overlap;
- font inventory and possible substitution;
- symbol or icon fonts used outside ordinary bullet markers;
- possible full-slide flattened image;
- skipped rendering or visual inspection;
- rendered text that is clipped, overcrowded, or out of scale with the approved mockup/template hierarchy.

## Human Judgment Checks

After static QA passes, still inspect:

- template/mockup adherence and deck-wide visual consistency;
- title, header, footer, caption, and page-number consistency;
- repeated visible skeletons;
- text scale, overflow, clipping, and accidental overlap;
- figure readability, including axes, legends, scale bars, panel labels, table headers, and necessary notes;
- figure handling across `preserve`, `overview+detail`, `split`, and `cross-slide`;
- whether final slides expose internal production language;
- whether images preserve aspect ratio and fit their containers without accidental blank strips, thin exposed gaps, or visibly uneven padding;
- whether commercial icons were recreated with PowerPoint shapes or embedded images, which static text QA cannot reliably identify;
- whether a mechanism diagram or scientific arrow lacks source verification, or presents an inference/hypothesis as an established conclusion;
- whether recurring visual components match the selected template or approved visual system.

If rendering or another required tool is unavailable, state the limitation and perform the strongest available substitute check.
