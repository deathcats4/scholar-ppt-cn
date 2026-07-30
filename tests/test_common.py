from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.common import load_json, write_json


class CommonTests(unittest.TestCase):
    def test_write_json_replaces_target_after_complete_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "project.json"
            write_json(target, {"version": 1})
            write_json(target, {"version": 2, "title": "测试"})
            self.assertEqual(
                {"version": 2, "title": "测试"},
                load_json(target),
            )

    def test_failed_serialization_preserves_existing_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "project.json"
            write_json(target, {"version": 1})
            with self.assertRaises(TypeError):
                write_json(target, {"invalid": object()})
            self.assertEqual({"version": 1}, load_json(target))
            temporary_files = list(target.parent.glob(f".{target.name}.*.tmp"))
            self.assertEqual([], temporary_files)


if __name__ == "__main__":
    unittest.main()
