from code.retrieval.indexer import (
    load_corpus,
)
from code.retrieval.document_loader import (
    build_chunks,
)
from code.retrieval.bm25 import (
    BM25Retriever,
)
def main():
    docs = load_corpus()
    chunks = build_chunks(docs)
    bm25 = BM25Retriever(chunks)
    results = bm25.search(
        "refund for claude subscription",
        top_k=5,
    )
    print("BM25 RESULTS:")
    for idx, r in enumerate(results):
        print("=" * 60)
        print(f"RESULT {idx+1}")
        print("PATH:")
        print(r["path"])
        print("SCORE:")
        print(r["score"])
        print("TEXT:")
        print(r["text"][:500])
if __name__ == "__main__":
    main()