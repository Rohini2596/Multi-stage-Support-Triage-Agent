from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from pathlib import Path
class EmbeddingRetriever:
    def __init__(self, model_name="BAAI/bge-small-en-v1.5"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
    def build_index(self, chunks):
        self.documents = chunks
        texts = [c["text"] for c in chunks]
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(np.array(embeddings).astype("float32"))
    def retrieve(self, query, top_k=5):
        q_emb = self.model.encode(
            [query],
            normalize_embeddings=True,
        )
        scores, indices = self.index.search(
            np.array(q_emb).astype("float32"),
            top_k,
        )
        results = []
        for score, idx in zip(scores[0], indices[0]):
            doc = self.documents[idx]
            doc["score"] = float(score)
            results.append(doc)
        return results