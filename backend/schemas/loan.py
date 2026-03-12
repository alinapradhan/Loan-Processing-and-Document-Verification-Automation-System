from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ExtractedFields(BaseModel):
    name: Optional[str] = None
    aadhaar_number: Optional[str] = None
    pan_number: Optional[str] = None
    monthly_income: Optional[float] = None
    employer: Optional[str] = None
    account_balance: Optional[float] = None
    employment_status: Optional[str] = None


class DocumentExtractionResult(BaseModel):
    filename: str
    document_type: str
    extracted_text: str
    extracted_fields: ExtractedFields


class ValidationResult(BaseModel):
    is_valid: bool
    issues: List[str] = Field(default_factory=list)


class ScoreResult(BaseModel):
    score: float
    approval_status: str
    factors: Dict[str, float]


class LoanProcessResponse(BaseModel):
    application_id: int
    extraction_results: List[DocumentExtractionResult]
    consolidated_fields: ExtractedFields
    validation: ValidationResult
    score: ScoreResult
