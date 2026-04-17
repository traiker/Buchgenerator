from __future__ import annotations

import argparse

from openai import OpenAI

from app.config import load_settings
from app.vector_pipeline import VectorIngestionPipeline
from app.vector_store import VectorStore



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dokumente einlesen, chunken und in Vector-DB speichern.")
    parser.add_argument("directory", type=str, help="Verzeichnis mit .txt/.md Dateien")
    parser.add_argument("--chunk-size", type=int, default=800)
    parser.add_argument("--overlap", type=int, default=120)
    return parser.parse_args()



def main() -> None:
    args = parse_args()
    settings = load_settings()

    openai_client = OpenAI(api_key=settings.openai_api_key)
    vector_store = VectorStore(settings.vector_db_path)

    pipeline = VectorIngestionPipeline(
        openai_client=openai_client,
        embedding_model=settings.embedding_model,
        vector_store=vector_store,
    )
    count = pipeline.run(args.directory, chunk_size=args.chunk_size, overlap=args.overlap)
    print(f"{count} Chunks erfolgreich gespeichert.")


if __name__ == "__main__":
    main()
