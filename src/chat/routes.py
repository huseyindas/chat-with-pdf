from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ai.chain import Chain
from chat.schemas import (
    ChatRequest,
    ChatResponse
)
from core.database import get_db
from core.rate_limiter import limiter
from core.redis import cache


router = APIRouter()


@router.post(
    "/{pdf_id}",
    description="Endpoint for chat with PDF.",
    response_model=ChatResponse
)
@limiter.limit("3/minute")
def chat(
        request: Request,
        pdf_id: UUID,
        chat_request: ChatRequest,
        db: Session = Depends(get_db),
        redis_client: cache = Depends(cache)
        ):

    if (cached_response := redis_client.get(f"{pdf_id}_{chat_request.message.lower()}")) is not None:
        return JSONResponse(
            status_code=200,
            content={
                "response": str(cached_response)
            }
        )

    chain = Chain()
    check_pdf = chain.check_source_on_db(db, pdf_id)

    if check_pdf:
        response = chain.chat(
            message=chat_request.message,
            source=pdf_id,
        )
        redis_client.set(
            f"{pdf_id}_{chat_request.message.lower()}",
            response["answer"]
        )
        return JSONResponse(
            status_code=200,
            content={
                "response": response["answer"]
            }
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="No document with this pdf id was found."
        )
