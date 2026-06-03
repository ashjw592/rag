"""Service layer for loading documents and indexing them into the vector store."""

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import CHUNK_OVERLAP, CHUNK_SIZE, DATA_PATH
from app.repositories.vector_store import clear_vector_store, get_vector_store


def load_documents():
    document_loader = PyPDFDirectoryLoader(str(DATA_PATH))
    return document_loader.load()


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0
    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id
    return chunks


def add_to_vector_store(chunks) -> int:
    db = get_vector_store()
    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])

    new_chunks = []
    for chunk in chunks_with_ids:
        chunk_id = chunk.metadata["id"]
        if chunk_id not in existing_ids:
            new_chunks.append(chunk)

    if new_chunks:
        db.add_documents(new_chunks)

    return len(new_chunks)


def ingest_documents(clear: bool = False) -> int:
    if clear:
        clear_vector_store()

    documents = load_documents()
    chunks = split_documents(documents)
    return add_to_vector_store(chunks)
