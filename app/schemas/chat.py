"""Schema definitions for chat requests, responses, and UI payloads."""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
