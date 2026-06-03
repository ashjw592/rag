"""Service layer for running retrieval-augmented generation workflows."""

from dataclasses import dataclass
from typing import List, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

from app.core.config import (
    DEFAULT_LLM_MODEL,
    DEFAULT_TOP_K,
    OLLAMA_BASE_URL,
    OLLAMA_KEEP_ALIVE,
    OLLAMA_MAX_TOKENS,
    OLLAMA_TIMEOUT_SECONDS,
)
from app.repositories.vector_store import get_vector_store

PROMPT_TEMPLATE = """
Answer the question based only on the following context. If you don't know the answer, say you don't know.

{context}

---

Answer the question based on the above context: {question}
"""


@dataclass
class RagResult:
    reply: str
    sources: List[str]
    context: Optional[str]


class RagService:
    """Coordinates retrieval and generation for chat replies."""

    def generate_reply(
        self,
        message: str,
        model_name: str = DEFAULT_LLM_MODEL,
        k: int = DEFAULT_TOP_K,
        include_context: bool = False,
    ) -> RagResult:
        db = get_vector_store()
        results = db.similarity_search_with_score(message, k=k)

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        formatted_prompt = prompt.format(context=context_text, question=message)

        model = OllamaLLM(
            model=model_name,
            base_url=OLLAMA_BASE_URL,
            keep_alive=OLLAMA_KEEP_ALIVE,
            num_predict=OLLAMA_MAX_TOKENS,
            sync_client_kwargs={"timeout": OLLAMA_TIMEOUT_SECONDS},
        )
        response_text = model.invoke(formatted_prompt)

        sources = [doc.metadata.get("id") for doc, _score in results]
        cleaned_sources = [source for source in sources if source]
        return RagResult(
            reply=response_text,
            sources=cleaned_sources,
            context=context_text if include_context else None,
        )
