# Buchgenerator (Python)

Gute Wahl: **Python** ist für einen Buchgenerator sehr sinnvoll, weil es schnell zu entwickeln ist, viele KI- und NLP-Bibliotheken hat und sich einfach als CLI oder Web-App erweitern lässt.

## Was dieses Projekt kann

- Erstellt ein Buch als Markdown-Datei.
- Generiert automatisch Inhaltsverzeichnis und Kapiteltexte.
- Unterstützt Parameter wie Thema, Genre, Ton, Kapitelanzahl und Wortziel.
- Reproduzierbare Ergebnisse über `--seed`.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Nutzung

```bash
buchgenerator \
  --title "Die Schatten der Stadt" \
  --topic "Korruption in einer futuristischen Metropole" \
  --genre "Thriller" \
  --chapters 6 \
  --tone "düster" \
  --words-per-chapter 220 \
  --seed 42 \
  --output roman.md
```

Danach findest du die Ausgabe in `roman.md`.

## Nächste sinnvolle Erweiterungen

1. LLM-Backend integrieren (z. B. OpenAI, lokale Modelle via Ollama).
2. Figuren- und Weltmodell als strukturierte Daten.
3. Mehrstufige Pipeline: Plot -> Kapitelplan -> Rohtext -> Überarbeitung.
4. Export nach EPUB/PDF.
