from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.common import load_json


def _copy_block(lines: list[str]) -> str:
    return "\n".join(f"- {line}" for line in lines)


def render_family_markdown(plan: dict[str, Any]) -> str:
    lines = [
        "# Blue Academic 完整视觉家族生成提示词",
        "",
        "本文件由 `family-expansion-plan.json` 导出。JSON 是机器真源。",
        "",
        "## 网页端生成方法",
        "",
        f"1. 每次生成前上传风格锚点：`{plan['anchor_image']}`。",
        "2. 每次只复制一个候选的完整提示词并生成一张 16:9 图片。",
        "3. 同一角色的三个候选独立生成，不要求复制前一个候选的几何。",
        "4. 人工只保留愿意用于真实学术汇报、且能重建为可编辑 PPT 的图片。",
        "5. 示例文字、图表、数值与结论只表达视觉结构，绝不进入真实 PPT。",
        "",
        "## 公共提示词",
        "",
        plan["shared_prompt"],
        "",
    ]
    for role in plan["roles"]:
        lines.extend([f"# {role['role']}", "", role["objective"], ""])
        for variant in role["variants"]:
            copy_block = _copy_block(variant["visible_copy"])
            lines.extend(
                [
                    f"## {variant['id']}",
                    "",
                    f"- 素材几何：`{variant['asset_geometry']}`",
                    f"- 示例主题：{variant['example_topic']}",
                    f"- 目标文件：`{variant['output_file']}`",
                    "",
                    "```text",
                    plan["shared_prompt"],
                    "",
                    "页面使用以下简短可见文字；如发生排版冲突，可减少辅助文字，但不要改成英文或乱码：",
                    copy_block,
                    "",
                    variant["task_prompt"],
                    "```",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export copy-ready prompts for a visual-reference family."
    )
    parser.add_argument("plan", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        plan = load_json(args.plan)
        content = render_family_markdown(plan)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8", newline="\n")
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
