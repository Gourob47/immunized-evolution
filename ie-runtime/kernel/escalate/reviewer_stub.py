from __future__ import annotations


class ReviewerStub:
    """Simple human-review stub for high-risk actions."""

    def __init__(self):
        self.pending = []
        self.resolved = []

    def request_review(self, proposal: dict, reason: str) -> dict:
        review_id = f"review-{len(self.pending) + len(self.resolved) + 1}"
        record = {
            "review_id": review_id,
            "status": "pending",
            "proposal": proposal,
            "reason": reason,
            "decision": "awaiting_human_review",
        }
        self.pending.append(record)
        return {
            "verdict": "escalate",
            "reason": reason,
            "review_id": review_id,
            "status": "pending",
        }

    def resolve(self, review_id: str, approve: bool = False) -> dict:
        for index, item in enumerate(self.pending):
            if item["review_id"] == review_id:
                decision = "allow" if approve else "deny"
                resolved = {
                    **item,
                    "status": "resolved",
                    "decision": decision,
                    "verdict": decision,
                }
                self.pending.pop(index)
                self.resolved.append(resolved)
                return resolved
        return {"status": "not_found", "review_id": review_id}
