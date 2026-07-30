from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required to build the contact sheet") from exc


def _font(size: int) -> ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/msyh.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def build_contact_sheet(image_dir: Path, output: Path) -> None:
    image_paths = sorted(image_dir.glob("*.png"))
    if not image_paths:
        raise ValueError(f"No PNG images found in {image_dir}")
    thumb_width, thumb_height = 480, 270
    padding, label_height = 24, 52
    columns = min(3, len(image_paths))
    rows = (len(image_paths) + columns - 1) // columns
    width = padding + columns * (thumb_width + padding)
    height = padding + rows * (thumb_height + label_height + padding)
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    font = _font(22)
    for index, path in enumerate(image_paths):
        column = index % columns
        row = index // columns
        left = padding + column * (thumb_width + padding)
        top = padding + row * (thumb_height + label_height + padding)
        with Image.open(path) as source:
            thumb = source.convert("RGB")
            thumb.thumbnail((thumb_width, thumb_height))
            x = left + (thumb_width - thumb.width) // 2
            y = top + (thumb_height - thumb.height) // 2
            canvas.paste(thumb, (x, y))
        draw.rectangle(
            (left, top, left + thumb_width, top + thumb_height),
            outline="#D8E2F0",
            width=2,
        )
        draw.text(
            (left, top + thumb_height + 12),
            path.stem,
            fill="#143B73",
            font=font,
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, format="PNG", optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a visual-reference contact sheet.")
    parser.add_argument("image_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        build_contact_sheet(args.image_dir, args.output)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
