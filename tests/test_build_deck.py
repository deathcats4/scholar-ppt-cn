from __future__ import annotations

import tempfile
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

try:
    from PIL import Image
    from pptx import Presentation

    RUNTIME_DEPENDENCIES = True
except ImportError:
    Image = Presentation = None
    RUNTIME_DEPENDENCIES = False

from scripts.build_deck import build_from_project
from scripts.common import load_json, write_json
from scripts.init_project import new_project
from scripts.pptx_runtime import _items_for_assets, infer_render_type
from scripts.qa_pptx import inspect_pptx
from scripts.validate_project import validate_project


def _slide(
    number: int,
    title: str,
    *,
    asset_ids: list[str] | None = None,
    render: dict | None = None,
) -> dict:
    return {
        "id": f"slide-{number}",
        "number": number,
        "title": title,
        "narrative_section": "测试",
        "communication_task": "验证稳定构建",
        "core_message": f"{title}的核心信息",
        "source_asset_ids": asset_ids or [],
        "layout": {
            "archetype_id": None,
            "family_id": None,
            "variant_id": None,
            "decision_reason": "Runtime regression fixture.",
        },
        "density": "medium",
        "asset_handling": "preserve" if asset_ids else "not-applicable",
        "risks": [],
        **({"render": render} if render else {}),
    }


def _project(base: Path) -> dict:
    project = new_project(
        "runtime-demo",
        "运行层回归测试",
        "outputs/runtime-demo",
    )
    for step in ("intake", "evidence-index", "template-dna", "planning"):
        project["workflow"]["steps"][step] = {
            "status": "completed",
            "reason": "Runtime fixture prepared.",
        }
    project["template"]["dna"]["status"] = "selected"
    project["template"]["dna"]["colors"] = ["#123B86", "#4C6FAE"]
    project["assets"] = [
        {
            "id": "asset-a",
            "type": "figure",
            "path": "assets/a.png",
            "source_ref": {},
            "geometry": "wide",
            "summary": "测试图 A",
            "used_on_slides": ["slide-3", "slide-4", "slide-5"],
        },
        {
            "id": "asset-b",
            "type": "figure",
            "path": "assets/b.png",
            "source_ref": {},
            "geometry": "wide",
            "summary": "测试图 B",
            "used_on_slides": ["slide-4", "slide-5"],
        },
    ]
    project["slides"] = [
        _slide(
            1,
            "运行层回归测试",
            render={
                "type": "cover",
                "subtitle": "固定构建器生成可编辑 PPTX",
                "items": [
                    {"title": "汇报人", "body": "测试", "asset_id": None},
                    {"title": "日期", "body": "2026 年 7 月", "asset_id": None},
                ],
            },
        ),
        _slide(
            2,
            "规划与内容先于页面几何",
            render={
                "type": "bullets",
                "items": [
                    {
                        "title": "规划保持权威",
                        "body": "运行层只处理可编辑对象和稳定坐标。",
                        "asset_id": None,
                    },
                    {
                        "title": "允许语义布局",
                        "body": "Agent 不需要重写底层 PPTX 代码。",
                        "asset_id": None,
                    },
                ],
            },
        ),
        _slide(
            3,
            "单图页保持证据主导",
            asset_ids=["asset-a"],
            render={
                "type": "figure",
                "asset_ids": ["asset-a"],
                "body": ["证据图保持完整，不自动裁剪坐标轴。"],
            },
        ),
        _slide(
            4,
            "双图页面支持直接比较",
            asset_ids=["asset-a", "asset-b"],
            render={
                "type": "comparison",
                "asset_ids": ["asset-a", "asset-b"],
                "items": [
                    {"title": "条件 A", "body": "基准结果", "asset_id": "asset-a"},
                    {"title": "条件 B", "body": "对照结果", "asset_id": "asset-b"},
                ],
            },
        ),
        _slide(
            5,
            "多面板页复用统一图像适配",
            asset_ids=["asset-a", "asset-b"],
            render={
                "type": "multi-panel",
                "asset_ids": ["asset-a", "asset-b"],
            },
        ),
        _slide(
            6,
            "固定运行层缩短生成链路",
            render={
                "type": "process",
                "items": [
                    {"title": "规划", "body": "确定汇报重点", "asset_id": None},
                    {"title": "描述", "body": "写入 render 字段", "asset_id": None},
                    {"title": "构建", "body": "生成 PPTX", "asset_id": None},
                    {"title": "检查", "body": "执行静态 QA", "asset_id": None},
                ],
            },
        ),
        _slide(
            7,
            "稳定底座让 Agent 专注学术表达",
            render={
                "type": "conclusion",
                "items": [
                    {"title": "减少临时代码", "body": "", "asset_id": None},
                    {"title": "支持中断恢复", "body": "", "asset_id": None},
                    {"title": "保留可编辑性", "body": "", "asset_id": None},
                ],
            },
        ),
        _slide(
            8,
            "章节页面形成叙事停顿",
            render={
                "type": "section",
                "subtitle": "运行层应稳定覆盖章节页。",
            },
        ),
        _slide(
            9,
            "陈述页面保持清晰层级",
            render={
                "type": "statement",
                "body": ["这是用于验证陈述页面的简短信息。"],
            },
        ),
    ]
    project["artifacts"]["pptx"] = "outputs/runtime-demo/deck.pptx"
    asset_dir = base / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (1200, 700), "#E8EEF8").save(asset_dir / "a.png")
    Image.new("RGB", (900, 900), "#D7E4F7").save(asset_dir / "b.png")
    return project


class BuildDeckDependencyTests(unittest.TestCase):
    def test_cli_malformed_nested_objects_returns_and_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project_path = base / "project.json"
            report_path = base / "build-report.json"
            project = new_project(
                "malformed-project",
                "畸形项目测试",
                "outputs/malformed-project",
            )
            project["artifacts"] = []
            project["project"] = []
            project["template"] = []
            write_json(project_path, project)
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_deck.py",
                    str(project_path),
                    "--base-dir",
                    str(base),
                    "--report",
                    str(report_path),
                ],
                cwd=Path(__file__).resolve().parent.parent,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(1, result.returncode, result.stdout)
            self.assertNotIn("Traceback", result.stderr)
            self.assertTrue(report_path.is_file())
            report = load_json(report_path)
        self.assertEqual("failed", report["status"])
        self.assertTrue(
            {"schema.type", "type.object"}
            & {issue["code"] for issue in report["issues"]}
        )

    def test_cli_unreadable_json_still_writes_requested_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project_path = base / "project.json"
            report_path = base / "build-report.json"
            project_path.write_text("{not-valid-json", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_deck.py",
                    str(project_path),
                    "--base-dir",
                    str(base),
                    "--report",
                    str(report_path),
                ],
                cwd=Path(__file__).resolve().parent.parent,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(1, result.returncode, result.stdout)
            self.assertNotIn("Traceback", result.stderr)
            self.assertTrue(report_path.is_file())
            report = load_json(report_path)
        self.assertIn(
            "input.read",
            {issue["code"] for issue in report["issues"]},
        )

    def test_missing_runtime_dependencies_return_structured_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project_path = base / "project.json"
            project = new_project("missing-deps", "缺失依赖测试", "outputs/missing")
            project["template"]["dna"]["status"] = "selected"
            project["slides"] = [
                _slide(1, "缺失依赖仍返回 JSON", render={"type": "cover"})
            ]
            write_json(project_path, project)
            with patch("scripts.pptx_runtime.PPTX_AVAILABLE", False):
                report = build_from_project(project_path, base_dir=base)
        self.assertEqual("failed", report["status"])
        self.assertIn(
            "dependency.python_pptx",
            {issue["code"] for issue in report["issues"]},
        )

    def test_asset_items_are_matched_by_asset_id_not_position(self) -> None:
        slide = {
            "core_message": "fallback",
            "render": {
                "type": "comparison",
                "asset_ids": ["asset-b", "asset-a"],
                "items": [
                    {"title": "A", "body": "first", "asset_id": "asset-a"},
                    {"title": "B", "body": "second", "asset_id": "asset-b"},
                ],
            },
        }
        resolved = _items_for_assets(slide, ["asset-b", "asset-a"])
        self.assertEqual(["B", "A"], [item["title"] for item in resolved])

    def test_comparison_body_is_used_without_item_metadata(self) -> None:
        slide = {
            "core_message": "fallback",
            "render": {
                "type": "comparison",
                "body": ["左侧说明", "右侧说明"],
                "asset_ids": ["asset-a", "asset-b"],
            },
        }
        resolved = _items_for_assets(slide, ["asset-a", "asset-b"])
        self.assertEqual(["左侧说明", "右侧说明"], [item["body"] for item in resolved])

    def test_auto_inference_keeps_evidence_before_conclusion_keyword(self) -> None:
        slide = _slide(
            3,
            "结果总结仍需展示证据",
            asset_ids=["asset-a"],
            render={"type": "auto"},
        )
        self.assertEqual("figure", infer_render_type(slide))


@unittest.skipUnless(
    RUNTIME_DEPENDENCIES,
    "python-pptx and Pillow are optional runtime dependencies",
)
class BuildDeckTests(unittest.TestCase):
    def test_runtime_builds_editable_pptx_and_updates_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project_path = base / "outputs" / "runtime-demo" / "project.json"
            project = _project(base)
            write_json(project_path, project)

            report = build_from_project(
                project_path,
                base_dir=base,
                update_project=True,
            )
            self.assertEqual(0, report["summary"]["error"], report)
            output = Path(report["details"]["output"])
            self.assertTrue(output.is_file())
            self.assertEqual(9, len(Presentation(output).slides))

            updated = load_json(project_path)
            self.assertEqual(
                "completed",
                updated["workflow"]["steps"]["editable-pptx"]["status"],
            )
            self.assertEqual(
                [],
                [
                    issue
                    for issue in validate_project(updated)
                    if issue.severity == "error"
                ],
            )
            qa = inspect_pptx(output, updated)
            self.assertEqual(0, qa["summary"]["error"], qa)
            self.assertEqual(9, qa["details"]["slide_count"])

    def test_runtime_preserves_previous_pptx_before_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project_path = base / "project.json"
            project = _project(base)
            write_json(project_path, project)
            output = base / "deck.pptx"
            first = build_from_project(
                project_path,
                base_dir=base,
                output=output,
            )
            self.assertEqual(0, first["summary"]["error"], first)
            second = build_from_project(
                project_path,
                base_dir=base,
                output=output,
            )
            self.assertEqual(0, second["summary"]["error"], second)
            backup = Path(second["details"]["backup"])
            self.assertTrue(backup.is_file())
            self.assertEqual(".pptx", backup.suffix)

    def test_runtime_refuses_to_overwrite_declared_input(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project_path = base / "project.json"
            project = _project(base)
            project["project"]["source_files"] = ["sources/input.pptx"]
            write_json(project_path, project)
            report = build_from_project(
                project_path,
                base_dir=base,
                output=base / "sources" / "input.pptx",
            )
            codes = {
                issue["code"]
                for issue in report["issues"]
                if issue["severity"] == "error"
            }
            self.assertIn("output.input_conflict", codes)
            self.assertFalse((base / "sources" / "input.pptx").exists())

    def test_runtime_requires_pptx_extension(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project_path = base / "project.json"
            write_json(project_path, _project(base))
            report = build_from_project(
                project_path,
                base_dir=base,
                output=base / "deck.bin",
            )
            codes = {
                issue["code"]
                for issue in report["issues"]
                if issue["severity"] == "error"
            }
            self.assertIn("output.extension", codes)
            self.assertFalse((base / "deck.bin").exists())

    def test_report_cannot_overwrite_project_or_pptx(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project_path = base / "project.json"
            write_json(project_path, _project(base))
            project_conflict = build_from_project(
                project_path,
                base_dir=base,
                report_path=project_path,
            )
            self.assertIn(
                "report.input_conflict",
                {issue["code"] for issue in project_conflict["issues"]},
            )
            same_output = base / "deck.pptx"
            output_conflict = build_from_project(
                project_path,
                base_dir=base,
                output=same_output,
                report_path=same_output,
            )
            self.assertIn(
                "output.path_conflict",
                {issue["code"] for issue in output_conflict["issues"]},
            )

    def test_cli_report_conflict_does_not_modify_project_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project_path = base / "project.json"
            write_json(project_path, _project(base))
            before = project_path.read_bytes()
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_deck.py",
                    str(project_path),
                    "--base-dir",
                    str(base),
                    "--report",
                    str(project_path),
                ],
                cwd=Path(__file__).resolve().parent.parent,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(1, result.returncode, result.stdout)
            self.assertEqual(before, project_path.read_bytes())
            report = json.loads(result.stdout)
            self.assertIn(
                "report.input_conflict",
                {issue["code"] for issue in report["issues"]},
            )

    def test_unexpected_runtime_failure_is_structured(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project_path = base / "project.json"
            write_json(project_path, _project(base))
            with patch(
                "scripts.build_deck.build_presentation",
                side_effect=RuntimeError("synthetic failure"),
            ):
                report = build_from_project(
                    project_path,
                    base_dir=base,
                    debug=True,
                )
            self.assertIn(
                "build.runtime",
                {issue["code"] for issue in report["issues"]},
            )
            self.assertIn("RuntimeError", report["details"]["debug_traceback"])

    def test_corrupt_image_returns_structured_asset_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project_path = base / "project.json"
            project = _project(base)
            (base / "assets" / "a.png").write_bytes(b"not-a-real-png")
            write_json(project_path, project)
            report = build_from_project(project_path, base_dir=base)
            self.assertIn(
                "build.asset_decode",
                {issue["code"] for issue in report["issues"]},
            )
            self.assertFalse((base / "outputs/runtime-demo/deck.pptx").exists())

    def test_declared_but_unrendered_evidence_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project_path = base / "project.json"
            project = _project(base)
            project["slides"][5]["source_asset_ids"] = ["asset-a"]
            project["slides"][5]["asset_handling"] = "preserve"
            project["assets"][0]["used_on_slides"].append("slide-6")
            write_json(project_path, project)
            report = build_from_project(project_path, base_dir=base)
            unused = [
                issue
                for issue in report["issues"]
                if issue["code"] == "build.asset_unused"
            ]
            self.assertEqual(1, len(unused), report)
            self.assertIn("slide-6:asset-a", unused[0]["path"])

    def test_explicitly_ignored_evidence_does_not_warn(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project_path = base / "project.json"
            project = _project(base)
            project["slides"][5]["source_asset_ids"] = ["asset-a"]
            project["slides"][5]["asset_handling"] = "preserve"
            project["slides"][5]["render"]["ignored_asset_ids"] = ["asset-a"]
            project["slides"][5]["render"]["ignore_reason"] = (
                "The process page summarizes the evidence shown on the prior slide."
            )
            project["assets"][0]["used_on_slides"].append("slide-6")
            write_json(project_path, project)
            report = build_from_project(project_path, base_dir=base)
            self.assertNotIn(
                "build.asset_unused",
                {issue["code"] for issue in report["issues"]},
            )


if __name__ == "__main__":
    unittest.main()
