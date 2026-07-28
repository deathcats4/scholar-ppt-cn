# Project State Rules

Use `schemas/project.schema.json` and schema version `1.0.0`.

`project.json` is the machine source of truth. Generate Markdown views from it;
do not maintain independent Markdown facts.

Create an initial state when local Python exists:

```text
python scripts/init_project.py --slug <slug> --title <title> --output <project.json>
```

Keep the state compact:

- use paths instead of embedded files;
- use short summaries instead of copied source text;
- assign stable IDs to slides, assets, families, and variants;
- preserve slide IDs even when page numbers change;
- record canvas dimensions in inches;
- record template source and typography roles;
- record host capabilities without assuming a specific provider;
- record workflow step status and reasons;
- record output artifact paths and QA results.

Validate before PPTX construction and after any structural revision:

```text
python scripts/validate_project.py <project.json>
```

Generate the readable planning view with:

```text
python scripts/export_planning.py <project.json> <planning.md>
```

Do not invent missing evidence provenance. Use null or an empty value when the
schema permits it.
