import os

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv

from chat import routes as chat_routes
from core import routes as core_routes
from pdf import routes as pdf_routes
from core.middlewares import CustomErrorHandlingMiddleware
from core.rate_limiter import limiter

load_dotenv()

tags_metadata = [
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

app = FastAPI(
    debug=bool(os.getenv("DEBUG", False)),
    title="Chat with PDF | Huseyin Das",
    summary="Application that lets you interact with PDF files via chat APIs.",
    description="""
        Welcome to the Chat with PDF API! 📄💬

        This API lets you effortlessly interact with PDF files through chat.
        From uploading to managing PDFs, you can engage in a conversation
        directly with your documents. Whether you're handling a single page
        or an entire file, we've got you covered!
    """,
    version="0.0.1",
    openapi_tags=tags_metadata,
    redirect_slashes=True,
    contact={
        "name": "Huseyin Das",
        "url": "https://www.linkedin.com/in/huseyindas/",
        "email": "hsyndass@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    root_path="/v1",
    root_path_in_servers=True

)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(CustomErrorHandlingMiddleware)

app.include_router(chat_routes.router, prefix="/chat", tags=["Chat"])
app.include_router(core_routes.router, prefix="", tags=["Core"])
app.include_router(pdf_routes.router, prefix="/pdf", tags=["Pdf"])
