"""FastAPI application entrypoint that wires the API and static UI."""

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api import chat
from app.core.config import API_PREFIX, APP_TITLE, STATIC_DIR

app = FastAPI(
    title=APP_TITLE,
)
# Serve the lightweight React UI from the /static route.
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.include_router(chat.router, prefix=API_PREFIX)
