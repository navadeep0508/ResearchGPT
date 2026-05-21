import requests

from app.core.config import HF_TOKEN


API_URL = (
    "https://router.huggingface.co/hf-inference/"
    "models/sentence-transformers/all-MiniLM-L6-v2/"
    "pipeline/feature-extraction"
)

headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}


def _json_from_response(response):
    if not response.ok:
        raise RuntimeError(
            f"Embedding API error {response.status_code}: {response.text}"
        )

    result = response.json()

    if isinstance(result, dict):
        error = result.get("error") or result.get("message") or result
        raise ValueError(f"Embedding API error: {error}")

    if not isinstance(result, list):
        raise ValueError("Embedding API returned an unsupported response format")

    return result


def _embedding_batch_from_response(response):
    result = _json_from_response(response)

    if result and isinstance(result[0], list):
        return result

    if result and isinstance(result[0], (int, float)):
        return [result]

    raise ValueError("Embedding API returned an unsupported batch format")


def _single_embedding_from_response(response):
    result = _json_from_response(response)

    if result and isinstance(result[0], list):
        return result[0]

    if result and isinstance(result[0], (int, float)):
        return result

    raise ValueError("Embedding API returned an unsupported embedding format")


def _post_embedding_request(inputs):
    if not HF_TOKEN:
        raise RuntimeError("HF_TOKEN is not configured.")

    return requests.post(
        API_URL,
        headers=headers,
        json={
            "inputs": inputs,
            "options": {
                "wait_for_model": True
            }
        },
        timeout=90
    )


def generate_embeddings(texts):
    if not texts:
        return []

    response = _post_embedding_request(texts)
    return _embedding_batch_from_response(response)


def generate_query_embedding(query):
    response = _post_embedding_request(query)

    return _single_embedding_from_response(response)
