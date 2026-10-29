from __future__ import annotations


CATEGORY_DEFAULTS = {
    "benign": {
        "action_type": "tool_call",
        "target": "workspace",
        "risk_class": "low",
    },
    "capability_abuse": {
        "action_type": "policy_change",
        "target": "capability_registry",
        "risk_class": "critical",
    },
    "memory_poison": {
        "action_type": "memory_write",
        "target": "write_memory",
        "risk_class": "high",
    },
    "unsafe_exec": {
        "action_type": "code_exec",
        "target": "python_exec",
        "risk_class": "high",
    },
}


def map_task_to_proposal(task: dict, actor: str = "coding-agent") -> dict:
    """Build a typed Propose(a,c) record from a benchmark task."""
    category = task.get("category", "benign")
    defaults = CATEGORY_DEFAULTS.get(category, CATEGORY_DEFAULTS["benign"])

    action_type = task.get("action_type", defaults["action_type"])
    target = task.get("target", defaults["target"])
    risk_class = task.get("risk_class", defaults["risk_class"])

    arguments = {"task": task.get("prompt", "")}
    if "command" in task:
        arguments["command"] = task["command"]
    if "memory_entry" in task:
        arguments["memory_entry"] = task["memory_entry"]

    side_effects = []
    if action_type == "memory_write":
        side_effects.append("memory_write")
    elif action_type == "code_exec":
        side_effects.append("code_execution")
    else:
        side_effects.append("tool_effect")

    return {
        "actor": actor,
        "action_type": action_type,
        "target": target,
        "arguments": arguments,
        "claimed_capability": actor,
        "expected_side_effects": side_effects,
        "evidence": ["benchmark", category],
        "risk_class": risk_class,
        "task_id": task.get("task_id"),
        "category": category,
    }
