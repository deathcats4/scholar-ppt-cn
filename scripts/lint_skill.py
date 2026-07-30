from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.common import Issue, make_report, print_report, write_json


REFERENCE_PATTERN = re.compile(r"`(references/[A-Za-z0-9_.\-/]+)`")


def lint_skill(root: Path) -> dict:
    issues: list[Issue] = []
    skill_path = root / "SKILL.md"
    if not skill_path.exists():
        return make_report(
            "lint_skill",
            [Issue("error", "skill.missing", "SKILL.md is missing", str(skill_path))],
            root=str(root),
        )

    text = skill_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        issues.append(
            Issue(
                "error",
                "frontmatter.open",
                "SKILL.md must start with YAML frontmatter",
                "SKILL.md:1",
            )
        )
        frontmatter_lines: list[str] = []
    else:
        try:
            closing = next(
                index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
            )
            frontmatter_lines = lines[1:closing]
        except StopIteration:
            frontmatter_lines = []
            issues.append(
                Issue(
                    "error",
                    "frontmatter.close",
                    "SKILL.md frontmatter is not closed",
                    "SKILL.md",
                )
            )

    keys = []
    for line in frontmatter_lines:
        match = re.match(r"^([A-Za-z0-9_-]+):", line)
        if match:
            keys.append(match.group(1))
    for required in ("name", "description"):
        if required not in keys:
            issues.append(
                Issue(
                    "error",
                    "frontmatter.required",
                    f"Missing frontmatter key: {required}",
                    "SKILL.md",
                )
            )
    for key in sorted(set(keys) - {"name", "description"}):
        issues.append(
            Issue(
                "error",
                "frontmatter.extra",
                f"Unsupported frontmatter key: {key}",
                "SKILL.md",
            )
        )

    name_line = next((line for line in frontmatter_lines if line.startswith("name:")), "")
    name = name_line.partition(":")[2].strip()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", name):
        issues.append(
            Issue(
                "error",
                "skill.name",
                "Skill name must use lowercase letters, digits, and hyphens",
                "SKILL.md",
            )
        )
    if len(lines) > 500:
        issues.append(
            Issue(
                "warning",
                "skill.length",
                f"SKILL.md has {len(lines)} lines; keep it under 500",
                "SKILL.md",
            )
        )

    referenced = set(REFERENCE_PATTERN.findall(text))
    for relative in sorted(referenced):
        if not (root / relative).is_file():
            issues.append(
                Issue(
                    "error",
                    "reference.missing",
                    f"Referenced file does not exist: {relative}",
                    "SKILL.md",
                )
            )
    reference_dir = root / "references"
    if reference_dir.exists():
        actual = {
            f"references/{path.name}"
            for path in reference_dir.iterdir()
            if path.is_file()
        }
        for relative in sorted(actual - referenced):
            issues.append(
                Issue(
                    "warning",
                    "reference.orphan",
                    f"Reference is not linked from SKILL.md: {relative}",
                    relative,
                )
            )
    return make_report(
        "lint_skill",
        issues,
        root=str(root),
        line_count=len(lines),
        referenced_count=len(referenced),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint the scholar-ppt-cn Skill package.")
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = lint_skill(args.root.resolve())
    if args.report:
        write_json(args.report, report)
    print_report(report)
    return 1 if report["summary"]["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
