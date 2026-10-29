from __future__ import annotations

import json
import os
from pathlib import Path


CHECKPOINT_NAME = "checkpoint.jsonl"


def checkpoint_path(results_dir: Path) -> Path:
    return results_dir / CHECKPOINT_NAME


def load_checkpoint(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def done_keys(rows: list[dict]) -> set[tuple[str, str]]:
    return {(row["condition"], row["task_id"]) for row in rows}


def append_checkpoint(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def write_text_atomic(path: Path, text: str) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)
