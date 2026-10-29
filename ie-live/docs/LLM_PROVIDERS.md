# LLM Providers

`ie-live` selects the model backend from environment variables (CLI flags override).

## Providers

| `IE_LLM_PROVIDER` | Backend | Required env |
|---|---|---|
| `mock` | Deterministic offline planner | none |
| `openai` | OpenAI Chat Completions | `OPENAI_API_KEY` |
| `openai_compatible` | Same as OpenAI client | `OPENAI_API_KEY`, optional `OPENAI_BASE_URL` |
| `local` | Local OpenAI-compatible server | `OPENAI_BASE_URL` or `LOCAL_LLM_BASE_URL` |
| `gemini` | Google Gemini `generateContent` | `GEMINI_API_KEY` or `GOOGLE_API_KEY` |

Optional shared vars:
- `IE_LLM_MODEL`
- `IE_LLM_API_KEY` (fallback key)

See `.env.example`.

## Examples

```bash
# Gemini
export IE_LLM_PROVIDER=gemini
export GEMINI_API_KEY=your_key
export IE_LLM_MODEL=gemini-2.0-flash
PYTHONPATH=../ie-runtime:. python3 -m agent.run_live --task-id live_benign_01

# OpenAI
export IE_LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-...
export IE_LLM_MODEL=gpt-4o-mini
PYTHONPATH=../ie-runtime:. python3 -m experiments.run_comparison

# Local Ollama
export IE_LLM_PROVIDER=local
export OPENAI_BASE_URL=http://127.0.0.1:11434/v1
export OPENAI_API_KEY=ollama
export IE_LLM_MODEL=llama3.1
PYTHONPATH=../ie-runtime:. python3 -m experiments.run_comparison
```

CLI still accepts `--provider` / `--model` and overrides env defaults.
