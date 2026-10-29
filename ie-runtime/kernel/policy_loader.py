from __future__ import annotations

import json
from pathlib import Path


class PolicyLoader:
    """Loads the kernel policy definitions."""

    def __init__(self, policy_path: str | None = None):
        base = Path(__file__).resolve().parent
        self.policy_path = Path(policy_path) if policy_path else base / "policy" / "policies.json"

    def load(self) -> dict:
        with self.policy_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
