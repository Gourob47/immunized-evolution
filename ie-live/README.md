# IE Live — Live-Agent Validation of Immunized Evolution

This folder implements the **live LLM coding-agent experiment** on top of `ie-runtime/`.

It upgrades from decision-level microbenchmarks to a **full system experiment**:

```text
Task + repo
  → LLM Operational layer
  → Immunized Evolution kernel (Propose → Authorize)
  → Tools / Memory / Sandbox
  → Audit + feedback
  → Continue until success / budget
```

## Relationship to `ie-runtime/`

| Artifact | Role |
|---|---|
| `ie-runtime/` | Kernel, policy, memory governor, sandbox, 201-task decision benchmark |
| `ie-live/` | Live agent loop, repo fixtures, comparative system experiments |

Keep both. The 201-task suite remains a supplementary microbenchmark; this folder is the live coding-agent experiment. System diagram, threat model, and scoring caveats: [root README](../README.md#architecture).

## Quick start

```bash
cd ie-live
PYTHONPATH=../ie-runtime:. python3 -m pytest tests -q
PYTHONPATH=../ie-runtime:. python3 -m agent.run_live --condition ie --task live_tasks/tasks.json --task-id live_benign_01
PYTHONPATH=../ie-runtime:. python3 -m experiments.run_comparison --tasks live_tasks/tasks.json
# Catalog and templates are canonical under ../datasets/ie-live/ (symlinked from live_tasks/).
```

### Switch LLM provider via env

See `docs/LLM_PROVIDERS.md` and `.env.example`.

```bash
# Gemini
export IE_LLM_PROVIDER=gemini
export GEMINI_API_KEY=your_key
export IE_LLM_MODEL=gemini-2.0-flash

# OpenAI
export IE_LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-...

# Local (Ollama)
export IE_LLM_PROVIDER=local
export OPENAI_BASE_URL=http://127.0.0.1:11434/v1
export OPENAI_API_KEY=ollama
export IE_LLM_MODEL=llama3.1
```

CLI `--provider` / `--model` override env defaults.

Results are written under `results/`.

## Layout

```text
ie-live/
  docs/                 # Provider setup (`LLM_PROVIDERS.md`)
  agent/                # Live LLM operational layer + loop
  tools/                # Kernel-mediated tool adapters
  live_tasks/           # Symlinks to ../datasets/ie-live/ + runtime repos/
  experiments/          # Comparative runners
  analysis/             # Metrics + paper table helpers
  results/              # Run outputs
  tests/                # Unit / smoke tests
```
