from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.common import load_json


def _visible_copy(copy: dict[str, Any]) -> str:
    lines = [
        f"- 栏目：{copy['eyebrow']}",
        f"- 标题：{copy['title']}",
    ]
    lines.extend(f"- 解释：{item}" for item in copy["interpretation"])
    lines.append(f"- 图注：{copy['caption']}")
    return "\n".join(lines)


def render_markdown(plan: dict[str, Any]) -> str:
    copy_block = _visible_copy(plan["visible_copy"])
    lines = [
        "# Blue Academic A/B 视觉参考图生成提示词",
        "",
        "本文件由 `generation-plan.json` 导出。请修改 JSON 后重新生成，不要独立维护两份提示词。",
        "",
        "## 使用方式",
        "",
        "1. 每次只生成一张完整的 16:9 幻灯片图片。",
        "2. 先生成每组 A 版；生成 B 版时上传对应 A 版作为参考图。",
        "3. 不满意时用同一提示词独立重试，不要求模型在一张图里拼多个方案。",
        "4. 候选图先保存在 `candidates/`，只有人工认可的图片才进入正式参考包。",
        "",
        "## 固定可见文字",
        "",
        copy_block,
        "",
        "## A 版公共提示词",
        "",
        plan["shared_prompt"],
        "",
    ]
    for task in plan["tasks"]:
        lines.extend(
            [
                f"## {task['id']}",
                "",
                f"- 构图：{task['composition']}",
                f"- 目标文件：`{task['output_file']}`",
            ]
        )
        if task["source_task_id"]:
            lines.append(f"- 编辑参考：先上传 `{task['source_task_id']}` 的输出图片")
        lines.extend(["", "```text"])
        if task["variant"] == "A-realistic-synthetic":
            lines.extend(
                [
                    plan["shared_prompt"],
                    "",
                    "页面必须准确使用以下可见文字：",
                    copy_block,
                    "",
                    task["task_prompt"],
                ]
            )
        else:
            lines.extend(
                [
                    task["task_prompt"],
                    "",
                    "页面中的固定文字仍为：",
                    copy_block,
                ]
            )
        lines.extend(["```", ""])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export copy-ready visual-reference prompts from JSON."
    )
    parser.add_argument("plan", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        plan = load_json(args.plan)
        content = render_markdown(plan)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8", newline="\n")
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

