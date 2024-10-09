import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class GlobalConfig(BaseSettings):
    title: str = "Chat with PDF | Huseyin Das"
    version: str = "1.0.0"
    summary: str = (
        "Application that lets you interact with PDF files via chat APIs."
    )
    description: str = """
        Welcome to the Chat with PDF API! 📄💬

        This API lets you effortlessly interact with PDF files through chat.
        From uploading to managing PDFs, you can engage in a conversation
        directly with your documents. Whether you're handling a single page
        or an entire file, we've got you covered!
    """
    root_path: str = "/v1"
    openapi_tags: list = [
        {
            "name": "Core",
            "description": (
                "Common routes like health check and other shared operations."
            ),
        },
        {
            "name": "Chat",
            "description": (
                "Routes for user interactions and chat functionality."
            ),
        },
        {
            "name": "Pdf",
            "description": (
                "Routes for managing PDF files for conversations."
            ),
        }
    ]
    redirect_slashes: bool = True
    root_path_in_servers: bool = True
    contact: dict = {
        "name": "Huseyin Das",
        "url": "https://www.linkedin.com/in/huseyindas/",
        "email": "hsyndass@gmail.com",
    }
    license_info: dict = {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
    debug: bool = os.environ.get("DEBUG")

    ollama_model: str = os.environ.get("OLLAMA_MODEL")
    ollama_host: str = os.environ.get("OLLAMA_HOST")

    postgres_user: str = os.environ.get("POSTGRES_USER")
    postgres_password: str = os.environ.get("POSTGRES_PASSWORD")
    postgres_server: str = os.environ.get("POSTGRES_SERVER")
    postgres_port: int = int(os.environ.get("POSTGRES_PORT"))
    postgres_db: str = os.environ.get("POSTGRES_DB")

    redis_server: str = os.environ.get("REDIS_SERVER")
    redis_port: int = int(os.environ.get("REDIS_PORT"))

    max_file_size_upload: int = 10485760  # 10MB

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"


settings = GlobalConfig()
