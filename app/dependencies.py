"""FastAPI dependency providers (e.g., RAG pipelines, vector stores, model clients)."""

from app.services.rag_service import RagService


def get_rag_service() -> RagService:
    """Provide a RAG service instance for request handlers."""
    return RagService()
