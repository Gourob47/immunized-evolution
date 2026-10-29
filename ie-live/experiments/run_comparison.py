from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from agent.live_loop import LiveAgentLoop, LiveBudget
from agent.llm_client import PROVIDERS, resolve_llm_config
from analysis.make_tables import render_comparison_markdown
from experiments.checkpoint import (
    append_checkpoint,
    checkpoint_path,
    done_keys,
    load_checkpoint,
    write_text_atomic,
)


CONDITIONS = [
    "open_loop",
    "introspection_only",
    "ie",
    "ablation_no_kernel",
    "ablation_no_sandbox",
    "ablation_no_memory",
]


def comparison_doc(
    *,
    provider: str,
    model: str,
    conditions: list[str],
    n_tasks: int,
    rows: list[dict],
    complete: bool,
) -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": provider,
        "model": model,
        "conditions": conditions,
        "n_tasks": n_tasks,
        "complete": complete,
        "rows": rows,
    }


def persist_outputs(results_dir: Path, doc: dict, *, write_stamped: bool) -> tuple[Path | None, Path]:
    latest_json = results_dir / "latest_comparison.json"
    latest_md = results_dir / "latest_comparison.md"
    payload = json.dumps(doc, indent=2) + "\n"
    md = render_comparison_markdown(doc)
    write_text_atomic(latest_json, payload)
    write_text_atomic(latest_md, md)
    stamped = None
    if write_stamped:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        stamped = results_dir / f"comparison_{stamp}.json"
        write_text_atomic(stamped, payload)
        write_text_atomic(results_dir / f"comparison_{stamp}.md", md)
    return stamped, latest_json


def main() -> None:
    defaults = resolve_llm_config()
    parser = argparse.ArgumentParser(
        description="Run live comparative IE experiment. Provider/model default from env (IE_LLM_*)."
    )
    parser.add_argument("--tasks", type=Path, default=Path("live_tasks/tasks.json"))
    parser.add_argument("--provider", default=defaults.provider, choices=list(PROVIDERS))
    parser.add_argument("--model", default=defaults.model)
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    parser.add_argument("--conditions", nargs="*", default=CONDITIONS)
    args = parser.parse_args()

    cfg = resolve_llm_config(provider=args.provider, model=args.model)
    payload = json.loads(args.tasks.read_text(encoding="utf-8"))
    tasks = payload["tasks"]
    repos_root = args.tasks.parent / "repos"
    args.results_dir.mkdir(parents=True, exist_ok=True)

    ckpt = checkpoint_path(args.results_dir)
    rows = load_checkpoint(ckpt)
    done = done_keys(rows)
    expected = len(args.conditions) * len(tasks)
    if done:
        print(f"resume checkpoint={ckpt} done={len(done)}/{expected}")

    for condition in args.conditions:
        loop = LiveAgentLoop(
            condition=condition,
            provider=cfg.provider,
            model=cfg.model,
            budget=LiveBudget(),
        )
        for task in tasks:
            key = (condition, task["task_id"])
            if key in done:
                print(f"{condition:22} {task['task_id']:18} skipped (checkpoint)")
                continue
            result = loop.run_task(task, repos_root)
            row = result.__dict__
            append_checkpoint(ckpt, row)
            rows.append(row)
            done.add(key)
            persist_outputs(
                args.results_dir,
                comparison_doc(
                    provider=cfg.provider,
                    model=cfg.model,
                    conditions=args.conditions,
                    n_tasks=len(tasks),
                    rows=rows,
                    complete=len(done) == expected,
                ),
                write_stamped=False,
            )
            print(
                f"{condition:22} {task['task_id']:18} "
                f"success={result.task_success} unauth={result.unauthorized_actions} "
                f"blocked={result.blocked_attacks}"
            )

    complete = len(done) == expected
    stamped, latest = persist_outputs(
        args.results_dir,
        comparison_doc(
            provider=cfg.provider,
            model=cfg.model,
            conditions=args.conditions,
            n_tasks=len(tasks),
            rows=rows,
            complete=complete,
        ),
        write_stamped=complete,
    )
    print(f"provider={cfg.provider} model={cfg.model} complete={complete} done={len(done)}/{expected}")
    print(f"checkpoint={ckpt}")
    print(f"saved_json={stamped or latest}")


if __name__ == "__main__":
    main()
