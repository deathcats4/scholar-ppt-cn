from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.common import Issue, load_json, make_report, print_report, write_json
from scripts.pptx_runtime import RENDER_CONTENT_LIMITS, infer_render_type
from scripts.schema_validation import validate_against_schema


SUPPORTED_SCHEMA_VERSION = "1.0.0"
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "project.schema.json"
REQUIRED_TOP_LEVEL = {
    "schema_version",
    "project",
    "canvas",
    "template",
    "capabilities",
    "workflow",
    "assets",
    "slides",
    "visual_system",
    "artifacts",
    "qa",
}
REQUIRED_STEPS = {
    "intake",
    "project-state",
    "planning",
    "template-dna",
    "editable-pptx",
    "static-qa",
}
STEP_STATUSES = {
    "planned",
    "in-progress",
    "completed",
    "skipped",
    "not-applicable",
}


def _require_object(
    parent: dict[str, Any], key: str, issues: list[Issue], path: str
) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        issues.append(Issue("error", "type.object", f"{key} must be an object", path))
        return {}
    return value


def _require_list(
    parent: dict[str, Any], key: str, issues: list[Issue], path: str
) -> list[Any]:
    value = parent.get(key)
    if not isinstance(value, list):
        issues.append(Issue("error", "type.array", f"{key} must be an array", path))
        return []
    return value


def _check_unique(
    values: list[Any], label: str, path: str, issues: list[Issue]
) -> None:
    seen: set[Any] = set()
    for value in values:
        if value in seen:
            issues.append(
                Issue("error", "id.duplicate", f"Duplicate {label}: {value}", path)
            )
        seen.add(value)


def validate_project(data: dict[str, Any]) -> list[Issue]:
    schema = load_json(SCHEMA_PATH)
    issues: list[Issue] = validate_against_schema(data, schema)
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    for key in missing:
        issues.append(
            Issue("error", "field.required", f"Missing top-level field: {key}", key)
        )

    extra = sorted(set(data) - REQUIRED_TOP_LEVEL - {"$schema"})
    for key in extra:
        issues.append(
            Issue("warning", "field.unknown", f"Unknown top-level field: {key}", key)
        )

    if data.get("schema_version") != SUPPORTED_SCHEMA_VERSION:
        issues.append(
            Issue(
                "error",
                "schema.unsupported",
                f"schema_version must be {SUPPORTED_SCHEMA_VERSION}",
                "schema_version",
            )
        )

    project = _require_object(data, "project", issues, "project")
    for key in ("id", "slug", "title", "task_type", "output_dir"):
        if not isinstance(project.get(key), str) or not project.get(key, "").strip():
            issues.append(
                Issue(
                    "error",
                    "field.required",
                    f"project.{key} must be a non-empty string",
                    f"project.{key}",
                )
            )
    slug = project.get("slug")
    if isinstance(slug, str) and not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
        issues.append(
            Issue(
                "error",
                "project.slug",
                "project.slug must use lowercase letters, digits, and hyphens",
                "project.slug",
            )
        )
    _require_list(project, "source_files", issues, "project.source_files")

    canvas = _require_object(data, "canvas", issues, "canvas")
    for key in ("width_inches", "height_inches"):
        value = canvas.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            issues.append(
                Issue(
                    "error",
                    "canvas.dimension",
                    f"canvas.{key} must be a positive number",
                    f"canvas.{key}",
                )
            )

    template = _require_object(data, "template", issues, "template")
    template_source = template.get("source")
    if (
        isinstance(template_source, str)
        and template_source in {"user", "existing-deck"}
        and not template.get("path")
    ):
        issues.append(
            Issue(
                "error",
                "template.path",
                "A user or existing-deck template requires template.path",
                "template.path",
            )
        )
    _require_object(template, "dna", issues, "template.dna")

    capabilities = _require_object(data, "capabilities", issues, "capabilities")
    for name, value in capabilities.items():
        if not isinstance(value, dict):
            issues.append(
                Issue(
                    "error",
                    "capability.type",
                    f"Capability {name} must be an object",
                    f"capabilities.{name}",
                )
            )
            continue
        available = value.get("available")
        if available is not None and not isinstance(available, bool):
            issues.append(
                Issue(
                    "error",
                    "capability.available",
                    f"Capability {name}.available must be true, false, or null",
                    f"capabilities.{name}.available",
                )
            )

    workflow = _require_object(data, "workflow", issues, "workflow")
    steps = _require_object(workflow, "steps", issues, "workflow.steps")
    for required in sorted(REQUIRED_STEPS - set(steps)):
        issues.append(
            Issue(
                "error",
                "workflow.step.required",
                f"Missing required workflow step: {required}",
                f"workflow.steps.{required}",
            )
        )
    for name, step in steps.items():
        if not isinstance(step, dict):
            issues.append(
                Issue(
                    "error",
                    "workflow.step.type",
                    f"Workflow step {name} must be an object",
                    f"workflow.steps.{name}",
                )
            )
            continue
        status = step.get("status")
        reason = step.get("reason")
        if not isinstance(status, str) or status not in STEP_STATUSES:
            issues.append(
                Issue(
                    "error",
                    "workflow.step.status",
                    f"Invalid workflow status for {name}: {status}",
                    f"workflow.steps.{name}.status",
                )
            )
        if (
            isinstance(status, str)
            and status in {"skipped", "not-applicable"}
            and not str(reason or "").strip()
        ):
            issues.append(
                Issue(
                    "error",
                    "workflow.step.reason",
                    f"Skipped workflow step {name} requires a reason",
                    f"workflow.steps.{name}.reason",
                )
            )

    assets = _require_list(data, "assets", issues, "assets")
    asset_ids: list[str] = []
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            issues.append(
                Issue("error", "asset.type", "Asset must be an object", f"assets[{index}]")
            )
            continue
        asset_id = asset.get("id")
        if not isinstance(asset_id, str) or not asset_id:
            issues.append(
                Issue(
                    "error",
                    "asset.id",
                    "Asset requires a non-empty id",
                    f"assets[{index}].id",
                )
            )
        else:
            asset_ids.append(asset_id)
    _check_unique(asset_ids, "asset id", "assets", issues)
    asset_id_set = set(asset_ids)

    slides = _require_list(data, "slides", issues, "slides")
    slide_ids: list[str] = []
    slide_numbers: list[int] = []
    for index, slide in enumerate(slides):
        if not isinstance(slide, dict):
            issues.append(
                Issue("error", "slide.type", "Slide must be an object", f"slides[{index}]")
            )
            continue
        slide_id = slide.get("id")
        number = slide.get("number")
        if not isinstance(slide_id, str) or not slide_id:
            issues.append(
                Issue(
                    "error",
                    "slide.id",
                    "Slide requires a non-empty id",
                    f"slides[{index}].id",
                )
            )
        else:
            slide_ids.append(slide_id)
        if not isinstance(number, int) or isinstance(number, bool) or number < 1:
            issues.append(
                Issue(
                    "error",
                    "slide.number",
                    "Slide number must be a positive integer",
                    f"slides[{index}].number",
                )
            )
        else:
            slide_numbers.append(number)
        for key in ("title", "core_message"):
            if not isinstance(slide.get(key), str) or not slide.get(key, "").strip():
                issues.append(
                    Issue(
                        "error",
                        "slide.content",
                        f"Slide requires non-empty {key}",
                        f"slides[{index}].{key}",
                    )
                )
        refs = slide.get("source_asset_ids", [])
        if not isinstance(refs, list):
            issues.append(
                Issue(
                    "error",
                    "slide.assets",
                    "source_asset_ids must be an array",
                    f"slides[{index}].source_asset_ids",
                )
            )
        else:
            for asset_id in refs:
                if isinstance(asset_id, str) and asset_id not in asset_id_set:
                    issues.append(
                        Issue(
                            "error",
                            "reference.asset",
                            f"Unknown source asset id: {asset_id}",
                            f"slides[{index}].source_asset_ids",
                        )
                    )
        render = slide.get("render")
        if render is not None and not isinstance(render, dict):
            issues.append(
                Issue(
                    "error",
                    "slide.render",
                    "render must be an object when present",
                    f"slides[{index}].render",
                )
            )
        elif isinstance(render, dict):
            effective_render_type = infer_render_type(slide)
            render_asset_ids = render.get("asset_ids", [])
            effective_asset_ids = (
                render_asset_ids
                if "asset_ids" in render and isinstance(render_asset_ids, list)
                else refs if isinstance(refs, list) else []
            )
            if isinstance(render_asset_ids, list):
                for asset_id in render_asset_ids:
                    if not isinstance(asset_id, str):
                        continue
                    if asset_id not in asset_id_set:
                        issues.append(
                            Issue(
                                "error",
                                "reference.asset",
                                f"Unknown render asset id: {asset_id}",
                                f"slides[{index}].render.asset_ids",
                            )
                        )
                    if isinstance(refs, list) and asset_id not in refs:
                        issues.append(
                            Issue(
                                "error",
                                "reference.render_asset",
                                f"Render asset {asset_id} is not listed in "
                                "source_asset_ids",
                                f"slides[{index}].render.asset_ids",
                            )
                        )
            items = render.get("items", [])
            item_asset_ids: list[str] = []
            if isinstance(items, list):
                for item_index, item in enumerate(items):
                    if not isinstance(item, dict):
                        continue
                    item_asset_id = item.get("asset_id")
                    if not isinstance(item_asset_id, str):
                        continue
                    item_asset_ids.append(item_asset_id)
                    if item_asset_id not in asset_id_set:
                        issues.append(
                            Issue(
                                "error",
                                "reference.asset",
                                f"Unknown render item asset id: {item_asset_id}",
                                f"slides[{index}].render.items[{item_index}].asset_id",
                            )
                        )
                    if isinstance(refs, list) and item_asset_id not in refs:
                        issues.append(
                            Issue(
                                "error",
                                "reference.render_asset",
                                f"Render item asset {item_asset_id} is not listed in "
                                "source_asset_ids",
                                f"slides[{index}].render.items[{item_index}].asset_id",
                            )
                        )
            if effective_render_type in {"comparison", "multi-panel"}:
                effective_set = {
                    item for item in effective_asset_ids if isinstance(item, str)
                }
                for item_asset_id in item_asset_ids:
                    if item_asset_id not in effective_set:
                        issues.append(
                            Issue(
                                "error",
                                "reference.render_item_mapping",
                                f"Render item asset {item_asset_id} is not selected "
                                "by the effective render asset list",
                                f"slides[{index}].render.items",
                            )
                        )

            ignored_asset_ids = render.get("ignored_asset_ids", [])
            if isinstance(ignored_asset_ids, list):
                selected = (
                    {
                        item
                        for item in effective_asset_ids
                        if isinstance(item, str)
                    }
                    if effective_render_type
                    in {"cover", "figure", "comparison", "multi-panel"}
                    else set()
                )
                for ignored_asset_id in ignored_asset_ids:
                    if not isinstance(ignored_asset_id, str):
                        continue
                    if isinstance(refs, list) and ignored_asset_id not in refs:
                        issues.append(
                            Issue(
                                "error",
                                "reference.ignored_asset",
                                f"Ignored asset {ignored_asset_id} is not listed in "
                                "source_asset_ids",
                                f"slides[{index}].render.ignored_asset_ids",
                            )
                        )
                    if ignored_asset_id in selected:
                        issues.append(
                            Issue(
                                "error",
                                "reference.ignored_asset",
                                f"Asset {ignored_asset_id} cannot be both selected "
                                "and ignored",
                                f"slides[{index}].render.ignored_asset_ids",
                            )
                        )
                if ignored_asset_ids and (
                    not isinstance(render.get("ignore_reason"), str)
                    or not render.get("ignore_reason", "").strip()
                ):
                    issues.append(
                        Issue(
                            "error",
                            "slide.ignore_reason",
                            "ignored_asset_ids requires a non-empty ignore_reason",
                            f"slides[{index}].render.ignore_reason",
                        )
                    )

            limits = RENDER_CONTENT_LIMITS.get(effective_render_type, {})
            content_field: str | None = None
            content_count = 0
            if isinstance(items, list) and items:
                content_field = "items"
                content_count = len(items)
            else:
                body = render.get("body", [])
                if isinstance(body, list) and body:
                    content_field = "body"
                    content_count = len(body)
            if content_field in limits and content_count > limits[content_field]:
                maximum = limits[content_field]
                issues.append(
                    Issue(
                        "error",
                        "slide.render_content_count",
                        f"{effective_render_type} render supports at most {maximum} "
                        f"{content_field} entries; found {content_count}",
                        f"slides[{index}].render.{content_field}",
                    )
                )

        if render is None or isinstance(render, dict):
            render_data = render if isinstance(render, dict) else {}
            effective_render_type = infer_render_type(slide)
            render_asset_ids = render_data.get("asset_ids", [])
            effective_asset_ids = (
                render_asset_ids
                if "asset_ids" in render_data and isinstance(render_asset_ids, list)
                else refs if isinstance(refs, list) else []
            )
            effective_count = len(
                [item for item in effective_asset_ids if isinstance(item, str)]
            )
            count_rules = {
                "cover": (0, 1, "at most one"),
                "figure": (1, 1, "exactly one"),
                "comparison": (2, 2, "exactly two"),
                "multi-panel": (2, 4, "between two and four"),
            }
            if effective_render_type in count_rules:
                minimum, maximum, label = count_rules[effective_render_type]
                if not minimum <= effective_count <= maximum:
                    issues.append(
                        Issue(
                            "error",
                            "slide.render_asset_count",
                            f"{effective_render_type} render requires {label} effective "
                            f"asset_ids; found {effective_count}",
                            f"slides[{index}].render.asset_ids",
                        )
                    )
    _check_unique(slide_ids, "slide id", "slides", issues)
    _check_unique(slide_numbers, "slide number", "slides", issues)
    slide_id_set = set(slide_ids)
    if slide_numbers and sorted(slide_numbers) != list(range(1, len(slide_numbers) + 1)):
        issues.append(
            Issue(
                "error",
                "slide.number_sequence",
                "Slide numbers must be contiguous and start at 1",
                "slides",
            )
        )

    asset_used_on_slides: dict[str, set[str]] = {}
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            continue
        asset_id = asset.get("id")
        used_on_slides = asset.get("used_on_slides", [])
        if not isinstance(used_on_slides, list):
            issues.append(
                Issue(
                    "error",
                    "asset.slides",
                    "used_on_slides must be an array",
                    f"assets[{index}].used_on_slides",
                )
            )
            continue
        valid_slide_refs = {
            slide_id for slide_id in used_on_slides if isinstance(slide_id, str)
        }
        if isinstance(asset_id, str):
            asset_used_on_slides[asset_id] = valid_slide_refs
        for slide_id in valid_slide_refs:
            if slide_id not in slide_id_set:
                issues.append(
                    Issue(
                        "error",
                        "reference.slide",
                        f"Asset references unknown slide id: {slide_id}",
                        f"assets[{index}].used_on_slides",
                    )
                )

    slide_source_assets: dict[str, set[str]] = {}
    for slide in slides:
        if not isinstance(slide, dict):
            continue
        slide_id = slide.get("id")
        refs = slide.get("source_asset_ids", [])
        if isinstance(slide_id, str) and isinstance(refs, list):
            slide_source_assets[slide_id] = {
                asset_id for asset_id in refs if isinstance(asset_id, str)
            }

    for slide_id, source_asset_ids in slide_source_assets.items():
        for asset_id in source_asset_ids & asset_id_set:
            if slide_id not in asset_used_on_slides.get(asset_id, set()):
                issues.append(
                    Issue(
                        "error",
                        "reference.asset_reverse",
                        f"Slide {slide_id} uses asset {asset_id}, but the asset does not "
                        "list the slide",
                        f"slides[{slide_ids.index(slide_id)}].source_asset_ids",
                    )
                )
    for asset_index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            continue
        asset_id = asset.get("id")
        if not isinstance(asset_id, str):
            continue
        for slide_id in asset_used_on_slides.get(asset_id, set()) & slide_id_set:
            if asset_id not in slide_source_assets.get(slide_id, set()):
                issues.append(
                    Issue(
                        "error",
                        "reference.slide_reverse",
                        f"Asset {asset_id} lists slide {slide_id}, but the slide does not "
                        "use the asset",
                        f"assets[{asset_index}].used_on_slides",
                    )
                )

    visual = _require_object(data, "visual_system", issues, "visual_system")
    families = _require_list(visual, "families", issues, "visual_system.families")
    variants = _require_list(visual, "variants", issues, "visual_system.variants")
    family_ids = [
        item.get("id")
        for item in families
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]
    variant_ids = [
        item.get("id")
        for item in variants
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]
    _check_unique(family_ids, "family id", "visual_system.families", issues)
    _check_unique(variant_ids, "variant id", "visual_system.variants", issues)
    family_id_set = set(family_ids)
    variant_id_set = set(variant_ids)

    variant_by_id = {
        item["id"]: item
        for item in variants
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    family_slide_ids: dict[str, set[str]] = {}
    variant_slide_ids: dict[str, set[str]] = {}
    slide_family_memberships: dict[str, set[str]] = {}
    slide_variant_memberships: dict[str, set[str]] = {}

    for index, family in enumerate(families):
        if not isinstance(family, dict):
            continue
        family_id = family.get("id")
        listed_slides = family.get("slide_ids", [])
        if not isinstance(family_id, str) or not isinstance(listed_slides, list):
            continue
        valid_listed_slides = {
            slide_id for slide_id in listed_slides if isinstance(slide_id, str)
        }
        family_slide_ids[family_id] = valid_listed_slides
        for slide_id in valid_listed_slides:
            slide_family_memberships.setdefault(slide_id, set()).add(family_id)
            if slide_id not in slide_id_set:
                issues.append(
                    Issue(
                        "error",
                        "reference.slide",
                        f"Family references unknown slide id: {slide_id}",
                        f"visual_system.families[{index}].slide_ids",
                    )
                )

    for slide_id, memberships in slide_family_memberships.items():
        if slide_id in slide_id_set and len(memberships) > 1:
            issues.append(
                Issue(
                    "error",
                    "reference.family_membership",
                    f"Slide {slide_id} is assigned to multiple families: "
                    f"{', '.join(sorted(memberships))}",
                    "visual_system.families",
                )
            )

    for index, variant in enumerate(variants):
        if not isinstance(variant, dict):
            continue
        variant_id = variant.get("id")
        family_id = variant.get("family_id")
        if isinstance(family_id, str) and family_id not in family_id_set:
            issues.append(
                Issue(
                    "error",
                    "reference.family",
                    f"Variant references unknown family: {family_id}",
                    f"visual_system.variants[{index}].family_id",
                )
            )
        listed_slides = variant.get("slide_ids", [])
        if not isinstance(variant_id, str) or not isinstance(listed_slides, list):
            continue
        valid_listed_slides = {
            slide_id for slide_id in listed_slides if isinstance(slide_id, str)
        }
        variant_slide_ids[variant_id] = valid_listed_slides
        for slide_id in valid_listed_slides:
            slide_variant_memberships.setdefault(slide_id, set()).add(variant_id)
            if slide_id not in slide_id_set:
                issues.append(
                    Issue(
                        "error",
                        "reference.slide",
                        f"Variant references unknown slide id: {slide_id}",
                        f"visual_system.variants[{index}].slide_ids",
                    )
                )
            if (
                isinstance(family_id, str)
                and family_id in family_id_set
                and slide_id not in family_slide_ids.get(family_id, set())
            ):
                issues.append(
                    Issue(
                        "error",
                        "reference.variant_family_membership",
                        f"Variant {variant_id} lists slide {slide_id}, but family "
                        f"{family_id} does not list it",
                        f"visual_system.variants[{index}].slide_ids",
                    )
                )

    for slide_id, memberships in slide_variant_memberships.items():
        if slide_id in slide_id_set and len(memberships) > 1:
            issues.append(
                Issue(
                    "error",
                    "reference.variant_membership",
                    f"Slide {slide_id} is assigned to multiple variants: "
                    f"{', '.join(sorted(memberships))}",
                    "visual_system.variants",
                )
            )

    for index, slide in enumerate(slides):
        if not isinstance(slide, dict):
            continue
        layout = slide.get("layout", {})
        if not isinstance(layout, dict):
            issues.append(
                Issue(
                    "error",
                    "slide.layout",
                    "Slide layout must be an object",
                    f"slides[{index}].layout",
                )
            )
            continue
        family_id = layout.get("family_id")
        variant_id = layout.get("variant_id")
        slide_id = slide.get("id")
        if (
            family_id is not None
            and isinstance(family_id, str)
            and family_id not in family_id_set
        ):
            issues.append(
                Issue(
                    "error",
                    "reference.family",
                    f"Slide references unknown family: {family_id}",
                    f"slides[{index}].layout.family_id",
                )
            )
        if (
            variant_id is not None
            and isinstance(variant_id, str)
            and variant_id not in variant_id_set
        ):
            issues.append(
                Issue(
                    "error",
                    "reference.variant",
                    f"Slide references unknown variant: {variant_id}",
                    f"slides[{index}].layout.variant_id",
                )
            )
        if isinstance(slide_id, str) and isinstance(family_id, str):
            if (
                family_id in family_id_set
                and slide_id not in family_slide_ids.get(family_id, set())
            ):
                issues.append(
                    Issue(
                        "error",
                        "reference.family_reverse",
                        f"Slide {slide_id} selects family {family_id}, but the family "
                        "does not list the slide",
                        f"slides[{index}].layout.family_id",
                    )
                )
        if isinstance(slide_id, str):
            for listed_family_id in slide_family_memberships.get(slide_id, set()):
                if family_id != listed_family_id:
                    issues.append(
                        Issue(
                            "error",
                            "reference.slide_family",
                            f"Family {listed_family_id} lists slide {slide_id}, but the "
                            f"slide selects {family_id!r}",
                            f"slides[{index}].layout.family_id",
                        )
                    )
        if isinstance(variant_id, str) and variant_id in variant_id_set:
            variant_family_id = variant_by_id[variant_id].get("family_id")
            if family_id != variant_family_id:
                issues.append(
                    Issue(
                        "error",
                        "reference.variant_family",
                        f"Slide {slide_id} selects variant {variant_id} from family "
                        f"{variant_family_id}, but selects family {family_id!r}",
                        f"slides[{index}].layout.variant_id",
                    )
                )
            if (
                isinstance(slide_id, str)
                and slide_id not in variant_slide_ids.get(variant_id, set())
            ):
                issues.append(
                    Issue(
                        "error",
                        "reference.variant_reverse",
                        f"Slide {slide_id} selects variant {variant_id}, but the variant "
                        "does not list the slide",
                        f"slides[{index}].layout.variant_id",
                    )
                )
        if isinstance(slide_id, str):
            for listed_variant_id in slide_variant_memberships.get(slide_id, set()):
                if variant_id != listed_variant_id:
                    issues.append(
                        Issue(
                            "error",
                            "reference.slide_variant",
                            f"Variant {listed_variant_id} lists slide {slide_id}, but the "
                            f"slide selects {variant_id!r}",
                            f"slides[{index}].layout.variant_id",
                        )
                    )

    sample_ids = visual.get("sample_slide_ids", [])
    if not isinstance(sample_ids, list):
        issues.append(
            Issue(
                "error",
                "visual.samples",
                "sample_slide_ids must be an array",
                "visual_system.sample_slide_ids",
            )
        )
    else:
        for slide_id in sample_ids:
            if isinstance(slide_id, str) and slide_id not in slide_id_set:
                issues.append(
                    Issue(
                        "error",
                        "reference.slide",
                        f"Unknown sample slide id: {slide_id}",
                        "visual_system.sample_slide_ids",
                    )
                )

    artifacts = _require_object(data, "artifacts", issues, "artifacts")
    qa = _require_object(data, "qa", issues, "qa")
    editable_step = steps.get("editable-pptx")
    static_qa_step = steps.get("static-qa")
    visual_samples_step = steps.get("visual-samples")
    if (
        isinstance(editable_step, dict)
        and editable_step.get("status") == "completed"
        and (
            not isinstance(artifacts.get("pptx"), str)
            or not artifacts.get("pptx", "").strip()
        )
    ):
        issues.append(
            Issue(
                "error",
                "workflow.artifact",
                "Completed editable-pptx step requires artifacts.pptx",
                "artifacts.pptx",
            )
        )
    if isinstance(static_qa_step, dict) and static_qa_step.get("status") == "completed":
        qa_status = qa.get("status")
        if (
            not isinstance(qa_status, str)
            or qa_status not in {"passed", "passed-with-warnings", "failed"}
        ):
            issues.append(
                Issue(
                    "error",
                    "workflow.qa_status",
                    "Completed static-qa step requires a completed qa.status",
                    "qa.status",
                )
            )
        if (
            not isinstance(artifacts.get("qa_report"), str)
            or not artifacts.get("qa_report", "").strip()
        ):
            issues.append(
                Issue(
                    "error",
                    "workflow.artifact",
                    "Completed static-qa step requires artifacts.qa_report",
                    "artifacts.qa_report",
                )
            )
    if (
        isinstance(visual_samples_step, dict)
        and visual_samples_step.get("status") == "completed"
        and (not isinstance(sample_ids, list) or not sample_ids)
    ):
        issues.append(
            Issue(
                "error",
                "workflow.visual_samples",
                "Completed visual-samples step requires sample_slide_ids",
                "visual_system.sample_slide_ids",
            )
        )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate scholar-ppt-cn project JSON.")
    parser.add_argument("project", type=Path)
    parser.add_argument("--report", type=Path, help="Write the JSON validation report.")
    args = parser.parse_args()

    try:
        data = load_json(args.project)
        issues = validate_project(data)
        report = make_report(
            "validate_project",
            issues,
            project=str(args.project),
            schema_version=data.get("schema_version"),
        )
    except (OSError, ValueError) as exc:
        report = make_report(
            "validate_project",
            [Issue("error", "input.read", str(exc), str(args.project))],
            project=str(args.project),
        )

    if args.report:
        write_json(args.report, report)
    print_report(report)
    return 1 if report["summary"]["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
