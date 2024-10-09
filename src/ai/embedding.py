from typing import List

from ollama import Client
from langchain_ollama import OllamaEmbeddings

from core.config import settings
from core.logging import logger


class CustomOllamaEmbeddings(OllamaEmbeddings):

    model: str = "nomic-embed-text"
    host: str = settings.ollama_host

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        client = Client(host=self.host)
        self.pull_model(client)

        embedded_docs = client.embed(self.model, texts)["embeddings"]
        return embedded_docs

    def pull_model(self, client):
        pulled_models = [model["name"] for model in client.list()["models"]]
        if self.model not in pulled_models:
            logger.info("No ready embedding model found. Downloading...")
            client.pull(self.model)
