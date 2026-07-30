from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.common import load_json


def render_qa_note(report: dict[str, Any]) -> str:
    summary = report.get("summary", {})
    lines = [
        "# PPTX QA 说明",
        "",
        f"- 状态：`{report.get('status', 'unknown')}`",
        f"- 错误：{summary.get('error', 0)}",
        f"- 警告：{summary.get('warning', 0)}",
        f"- 信息：{summary.get('info', 0)}",
        "",
    ]
    details = report.get("details", {})
    if isinstance(details, dict):
        lines.extend(
            [
                "## 产物概况",
                "",
                f"- PPTX：`{details.get('pptx', '')}`",
                f"- 页数：{details.get('slide_count', '')}",
                f"- 画布：`{details.get('canvas_inches', '')}`",
                f"- 媒体数量：{details.get('media_count', '')}",
                "",
            ]
        )

    issues = report.get("issues", [])
    if issues:
        lines.extend(
            [
                "## 检查结果",
                "",
                "| 严重度 | 代码 | 位置 | 说明 |",
                "|---|---|---|---|",
            ]
        )
        for issue in issues:
            values = [
                issue.get("severity", ""),
                issue.get("code", ""),
                issue.get("path", ""),
                issue.get("message", ""),
            ]
            escaped = [str(value).replace("|", "\\|").replace("\n", "<br>") for value in values]
            lines.append("| " + " | ".join(escaped) + " |")
    else:
        lines.extend(["## 检查结果", "", "未发现静态 QA 问题。"])
    lines.extend(
        [
            "",
            "> 本说明由 qa-report.json 生成。静态重叠和分辨率提示应结合预览复核。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a readable QA note from QA JSON.")
    parser.add_argument("report", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    report = load_json(args.report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_qa_note(report), encoding="utf-8", newline="\n")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
