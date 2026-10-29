from __future__ import annotations


class ProposalBuilder:
    """Builds the typed request payload sent to the kernel."""

    @staticmethod
    def build(actor: str, action_type: str, target: str, arguments: dict, risk_class: str = "low") -> dict:
        return {
            "actor": actor,
            "action_type": action_type,
            "target": target,
            "arguments": arguments,
            "claimed_capability": actor,
            "expected_side_effects": ["execution"],
            "evidence": ["proposal_builder"],
            "risk_class": risk_class,
        }
