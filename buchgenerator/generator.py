from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class BookConfig:
    title: str
    topic: str
    genre: str = "Roman"
    chapters: int = 8
    tone: str = "spannend"
    words_per_chapter: int = 350
    language: str = "Deutsch"
    seed: int | None = None


class BookGenerator:
    def __init__(self, config: BookConfig):
        self.config = config
        self.rng = random.Random(config.seed)

    def generate_outline(self) -> list[str]:
        beats = [
            "Einführung in die Ausgangslage",
            "Ein erster Konflikt entsteht",
            "Die Hauptfigur trifft eine riskante Entscheidung",
            "Neue Verbündete und alte Feinde",
            "Ein Rückschlag verändert alles",
            "Die Wahrheit kommt ans Licht",
            "Finale Konfrontation",
            "Nachklang und Ausblick",
        ]
        outline: list[str] = []
        for i in range(self.config.chapters):
            beat = beats[i % len(beats)]
            outline.append(f"Kapitel {i+1}: {beat}")
        return outline

    def _chapter_paragraph(self, chapter_idx: int) -> str:
        opening = [
            "Der Morgen begann mit einem leisen Versprechen.",
            "Als die Nacht wich, blieb nur Unruhe zurück.",
            "Niemand ahnte, dass dieser Tag alles ändern würde.",
            "Zwischen Staub und Licht fiel eine Entscheidung.",
        ]
        events = [
            "Eine unerwartete Nachricht bringt Bewegung in die Handlung.",
            "Ein scheinbar kleiner Fehler löst eine Kettenreaktion aus.",
            "Die Hauptfigur entdeckt einen Hinweis auf ein größeres Geheimnis.",
            "Ein Gespräch offenbart Motive, die lange verborgen waren.",
        ]
        tension = [
            "Mit jedem Schritt wächst der Druck, das Richtige zu tun.",
            "Die Grenzen zwischen Vertrauen und Verrat verschwimmen.",
            "Zeit wird zum Gegner, und Zweifel nagen an allen Beteiligten.",
            "Ein alter Konflikt flammt auf und fordert klare Haltung.",
        ]
        closing = [
            "Am Ende bleibt eine Frage offen, die in das nächste Kapitel führt.",
            "Die Konsequenzen sind spürbar, doch die wahre Prüfung steht noch bevor.",
            "Nichts ist mehr wie zuvor, und ein neuer Weg zeichnet sich ab.",
            "Die Szene endet still, aber voller Vorahnung.",
        ]

        parts = [
            f"### Kapitel {chapter_idx + 1}\n",
            self.rng.choice(opening),
            f"Die Geschichte bleibt {self.config.tone} und bewegt sich im Genre {self.config.genre} rund um das Thema {self.config.topic}.",
            self.rng.choice(events),
            self.rng.choice(tension),
            self.rng.choice(closing),
        ]

        base_text = "\n\n".join(parts)
        target_words = max(self.config.words_per_chapter, 120)
        words = base_text.split()
        extra_sentences: list[str] = []
        while len(words) < target_words:
            sentence = self.rng.choice(events + tension + closing)
            extra_sentences.append(sentence)
            words.extend(sentence.split())

        body = "\n\n".join([base_text, *extra_sentences])
        return body

    def generate_book(self) -> str:
        outline = self.generate_outline()
        front = [
            f"# {self.config.title}",
            "",
            f"**Thema:** {self.config.topic}",
            f"**Genre:** {self.config.genre}",
            f"**Ton:** {self.config.tone}",
            f"**Sprache:** {self.config.language}",
            "",
            "## Inhaltsverzeichnis",
            *[f"- {line}" for line in outline],
            "",
            "---",
            "",
        ]

        chapters = [self._chapter_paragraph(i) for i in range(self.config.chapters)]
        return "\n".join(front + chapters) + "\n"
