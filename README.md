# Dokumenten- und Daten-Chat (RAG + MCP)

Diese Anwendung kombiniert drei Datenquellen für Antworten auf Nutzerfragen:

1. **Dokumente aus einer Vektor-Datenbank** (RAG)
2. **Strukturierte Daten über einen MCP-Server via REST**
3. **Remote-LLM-Verarbeitung über ChatGPT (OpenAI API)**

Zusätzlich gibt es eine **UI mit Dialog-Historie**, damit du über mehrere Nachrichten hinweg weiterfragen kannst.

## Architektur

- `ingest.py`: Pipeline für Dokument-Ingestion (Dateien laden, chunking, Embeddings, Speicherung in Vector-DB)
- `ui.py`: Streamlit-Chatoberfläche mit Sitzungsverlauf
- `app/vector_store.py`: Persistente Chroma-Vector-DB
- `app/mcp_client.py`: REST-Client für MCP-Backend
- `app/chat_service.py`: Orchestriert Vektorsuche + MCP-Antwort + ChatGPT-Antwort
- `app/history.py`: SQLite-Speicherung der Chat-Historie

## Voraussetzungen

- Python 3.10+
- `OPENAI_API_KEY`
- Laufender MCP REST Endpoint (Standard: `http://localhost:8080/query`)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Konfiguration über Umgebungsvariablen

- `OPENAI_API_KEY` (Pflicht)
- `CHAT_MODEL` (Default: `gpt-4.1-mini`)
- `EMBEDDING_MODEL` (Default: `text-embedding-3-small`)
- `VECTOR_DB_PATH` (Default: `./data/vector_db`)
- `HISTORY_DB_PATH` (Default: `./data/history.db`)
- `MCP_REST_ENDPOINT` (Default: `http://localhost:8080/query`)
- `RETRIEVAL_K` (Default: `5`)

Beispiel:

```bash
export OPENAI_API_KEY="sk-..."
export MCP_REST_ENDPOINT="http://localhost:8080/query"
```

## 1) Dokumente ingestieren

Lege `.txt` und `.md` Dateien in ein Verzeichnis, z. B. `./docs`.

```bash
python ingest.py ./docs --chunk-size 800 --overlap 120
```

Die Pipeline:
- liest Dokumente aus dem Verzeichnis,
- chunked die Inhalte,
- berechnet Embeddings via OpenAI,
- speichert Chunks + Embeddings in Chroma.

## 2) UI starten

```bash
streamlit run ui.py
```

In der Oberfläche kannst du Fragen stellen. Die Antwort wird aus:
- relevanten Dokument-Chunks (RAG),
- der MCP/REST-Datenantwort,
- und der Modellgenerierung kombiniert.

Der Verlauf wird pro Sitzung in SQLite gespeichert.

## MCP REST-Response-Format (erwartet)

`POST /query` mit Body:

```json
{
  "question": "Wie viele offene Bestellungen gibt es?"
}
```

Antwort:

```json
{
  "answer": "Aktuell gibt es 42 offene Bestellungen."
}
```

## Hinweise

- Für produktive Nutzung sollten Authentifizierung, Rate-Limits und Observability ergänzt werden.
- Aktuell werden nur `.txt` und `.md` Dateien ingestiert.
