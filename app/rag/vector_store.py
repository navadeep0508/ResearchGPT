import chromadb
from uuid import uuid4
from chromadb import PersistentClient
from chromadb.config import Settings
from app.core.config import CHROMA_DIR

client=PersistentClient(
    path=CHROMA_DIR,
    settings=Settings(anonymized_telemetry=False)
)
collection=client.get_or_create_collection(name="researchgpt")

def store_embeddings(chunks, embeddings):
    if not chunks:
        return

    ids=[f"chunk_{uuid4().hex}" for _ in chunks]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

def search_documents(query_embedding, n_results=3):
    if collection.count() == 0:
        return {"documents": [[]], "distances": [[]], "ids": [[]]}

    emb = query_embedding.tolist() if hasattr(query_embedding, "tolist") else query_embedding

    result = collection.query(
        query_embeddings=[emb],
        n_results=n_results
    )
    return result
