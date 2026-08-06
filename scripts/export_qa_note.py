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
        "# PPTX QA Note",
        "",
        f"- Status: `{report.get('status', 'unknown')}`",
        f"- Errors: {summary.get('error', 0)}",
        f"- Warnings: {summary.get('warning', 0)}",
        f"- Info: {summary.get('info', 0)}",
        "",
    ]
    details = report.get("details", {})
    if isinstance(details, dict):
        lines.extend(
            [
                "## Artifact Summary",
                "",
                f"- PPTX: `{details.get('pptx', '')}`",
                f"- Slide count: {details.get('slide_count', '')}",
                f"- Canvas: `{details.get('canvas_inches', '')}`",
                f"- Media count: {details.get('media_count', '')}",
                "",
            ]
        )

    issues = report.get("issues", [])
    if issues:
        lines.extend(
            [
                "## Issues",
                "",
                "| Severity | Code | Location | Message |",
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
        lines.extend(["## Issues", "", "No static QA issues found."])
    lines.extend(
        [
            "",
            "> Generated from qa-report.json. Static overlap and resolution warnings must be reviewed with rendered previews.",
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
