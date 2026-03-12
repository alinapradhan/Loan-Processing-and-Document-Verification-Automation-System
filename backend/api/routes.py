from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.loan import LoanProcessResponse
from services.document_processor import DocumentProcessorService

router = APIRouter(prefix="/api/v1", tags=["loan-processing"])
service = DocumentProcessorService()


@router.post("/process-loan-application", response_model=LoanProcessResponse)
async def process_loan_application(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    return await service.process_application(files=files, db=db)


@router.get("/health")
def health_check():
    return {"status": "ok"}
