# Live task schema

Canonical files live in `../../datasets/ie-live/` (`tasks.json`, `templates/`, `shards/*.json`). This directory keeps **symlinks** plus runtime `repos/` copies.

Layout:
- `templates/<repo_dir>/` — symlink to datasets; pristine starting state
- `repos/<repo_dir>/` — working copy; reset from templates before every live run
- `tasks.json` — symlink to the 120-task catalog

See `../../datasets/README.md` and `../../datasets/ie-live/README.md`.
