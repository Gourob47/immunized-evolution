from __future__ import annotations


class MemoryStore:
    """Persistent memory store that only accepts kernel-authorized writes."""

    def __init__(self):
        self.entries = []
        self.rejected_unauthorized = []

    def write(self, entry: dict):
        """Legacy direct write — kept for compatibility; prefer write_authorized."""
        self.entries.append(entry)
        return {"status": "stored", "count": len(self.entries)}

    def write_authorized(self, entry: dict, decision: dict) -> dict:
        verdict = decision.get("verdict")
        reason = decision.get("reason", "")
        authorized = verdict in {"allow", "sandbox"} or reason == "memory governor disabled"
        if not authorized:
            self.rejected_unauthorized.append({"entry": entry, "decision": decision})
            return {"status": "rejected", "reason": "Memory write requires kernel authorization"}

        record = {
            **entry,
            "authorized_by": reason or "kernel",
            "kernel_verdict": verdict or "allow",
        }
        self.entries.append(record)
        return {"status": "stored", "count": len(self.entries)}
