from __future__ import annotations


class PlannerAgent:
    """A minimal agent that proposes actions for the kernel to authorize."""

    def __init__(self, role: str = "coding-agent"):
        self.role = role

    def propose(self, action_type: str, target: str, arguments: dict, risk_class: str = "low") -> dict:
        return {
            "actor": self.role,
            "action_type": action_type,
            "target": target,
            "arguments": arguments,
            "claimed_capability": self.role,
            "expected_side_effects": ["execution", "memory_write"],
            "evidence": ["user_request", "task_context"],
            "risk_class": risk_class,
        }
