# Changelog

## 3.4.0-beta.1

Host-agnostic structured workflow beta candidate.

### Added

- Repository-level `AGENTS.md` with product and development decisions.
- Versioned unified project JSON Schema.
- Zero-dependency project scaffolding, JSON validation, and Markdown planning
  export.
- Capability/dependency preflight probe.
- Lightweight Python fallback runtime for baseline editable PPTX generation,
  with optional semantic slide render intent, atomic writes, and recoverable
  previous artifacts.
- Deterministic PPTX ZIP/OOXML static QA and generated readable QA notes.
- Deterministic Skill packaging with manifest and SHA-256.
- Unit fixtures and cross-platform GitHub Actions validation.
- Provider-neutral visual-reference-pack schemas, metadata validation, prompt
  export, and an initial active blue academic reference family.
- Static QA warnings for defensive or builder-facing meta-language that should
  remain internal instead of appearing in final slides.

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
- Made content planning authoritative over visual references and treated
  reference images as late aesthetic anchors rather than editable page
  stencils.
- Kept epistemic safeguards internal while allowing concise evidence limits and
  uncertainty statements in audience-facing slide copy.

### Beta note

- v3.3.1 remains available as the stable release and is not overwritten by this
  beta.
- The legacy reference template remains tracked and is not selected
  automatically by the redesigned workflow.
- Visual-reference coverage, cross-host generation consistency, and internal
  schemas may continue to change before v3.4.0.

## 3.3.1-codex-artifact-workflow

Improved artifact generation, preview inspection, QA guidance, explicit
reference loading, and image-generation batching.

## 3.3.0-productized-planned-family

Added a mandatory mockup family + variants blueprint stage between production
planning and generation.

## 3.2.0-productized-planned-archetype

Restored planning as a production planning table with narrative, source asset,
geometry, message, layout, density, handling, and risk fields.
