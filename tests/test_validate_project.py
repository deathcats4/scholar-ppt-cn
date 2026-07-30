from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.common import load_json
from scripts.export_planning import render_markdown
from scripts.export_qa_note import render_qa_note
from scripts.init_project import new_project
from scripts.validate_project import validate_project


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


class ProjectValidationTests(unittest.TestCase):
    def test_valid_fixture_has_no_errors(self) -> None:
        issues = validate_project(load_json(FIXTURES / "project-valid.json"))
        self.assertEqual([], [issue for issue in issues if issue.severity == "error"])

    def test_invalid_fixture_exposes_cross_reference_errors(self) -> None:
        issues = validate_project(load_json(FIXTURES / "project-invalid.json"))
        codes = {issue.code for issue in issues if issue.severity == "error"}
        self.assertIn("project.slug", codes)
        self.assertIn("canvas.dimension", codes)
        self.assertIn("workflow.step.reason", codes)
        self.assertIn("reference.asset", codes)
        self.assertIn("id.duplicate", codes)

    def test_schema_rejects_unknown_nested_fields(self) -> None:
        data = load_json(FIXTURES / "project-valid.json")
        data["canvas"]["unexpected"] = True
        issues = validate_project(data)
        codes = {issue.code for issue in issues if issue.severity == "error"}
        self.assertIn("schema.additional_property", codes)

    def test_wrong_nested_types_return_issues_instead_of_crashing(self) -> None:
        base = load_json(FIXTURES / "project-valid.json")
        mutations = {
            "null asset slide list": lambda data: data["assets"][0].__setitem__(
                "used_on_slides", None
            ),
            "array capability availability": lambda data: data["capabilities"][
                "filesystem"
            ].__setitem__("available", []),
            "array workflow status": lambda data: data["workflow"]["steps"][
                "planning"
            ].__setitem__("status", []),
            "array template source": lambda data: data["template"].__setitem__(
                "source", []
            ),
            "object slide asset id": lambda data: data["slides"][1].__setitem__(
                "source_asset_ids", [{}]
            ),
            "array layout family id": lambda data: data["slides"][1]["layout"].__setitem__(
                "family_id", []
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                data = copy.deepcopy(base)
                mutate(data)
                issues = validate_project(data)
                self.assertTrue(
                    any(issue.severity == "error" for issue in issues),
                    issues,
                )

    def test_cli_returns_json_report_for_wrong_nested_type(self) -> None:
        data = load_json(FIXTURES / "project-valid.json")
        data["assets"][0]["used_on_slides"] = None
        with tempfile.TemporaryDirectory() as directory:
            project_path = Path(directory) / "project.json"
            project_path.write_text(
                json.dumps(data, ensure_ascii=False),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate_project.py"),
                    str(project_path),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
        self.assertEqual(1, result.returncode)
        report = json.loads(result.stdout)
        self.assertEqual("failed", report["status"])
        self.assertNotIn("Traceback", result.stderr)

    def test_family_variant_and_slide_mappings_are_consistent(self) -> None:
        data = load_json(FIXTURES / "project-valid.json")
        data["visual_system"]["families"] = [
            {"id": "family-a", "name": "A", "slide_ids": ["slide-2"]},
            {"id": "family-b", "name": "B", "slide_ids": []},
        ]
        data["visual_system"]["variants"] = [
            {
                "id": "variant-b",
                "family_id": "family-b",
                "name": "B",
                "slide_ids": ["slide-2"],
            }
        ]
        data["slides"][1]["layout"]["family_id"] = "family-a"
        data["slides"][1]["layout"]["variant_id"] = "variant-b"
        codes = {
            issue.code
            for issue in validate_project(data)
            if issue.severity == "error"
        }
        self.assertIn("reference.variant_family", codes)
        self.assertIn("reference.variant_family_membership", codes)

    def test_family_and_variant_slide_ids_must_reference_real_slides(self) -> None:
        data = load_json(FIXTURES / "project-valid.json")
        data["visual_system"]["families"] = [
            {"id": "family-a", "name": "A", "slide_ids": ["slide-999"]}
        ]
        data["visual_system"]["variants"] = [
            {
                "id": "variant-a",
                "family_id": "family-a",
                "name": "A",
                "slide_ids": ["slide-998"],
            }
        ]
        issues = validate_project(data)
        unknown_slide_errors = [
            issue
            for issue in issues
            if issue.severity == "error" and issue.code == "reference.slide"
        ]
        self.assertGreaterEqual(len(unknown_slide_errors), 2, issues)

    def test_asset_slide_references_are_bidirectional(self) -> None:
        slide_only = load_json(FIXTURES / "project-valid.json")
        slide_only["assets"][0]["used_on_slides"] = []
        slide_codes = {
            issue.code
            for issue in validate_project(slide_only)
            if issue.severity == "error"
        }
        self.assertIn("reference.asset_reverse", slide_codes)

        asset_only = load_json(FIXTURES / "project-valid.json")
        asset_only["slides"][1]["source_asset_ids"] = []
        asset_codes = {
            issue.code
            for issue in validate_project(asset_only)
            if issue.severity == "error"
        }
        self.assertIn("reference.slide_reverse", asset_codes)

    def test_render_assets_must_belong_to_the_slide_evidence_set(self) -> None:
        data = load_json(FIXTURES / "project-valid.json")
        data["assets"].append(
            {
                "id": "asset-extra",
                "type": "figure",
                "path": "sources/extra.png",
                "source_ref": {},
                "geometry": "wide",
                "summary": "Extra figure",
                "used_on_slides": [],
            }
        )
        data["slides"][1]["render"] = {
            "type": "figure",
            "asset_ids": ["asset-extra"],
        }
        codes = {
            issue.code
            for issue in validate_project(data)
            if issue.severity == "error"
        }
        self.assertIn("reference.render_asset", codes)

    def test_comparison_render_requires_two_explicit_assets(self) -> None:
        data = load_json(FIXTURES / "project-valid.json")
        data["slides"][1]["render"] = {
            "type": "comparison",
            "asset_ids": ["asset-fig-1"],
        }
        codes = {
            issue.code
            for issue in validate_project(data)
            if issue.severity == "error"
        }
        self.assertIn("slide.render_asset_count", codes)

    def test_render_asset_count_uses_source_assets_when_override_is_absent(self) -> None:
        data = load_json(FIXTURES / "project-valid.json")
        data["slides"][1]["render"] = {"type": "comparison"}
        codes = {
            issue.code
            for issue in validate_project(data)
            if issue.severity == "error"
        }
        self.assertIn("slide.render_asset_count", codes)

    def test_figure_render_rejects_multiple_effective_assets(self) -> None:
        data = load_json(FIXTURES / "project-valid.json")
        data["assets"].append(
            {
                "id": "asset-extra",
                "type": "figure",
                "path": "sources/extra.png",
                "source_ref": {},
                "geometry": "wide",
                "summary": "Extra figure",
                "used_on_slides": ["slide-2"],
            }
        )
        data["slides"][1]["source_asset_ids"].append("asset-extra")
        data["slides"][1]["render"] = {"type": "figure"}
        codes = {
            issue.code
            for issue in validate_project(data)
            if issue.severity == "error"
        }
        self.assertIn("slide.render_asset_count", codes)

    def test_ignored_assets_require_reason_and_cannot_be_selected(self) -> None:
        data = load_json(FIXTURES / "project-valid.json")
        data["slides"][1]["render"] = {
            "type": "figure",
            "asset_ids": ["asset-fig-1"],
            "ignored_asset_ids": ["asset-fig-1"],
        }
        codes = {
            issue.code
            for issue in validate_project(data)
            if issue.severity == "error"
        }
        self.assertIn("reference.ignored_asset", codes)
        self.assertIn("slide.ignore_reason", codes)

    def test_multi_panel_rejects_more_than_four_effective_assets(self) -> None:
        data = load_json(FIXTURES / "project-valid.json")
        for number in range(2, 6):
            asset_id = f"asset-{number}"
            data["assets"].append(
                {
                    "id": asset_id,
                    "type": "figure",
                    "path": f"sources/{asset_id}.png",
                    "source_ref": {},
                    "geometry": "wide",
                    "summary": asset_id,
                    "used_on_slides": ["slide-2"],
                }
            )
            data["slides"][1]["source_asset_ids"].append(asset_id)
        data["slides"][1]["render"] = {"type": "multi-panel"}
        codes = {
            issue.code
            for issue in validate_project(data)
            if issue.severity == "error"
        }
        self.assertIn("slide.render_asset_count", codes)

    def test_slide_numbers_must_be_contiguous(self) -> None:
        data = load_json(FIXTURES / "project-valid.json")
        data["slides"][1]["number"] = 3
        codes = {
            issue.code
            for issue in validate_project(data)
            if issue.severity == "error"
        }
        self.assertIn("slide.number_sequence", codes)

    def test_completed_workflow_steps_require_matching_state(self) -> None:
        data = load_json(FIXTURES / "project-valid.json")
        data["workflow"]["steps"]["editable-pptx"]["status"] = "completed"
        data["workflow"]["steps"]["static-qa"]["status"] = "completed"
        data["artifacts"]["pptx"] = None
        data["artifacts"]["qa_report"] = None
        data["qa"]["status"] = "not-run"
        codes = {
            issue.code
            for issue in validate_project(data)
            if issue.severity == "error"
        }
        self.assertIn("workflow.artifact", codes)
        self.assertIn("workflow.qa_status", codes)

    def test_markdown_is_derived_from_json(self) -> None:
        markdown = render_markdown(load_json(FIXTURES / "project-valid.json"))
        self.assertIn("# 示例学术汇报｜生产规划", markdown)
        self.assertIn("| 2 | 研究流程 |", markdown)
        self.assertIn("本文件由 project.json 生成", markdown)

    def test_project_scaffold_is_valid(self) -> None:
        project = new_project("new-project", "新项目", "outputs/new-project")
        issues = validate_project(project)
        self.assertEqual([], [issue for issue in issues if issue.severity == "error"])

    def test_planning_only_scaffold_does_not_claim_pptx_artifacts(self) -> None:
        project = new_project(
            "planning-project",
            "规划项目",
            "outputs/planning-project",
            task_type="planning-only",
        )
        self.assertIsNone(project["artifacts"]["pptx"])
        self.assertIsNone(project["artifacts"]["qa_report"])
        self.assertEqual(
            "not-applicable",
            project["workflow"]["steps"]["editable-pptx"]["status"],
        )
        issues = validate_project(project)
        self.assertEqual([], [issue for issue in issues if issue.severity == "error"])

    def test_qa_note_is_derived_from_report(self) -> None:
        note = render_qa_note(
            {
                "status": "passed-with-warnings",
                "summary": {"error": 0, "warning": 1, "info": 0},
                "issues": [
                    {
                        "severity": "warning",
                        "code": "demo.warning",
                        "message": "Review this item",
                        "path": "slide:1",
                    }
                ],
                "details": {"pptx": "deck.pptx", "slide_count": 1},
            }
        )
        self.assertIn("demo.warning", note)
        self.assertIn("本说明由 qa-report.json 生成", note)


if __name__ == "__main__":
    unittest.main()
