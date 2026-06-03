"""Schema definitions for the query API endpoints."""

from typing import List, Optional

from pydantic import BaseModel


class QueryRequest(BaseModel):
    query_text: str
    model: Optional[str] = None
    k: Optional[int] = None
    show_context: bool = False


class QueryResponse(BaseModel):
    reply: str
    sources: List[str]
    context: Optional[str] = None
