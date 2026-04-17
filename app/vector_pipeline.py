from __future__ import annotations

from pathlib import Path

from openai import OpenAI

from app.chunking import build_chunks
from app.vector_store import VectorStore


class VectorIngestionPipeline:
    def __init__(
        self,
        openai_client: OpenAI,
        embedding_model: str,
        vector_store: VectorStore,
    ):
        self.openai_client = openai_client
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def _embed_texts(self, texts: list[str]) -> list[list[float]]:
        response = self.openai_client.embeddings.create(model=self.embedding_model, input=texts)
        return [item.embedding for item in response.data]

    def run(self, directory: str, chunk_size: int = 800, overlap: int = 120) -> int:
        chunks = build_chunks(Path(directory), chunk_size=chunk_size, overlap=overlap)
        if not chunks:
            return 0

        embeddings = self._embed_texts([chunk.text for chunk in chunks])
        self.vector_store.upsert_chunks(chunks, embeddings)
        return len(chunks)
