# Bundled fallback PPTX runtime

The bundled Python runtime is a reliability fallback for execution environments
that can read files and run Python but benefit from a more deterministic PPTX
output path. It is not the project's complete high-fidelity design engine.

## When to use it

Prefer a capable host presentation tool when it can reliably preserve a user
template, create editable objects, and follow the approved visual system.

Use the fallback runtime when the alternative would be:

- a large one-off Python or JavaScript builder written during the task;
- planning-only output even though the user requested an editable PPTX;
- an unstable or repeatedly timing-out host presentation path.

Do not use the fallback for strict reproduction of a user-supplied master,
custom layouts, animations, embedded charts, or complex editable scientific
diagrams. It preserves the project canvas and basic visual tokens, but it does
not import a source template's slide master.

## Dependency

The runtime requires the pinned packages in `requirements-runtime.txt`.
Explain that they provide editable PPTX writing and image inspection, then ask
before installing them:

```text
python -m pip install -r requirements-runtime.txt
```

If installation is declined or unavailable, continue with validated project
JSON, planning, and host-supported output.

## Project state

`project.json` remains the machine source of truth. Each slide may optionally
contain a compact `render` object:

```json
{
  "id": "slide-3",
  "number": 3,
  "title": "多源证据共同支持该机制",
  "communication_task": "用两张证据图解释一致结论",
  "source_asset_ids": ["figure-2", "figure-3"],
  "render": {
    "type": "comparison",
    "subtitle": "两类观测结果相互印证",
    "body": ["证据一说明现象", "证据二约束解释"],
    "asset_ids": ["figure-2", "figure-3"],
    "footer": null
  }
}
```

Supported types are:

- `auto`;
- `cover`;
- `section`;
- `statement`;
- `bullets`;
- `figure`;
- `comparison`;
- `multi-panel`;
- `process`;
- `conclusion`.

The optional fields are `subtitle`, `body`, `items`, `asset_ids`,
`ignored_asset_ids`, `ignore_reason`, and `footer`. Every render asset must
exist and must also appear in the slide's `source_asset_ids`.

When `asset_ids` is omitted, the runtime uses `source_asset_ids` as the
effective render list. `figure` requires one effective asset, `comparison`
requires two, `multi-panel` requires two to four, and `cover` permits at most
one. For comparison and multi-panel pages, `items[].asset_id` binds its label
and explanation to that asset instead of relying on array position. A short
`body` array remains a valid fallback when no item metadata is supplied.

The fixed layouts also have explicit content capacities so valid input is
never silently truncated: cover metadata, bullet/statement items, figure
annotations, and conclusion entries permit at most four items; process pages
permit at most five steps. The validator applies these rules after resolving
`auto` to its effective render type and reports `slide.render_content_count`
or `slide.render_asset_count` before a build can begin.

The build report records which declared evidence assets were actually placed.
If a page intentionally leaves declared evidence out, list those IDs in
`ignored_asset_ids` and give a concise `ignore_reason`; otherwise the runtime
reports `build.asset_unused`.

Keep this object semantic. Do not store pixel coordinates or reproduce an
entire visual-reference image as a fixed stencil. Without `render`, the runtime
infers a conservative layout from the slide task and evidence count.

## Build

```text
python scripts/build_deck.py <project.json> \
  --base-dir <project-root> \
  --report <build-report.json> \
  --update-project
```

PPTX and report paths are validated together. Neither may overwrite
`project.json`, a declared source/template/asset, or each other. Unexpected
runtime failures are returned as structured `build.runtime` errors; add
`--debug` only when a traceback is useful for development.

The builder:

- creates native editable text, shapes, lines, and image objects;
- keeps source images uncropped by default;
- uses the project's canvas size;
- uses project font/color roles where available, with Microsoft YaHei and
  Times New Roman defaults;
- writes through a temporary file and atomically replaces the output;
- preserves an existing generated deck under `versions/` before replacement;
- does not automatically add a cover image, source region, warning banner, or
  internal QA language.

Run static QA immediately after the build. Rendering and montage inspection
remain conditional enhancements.

## Visual expectations

The fallback is designed to produce a usable, restrained academic baseline. It
does not promise pixel-level reconstruction of visual-reference packs. A host
with stronger editable-slide capabilities may use the same project state and
reference metadata to produce a more expressive result.
