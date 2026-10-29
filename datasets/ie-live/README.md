# IE-live task suite (N=120)

- `tasks.json` — 48 benign + 24 capability_abuse + 24 memory_poison + 24 unsafe_exec
- `templates/<repo_dir>/` — pristine repos (source of truth)
- `shards/` — costing slices (`tasks_shard_01.json` … `06.json`)

Fields include `task_id`, `category`, `prompt`, `repo_dir`, `expected_safety`, `success_check`.
