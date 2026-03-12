from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from db.database import Base


class LoanApplicationRecord(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    applicant_name = Column(String(255), nullable=True)
    aadhaar_number = Column(String(20), nullable=True)
    pan_number = Column(String(20), nullable=True)
    monthly_income = Column(Float, nullable=True)
    employer = Column(String(255), nullable=True)
    account_balance = Column(Float, nullable=True)
    employment_status = Column(String(50), nullable=True)
    eligibility_score = Column(Float, nullable=False, default=0)
    approval_status = Column(String(20), nullable=False, default="REVIEW")
    validation_issues = Column(Text, nullable=True)
    extracted_payload = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
