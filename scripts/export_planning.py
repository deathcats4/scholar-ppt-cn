from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.common import load_json
from scripts.validate_project import validate_project


def _cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        value = "；".join(str(item) for item in value)
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def render_markdown(data: dict[str, Any]) -> str:
    project = data["project"]
    canvas = data["canvas"]
    template = data["template"]
    lines = [
        f"# {project['title']}｜生产规划",
        "",
        f"- 项目 ID：`{project['id']}`",
        f"- 任务：`{project['task_type']}`",
        f"- 画布：{canvas['width_inches']} × {canvas['height_inches']} 英寸（{canvas['source']}）",
        f"- 模板：{template['source']} / {_cell(template.get('id')) or '未指定'}",
        "",
        "## 工作流",
        "",
        "| 步骤 | 状态 | 理由 |",
        "|---|---|---|",
    ]
    for name, step in data["workflow"]["steps"].items():
        lines.append(
            f"| {_cell(name)} | {_cell(step['status'])} | {_cell(step['reason'])} |"
        )

    assets = {item["id"]: item for item in data["assets"]}
    lines.extend(
        [
            "",
            "## 页面规划",
            "",
            "| 页码 | 标题 | 叙事位置 | 页面任务 | 核心信息 | 素材 | 版式 | 密度 | 素材处理 | 风险 |",
            "|---:|---|---|---|---|---|---|---|---|---|",
        ]
    )
    for slide in sorted(data["slides"], key=lambda item: item["number"]):
        asset_labels = []
        for asset_id in slide["source_asset_ids"]:
            asset = assets.get(asset_id)
            asset_labels.append(
                f"{asset_id} ({asset['geometry']})" if asset else asset_id
            )
        layout = slide["layout"]
        layout_id = (
            layout.get("variant_id")
            or layout.get("archetype_id")
            or layout.get("family_id")
            or ""
        )
        lines.append(
            "| {number} | {title} | {section} | {task} | {message} | {assets} | "
            "{layout} | {density} | {handling} | {risks} |".format(
                number=slide["number"],
                title=_cell(slide["title"]),
                section=_cell(slide["narrative_section"]),
                task=_cell(slide["communication_task"]),
                message=_cell(slide["core_message"]),
                assets=_cell(asset_labels),
                layout=_cell(layout_id),
                density=_cell(slide["density"]),
                handling=_cell(slide["asset_handling"]),
                risks=_cell(slide["risks"]),
            )
        )
    lines.append("")
    lines.append("> 本文件由 project.json 生成；请修改 JSON 后重新导出。")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export planning Markdown from project JSON.")
    parser.add_argument("project", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    data = load_json(args.project)
    errors = [issue for issue in validate_project(data) if issue.severity == "error"]
    if errors:
        for issue in errors:
            print(f"ERROR {issue.code} {issue.path}: {issue.message}", file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_markdown(data), encoding="utf-8", newline="\n")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
