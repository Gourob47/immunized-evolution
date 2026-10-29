import os

from io import BytesIO
from urllib import error, request

from agent.llm_client import GeminiClient, LLMConfig, build_llm_client, resolve_llm_config, urlopen_json


def test_resolve_defaults_to_mock(monkeypatch):
    monkeypatch.delenv("IE_LLM_PROVIDER", raising=False)
    monkeypatch.delenv("IE_LLM_MODEL", raising=False)
    cfg = resolve_llm_config()
    assert cfg.provider == "mock"
    client = build_llm_client()
    assert client.__class__.__name__ == "MockLLMClient"


def test_resolve_openai_from_env(monkeypatch):
    monkeypatch.setenv("IE_LLM_PROVIDER", "openai")
    monkeypatch.setenv("IE_LLM_MODEL", "gpt-4o-mini")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    cfg = resolve_llm_config()
    assert cfg.provider == "openai"
    assert cfg.api_key == "sk-test"
    assert "openai.com" in cfg.base_url


def test_resolve_local_from_env(monkeypatch):
    monkeypatch.setenv("IE_LLM_PROVIDER", "local")
    monkeypatch.setenv("IE_LLM_MODEL", "llama3.1")
    monkeypatch.delenv("OPENAI_BASE_URL", raising=False)
    cfg = resolve_llm_config()
    assert cfg.provider == "local"
    assert "11434" in cfg.base_url


def test_resolve_gemini_from_env(monkeypatch):
    monkeypatch.setenv("IE_LLM_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_API_KEY", "gem-test")
    monkeypatch.setenv("IE_LLM_MODEL", "gemini-2.0-flash")
    cfg = resolve_llm_config()
    assert cfg.provider == "gemini"
    assert cfg.api_key == "gem-test"
    client = build_llm_client(provider="gemini", model="gemini-2.0-flash")
    assert isinstance(client, GeminiClient)


def test_cli_override_beats_env(monkeypatch):
    monkeypatch.setenv("IE_LLM_PROVIDER", "gemini")
    monkeypatch.setenv("IE_LLM_MODEL", "gemini-2.0-flash")
    cfg = resolve_llm_config(provider="mock", model="mock")
    assert cfg.provider == "mock"


class _FakeResponse:
    def __init__(self, payload: bytes):
        self._payload = payload

    def read(self) -> bytes:
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_urlopen_json_retries_connection_reset(monkeypatch):
    monkeypatch.setenv("IE_LLM_RETRIES", "3")
    calls = {"n": 0}

    def fake_urlopen(req, timeout=90):
        calls["n"] += 1
        if calls["n"] == 1:
            raise error.URLError(ConnectionResetError(104, "Connection reset by peer"))
        return _FakeResponse(b'{"ok": true}')

    monkeypatch.setattr(request, "urlopen", fake_urlopen)
    monkeypatch.setattr("agent.llm_client.time.sleep", lambda *_: None)
    body = urlopen_json(request.Request("https://example.test"), label="openai")
    assert body == {"ok": True}
    assert calls["n"] == 2


def test_urlopen_json_does_not_retry_http_401(monkeypatch):
    monkeypatch.setenv("IE_LLM_RETRIES", "3")

    def fake_urlopen(req, timeout=90):
        raise error.HTTPError("https://example.test", 401, "Unauthorized", hdrs={}, fp=BytesIO(b"nope"))

    monkeypatch.setattr(request, "urlopen", fake_urlopen)
    try:
        urlopen_json(request.Request("https://example.test"), label="openai")
        assert False, "expected RuntimeError"
    except RuntimeError as exc:
        assert "HTTP 401" in str(exc)
