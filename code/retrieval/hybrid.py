from code.retrieval.indexer import (
    load_corpus,
    HybridRetriever,
)
from code.retrieval.document_loader import (
    build_chunks,
)
from code.retrieval.bm25 import (
    BM25Retriever,
)
from code.retrieval.reranker import (
    SimpleReranker,
)
class HybridSearch:
    def __init__(self):
        print("Initializing Hybrid Search...")
        self.docs = load_corpus()
        # BUILD CHUNKS
        self.chunks = build_chunks(
            self.docs
        )
        print(
            f"Total Chunks: "
            f"{len(self.chunks)}"
        )
        self.tfidf = HybridRetriever(
            self.docs
        )
        self.bm25 = BM25Retriever(
            self.chunks
        )
        self.reranker = (
            SimpleReranker()
        )
    def search(
        self,
        query: str,
        company_hint=None,
        top_k: int = 5,
    ):
        print("SEARCH QUERY:")
        print(query)
        # TFIDF SEARCH
        tfidf_results = (
            self.tfidf.retrieve(
                query=query,
                company_hint=company_hint,
                top_k=top_k * 2,
            )
        )
        # BM25 SEARCH
        bm25_results = (
            self.bm25.search(
                query=query,
                top_k=top_k * 2,
            )
        )
        print(
            f"TFIDF RESULTS: "
            f"{len(tfidf_results)}"
        )

        print(
            f"BM25 RESULTS: "
            f"{len(bm25_results)}"
        )
        combined = {}
        # ADD TFIDF RESULTS
        for r in tfidf_results:
            key = (
                r["path"]
                + r["text"][:120]
            )
            combined[key] = {
                **r,
                "score":
                    r["score"] * 0.45,
            }
        # ADD BM25 RESULTS
        for r in bm25_results:
            key = (
                r["path"]
                + r["text"][:120]
            )
            if key not in combined:
                combined[key] = {
                    **r,
                    "score": 0,
                }
            combined[key]["score"] += (
                r["score"] * 0.55
            )
        combined = dict(sorted(combined.items(), key=lambda x: x[0]))
        final_results = list(
            combined.values()
        )
        print(
            f"COMBINED RESULTS: "
            f"{len(final_results)}"
        )
        final_results = sorted(final_results, key=lambda x: (x.get("path", ""), round(x.get("score", 0),6),))
        # RERANK
        reranked = (
            self.reranker.rerank(
                query=query,
                results=final_results,
                company_hint=company_hint,
                top_k=top_k,
            )
        )
        print(
            f"FINAL RERANKED: "
            f"{len(reranked)}"
        )
        return reranked