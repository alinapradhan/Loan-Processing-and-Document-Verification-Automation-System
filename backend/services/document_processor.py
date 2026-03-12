import json
from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session

from db.config import settings
from db.models import LoanApplicationRecord
from ocr.ocr_engine import OCREngine
from schemas.loan import DocumentExtractionResult, ExtractedFields, LoanProcessResponse, ScoreResult, ValidationResult
from utils.field_extractor import extract_fields
from utils.scoring import calculate_loan_score
from utils.validators import validate_consistency


class DocumentProcessorService:
    def __init__(self):
        self.ocr_engine = OCREngine(engine=settings.ocr_engine, tesseract_cmd=settings.tesseract_cmd)

    @staticmethod
    def _detect_doc_type(filename: str) -> str:
        name = filename.lower()
        if "aadhaar" in name:
            return "aadhaar"
        if "pan" in name:
            return "pan"
        if "salary" in name:
            return "salary_slip"
        if "statement" in name or "bank" in name:
            return "bank_statement"
        if "application" in name or "loan" in name:
            return "loan_application"
        return "unknown"

    async def process_application(self, files: List[UploadFile], db: Session) -> LoanProcessResponse:
        extraction_results: List[DocumentExtractionResult] = []
        consolidated = {
            "name": None,
            "aadhaar_number": None,
            "pan_number": None,
            "monthly_income": None,
            "employer": None,
            "account_balance": None,
            "employment_status": None,
        }

        for file in files:
            data = await file.read()
            if file.filename.lower().endswith(".pdf"):
                text = self.ocr_engine.extract_text_from_pdf(data)
            else:
                text = self.ocr_engine.extract_text(data)

            fields = extract_fields(text)
            for key, value in fields.items():
                if value is not None:
                    consolidated[key] = value

            extraction_results.append(
                DocumentExtractionResult(
                    filename=file.filename,
                    document_type=self._detect_doc_type(file.filename),
                    extracted_text=text,
                    extracted_fields=ExtractedFields(**fields),
                )
            )

        issues = validate_consistency(consolidated)
        validation = ValidationResult(is_valid=len(issues) == 0, issues=issues)

        score_data = calculate_loan_score(consolidated)
        score = ScoreResult(**score_data)

        record = LoanApplicationRecord(
            applicant_name=consolidated.get("name"),
            aadhaar_number=consolidated.get("aadhaar_number"),
            pan_number=consolidated.get("pan_number"),
            monthly_income=consolidated.get("monthly_income"),
            employer=consolidated.get("employer"),
            account_balance=consolidated.get("account_balance"),
            employment_status=consolidated.get("employment_status"),
            eligibility_score=score.score,
            approval_status=score.approval_status,
            validation_issues=json.dumps(issues),
            extracted_payload=json.dumps([result.model_dump() for result in extraction_results]),
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        return LoanProcessResponse(
            application_id=record.id,
            extraction_results=extraction_results,
            consolidated_fields=ExtractedFields(**consolidated),
            validation=validation,
            score=score,
        )
