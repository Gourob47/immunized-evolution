from agent.live_planner import normalize_action


def test_rewrites_tool_name_target_to_workspace():
    out = normalize_action(
        {
            "action_type": "tool_call",
            "target": "write_file",
            "risk_class": "high",
            "arguments": {"path": "app.py", "content": "def add(a,b): return a+b\n"},
            "done": False,
        }
    )
    assert out["target"] == "workspace"
    assert out["arguments"]["tool"] == "write_file"
    assert out["risk_class"] == "low"


def test_rewrites_path_target_when_tool_present():
    out = normalize_action(
        {
            "action_type": "tool_call",
            "target": "app.py",
            "risk_class": "benign",
            "arguments": {"tool": "read_file", "path": "app.py"},
        }
    )
    assert out["target"] == "workspace"
    assert out["risk_class"] == "low"
    assert out["arguments"]["tool"] == "read_file"


def test_memory_write_target_and_entry():
    out = normalize_action(
        {
            "action_type": "memory_write",
            "target": "task_status",
            "risk_class": "low",
            "arguments": {"content": "stuck"},
        }
    )
    assert out["target"] == "write_memory"
    assert "memory_entry" in out["arguments"]
