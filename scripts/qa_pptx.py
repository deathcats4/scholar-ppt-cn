from __future__ import annotations

import argparse
import io
import hashlib
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
DEFAULT_QA_PROFILE = "group-meeting"
QA_PROFILES: dict[str, dict[str, Any]] = {
    "group-meeting": {
        "strict_projection": True,
    },
    "defense": {
        "strict_projection": True,
    },
    "conference": {
        "strict_projection": True,
    },
    "classroom": {
        "strict_projection": True,
    },
    "template-preserve": {
        "strict_projection": False,
        "allow_legacy_icon_fonts": True,
    },
}
TEXT_ROLE_PREFIXES = {
    "TITLE_": "title",
    "BODY_": "body",
    "LABEL_": "label",
    "CAPTION_": "caption",
    "SOURCE_": "source",
    "PAGE_NUMBER_": "source",
}
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
    "design rationale",
    "设计理由",
    "reading order",
    "阅读顺序",
    "risk level",
    "风险等级",
    "candidate plan",
    "候选方案",
    "rebuild queue",
    "visual_review",
    "source_ref",
    "project.json",
    "system prompt",
    "系统指令",
    "提示词",
    "pptxgenjs",
    "python-pptx",
)

DISALLOWED_PRESENTATION_LABELS = (
    "读图要点",
    "读图结论",
    "关键认识",
    "综合判断",
    "支持证据",
    "注意事项",
    "证据观察",
    "预期输出",
    "本文切口",
    "基于论文证据的结构化归纳",
    "作者解释",
    "作者综合模型",
    "证据锚点",
    "本页重点",
    "一句话结论",
)

MODEL_META_TERMS = (
    "作为 ai",
    "作为一个语言模型",
    "根据你的要求",
    "以下是为你生成的",
    "我将为你",
    "todo",
    "tbd",
    "lorem ipsum",
    "示例文本",
    "在此插入图片",
    "点击添加标题",
    "点击添加文本",
    "placeholder",
)

DISALLOWED_ICON_GLYPHS = (
    "💡",
    "📖",
    "📚",
    "📄",
    "📑",
    "👤",
    "👥",
    "🌍",
    "🌎",
    "🌏",
    "👁",
    "👀",
    "🎯",
    "🏆",
    "🧩",
    "⚙",
    "✅",
    "☑",
    "❗",
    "⚠",
    "🔬",
    "⚗",
    "🔨",
    "◎",
    "✦",
    "▤",
    "▰",
    "↻",
)

DISALLOWED_ICON_FONT_MARKERS = (
    "wingdings",
    "webdings",
    "font awesome",
    "material icons",
    "material symbols",
    "segoe ui emoji",
    "apple color emoji",
    "noto color emoji",
)

EVIDENCE_PAGE_LABEL_PATTERN = re.compile(
    r"证据页\s*[12一二]\s*/\s*2", re.IGNORECASE
)
EDITORIAL_WARNING_PREFIX_PATTERN = re.compile(
    r"^\s*(?:提示|注意)\s*[：:]", re.IGNORECASE
)


def _visible_policy_hits(text: str) -> list[tuple[str, str]]:
    normalized = text.casefold()
    hits: list[tuple[str, str]] = []
    for term in DISALLOWED_PRESENTATION_LABELS:
        if term.casefold() in normalized:
            hits.append(("label", term))
    if EVIDENCE_PAGE_LABEL_PATTERN.search(text):
        hits.append(("label", "证据页 1/2 or 2/2"))
    for term in MODEL_META_TERMS:
        if term in normalized:
            hits.append(("model-meta", term))
    return hits


REQUIRED_PARTS = {
    "[Content_Types].xml",
    "_rels/.rels",
    "ppt/presentation.xml",
}
R_ID = f"{{{NS['r']}}}embed"
R_REL_ID = f"{{{NS['r']}}}id"


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


def _relationship_entries(
    root: ET.Element, base_part: str
) -> dict[str, tuple[str, bool, str]]:
    result: dict[str, tuple[str, bool, str]] = {}
    for rel in root.findall("rel:Relationship", NS):
        rel_id = rel.attrib.get("Id", "")
        external = rel.attrib.get("TargetMode") == "External"
        target = rel.attrib.get("Target", "")
        result[rel_id] = (
            target if external else _resolve_target(base_part, target),
            external,
            rel.attrib.get("Type", ""),
        )
    return result


def _presentation_slide_names(
    presentation: ET.Element,
    presentation_rels: dict[str, tuple[str, bool, str]],
    slide_parts: set[str],
    issues: list[Issue],
) -> list[str]:
    slide_list = presentation.find("p:sldIdLst", NS)
    slide_nodes = [] if slide_list is None else slide_list.findall("p:sldId", NS)
    ordered: list[str] = []
    seen_targets: set[str] = set()
    for index, slide_node in enumerate(slide_nodes, start=1):
        rel_id = slide_node.attrib.get(R_REL_ID)
        if not rel_id:
            issues.append(
                Issue(
                    "error",
                    "pptx.slide_relationship",
                    "Slide entry has no relationship id",
                    f"ppt/presentation.xml:sldId[{index}]",
                )
            )
            continue
        relationship = presentation_rels.get(rel_id)
        if relationship is None:
            issues.append(
                Issue(
                    "error",
                    "pptx.slide_relationship",
                    f"Slide relationship does not exist: {rel_id}",
                    f"ppt/presentation.xml:sldId[{index}]",
                )
            )
            continue
        target, external, rel_type = relationship
        if external:
            issues.append(
                Issue(
                    "error",
                    "pptx.slide_relationship",
                    f"Slide relationship cannot be external: {rel_id}",
                    f"ppt/presentation.xml:sldId[{index}]",
                )
            )
            continue
        if rel_type != "slide" and not rel_type.endswith("/slide"):
            issues.append(
                Issue(
                    "error",
                    "pptx.slide_relationship_type",
                    f"Relationship {rel_id} is not a slide relationship",
                    "ppt/_rels/presentation.xml.rels",
                )
            )
            continue
        if target in seen_targets:
            issues.append(
                Issue(
                    "error",
                    "pptx.duplicate_slide_reference",
                    f"Slide part is referenced more than once: {target}",
                    "ppt/presentation.xml",
                )
            )
            continue
        seen_targets.add(target)
        if target not in slide_parts:
            issues.append(
                Issue(
                    "error",
                    "pptx.slide_relationship_target",
                    f"Slide relationship target does not exist: {target or '<empty>'}",
                    f"ppt/presentation.xml:sldId[{index}]",
                )
            )
            continue
        ordered.append(target)

    for orphan in sorted(slide_parts - seen_targets, key=_natural_slide_key):
        issues.append(
            Issue(
                "error",
                "pptx.orphan_slide_part",
                "Slide part is not referenced by presentation.xml",
                orphan,
            )
        )
    return ordered


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


ShapeRecord = tuple[ET.Element, tuple[int, int, int, int], str]
Transform = tuple[float, float, float, float]


def _slide_shapes(root: ET.Element) -> list[ShapeRecord]:
    tree = root.find(".//p:cSld/p:spTree", NS)
    if tree is None:
        return []
    records: list[ShapeRecord] = []
    for child in tree:
        records.extend(_iter_shape_records(child, (1.0, 1.0, 0.0, 0.0), ()))
    return records


def _iter_shape_records(
    node: ET.Element,
    transform: Transform,
    name_path: tuple[str, ...],
) -> list[ShapeRecord]:
    supported = {
        f"{{{NS['p']}}}sp",
        f"{{{NS['p']}}}pic",
        f"{{{NS['p']}}}graphicFrame",
        f"{{{NS['p']}}}cxnSp",
    }
    if node.tag == f"{{{NS['p']}}}grpSp":
        group_name = _shape_name(node)
        group_transform = _compose_group_transform(node, transform)
        group_path = name_path + (group_name,)
        records: list[ShapeRecord] = []
        for child in node:
            records.extend(_iter_shape_records(child, group_transform, group_path))
        return records
    if node.tag not in supported:
        return []
    box = _shape_box(node)
    if box is None:
        return []
    shape_name = _shape_name(node)
    display_name = " / ".join(name_path + (shape_name,)) if name_path else shape_name
    return [(node, _apply_transform(box, transform), display_name)]


def _xfrm_box(xfrm: ET.Element | None) -> tuple[int, int, int, int] | None:
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


def _compose_group_transform(group: ET.Element, parent: Transform) -> Transform:
    parent_sx, parent_sy, parent_tx, parent_ty = parent
    xfrm = group.find("p:grpSpPr/a:xfrm", NS)
    group_box = _xfrm_box(xfrm)
    if group_box is None:
        return parent
    group_x, group_y, group_w, group_h = group_box
    ch_off = xfrm.find("a:chOff", NS) if xfrm is not None else None
    ch_ext = xfrm.find("a:chExt", NS) if xfrm is not None else None
    try:
        child_x = int(ch_off.attrib.get("x", "0")) if ch_off is not None else 0
        child_y = int(ch_off.attrib.get("y", "0")) if ch_off is not None else 0
        child_w = int(ch_ext.attrib.get("cx", str(group_w))) if ch_ext is not None else group_w
        child_h = int(ch_ext.attrib.get("cy", str(group_h))) if ch_ext is not None else group_h
    except ValueError:
        return parent
    if child_w == 0 or child_h == 0:
        return parent
    group_sx = group_w / child_w
    group_sy = group_h / child_h
    return (
        parent_sx * group_sx,
        parent_sy * group_sy,
        parent_sx * (group_x - group_sx * child_x) + parent_tx,
        parent_sy * (group_y - group_sy * child_y) + parent_ty,
    )


def _apply_transform(box: tuple[int, int, int, int], transform: Transform) -> tuple[int, int, int, int]:
    sx, sy, tx, ty = transform
    x, y, width, height = box
    return (
        round(sx * x + tx),
        round(sy * y + ty),
        round(abs(sx) * width),
        round(abs(sy) * height),
    )


def _shape_box(shape: ET.Element) -> tuple[int, int, int, int] | None:
    if shape.tag == f"{{{NS['p']}}}graphicFrame":
        xfrm = shape.find("p:xfrm", NS)
    else:
        xfrm = shape.find("p:spPr/a:xfrm", NS)
    return _xfrm_box(xfrm)


def _shape_name(shape: ET.Element) -> str:
    props = shape.find("p:nvSpPr/p:cNvPr", NS)
    if props is None:
        props = shape.find("p:nvPicPr/p:cNvPr", NS)
    if props is None:
        props = shape.find("p:nvGraphicFramePr/p:cNvPr", NS)
    if props is None:
        props = shape.find("p:nvCxnSpPr/p:cNvPr", NS)
    if props is None:
        props = shape.find("p:nvGrpSpPr/p:cNvPr", NS)
    return props.attrib.get("name", "unnamed") if props is not None else "unnamed"


def _shape_text(shape: ET.Element) -> str:
    return " ".join(node.text or "" for node in shape.findall(".//a:t", NS)).strip()


def _shape_font_sizes(shape: ET.Element) -> list[float]:
    sizes: list[float] = []
    for node in shape.findall(".//*[@sz]"):
        try:
            value = int(node.attrib["sz"]) / 100
        except (KeyError, ValueError):
            continue
        if value > 0:
            sizes.append(value)
    return sizes


def _shape_norm_autofit(shape: ET.Element) -> tuple[bool, float]:
    node = shape.find(".//a:bodyPr/a:normAutofit", NS)
    if node is None:
        return False, 1.0
    raw_scale = node.attrib.get("fontScale", "100000")
    try:
        scale = int(raw_scale) / 100000
    except ValueError:
        scale = 1.0
    if scale <= 0:
        scale = 1.0
    return True, scale


def _shape_text_role(
    shape_name: str,
    text: str,
    box: tuple[int, int, int, int],
    slide_height: int,
    sizes: list[float],
) -> str:
    normalized_names = [shape_name.strip().upper()]
    if "/" in shape_name:
        normalized_names.append(shape_name.rsplit("/", 1)[-1].strip().upper())
    for normalized_name in normalized_names:
        for prefix, role in TEXT_ROLE_PREFIXES.items():
            if normalized_name.startswith(prefix):
                return role
    if _is_source_footer_or_page_number(text, box, slide_height):
        return "source"
    if _is_necessary_caption(text):
        return "caption"

    _x, y, _w, height = box
    if (
        slide_height
        and y <= slide_height * 0.2
        and height <= 1.25 * EMU_PER_INCH
        and sizes
        and max(sizes) >= 26
    ):
        return "title"

    compact = re.sub(r"\s+", "", text)
    if len(compact) <= 14 and height <= 0.6 * EMU_PER_INCH:
        return "label"
    return "body"


def _is_source_footer_or_page_number(
    text: str, box: tuple[int, int, int, int], slide_height: int
) -> bool:
    normalized = text.strip().casefold()
    _x, y, _w, h = box
    near_bottom = bool(slide_height) and y + h >= slide_height * 0.86
    source_like = bool(
        re.match(
            r"^(?:图源|资料来源|来源|源文献|source|sources|reference|references|copyright|©|doi\b)",
            normalized,
        )
    )
    page_number = bool(re.fullmatch(r"(?:0?[1-9]|[1-9]\d{1,2})", normalized))
    return source_like or (near_bottom and page_number)


def _is_necessary_caption(text: str) -> bool:
    normalized = text.strip().casefold()
    if len(normalized) > 180:
        return False
    return bool(
        re.match(
            r"^(?:图\s*\d+|表\s*\d+|图注|表注|fig\.?\s*\d+|figure\s*\d+|table\s*\d+|注\s*[：:])",
            normalized,
        )
    )


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


def inspect_pptx(
    path: Path,
    project: dict[str, Any] | None = None,
    profile: str = DEFAULT_QA_PROFILE,
) -> dict[str, Any]:
    if profile not in QA_PROFILES:
        raise ValueError(f"Unknown QA profile: {profile}")
    profile_rules = QA_PROFILES[profile]
    strict_projection = bool(profile_rules["strict_projection"])

    issues: list[Issue] = []
    details: dict[str, Any] = {
        "pptx": str(path),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None,
        "slide_count": 0,
        "canvas_inches": None,
        "fonts": [],
        "media_count": 0,
        "security_parts": [],
        "qa_profile": profile,
        "typography": {
            "strict_projection": strict_projection,
            "body_text_boxes": 0,
            "body_norm_autofit": 0,
        },
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

        try:
            presentation = _xml(zf, "ppt/presentation.xml")
        except ET.ParseError as exc:
            issues.append(
                Issue(
                    "error",
                    "pptx.presentation_xml",
                    str(exc),
                    "ppt/presentation.xml",
                )
            )
            return make_report("qa_pptx", issues, **details)
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

        relationship_maps: dict[str, dict[str, tuple[str, bool, str]]] = {}
        for rel_name in sorted(name for name in names if name.endswith(".rels")):
            try:
                rel_root = _xml(zf, rel_name)
            except ET.ParseError as exc:
                issues.append(
                    Issue("error", "pptx.relationship_xml", str(exc), rel_name)
                )
                relationship_maps[rel_name] = {}
                continue
            base_part = _relationship_base(rel_name)
            rel_entries = _relationship_entries(rel_root, base_part)
            relationship_maps[rel_name] = rel_entries
            for target, external, _rel_type in rel_entries.values():
                if external:
                    issues.append(
                        Issue(
                            "warning",
                            "pptx.external_relationship",
                            f"External relationship target: {target}",
                            rel_name,
                        )
                    )
                    continue
                if target and target not in names:
                    issues.append(
                        Issue(
                            "error",
                            "pptx.broken_relationship",
                            f"Relationship target does not exist: {target}",
                            rel_name,
                        )
                    )

        presentation_rel_name = "ppt/_rels/presentation.xml.rels"
        if presentation_rel_name not in names:
            issues.append(
                Issue(
                    "error",
                    "pptx.presentation_relationships",
                    "Missing presentation relationship part",
                    presentation_rel_name,
                )
            )
        slide_parts = {
            name
            for name in names
            if PurePosixPath(name).parent == PurePosixPath("ppt/slides")
            and name.endswith(".xml")
        }
        slide_names = _presentation_slide_names(
            presentation,
            relationship_maps.get(presentation_rel_name, {}),
            slide_parts,
            issues,
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
            for hit_type, value in _visible_policy_hits(text):
                code = (
                    "pptx.disallowed_presentation_label"
                    if hit_type == "label"
                    else "pptx.model_meta_language"
                )
                message = (
                    f"Disallowed presentation label: {value}"
                    if hit_type == "label"
                    else f"Visible model/generation language: {value}"
                )
                issues.append(
                    Issue(
                        "error",
                        code,
                        message,
                        f"slide:{slide_index}",
                    )
                )
            icon_fonts_on_slide: set[str] = set()
            for node in root.findall(".//*[@typeface]"):
                typeface = node.attrib.get("typeface")
                if typeface:
                    font_names.add(typeface)
                    folded_typeface = typeface.casefold()
                    if any(marker in folded_typeface for marker in DISALLOWED_ICON_FONT_MARKERS):
                        icon_fonts_on_slide.add(typeface)
            for typeface in sorted(icon_fonts_on_slide, key=str.casefold):
                icon_font_severity = (
                    "warning"
                    if profile_rules.get("allow_legacy_icon_fonts")
                    else "error"
                )
                issues.append(
                    Issue(
                        icon_font_severity,
                        "pptx.disallowed_icon_font",
                        f"Disallowed icon or emoji font used: {typeface}",
                        f"slide:{slide_index}",
                    )
                )
            slide_path = PurePosixPath(slide_name)
            slide_rel_name = str(
                slide_path.parent / "_rels" / f"{slide_path.name}.rels"
            )
            slide_rels = relationship_maps.get(slide_rel_name, {})
            slide_shapes = _slide_shapes(root)
            picture_boxes: list[tuple[str, tuple[int, int, int, int]]] = []
            for shape, box, shape_name in slide_shapes:
                x, y, width, height = box
                if shape.tag == f"{{{NS['p']}}}pic":
                    picture_boxes.append((shape_name, box))
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
                    shape_text = _shape_text(shape)
                    for glyph in DISALLOWED_ICON_GLYPHS:
                        if glyph in shape_text:
                            issues.append(
                                Issue(
                                    "error",
                                    "pptx.disallowed_commercial_icon_glyph",
                                    f"Disallowed commercial-course icon or decorative glyph: {glyph}",
                                    f"slide:{slide_index}:{shape_name}",
                                )
                            )
                    if EDITORIAL_WARNING_PREFIX_PATTERN.match(shape_text):
                        issues.append(
                            Issue(
                                "error",
                                "pptx.disallowed_editorial_prefix",
                                "Generic 提示：/注意： editorial prefix should be rewritten as a direct academic statement",
                                f"slide:{slide_index}:{shape_name}",
                            )
                        )
                    issue_path = f"slide:{slide_index}:{shape_name}"
                    sizes = _shape_font_sizes(shape)
                    has_norm_autofit, autofit_scale = _shape_norm_autofit(shape)
                    role = _shape_text_role(
                        shape_name, shape_text, box, slide_height, sizes
                    )
                    if role == "body":
                        typography = details["typography"]
                        typography["body_text_boxes"] += 1
                    if sizes:
                        declared_min_size = min(sizes)
                        effective_min_size = declared_min_size * autofit_scale

                        if effective_min_size < 9:
                            issues.append(
                                Issue(
                                    "warning",
                                    "pptx.small_text",
                                    f"Effective text size below 9 pt: {effective_min_size:g} pt",
                                    issue_path,
                                )
                            )

                        if role == "body":
                            if has_norm_autofit:
                                typography["body_norm_autofit"] += 1
                                issues.append(
                                    Issue(
                                        "warning",
                                        "pptx.body_autofit",
                                        "Body text uses normAutofit/shrink-to-fit; "
                                        f"declared {declared_min_size:g} pt, fontScale "
                                        f"{autofit_scale:.0%}, effective {effective_min_size:g} pt",
                                        issue_path,
                                    )
                                )
                        elif role == "label" and effective_min_size < 16:
                            issues.append(
                                Issue(
                                    "warning",
                                    "pptx.label_text_too_small",
                                    f"Label text effective size is below 16 pt: "
                                    f"{effective_min_size:g} pt",
                                    issue_path,
                                )
                            )
                        elif role == "caption" and effective_min_size < 12:
                            issues.append(
                                Issue(
                                    "warning",
                                    "pptx.caption_text_too_small",
                                    f"Caption effective size is below 12 pt: "
                                    f"{effective_min_size:g} pt",
                                    issue_path,
                                )
                            )

                blip = shape.find(".//a:blip", NS)
                rel_id = blip.attrib.get(R_ID) if blip is not None else None
                if rel_id and rel_id in slide_rels:
                    media_name, external, _rel_type = slide_rels[rel_id]
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

            if not text and slide_width and slide_height and len(picture_boxes) == 1:
                picture_name, picture_box = picture_boxes[0]
                _px, _py, picture_width, picture_height = picture_box
                coverage = (picture_width * picture_height) / max(slide_width * slide_height, 1)
                if coverage >= 0.9:
                    issues.append(
                        Issue(
                            "warning",
                            "pptx.possible_flattened_slide",
                            "Slide appears to be a single near-full-slide image; verify editability",
                            f"slide:{slide_index}:{picture_name}",
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
        "--profile",
        choices=sorted(QA_PROFILES),
        default=DEFAULT_QA_PROFILE,
        help=(
            "Typography/QA profile. Body font-size findings follow v3.3.1 "
            "behavior: report readability concerns without turning body size "
            "or body auto-shrink into delivery-blocking errors."
        ),
    )
    parser.add_argument(
        "--update-project",
        action="store_true",
        help="Write QA status/issues back to --project after the check.",
    )
    args = parser.parse_args()

    if args.update_project and not args.project:
        parser.error("--update-project requires --project")
    project = load_json(args.project) if args.project else None
    report = inspect_pptx(args.pptx, project, profile=args.profile)
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
