from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.package_skill import build_package, re_safe_version
from scripts.preflight import probe


ROOT = Path(__file__).resolve().parents[1]


class PreflightAndPackageTests(unittest.TestCase):
    def test_preflight_reports_python(self) -> None:
        report = probe()
        self.assertIn("python", report["capabilities"])
        self.assertTrue(report["capabilities"]["filesystem"]["available"])

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


if __name__ == "__main__":
    unittest.main()
