from __future__ import annotations

import json
from pathlib import Path

from benchmark.result_writer import save_run_results


def test_save_run_results_creates_and_updates_files(tmp_path: Path):
    first = save_run_results(
        "benchmark",
        {"ie": {"counts": {"allow": 1}, "results": [{"task_id": "t1", "verdict": "allow"}]}},
        results_dir=tmp_path,
    )
    assert first["run_file"].exists()
    assert first["latest_file"].exists()
    assert first["history_file"].exists()

    latest = json.loads(first["latest_file"].read_text(encoding="utf-8"))
    assert latest["run_type"] == "benchmark"
    assert latest["results"]["ie"]["counts"]["allow"] == 1

    second = save_run_results(
        "ablation",
        {"no_sandbox": {"results": [{"task_id": "t2", "verdict": "allow"}]}},
        results_dir=tmp_path,
    )
    assert second["run_file"].exists()
    assert second["run_file"] != first["run_file"]

    latest2 = json.loads(second["latest_file"].read_text(encoding="utf-8"))
    assert latest2["run_type"] == "ablation"

    history_lines = first["history_file"].read_text(encoding="utf-8").strip().splitlines()
    assert len(history_lines) == 2
