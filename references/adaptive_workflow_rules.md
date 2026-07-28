# Adaptive Workflow Rules

Use one workflow and decide each step independently. Do not assign a user-facing
mode.

## Always perform

- register the request and source files;
- create or update `project.json`;
- determine canvas and template behavior;
- create or update affected slide records;
- validate project state;
- run the strongest QA available for every produced artifact.

## Perform when useful

- evidence index: when source figures, tables, screenshots, or citations matter;
- family blueprint: when several slides benefit from reusable visual families;
- visual samples: when the user requests samples or visual uncertainty is high;
- editable PPTX: when requested and the host can write PPTX;
- rendering: when a renderer is available and a PPTX exists;
- visual QA: when rendered previews and visual inspection are available.

Record every step under `workflow.steps` with `status` and `reason`. A skipped or
not-applicable step must have a reason.

For a partial revision, preserve stable IDs and update only affected slide,
asset, artifact, and QA records.
