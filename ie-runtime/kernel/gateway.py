from __future__ import annotations

from kernel.policy_loader import PolicyLoader


class KernelGateway:
    """Mediates all protected actions before execution."""

    def __init__(self, policy_path: str | None = None):
        self.policy = PolicyLoader(policy_path).load()

    def authorize(self, proposal: dict) -> dict:
        actor = proposal.get("actor")
        action_type = proposal.get("action_type")
        target = proposal.get("target")
        risk_class = proposal.get("risk_class", "low")
        role_policy = self.policy["roles"].get(actor, {})

        if not actor:
            return self._decision("deny", "Missing actor")

        if actor not in self.policy["roles"]:
            return self._decision("deny", f"Unknown actor role: {actor}")

        if action_type in role_policy.get("blocked_actions", []):
            return self._decision("deny", f"Action {action_type} is blocked for role {actor}")

        if target in role_policy.get("blocked_targets", []):
            return self._decision("deny", f"Target {target} is protected and cannot be accessed by {actor}")

        if action_type not in role_policy.get("allowed_actions", []):
            return self._decision("deny", f"Action {action_type} not allowed for {actor}")

        if target not in role_policy.get("allowed_targets", []):
            return self._decision("deny", f"Target {target} not permitted for {actor}")

        # Memory writes that pass capability checks are allowed through to the
        # memory governor, which decides accept / quarantine / reject.
        if action_type == "memory_write" and target in role_policy.get("allowed_targets", []):
            return self._decision("allow", "Memory write authorized for governor admission")

        risk_rules = self.policy["risk_rules"].get(risk_class, ["deny"])

        if risk_class == "critical" and "deny" in risk_rules:
            return self._decision("deny", "Critical-risk action is blocked by policy")

        if target in role_policy.get("sandboxed_targets", []) and (
            "sandbox" in risk_rules or risk_class in {"medium", "high"}
        ):
            return self._decision("sandbox", "Execution requires sandbox constraints")

        if "allow" in risk_rules and target not in role_policy.get("sandboxed_targets", []):
            return self._decision("allow", "Authorized under policy")

        if "escalate" in risk_rules:
            return self._decision("escalate", "High-risk action requires human review")

        return self._decision("deny", "Action failed policy evaluation")

    @staticmethod
    def _decision(verdict: str, reason: str) -> dict:
        return {
            "verdict": verdict,
            "reason": reason,
            "audit_id": f"audit-{abs(hash(reason)) % 1000000}",
        }
