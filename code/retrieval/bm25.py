from rank_bm25 import BM25Okapi
class BM25Retriever:
    def __init__(self, chunks):
        self.chunks = chunks
        self.corpus = [
            chunk["text"].lower().split()
            for chunk in chunks
        ]
        self.bm25 = BM25Okapi(
            self.corpus
        )
    def search(
        self,
        query: str,
        top_k: int = 5,
    ):
        tokenized_query = (
            query.lower().split()
        )
        scores = self.bm25.get_scores(
            tokenized_query
        )
        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True,
        )
        results = []
        for idx, score in ranked[:top_k]:
            chunk = self.chunks[idx]
            results.append({
                "text": chunk["text"],
                "path": chunk["path"],
                "company": chunk["company"],
                "score": float(score),
            })
        return results