import tempfile
import unittest
from pathlib import Path

from experiments.checkpoint import append_checkpoint, done_keys, load_checkpoint, write_text_atomic


class CheckpointTests(unittest.TestCase):
    def test_checkpoint_append_and_resume(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "checkpoint.jsonl"
            append_checkpoint(path, {"condition": "open_loop", "task_id": "live_benign_25", "task_success": False})
            append_checkpoint(path, {"condition": "open_loop", "task_id": "live_benign_26", "task_success": False})
            rows = load_checkpoint(path)
            self.assertEqual(len(rows), 2)
            done = done_keys(rows)
            self.assertIn(("open_loop", "live_benign_25"), done)
            self.assertNotIn(("introspection_only", "live_benign_25"), done)

    def test_write_text_atomic(self):
        with tempfile.TemporaryDirectory() as raw:
            dest = Path(raw) / "latest_comparison.json"
            write_text_atomic(dest, '{"ok": true}\n')
            self.assertEqual(dest.read_text(encoding="utf-8"), '{"ok": true}\n')
            self.assertFalse(dest.with_name(dest.name + ".tmp").exists())
