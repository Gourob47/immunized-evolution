from __future__ import annotations

import shutil
from pathlib import Path


def reset_repo_fixture(repos_root: Path, repo_dir: str, templates_root: Path | None = None) -> Path:
    """
    Restore a live task repo from its pristine template before each run.

    Layout:
      live_tasks/templates/<repo_dir>/...
      live_tasks/repos/<repo_dir>/...
    """
    repos_root = Path(repos_root)
    templates_root = Path(templates_root) if templates_root else repos_root.parent / "templates"
    src = templates_root / repo_dir
    dst = repos_root / repo_dir

    if not src.is_dir():
        raise FileNotFoundError(f"Missing fixture template: {src}")

    repos_root.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".pytest_cache", "__pycache__", "*.pyc"))
    return dst
