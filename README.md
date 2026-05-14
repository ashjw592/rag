# Simple RAG Chat Bot

## Prerequisites

- Python
- Ollama

## Setup

1. Setup venv

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run Ollama

```bash
ollama serve
```

4. Install Models

```bash
ollama pull nomic-embed-text
ollama pull mistral
```

5. Put PDFs in `data/` directory

6. Run Ingest Script

```bash
python ingest.py
```

7. Run Query

```bash
python query.py <your query here>
```

## Notes

- The `ingest.py` script processes PDFs in the `data/` directory, extracts
  text, generates embeddings using the `nomic-embed-text` model, and stores
  them in a local vector store.
- The `query.py` script takes a user query, generates an embedding, retrieves
  relevant documents from the vector store, and uses the `mistral` model to
  generate a response based on the retrieved documents.
- Ensure that Ollama is running and the required models are pulled before executing the scripts.
