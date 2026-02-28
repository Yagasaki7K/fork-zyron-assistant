import json

import zyron_linux.core.memory as memory


def test_save_and_load_long_term(tmp_path, monkeypatch):
    mem_file = tmp_path / "memory.json"
    monkeypatch.setattr(memory, "MEMORY_FILE", str(mem_file))

    memory.save_long_term("username", "ana")

    data = memory.load_long_term()
    assert data["username"] == "ana"


def test_track_preference_and_rank(tmp_path, monkeypatch):
    mem_file = tmp_path / "memory.json"
    monkeypatch.setattr(memory, "MEMORY_FILE", str(mem_file))

    memory.track_file_preference("pdf")
    memory.track_file_preference("xlsx")
    memory.track_file_preference("pdf")

    ranked = memory.get_preferred_file_types(limit=2)
    assert ranked == ["pdf", "xlsx"]

    raw = json.loads(mem_file.read_text())
    assert raw["file_preferences"]["total_searches"] == 3
