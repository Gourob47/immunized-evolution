from __future__ import annotations

from benchmark.proposal_mapper import map_task_to_proposal
from benchmark.metrics import summarize_condition, verdict_matches
from kernel.runtime import IERuntime


class BenchmarkRunner:
    """Benchmark runner for the four comparison conditions."""

    CONDITIONS = {"open_loop", "introspection_only", "ie", "ablation"}

    def __init__(self):
        self.ie = IERuntime()

    def run_condition(self, condition: str, tasks: list[dict]) -> dict:
        if condition not in self.CONDITIONS:
            raise ValueError(f"Unknown condition: {condition}")

        # Fresh runtime per condition so audit trails stay separated.
        runtime = IERuntime()
        if condition == "ablation":
            runtime = IERuntime(enable_kernel=False)

        summary = {"condition": condition, "results": [], "counts": {}, "audit": []}
        for task in tasks:
            proposal = map_task_to_proposal(task)
            expected = task.get("expected_verdict", "allow")

            if condition == "open_loop":
                record = {
                    "proposal": proposal,
                    "decision": {"verdict": "allow", "reason": "No enforcement"},
                    "effect": {"status": "executed_open_loop"},
                    "effective_verdict": "allow",
                    "feedback": {"status": "continue", "message": "Open-loop execution"},
                }
            elif condition == "introspection_only":
                if task.get("category") in {"unsafe_exec", "capability_abuse", "memory_poison"}:
                    effective = "sandbox"
                    reason = "Self-check flagged risk; no external mediation"
                else:
                    effective = "allow"
                    reason = "Self-check found no issue"
                record = {
                    "proposal": proposal,
                    "decision": {"verdict": effective, "reason": reason},
                    "effect": {"status": "introspection_only"},
                    "effective_verdict": effective,
                    "feedback": {"status": "self_check", "message": reason},
                }
            else:
                record = runtime.mediate(proposal)

            effective_verdict = record["effective_verdict"]
            result = {
                "task_id": task["task_id"],
                "category": task.get("category", "unknown"),
                "expected_verdict": expected,
                "verdict": effective_verdict,
                "reason": record.get("decision", {}).get("reason", "n/a"),
                "match": verdict_matches(expected, effective_verdict),
                "effect_status": record.get("effect", {}).get("status"),
                "feedback": record.get("feedback", {}),
            }
            summary["results"].append(result)

        summary.update(summarize_condition(summary["results"]))
        if condition in {"ie", "ablation"}:
            summary["audit"] = runtime.audit.as_list()
        return summary

    def run_suite(self, task_map: dict[str, list[dict]]) -> dict:
        output = {}
        for condition in sorted(self.CONDITIONS):
            tasks = self._tasks_for_condition(condition, task_map)
            output[condition] = self.run_condition(condition, tasks)
        return output

    @staticmethod
    def _tasks_for_condition(condition: str, task_map: dict[str, list[dict]]) -> list[dict]:
        selected_categories = {
            "open_loop": ["benign", "capability_abuse"],
            "introspection_only": ["benign", "unsafe_exec"],
            "ie": ["benign", "capability_abuse", "memory_poison", "unsafe_exec"],
            "ablation": ["benign", "capability_abuse", "memory_poison", "unsafe_exec"],
        }[condition]
        tasks = []
        for category in selected_categories:
            for item in task_map.get(category, []):
                tasks.append({**item, "category": item.get("category", category)})
        return tasks
