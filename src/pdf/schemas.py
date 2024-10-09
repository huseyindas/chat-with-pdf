from uuid import UUID

from pydantic import BaseModel


class UploadPDFResponse(BaseModel):
    pdf_id: UUID
