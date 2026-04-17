from __future__ import annotations

from openai import OpenAI

from app.history import Message
from app.mcp_client import MCPRestClient
from app.vector_store import VectorStore


class ChatService:
    def __init__(
        self,
        openai_client: OpenAI,
        chat_model: str,
        embedding_model: str,
        vector_store: VectorStore,
        mcp_client: MCPRestClient,
        retrieval_k: int = 5,
    ):
        self.openai_client = openai_client
        self.chat_model = chat_model
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.mcp_client = mcp_client
        self.retrieval_k = retrieval_k

    def _embed(self, text: str) -> list[float]:
        response = self.openai_client.embeddings.create(model=self.embedding_model, input=text)
        return response.data[0].embedding

    def answer(self, question: str, history: list[Message]) -> str:
        query_embedding = self._embed(question)
        retrieved_chunks = self.vector_store.search(query_embedding, k=self.retrieval_k)

        rag_context = "\n\n".join(
            [f"Quelle: {item['source_path']}\nInhalt: {item['text']}" for item in retrieved_chunks]
        )
        mcp_answer = self.mcp_client.query(question)

        history_text = "\n".join([f"{m.role}: {m.content}" for m in history])

        prompt = (
            "Du bist ein Assistent für Fragen über Dokumente und strukturierte Daten. "
            "Nutze den Kontext aus der Vektorsuche und die MCP-Datenantwort zusammen.\n\n"
            f"Verlauf:\n{history_text}\n\n"
            f"Dokument-Kontext:\n{rag_context}\n\n"
            f"MCP-Antwort:\n{mcp_answer}\n\n"
            f"Frage:\n{question}\n\n"
            "Formuliere eine präzise Antwort auf Deutsch."
        )

        completion = self.openai_client.responses.create(
            model=self.chat_model,
            input=prompt,
            temperature=0.2,
        )
        return completion.output_text
