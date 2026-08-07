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
11. Deliver only when delivery-blocking errors are zero and the QA report hash matches the final PPTX.

## Scenario Profiles

Typical commands:

```text
python scripts/qa_pptx.py deck.pptx --profile group-meeting --report qa-report.json
python scripts/verify_final_qa.py deck.pptx qa-report.json --require-profile group-meeting
```

Available profiles: `group-meeting`, `defense`, `conference`, `classroom`, and `template-preserve`. The first four are strict projection scenarios. Use `template-preserve` only when the user explicitly requires in-place preservation of an existing template typography system; in that profile, legacy icon fonts are review warnings rather than delivery-blocking errors.

## Delivery-Blocking Errors

- invalid ZIP/OOXML;
- missing required parts or broken relationships;
- no slides;
- objects entirely outside the slide;
- visible internal workflow terms;
- prohibited literature-report labels selected by the user preference profile;
- prohibited commercial icon glyphs or icon/emoji fonts in editable text objects;
- project-record slide count or canvas mismatch when a project record is supplied.

## Warnings Requiring Review

- external relationships, macros, ActiveX, or embedded objects;
- partially out-of-bounds objects;
- low effective image resolution;
- possible text-box overlap;
- font inventory and possible substitution;
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
- whether commercial icons were recreated with PowerPoint shapes or embedded images, which static text QA cannot reliably identify;
- whether a mechanism diagram or scientific arrow lacks source verification, or presents an inference/hypothesis as an established conclusion;
- whether cards or bottom conclusion strips are repeated mechanically across the deck.

If rendering or another required tool is unavailable, state the limitation and perform the strongest available substitute check.
