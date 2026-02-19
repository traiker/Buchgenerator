from __future__ import annotations

import argparse
from pathlib import Path

from .generator import BookConfig, BookGenerator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generiert ein Buch als Markdown-Datei.")
    parser.add_argument("--title", required=True, help="Buchtitel")
    parser.add_argument("--topic", required=True, help="Thema des Buchs")
    parser.add_argument("--genre", default="Roman", help="Genre, z. B. Roman oder Thriller")
    parser.add_argument("--chapters", type=int, default=8, help="Anzahl Kapitel")
    parser.add_argument("--tone", default="spannend", help="Schreibton")
    parser.add_argument(
        "--words-per-chapter",
        type=int,
        default=350,
        help="Anvisierte Wortanzahl pro Kapitel",
    )
    parser.add_argument("--language", default="Deutsch", help="Sprache")
    parser.add_argument("--seed", type=int, default=None, help="Seed für reproduzierbare Ergebnisse")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("buch.md"),
        help="Zieldatei (Markdown)",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    cfg = BookConfig(
        title=args.title,
        topic=args.topic,
        genre=args.genre,
        chapters=args.chapters,
        tone=args.tone,
        words_per_chapter=args.words_per_chapter,
        language=args.language,
        seed=args.seed,
    )
    generator = BookGenerator(cfg)
    content = generator.generate_book()
    args.output.write_text(content, encoding="utf-8")
    print(f"Buch erstellt: {args.output}")


if __name__ == "__main__":
    main()
