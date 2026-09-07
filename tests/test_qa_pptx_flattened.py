from __future__ import annotations

import struct
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.qa_pptx import EMU_PER_INCH, inspect_pptx


SLIDE_WIDTH = 13.333
SLIDE_HEIGHT = 7.5


def emu(inches: float) -> int:
    return round(inches * EMU_PER_INCH)


def fake_png_header(width: int = 2400, height: int = 1350) -> bytes:
    return b"\x89PNG\r\n\x1a\n" + b"\x00" * 8 + struct.pack(">II", width, height)


def picture_shape(
    shape_id: int,
    name: str,
    rel_id: str,
    x: float,
    y: float,
    width: float,
    height: float,
) -> str:
    return f"""
    <p:pic>
      <p:nvPicPr><p:cNvPr id="{shape_id}" name="{name}"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr>
      <p:blipFill><a:blip r:embed="{rel_id}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
      <p:spPr>
        <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(width)}" cy="{emu(height)}"/></a:xfrm>
        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
      </p:spPr>
    </p:pic>
    """


def text_shape(shape_id: int, text: str) -> str:
    return f"""
    <p:sp>
      <p:nvSpPr><p:cNvPr id="{shape_id}" name="TITLE_Overlay"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
      <p:spPr>
        <a:xfrm><a:off x="{emu(0.5)}" y="{emu(0.3)}"/><a:ext cx="{emu(6)}" cy="{emu(0.6)}"/></a:xfrm>
        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
      </p:spPr>
      <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr sz="3200"/><a:t>{text}</a:t></a:r></a:p></p:txBody>
    </p:sp>
    """


def write_fixture(
    path: Path,
    pictures: list[tuple[str, float, float, float, float]],
    *,
    overlay_text: str | None = None,
    image_background: bool = False,
) -> None:
    relationships: list[str] = []
    media: list[tuple[str, bytes]] = []
    shapes: list[str] = []
    next_shape_id = 2
    for index, (name, x, y, width, height) in enumerate(pictures, start=1):
        rel_id = f"rIdImage{index}"
        media_name = f"image{index}.png"
        relationships.append(
            f'<Relationship Id="{rel_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{media_name}"/>'
        )
        media.append((f"ppt/media/{media_name}", fake_png_header()))
        shapes.append(
            picture_shape(next_shape_id, name, rel_id, x, y, width, height)
        )
        next_shape_id += 1

    background_xml = ""
    if image_background:
        rel_id = "rIdBackground"
        relationships.append(
            f'<Relationship Id="{rel_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/background.png"/>'
        )
        media.append(("ppt/media/background.png", fake_png_header()))
        background_xml = f"""
    <p:bg><p:bgPr><a:blipFill><a:blip r:embed="{rel_id}"/><a:stretch><a:fillRect/></a:stretch></a:blipFill><a:effectLst/></p:bgPr></p:bg>
        """

    if overlay_text is not None:
        shapes.append(text_shape(next_shape_id, overlay_text))

    slide_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>{background_xml}<p:spTree>
    <p:nvGrpSpPr><p:cNvPr id="1" name="Root"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
    <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    {''.join(shapes)}
  </p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>
"""
    presentation_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst>
  <p:sldSz cx="{emu(SLIDE_WIDTH)}" cy="{emu(SLIDE_HEIGHT)}" type="screen16x9"/>
</p:presentation>
"""
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as package:
        package.writestr("[Content_Types].xml", "<Types/>")
        package.writestr(
            "_rels/.rels",
            """<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>""",
        )
        package.writestr("ppt/presentation.xml", presentation_xml)
        package.writestr(
            "ppt/_rels/presentation.xml.rels",
            """<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>
</Relationships>""",
        )
        package.writestr("ppt/slides/slide1.xml", slide_xml)
        if relationships:
            package.writestr(
                "ppt/slides/_rels/slide1.xml.rels",
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                + "".join(relationships)
                + "</Relationships>",
            )
        for media_name, data in media:
            package.writestr(media_name, data)


def flattened_issues(report: dict) -> list[dict]:
    return [
        issue
        for issue in report["issues"]
        if issue["code"] == "pptx.possible_flattened_slide"
    ]


class FlattenedSlideQATests(unittest.TestCase):
    def inspect_fixture(self, **kwargs) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            pptx = Path(tmp) / "fixture.pptx"
            write_fixture(pptx, **kwargs)
            return inspect_pptx(pptx)

    def test_full_slide_picture_without_text_warns(self) -> None:
        report = self.inspect_fixture(
            pictures=[("FullSlide", 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)]
        )

        issues = flattened_issues(report)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["severity"], "warning")
        self.assertIn("FullSlide", issues[0]["path"])
        self.assertEqual(report["summary"]["error"], 0)

    def test_full_slide_picture_with_title_overlay_still_warns(self) -> None:
        report = self.inspect_fixture(
            pictures=[("FullSlide", 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)],
            overlay_text="Editable title",
        )

        self.assertEqual(len(flattened_issues(report)), 1)

    def test_full_slide_picture_with_small_logo_still_warns(self) -> None:
        report = self.inspect_fixture(
            pictures=[
                ("FullSlide", 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT),
                ("SmallLogo", 12.3, 0.2, 0.6, 0.4),
            ]
        )

        issues = flattened_issues(report)
        self.assertEqual(len(issues), 1)
        self.assertIn("FullSlide", issues[0]["path"])

    def test_each_near_full_picture_on_a_multi_picture_page_warns(self) -> None:
        report = self.inspect_fixture(
            pictures=[
                ("FlattenedBase", 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT),
                ("FlattenedOverlay", 0.1, 0.1, 13.1, 7.3),
            ]
        )

        issues = flattened_issues(report)
        self.assertEqual(len(issues), 2)
        self.assertEqual(
            {issue["path"].rsplit(":", 1)[-1] for issue in issues},
            {"FlattenedBase", "FlattenedOverlay"},
        )

    def test_large_in_slide_figure_below_threshold_does_not_warn(self) -> None:
        report = self.inspect_fixture(
            pictures=[("ScientificFigure", 0.5, 0.8, 12.0, 5.8)]
        )

        self.assertEqual(flattened_issues(report), [])

    def test_oversized_picture_with_small_visible_intersection_does_not_warn(self) -> None:
        report = self.inspect_fixture(
            pictures=[("MostlyOffCanvas", -100, -100, 105, 105)]
        )

        self.assertEqual(flattened_issues(report), [])
        codes = {issue["code"] for issue in report["issues"]}
        self.assertIn("pptx.shape_bleed", codes)

    def test_multi_picture_page_without_near_full_picture_does_not_warn(self) -> None:
        report = self.inspect_fixture(
            pictures=[
                ("PanelA", 0.5, 0.8, 5.8, 2.6),
                ("PanelB", 7.0, 0.8, 5.8, 2.6),
                ("PanelC", 0.5, 4.0, 5.8, 2.6),
                ("PanelD", 7.0, 4.0, 5.8, 2.6),
            ]
        )

        self.assertEqual(flattened_issues(report), [])

    def test_slide_level_image_background_warns_for_manual_review(self) -> None:
        report = self.inspect_fixture(pictures=[], image_background=True)

        issues = flattened_issues(report)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["severity"], "warning")
        self.assertEqual(issues[0]["path"], "slide:1:background-image")
        self.assertEqual(report["summary"]["error"], 0)


if __name__ == "__main__":
    unittest.main()
