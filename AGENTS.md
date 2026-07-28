# Scholar PPT CN Repository Instructions

## Mission

Build a host-agnostic Chinese academic presentation workflow Skill for capable
AI agents. The repository may use host-provided file, presentation, rendering,
vision, or image-generation tools, but the core workflow must not depend on
Codex, ChatGPT, or any named image model.

The project is a workflow Skill with deterministic planning validation, PPTX
static QA, packaging, and CI support. It does not promise a bundled,
deterministic end-to-end PPTX generation engine.

## Product principles

1. Keep one user-facing adaptive workflow:
   source intake -> project state -> planning -> template/layout selection ->
   optional visual samples -> editable PPTX -> QA -> revision.
2. Do not expose internal execution modes. Record enabled/skipped steps and
   their reasons in project JSON instead.
3. Prefer flow over interrogation. Infer discoverable facts from files and the
   environment. Ask only when missing information would materially change the
   result and cannot be inferred safely.
4. Treat image generation, visual inspection, office rendering, and local PPTX
   writing as optional capabilities. Degrade gracefully when they are absent.
5. When a useful dependency is missing, explain its purpose and ask whether to
   install it. If the user declines, continue with the strongest available
   fallback and record the limitation.
6. Preserve existing natural-language usage such as:
   - planning only;
   - direct editable PPTX without image generation;
   - sample-first visual exploration;
   - expansion from approved samples;
   - revision of selected slides.
7. Keep internal workflow terms out of final slide text.

## Structured state

1. Every task produces JSON, including small and partial tasks.
2. JSON is the machine source of truth. Markdown is a derived human-readable
   view and must not become a second independently maintained source.
3. Use one versioned `project.json` per presentation project.
4. Keep JSON compact. Store IDs, paths, short summaries, decisions, mappings,
   and QA results. Never embed source PDFs, images, Base64 data, or full paper
   text.
5. Record actual workflow steps as booleans/status values plus concise decision
   reasons. Do not map them to Lite/Standard/Full labels.
6. Give every durable entity a stable ID. Validate duplicate IDs, broken
   references, slide coverage, and schema version.
7. Add schema migration support before making an incompatible schema revision.

## Template behavior

1. User-provided templates take priority. Preserve their native canvas size,
   including 4:3 or custom dimensions.
2. When no user template exists, default to a 16:9 built-in template or neutral
   design-token preset.
3. The intended built-in set is three original, neutral academic templates:
   concise technical, dark report, and warm humanities.
4. Each built-in template must ship with:
   - editable PPTX;
   - template DNA JSON;
   - previews;
   - font fallback notes;
   - asset and license inventory.
5. Do not use institutional names, logos, personal metadata, fabricated
   academic claims, or unlicensed third-party imagery in built-in templates.
6. Keep the existing legacy reference template tracked during the current local
   experimentation phase. Do not delete, move, publish a replacement, or change
   remote releases until the user explicitly approves that action.
7. The redesigned Skill must stop treating the legacy template as the automatic
   default before new templates are published.

## Typography

1. Prefer typography roles extracted from the user template.
2. For built-in templates, define title, heading, body, caption, source-note,
   and emphasis roles separately.
3. Do not require all CJK text to use Microsoft YaHei or bold.
4. Use platform-aware CJK fallback stacks and check font availability.
5. QA should detect missing fonts, substitutions, unreadable sizing, and lost
   hierarchy rather than merely checking `bold=true`.

## Evidence and editability

1. Preserve source figures as evidence assets unless the user requests a
   redraw.
2. Do not crop essential axes, legends, labels, scale bars, panel markers,
   headers, or explanatory notes.
3. Keep slide titles, body text, captions, source notes, page numbers, simple
   shapes, arrows, and callouts editable.
4. Do not use a full-slide mockup image as the final editable slide background.
5. Keep evidence provenance proportional to available source information.
   Missing optional citation details should be reported, not invented.

## Image and visual-model behavior

1. Do not name or require a specific image model in the core workflow.
2. Represent visual exploration through provider-neutral requests and project
   state.
3. Skip visual samples when they add little value or the user requests direct
   editable output.
4. Use visual samples when the user requests them or when they materially reduce
   visual uncertainty.
5. A workflow without image generation must remain complete and useful.

## Output layout

Use a project-specific output directory:

```text
outputs/<project-slug>/
  project.json
  planning.md
  deck.pptx
  previews/
  qa-report.json
  qa-note.md
```

Do not overwrite user-provided source papers, templates, or PPTX files. Preserve
recoverable versions of generated artifacts when revising an existing project.

## Python implementation

1. Use Python 3.11+ for deterministic tools.
2. Keep core commands cross-platform across Windows, macOS, and Linux.
3. Prefer the standard library where practical. Declare and pin required
   third-party dependencies.
4. PowerShell and shell scripts may be thin convenience wrappers only; do not
   place core logic in them.
5. Detect optional tools such as LibreOffice, PowerPoint, PDF renderers, image
   tools, vision models, and image generators at runtime.
6. Commands must return meaningful exit codes and support machine-readable JSON
   reports.

## QA policy

Use three severities:

- `error`: deterministic defects that block delivery, such as a broken PPTX
  package, missing required slide records, invalid media references, obvious
  slide-bound violations, visible internal workflow terms, or JSON/PPTX slide
  count mismatch.
- `warning`: deliverable limitations that must be reported, such as low image
  resolution, possible overlap, font substitution, very small text, repeated
  layout structure, or incomplete source information.
- `info`: ordinary inventory and environment facts.

Static Python QA is required whenever a PPTX exists. Rendering and visual QA are
conditional enhancements:

1. Render previews and a montage when a renderer is available.
2. Use visual inspection when the host supports it.
3. Do not block delivery solely because a visual model is unavailable.
4. Record every skipped check and the reason.

## Repository structure

- Keep `SKILL.md` concise and procedural.
- Put detailed domain rules in directly linked files under `references/`.
- Put deterministic reusable code under `scripts/`.
- Put JSON Schemas under `schemas/`.
- Put small deterministic test fixtures under `tests/fixtures/`.
- Do not duplicate normative rules between `SKILL.md` and references.
- Avoid orphan reference files; every normative reference must be linked from
  `SKILL.md` or intentionally marked as user documentation.

## Testing and definition of done

For changes to scripts or schemas:

1. Run unit tests.
2. Validate all JSON fixtures against the current schema.
3. Run PPTX QA against at least one valid fixture and one intentionally invalid
   fixture.
4. Run the Skill package validator.
5. Verify commands on the current platform without assuming optional tools are
   installed.
6. Report checks that could not run.

Do not claim a check passed unless it was executed successfully.

## Current local milestone

The first milestone includes:

- this `AGENTS.md`;
- a concise, host-agnostic `SKILL.md`;
- a versioned unified project JSON Schema;
- Python environment probing, project validation, Markdown export, and PPTX
  static QA;
- fixtures and automated tests;
- GitHub Actions configuration;
- README and changelog updates.

Do not create the three new built-in templates in this milestone.

## Draft PR review collaboration

Use a Draft PR as the review center for substantial milestones after the user
authorizes publishing the local work for review.

### PR shape

1. Prefer one coherent Draft PR when schemas, scripts, Skill rules, tests, and
   documentation depend on one another.
2. Split work into logical commits so reviewers can inspect intent without
   creating intermediate PRs that are knowingly unusable.
3. Use the `codex/` branch prefix unless the user requests another convention.
4. Keep the PR in draft state until review findings are resolved and the user
   explicitly approves readiness.
5. Do not mix unrelated cleanup or template redesign into a foundation PR.

### PR description

State:

- objective and user-visible outcome;
- important architectural decisions;
- explicit non-goals;
- files or assets intentionally left unchanged;
- tests and checks actually run;
- known limitations and deferred work;
- focused questions for reviewers.

Do not claim GitHub CI passed until the remote checks have completed.

### Multi-AI review roles

Assign independent reviewers narrow, non-overlapping scopes instead of asking
every reviewer to "review everything." Useful roles include:

1. schema and state architecture;
2. Python, OOXML, and cross-platform behavior;
3. Skill instructions, adaptive workflow, and host portability;
4. CI, deterministic packaging, and release contents;
5. realistic forward-testing from ordinary user prompts.

Ask reviewers to:

- cite exact files and line numbers;
- classify findings as error, warning, or suggestion;
- separate confirmed defects from inference;
- explain user impact and a reproducible failure case when possible;
- avoid reopening already accepted product decisions unless new evidence shows a
  concrete problem.

By default, external AI reviewers should comment rather than write directly to
the working branch.

### Review iteration

1. Triage every finding as accepted, rejected with evidence, deferred, or
   duplicate.
2. Fix accepted findings locally and add regression coverage where practical.
3. Reply with the change and verification evidence.
4. Use a fresh reviewer/context for the final pass when independence matters.
5. Keep merge authority with the user; AI approval is advisory.

Do not create commits, push a branch, open a PR, mark a PR ready, or merge merely
because this review protocol exists. Each external Git action still requires the
user's explicit instruction.

## Git and external actions

1. Work locally and show the user milestone summaries.
2. Do not commit, push, publish a release, modify GitHub issues, or change remote
   state without explicit user instruction.
3. Do not remove or replace the legacy template without explicit user
   instruction.
4. Preserve unrelated user changes in a dirty worktree.
