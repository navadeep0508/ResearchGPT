import math

from app.db.database import SessionLocal
from app.db.models import DocumentChunk


def store_embeddings(chunks, embeddings):
    if not chunks:
        return

    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings length mismatch.")

    db = SessionLocal()
    try:
        for chunk, embedding in zip(chunks, embeddings):
            db.add(DocumentChunk(document=chunk, embedding=embedding))
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def search_documents(query_embedding, n_results=3):
    db = SessionLocal()
    try:
        chunks = db.query(DocumentChunk).all()
    finally:
        db.close()

    if not chunks:
        return {"documents": [[]], "distances": [[]], "ids": [[]]}

    query = query_embedding.tolist() if hasattr(query_embedding, "tolist") else query_embedding
    scored_chunks = []

    for chunk in chunks:
        score = _cosine_similarity(query, chunk.embedding)
        scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda item: item[0], reverse=True)
    top_chunks = scored_chunks[:n_results]

    return {
        "documents": [[chunk.document for _, chunk in top_chunks]],
        "distances": [[1 - score for score, _ in top_chunks]],
        "ids": [[str(chunk.id) for _, chunk in top_chunks]]
    }


def _cosine_similarity(left, right):
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))

    if not left_norm or not right_norm:
        return 0.0

    return dot / (left_norm * right_norm)
