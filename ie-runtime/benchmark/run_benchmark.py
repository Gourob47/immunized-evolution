from __future__ import annotations

import argparse
import json
from pathlib import Path

from benchmark.result_writer import save_run_results
from benchmark.runners import BenchmarkRunner
from benchmark.task_loader import TASKS, all_tasks, load_tasks_from_json
from benchmark.metrics import build_summary_table


def _annotate_categories(task_map: dict) -> dict:
    """Ensure each task carries its category label."""
    annotated = {}
    for category, tasks in task_map.items():
        annotated[category] = [{**task, "category": category} for task in tasks]
    return annotated


def main() -> None:
    parser = argparse.ArgumentParser(description="Run IE benchmark suite and save results.")
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=None,
        help="Optional output directory (default: ie-runtime/results)",
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=None,
        help="Optional external dataset JSON path (see DATASET_SCHEMA.md)",
    )
    parser.add_argument(
        "--print-json",
        action="store_true",
        help="Also print the full results payload to stdout",
    )
    args = parser.parse_args()

    if args.dataset:
        task_map = _annotate_categories(load_tasks_from_json(str(args.dataset)))
        total_tasks = sum(len(v) for v in task_map.values())
        categories = {name: len(items) for name, items in task_map.items()}
    else:
        task_map = _annotate_categories(TASKS)
        total_tasks = len(all_tasks())
        categories = {name: len(items) for name, items in TASKS.items()}

    runner = BenchmarkRunner()
    suite_results = runner.run_suite(task_map)
    table = build_summary_table(suite_results)

    paths = save_run_results(
        "benchmark",
        suite_results,
        results_dir=args.results_dir,
        extra={
            "total_unique_tasks": total_tasks,
            "categories": categories,
            "conditions": sorted(BenchmarkRunner.CONDITIONS),
            "summary_table": table,
            "dataset": str(args.dataset) if args.dataset else "builtin_TASKS",
        },
    )

    print("Benchmark run complete.")
    print(f"  tasks: {total_tasks}")
    print("Summary table:")
    for row in table:
        print(
            f"  {row['condition']}: n={row['n']} match_rate={row['match_rate']} "
            f"counts={row['counts']} unauthorized_allows={row['unauthorized_allows']}"
        )
    print("Results saved:")
    print(f"  new file : {paths['run_file']}")
    print(f"  latest   : {paths['latest_file']}")
    print(f"  history  : {paths['history_file']}")

    if args.print_json:
        print(json.dumps(suite_results, indent=2))


if __name__ == "__main__":
    main()
