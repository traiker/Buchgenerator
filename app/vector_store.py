from __future__ import annotations

from pathlib import Path

import chromadb
from chromadb.api.models.Collection import Collection

from app.chunking import DocumentChunk


class VectorStore:
    def __init__(self, db_path: str, collection_name: str = "documents"):
        Path(db_path).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection: Collection = self.client.get_or_create_collection(name=collection_name)

    def upsert_chunks(self, chunks: list[DocumentChunk], embeddings: list[list[float]]) -> None:
        ids = [chunk.chunk_id for chunk in chunks]
        docs = [chunk.text for chunk in chunks]
        metadatas = [{"doc_id": chunk.doc_id, "source_path": chunk.source_path} for chunk in chunks]
        self.collection.upsert(ids=ids, documents=docs, embeddings=embeddings, metadatas=metadatas)

    def search(self, query_embedding: list[float], k: int = 5) -> list[dict]:
        result = self.collection.query(query_embeddings=[query_embedding], n_results=k)
        ids = result.get("ids", [[]])[0]
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]

        payload: list[dict] = []
        for idx, doc_text, meta in zip(ids, docs, metas, strict=True):
            payload.append(
                {
                    "chunk_id": idx,
                    "text": doc_text,
                    "doc_id": meta.get("doc_id", ""),
                    "source_path": meta.get("source_path", ""),
                }
            )
        return payload
