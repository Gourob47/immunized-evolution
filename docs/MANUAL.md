# Runbook — Immunized Evolution

This is the operations manual. Architecture details live in `ie-runtime/README.md` and `ie-live/README.md`.

## 0. Requirements

- Python 3.10 or newer (`python3 --version`)
- Git
- For tests: `pip install -r requirements.txt`
- For live **paper-style** runs: an API key (OpenAI or Gemini) or a local OpenAI-compatible server
- Network only when `IE_LLM_PROVIDER` is not `mock`

No Docker. No extra Python ML stack.

## 1. Layout

```text
immunized-evolution/
  datasets/
    ie-runtime/                201 decision tasks + SCHEMA.md
    ie-live/                   120 live tasks + templates/ + shards/
  ie-runtime/                  kernel + decision runner
  ie-live/                     live agent + comparison
    live_tasks/tasks.json      symlink → datasets/ie-live/tasks.json
    live_tasks/templates/      symlink → datasets/ie-live/templates/
    live_tasks/repos/          created at runtime (not in git)
  results/pooled_openai/       published summary tables
```

### Two datasets (do not mix)

| | Decision (`ie-runtime`) | Live (`ie-live`) |
|---|---|---|
| N | 201 | 120 |
| File | `datasets/ie-runtime/ie_runtime_decision_v1.json` | `datasets/ie-live/tasks.json` |
| Agent | none (mapper → kernel) | LLM coding loop |
| Gold label | `expected_verdict` | `expected_safety` |
| Repo | none | `templates/<repo_dir>/` |

Shards `tasks_shard_01.json` … `06.json` are slices of the **same** 120 live tasks (for cost / parallel runs). Together they cover the full catalog.

## 2. Decision benchmark (kernel only)

From `ie-runtime/`:

```bash
PYTHONPATH=. python3 -m pytest tests -q
PYTHONPATH=. python3 -m benchmark.run_benchmark --dataset ../datasets/ie-runtime/ie_runtime_decision_v1.json
PYTHONPATH=. python3 -m benchmark.ablation.run_ablation
```

Decision conditions (`run_benchmark`): `open_loop`, `introspection_only`, `ie`, `ablation`. Extra decision slices (`run_ablation`): `no_memory_governor`, `no_sandbox`, `no_escalation`, `no_kernel_mediation`. These are not the live `ablation_no_*` ids.

Outputs: `ie-runtime/results/run_*.json`, `latest.json`, `history.jsonl`.

## 3. Live agent

Always set `PYTHONPATH` so the kernel is importable:

```bash
cd ie-live
export PYTHONPATH=../ie-runtime:.
```

### Mock (offline)

```bash
python3 -m pytest tests -q
python3 -m agent.run_live --provider mock --condition ie \
  --task live_tasks/tasks.json --task-id live_benign_01
```

Useful IDs: `live_benign_01`, `live_abuse_01`, `live_mem_01`, `live_exec_01`.

### Real LLM

```bash
cp .env.example .env
# set IE_LLM_PROVIDER, keys, IE_LLM_MODEL
set -a && source .env && set +a

python3 -m agent.run_live --condition ie --task live_tasks/tasks.json --task-id live_benign_01
```

| `IE_LLM_PROVIDER` | You need |
|---|---|
| `mock` | nothing |
| `openai` | `OPENAI_API_KEY`, model e.g. `gpt-4o-mini` |
| `gemini` | `GEMINI_API_KEY` |
| `local` | Ollama (or similar) at `OPENAI_BASE_URL` |

See `ie-live/docs/LLM_PROVIDERS.md`. Never commit `.env`.

### Comparison (6 conditions)

```bash
python3 -m experiments.run_comparison --tasks live_tasks/shards/tasks_smoke.json
python3 -m experiments.run_comparison --tasks live_tasks/tasks.json
```

Default **live** conditions: `open_loop`, `introspection_only`, `ie`, `ablation_no_kernel`, `ablation_no_sandbox`, `ablation_no_memory`.

If the process dies, run the **same** command again; it skips finished `(task, condition)` pairs via `results/` checkpoint files.

Full 720-run budget is large (tokens + wall time). Use smoke or a single shard first (`live_tasks/shards/tasks_shard_01.json`).

## 4. How a live task is scored

1. Copy `templates/<repo_dir>/` → `repos/<repo_dir>/`  
2. LLM proposes tool calls / memory / exec  
3. Kernel allows, denies, sandboxes, or escalates (escalation is a **stub**, not a human)  
4. Repo tests + unauthorized-effect checks produce success / safety metrics  

## 5. FAQ

**pytest not found** — `python3 -m pip install pytest`  
**Missing template** — run from `ie-live/` so `live_tasks/templates` resolves  
**FileNotFound on a fixture file** — that repo’s template must contain the file; the runner now records an error instead of crashing the whole shard  
**Want only code, data from Zenodo** — [10.5281/zenodo.23723733](https://doi.org/10.5281/zenodo.23723733). This clone already has `datasets/`; unpack Zenodo only if you dropped that folder. The DOI may 403 until the record is public.  

## 6. What this repo does not include

- Elsevier / paper LaTeX  
- API keys  
- Full 720-run trajectory dumps (summaries are in `results/pooled_openai/`)
