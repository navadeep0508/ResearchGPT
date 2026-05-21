import chromadb
from uuid import uuid4
from chromadb import PersistentClient
from chromadb.config import Settings
from app.core.config import CHROMA_DIR
from app.rag.local_embeddings import HashEmbeddingFunction

client=PersistentClient(
    path=CHROMA_DIR,
    settings=Settings(anonymized_telemetry=False)
)
collection=client.get_or_create_collection(
    name="researchgpt",
    embedding_function=HashEmbeddingFunction()
)

def store_documents(chunks):
    if not chunks:
        return

    ids=[f"chunk_{uuid4().hex}" for _ in chunks]

    collection.add(ids=ids,
    documents=chunks)

def search_documents(query, n_results=3):
    if collection.count() == 0:
        return {"documents": [[]], "distances": [[]], "ids": [[]]}

    result = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return result
