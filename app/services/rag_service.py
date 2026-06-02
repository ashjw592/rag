"""Service layer for running retrieval-augmented generation workflows."""


class RagService:
    """Coordinates retrieval and generation for chat replies."""

    def generate_reply(self, message: str) -> str:
        # Placeholder until the full RAG pipeline is wired up.
        return f"Echo: {message}"
