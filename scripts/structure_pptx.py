from __future__ import annotations

import argparse
import io
import os
import posixpath
import re
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from xml.sax.saxutils import quoteattr

if __package__ in {None, ""}:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.common import Issue, load_json, make_report, print_report, write_json


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}
for _prefix, _uri in NS.items():
    if _prefix != "rel":
        ET.register_namespace(_prefix, _uri)

P = f"{{{NS['p']}}}"
A = f"{{{NS['a']}}}"
R_ID = f"{{{NS['r']}}}id"

SHAPE_TAGS = {P + name for name in ("sp", "pic", "graphicFrame", "cxnSp", "grpSp")}
GROUPABLE_TAGS = {P + name for name in ("sp", "pic", "graphicFrame", "cxnSp")}
SIMPLE_LINE_PRESETS = {"line", "straightConnector1"}
XMLNS_RE = re.compile(rb"\sxmlns(?::([A-Za-z_][\w.\-]*))?=(?:\"([^\"]*)\"|'([^']*)')")


class StructurePlanError(ValueError):
    def __init__(self, code: str, message: str, path: str = "") -> None:
        super().__init__(message)
        self.code = code
        self.path = path


@dataclass(frozen=True)
class ShapeRef:
    element: ET.Element
    parent: ET.Element
    index: int
    name: str
    shape_id: int


@dataclass(frozen=True)
class GroupOperation:
    slide: int
    name: str
    members: tuple[ShapeRef, ...]
    group_id: int
    bbox: tuple[int, int, int, int]


@dataclass(frozen=True)
class ConnectorOperation:
    slide: int
    connector: ShapeRef
    start: ShapeRef
    start_site: int
    end: ShapeRef
    end_site: int


@dataclass
class ParsedSlide:
    part_name: str
    original: bytes
    root: ET.Element
    namespaces: list[tuple[str, str]]
    names: dict[str, list[ShapeRef]]
    max_shape_id: int


def _error(code: str, message: str, path: str = "") -> StructurePlanError:
    return StructurePlanError(code, message, path)


def _require_object(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise _error("structure.invalid_plan", "Expected a JSON object", path)
    return value


def _require_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise _error("structure.invalid_plan", "Expected a JSON array", path)
    return value


def _require_string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise _error("structure.invalid_plan", "Expected a non-empty string", path)
    return value


def _require_slide(value: Any, slide_count: int, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise _error("structure.invalid_slide", "Slide must be a 1-based integer", path)
    if value < 1 or value > slide_count:
        raise _error(
            "structure.invalid_slide",
            f"Slide {value} is outside the available range 1..{slide_count}",
            path,
        )
    return value


def _require_site(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0 or value > 255:
        raise _error(
            "structure.invalid_site",
            "Connection site must be an integer from 0 through 255",
            path,
        )
    return value


def _parse_xml(data: bytes, part_name: str) -> tuple[ET.Element, list[tuple[str, str]]]:
    namespaces: list[tuple[str, str]] = []
    prefix_uris: dict[str, str] = {}
    try:
        for _, namespace in ET.iterparse(io.BytesIO(data), events=("start-ns",)):
            prefix, uri = namespace
            if prefix in prefix_uris and prefix_uris[prefix] != uri:
                raise _error(
                    "structure.unsupported_namespace",
                    f"Namespace prefix {prefix!r} is rebound inside one XML part",
                    part_name,
                )
            prefix_uris[prefix] = uri
            if namespace not in namespaces:
                namespaces.append(namespace)
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise _error("structure.invalid_xml", str(exc), part_name) from exc
    for prefix, uri in namespaces:
        try:
            ET.register_namespace(prefix, uri)
        except ValueError:
            # ElementTree reserves ns\d+ prefixes. They are restored on serialization below.
            pass
    return root, namespaces


def _serialize_xml(root: ET.Element, namespaces: list[tuple[str, str]]) -> bytes:
    serialized = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    declaration_end = serialized.find(b"?>")
    root_start = serialized.find(b"<", declaration_end + 2)
    root_end = serialized.find(b">", root_start)
    if root_start < 0 or root_end < 0:
        return serialized

    root_open = serialized[root_start:root_end]
    present: set[str] = set()
    for match in XMLNS_RE.finditer(root_open):
        present.add((match.group(1) or b"").decode("utf-8"))

    additions: list[str] = []
    for prefix, uri in namespaces:
        if prefix in present:
            continue
        attribute = "xmlns" if not prefix else f"xmlns:{prefix}"
        additions.append(f" {attribute}={quoteattr(uri)}")
        present.add(prefix)
    if not additions:
        return serialized
    insertion = "".join(additions).encode("utf-8")
    return serialized[:root_end] + insertion + serialized[root_end:]


def _slide_parts(package: dict[str, bytes]) -> list[str]:
    required = {
        "ppt/presentation.xml",
        "ppt/_rels/presentation.xml.rels",
    }
    missing = sorted(required - package.keys())
    if missing:
        raise _error("structure.invalid_pptx", f"Missing required package part: {missing[0]}")

    presentation, _ = _parse_xml(package["ppt/presentation.xml"], "ppt/presentation.xml")
    relationships, _ = _parse_xml(
        package["ppt/_rels/presentation.xml.rels"],
        "ppt/_rels/presentation.xml.rels",
    )
    rel_targets: dict[str, str] = {}
    for relationship in relationships.findall("rel:Relationship", NS):
        rel_id = relationship.attrib.get("Id")
        target = relationship.attrib.get("Target")
        rel_type = relationship.attrib.get("Type", "")
        if rel_id and target and rel_type.endswith("/slide"):
            rel_targets[rel_id] = posixpath.normpath(posixpath.join("ppt", target))

    slide_parts: list[str] = []
    for slide_id in presentation.findall("p:sldIdLst/p:sldId", NS):
        rel_id = slide_id.attrib.get(R_ID)
        part_name = rel_targets.get(rel_id or "")
        if not part_name or part_name not in package:
            raise _error(
                "structure.invalid_pptx",
                f"Cannot resolve slide relationship {rel_id!r}",
                "ppt/presentation.xml",
            )
        slide_parts.append(part_name)
    if not slide_parts:
        raise _error("structure.invalid_pptx", "Presentation contains no slides")
    return slide_parts


def _shape_properties(shape: ET.Element) -> ET.Element | None:
    paths = {
        P + "sp": "p:nvSpPr/p:cNvPr",
        P + "pic": "p:nvPicPr/p:cNvPr",
        P + "graphicFrame": "p:nvGraphicFramePr/p:cNvPr",
        P + "cxnSp": "p:nvCxnSpPr/p:cNvPr",
        P + "grpSp": "p:nvGrpSpPr/p:cNvPr",
    }
    path = paths.get(shape.tag)
    return shape.find(path, NS) if path else None


def _shape_transform(shape: ET.Element) -> ET.Element | None:
    if shape.tag == P + "graphicFrame":
        return shape.find("p:xfrm", NS)
    if shape.tag == P + "grpSp":
        return shape.find("p:grpSpPr/a:xfrm", NS)
    return shape.find("p:spPr/a:xfrm", NS)


def _shape_bbox(shape: ET.Element, path: str) -> tuple[int, int, int, int]:
    xfrm = _shape_transform(shape)
    if xfrm is None:
        raise _error("structure.unsupported_transform", "Shape has no supported transform", path)
    if any(key in xfrm.attrib for key in ("rot", "flipH", "flipV")):
        raise _error(
            "structure.unsupported_transform",
            "Rotated or flipped shapes are not supported for grouping",
            path,
        )
    off = xfrm.find("a:off", NS)
    ext = xfrm.find("a:ext", NS)
    if off is None or ext is None:
        raise _error("structure.unsupported_transform", "Shape transform lacks off/ext", path)
    try:
        x = int(off.attrib["x"])
        y = int(off.attrib["y"])
        width = int(ext.attrib["cx"])
        height = int(ext.attrib["cy"])
    except (KeyError, ValueError) as exc:
        raise _error("structure.unsupported_transform", "Shape transform is not numeric", path) from exc
    if width <= 0 or height <= 0:
        raise _error("structure.unsupported_transform", "Shape extent must be positive", path)
    return x, y, width, height


def _index_shapes(root: ET.Element, part_name: str) -> tuple[dict[str, list[ShapeRef]], int]:
    names: dict[str, list[ShapeRef]] = {}
    shape_ids: dict[int, str] = {}

    def visit(parent: ET.Element) -> None:
        for index, child in enumerate(list(parent)):
            if child.tag not in SHAPE_TAGS:
                continue
            properties = _shape_properties(child)
            if properties is None:
                raise _error("structure.invalid_shape", "Shape lacks p:cNvPr", part_name)
            name = properties.attrib.get("name", "")
            try:
                shape_id = int(properties.attrib["id"])
            except (KeyError, ValueError) as exc:
                raise _error("structure.invalid_shape", "Shape has an invalid cNvPr id", part_name) from exc
            if shape_id in shape_ids:
                raise _error(
                    "structure.duplicate_shape_id",
                    f"Duplicate cNvPr id {shape_id} on one slide",
                    part_name,
                )
            shape_ids[shape_id] = name
            ref = ShapeRef(child, parent, index, name, shape_id)
            names.setdefault(name, []).append(ref)
            if child.tag == P + "grpSp":
                visit(child)

    tree = root.find("p:cSld/p:spTree", NS)
    if tree is None:
        raise _error("structure.invalid_slide_xml", "Slide lacks p:cSld/p:spTree", part_name)
    visit(tree)
    return names, max(shape_ids, default=0)


def _resolve_name(slide: ParsedSlide, name: str, path: str) -> ShapeRef:
    matches = slide.names.get(name, [])
    if not matches:
        raise _error("structure.missing_name", f"No shape named {name!r}", path)
    if len(matches) > 1:
        raise _error("structure.ambiguous_name", f"Shape name {name!r} is not unique", path)
    return matches[0]


def _validate_group(
    entry: Any,
    entry_path: str,
    slides: list[ParsedSlide],
    used_members: set[tuple[int, int]],
    allocated_ids: list[int],
    planned_group_names: set[tuple[int, str]],
) -> GroupOperation:
    value = _require_object(entry, entry_path)
    slide_number = _require_slide(value.get("slide"), len(slides), f"{entry_path}.slide")
    name = _require_string(value.get("name"), f"{entry_path}.name")
    slide = slides[slide_number - 1]
    if slide.names.get(name) or (slide_number, name) in planned_group_names:
        raise _error("structure.duplicate_name", f"Group name {name!r} already exists", f"{entry_path}.name")
    planned_group_names.add((slide_number, name))

    member_values = _require_list(value.get("members"), f"{entry_path}.members")
    if len(member_values) < 2:
        raise _error("structure.invalid_group", "A group requires at least two members", f"{entry_path}.members")
    member_names = [
        _require_string(member, f"{entry_path}.members[{index}]")
        for index, member in enumerate(member_values)
    ]
    if len(set(member_names)) != len(member_names):
        raise _error("structure.duplicate_member", "A group member is listed more than once", entry_path)

    members = tuple(
        _resolve_name(slide, member_name, f"{entry_path}.members[{index}]")
        for index, member_name in enumerate(member_names)
    )
    parent = members[0].parent
    tree = slide.root.find("p:cSld/p:spTree", NS)
    if tree is None or parent is not tree or any(member.parent is not parent for member in members):
        raise _error(
            "structure.cross_level_group",
            "Group members must be direct children of the same top-level slide shape tree",
            entry_path,
        )
    if any(member.element.tag not in GROUPABLE_TAGS for member in members):
        raise _error("structure.unsupported_group_member", "Nested groups are not supported", entry_path)

    indices = sorted(member.index for member in members)
    if indices != list(range(indices[0], indices[0] + len(indices))):
        raise _error(
            "structure.non_contiguous_group",
            "Group members must be consecutive in z-order",
            entry_path,
        )
    for member in members:
        key = (slide_number, member.shape_id)
        if key in used_members:
            raise _error("structure.duplicate_member", f"Shape {member.name!r} is used by two groups", entry_path)
        used_members.add(key)

    boxes = [
        _shape_bbox(member.element, f"{entry_path}.members[{index}]")
        for index, member in enumerate(members)
    ]
    min_x = min(box[0] for box in boxes)
    min_y = min(box[1] for box in boxes)
    max_x = max(box[0] + box[2] for box in boxes)
    max_y = max(box[1] + box[3] for box in boxes)
    allocated_ids[slide_number - 1] += 1
    return GroupOperation(
        slide_number,
        name,
        tuple(sorted(members, key=lambda member: member.index)),
        allocated_ids[slide_number - 1],
        (min_x, min_y, max_x - min_x, max_y - min_y),
    )


def _validate_connector(
    entry: Any,
    entry_path: str,
    slides: list[ParsedSlide],
    used_connectors: set[tuple[int, int]],
    grouped_members: set[tuple[int, int]],
) -> ConnectorOperation:
    value = _require_object(entry, entry_path)
    slide_number = _require_slide(value.get("slide"), len(slides), f"{entry_path}.slide")
    slide = slides[slide_number - 1]
    connector_name = _require_string(value.get("name"), f"{entry_path}.name")
    connector = _resolve_name(slide, connector_name, f"{entry_path}.name")
    key = (slide_number, connector.shape_id)
    if key in used_connectors:
        raise _error("structure.duplicate_connector", f"Connector {connector_name!r} is listed twice", entry_path)
    if key in grouped_members:
        raise _error("structure.unsupported_connector", "A connector cannot also be a new group member", entry_path)
    used_connectors.add(key)

    tree = slide.root.find("p:cSld/p:spTree", NS)
    if tree is None or connector.parent is not tree:
        raise _error(
            "structure.cross_level_connector",
            "Connector must be a direct child of the top-level slide shape tree",
            entry_path,
        )
    if connector.element.tag not in {P + "sp", P + "cxnSp"}:
        raise _error("structure.unsupported_connector", "Named connector is not a line shape", entry_path)
    if connector.element.tag == P + "sp":
        allowed_children = {P + name for name in ("nvSpPr", "spPr", "style", "extLst")}
        if connector.element.attrib or any(child.tag not in allowed_children for child in connector.element):
            raise _error(
                "structure.unsupported_connector",
                "Plain line contains text or shape-only properties that a connector cannot preserve",
                entry_path,
            )
    geometry = connector.element.find("p:spPr/a:prstGeom", NS)
    if connector.element.tag == P + "sp" and (
        geometry is None or geometry.attrib.get("prst") not in SIMPLE_LINE_PRESETS
    ):
        raise _error(
            "structure.unsupported_connector",
            "Only ordinary straight line shapes can be converted to connectors",
            entry_path,
        )
    xfrm = _shape_transform(connector.element)
    if xfrm is None or "rot" in xfrm.attrib:
        raise _error(
            "structure.unsupported_transform",
            "Rotated connector transforms are not supported",
            entry_path,
        )

    start_value = _require_object(value.get("from"), f"{entry_path}.from")
    end_value = _require_object(value.get("to"), f"{entry_path}.to")
    start_name = _require_string(start_value.get("shape"), f"{entry_path}.from.shape")
    end_name = _require_string(end_value.get("shape"), f"{entry_path}.to.shape")
    start = _resolve_name(slide, start_name, f"{entry_path}.from.shape")
    end = _resolve_name(slide, end_name, f"{entry_path}.to.shape")
    if connector.shape_id in {start.shape_id, end.shape_id}:
        raise _error("structure.invalid_connector", "A connector cannot connect to itself", entry_path)
    if start.shape_id == end.shape_id:
        raise _error("structure.invalid_connector", "Connector endpoints must be different shapes", entry_path)
    if start.element.tag != P + "sp" or end.element.tag != P + "sp":
        raise _error(
            "structure.unsupported_endpoint",
            "Connection endpoints must be native p:sp shapes",
            entry_path,
        )
    start_site = _require_site(start_value.get("site"), f"{entry_path}.from.site")
    end_site = _require_site(end_value.get("site"), f"{entry_path}.to.site")
    return ConnectorOperation(slide_number, connector, start, start_site, end, end_site)


def _make_group(operation: GroupOperation) -> ET.Element:
    group = ET.Element(P + "grpSp")
    non_visual = ET.SubElement(group, P + "nvGrpSpPr")
    ET.SubElement(non_visual, P + "cNvPr", {"id": str(operation.group_id), "name": operation.name})
    ET.SubElement(non_visual, P + "cNvGrpSpPr")
    ET.SubElement(non_visual, P + "nvPr")

    group_properties = ET.SubElement(group, P + "grpSpPr")
    transform = ET.SubElement(group_properties, A + "xfrm")
    x, y, width, height = operation.bbox
    ET.SubElement(transform, A + "off", {"x": str(x), "y": str(y)})
    ET.SubElement(transform, A + "ext", {"cx": str(width), "cy": str(height)})
    ET.SubElement(transform, A + "chOff", {"x": str(x), "y": str(y)})
    ET.SubElement(transform, A + "chExt", {"cx": str(width), "cy": str(height)})
    for member in operation.members:
        group.append(member.element)
    return group


def _apply_group(operation: GroupOperation) -> None:
    parent = operation.members[0].parent
    insertion_index = min(member.index for member in operation.members)
    for member in operation.members:
        parent.remove(member.element)
    parent.insert(insertion_index, _make_group(operation))


def _connection_properties(connector: ET.Element) -> ET.Element:
    if connector.tag == P + "sp":
        old_non_visual = connector.find("p:nvSpPr", NS)
        if old_non_visual is None:
            raise _error("structure.invalid_shape", "Line shape lacks p:nvSpPr")
        non_visual_index = list(connector).index(old_non_visual)
        c_nv_pr = old_non_visual.find("p:cNvPr", NS)
        nv_pr = old_non_visual.find("p:nvPr", NS)
        if c_nv_pr is None or nv_pr is None:
            raise _error("structure.invalid_shape", "Line shape has incomplete non-visual properties")
        old_non_visual.remove(c_nv_pr)
        old_non_visual.remove(nv_pr)
        new_non_visual = ET.Element(P + "nvCxnSpPr")
        new_non_visual.append(c_nv_pr)
        connection_properties = ET.SubElement(new_non_visual, P + "cNvCxnSpPr")
        new_non_visual.append(nv_pr)
        connector.remove(old_non_visual)
        connector.insert(non_visual_index, new_non_visual)
        connector.tag = P + "cxnSp"
        return connection_properties

    non_visual = connector.find("p:nvCxnSpPr", NS)
    if non_visual is None:
        raise _error("structure.invalid_shape", "Connector lacks p:nvCxnSpPr")
    connection_properties = non_visual.find("p:cNvCxnSpPr", NS)
    if connection_properties is None:
        connection_properties = ET.Element(P + "cNvCxnSpPr")
        nv_pr = non_visual.find("p:nvPr", NS)
        insert_at = list(non_visual).index(nv_pr) if nv_pr is not None else len(non_visual)
        non_visual.insert(insert_at, connection_properties)
    return connection_properties


def _apply_connector(operation: ConnectorOperation) -> bool:
    was_plain_shape = operation.connector.element.tag == P + "sp"
    properties = _connection_properties(operation.connector.element)
    for tag in (A + "stCxn", A + "endCxn"):
        for existing in list(properties.findall(tag)):
            properties.remove(existing)
    extension = properties.find("a:extLst", NS)
    insert_at = list(properties).index(extension) if extension is not None else len(properties)
    properties.insert(
        insert_at,
        ET.Element(A + "stCxn", {"id": str(operation.start.shape_id), "idx": str(operation.start_site)}),
    )
    properties.insert(
        insert_at + 1,
        ET.Element(A + "endCxn", {"id": str(operation.end.shape_id), "idx": str(operation.end_site)}),
    )
    return was_plain_shape


def _read_package(input_path: Path) -> tuple[list[zipfile.ZipInfo], dict[str, bytes], bytes]:
    try:
        with zipfile.ZipFile(input_path) as source:
            infos = source.infolist()
            names = [info.filename for info in infos]
            if len(set(names)) != len(names):
                raise _error("structure.invalid_pptx", "Package contains duplicate part names")
            package = {info.filename: source.read(info.filename) for info in infos}
            comment = source.comment
    except (OSError, zipfile.BadZipFile) as exc:
        raise _error("structure.invalid_pptx", str(exc), str(input_path)) from exc
    return infos, package, comment


def _write_package(
    output_path: Path,
    infos: list[zipfile.ZipInfo],
    package: dict[str, bytes],
    comment: bytes,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output_path.name}.",
        suffix=".tmp",
        dir=output_path.parent,
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(temporary, "w") as destination:
            destination.comment = comment
            for info in infos:
                destination.writestr(info, package[info.filename])
        with temporary.open("r+b") as handle:
            os.fsync(handle.fileno())
        os.replace(temporary, output_path)
    finally:
        temporary.unlink(missing_ok=True)


def structure_pptx(
    input_path: str | Path,
    plan: dict[str, Any],
    output_path: str | Path,
) -> dict[str, Any]:
    source_path = Path(input_path).resolve()
    target_path = Path(output_path).resolve()
    if source_path == target_path:
        raise _error(
            "structure.in_place_not_allowed",
            "Input and output must be different files; in-place overwrite is refused",
            str(source_path),
        )
    if not source_path.is_file():
        raise _error("structure.missing_input", "Input PPTX does not exist", str(source_path))
    plan_value = _require_object(plan, "plan")
    unknown_keys = sorted(set(plan_value) - {"groups", "connectors"})
    if unknown_keys:
        raise _error("structure.invalid_plan", f"Unknown plan key: {unknown_keys[0]}", "plan")

    infos, package, package_comment = _read_package(source_path)
    slide_parts = _slide_parts(package)
    slides: list[ParsedSlide] = []
    for part_name in slide_parts:
        root, namespaces = _parse_xml(package[part_name], part_name)
        names, max_shape_id = _index_shapes(root, part_name)
        slides.append(ParsedSlide(part_name, package[part_name], root, namespaces, names, max_shape_id))

    groups_value = _require_list(plan_value.get("groups", []), "plan.groups")
    connectors_value = _require_list(plan_value.get("connectors", []), "plan.connectors")
    used_members: set[tuple[int, int]] = set()
    allocated_ids = [slide.max_shape_id for slide in slides]
    planned_group_names: set[tuple[int, str]] = set()
    group_operations = [
        _validate_group(
            entry,
            f"plan.groups[{index}]",
            slides,
            used_members,
            allocated_ids,
            planned_group_names,
        )
        for index, entry in enumerate(groups_value)
    ]
    used_connectors: set[tuple[int, int]] = set()
    connector_operations = [
        _validate_connector(
            entry,
            f"plan.connectors[{index}]",
            slides,
            used_connectors,
            used_members,
        )
        for index, entry in enumerate(connectors_value)
    ]

    groups_by_slide: dict[int, list[GroupOperation]] = {}
    for operation in group_operations:
        groups_by_slide.setdefault(operation.slide, []).append(operation)
    for operations in groups_by_slide.values():
        for operation in sorted(
            operations,
            key=lambda item: min(member.index for member in item.members),
            reverse=True,
        ):
            _apply_group(operation)

    converted_connectors = 0
    for operation in connector_operations:
        converted_connectors += int(_apply_connector(operation))

    modified_slides = sorted(
        {operation.slide for operation in group_operations}
        | {operation.slide for operation in connector_operations}
    )
    for slide_number in modified_slides:
        slide = slides[slide_number - 1]
        package[slide.part_name] = _serialize_xml(slide.root, slide.namespaces)

    _write_package(target_path, infos, package, package_comment)
    return make_report(
        "structure_pptx",
        [],
        input=str(source_path),
        output=str(target_path),
        slides_modified=modified_slides,
        groups_created=len(group_operations),
        connectors_bound=len(connector_operations),
        plain_lines_converted=converted_connectors,
        limitations=[
            "Connection site values are geometry-specific OOXML indices, not Cartesian direction labels.",
            "The tool verifies OOXML structure and package readability; it does not claim PowerPoint UI interaction was tested.",
            "Connector xfrm is preserved, but an editor may reroute a bound connector when shapes move or when the file is opened.",
            "Grouping is limited to consecutive, top-level, unrotated shapes with simple transforms.",
        ],
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Add small, explicit native groups and connector bindings to an existing PPTX.",
        epilog=(
            "The plan uses 1-based slide numbers and exact objectName values. Connector site is the "
            "shape geometry's OOXML connection-point index; it is not mapped from up/down/left/right."
        ),
    )
    parser.add_argument("input", help="Input PPTX. It is never modified in place.")
    parser.add_argument("--plan", required=True, help="JSON structure plan")
    parser.add_argument("--output", required=True, help="New PPTX path")
    parser.add_argument("--report", help="Optional JSON report path")
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        plan = load_json(args.plan)
        report = structure_pptx(args.input, plan, args.output)
    except (OSError, ValueError, StructurePlanError) as exc:
        if isinstance(exc, StructurePlanError):
            code = exc.code
            path = exc.path
        else:
            code = "structure.failed"
            path = ""
        report = make_report(
            "structure_pptx",
            [Issue("error", code, str(exc), path)],
            input=str(Path(args.input).resolve()),
            output=str(Path(args.output).resolve()),
        )
        if args.report:
            write_json(args.report, report)
        print_report(report)
        return 2
    if args.report:
        write_json(args.report, report)
    print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
