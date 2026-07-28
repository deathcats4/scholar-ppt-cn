from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.common import Issue, load_json, make_report, print_report, write_json
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
    if template.get("source") in {"user", "existing-deck"} and not template.get("path"):
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
        if value.get("available") not in {True, False, None}:
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
        if status not in STEP_STATUSES:
            issues.append(
                Issue(
                    "error",
                    "workflow.step.status",
                    f"Invalid workflow status for {name}: {status}",
                    f"workflow.steps.{name}.status",
                )
            )
        if status in {"skipped", "not-applicable"} and not str(reason or "").strip():
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
                if asset_id not in asset_id_set:
                    issues.append(
                        Issue(
                            "error",
                            "reference.asset",
                            f"Unknown source asset id: {asset_id}",
                            f"slides[{index}].source_asset_ids",
                        )
                    )
    _check_unique(slide_ids, "slide id", "slides", issues)
    _check_unique(slide_numbers, "slide number", "slides", issues)
    slide_id_set = set(slide_ids)

    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            continue
        for slide_id in asset.get("used_on_slides", []):
            if slide_id not in slide_id_set:
                issues.append(
                    Issue(
                        "error",
                        "reference.slide",
                        f"Asset references unknown slide id: {slide_id}",
                        f"assets[{index}].used_on_slides",
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

    for index, variant in enumerate(variants):
        if isinstance(variant, dict) and variant.get("family_id") not in family_id_set:
            issues.append(
                Issue(
                    "error",
                    "reference.family",
                    f"Variant references unknown family: {variant.get('family_id')}",
                    f"visual_system.variants[{index}].family_id",
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
        if family_id is not None and family_id not in family_id_set:
            issues.append(
                Issue(
                    "error",
                    "reference.family",
                    f"Slide references unknown family: {family_id}",
                    f"slides[{index}].layout.family_id",
                )
            )
        if variant_id is not None and variant_id not in variant_id_set:
            issues.append(
                Issue(
                    "error",
                    "reference.variant",
                    f"Slide references unknown variant: {variant_id}",
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
            if slide_id not in slide_id_set:
                issues.append(
                    Issue(
                        "error",
                        "reference.slide",
                        f"Unknown sample slide id: {slide_id}",
                        "visual_system.sample_slide_ids",
                    )
                )

    _require_object(data, "artifacts", issues, "artifacts")
    _require_object(data, "qa", issues, "qa")
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
