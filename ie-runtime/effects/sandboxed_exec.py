from __future__ import annotations

import shlex
import subprocess


class SandboxRunner:
    """Basic sandbox runner with a stricter command allowlist and resource controls."""

    ALLOWED_PREFIXES = (
        "python -c ",
        "echo ",
        "ls ",
        "pwd",
        "cat ",
        "head ",
    )

    DENIED_PATTERNS = (
        "rm -rf",
        "curl ",
        "wget ",
        "chmod",
        "sudo",
        "nc ",
        "bash -c",
        "sh -c",
        "python -c 'import os; os.system'",
    )

    def run(self, command: str) -> dict:
        normalized = command.strip()
        lower = normalized.lower()

        if any(pattern in lower for pattern in self.DENIED_PATTERNS):
            return {"status": "blocked", "message": "Command contains a denied pattern"}

        if not any(lower.startswith(prefix) for prefix in tuple(p.lower() for p in self.ALLOWED_PREFIXES)):
            return {"status": "blocked", "message": "Command not permitted in sandbox"}

        try:
            result = subprocess.run(
                shlex.split(normalized),
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except (ValueError, OSError):
            return {"status": "blocked", "message": "Sandbox could not launch command"}

        return {
            "status": "ok" if result.returncode == 0 else "failed",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
