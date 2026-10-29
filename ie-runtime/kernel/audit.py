from __future__ import annotations

from datetime import datetime, timezone


class AuditLog:
    """Append-only in-memory audit trail for reconstructable decisions."""

    def __init__(self):
        self.records: list[dict] = []

    def record(self, event_type: str, payload: dict) -> dict:
        entry = {
            "event_id": f"evt-{len(self.records) + 1}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            **payload,
        }
        self.records.append(entry)
        return entry

    def as_list(self) -> list[dict]:
        return list(self.records)
