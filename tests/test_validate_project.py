from __future__ import annotations

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
