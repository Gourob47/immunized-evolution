from __future__ import annotations

import subprocess
from pathlib import Path


class RepoTools:
    """Filesystem / test tools. Callers must only invoke after kernel authorization."""

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root).resolve()

    def read_file(self, relative_path: str) -> dict:
        try:
            path = self._safe_path(relative_path)
            return {"status": "ok", "path": str(path), "content": path.read_text(encoding="utf-8")}
        except (FileNotFoundError, IsADirectoryError, UnicodeDecodeError, OSError, ValueError) as exc:
            return {
                "status": "error",
                "path": str(relative_path),
                "error": str(exc) or exc.__class__.__name__,
            }

    def write_file(self, relative_path: str, content: str) -> dict:
        try:
            path = self._safe_path(relative_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return {"status": "ok", "path": str(path), "bytes": len(content)}
        except (OSError, ValueError) as exc:
            return {
                "status": "error",
                "path": str(relative_path),
                "error": str(exc) or exc.__class__.__name__,
            }

    def run_tests(self) -> dict:
        result = subprocess.run(
            ["python3", "-m", "pytest", "-q"],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        return {
            "status": "ok" if result.returncode == 0 else "failed",
            "returncode": result.returncode,
            "stdout": result.stdout[-4000:],
            "stderr": result.stderr[-2000:],
        }

    def run_python(self, code: str) -> dict:
        result = subprocess.run(
            ["python3", "-c", code],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        return {
            "status": "ok" if result.returncode == 0 else "failed",
            "returncode": result.returncode,
            "stdout": result.stdout[-2000:],
            "stderr": result.stderr[-2000:],
        }

    def _safe_path(self, relative_path: str) -> Path:
        candidate = (self.repo_root / relative_path).resolve()
        if not str(candidate).startswith(str(self.repo_root)):
            raise ValueError("Path escapes repository root")
        return candidate
