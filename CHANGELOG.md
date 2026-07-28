# Changelog

## 3.4.0-dev

Host-agnostic structured workflow under local development.

### Added

- Repository-level `AGENTS.md` with product and development decisions.
- Versioned unified project JSON Schema.
- Zero-dependency project scaffolding, JSON validation, and Markdown planning
  export.
- Capability/dependency preflight probe.
- Deterministic PPTX ZIP/OOXML static QA and generated readable QA notes.
- Deterministic Skill packaging with manifest and SHA-256.
- Unit fixtures and cross-platform GitHub Actions validation.

### Changed

- Replaced named-host routing with one adaptive workflow.
- Made image generation and visual samples optional and provider-neutral.
- Made mockup family/variant planning conditional.
- Preserved user-template canvas dimensions; default to 16:9 only without a
  source canvas.
- Replaced mandatory Microsoft YaHei bold CJK text with role-based typography
  and platform-aware fallbacks.
- Made JSON the machine source of truth and Markdown a generated view.
- Reduced `SKILL.md` and moved detailed rules to directly linked references.
- Stopped selecting the legacy reference template automatically.
- Ask users about material preference and quality/time decisions such as
  template direction and representative-sample approval instead of silently
  guessing.
- Changed rendered QA to montage-first anomaly triage and individual inspection
  of affected slides only.

### Development note

- The legacy reference template remains tracked during local testing and has not
  been removed or replaced.
- No commit, push, release, or remote issue action is part of this local phase.

## 3.3.1-codex-artifact-workflow

Improved artifact generation, preview inspection, QA guidance, explicit
reference loading, and image-generation batching.

## 3.3.0-productized-planned-family

Added a mandatory mockup family + variants blueprint stage between production
planning and generation.

## 3.2.0-productized-planned-archetype

Restored planning as a production planning table with narrative, source asset,
geometry, message, layout, density, handling, and risk fields.
