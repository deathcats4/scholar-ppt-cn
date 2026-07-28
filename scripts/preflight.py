from __future__ import annotations

import argparse
import importlib.util
import platform
import shutil
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.common import write_json


EXECUTABLES = {
    "office_renderer": ("soffice", "libreoffice"),
    "pdf_renderer": ("pdftoppm", "mutool"),
    "pdf_converter": ("pdftocairo",),
}
OPTIONAL_MODULES = {
    "pptx_write": "pptx",
    "image_inspection": "PIL",
    "json_schema": "jsonschema",
}
CJK_FONT_HINTS = (
    "microsoft yahei",
    "msyh",
    "pingfang",
    "source han sans",
    "sourcehansans",
    "noto sans cjk",
    "noto sans sc",
    "notosanscjk",
    "notosanssc",
    "simhei",
    "simsun",
    "deng",
    "思源黑体",
    "微软雅黑",
)


def _find_executable(names: tuple[str, ...]) -> str | None:
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    return None


def _font_roots() -> list[Path]:
    system = platform.system()
    home = Path.home()
    if system == "Windows":
        return [Path("C:/Windows/Fonts")]
    if system == "Darwin":
        return [
            Path("/System/Library/Fonts"),
            Path("/Library/Fonts"),
            home / "Library/Fonts",
        ]
    return [
        Path("/usr/share/fonts"),
        Path("/usr/local/share/fonts"),
        home / ".fonts",
        home / ".local/share/fonts",
    ]


def _font_inventory() -> dict[str, Any]:
    names: list[str] = []
    for root in _font_roots():
        if not root.exists():
            continue
        for pattern in ("*.ttf", "*.otf", "*.ttc"):
            names.extend(path.stem for path in root.rglob(pattern))
    normalized = sorted(set(names), key=str.casefold)
    matches = [
        name
        for name in normalized
        if any(hint in name.casefold() for hint in CJK_FONT_HINTS)
    ]
    return {
        "available": bool(matches),
        "provider": matches[0] if matches else None,
        "notes": f"Detected {len(normalized)} font files; CJK candidates: {len(matches)}",
        "cjk_candidates": matches[:30],
    }


def probe() -> dict[str, Any]:
    capabilities: dict[str, Any] = {
        "filesystem": {
            "available": True,
            "provider": "python-pathlib",
            "notes": "Local filesystem access is available.",
        },
        "python": {
            "available": sys.version_info >= (3, 11),
            "provider": sys.executable,
            "notes": platform.python_version(),
        },
    }
    for capability, names in EXECUTABLES.items():
        found = _find_executable(names)
        capabilities[capability] = {
            "available": found is not None,
            "provider": found,
            "notes": "Detected locally." if found else f"Not found: {', '.join(names)}",
        }
    for capability, module in OPTIONAL_MODULES.items():
        available = importlib.util.find_spec(module) is not None
        capabilities[capability] = {
            "available": available,
            "provider": module if available else None,
            "notes": f"Python module {'available' if available else 'not installed'}: {module}",
        }
    capabilities["cjk_fonts"] = _font_inventory()
    capabilities["image_generation"] = {
        "available": None,
        "provider": None,
        "notes": "Host capability; the active agent must set this value.",
    }
    capabilities["vision_inspection"] = {
        "available": None,
        "provider": None,
        "notes": "Host capability; the active agent must set this value.",
    }
    return {
        "tool": "preflight",
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        "capabilities": capabilities,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe optional scholar-ppt-cn capabilities.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = probe()
    if args.output:
        write_json(args.output, report)
    import json

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
