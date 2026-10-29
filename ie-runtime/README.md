# IE Runtime

Kernel-mediated control for coding-agent actions: **propose → authorize → (optional) sandbox / memory / escalate**. Decision-suite runner for the 201-task JSON.

See the repository root [README](../README.md) for the system diagram and threat model. Live LLM loops live in `../ie-live/`.

## Scope

- Domain: coding assistant
- Protected actions: `tool_call`, `memory_write`, `code_exec`
- Verdicts: `allow`, `deny`, `sandbox`, `escalate` (+ memory `quarantined` / `rejected`)
- Escalation uses `kernel/escalate/reviewer_stub.py` (pending review only; no human in the loop)
- Dataset: `../datasets/ie-runtime/ie_runtime_decision_v1.json`. Schema: `DATASET_SCHEMA.md`.

## Architecture flow

```text
Task → map_task_to_proposal → IERuntime.mediate
         → KernelGateway.authorize
         → MemoryGovernor / Sandbox / ReviewerStub (as needed)
         → gated MemoryStore + AuditLog
         → feedback + benchmark metrics
```

## Quick start

```bash
cd ie-runtime
PYTHONPATH=. python3 -m pytest tests -q
```

## Run benchmark and save results

```bash
cd ie-runtime
PYTHONPATH=. python3 -m benchmark.run_benchmark --dataset ../datasets/ie-runtime/ie_runtime_decision_v1.json
PYTHONPATH=. python3 -m benchmark.ablation.run_ablation
```

Each run writes under `results/` (gitignored):

- `run_<timestamp>_<type>.json` — new file for that run
- `latest.json` — overwritten with the most recent run
- `history.jsonl` — append-only index of past runs

## Benchmark conditions

These names are for the **201-task decision suite** (`benchmark.run_benchmark`). They are not the live-agent condition ids.

1. `open_loop` — no kernel gate
2. `introspection_only` — self-check only (no external mediation)
3. `ie` — full kernel + memory governor + sandbox + audit
4. `ablation` — same runner, kernel mediation disabled (`enable_kernel=False`)

Additional decision ablations (`python3 -m benchmark.ablation.run_ablation`):

| Mode | What is turned off |
|---|---|
| `no_memory_governor` | memory governor |
| `no_sandbox` | sandbox |
| `no_escalation` | escalation stub |
| `no_kernel_mediation` | whole kernel (same idea as `ablation`) |

**Live** comparison (`ie-live`) uses different ids: `ablation_no_kernel`, `ablation_no_sandbox`, `ablation_no_memory`. Do not pass those strings to `run_benchmark`.

## Key modules

- `operational/` — proposer / planner / feedback
- `kernel/` — gateway, runtime pipeline, memory governor, audit, escalation stub
- `effects/` — gated memory store, sandbox runner
- `benchmark/` — mapper, runners, metrics, result writer
- `tests/` — unit and flow validation

Load the 201-task file with `DATASET_SCHEMA.md`. Do not use that file as live-agent tasks (`ie-live` uses `expected_safety` and repos).
