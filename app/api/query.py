"""Query API routes that mirror the CLI query options."""

from fastapi import APIRouter, Depends

from app.core.config import DEFAULT_LLM_MODEL, DEFAULT_TOP_K
from app.dependencies import get_rag_service
from app.schemas.query import QueryRequest, QueryResponse
from app.services.rag_service import RagService

router = APIRouter(prefix="/query")


@router.post("/", response_model=QueryResponse)
def query(
    payload: QueryRequest,
    rag_service: RagService = Depends(get_rag_service),
) -> QueryResponse:
    model_name = payload.model or DEFAULT_LLM_MODEL
    top_k = payload.k if payload.k is not None else DEFAULT_TOP_K
    result = rag_service.generate_reply(
        message=payload.query_text,
        model_name=model_name,
        k=top_k,
        include_context=payload.show_context,
    )
    return QueryResponse(
        reply=result.reply,
        sources=result.sources,
        context=result.context,
    )
