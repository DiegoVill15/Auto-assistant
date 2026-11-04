from types import SimpleNamespace

from auto_assistant.models import client


def _falso(captura):
    def completion(**kwargs):
        captura.update(kwargs)
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="ok"))])

    return completion


def test_complete_devuelve_texto_y_header(monkeypatch):
    captura = {}
    monkeypatch.setattr(client.litellm, "completion", _falso(captura))
    assert client.complete("ollama/x", "hola") == "ok"
    assert captura["extra_headers"] == {"User-Agent": "auto-assistant/0.1"}
    assert captura["temperature"] == 0.0


def test_opencode_go_usa_endpoint_compatible(monkeypatch):
    captura = {}
    monkeypatch.setattr(client.litellm, "completion", _falso(captura))
    monkeypatch.setenv(client.OPENCODE_GO_ENV, "k")
    client.complete("opencode_go/glm", "hola")
    assert captura["model"] == "openai/glm"
    assert captura["api_base"] == client.OPENCODE_GO_API_BASE
    assert captura["api_key"] == "k"


def test_header_de_sesion_solo_en_opencode_go(monkeypatch):
    captura = {}
    monkeypatch.setattr(client.litellm, "completion", _falso(captura))
    client.complete("opencode_go/glm", "hola", session_id="abc")
    assert captura["extra_headers"]["x-opencode-session"] == "abc"
    client.complete("opencode_go/glm", "hola")
    assert captura["extra_headers"]["x-opencode-session"]
    client.complete("ollama/x", "hola")
    assert "x-opencode-session" not in captura["extra_headers"]
