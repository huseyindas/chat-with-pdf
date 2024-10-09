from fastapi import APIRouter, UploadFile, HTTPException, Request

from core.loader import Loader
from core.consts import MAX_FILE_SIZE_UPLOAD
from pdf.schemas import UploadPDFResponse
from core.rate_limiter import limiter

router = APIRouter()


@router.post(
    "/",
    description="Endpoint for uploading and registering a PDF",
    response_model=UploadPDFResponse
)
@limiter.limit("1/minute")
async def upload_pdf(request: Request, file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file!"
        )

    if file.size > MAX_FILE_SIZE_UPLOAD:
        raise HTTPException(
            status_code=413,
            detail=(
                "The PDF file you want to upload "
                f"cannot be larger than {MAX_FILE_SIZE_UPLOAD/1024/1024}MB!"
            )
        )

    loader = Loader(file=file)
    pdf_id = await loader.commit()
    return {
        "pdf_id": pdf_id
    }
