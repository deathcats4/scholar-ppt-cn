# Adaptive Workflow Rules

Use one workflow and decide each step independently. Do not assign a user-facing
mode.

## Ask at meaningful decision points

Infer objective facts from the request, source files, templates, and runtime.
Ask the user when the answer is a preference or tradeoff that materially changes
quality, time, or deliverables.

Useful questions include:

- which template direction to use when no approved template exists;
- whether to approve 3–5 representative samples before full production;
- target duration or page count when it cannot be inferred from context;
- whether to install a useful missing dependency;
- whether to wait for a missing key evidence asset or continue with a fallback.

Keep questions user-facing and concise. Bundle related choices when practical.
Do not ask about JSON fields, layout IDs, capability flags, internal route
names, or facts that the agent can discover safely.

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
- visual samples: ask when a new or long deck has no approved visual system or
  visual uncertainty is high; follow the user's choice;
- editable PPTX: when requested and the host can write PPTX;
- rendering: when a renderer is available and a PPTX exists;
- visual QA: when rendered previews and visual inspection are available.

Record every step under `workflow.steps` with `status` and `reason`. A skipped or
not-applicable step must have a reason.

Representative samples may be editable template-based slides. Image generation
is optional and must not be treated as a prerequisite for sample approval.

For a partial revision, preserve stable IDs and update only affected slide,
asset, artifact, and QA records.
