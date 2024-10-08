from mistralai.models.embeddingresponse import EmbeddingResponse
from mistralai import Mistral
from typing import List, Union
from .base import BaseEmbedding


class LeMistralEmbeddings(BaseEmbedding):
    def __init__(self, api_key: str = "xyz", model_name: str = "nomic-embed-text"):
        self.api_key = api_key
        self.model = model_name
        self.mistral_client = Mistral(api_key=self.api_key)

    def embed(self, text: str) -> List[float]:
        response: Union[EmbeddingResponse, None] = (
            self.mistral_client.embeddings.create(model=self.model, inputs=[text])
        )
        if not response:
            return []

        if not response.data[0].embedding:
            return []
        return response.data[0].embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        response: Union[EmbeddingResponse, None] = (
            self.mistral_client.embeddings.create(model=self.model, inputs=texts)
        )
        if not response:
            return []

        _embeddings = []
        for item in response.data:
            if item.embedding is not None:
                _embeddings.append(item.embedding)
            else:
                _embeddings.append([])
        return _embeddings
