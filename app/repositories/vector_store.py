"""Vector store access helpers for indexing and semantic search."""

import shutil

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from app.core.config import (
    CHROMA_PATH,
    EMBEDDING_MODEL,
    OLLAMA_BASE_URL,
    OLLAMA_KEEP_ALIVE,
    OLLAMA_TIMEOUT_SECONDS,
)


def get_embedding_function() -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL,
        keep_alive=OLLAMA_KEEP_ALIVE,
        sync_client_kwargs={"timeout": OLLAMA_TIMEOUT_SECONDS},
    )


def get_vector_store() -> Chroma:
    return Chroma(
        persist_directory=str(CHROMA_PATH),
        embedding_function=get_embedding_function(),
    )


def clear_vector_store() -> None:
    if CHROMA_PATH.exists():
        shutil.rmtree(CHROMA_PATH)
