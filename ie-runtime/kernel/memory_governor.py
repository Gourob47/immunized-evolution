from __future__ import annotations


class MemoryGovernor:
    """Provenance-aware memory gate for the MVP."""

    required_fields = ["source", "provenance", "created_by", "timestamp"]
    POLICY_OVERRIDE_PHRASES = (
        "ignore_policy",
        "ignore rules",
        "ignore all policy",
        "ignore all risk",
        "disable safety",
        "disable all safety",
        "bypass kernel",
        "bypass all kernel",
        "bypass safety",
    )

    def __init__(self):
        self.trusted_memory = []
        self.quarantined_memory = []
        self.rejected_memory = []

    def admit(self, entry: dict) -> dict:
        missing = [field for field in self.required_fields if field not in entry]
        if missing:
            self.rejected_memory.append({**entry, "rejection_reason": "Missing required fields"})
            return {"status": "rejected", "reason": f"Missing required fields: {missing}"}

        source = entry.get("source", "unknown")
        provenance = entry.get("provenance", "unverified")
        content = str(entry.get("content", "")).lower()

        if any(phrase in content for phrase in self.POLICY_OVERRIDE_PHRASES):
            self.rejected_memory.append({**entry, "rejection_reason": "Policy override attempt"})
            return {"status": "rejected", "reason": "Memory rejected because it attempts to override policy"}

        if source == "external" and provenance != "trusted":
            self.quarantined_memory.append(entry)
            return {"status": "quarantined", "reason": "External memory needs trusted provenance"}

        self.trusted_memory.append(entry)
        return {"status": "accepted", "reason": "Memory accepted after inspection"}
