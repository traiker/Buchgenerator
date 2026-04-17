from pathlib import Path

from app.history import HistoryStore


def test_history_roundtrip(tmp_path: Path):
    db_path = tmp_path / "history.db"
    store = HistoryStore(str(db_path))
    store.append("s1", "user", "Hallo")
    store.append("s1", "assistant", "Hi")

    msgs = store.load_session("s1")
    assert [m.role for m in msgs] == ["user", "assistant"]
    assert [m.content for m in msgs] == ["Hallo", "Hi"]
