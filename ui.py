from __future__ import annotations

import uuid

import streamlit as st
from openai import OpenAI

from app.chat_service import ChatService
from app.config import load_settings
from app.history import HistoryStore
from app.mcp_client import MCPRestClient
from app.vector_store import VectorStore


st.set_page_config(page_title="RAG + MCP Chat", page_icon="💬", layout="wide")
st.title("💬 Dokumenten- und Daten-Chat")

settings = load_settings()
openai_client = OpenAI(api_key=settings.openai_api_key)
vector_store = VectorStore(settings.vector_db_path)
mcp_client = MCPRestClient(settings.mcp_rest_endpoint)
history_store = HistoryStore(settings.history_db_path)
chat_service = ChatService(
    openai_client=openai_client,
    chat_model=settings.chat_model,
    embedding_model=settings.embedding_model,
    vector_store=vector_store,
    mcp_client=mcp_client,
    retrieval_k=settings.retrieval_k,
)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.sidebar.header("Sitzung")
st.sidebar.write(f"Session-ID: `{st.session_state.session_id}`")
if st.sidebar.button("Neue Sitzung"):
    st.session_state.session_id = str(uuid.uuid4())
    st.rerun()

st.subheader("Verlauf")
messages = history_store.load_session(st.session_state.session_id)
for msg in messages:
    with st.chat_message(msg.role):
        st.markdown(msg.content)

user_question = st.chat_input("Stelle eine Frage zu Dokumenten und Daten...")

if user_question:
    history_store.append(st.session_state.session_id, "user", user_question)
    updated_history = history_store.load_session(st.session_state.session_id)

    with st.chat_message("user"):
        st.markdown(user_question)

    answer = chat_service.answer(user_question, updated_history)
    history_store.append(st.session_state.session_id, "assistant", answer)

    with st.chat_message("assistant"):
        st.markdown(answer)
