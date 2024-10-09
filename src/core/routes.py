from fastapi import APIRouter, Request

from core.rate_limiter import limiter

router = APIRouter()


@router.get(
    path="/",
    description="Endpoint for health check project.",
)
@limiter.limit("1/second")
async def health(request: Request):
    return {
        "status": True,
    }
