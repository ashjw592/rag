"""Chat API routes exposed to the UI and external clients."""

import logging

from fastapi import APIRouter, Depends

from app.dependencies import get_rag_service
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import RagService

router = APIRouter(prefix="/chat")

logger = logging.getLogger(__name__)


@router.post("/", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    rag_service: RagService = Depends(get_rag_service),
) -> ChatResponse:

    logger.info(f"Received chat message: {payload.message[:50]}")
    try:
        result = await rag_service.generate_reply(payload.message)
        logger.info(f"Generated chat reply: {result.reply[:50]}")
        return ChatResponse(reply=result.reply)
    except Exception as e:
        logger.error(f"Error generating chat reply: {e}")
        return ChatResponse(
            reply="Sorry, something went wrong while processing your message."
        )


from fastapi.responses import StreamingResponse


@router.post("/stream")
async def chat_stream(
    payload: ChatRequest,
    rag_service: RagService = Depends(get_rag_service),
):
    return StreamingResponse(
        rag_service.stream_reply(payload.message),
        media_type="text/plain",
    )
