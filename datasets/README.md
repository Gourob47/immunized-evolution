# Immunized Evolution datasets

Canonical **task suites** only. Code stays in `ie-runtime/` and `ie-live/`. Run outputs live in `results/` (sibling), not here.

Those trees **symlink** back here so existing commands keep working (`ie-live/live_tasks/tasks.json`, `templates/`, `shards/*.json`).

| Suite | Path | What it is |
|---|---|---|
| Decision (201 tasks) | `ie-runtime/ie_runtime_decision_v1.json` | Kernel microbenchmark (`expected_verdict`) |
| Live (120 tasks) | `ie-live/tasks.json` + `ie-live/templates/` | Coding-agent fixtures (`expected_safety`, repos) |
| Live shards | `ie-live/shards/tasks_shard_0N.json` | Same 120 tasks in 6 slices |

Do **not** merge the two JSON schemas. Runtime uses `expected_verdict` / `action_type`. Live uses `repo_dir` / `success_check`.

## Load from the repo root

```text
ie-live/live_tasks/tasks.json        -> datasets/ie-live/tasks.json
ie-live/live_tasks/templates/        -> datasets/ie-live/templates/
ie-live/live_tasks/shards/tasks_*.json -> datasets/ie-live/shards/
```

Runtime working copies remain in `ie-live/live_tasks/repos/` (reset from templates; not published as source of truth).

```bash
# decision suite
cd ie-runtime
PYTHONPATH=. python3 -m benchmark.run_benchmark --dataset ../datasets/ie-runtime/ie_runtime_decision_v1.json

# live suite (paths via symlink)
cd ie-live
PYTHONPATH=../ie-runtime:. python3 -m experiments.run_comparison --tasks live_tasks/tasks.json
```
