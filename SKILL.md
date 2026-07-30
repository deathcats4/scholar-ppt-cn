---
name: scholar-ppt-cn
description: Host-agnostic workflow for creating, rebuilding, restyling, planning, sampling, and revising Chinese academic presentations from papers, theses, reports, figures, notes, screenshots, existing decks, or reference templates. Use when an agent needs structured project state, presentation planning, template DNA, optional visual exploration, editable PPTX work, or deterministic PPTX QA.
---

# Scholar PPT CN

## Interaction

Keep one simple user-facing workflow. Accept natural-language requests such as:

- "参考论文和模板做一份中文组会 PPT。"
- "先做规划表，不要生成 PPT。"
- "不要生图，直接生成可编辑 PPTX。"
- "先做几页视觉样板。"
- "修改第 4 页和第 7 页并重新检查。"

Infer discoverable facts from supplied files and the runtime. Ask when a
subjective preference or a quality/time tradeoff would materially change the
result, even if an agent could make a plausible guess. Useful questions include
template choice, whether to approve representative samples before full
production, target duration/page count, and whether to install a helpful
dependency. Bundle related choices into one short question when practical.

When a useful dependency is missing, state its purpose and ask whether to install
it. If the user declines, continue with the strongest available fallback.

Do not require the user to understand route names, layout IDs, capability flags,
or JSON fields.

## Core contract

Use one adaptive workflow:

1. Read the request and register source files.
2. Probe available capabilities when local tools exist.
3. Create or update a versioned `project.json`.
4. Determine the canvas and authoritative user-template constraints.
5. Plan the narrative, slide communication tasks, evidence coverage, and
   source-asset geometry before choosing reference pages or page skeletons.
6. Select or extract Template DNA, then define deck-wide visual-family
   behaviors and cross-slide rhythm.
7. Retrieve approved visual references only as late aesthetic anchors. Ask
   whether to use representative samples when they would materially reduce
   visual uncertainty.
8. Compose each slide from its current message and evidence. Treat family,
   variant, archetype, and reference-image choices as guidance unless strict
   template adherence was explicitly requested.
9. Create the requested artifact with the available host tools.
10. Run deterministic QA, render/inspect when possible, revise, and deliver.

Do not define Lite, Standard, or Full modes. Record each workflow step as
completed, planned, skipped, or not applicable, with a short reason.

Follow `references/adaptive_workflow_rules.md` for step-selection decisions and
`references/project_state_rules.md` for the project-state contract.

## Project JSON

Create JSON for every task, including planning-only and partial-revision work.
Treat JSON as the machine source of truth and Markdown as a generated view.

Use `schemas/project.schema.json`. Keep project state compact:

- store IDs, paths, short summaries, mappings, decisions, and QA results;
- do not embed PDFs, images, Base64 data, or full source text;
- preserve stable slide and asset IDs across revisions;
- record enabled/skipped steps and reasons;
- update only affected records during partial revisions.

When local Python is available, run:

```text
python scripts/init_project.py --slug <slug> --title <title> --output <project.json>
python scripts/validate_project.py <project.json>
python scripts/export_planning.py <project.json> <planning.md>
```

Do not proceed past a project-state error that would make later artifacts
inconsistent.

## Capability adaptation

Do not bind the workflow to Codex, ChatGPT, a named image model, PowerPoint, or
LibreOffice.

Use `references/capability_rules.md`. When local Python is available, probe with:

```text
python scripts/preflight.py --output <preflight.json>
```

Apply these fallbacks:

- no image generation: construct directly from Template DNA and editable objects;
- no visual model: run static QA and inspect previews manually when possible;
- no office renderer: run OOXML static QA and report skipped visual checks;
- no PPTX writer: deliver validated JSON, planning, and implementation guidance;
- text-only host: deliver project JSON plus readable planning and blueprint views.

Never claim an unavailable check was completed.

## Templates and canvas

Prefer a user-provided template and preserve its native canvas dimensions. When
no user template exists, use an approved visual reference pack or neutral
design tokens and default to 16:9.

When visual identity materially affects the outcome, do not silently choose
between several plausible template directions. Ask whether the user wants to
provide a template, choose an available built-in direction, or accept the
agent's recommendation.

Do not use `assets/templates/scholar-ppt-cn-reference-template.pptx` as the
automatic default. It is a legacy development asset pending replacement.

Treat Template DNA as visual identity, not fixed geometry. Read
`references/template_dna_rules.md` and `references/cjk_typography_rules.md`.

When an approved visual reference pack is available, read
`references/visual_reference_pack_rules.md`. Filter by JSON metadata before
opening only the best 1–3 images. A draft pack is never a runtime default.

Keep this authority order:

- planning decides what each slide must communicate and which evidence it uses;
- the visual family decides identity, hierarchy, annotation behavior, density,
  and cross-slide rhythm;
- reference images indicate the aesthetic target and useful composition
  behaviors;
- the builder decides actual geometry from current title length, evidence
  geometry, density, and neighboring-slide rhythm.

Do not select a reference image first and then reshape the slide task to match
it. Do not turn an approved reference page into a fixed editable stencil.

Use role-based typography:

- inherit template roles when practical;
- keep title, heading, body, caption, source-note, and emphasis roles distinct;
- use platform-aware CJK fallbacks;
- do not force all Chinese text to Microsoft YaHei or bold.

## Narrative and planning

Select a narrative preset from `references/hidden_narrative_presets.md`, unless
the user supplies an explicit structure.

Before planning, index evidence proportionally to the available material. Read:

- `references/evidence_index_rules.md`;
- `references/source_asset_geometry_rules.md`;
- `references/evidence_asset_rules.md`.

Build slide records using `references/production_planning_table_rules.md`.
Record layout intent without locking exact geometry. Use
`references/fallback_layout_archetype_library.md` as an internal vocabulary of
composition possibilities when useful, not as a mandatory page-template
catalog.

Keep evidence figures readable and faithful. Preserve axes, legends, scale bars,
panel labels, table headers, units, and essential notes. Request a better source
only when the missing quality prevents a useful result.

## Optional visual exploration

Treat image generation as a provider-neutral, optional design tool.

Create a mockup family/variant blueprint only when reusable visual planning adds
value, such as a long deck, repeated evidence types, or explicit sample-first
work. Describe visual behavior and variation strategy rather than assigning a
fixed skeleton to every slide. Skip it for simple or local revisions when it
would add no value.

For a new deck with no approved template or visual system, ask whether the user
wants 3–5 representative samples before full production. Recommend samples when
visual uncertainty is high, but let the user skip them. Samples may be editable
PPTX slides built from a template; they do not require image generation.

When visual exploration is used, read:

- `references/mockup_family_variant_blueprint_rules.md`;
- `references/mockup_exploration_rules.md`;
- `references/image_generation_efficiency_rules.md`.

After the user approves samples, read:

- `references/locked_visual_system_rules.md`;
- `references/mockup_derived_archetype_rules.md`.

Approval locks the visual identity and quality bar, not the exact geometry of
the sample pages. Recompose later slides when their real evidence, title length,
or density differs from the sample.

Do not paste a full-slide mockup image as the final editable slide background.
The same rule applies to bundled visual reference images: learn from them, then
rebuild with current-project content and editable objects.

## Editable PPTX

Use the host's available presentation tooling. Follow:

- `references/editable_reconstruction_rules.md`;
- `references/layout_repetition_control.md`;
- `references/visible_text_filter_rules.md`;
- `references/evidence_asset_rules.md`.

Keep titles, body text, captions, source notes, page numbers, simple shapes,
lines, arrows, and callouts editable. Insert source figures as image objects
unless the user requests a redraw.

Keep epistemic guardrails internal. Final slide copy should state what the
evidence supports, limits, or leaves unverified instead of telling the audience
what not to infer or how the builder must avoid misreading it.

Write outputs under a project-specific directory:

```text
outputs/<project-slug>/
  project.json
  planning.md
  deck.pptx
  previews/
  qa-report.json
  qa-note.md
```

Preserve user source files. Retain recoverable versions when revising generated
artifacts.

## QA

Run static QA whenever a PPTX exists:

```text
python scripts/qa_pptx.py <deck.pptx> --project <project.json> --report <qa-report.json> --update-project
python scripts/export_qa_note.py <qa-report.json> <qa-note.md>
```

Use `references/artifact_qa_rules.md`. Classify results as:

- error: deterministic defects that block delivery;
- warning: deliverable limitations that must be reported;
- info: inventory and environment facts.

Render previews and a montage when a renderer exists. Use visual inspection when
the host supports it. Read `references/comparative_montage_qa.md` for rendered
deck review.

Run static QA across the whole deck. Use one montage pass to locate visual
anomalies, then open and re-render only affected slides. Do not inspect every
slide individually unless the montage cannot resolve a suspected issue or the
user requests exhaustive review.

Fix deterministic errors before delivery. Do not block delivery solely because
an optional renderer, image generator, or visual model is unavailable.

## Delivery

Deliver only the artifacts requested by the user plus the project JSON and the
relevant QA result.

- Planning request: `project.json` and generated planning Markdown.
- Sample request: project state and sample images; do not generate PPTX unless
  requested.
- PPTX request: editable PPTX, project JSON, QA report/note, and previews when
  available.
- Revision request: updated artifacts, affected slide summary, and rerun checks.

Use `references/usage_prompts.md` only for invocation examples.
Keep the final response short and practical.
