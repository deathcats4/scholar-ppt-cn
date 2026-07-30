from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.common import write_json
from scripts.validate_project import validate_project


WORKFLOW_STEPS = (
    "intake",
    "project-state",
    "evidence-index",
    "template-dna",
    "planning",
    "family-blueprint",
    "visual-samples",
    "editable-pptx",
    "static-qa",
    "render-preview",
    "visual-qa",
)


def new_project(
    slug: str,
    title: str,
    output_dir: str,
    task_type: str = "create",
    width: float = 13.3333,
    height: float = 7.5,
) -> dict:
    steps = {
        name: {
            "status": "planned",
            "reason": "Evaluate this step from the request and available capabilities.",
        }
        for name in WORKFLOW_STEPS
    }
    steps["intake"] = {
        "status": "in-progress",
        "reason": "Register user request and source files.",
    }
    steps["project-state"] = {
        "status": "completed",
        "reason": "Initial project.json created.",
    }
    pptx_path: str | None = f"{output_dir}/deck.pptx"
    preview_dir: str | None = f"{output_dir}/previews"
    montage_path: str | None = f"{output_dir}/previews/montage.png"
    qa_report_path: str | None = f"{output_dir}/qa-report.json"
    qa_note_path: str | None = f"{output_dir}/qa-note.md"
    if task_type == "planning-only":
        for name in (
            "visual-samples",
            "editable-pptx",
            "static-qa",
            "render-preview",
            "visual-qa",
        ):
            steps[name] = {
                "status": "not-applicable",
                "reason": "Planning-only request does not produce visual or PPTX artifacts.",
            }
        pptx_path = preview_dir = montage_path = qa_report_path = qa_note_path = None
    elif task_type == "samples-only":
        for name in ("editable-pptx", "static-qa", "render-preview"):
            steps[name] = {
                "status": "not-applicable",
                "reason": "Samples-only request does not produce an editable PPTX.",
            }
        steps["visual-samples"] = {
            "status": "planned",
            "reason": "Visual samples are the requested artifact.",
        }
        pptx_path = qa_report_path = qa_note_path = None
    return {
        "$schema": "urn:scholar-ppt-cn:project:1.0.0",
        "schema_version": "1.0.0",
        "project": {
            "id": slug,
            "slug": slug,
            "title": title,
            "language": "zh-CN",
            "task_type": task_type,
            "output_dir": output_dir,
            "source_files": [],
        },
        "canvas": {
            "source": "default",
            "width_inches": width,
            "height_inches": height,
        },
        "template": {
            "source": "neutral-tokens",
            "id": "neutral-pending",
            "path": None,
            "adherence": "guided",
            "dna": {
                "status": "pending",
                "colors": [],
                "font_roles": {
                    "title": {
                        "families": [
                            "Microsoft YaHei",
                            "PingFang SC",
                            "Source Han Sans SC",
                            "Noto Sans CJK SC",
                        ],
                        "weight": 700,
                    },
                    "body": {
                        "families": [
                            "Microsoft YaHei",
                            "PingFang SC",
                            "Source Han Sans SC",
                            "Noto Sans CJK SC",
                        ],
                        "weight": 400,
                    },
                },
                "notes": [],
            },
        },
        "capabilities": {},
        "workflow": {"steps": steps},
        "assets": [],
        "slides": [],
        "visual_system": {
            "families": [],
            "variants": [],
            "sample_slide_ids": [],
        },
        "artifacts": {
            "planning_markdown": f"{output_dir}/planning.md",
            "pptx": pptx_path,
            "preview_dir": preview_dir,
            "montage": montage_path,
            "qa_report": qa_report_path,
            "qa_note": qa_note_path,
        },
        "qa": {
            "status": "not-run",
            "issues": [],
            "skipped_checks": [],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a scholar-ppt-cn project.json.")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--task-type",
        choices=(
            "create",
            "rebuild",
            "restyle",
            "revise",
            "planning-only",
            "samples-only",
        ),
        default="create",
    )
    parser.add_argument("--width", type=float, default=13.3333)
    parser.add_argument("--height", type=float, default=7.5)
    args = parser.parse_args()
    project = new_project(
        args.slug,
        args.title,
        str(args.output.parent).replace("\\", "/"),
        args.task_type,
        args.width,
        args.height,
    )
    issues = [issue for issue in validate_project(project) if issue.severity == "error"]
    if issues:
        for issue in issues:
            print(f"ERROR {issue.code} {issue.path}: {issue.message}", file=sys.stderr)
        return 1
    write_json(args.output, project)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
