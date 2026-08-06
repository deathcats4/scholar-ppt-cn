from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import render_preview


class RenderPreviewTests(unittest.TestCase):
    def test_render_cleans_stale_outputs_and_orders_pages_numerically(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pptx = root / "deck.pptx"
            output_dir = root / "previews"
            pptx.write_bytes(b"pptx")
            output_dir.mkdir()
            (output_dir / "slide-99.png").write_bytes(b"old")
            (output_dir / "old.pdf").write_bytes(b"old")
            (output_dir / "deck.pdf").write_bytes(b"old")
            cleanup_was_seen = {"value": False}

            def fake_run(command: list[str]) -> None:
                if "--convert-to" in command:
                    cleanup_was_seen["value"] = not list(output_dir.glob("slide-*.png")) and not list(
                        output_dir.glob("*.pdf")
                    )
                    (output_dir / "deck.pdf").write_bytes(b"pdf")
                else:
                    for number in (1, 10, 2, 3, 4, 5, 6, 7, 8, 9):
                        (output_dir / f"slide-{number}.png").write_bytes(b"png")

            with mock.patch.object(render_preview.shutil, "which", side_effect=lambda name: name):
                with mock.patch.object(render_preview, "_run", side_effect=fake_run):
                    report = render_preview.render(pptx, output_dir)

            self.assertTrue(cleanup_was_seen["value"])
            self.assertEqual(report["slide_count"], 10)
            self.assertEqual(
                [Path(path).name for path in report["slides"]],
                [f"slide-{number}.png" for number in range(1, 11)],
            )

    def test_render_does_not_reuse_stale_pdf_when_conversion_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pptx = root / "deck.pptx"
            output_dir = root / "previews"
            pptx.write_bytes(b"pptx")
            output_dir.mkdir()
            (output_dir / "stale.pdf").write_bytes(b"old")

            with mock.patch.object(render_preview.shutil, "which", side_effect=lambda name: name):
                with mock.patch.object(render_preview, "_run", return_value=None):
                    with self.assertRaisesRegex(RuntimeError, "expected PDF"):
                        render_preview.render(pptx, output_dir)

            self.assertFalse((output_dir / "stale.pdf").exists())

    def test_render_rejects_non_contiguous_slide_images(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pptx = root / "deck.pptx"
            output_dir = root / "previews"
            pptx.write_bytes(b"pptx")

            def fake_run(command: list[str]) -> None:
                if "--convert-to" in command:
                    output_dir.mkdir(exist_ok=True)
                    (output_dir / "deck.pdf").write_bytes(b"pdf")
                else:
                    (output_dir / "slide-1.png").write_bytes(b"png")
                    (output_dir / "slide-3.png").write_bytes(b"png")

            with mock.patch.object(render_preview.shutil, "which", side_effect=lambda name: name):
                with mock.patch.object(render_preview, "_run", side_effect=fake_run):
                    with self.assertRaisesRegex(RuntimeError, "not contiguous"):
                        render_preview.render(pptx, output_dir)


if __name__ == "__main__":
    unittest.main()
