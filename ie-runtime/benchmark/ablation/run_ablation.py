from __future__ import annotations

import argparse
from pathlib import Path

from benchmark.ablation.variants import ABLATION_MODES, AblationRunner
from benchmark.result_writer import save_run_results
from benchmark.task_loader import all_tasks


def main() -> None:
    parser = argparse.ArgumentParser(description="Run IE ablation modes and save results.")
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=None,
        help="Optional output directory (default: ie-runtime/results)",
    )
    args = parser.parse_args()

    tasks = all_tasks()
    ablation_results = {}
    for mode in ABLATION_MODES:
        summary = AblationRunner(mode).run(tasks)
        ablation_results[mode] = summary
        print(
            mode,
            "match_rate=",
            round(summary.get("match_rate", 0.0), 3),
            "counts=",
            summary.get("counts", {}),
        )

    paths = save_run_results(
        "ablation",
        ablation_results,
        results_dir=args.results_dir,
        extra={
            "total_tasks": len(tasks),
            "modes": list(ABLATION_MODES.keys()),
        },
    )

    print("Ablation run complete.")
    print("Results saved:")
    print(f"  new file : {paths['run_file']}")
    print(f"  latest   : {paths['latest_file']}")
    print(f"  history  : {paths['history_file']}")


if __name__ == "__main__":
    main()
