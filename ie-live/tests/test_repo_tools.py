import tempfile
import unittest
from pathlib import Path

from tools.repo_tools import RepoTools


class RepoToolsTests(unittest.TestCase):
    def test_read_missing_file_returns_error(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "app.py").write_text("x = 1\n", encoding="utf-8")
            tools = RepoTools(root)
            result = tools.read_file("benign_json_key.json")
            self.assertEqual(result["status"], "error")
            self.assertIn("error", result)

    def test_read_existing_file_ok(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "app.py").write_text("x = 1\n", encoding="utf-8")
            tools = RepoTools(root)
            result = tools.read_file("app.py")
            self.assertEqual(result["status"], "ok")
            self.assertIn("x = 1", result["content"])
