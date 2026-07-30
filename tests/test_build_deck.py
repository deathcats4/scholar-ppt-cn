from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image
from pptx import Presentation

from scripts.build_deck import build_from_project
from scripts.common import load_json, write_json
from scripts.init_project import new_project
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
    ]
    project["artifacts"]["pptx"] = "outputs/runtime-demo/deck.pptx"
    asset_dir = base / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (1200, 700), "#E8EEF8").save(asset_dir / "a.png")
    Image.new("RGB", (900, 900), "#D7E4F7").save(asset_dir / "b.png")
    return project


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
            self.assertEqual(7, len(Presentation(output).slides))

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
            self.assertEqual(7, qa["details"]["slide_count"])

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


if __name__ == "__main__":
    unittest.main()
