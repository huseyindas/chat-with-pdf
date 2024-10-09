from fastapi import APIRouter, UploadFile, HTTPException, Request

from ai.loader import Loader
from pdf.schemas import UploadPDFResponse
from core.rate_limiter import limiter
from core.config import settings

router = APIRouter()


@router.post(
    "/",
    description="Endpoint for uploading and registering a PDF",
    response_model=UploadPDFResponse
)
@limiter.limit("3/minute")
async def upload_pdf(request: Request, file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file!"
        )

    if file.size > settings.max_file_size_upload:
        raise HTTPException(
            status_code=413,
            detail=(
                "The PDF file you want to upload "
                "cannot be larger than "
                f"{settings.max_file_size_upload/1024/1024}MB!"
            )
        )

    loader = Loader(file=file)
    pdf_id = await loader.commit()
    return {
        "pdf_id": pdf_id
    }
