import argparse

from app.services.ingest_service import ingest_documents


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--clear", action="store_true", help="Clear existing data and Chroma database"
    )
    args = parser.parse_args()
    if args.clear:
        print("Clearing existing data and Chroma database...")

    new_chunks = ingest_documents(clear=args.clear)
    if new_chunks > 0:
        print(f"Added {new_chunks} new chunks to Chroma database.")
    else:
        print("No new chunks to add to Chroma database.")


if __name__ == "__main__":
    main()
