import ollama
from .base import BaseLLM


class OllamaLLM(BaseLLM):
    def __init__(self, api_key: str = "xyz", model: str = "llama3.1"):
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
        )
        return response["message"]["content"]
