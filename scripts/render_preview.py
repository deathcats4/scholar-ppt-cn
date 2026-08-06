from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
from pathlib import Path


SLIDE_IMAGE_RE = re.compile(r"^slide-(\d+)\.png$")


def _run(command: list[str]) -> None:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed ({result.returncode}): {' '.join(command)}\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )


def _clear_previous_outputs(output_dir: Path) -> None:
    for pattern in ("slide-*.png", "*.pdf"):
        for path in output_dir.glob(pattern):
            if path.is_file():
                path.unlink()


def _slide_number(path: Path) -> int:
    match = SLIDE_IMAGE_RE.match(path.name)
    if not match:
        raise RuntimeError(f"Unexpected slide preview filename: {path.name}")
    return int(match.group(1))


def render(pptx: Path, output_dir: Path, dpi: int = 144, montage: Path | None = None, columns: int = 4) -> dict:
    if not pptx.exists():
        raise FileNotFoundError(pptx)
    soffice = shutil.which("soffice")
    pdftoppm = shutil.which("pdftoppm")
    if not soffice:
        raise RuntimeError("LibreOffice soffice is required to render PPTX previews.")
    if not pdftoppm:
        raise RuntimeError("Poppler pdftoppm is required to render PDF pages.")

    output_dir.mkdir(parents=True, exist_ok=True)
    _clear_previous_outputs(output_dir)
    _run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(output_dir), str(pptx)])
    pdf = output_dir / f"{pptx.stem}.pdf"
    if not pdf.exists():
        candidates = list(output_dir.glob("*.pdf"))
        if len(candidates) != 1:
            raise RuntimeError("LibreOffice did not produce the expected PDF.")
        pdf = candidates[0]

    prefix = output_dir / "slide"
    _run([pdftoppm, "-png", "-r", str(dpi), str(pdf), str(prefix)])
    pages = sorted(output_dir.glob("slide-*.png"), key=_slide_number)
    if not pages:
        raise RuntimeError("No slide images were produced.")
    page_numbers = [_slide_number(path) for path in pages]
    expected_numbers = list(range(1, len(pages) + 1))
    if page_numbers != expected_numbers:
        raise RuntimeError(
            "Slide preview sequence is not contiguous: "
            f"found {page_numbers}, expected {expected_numbers}"
        )

    montage_path = None
    if montage:
        try:
            from PIL import Image, ImageOps, ImageDraw
        except ImportError as exc:
            raise RuntimeError("Pillow is required to create a montage.") from exc

        images = [Image.open(path).convert("RGB") for path in pages]
        thumb_width = min(480, max(image.width for image in images))
        thumb_height = round(thumb_width * images[0].height / images[0].width)
        gutter = 24
        label_height = 34
        cols = max(1, columns)
        rows = math.ceil(len(images) / cols)
        canvas = Image.new("RGB", (cols * thumb_width + (cols + 1) * gutter, rows * (thumb_height + label_height) + (rows + 1) * gutter), "white")
        draw = ImageDraw.Draw(canvas)
        for index, image in enumerate(images):
            fitted = ImageOps.contain(image, (thumb_width, thumb_height))
            x = gutter + (index % cols) * (thumb_width + gutter)
            y = gutter + (index // cols) * (thumb_height + label_height + gutter)
            canvas.paste(fitted, (x, y))
            draw.text((x, y + thumb_height + 6), f"Slide {index + 1}", fill="black")
        montage.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(montage)
        montage_path = str(montage)

    return {
        "pptx": str(pptx),
        "pdf": str(pdf),
        "preview_dir": str(output_dir),
        "slide_count": len(pages),
        "slides": [str(path) for path in pages],
        "montage": montage_path,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Render PPTX slides and an optional montage.")
    parser.add_argument("pptx")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--montage")
    parser.add_argument("--dpi", type=int, default=144)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--report")
    args = parser.parse_args()

    report = render(
        Path(args.pptx),
        Path(args.output_dir),
        dpi=args.dpi,
        montage=Path(args.montage) if args.montage else None,
        columns=args.columns,
    )
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        Path(args.report).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
