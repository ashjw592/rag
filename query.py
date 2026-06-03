import argparse

from app.core.config import DEFAULT_LLM_MODEL, DEFAULT_TOP_K
from app.services.rag_service import RagService


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    parser.add_argument(
        "--model", type=str, default=DEFAULT_LLM_MODEL, help="The Ollama model to use."
    )
    parser.add_argument(
        "--k",
        type=int,
        default=DEFAULT_TOP_K,
        help="The number of similar documents to retrieve.",
    )
    parser.add_argument(
        "--show-context",
        action="store_true",
        help="Whether to show the retrieved context.",
    )
    args = parser.parse_args()
    query_text = args.query_text
    k = args.k
    model_name = args.model
    show_context = args.show_context
    query_rag(query_text, model_name, k, show_context)


def query_rag(
    query_text: str,
    model_name: str = DEFAULT_LLM_MODEL,
    k: int = DEFAULT_TOP_K,
    show_context: bool = False,
) -> str:
    rag_service = RagService()
    result = rag_service.generate_reply(
        message=query_text,
        model_name=model_name,
        k=k,
        include_context=show_context,
    )
    if show_context and result.context:
        print(f"Context:\n{result.context}\n\n---\n\n")

    formatted_response = f"Response: {result.reply}\n\nSources: {result.sources}"
    print(formatted_response)
    return result.reply


if __name__ == "__main__":
    main()
