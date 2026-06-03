"""FastAPI application entrypoint that wires the API and static UI."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api import chat, query
from app.core.config import ALLOWED_ORIGINS, API_PREFIX, APP_TITLE, STATIC_DIR

logging.basicConfig(level=logging.INFO)
app = FastAPI(
    title=APP_TITLE,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_connection_close(request, call_next):
    response = await call_next(request)
    response.headers["Connection"] = "close"
    return response


# Serve the lightweight React UI from the /static route.
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.include_router(chat.router, prefix=API_PREFIX)
app.include_router(query.router, prefix=API_PREFIX)
