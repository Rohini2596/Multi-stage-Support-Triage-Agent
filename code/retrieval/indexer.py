from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
SUPPORTED_SUFFIXES = {".md", ".txt", ".json", ".csv",}
@dataclass
class CorpusChunk:
    text: str
    path: str
    company: str
def clean_text(text: str) -> str:
    return (text.replace("\r", "\n").replace("\t", " ").strip())
def infer_company(path: str) -> str:
    p = path.lower()
    if "visa" in p:
        return "visa"
    if "claude" in p:
        return "claude"
    if "devplatform" in p:
        return "devplatform"
    return "unknown"
def load_corpus(base_dir=DATA_DIR):
    docs = []
    base = Path(base_dir).resolve()
    print(f"Loading corpus from: {base}")
    print(f"Directory exists: {base.exists()}")
    if not base.exists():
        print("DATA DIRECTORY NOT FOUND")
        return []
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        path_str = str(path).lower()
        if "api_specs" in path_str:
            continue
        if path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        try:
            text = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except Exception as e:
            print(f"FAILED TO READ: {path}")
            print(e)
            continue
        text = clean_text(text)
        if len(text) < 50:
            continue
        docs.append(
            CorpusChunk(
                text=text,
                path=str(
                    path.relative_to(ROOT_DIR)
                ),
                company=infer_company(
                    str(path)
                ),
            )
        )
    print(f"Loaded {len(docs)} documents")
    return docs
class HybridRetriever:
    def __init__(self, docs):
        self.docs = docs
        self.texts = [d.text for d in docs]
        print(f"Retriever initialized with {len(self.docs)} docs")
        if not self.texts:
            self.vectorizer = None
            self.matrix = None
            return
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            lowercase=True,
            max_features=50000,
            ngram_range=(1, 2),
        )
        self.matrix = self.vectorizer.fit_transform(self.texts)
    def retrieve(self, query: str, company_hint: Optional[str] = None, top_k: int = 5,):
        if self.matrix is None:
            return []
        query = clean_text(query)
        if not query:
            return []
        q = self.vectorizer.transform([query])
        raw_scores = (self.matrix @ q.T).toarray().ravel()
        ranked = []
        for idx, raw_score in enumerate(raw_scores):
            d = self.docs[idx]
            boost = 0.0
            if company_hint:
                if (company_hint.lower() in d.company.lower()):
                    boost = 0.15
            final_score = (float(raw_score) + boost)
            ranked.append((idx, final_score))
        ranked.sort(key=lambda x: x[1], reverse=True,)
        results = []
        for idx, score in ranked:
            if score <= 0:
                continue
            d = self.docs[idx]
            results.append({
                "text": d.text[:1500],
                "path": d.path,
                "company": d.company,
                "score": round(
                    float(score),
                    4,
                ),
            })
            if len(results) >= top_k:
                break
        return results