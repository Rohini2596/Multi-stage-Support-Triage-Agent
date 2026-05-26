from code.retrieval.indexer import (
    load_corpus,
)
from code.retrieval.document_loader import (
    build_chunks,
)
def main():
    docs = load_corpus()
    print(f"Loaded Docs: {len(docs)}")
    assert len(docs) > 0, (
        "No documents loaded"
    )
    chunks = build_chunks(docs)
    print(f"Total Chunks: {len(chunks)}")
    assert len(chunks) > 0, (
        "No chunks created"
    )
    print("FIRST CHUNK:")
    print(chunks[0])
if __name__ == "__main__":
    main()