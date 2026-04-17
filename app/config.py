from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    chat_model: str = "gpt-4.1-mini"
    embedding_model: str = "text-embedding-3-small"
    vector_db_path: str = "./data/vector_db"
    history_db_path: str = "./data/history.db"
    mcp_rest_endpoint: str = "http://localhost:8080/query"
    retrieval_k: int = 5



def load_settings() -> Settings:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY ist nicht gesetzt.")

    return Settings(
        openai_api_key=api_key,
        chat_model=os.getenv("CHAT_MODEL", "gpt-4.1-mini"),
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        vector_db_path=os.getenv("VECTOR_DB_PATH", "./data/vector_db"),
        history_db_path=os.getenv("HISTORY_DB_PATH", "./data/history.db"),
        mcp_rest_endpoint=os.getenv("MCP_REST_ENDPOINT", "http://localhost:8080/query"),
        retrieval_k=int(os.getenv("RETRIEVAL_K", "5")),
    )
