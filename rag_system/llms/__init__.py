from .base import BaseLLM
from .openai import OpenAILLM
from .gemini import GeminiLLM
from .ollama import OllamaLLM
from .le_mistral import LeMistralLLM


def get_llm(provider: str, api_key: str, model: str = "ollama") -> BaseLLM:
    if provider == "ollama":
        return OllamaLLM(api_key, model)
    elif provider == "mistral":
        return LeMistralLLM(api_key, model)
    elif provider == "openai":
        return OpenAILLM(api_key, model)
    elif provider == "gemini":
        return GeminiLLM(api_key, model)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
