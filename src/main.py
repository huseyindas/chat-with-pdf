from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv

from chat import routes as chat_routes
from core import routes as core_routes
from pdf import routes as pdf_routes
from core.middlewares import (
    CustomErrorHandlingMiddleware,
    CustomTimeoutHandlingMiddleware
)
from core.rate_limiter import limiter
from core.config import settings

load_dotenv()


app = FastAPI(
    debug=settings.debug,
    title=settings.title,
    summary=settings.summary,
    description=settings.description,
    version=settings.version,
    openapi_tags=settings.openapi_tags,
    redirect_slashes=settings.redirect_slashes,
    contact=settings.contact,
    license_info=settings.license_info,
    root_path=settings.root_path,
    root_path_in_servers=settings.root_path_in_servers
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(CustomErrorHandlingMiddleware)
app.add_middleware(CustomTimeoutHandlingMiddleware)

app.include_router(chat_routes.router, prefix="/chat", tags=["Chat"])
app.include_router(core_routes.router, prefix="", tags=["Core"])
app.include_router(pdf_routes.router, prefix="/pdf", tags=["Pdf"])
