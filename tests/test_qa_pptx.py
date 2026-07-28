from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.common import load_json
from scripts.qa_pptx import apply_qa_to_project, inspect_pptx


CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
</Types>
"""
ROOT_RELS = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="officeDocument" Target="ppt/presentation.xml"/>
</Relationships>
"""
PRESENTATION = """<?xml version="1.0" encoding="UTF-8"?>
<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst>
  <p:sldSz cx="12192000" cy="6858000"/>
</p:presentation>
"""
PRESENTATION_RELS = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="slide" Target="slides/slide1.xml"/>
</Relationships>
"""


def slide_xml(text: str, x: int = 0) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
 xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <p:cSld><p:spTree>
    <p:nvGrpSpPr/><p:grpSpPr/>
    <p:sp>
      <p:nvSpPr><p:cNvPr id="2" name="Text Box"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
      <p:spPr><a:xfrm><a:off x="{x}" y="0"/><a:ext cx="3000000" cy="1000000"/></a:xfrm></p:spPr>
      <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr sz="1800"/><a:t>{text}</a:t></a:r></a:p></p:txBody>
    </p:sp>
  </p:spTree></p:cSld>
</p:sld>
"""


def make_pptx(path: Path, text: str = "Academic presentation", x: int = 0) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", CONTENT_TYPES)
        archive.writestr("_rels/.rels", ROOT_RELS)
        archive.writestr("ppt/presentation.xml", PRESENTATION)
        archive.writestr("ppt/_rels/presentation.xml.rels", PRESENTATION_RELS)
        archive.writestr("ppt/slides/slide1.xml", slide_xml(text, x))


class PptxQaTests(unittest.TestCase):
    def test_minimal_package_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "valid.pptx"
            make_pptx(path)
            report = inspect_pptx(path)
            self.assertEqual(0, report["summary"]["error"], report)
            self.assertEqual(1, report["details"]["slide_count"])

    def test_internal_term_blocks_delivery(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "internal-term.pptx"
            make_pptx(path, text="Template DNA")
            report = inspect_pptx(path)
            codes = {item["code"] for item in report["issues"]}
            self.assertIn("pptx.internal_term", codes)

    def test_entirely_outside_shape_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "outside.pptx"
            make_pptx(path, x=13000000)
            report = inspect_pptx(path)
            codes = {item["code"] for item in report["issues"]}
            self.assertIn("pptx.shape_outside", codes)

    def test_qa_report_updates_project_state(self) -> None:
        fixture = (
            Path(__file__).resolve().parents[1]
            / "tests"
            / "fixtures"
            / "project-valid.json"
        )
        project = load_json(fixture)
        report = {
            "status": "passed-with-warnings",
            "issues": [
                {
                    "severity": "warning",
                    "code": "demo.warning",
                    "message": "Review",
                    "path": "slide:1",
                }
            ],
        }
        updated = apply_qa_to_project(project, report, Path("out/qa-report.json"))
        self.assertEqual("passed-with-warnings", updated["qa"]["status"])
        self.assertEqual(
            "completed", updated["workflow"]["steps"]["static-qa"]["status"]
        )
        self.assertEqual("out/qa-report.json", updated["artifacts"]["qa_report"])


if __name__ == "__main__":
    unittest.main()
