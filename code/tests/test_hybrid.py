from code.retrieval.hybrid import (
    HybridSearch,
)
def main():
    search = HybridSearch()
    results = search.search(
        query=(
            "refund for claude "
            "subscription"
        ),
        company_hint="claude",
        top_k=5,
    )
    print("HYBRID RESULTS:")
    for idx, r in enumerate(results):
        print("=" * 60)
        print(f"RESULT {idx+1}")
        print("PATH:")
        print(r["path"])
        print("COMPANY:")
        print(r["company"])
        print("FINAL SCORE:")
        print(r["rerank_score"])
        print("TEXT:")
        print(r["text"][:500])
if __name__ == "__main__":
    main()