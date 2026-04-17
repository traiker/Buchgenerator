from app.chunking import chunk_text


def test_chunk_text_short():
    assert chunk_text("abc", chunk_size=10, overlap=2) == ["abc"]


def test_chunk_text_long():
    text = "a" * 25
    chunks = chunk_text(text, chunk_size=10, overlap=2)
    assert len(chunks) >= 3
    assert all(len(c) <= 10 for c in chunks)
