from __future__ import annotations

import json
import struct
import tempfile
import unittest
from pathlib import Path

from scripts.common import load_json
from scripts.export_visual_generation_prompts import render_markdown
from scripts.export_visual_family_prompts import render_family_markdown
from scripts.validate_visual_references import (
    validate_family_plan,
    validate_pack,
    validate_plan,
)


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets" / "visual-reference-packs" / "blue-academic" / "pack.json"
GENERATION_DIR = (
    ROOT / "assets" / "visual-reference-packs" / "blue-academic" / "generation"
)
PLAN = GENERATION_DIR / "generation-plan.json"
PROMPTS = GENERATION_DIR / "GENERATION_PROMPTS.md"
FAMILY_PLAN = GENERATION_DIR / "family-expansion-plan.json"
FAMILY_PROMPTS = GENERATION_DIR / "FAMILY_EXPANSION_PROMPTS.md"


class VisualReferenceTests(unittest.TestCase):
    def test_bundled_pack_is_valid_and_complete(self) -> None:
        report = validate_pack(PACK)
        self.assertEqual("passed", report["status"])
        self.assertEqual(31, report["details"]["reference_count"])

    def test_ab_generation_plan_has_three_complete_pairs(self) -> None:
        report = validate_plan(PLAN)
        self.assertEqual("passed", report["status"])
        self.assertEqual(6, report["details"]["task_count"])
        self.assertEqual(3, report["details"]["pair_count"])

    def test_prompt_markdown_is_derived_from_json(self) -> None:
        expected = render_markdown(load_json(PLAN))
        self.assertEqual(expected, PROMPTS.read_text(encoding="utf-8"))

    def test_family_expansion_has_nine_roles_and_at_least_twenty_seven_variants(
        self,
    ) -> None:
        report = validate_family_plan(FAMILY_PLAN)
        self.assertEqual("passed", report["status"])
        self.assertEqual(9, report["details"]["role_count"])
        self.assertGreaterEqual(report["details"]["variant_count"], 27)

    def test_family_prompt_markdown_is_derived_from_json(self) -> None:
        expected = render_family_markdown(load_json(FAMILY_PLAN))
        self.assertEqual(expected, FAMILY_PROMPTS.read_text(encoding="utf-8"))

    def test_active_pack_cannot_be_empty(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "pack.json"
            value = load_json(PACK)
            value["status"] = "active"
            value["references"] = []
            target.write_text(
                json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            report = validate_pack(target)
        codes = {issue["code"] for issue in report["issues"]}
        self.assertIn("visual_pack.active_empty", codes)

    def test_pack_enforces_aesthetic_anchor_authority(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "pack.json"
            value = load_json(PACK)
            value["runtime_policy"]["reference_authority"] = "template-stencil"
            target.write_text(
                json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            report = validate_pack(target)
        codes = {issue["code"] for issue in report["issues"]}
        self.assertIn("schema.const", codes)

    def test_draft_pack_accepts_valid_image_and_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            pack_dir = Path(directory)
            image_dir = pack_dir / "images"
            metadata_dir = pack_dir / "metadata"
            image_dir.mkdir()
            metadata_dir.mkdir()
            image_path = image_dir / "dominant-result-01.png"
            image_path.write_bytes(
                b"\x89PNG\r\n\x1a\n"
                + struct.pack(">I", 13)
                + b"IHDR"
                + struct.pack(">II", 1600, 900)
            )
            metadata = {
                "$schema": "visual-reference-item.schema.json",
                "schema_version": "1.0.0",
                "id": "dominant-result-01",
                "file": "../images/dominant-result-01.png",
                "role": "dominant-result",
                "asset_geometry": "wide",
                "density": "medium",
                "title_mode": "takeaway",
                "example_content": True,
                "editable_rebuild": True,
                "learn": ["主图优先"],
                "do_not_copy": ["示例数据"],
            }
            (metadata_dir / "dominant-result-01.json").write_text(
                json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            pack = load_json(PACK)
            pack["status"] = "draft"
            pack["references"] = [
                {
                    "id": "dominant-result-01",
                    "file": "images/dominant-result-01.png",
                    "metadata_file": "metadata/dominant-result-01.json",
                }
            ]
            target = pack_dir / "pack.json"
            target.write_text(
                json.dumps(pack, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            report = validate_pack(target)
        self.assertEqual("passed", report["status"])

    def test_active_pack_requires_every_core_role(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            pack_dir = Path(directory)
            image_dir = pack_dir / "images"
            metadata_dir = pack_dir / "metadata"
            image_dir.mkdir()
            metadata_dir.mkdir()
            image_path = image_dir / "dominant-result-01.png"
            image_path.write_bytes(
                b"\x89PNG\r\n\x1a\n"
                + struct.pack(">I", 13)
                + b"IHDR"
                + struct.pack(">II", 1600, 900)
            )
            metadata = {
                "$schema": "visual-reference-item.schema.json",
                "schema_version": "1.0.0",
                "id": "dominant-result-01",
                "file": "../images/dominant-result-01.png",
                "role": "dominant-result",
                "asset_geometry": "wide",
                "density": "medium",
                "title_mode": "takeaway",
                "example_content": True,
                "editable_rebuild": True,
                "learn": ["主图优先"],
                "do_not_copy": ["示例数据"],
            }
            (metadata_dir / "dominant-result-01.json").write_text(
                json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            pack = load_json(PACK)
            pack["status"] = "active"
            pack["references"] = [
                {
                    "id": "dominant-result-01",
                    "file": "images/dominant-result-01.png",
                    "metadata_file": "metadata/dominant-result-01.json",
                }
            ]
            target = pack_dir / "pack.json"
            target.write_text(
                json.dumps(pack, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            report = validate_pack(target)
        codes = {issue["code"] for issue in report["issues"]}
        self.assertIn("visual_pack.active_incomplete", codes)


if __name__ == "__main__":
    unittest.main()
