import hashlib
import math
import re


class HashEmbeddingFunction:
    def __init__(self, dimensions=384):
        self.dimensions = dimensions

    @staticmethod
    def name():
        return "default"

    def __call__(self, input):
        return [self._embed(text) for text in input]

    def embed_documents(self, input):
        return self(input)

    def embed_query(self, input):
        return self(input)

    def _embed(self, text):
        vector = [0.0] * self.dimensions
        tokens = re.findall(r"\w+", text.lower())

        for token in tokens:
            digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
            bucket = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[bucket] += sign

        norm = math.sqrt(sum(value * value for value in vector))
        if not norm:
            return vector

        return [value / norm for value in vector]
