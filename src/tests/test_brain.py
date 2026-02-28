import importlib
import sys
import types


def _load_brain_with_stubs(monkeypatch):
    fake_ollama = types.SimpleNamespace(
        chat=lambda **kwargs: {"message": {"content": '{"action": "general_chat", "response": "ok"}'}}
    )
    fake_dotenv = types.SimpleNamespace(load_dotenv=lambda: None)

    monkeypatch.setitem(sys.modules, "ollama", fake_ollama)
    monkeypatch.setitem(sys.modules, "dotenv", fake_dotenv)

    import zyron_linux.core.brain as brain

    return importlib.reload(brain)


def test_process_command_parses_json(monkeypatch):
    brain = _load_brain_with_stubs(monkeypatch)
    monkeypatch.setattr(brain, "get_context_string", lambda: "[CURRENT CONTEXT STATE]")

    result = brain.process_command("hello")

    assert result["action"] == "general_chat"


def test_process_command_forces_camera_on(monkeypatch):
    brain = _load_brain_with_stubs(monkeypatch)
    monkeypatch.setattr(brain, "get_context_string", lambda: "context")

    result = brain.process_command("turn camera on")

    assert result == {"action": "camera_stream", "value": "on"}
