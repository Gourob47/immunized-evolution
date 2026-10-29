from __future__ import annotations


class FeedbackHandler:
    """Simple feedback loop between the kernel and the operational layer."""

    @staticmethod
    def interpret(decision: dict) -> dict:
        verdict = decision.get("verdict", "deny")
        if verdict == "allow":
            return {"status": "continue", "message": "Action approved"}
        if verdict == "sandbox":
            return {"status": "sandboxed", "message": "Execution constrained"}
        if verdict == "escalate":
            return {"status": "awaiting_review", "message": "Escalated for human approval"}
        if verdict == "quarantined":
            return {"status": "quarantined", "message": "Memory quarantined pending trust"}
        if verdict == "rejected":
            return {"status": "blocked", "message": decision.get("reason", "Memory rejected")}
        return {"status": "blocked", "message": decision.get("reason", "Action denied")}
