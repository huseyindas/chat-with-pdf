from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from chat.schemas import (
    ChatRequest,
    ChatResponse
)
from core.chain import Chain
from core.database import get_db
from core.rate_limiter import limiter


router = APIRouter()


@router.post(
    "/{pdf_id}",
    response_model=ChatResponse
)
@limiter.limit("3/minute")
def chat(
        request: Request,
        pdf_id: UUID,
        chat_request: ChatRequest,
        db: Session = Depends(get_db)
        ):
    chain = Chain()
    check_pdf = chain.check_source_on_db(db, pdf_id)
    if check_pdf:
        response = chain.chat(
            message=chat_request.message,
            source=pdf_id,
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
