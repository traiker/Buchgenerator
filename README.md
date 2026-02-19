# Buchgenerator (Python)

Ein einfacher Buchgenerator, der automatisch ein kleines Buch im Markdown-Format erstellt.

## Voraussetzungen

- Python 3.10+

## Nutzung

```bash
python3 buchgenerator.py --output mein_buch.md
```

Optionen:

- `--titel` eigener Buchtitel
- `--kapitel` Anzahl Kapitel (Standard: `5`)
- `--abschnitte` Abschnitte pro Kapitel (Standard: `3`)
- `--seed` reproduzierbare Zufallsausgabe
- `--output` Ausgabedatei (Standard: `buch.md`)

Beispiel:

```bash
python3 buchgenerator.py --titel "Der letzte Stern" --kapitel 4 --abschnitte 2 --seed 42 --output stern.md
```
