from dataclasses import dataclass
from typing import Optional


@dataclass
class LoanApplicationModel:
    name: Optional[str]
    aadhaar_number: Optional[str]
    pan_number: Optional[str]
    monthly_income: Optional[float]
    employer: Optional[str]
    account_balance: Optional[float]
    employment_status: Optional[str]
