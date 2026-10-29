# IE-live shards (1/6 costing slices)

Each numbered shard has **20 tasks** (8 benign + 4 abuse + 4 memory + 4 unsafe_exec).
Full comparison on one shard: **20 × 6 conditions = 120 runs** = **1/6 of 720**.

Templates stay in `../templates/`. Do not copy them per shard.

## Result directories

| Run | `--tasks` | `--results-dir` |
|---|---|---|
| Paper (OpenAI) | `tasks_shard_0N.json` | `results/shard_0N_openai` |
| Mock costing | `tasks_shard_0N.json` | `results/shard_0N` |
| Extra seed (optional) | same shard file again | e.g. `results/shard_02_openai_seed2` |

See `results/README.md` for the on-disk inventory.

## Costing order

1. Smoke (4 tasks, `ie` only) — measure tokens, stop if too expensive.
2. Shard 01 × all 6 conditions — multiply that bill by 6 for the paper estimate.
3. Shards 02–06 when the first shard looks acceptable.

```bash
cd ie-live
set -a; source .env; set +a

# 0) smoke
PYTHONPATH=../ie-runtime:. python3 -m experiments.run_comparison \
  --tasks live_tasks/shards/tasks_smoke.json \
  --conditions ie \
  --results-dir results/smoke_ie

# 1) paper sixth (OpenAI via .env)
PYTHONPATH=../ie-runtime:. python3 -m experiments.run_comparison \
  --tasks live_tasks/shards/tasks_shard_01.json \
  --results-dir results/shard_01_openai
```

Then `tasks_shard_02.json` … `06.json` with `results/shard_02_openai` … `shard_06_openai`.

Use a separate `--results-dir` per job so later runs do not overwrite `latest_comparison.md`. Re-run the **same** command after a crash: finished `(condition, task_id)` pairs are stored in `checkpoint.jsonl` and skipped. Never point a new shard's task file at another shard's results dir.
