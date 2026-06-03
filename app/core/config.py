"""Application settings, environment variables, and default configuration values."""

from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = APP_DIR.parent

STATIC_DIR = APP_DIR / "static"
API_PREFIX = "/api"
APP_TITLE = "RAG Chatbot"

DATA_PATH = REPO_DIR / "data"
CHROMA_PATH = REPO_DIR / "chroma"

ALLOWED_ORIGINS = ["*"]

EMBEDDING_MODEL = "nomic-embed-text"
DEFAULT_LLM_MODEL = "mistral"
DEFAULT_TOP_K = 5
OLLAMA_TIMEOUT_SECONDS = 120
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_KEEP_ALIVE = 300
OLLAMA_MAX_TOKENS = 256

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
