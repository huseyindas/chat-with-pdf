import os
import uuid
import logging

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from ai.pgvector import PGVectorUtils
from core.config import settings


class Loader:

    def __init__(self, file) -> None:
        self.pdf_id = uuid.uuid4()
        self.file = file
        self.file_location = f"tmp/documents/{file.filename}"
        self.vectorstore_utils = PGVectorUtils(settings.database_url)
        self.manage_directory("create")

    def manage_directory(self, action):
        directory = os.path.dirname(self.file_location)

        if action == "create":
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
        elif action == "delete":
            if os.path.exists(self.file_location):
                os.remove(self.file_location)
            else:
                logging.warning(
                    f"File {self.file_location} not found, no action taken."
                )
        else:
            raise ValueError(
                f"Invalid action '{action}'. Use 'create' or 'delete'."
            )

    async def write_pdf_on_storage(self):
        with open(self.file_location, "wb") as f:
            content = await self.file.read()
            f.write(content)

    def load_docs(self):
        loader = PyPDFLoader(
            self.file_location
        )
        docs = loader.load()
        return docs

    def split_data(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        all_splits = text_splitter.split_documents(docs)
        return all_splits

    def data_preprocess(self, all_splits_data):
        metadata = all_splits_data[0].metadata
        metadata["pdf_id"] = self.pdf_id.hex

        documents = []
        for data in all_splits_data:
            document = Document(
                page_content=data.page_content.replace('\x00', ''),
                metadata=metadata,
            )
            documents.append(document)
        return documents

    async def commit(self):
        await self.write_pdf_on_storage()
        docs = self.load_docs()
        all_splits_data = self.split_data(docs)
        prepared_data = self.data_preprocess(all_splits_data)
        self.vectorstore_utils.add_docs_to_vectorstore(prepared_data)
        self.manage_directory("delete")

        return self.pdf_id
