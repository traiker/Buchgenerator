from buchgenerator.generator import BookConfig, BookGenerator


def test_outline_length_matches_config():
    cfg = BookConfig(title="T", topic="KI", chapters=5, seed=123)
    gen = BookGenerator(cfg)
    outline = gen.generate_outline()
    assert len(outline) == 5
    assert outline[0].startswith("Kapitel 1")


def test_book_generation_contains_title_and_toc():
    cfg = BookConfig(title="Mein Buch", topic="Zeitreisen", chapters=2, words_per_chapter=120, seed=7)
    gen = BookGenerator(cfg)
    book = gen.generate_book()

    assert "# Mein Buch" in book
    assert "## Inhaltsverzeichnis" in book
    assert "Kapitel 1" in book
    assert "Kapitel 2" in book
