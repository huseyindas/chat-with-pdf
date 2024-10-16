from ollama import Client
from langchain_ollama import ChatOllama

from core.config import settings


class LLM:

    def __init__(
        self,
        model: str = settings.ollama_model,
        host: str = settings.ollama_host
    ) -> None:

        self.model = model
        self.host = host
        self.num_predict: int = 128
        self.temperature: int = 0

    def get_model(self):
        self.check_model()
        model = ChatOllama(
            base_url=self.host,
            model=self.model,
            num_predict=self.num_predict,
            temperature=self.temperature,
        )
        return model

    def check_model(self):
        client = Client(host=self.host)
        pulled_models = [model["name"] for model in client.list()["models"]]
        if self.model not in pulled_models:
            client.pull(self.model)
