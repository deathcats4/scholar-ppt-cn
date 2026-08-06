from __future__ import annotations

import struct
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.qa_pptx import EMU_PER_INCH, inspect_pptx


def emu(inches: float) -> int:
    return round(inches * EMU_PER_INCH)


def fake_png_header(width: int, height: int) -> bytes:
    return b"\x89PNG\r\n\x1a\n" + b"\x00" * 8 + struct.pack(">II", width, height)


def text_shape(
    shape_id: int,
    name: str,
    x: float,
    y: float,
    width: float,
    height: float,
    text: str,
    size: int | None = None,
    autofit: bool = False,
) -> str:
    rpr = f'<a:rPr lang="zh-CN" sz="{size}"><a:latin typeface="Microsoft YaHei"/></a:rPr>' if size else ""
    autofit_xml = '<a:normAutofit fontScale="50000"/>' if autofit else ""
    return f"""
    <p:sp>
      <p:nvSpPr><p:cNvPr id="{shape_id}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
      <p:spPr>
        <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(width)}" cy="{emu(height)}"/></a:xfrm>
        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
      </p:spPr>
      <p:txBody><a:bodyPr>{autofit_xml}</a:bodyPr><a:lstStyle/><a:p><a:r>{rpr}<a:t>{text}</a:t></a:r></a:p></p:txBody>
    </p:sp>
    """


def picture_shape(shape_id: int, name: str, x: float, y: float, width: float, height: float) -> str:
    return f"""
    <p:pic>
      <p:nvPicPr><p:cNvPr id="{shape_id}" name="{name}"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr>
      <p:blipFill><a:blip r:embed="rIdImage"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
      <p:spPr>
        <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(width)}" cy="{emu(height)}"/></a:xfrm>
        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
      </p:spPr>
    </p:pic>
    """


def write_group_fixture(path: Path) -> None:
    slide_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree>
    <p:nvGrpSpPr><p:cNvPr id="1" name="Root"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
    <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    <p:grpSp>
      <p:nvGrpSpPr><p:cNvPr id="2" name="Group 1"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm><a:off x="0" y="0"/><a:ext cx="{emu(13.333)}" cy="{emu(7.5)}"/><a:chOff x="0" y="0"/><a:chExt cx="{emu(13.333)}" cy="{emu(7.5)}"/></a:xfrm>
      </p:grpSpPr>
      {text_shape(3, "BODY_GroupedSmall", 1.0, 1.0, 2.0, 0.5, "Alpha", size=800, autofit=True)}
      {text_shape(4, "BODY_GroupedInherited", 1.1, 1.1, 2.0, 0.5, "Beta")}
      {picture_shape(5, "GroupedPicture", 1.0, 2.0, 2.0, 2.0)}
      {text_shape(6, "BODY_GroupedOutside", 14.0, 1.0, 0.5, 0.5, "Outside", size=1200)}
    </p:grpSp>
  </p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>
"""
    presentation_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst>
  <p:sldSz cx="{emu(13.333)}" cy="{emu(7.5)}" type="screen16x9"/>
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
        package.writestr(
            "ppt/slides/_rels/slide1.xml.rels",
            """<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rIdImage" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.png"/>
</Relationships>""",
        )
        package.writestr("ppt/media/image1.png", fake_png_header(100, 100))


def write_body_autofit_fixture(path: Path) -> None:
    slide_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree>
    <p:nvGrpSpPr><p:cNvPr id="1" name="Root"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
    <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    {text_shape(2, "BODY_SmallAutofit", 1.0, 1.0, 3.0, 0.7, "Alpha", size=800, autofit=True)}
  </p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>
"""
    presentation_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst>
  <p:sldSz cx="{emu(13.333)}" cy="{emu(7.5)}" type="screen16x9"/>
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


class GroupShapeQATests(unittest.TestCase):
    def test_grouped_shapes_participate_in_static_qa(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pptx = Path(tmp) / "grouped.pptx"
            write_group_fixture(pptx)

            report = inspect_pptx(pptx)

        codes = {issue["code"] for issue in report["issues"]}
        messages = "\n".join(issue["message"] for issue in report["issues"])
        paths = "\n".join(issue["path"] for issue in report["issues"])
        self.assertIn("pptx.shape_outside", codes)
        self.assertIn("pptx.small_text", codes)
        self.assertIn("pptx.body_autofit", codes)
        self.assertIn("pptx.low_image_ppi", codes)
        self.assertIn("pptx.possible_text_overlap", codes)
        self.assertIn("Group 1 / BODY_GroupedOutside", messages)
        self.assertIn("Group 1 / GroupedPicture", paths)
        self.assertIn("Group 1 / BODY_GroupedSmall", messages)
        self.assertEqual(report["details"]["typography"]["body_text_boxes"], 3)
        self.assertEqual(report["details"]["typography"]["body_norm_autofit"], 1)

    def test_small_body_autofit_is_warning_not_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pptx = Path(tmp) / "small-body.pptx"
            write_body_autofit_fixture(pptx)

            report = inspect_pptx(pptx)

        codes = {issue["code"] for issue in report["issues"]}
        self.assertEqual(report["summary"]["error"], 0)
        self.assertEqual(report["status"], "passed-with-warnings")
        self.assertIn("pptx.small_text", codes)
        self.assertIn("pptx.body_autofit", codes)


if __name__ == "__main__":
    unittest.main()
