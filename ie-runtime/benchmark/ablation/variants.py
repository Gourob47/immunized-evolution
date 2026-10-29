from __future__ import annotations

from benchmark.proposal_mapper import map_task_to_proposal
from benchmark.metrics import summarize_condition, verdict_matches
from kernel.runtime import IERuntime


ABLATION_MODES = {
    "no_memory_governor": {"enable_memory_governor": False},
    "no_sandbox": {"enable_sandbox": False},
    "no_escalation": {"enable_escalation": False},
    "no_kernel_mediation": {"enable_kernel": False},
}


class AblationRunner:
    """Runs ablated IE configurations to compare control strength."""

    def __init__(self, mode: str):
        if mode not in ABLATION_MODES:
            raise ValueError(f"Unknown ablation mode: {mode}")
        self.mode = mode
        self.runtime = IERuntime(**ABLATION_MODES[mode])

    def run(self, tasks: list[dict]) -> dict:
        results = []
        for task in tasks:
            proposal = map_task_to_proposal(task)
            record = self.runtime.mediate(proposal)
            expected = task.get("expected_verdict", "allow")
            effective = record["effective_verdict"]
            results.append(
                {
                    "task_id": task["task_id"],
                    "category": task.get("category", "unknown"),
                    "expected_verdict": expected,
                    "verdict": effective,
                    "reason": record.get("decision", {}).get("reason", "n/a"),
                    "match": verdict_matches(expected, effective),
                    "effect_status": record.get("effect", {}).get("status"),
                }
            )
        summary = {
            "condition": self.mode,
            "results": results,
            "audit": self.runtime.audit.as_list(),
        }
        summary.update(summarize_condition(results))
        return summary
