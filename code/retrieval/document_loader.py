from __future__ import annotations
from typing import List, Dict
def chunk_text(text: str, chunk_size: int = 700, overlap: int = 120,) -> List[str]:
    if not text:
        return []
    text = text.strip()
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks
def build_chunks(docs) -> List[Dict]:
    chunks = []
    for doc in docs:
        split_chunks = chunk_text(doc.text)
        for idx, chunk in enumerate(split_chunks):
            chunks.append({
                "text": chunk,
                "path": doc.path,
                "company": doc.company,
                "chunk_id": idx,
            })
    return chunks