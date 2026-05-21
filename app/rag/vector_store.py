import chromadb
from chromadb import PersistentClient

client=PersistentClient(path="chroma_db")
collection=client.get_or_create_collection(name="researchgpt")

def store_embeddings(chunks,embeddings):
    ids=[f"id_{i}" for i in range(len(chunks))]

    collection.add(ids=ids,
    documents=chunks,
    embeddings=embeddings)

def search_documents(query_embedding, n_results=3):
    result=collection.query(query_embeddings=[query_embedding.tolist()],n_results=n_results)
    return result