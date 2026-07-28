from __future__ import annotations

import argparse
import io
import posixpath
import re
import struct
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any
from xml.etree import ElementTree as ET

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.common import Issue, load_json, make_report, print_report, write_json


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}
EMU_PER_INCH = 914400
INTERNAL_TERMS = (
    "template dna",
    "模板 dna",
    "模板dna",
    "production planning table",
    "生产规划表",
    "qa note",
    "qa 说明",
    "qa说明",
    "archetype",
    "版式原型",
    "mockup-derived",
    "internal route",
    "内部路线",
    "page task",
    "页面任务",
    "production note",
    "制作说明",
    "source gap",
    "来源缺口",
)
REQUIRED_PARTS = {
    "[Content_Types].xml",
    "_rels/.rels",
    "ppt/presentation.xml",
}
R_ID = f"{{{NS['r']}}}embed"


def _natural_slide_key(name: str) -> tuple[int, str]:
    match = re.search(r"slide(\d+)\.xml$", name)
    return (int(match.group(1)) if match else 10**9, name)


def _xml(zf: zipfile.ZipFile, name: str) -> ET.Element:
    return ET.fromstring(zf.read(name))


def _relationship_base(rel_name: str) -> str:
    path = PurePosixPath(rel_name)
    if rel_name == "_rels/.rels":
        return ""
    if path.parent.name != "_rels" or not path.name.endswith(".rels"):
        return ""
    part_name = path.name[:-5]
    return str(path.parent.parent / part_name)


def _resolve_target(base_part: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    base_dir = posixpath.dirname(base_part)
    return posixpath.normpath(posixpath.join(base_dir, target))


def _slide_relationships(
    zf: zipfile.ZipFile, slide_name: str
) -> dict[str, tuple[str, bool]]:
    path = PurePosixPath(slide_name)
    rel_name = str(path.parent / "_rels" / f"{path.name}.rels")
    if rel_name not in zf.namelist():
        return {}
    root = _xml(zf, rel_name)
    result: dict[str, tuple[str, bool]] = {}
    for rel in root.findall("rel:Relationship", NS):
        rel_id = rel.attrib.get("Id", "")
        external = rel.attrib.get("TargetMode") == "External"
        result[rel_id] = (
            rel.attrib.get("Target", "")
            if external
            else _resolve_target(slide_name, rel.attrib.get("Target", "")),
            external,
        )
    return result


def _image_size(data: bytes) -> tuple[int, int] | None:
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data[:2] != b"\xff\xd8":
        return None
    stream = io.BytesIO(data)
    stream.read(2)
    while True:
        marker_start = stream.read(1)
        if not marker_start:
            return None
        if marker_start != b"\xff":
            continue
        marker = stream.read(1)
        while marker == b"\xff":
            marker = stream.read(1)
        if marker in {b"\xd8", b"\xd9"}:
            continue
        length_raw = stream.read(2)
        if len(length_raw) != 2:
            return None
        length = struct.unpack(">H", length_raw)[0]
        if marker and marker[0] in {
            0xC0,
            0xC1,
            0xC2,
            0xC3,
            0xC5,
            0xC6,
            0xC7,
            0xC9,
            0xCA,
            0xCB,
            0xCD,
            0xCE,
            0xCF,
        }:
            payload = stream.read(length - 2)
            if len(payload) >= 5:
                height, width = struct.unpack(">HH", payload[1:5])
                return width, height
            return None
        stream.seek(max(length - 2, 0), io.SEEK_CUR)


def _direct_shapes(root: ET.Element) -> list[ET.Element]:
    tree = root.find(".//p:cSld/p:spTree", NS)
    if tree is None:
        return []
    supported = {
        f"{{{NS['p']}}}sp",
        f"{{{NS['p']}}}pic",
        f"{{{NS['p']}}}graphicFrame",
        f"{{{NS['p']}}}cxnSp",
    }
    return [child for child in tree if child.tag in supported]


def _shape_box(shape: ET.Element) -> tuple[int, int, int, int] | None:
    if shape.tag == f"{{{NS['p']}}}graphicFrame":
        xfrm = shape.find("p:xfrm", NS)
    else:
        xfrm = shape.find("p:spPr/a:xfrm", NS)
    if xfrm is None:
        return None
    off = xfrm.find("a:off", NS)
    ext = xfrm.find("a:ext", NS)
    if off is None or ext is None:
        return None
    try:
        return (
            int(off.attrib.get("x", "0")),
            int(off.attrib.get("y", "0")),
            int(ext.attrib.get("cx", "0")),
            int(ext.attrib.get("cy", "0")),
        )
    except ValueError:
        return None


def _shape_name(shape: ET.Element) -> str:
    props = shape.find("p:nvSpPr/p:cNvPr", NS)
    if props is None:
        props = shape.find("p:nvPicPr/p:cNvPr", NS)
    if props is None:
        props = shape.find("p:nvGraphicFramePr/p:cNvPr", NS)
    return props.attrib.get("name", "unnamed") if props is not None else "unnamed"


def _intersection_ratio(
    first: tuple[int, int, int, int], second: tuple[int, int, int, int]
) -> float:
    ax, ay, aw, ah = first
    bx, by, bw, bh = second
    width = max(0, min(ax + aw, bx + bw) - max(ax, bx))
    height = max(0, min(ay + ah, by + bh) - max(ay, by))
    intersection = width * height
    smaller = min(max(aw * ah, 1), max(bw * bh, 1))
    return intersection / smaller


def inspect_pptx(path: Path, project: dict[str, Any] | None = None) -> dict[str, Any]:
    issues: list[Issue] = []
    details: dict[str, Any] = {
        "pptx": str(path),
        "slide_count": 0,
        "canvas_inches": None,
        "fonts": [],
        "media_count": 0,
        "security_parts": [],
    }
    try:
        zf = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as exc:
        return make_report(
            "qa_pptx",
            [Issue("error", "pptx.invalid_zip", str(exc), str(path))],
            **details,
        )

    with zf:
        names = set(zf.namelist())
        bad_member = zf.testzip()
        if bad_member:
            issues.append(
                Issue(
                    "error",
                    "pptx.crc",
                    f"CRC failure in package member: {bad_member}",
                    bad_member,
                )
            )
        for required in sorted(REQUIRED_PARTS - names):
            issues.append(
                Issue(
                    "error",
                    "pptx.required_part",
                    f"Missing required PPTX part: {required}",
                    required,
                )
            )
        if "ppt/presentation.xml" not in names:
            return make_report("qa_pptx", issues, **details)

        presentation = _xml(zf, "ppt/presentation.xml")
        size = presentation.find("p:sldSz", NS)
        slide_width = slide_height = 0
        if size is None:
            issues.append(
                Issue(
                    "error",
                    "pptx.canvas",
                    "presentation.xml has no slide size",
                    "ppt/presentation.xml",
                )
            )
        else:
            try:
                slide_width = int(size.attrib["cx"])
                slide_height = int(size.attrib["cy"])
                details["canvas_inches"] = {
                    "width": round(slide_width / EMU_PER_INCH, 4),
                    "height": round(slide_height / EMU_PER_INCH, 4),
                }
            except (KeyError, ValueError):
                issues.append(
                    Issue(
                        "error",
                        "pptx.canvas",
                        "Invalid slide dimensions",
                        "ppt/presentation.xml",
                    )
                )

        slide_names = sorted(
            (
                name
                for name in names
                if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
            ),
            key=_natural_slide_key,
        )
        details["slide_count"] = len(slide_names)
        details["media_count"] = sum(
            1 for name in names if name.startswith("ppt/media/") and not name.endswith("/")
        )
        if not slide_names:
            issues.append(
                Issue("error", "pptx.no_slides", "PPTX contains no slides", "ppt/slides")
            )

        security_parts = sorted(
            name
            for name in names
            if not name.endswith("/")
            and (
                "vbaproject" in name.casefold()
                or "/activex/" in name.casefold()
                or "/embeddings/" in name.casefold()
            )
        )
        details["security_parts"] = security_parts
        for name in security_parts:
            issues.append(
                Issue(
                    "warning",
                    "pptx.embedded_content",
                    "Package contains macro, ActiveX, or embedded-object content",
                    name,
                )
            )

        for rel_name in sorted(name for name in names if name.endswith(".rels")):
            try:
                rel_root = _xml(zf, rel_name)
            except ET.ParseError as exc:
                issues.append(
                    Issue("error", "pptx.relationship_xml", str(exc), rel_name)
                )
                continue
            base_part = _relationship_base(rel_name)
            for rel in rel_root.findall("rel:Relationship", NS):
                target = rel.attrib.get("Target", "")
                if rel.attrib.get("TargetMode") == "External":
                    issues.append(
                        Issue(
                            "warning",
                            "pptx.external_relationship",
                            f"External relationship target: {target}",
                            rel_name,
                        )
                    )
                    continue
                resolved = _resolve_target(base_part, target)
                if resolved and resolved not in names:
                    issues.append(
                        Issue(
                            "error",
                            "pptx.broken_relationship",
                            f"Relationship target does not exist: {resolved}",
                            rel_name,
                        )
                    )

        font_names: set[str] = set()
        text_boxes: list[tuple[int, str, tuple[int, int, int, int]]] = []
        for slide_index, slide_name in enumerate(slide_names, start=1):
            try:
                root = _xml(zf, slide_name)
            except ET.ParseError as exc:
                issues.append(Issue("error", "pptx.slide_xml", str(exc), slide_name))
                continue
            text = " ".join(
                node.text or "" for node in root.findall(".//a:t", NS)
            ).strip()
            has_visual = bool(
                root.findall(".//p:pic", NS)
                or root.findall(".//p:graphicFrame", NS)
                or root.findall(".//p:cxnSp", NS)
            )
            if not text and not has_visual:
                issues.append(
                    Issue(
                        "warning",
                        "pptx.possible_empty_slide",
                        "Slide has no visible text or supported visual object",
                        f"slide:{slide_index}",
                    )
                )
            normalized_text = text.casefold()
            for term in INTERNAL_TERMS:
                if term in normalized_text:
                    issues.append(
                        Issue(
                            "error",
                            "pptx.internal_term",
                            f"Visible internal workflow term: {term}",
                            f"slide:{slide_index}",
                        )
                    )
            for node in root.findall(".//*[@typeface]"):
                typeface = node.attrib.get("typeface")
                if typeface:
                    font_names.add(typeface)
            for node in root.findall(".//*[@sz]"):
                try:
                    size_pt = int(node.attrib["sz"]) / 100
                except ValueError:
                    continue
                if 0 < size_pt < 9:
                    issues.append(
                        Issue(
                            "warning",
                            "pptx.small_text",
                            f"Text size below 9 pt: {size_pt:g} pt",
                            f"slide:{slide_index}",
                        )
                    )

            slide_rels = _slide_relationships(zf, slide_name)
            for shape in _direct_shapes(root):
                box = _shape_box(shape)
                if box is None:
                    continue
                x, y, width, height = box
                shape_name = _shape_name(shape)
                if width < 0 or height < 0:
                    issues.append(
                        Issue(
                            "error",
                            "pptx.shape_extent",
                            f"Negative shape extent: {shape_name}",
                            f"slide:{slide_index}",
                        )
                    )
                if slide_width and slide_height:
                    entirely_outside = (
                        x + width <= 0
                        or y + height <= 0
                        or x >= slide_width
                        or y >= slide_height
                    )
                    partly_outside = (
                        x < 0
                        or y < 0
                        or x + width > slide_width
                        or y + height > slide_height
                    )
                    if entirely_outside:
                        issues.append(
                            Issue(
                                "error",
                                "pptx.shape_outside",
                                f"Shape is entirely outside the slide: {shape_name}",
                                f"slide:{slide_index}",
                            )
                        )
                    elif partly_outside:
                        issues.append(
                            Issue(
                                "warning",
                                "pptx.shape_bleed",
                                f"Shape extends beyond slide bounds: {shape_name}",
                                f"slide:{slide_index}",
                            )
                        )
                if shape.findall(".//a:t", NS):
                    text_boxes.append((slide_index, shape_name, box))

                blip = shape.find(".//a:blip", NS)
                rel_id = blip.attrib.get(R_ID) if blip is not None else None
                if rel_id and rel_id in slide_rels:
                    media_name, external = slide_rels[rel_id]
                    if not external and media_name in names and width > 0 and height > 0:
                        pixels = _image_size(zf.read(media_name))
                        if pixels:
                            ppi_x = pixels[0] / (width / EMU_PER_INCH)
                            ppi_y = pixels[1] / (height / EMU_PER_INCH)
                            effective_ppi = min(ppi_x, ppi_y)
                            if effective_ppi < 120:
                                issues.append(
                                    Issue(
                                        "warning",
                                        "pptx.low_image_ppi",
                                        f"Effective image resolution is about {effective_ppi:.0f} PPI",
                                        f"slide:{slide_index}:{shape_name}",
                                    )
                                )

        details["fonts"] = sorted(font_names, key=str.casefold)
        by_slide: dict[int, list[tuple[str, tuple[int, int, int, int]]]] = {}
        for slide_index, name, box in text_boxes:
            by_slide.setdefault(slide_index, []).append((name, box))
        for slide_index, boxes in by_slide.items():
            for first_index, (first_name, first_box) in enumerate(boxes):
                for second_name, second_box in boxes[first_index + 1 :]:
                    ratio = _intersection_ratio(first_box, second_box)
                    if ratio >= 0.25:
                        issues.append(
                            Issue(
                                "warning",
                                "pptx.possible_text_overlap",
                                f"Text-bearing shapes overlap by {ratio:.0%}: "
                                f"{first_name} / {second_name}",
                                f"slide:{slide_index}",
                            )
                        )

        if project is not None:
            expected_slides = project.get("slides", [])
            if isinstance(expected_slides, list) and len(expected_slides) != len(slide_names):
                issues.append(
                    Issue(
                        "error",
                        "project.slide_count",
                        f"project.json has {len(expected_slides)} slides but PPTX has "
                        f"{len(slide_names)}",
                        "project.slides",
                    )
                )
            expected_canvas = project.get("canvas", {})
            actual_canvas = details["canvas_inches"]
            if isinstance(expected_canvas, dict) and actual_canvas:
                expected_width = expected_canvas.get("width_inches")
                expected_height = expected_canvas.get("height_inches")
                if isinstance(expected_width, (int, float)) and isinstance(
                    expected_height, (int, float)
                ):
                    if (
                        abs(expected_width - actual_canvas["width"]) > 0.02
                        or abs(expected_height - actual_canvas["height"]) > 0.02
                    ):
                        issues.append(
                            Issue(
                                "error",
                                "project.canvas_mismatch",
                                "project.json canvas does not match PPTX canvas",
                                "project.canvas",
                            )
                        )

    return make_report("qa_pptx", issues, **details)


def apply_qa_to_project(
    project: dict[str, Any],
    report: dict[str, Any],
    report_path: Path | None = None,
) -> dict[str, Any]:
    project["qa"] = {
        "status": report["status"],
        "issues": report["issues"],
        "skipped_checks": project.get("qa", {}).get("skipped_checks", []),
    }
    steps = project.get("workflow", {}).get("steps", {})
    if isinstance(steps, dict):
        steps["static-qa"] = {
            "status": "completed",
            "reason": "Deterministic PPTX static QA executed.",
        }
    artifacts = project.get("artifacts", {})
    if isinstance(artifacts, dict) and report_path:
        artifacts["qa_report"] = str(report_path).replace("\\", "/")
    return project


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic static QA on a PPTX.")
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--project", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument(
        "--update-project",
        action="store_true",
        help="Write QA status/issues back to --project after the check.",
    )
    args = parser.parse_args()

    if args.update_project and not args.project:
        parser.error("--update-project requires --project")
    project = load_json(args.project) if args.project else None
    report = inspect_pptx(args.pptx, project)
    if args.report:
        write_json(args.report, report)
    if args.update_project and args.project and project is not None:
        write_json(
            args.project,
            apply_qa_to_project(project, report, args.report),
        )
    print_report(report)
    return 1 if report["summary"]["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
