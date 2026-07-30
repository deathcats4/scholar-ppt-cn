from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.lint_skill import lint_skill


PACKAGE_ROOTS = (
    "SKILL.md",
    "LICENSE",
    "requirements-runtime.txt",
    "agents",
    "assets",
    "references",
    "schemas",
    "scripts",
)
LEGACY_TEMPLATE = "assets/templates/scholar-ppt-cn-reference-template.pptx"
EXCLUDED_NAMES = {"__pycache__", ".DS_Store", "Thumbs.db"}
AUTHORING_ONLY_PATHS = {
    "assets/visual-reference-packs/blue-academic/contact-sheet.png",
}
AUTHORING_ONLY_PREFIXES = (
    "assets/visual-reference-packs/blue-academic/generation/",
)
FIXED_ZIP_TIME = (2020, 1, 1, 0, 0, 0)


def _is_authoring_only(relative: str) -> bool:
    return relative in AUTHORING_ONLY_PATHS or relative.startswith(
        AUTHORING_ONLY_PREFIXES
    )


def _files(root: Path, include_legacy_template: bool) -> list[Path]:
    result: list[Path] = []
    for entry in PACKAGE_ROOTS:
        path = root / entry
        if not path.exists():
            if entry in {"SKILL.md", "agents", "references", "schemas", "scripts"}:
                raise FileNotFoundError(f"Required package entry is missing: {entry}")
            continue
        candidates = [path] if path.is_file() else path.rglob("*")
        for candidate in candidates:
            if not candidate.is_file():
                continue
            relative = candidate.relative_to(root).as_posix()
            if any(part in EXCLUDED_NAMES for part in candidate.parts):
                continue
            if candidate.suffix in {".pyc", ".pyo"}:
                continue
            if relative == LEGACY_TEMPLATE and not include_legacy_template:
                continue
            if _is_authoring_only(relative):
                continue
            result.append(candidate)
    return sorted(set(result), key=lambda item: item.relative_to(root).as_posix())


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_package(
    root: Path,
    output: Path,
    version: str,
    include_legacy_template: bool = False,
) -> dict:
    lint = lint_skill(root)
    if lint["summary"]["error"]:
        raise ValueError("Skill lint failed; fix errors before packaging")
    files = _files(root, include_legacy_template)
    payloads = {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in files
    }
    manifest = {
        "name": "scholar-ppt-cn",
        "version": version,
        "legacy_template_included": include_legacy_template,
        "files": [
            {
                "path": name,
                "bytes": len(data),
                "sha256": _hash(data),
            }
            for name, data in sorted(payloads.items())
        ],
    }
    manifest_data = (
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")

    output.parent.mkdir(parents=True, exist_ok=True)
    package_prefix = PurePosixPath("scholar-ppt-cn")
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(payloads.items()):
            info = zipfile.ZipInfo(str(package_prefix / name), FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
        info = zipfile.ZipInfo(str(package_prefix / "manifest.json"), FIXED_ZIP_TIME)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, manifest_data)

    digest = _hash(output.read_bytes())
    checksum = output.with_suffix(output.suffix + ".sha256")
    checksum.write_text(f"{digest}  {output.name}\n", encoding="utf-8", newline="\n")
    return {
        "package": str(output),
        "sha256": digest,
        "checksum_file": str(checksum),
        "file_count": len(payloads),
        "legacy_template_included": include_legacy_template,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a deterministic Skill ZIP.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    parser.add_argument("--version", default="dev")
    parser.add_argument("--include-legacy-template", action="store_true")
    args = parser.parse_args()
    if not re_safe_version(args.version):
        parser.error("--version may contain only letters, digits, dots, hyphens, and underscores")
    root = args.root.resolve()
    output = args.output or root / "dist" / f"scholar-ppt-cn-{args.version}.zip"
    try:
        result = build_package(
            root,
            output,
            args.version,
            include_legacy_template=args.include_legacy_template,
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def re_safe_version(value: str) -> bool:
    return re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value) is not None


if __name__ == "__main__":
    raise SystemExit(main())
