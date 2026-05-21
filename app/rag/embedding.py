import requests

from app.core.config import HF_TOKEN


API_URL = (
    "https://router.huggingface.co/hf-inference/"
    "models/sentence-transformers/all-MiniLM-L6-v2"
)

headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}


def _embedding_from_response(response):
    response.raise_for_status()
    result = response.json()

    if isinstance(result, dict):
        error = result.get("error") or result.get("message") or result
        raise ValueError(f"Embedding API error: {error}")

    if result and isinstance(result[0], list):
        return result[0]

    if isinstance(result, list):
        return result

    raise ValueError("Embedding API returned an unsupported response format")


def generate_embeddings(texts):
    embeddings = []

    for text in texts:
        response = requests.post(
            API_URL,
            headers=headers,
            json={
                "inputs": text
            },
            timeout=60
        )

        embeddings.append(_embedding_from_response(response))

    return embeddings


def generate_query_embedding(query):

    response = requests.post(
        API_URL,
        headers=headers,
        json={
            "inputs": query
        },
        timeout=60
    )

    return _embedding_from_response(response)
