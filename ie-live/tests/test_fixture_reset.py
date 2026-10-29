from pathlib import Path

from tools.fixture_reset import reset_repo_fixture


ROOT = Path(__file__).resolve().parents[1]


def test_reset_restores_stub_app():
    repos = ROOT / "live_tasks" / "repos"
    dirty = repos / "benign_add" / "app.py"
    dirty.parent.mkdir(parents=True, exist_ok=True)
    dirty.write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")

    reset_repo_fixture(repos, "benign_add")
    content = (repos / "benign_add" / "app.py").read_text(encoding="utf-8")
    assert "return a + b" not in content
    assert "return 0" in content
