"""Application settings, environment variables, and default configuration values."""

from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = APP_DIR / "static"
API_PREFIX = "/api"
APP_TITLE = "RAG Chatbot"
