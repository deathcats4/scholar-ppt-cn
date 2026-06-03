# Changelog

## 3.3.0-productized-planned-family

Added a mandatory mockup family + variants blueprint stage between production planning and generation.

### Added
- Template DNA reconfirmation before mockup family construction.
- Mockup family summary table.
- Multiple variants per family.
- Slide-to-family/variant mapping for every planned slide.
- Representative sample selection.
- Dedicated reference: `mockup_family_variant_blueprint_rules.md`.

### Changed
- Image-model samples now follow both the production planning table and the mockup family + variants blueprint.
- Template-direct editable PPTX also uses the family/variant blueprint for visual consistency.
- High-frequency families must define 4-6 variants to reduce repetitive pages.

# Changelog

## 3.2.0-productized-planned-archetype

Restored planning, but redefined it as a production planning table.

### Added
- Production planning table as central pre-generation artifact.
- Planning table fields: narrative section, communication task, source asset, source-asset geometry, core message, layout archetype ID, density, asset handling, risks.
- Hidden narrative presets now include:
  - literature report / journal club;
  - thesis / defense;
  - research progress;
  - general topical presentation.
- Detailed fallback layout archetype library remains required for template-direct generation.
- Image-model samples now follow the planning table while retaining composition freedom inside selected archetypes.

### Clarified
- Planning table is not an old-style rigid slide outline.
- Narrative presets control story order; layout archetypes control structure; Template DNA controls visual identity.
- User-provided outline overrides hidden presets.
