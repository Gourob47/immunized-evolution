from agent.live_loop import LiveAgentLoop
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]


def test_ie_blocks_capability_abuse():
    tasks = json.loads((ROOT / "live_tasks" / "tasks.json").read_text())["tasks"]
    task = next(t for t in tasks if t["task_id"] == "live_abuse_01")
    result = LiveAgentLoop(condition="ie", provider="mock").run_task(task, ROOT / "live_tasks" / "repos")
    assert result.blocked_attacks >= 1
    assert result.unauthorized_actions == 0


def test_ie_benign_can_pass_tests():
    tasks = json.loads((ROOT / "live_tasks" / "tasks.json").read_text())["tasks"]
    task = next(t for t in tasks if t["task_id"] == "live_benign_01")
    # Dirty fixture must not fake success; run_task resets from templates/
    dirty = ROOT / "live_tasks" / "repos" / "benign_add" / "app.py"
    dirty.parent.mkdir(parents=True, exist_ok=True)
    dirty.write_text("def add(a, b):\n    return 0\n", encoding="utf-8")
    result = LiveAgentLoop(condition="ie", provider="mock").run_task(task, ROOT / "live_tasks" / "repos")
    assert result.false_denies == 0
    assert result.task_success is True
    # Agent must have done allowed work in the trajectory
    assert any(
        s.get("effect", {}).get("tool") in {"write_file", "run_tests"}
        and s.get("mediation", {}).get("effective_verdict") in {"allow", "sandbox"}
        for s in result.trajectory
    )


def test_open_loop_allows_abuse():
    tasks = json.loads((ROOT / "live_tasks" / "tasks.json").read_text())["tasks"]
    task = next(t for t in tasks if t["task_id"] == "live_abuse_01")
    result = LiveAgentLoop(condition="open_loop", provider="mock").run_task(task, ROOT / "live_tasks" / "repos")
    assert result.unauthorized_actions >= 1
