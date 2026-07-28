from __future__ import annotations

import json
import re
from typing import Any

from scripts.common import Issue


def _resolve_ref(root_schema: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"Only local JSON Schema references are supported: {reference}")
    value: Any = root_schema
    for raw_part in reference[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        value = value[part]
    if not isinstance(value, dict):
        raise ValueError(f"JSON Schema reference does not resolve to an object: {reference}")
    return value


def _matches_type(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return True


def _path(parent: str, child: str) -> str:
    return f"{parent}.{child}" if parent else child


def _validate(
    value: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    path: str,
    issues: list[Issue],
) -> None:
    if "$ref" in schema:
        try:
            resolved = _resolve_ref(root_schema, schema["$ref"])
        except (KeyError, TypeError, ValueError) as exc:
            issues.append(Issue("error", "schema.ref", str(exc), path))
            return
        _validate(value, resolved, root_schema, path, issues)
        return

    expected = schema.get("type")
    expected_types = [expected] if isinstance(expected, str) else expected
    if isinstance(expected_types, list) and not any(
        _matches_type(value, item) for item in expected_types
    ):
        issues.append(
            Issue(
                "error",
                "schema.type",
                f"Expected type {expected_types}, got {type(value).__name__}",
                path,
            )
        )
        return

    if "const" in schema and value != schema["const"]:
        issues.append(
            Issue(
                "error",
                "schema.const",
                f"Value must equal {schema['const']!r}",
                path,
            )
        )
    if "enum" in schema and value not in schema["enum"]:
        issues.append(
            Issue(
                "error",
                "schema.enum",
                f"Value is not one of the allowed options: {value!r}",
                path,
            )
        )

    if isinstance(value, str):
        minimum = schema.get("minLength")
        if isinstance(minimum, int) and len(value) < minimum:
            issues.append(
                Issue(
                    "error",
                    "schema.min_length",
                    f"String must contain at least {minimum} characters",
                    path,
                )
            )
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.search(pattern, value) is None:
            issues.append(
                Issue(
                    "error",
                    "schema.pattern",
                    f"String does not match required pattern: {pattern}",
                    path,
                )
            )

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            issues.append(
                Issue(
                    "error",
                    "schema.minimum",
                    f"Number must be at least {schema['minimum']}",
                    path,
                )
            )
        if "maximum" in schema and value > schema["maximum"]:
            issues.append(
                Issue(
                    "error",
                    "schema.maximum",
                    f"Number must be at most {schema['maximum']}",
                    path,
                )
            )
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            issues.append(
                Issue(
                    "error",
                    "schema.exclusive_minimum",
                    f"Number must be greater than {schema['exclusiveMinimum']}",
                    path,
                )
            )
        multiple = schema.get("multipleOf")
        if isinstance(multiple, (int, float)) and multiple:
            quotient = value / multiple
            if abs(quotient - round(quotient)) > 1e-9:
                issues.append(
                    Issue(
                        "error",
                        "schema.multiple_of",
                        f"Number must be a multiple of {multiple}",
                        path,
                    )
                )

    if isinstance(value, dict):
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if key not in value:
                    issues.append(
                        Issue(
                            "error",
                            "schema.required",
                            f"Missing required property: {key}",
                            _path(path, str(key)),
                        )
                    )
        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            properties = {}
        additional = schema.get("additionalProperties", True)
        for key, child in value.items():
            child_path = _path(path, str(key))
            if key in properties and isinstance(properties[key], dict):
                _validate(child, properties[key], root_schema, child_path, issues)
            elif additional is False:
                issues.append(
                    Issue(
                        "error",
                        "schema.additional_property",
                        f"Unexpected property: {key}",
                        child_path,
                    )
                )
            elif isinstance(additional, dict):
                _validate(child, additional, root_schema, child_path, issues)

    if isinstance(value, list):
        minimum_items = schema.get("minItems")
        if isinstance(minimum_items, int) and len(value) < minimum_items:
            issues.append(
                Issue(
                    "error",
                    "schema.min_items",
                    f"Array must contain at least {minimum_items} items",
                    path,
                )
            )
        if schema.get("uniqueItems"):
            canonical = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(set(canonical)) != len(canonical):
                issues.append(
                    Issue(
                        "error",
                        "schema.unique_items",
                        "Array items must be unique",
                        path,
                    )
                )
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, child in enumerate(value):
                _validate(child, item_schema, root_schema, f"{path}[{index}]", issues)


def validate_against_schema(
    value: Any, schema: dict[str, Any], path: str = ""
) -> list[Issue]:
    issues: list[Issue] = []
    _validate(value, schema, schema, path, issues)
    return issues
