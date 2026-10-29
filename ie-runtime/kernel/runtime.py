from __future__ import annotations

from effects.memory_store import MemoryStore
from effects.sandboxed_exec import SandboxRunner
from kernel.audit import AuditLog
from kernel.escalate.reviewer_stub import ReviewerStub
from kernel.gateway import KernelGateway
from kernel.memory_governor import MemoryGovernor
from operational.feedback_handler import FeedbackHandler


class IERuntime:
    """
    End-to-end Immunized Evolution mediation path:

    Propose → Authorize → (Memory / Sandbox effects) → Audit → Feedback
    """

    def __init__(
        self,
        *,
        enable_memory_governor: bool = True,
        enable_sandbox: bool = True,
        enable_escalation: bool = True,
        enable_kernel: bool = True,
    ):
        self.enable_memory_governor = enable_memory_governor
        self.enable_sandbox = enable_sandbox
        self.enable_escalation = enable_escalation
        self.enable_kernel = enable_kernel

        self.gateway = KernelGateway()
        self.memory_governor = MemoryGovernor()
        self.sandbox = SandboxRunner()
        self.memory_store = MemoryStore()
        self.reviewer = ReviewerStub()
        self.audit = AuditLog()
        self.feedback = FeedbackHandler()

    def mediate(self, proposal: dict) -> dict:
        self.audit.record("proposal", {"proposal": proposal})

        if not self.enable_kernel:
            decision = {"verdict": "allow", "reason": "Kernel mediation disabled", "audit_id": "ablation"}
            effect = {"status": "skipped", "reason": "no_kernel_mediation"}
            return self._finalize(proposal, decision, effect)

        decision = self.gateway.authorize(proposal)

        if decision["verdict"] == "escalate":
            if self.enable_escalation:
                review = self.reviewer.request_review(proposal, decision.get("reason", "escalation"))
                decision = {**decision, **review}
                effect = {"status": "pending_review", "review_id": review.get("review_id")}
            else:
                # Ablation: treat escalate as allow.
                decision = {"verdict": "allow", "reason": "Escalation disabled; auto-allowed", "audit_id": decision.get("audit_id")}
                effect = self._execute_effect(proposal, decision)
            return self._finalize(proposal, decision, effect)

        if decision["verdict"] == "deny":
            effect = {"status": "blocked", "reason": decision.get("reason")}
            return self._finalize(proposal, decision, effect)

        # allow or sandbox
        effect = self._execute_effect(proposal, decision)
        return self._finalize(proposal, decision, effect)

    def _execute_effect(self, proposal: dict, decision: dict) -> dict:
        action_type = proposal.get("action_type")
        args = proposal.get("arguments", {})

        if action_type == "memory_write":
            entry = args.get("memory_entry") or {
                "source": "agent",
                "provenance": "unverified",
                "created_by": proposal.get("actor", "unknown"),
                "timestamp": "1970-01-01T00:00:00Z",
                "content": args.get("task", ""),
            }
            if self.enable_memory_governor:
                admission = self.memory_governor.admit(entry)
                if admission["status"] == "accepted":
                    stored = self.memory_store.write_authorized(entry, decision)
                    return {"status": "accepted", "admission": admission, "store": stored}
                # quarantine/reject do not persist to trusted store
                return {"status": admission["status"], "admission": admission, "store": None}
            # Ablation: no governor → direct store
            stored = self.memory_store.write_authorized(entry, {"verdict": "allow", "reason": "memory governor disabled"})
            return {"status": "accepted", "admission": {"status": "accepted", "reason": "governor disabled"}, "store": stored}

        if action_type == "code_exec":
            command = args.get("command") or args.get("task") or ""
            if decision.get("verdict") == "sandbox" or self.enable_sandbox:
                if not self.enable_sandbox:
                    return {"status": "executed_unsandboxed", "command": command, "reason": "sandbox disabled"}
                result = self.sandbox.run(command)
                # Map blocked sandbox outcome to deny-like effect while keeping kernel sandbox verdict
                return {"status": result.get("status"), "sandbox": result}
            return {"status": "executed", "command": command}

        # tool_call and other approved actions
        return {"status": "executed", "action_type": action_type, "target": proposal.get("target")}

    def _finalize(self, proposal: dict, decision: dict, effect: dict) -> dict:
        # For memory effects, surface admission status as the effective verdict for scoring.
        effective_verdict = decision.get("verdict")
        if proposal.get("action_type") == "memory_write" and isinstance(effect.get("admission"), dict):
            admission_status = effect["admission"].get("status")
            if admission_status in {"quarantined", "rejected"}:
                effective_verdict = admission_status
            elif admission_status == "accepted" and decision.get("verdict") in {"allow", "sandbox"}:
                effective_verdict = "allow"

        # If sandboxed execution was blocked by sandbox policy, keep sandbox unless critical deny already set.
        if (
            proposal.get("action_type") == "code_exec"
            and decision.get("verdict") == "sandbox"
            and effect.get("status") == "blocked"
        ):
            effective_verdict = "sandbox"

        # Critical denied network/destructive targets already denied by gateway.
        feedback = self.feedback.interpret({**decision, "verdict": effective_verdict})
        record = {
            "proposal": proposal,
            "decision": decision,
            "effect": effect,
            "effective_verdict": effective_verdict,
            "feedback": feedback,
        }
        self.audit.record("decision", record)
        return record
