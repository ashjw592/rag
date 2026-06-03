"""Chat API routes exposed to the UI and external clients."""

from fastapi import APIRouter, Depends

from app.dependencies import get_rag_service
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import RagService

router = APIRouter(prefix="/chat")


@router.post("/", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    rag_service: RagService = Depends(get_rag_service),
) -> ChatResponse:
    result = rag_service.generate_reply(payload.message)
    return ChatResponse(reply=result.reply)
