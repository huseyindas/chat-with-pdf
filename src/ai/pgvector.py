from langchain_postgres import PGVector

from ai.embedding import CustomOllamaEmbeddings
from core.config import settings


class PGVectorUtils:

    def __init__(self, pgvector_dsn: str = settings.database_url) -> None:
        self.pgvector_dsn = pgvector_dsn
        self.embedding = CustomOllamaEmbeddings()
        self.retriever_score_threshold = 0.5
        self.retriever_k = 2

    def get_vectorstore(self):
        vectorstore = PGVector(
            embeddings=self.embedding,
            connection=self.pgvector_dsn
            )
        return vectorstore

    def get_retriever(self, source=None):
        vectorstore = self.get_vectorstore()
        vectorstore.as_retriever
        retriever = vectorstore.as_retriever(
            search_kwargs={
                "filter": {"pdf_id": source.hex}
            }
        )
        return retriever

    def add_docs_to_vectorstore(self, all_splits_data):
        vectorstore = self.get_vectorstore()

        vectorstore = vectorstore.add_documents(
            documents=all_splits_data,
            embedding=self.embedding,
            connection=self.pgvector_dsn
        )
        return vectorstore
