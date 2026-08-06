from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


STRICT_PROFILES = {"group-meeting", "defense", "conference", "classroom"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify that a QA report belongs to the final PPTX bytes and that "
            "the report passed its delivery-blocking checks."
        )
    )
    parser.add_argument("pptx", type=Path)
    parser.add_argument("report", type=Path)
    parser.add_argument(
        "--require-profile",
        choices=sorted(STRICT_PROFILES | {"template-preserve"}),
        help="Fail if the QA report was not generated with this profile.",
    )
    args = parser.parse_args()

    report = json.loads(args.report.read_text(encoding="utf-8"))
    details = report.get("details", {})
    summary = report.get("summary", {})
    expected = details.get("sha256")
    actual = sha256(args.pptx)
    hash_ok = isinstance(expected, str) and expected == actual

    error_count = summary.get("error")
    qa_ok = isinstance(error_count, int) and error_count == 0

    profile = details.get("qa_profile")
    profile_ok = args.require_profile is None or profile == args.require_profile

    typography = details.get("typography", {})
    ok = hash_ok and qa_ok and profile_ok
    print(
        json.dumps(
            {
                "status": "passed" if ok else "failed",
                "pptx": str(args.pptx),
                "report": str(args.report),
                "expected_sha256": expected,
                "actual_sha256": actual,
                "hash_ok": hash_ok,
                "qa_error_count": error_count,
                "qa_ok": qa_ok,
                "qa_profile": profile,
                "required_profile": args.require_profile,
                "profile_ok": profile_ok,
                "body_norm_autofit": typography.get("body_norm_autofit"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
