from .base import BaseEmbedding
from .openai_embeddings import OpenAIEmbedding
from .ollama_embeddngs import OllamaEmbeddings
from .le_mistral_embeddings import LeMistralEmbeddings


def get_embedding_model(
    provider: str, api_key: str, model: str = "ollama"
) -> BaseEmbedding:
    if provider == "ollama":
        return OllamaEmbeddings(api_key, model)
    elif provider == "mistral":
        return LeMistralEmbeddings(api_key, model)
    elif provider == "openai":
        return OpenAIEmbedding(api_key, model)
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")
