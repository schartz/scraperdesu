from typing import Union
from .base import BaseLLM
from mistralai import ChatCompletionResponse, Mistral


class LeMistralLLM(BaseLLM):
    def __init__(self, api_key: str = "xyz", model: str = "llama3.1"):
        self.api_key = api_key
        self.model = model
        self.mistral_client = Mistral(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        response: Union[None, ChatCompletionResponse] = (
            self.mistral_client.chat.complete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                stream=False,
            )
        )
        if (
            not response
            or not response.choices
            or not response.choices[0].message.content
        ):
            return ""
        return response.choices[0].message.content
