#!/usr/bin/env python3
"""Ein einfacher Buchgenerator auf Basis von Vorlagen.

Der Generator erzeugt ein kleines "Buch" mit Titel, Kapitelüberschriften
und Absätzen. Inhalte werden aus kombinierbaren Textbausteinen erstellt.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from pathlib import Path


ADJEKTIVE = [
    "vergessenen",
    "leuchtenden",
    "stillen",
    "mysteriösen",
    "wilden",
    "verbotenen",
    "goldenen",
]

ORTE = [
    "Wäldern",
    "Bergen",
    "Gassen",
    "Inseln",
    "Ruinen",
    "Tälern",
    "Sternenfeldern",
]

HELDEN = [
    "Alina",
    "Jonas",
    "Mira",
    "Levin",
    "Nora",
    "Taro",
    "Elia",
]

ZIELE = [
    "das verlorene Manuskript zu finden",
    "die Wahrheit über ein altes Versprechen zu enthüllen",
    "einen gefährlichen Schwur zu brechen",
    "den letzten Funken Hoffnung zu retten",
    "ein uraltes Rätsel zu lösen",
]

HINDERNISSE = [
    "ein Sturm aus Erinnerungen", 
    "ein Rat, der nur in Rätseln spricht", 
    "eine Karte mit fehlenden Seiten", 
    "eine Schattenfigur ohne Namen", 
    "eine Tür, die nur bei Mondlicht erscheint", 
]

WENDUNGEN = [
    "Die größte Gefahr entpuppt sich als unerwarteter Verbündeter.",
    "Ein scheinbar bedeutungsloser Brief verändert den gesamten Plan.",
    "Ein Geheimnis aus der Vergangenheit lässt alles in neuem Licht erscheinen.",
    "Die Heldin erkennt, dass die Suche zugleich eine Heimkehr ist.",
    "Ein alter Feind bietet Hilfe – zu einem hohen Preis.",
]

SCHLUESSE = [
    "Am Ende bleibt nicht Gewissheit, sondern Mut für den nächsten Schritt.",
    "Die Welt ist nicht gerettet, aber sie ist wieder voller Möglichkeiten.",
    "Was verloren schien, kehrt in veränderter Form zurück.",
    "Die Antwort war nie ein Ort, sondern eine Entscheidung.",
    "Und während die Nacht endet, beginnt eine neue Geschichte.",
]


@dataclass
class BuchKonfiguration:
    titel: str | None
    kapitel: int = 5
    abschnitte_pro_kapitel: int = 3
    seed: int | None = None


class BuchGenerator:
    def __init__(self, config: BuchKonfiguration):
        self.config = config
        self.zufall = random.Random(config.seed)

    def generiere_titel(self) -> str:
        if self.config.titel:
            return self.config.titel
        return f"Die Chronik der {self.zufall.choice(ADJEKTIVE)} {self.zufall.choice(ORTE)}"

    def generiere_kapitelueberschrift(self, nummer: int) -> str:
        held = self.zufall.choice(HELDEN)
        ziel = self.zufall.choice(ZIELE)
        return f"Kapitel {nummer}: {held} beschließt, {ziel}"

    def generiere_absatz(self) -> str:
        held = self.zufall.choice(HELDEN)
        ort = self.zufall.choice(ORTE)
        hindernis = self.zufall.choice(HINDERNISSE)
        wendung = self.zufall.choice(WENDUNGEN)
        return (
            f"{held} reist durch die {ort} und begegnet {hindernis}. "
            f"Auf dem Weg wächst Zweifel, doch auch Entschlossenheit. {wendung}"
        )

    def generiere_buch(self) -> str:
        titel = self.generiere_titel()
        teile = [f"# {titel}", ""]

        for kapitel_nummer in range(1, self.config.kapitel + 1):
            teile.append(self.generiere_kapitelueberschrift(kapitel_nummer))
            teile.append("-" * 72)
            for _ in range(self.config.abschnitte_pro_kapitel):
                teile.append(self.generiere_absatz())
                teile.append("")

        teile.append(self.zufall.choice(SCHLUESSE))
        return "\n".join(teile).strip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generiert ein kleines Buch als Markdown-Datei.")
    parser.add_argument("-t", "--titel", type=str, help="Optionaler Buchtitel")
    parser.add_argument("-k", "--kapitel", type=int, default=5, help="Anzahl der Kapitel")
    parser.add_argument(
        "-a",
        "--abschnitte",
        type=int,
        default=3,
        help="Anzahl der Abschnitte pro Kapitel",
    )
    parser.add_argument("-s", "--seed", type=int, default=None, help="Seed für reproduzierbare Ausgaben")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("buch.md"),
        help="Ausgabedatei (Markdown)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.kapitel < 1:
        raise SystemExit("Fehler: --kapitel muss mindestens 1 sein.")
    if args.abschnitte < 1:
        raise SystemExit("Fehler: --abschnitte muss mindestens 1 sein.")

    config = BuchKonfiguration(
        titel=args.titel,
        kapitel=args.kapitel,
        abschnitte_pro_kapitel=args.abschnitte,
        seed=args.seed,
    )

    generator = BuchGenerator(config)
    text = generator.generiere_buch()
    args.output.write_text(text, encoding="utf-8")
    print(f"Buch erstellt: {args.output}")


if __name__ == "__main__":
    main()
