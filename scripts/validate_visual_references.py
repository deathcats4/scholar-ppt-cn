from __future__ import annotations

import argparse
import json
import struct
import sys
import zlib
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.common import Issue, load_json, make_report, print_report, write_json
from scripts.schema_validation import validate_against_schema


ROOT = Path(__file__).resolve().parents[1]
PACK_SCHEMA = ROOT / "schemas" / "visual-reference-pack.schema.json"
ITEM_SCHEMA = ROOT / "schemas" / "visual-reference-item.schema.json"
PLAN_SCHEMA = ROOT / "schemas" / "visual-reference-generation-plan.schema.json"
FAMILY_PLAN_SCHEMA = (
    ROOT / "schemas" / "visual-reference-family-generation-plan.schema.json"
)
CORE_REFERENCE_ROLES = {
    "cover",
    "research-gap",
    "research-question",
    "method-design",
    "dominant-result",
    "comparison",
    "multi-panel",
    "mechanism",
    "discussion-outlook",
    "conclusion",
}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_CHANNELS = {
    0: 1,
    2: 3,
    3: 1,
    4: 2,
    6: 4,
}
PNG_BIT_DEPTHS = {
    0: {1, 2, 4, 8, 16},
    2: {8, 16},
    3: {1, 2, 4, 8},
    4: {8, 16},
    6: {8, 16},
}
ADAM7_PASSES = (
    (0, 0, 8, 8),
    (4, 0, 8, 8),
    (0, 4, 4, 8),
    (2, 0, 4, 4),
    (0, 2, 2, 4),
    (1, 0, 2, 2),
    (0, 1, 1, 2),
)
MAX_DECODED_PNG_BYTES = 256 * 1024 * 1024


def _pass_size(size: int, start: int, step: int) -> int:
    if size <= start:
        return 0
    return (size - start + step - 1) // step


def _png_scanlines(
    width: int,
    height: int,
    channels: int,
    bit_depth: int,
    interlace: int,
) -> list[tuple[int, int]]:
    passes = ((0, 0, 1, 1),) if interlace == 0 else ADAM7_PASSES
    result: list[tuple[int, int]] = []
    for start_x, start_y, step_x, step_y in passes:
        pass_width = _pass_size(width, start_x, step_x)
        pass_height = _pass_size(height, start_y, step_y)
        if not pass_width or not pass_height:
            continue
        row_bytes = (pass_width * channels * bit_depth + 7) // 8
        result.append((pass_height, row_bytes))
    return result


def _validate_png(path: Path) -> tuple[int, int]:
    payload = path.read_bytes()
    if len(payload) < 8 or payload[:8] != PNG_SIGNATURE:
        raise ValueError("File is not a valid PNG")

    offset = 8
    chunk_index = 0
    ihdr: bytes | None = None
    idat: list[bytes] = []
    has_palette = False
    has_iend = False
    while offset < len(payload):
        if len(payload) - offset < 12:
            raise ValueError("PNG is truncated before a complete chunk")
        length = struct.unpack(">I", payload[offset : offset + 4])[0]
        chunk_type = payload[offset + 4 : offset + 8]
        chunk_end = offset + 12 + length
        if chunk_end > len(payload):
            raise ValueError("PNG chunk extends beyond the end of the file")
        chunk_data = payload[offset + 8 : offset + 8 + length]
        expected_crc = struct.unpack(
            ">I", payload[offset + 8 + length : chunk_end]
        )[0]
        actual_crc = zlib.crc32(chunk_type)
        actual_crc = zlib.crc32(chunk_data, actual_crc) & 0xFFFFFFFF
        if actual_crc != expected_crc:
            name = chunk_type.decode("ascii", errors="replace")
            raise ValueError(f"PNG chunk CRC mismatch: {name}")

        if chunk_index == 0 and chunk_type != b"IHDR":
            raise ValueError("PNG must begin with an IHDR chunk")
        if chunk_type == b"IHDR":
            if ihdr is not None or length != 13:
                raise ValueError("PNG contains an invalid IHDR chunk")
            ihdr = chunk_data
        elif chunk_type == b"PLTE":
            has_palette = True
        elif chunk_type == b"IDAT":
            idat.append(chunk_data)
        elif chunk_type == b"IEND":
            if length != 0:
                raise ValueError("PNG contains an invalid IEND chunk")
            has_iend = True
            offset = chunk_end
            if offset != len(payload):
                raise ValueError("PNG contains trailing data after IEND")
            break

        offset = chunk_end
        chunk_index += 1

    if ihdr is None or not idat or not has_iend:
        raise ValueError("PNG is missing IHDR, IDAT, or IEND data")

    width, height, bit_depth, color_type, compression, filter_method, interlace = (
        struct.unpack(">IIBBBBB", ihdr)
    )
    if width == 0 or height == 0:
        raise ValueError("PNG dimensions must be positive")
    if color_type not in PNG_CHANNELS or bit_depth not in PNG_BIT_DEPTHS[color_type]:
        raise ValueError("PNG uses an unsupported color type or bit depth")
    if compression != 0 or filter_method != 0 or interlace not in {0, 1}:
        raise ValueError("PNG uses an unsupported encoding method")
    if color_type == 3 and not has_palette:
        raise ValueError("Indexed PNG is missing its palette")

    scanlines = _png_scanlines(
        width,
        height,
        PNG_CHANNELS[color_type],
        bit_depth,
        interlace,
    )
    expected_size = sum(rows * (row_bytes + 1) for rows, row_bytes in scanlines)
    if expected_size > MAX_DECODED_PNG_BYTES:
        raise ValueError("Decoded PNG exceeds the validation size limit")

    decoder = zlib.decompressobj()
    decoded = decoder.decompress(b"".join(idat), expected_size + 1)
    if decoder.unconsumed_tail or len(decoded) > expected_size:
        raise ValueError("PNG expands beyond its declared dimensions")
    decoded += decoder.flush()
    if not decoder.eof or decoder.unused_data:
        raise ValueError("PNG contains incomplete or trailing compressed image data")
    if len(decoded) != expected_size:
        raise ValueError("PNG decoded data does not match its declared dimensions")

    decoded_offset = 0
    for rows, row_bytes in scanlines:
        for _ in range(rows):
            if decoded[decoded_offset] > 4:
                raise ValueError("PNG contains an invalid scanline filter")
            decoded_offset += row_bytes + 1
    return width, height


def _schema_issues(value: dict[str, Any], schema_path: Path, path: str) -> list[Issue]:
    schema = load_json(schema_path)
    return validate_against_schema(value, schema, path)


def validate_pack(pack_path: Path) -> dict[str, Any]:
    issues: list[Issue] = []
    pack = load_json(pack_path)
    issues.extend(_schema_issues(pack, PACK_SCHEMA, "pack"))
    references = pack.get("references")
    if not isinstance(references, list):
        references = []
    if pack.get("status") == "active" and not references:
        issues.append(
            Issue(
                "error",
                "visual_pack.active_empty",
                "An active visual reference pack must contain approved references",
                "pack.references",
            )
        )

    seen_ids: set[str] = set()
    seen_files: set[str] = set()
    seen_roles: set[str] = set()
    for index, entry in enumerate(references):
        entry_path = f"pack.references[{index}]"
        if not isinstance(entry, dict):
            continue
        reference_id = entry.get("id")
        image_relative = entry.get("file")
        metadata_relative = entry.get("metadata_file")
        if isinstance(reference_id, str):
            if reference_id in seen_ids:
                issues.append(
                    Issue(
                        "error",
                        "visual_pack.duplicate_id",
                        f"Duplicate reference ID: {reference_id}",
                        f"{entry_path}.id",
                    )
                )
            seen_ids.add(reference_id)
        for value, suffix in (
            (image_relative, "file"),
            (metadata_relative, "metadata_file"),
        ):
            if isinstance(value, str):
                if value in seen_files:
                    issues.append(
                        Issue(
                            "error",
                            "visual_pack.duplicate_path",
                            f"Duplicate reference path: {value}",
                            f"{entry_path}.{suffix}",
                        )
                    )
                seen_files.add(value)

        if not isinstance(image_relative, str) or not isinstance(metadata_relative, str):
            continue
        image_path = pack_path.parent / image_relative
        metadata_path = pack_path.parent / metadata_relative
        if not image_path.is_file():
            issues.append(
                Issue(
                    "error",
                    "visual_pack.image_missing",
                    f"Reference image does not exist: {image_relative}",
                    f"{entry_path}.file",
                )
            )
        else:
            try:
                width, height = _validate_png(image_path)
                if (width, height) != (1600, 900):
                    issues.append(
                        Issue(
                            "error",
                            "visual_pack.image_size",
                            f"Expected 1600x900 PNG, got {width}x{height}",
                            f"{entry_path}.file",
                        )
                    )
            except (OSError, ValueError) as exc:
                issues.append(
                    Issue(
                        "error",
                        "visual_pack.image_invalid",
                        str(exc),
                        f"{entry_path}.file",
                    )
                )
        if not metadata_path.is_file():
            issues.append(
                Issue(
                    "error",
                    "visual_pack.metadata_missing",
                    f"Reference metadata does not exist: {metadata_relative}",
                    f"{entry_path}.metadata_file",
                )
            )
            continue
        try:
            metadata = load_json(metadata_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            issues.append(
                Issue(
                    "error",
                    "visual_pack.metadata_invalid",
                    str(exc),
                    f"{entry_path}.metadata_file",
                )
            )
            continue
        issues.extend(_schema_issues(metadata, ITEM_SCHEMA, f"metadata.{reference_id}"))
        metadata_role = metadata.get("role")
        if isinstance(metadata_role, str):
            seen_roles.add(metadata_role)
        if metadata.get("id") != reference_id:
            issues.append(
                Issue(
                    "error",
                    "visual_pack.metadata_id",
                    "Metadata ID does not match the pack index",
                    f"{entry_path}.metadata_file",
                )
            )
        expected_image = f"../{image_relative}"
        if metadata.get("file") != expected_image:
            issues.append(
                Issue(
                    "error",
                    "visual_pack.metadata_image",
                    f"Metadata file must point to {expected_image}",
                    f"{entry_path}.metadata_file",
                )
            )

    if pack.get("status") == "active":
        missing_roles = CORE_REFERENCE_ROLES - seen_roles
        if missing_roles:
            issues.append(
                Issue(
                    "error",
                    "visual_pack.active_incomplete",
                    (
                        "An active visual reference pack must cover every core role; "
                        f"missing={sorted(missing_roles)}"
                    ),
                    "pack.references",
                )
            )

    return make_report(
        "validate_visual_reference_pack",
        issues,
        pack=str(pack_path),
        reference_count=len(references),
    )


def validate_plan(plan_path: Path) -> dict[str, Any]:
    issues: list[Issue] = []
    plan = load_json(plan_path)
    issues.extend(_schema_issues(plan, PLAN_SCHEMA, "plan"))
    tasks = plan.get("tasks")
    if not isinstance(tasks, list):
        tasks = []
    by_id = {
        task.get("id"): task
        for task in tasks
        if isinstance(task, dict) and isinstance(task.get("id"), str)
    }
    if len(by_id) != len(tasks):
        issues.append(
            Issue(
                "error",
                "visual_plan.duplicate_task_id",
                "Generation task IDs must be unique",
                "plan.tasks",
            )
        )

    pairs: dict[str, set[str]] = {}
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            continue
        pair_id = task.get("pair_id")
        variant = task.get("variant")
        if isinstance(pair_id, str) and isinstance(variant, str):
            pairs.setdefault(pair_id, set()).add(variant)
        source_task_id = task.get("source_task_id")
        if variant == "B-neutral-simulated":
            source = by_id.get(source_task_id)
            if not isinstance(source, dict) or source.get("variant") != "A-realistic-synthetic":
                issues.append(
                    Issue(
                        "error",
                        "visual_plan.invalid_source",
                        "Every B task must reference its A task",
                        f"plan.tasks[{index}].source_task_id",
                    )
                )
            elif source.get("pair_id") != pair_id:
                issues.append(
                    Issue(
                        "error",
                        "visual_plan.source_pair",
                        "A and B tasks must share the same pair_id",
                        f"plan.tasks[{index}].source_task_id",
                    )
                )
        elif source_task_id is not None:
            issues.append(
                Issue(
                    "error",
                    "visual_plan.a_has_source",
                    "An A task must not reference another task",
                    f"plan.tasks[{index}].source_task_id",
                )
            )
    expected_variants = {"A-realistic-synthetic", "B-neutral-simulated"}
    for pair_id, variants in sorted(pairs.items()):
        if variants != expected_variants:
            issues.append(
                Issue(
                    "error",
                    "visual_plan.incomplete_pair",
                    f"Pair {pair_id} must contain one A and one B task",
                    "plan.tasks",
                )
            )
    if len(pairs) != 3:
        issues.append(
            Issue(
                "error",
                "visual_plan.pair_count",
                f"The initial experiment requires exactly 3 A/B pairs, got {len(pairs)}",
                "plan.tasks",
            )
        )
    return make_report(
        "validate_visual_reference_generation_plan",
        issues,
        plan=str(plan_path),
        task_count=len(tasks),
        pair_count=len(pairs),
    )


def validate_family_plan(plan_path: Path) -> dict[str, Any]:
    issues: list[Issue] = []
    plan = load_json(plan_path)
    issues.extend(_schema_issues(plan, FAMILY_PLAN_SCHEMA, "family_plan"))
    roles = plan.get("roles")
    if not isinstance(roles, list):
        roles = []
    expected_roles = {
        "cover",
        "research-gap",
        "research-question",
        "method-design",
        "comparison",
        "multi-panel",
        "mechanism",
        "discussion-outlook",
        "conclusion",
    }
    seen_roles: set[str] = set()
    seen_ids: set[str] = set()
    variant_count = 0
    for role_index, role in enumerate(roles):
        if not isinstance(role, dict):
            continue
        role_id = role.get("role")
        if isinstance(role_id, str):
            if role_id in seen_roles:
                issues.append(
                    Issue(
                        "error",
                        "visual_family.duplicate_role",
                        f"Duplicate role: {role_id}",
                        f"family_plan.roles[{role_index}].role",
                    )
                )
            seen_roles.add(role_id)
        variants = role.get("variants")
        if not isinstance(variants, list):
            variants = []
        if len(variants) < 3:
            issues.append(
                Issue(
                    "error",
                    "visual_family.variant_count",
                    f"Role {role_id} must contain at least 3 variants",
                    f"family_plan.roles[{role_index}].variants",
                )
            )
        for variant_index, variant in enumerate(variants):
            if not isinstance(variant, dict):
                continue
            variant_count += 1
            variant_id = variant.get("id")
            if isinstance(variant_id, str):
                if variant_id in seen_ids:
                    issues.append(
                        Issue(
                            "error",
                            "visual_family.duplicate_variant",
                            f"Duplicate variant ID: {variant_id}",
                            (
                                f"family_plan.roles[{role_index}]"
                                f".variants[{variant_index}].id"
                            ),
                        )
                    )
                seen_ids.add(variant_id)
                if isinstance(role_id, str) and not variant_id.startswith(f"{role_id}-"):
                    issues.append(
                        Issue(
                            "error",
                            "visual_family.variant_role",
                            f"Variant {variant_id} does not match role {role_id}",
                            (
                                f"family_plan.roles[{role_index}]"
                                f".variants[{variant_index}].id"
                            ),
                        )
                    )
                expected_file = f"candidates/{variant_id}.png"
                if variant.get("output_file") != expected_file:
                    issues.append(
                        Issue(
                            "error",
                            "visual_family.output_file",
                            f"Output file must be {expected_file}",
                            (
                                f"family_plan.roles[{role_index}]"
                                f".variants[{variant_index}].output_file"
                            ),
                        )
                    )
    missing_roles = expected_roles - seen_roles
    extra_roles = seen_roles - expected_roles
    if missing_roles or extra_roles:
        issues.append(
            Issue(
                "error",
                "visual_family.role_set",
                (
                    f"Expected roles {sorted(expected_roles)}; "
                    f"missing={sorted(missing_roles)}, extra={sorted(extra_roles)}"
                ),
                "family_plan.roles",
            )
        )
    if variant_count < 27:
        issues.append(
            Issue(
                "error",
                "visual_family.total_variants",
                f"Family expansion requires at least 27 variants, got {variant_count}",
                "family_plan.roles",
            )
        )
    return make_report(
        "validate_visual_reference_family_generation_plan",
        issues,
        plan=str(plan_path),
        role_count=len(roles),
        variant_count=variant_count,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a visual reference pack or generation plan."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pack", type=Path)
    group.add_argument("--plan", type=Path)
    group.add_argument("--family-plan", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        if args.pack:
            report = validate_pack(args.pack)
        elif args.plan:
            report = validate_plan(args.plan)
        else:
            report = validate_family_plan(args.family_plan)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report = make_report(
            "validate_visual_references",
            [Issue("error", "visual_reference.read", str(exc), "")],
        )
    if args.report:
        write_json(args.report, report)
    print_report(report)
    return 1 if report["summary"]["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
