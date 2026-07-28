# Artifact QA Rules

Run deterministic static QA whenever a PPTX exists.

## Error

Block delivery for:

- invalid ZIP/OOXML package structure;
- missing required presentation parts or broken internal relationships;
- no slides;
- JSON/PPTX slide-count mismatch;
- JSON/PPTX canvas mismatch;
- entirely off-slide elements;
- visible internal workflow terms.

## Warning

Report but do not automatically block for:

- external relationships, macros, ActiveX, or embedded objects;
- partial slide bleed;
- effective image resolution below the configured threshold;
- very small editable text;
- possible text-box overlap;
- font substitution or missing preferred fonts;
- incomplete optional provenance;
- repeated visible skeletons;
- skipped rendering or visual inspection.

## Info

Record:

- page count and canvas;
- fonts and media inventory;
- available renderers and inspection capabilities;
- checks performed and skipped.

Run:

```text
python scripts/qa_pptx.py <deck.pptx> --project <project.json> --report <qa-report.json> --update-project
python scripts/export_qa_note.py <qa-report.json> <qa-note.md>
```

Treat static overlap and resolution findings as candidates for visual
verification because intentional composition can produce false positives.
