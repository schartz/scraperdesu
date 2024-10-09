import ollama
from typing import List
from .base import BaseEmbedding


class OllamaEmbeddings(BaseEmbedding):
    def __init__(self, api_key: str = "xyz", model_name: str = "nomic-embed-text"):
        self.api_key = api_key
        self.model = model_name

    def embed(self, text: str) -> List[float]:
        response = ollama.embed(model=self.model, input=[text])
        return response["embeddings"][0]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        response = ollama.embed(model=self.model, input=texts)
        return response["embeddings"]
