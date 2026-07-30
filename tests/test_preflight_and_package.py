from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.package_skill import build_package, re_safe_version
from scripts.preflight import probe


ROOT = Path(__file__).resolve().parents[1]


class PreflightAndPackageTests(unittest.TestCase):
    def test_preflight_reports_python(self) -> None:
        report = probe()
        self.assertIn("python", report["capabilities"])
        self.assertTrue(report["capabilities"]["filesystem"]["available"])
        for capability in report["capabilities"].values():
            self.assertEqual(
                {"available", "provider", "notes"},
                set(capability),
            )
        self.assertIn("cjk_font_candidates", report["details"])

    def test_release_version_filter(self) -> None:
        self.assertTrue(re_safe_version("3.4.0-dev"))
        self.assertFalse(re_safe_version("../unsafe"))
        self.assertFalse(re_safe_version("版本一"))
        self.assertFalse(re_safe_version(""))

    def test_package_is_deterministic_and_excludes_legacy_template(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.zip"
            second = Path(directory) / "second.zip"
            first_result = build_package(ROOT, first, "test")
            second_result = build_package(ROOT, second, "test")
            self.assertEqual(first_result["sha256"], second_result["sha256"])
            self.assertFalse(first_result["legacy_template_included"])
            with zipfile.ZipFile(first) as archive:
                names = set(archive.namelist())
            prefix = "scholar-ppt-cn/assets/visual-reference-packs/blue-academic/"
            self.assertIn("scholar-ppt-cn/requirements-runtime.txt", names)
            self.assertIn("scholar-ppt-cn/scripts/build_deck.py", names)
            self.assertIn("scholar-ppt-cn/scripts/pptx_runtime.py", names)
            self.assertIn(
                "scholar-ppt-cn/references/fallback_pptx_runtime.md",
                names,
            )
            self.assertIn(f"{prefix}pack.json", names)
            self.assertIn(f"{prefix}images/cover-01.png", names)
            self.assertNotIn(f"{prefix}contact-sheet.png", names)
            self.assertFalse(
                any(name.startswith(f"{prefix}generation/") for name in names)
            )


if __name__ == "__main__":
    unittest.main()
