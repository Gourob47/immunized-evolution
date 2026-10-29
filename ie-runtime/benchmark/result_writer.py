from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def ensure_results_dir(results_dir: Path | None = None) -> Path:
    path = Path(results_dir) if results_dir is not None else DEFAULT_RESULTS_DIR
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_payload(
    run_type: str,
    results: dict[str, Any],
    *,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    now = _utc_now()
    payload: dict[str, Any] = {
        "run_id": now.strftime("%Y%m%d_%H%M%S"),
        "timestamp": now.isoformat(),
        "run_type": run_type,
        "results": results,
    }
    if extra:
        payload["meta"] = extra
    return payload


def save_run_results(
    run_type: str,
    results: dict[str, Any],
    *,
    results_dir: Path | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Path]:
    """
    Persist one benchmark run.

    Creates:
    - results/run_<timestamp>_<run_type>.json  (new file each run)
    - results/latest.json                      (updated each run)
    - results/history.jsonl                    (append one summary line)
    """
    out_dir = ensure_results_dir(results_dir)
    payload = build_payload(run_type, results, extra=extra)
    run_id = payload["run_id"]

    run_path = out_dir / f"run_{run_id}_{run_type}.json"
    latest_path = out_dir / "latest.json"
    history_path = out_dir / "history.jsonl"

    text = json.dumps(payload, indent=2, sort_keys=False)
    run_path.write_text(text + "\n", encoding="utf-8")
    latest_path.write_text(text + "\n", encoding="utf-8")

    history_line = {
        "run_id": run_id,
        "timestamp": payload["timestamp"],
        "run_type": run_type,
        "result_file": run_path.name,
        "summary": _compact_summary(results),
    }
    with history_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(history_line) + "\n")

    return {
        "run_file": run_path,
        "latest_file": latest_path,
        "history_file": history_path,
    }


def _compact_summary(results: dict[str, Any]) -> dict[str, Any]:
    """Build a small summary for history.jsonl."""
    summary: dict[str, Any] = {}
    for key, value in results.items():
        if isinstance(value, dict) and "counts" in value:
            summary[key] = {
                "counts": value.get("counts", {}),
                "n": len(value.get("results", [])),
            }
        elif isinstance(value, dict) and "results" in value:
            summary[key] = {"n": len(value.get("results", []))}
        else:
            summary[key] = "present"
    return summary
