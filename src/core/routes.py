from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from core.rate_limiter import limiter
from core.heatlh import health_check


router = APIRouter()


@router.get(
    path="/health",
    description="Endpoint for health check project.",
)
@limiter.limit("1/second")
async def health(request: Request):
    health_status = health_check()

    return JSONResponse(
        status_code=health_status["status_code"],
        content=health_status
    )
