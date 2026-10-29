from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from agent.live_loop import LiveAgentLoop, LiveBudget
from agent.llm_client import PROVIDERS, resolve_llm_config


def load_task(tasks_path: Path, task_id: str) -> dict:
    payload = json.loads(tasks_path.read_text(encoding="utf-8"))
    for task in payload["tasks"]:
        if task["task_id"] == task_id:
            return task
    raise KeyError(f"Task not found: {task_id}")


def main() -> None:
    defaults = resolve_llm_config()
    parser = argparse.ArgumentParser(
        description="Run one live IE agent task. Provider/model default from env (IE_LLM_*)."
    )
    parser.add_argument("--task", type=Path, default=Path("live_tasks/tasks.json"))
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--condition", default="ie")
    parser.add_argument("--provider", default=defaults.provider, choices=list(PROVIDERS))
    parser.add_argument("--model", default=defaults.model)
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    args = parser.parse_args()

    task = load_task(args.task, args.task_id)
    repos_root = args.task.parent / "repos"
    cfg = resolve_llm_config(provider=args.provider, model=args.model)
    loop = LiveAgentLoop(
        condition=args.condition,
        provider=cfg.provider,
        model=cfg.model,
        budget=LiveBudget(),
    )
    result = loop.run_task(task, repos_root)

    args.results_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out = args.results_dir / f"live_{stamp}_{args.condition}_{args.task_id}.json"
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "task": task,
        "condition": args.condition,
        "provider": cfg.provider,
        "model": cfg.model,
        "result": result.__dict__,
    }
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest = args.results_dir / "latest_live.json"
    latest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"provider={cfg.provider} model={cfg.model}")
    print(f"task_id={result.task_id} condition={result.condition}")
    print(f"task_success={result.task_success} unauthorized={result.unauthorized_actions} blocked={result.blocked_attacks}")
    print(f"steps={result.steps_used} tokens={result.tokens_used} latency_ms={result.latency_ms:.1f}")
    print(f"saved={out}")


if __name__ == "__main__":
    main()
