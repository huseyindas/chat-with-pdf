from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_postgres.vectorstores import _get_embedding_collection_store

from ai.llm import LLM
from ai.pgvector import PGVectorUtils
from core.config import settings
from core.logging import logger


class Chain:

    def __init__(self) -> None:
        self.llm = LLM()
        self.vectorstore_utils = PGVectorUtils(settings.database_url)

    def get_chat_template(self):
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are an assistant for question-answering tasks. "
                "Use the following pieces of retrieved context to answer "
                "the question. If you don't know the answer, say that you "
                "don't know."
                "\n\n"
                "{context}"
            ),
            ("user", "{input}"),
        ])
        return prompt

    def get_rag_chain(self, source):
        model = self.llm.get_model()
        retriever = self.vectorstore_utils.get_retriever(source=source)
        chat_template = self.get_chat_template()

        question_answer_chain = create_stuff_documents_chain(
            model, chat_template
        )
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        return rag_chain, retriever

    def chat(self, message: str, source):
        rag_chain, retriever = self.get_rag_chain(source)
        response = rag_chain.invoke({
            "input": message,
            "question": RunnablePassthrough(),
            "context": retriever
        })
        return response

    def check_source_on_db(self, db_session, source):
        embedding_model = _get_embedding_collection_store()[0]

        docs = (
            db_session.query(embedding_model)
            .filter(embedding_model.cmetadata["pdf_id"].astext == source.hex)
            .all()
        )
        result = False if docs == [] else True
        if not result:
            logger.warning("No document with this pdf id was found.")
        return result
