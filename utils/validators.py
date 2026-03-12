import re
from typing import Dict, List


def validate_aadhaar(aadhaar_number: str | None) -> bool:
    if not aadhaar_number:
        return False
    return bool(re.fullmatch(r"\d{12}", aadhaar_number))


def validate_pan(pan_number: str | None) -> bool:
    if not pan_number:
        return False
    return bool(re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", pan_number))


def validate_consistency(fields: Dict[str, object]) -> List[str]:
    issues: List[str] = []

    if not validate_aadhaar(fields.get("aadhaar_number")):
        issues.append("Invalid or missing Aadhaar number format")

    if not validate_pan(fields.get("pan_number")):
        issues.append("Invalid or missing PAN number format")

    if not fields.get("name"):
        issues.append("Applicant name missing")

    monthly_income = fields.get("monthly_income")
    account_balance = fields.get("account_balance")

    if monthly_income is None:
        issues.append("Monthly income missing")

    if account_balance is None:
        issues.append("Account balance missing")

    if isinstance(monthly_income, (int, float)) and monthly_income <= 0:
        issues.append("Monthly income must be positive")

    if isinstance(account_balance, (int, float)) and account_balance < 0:
        issues.append("Account balance cannot be negative")

    return issues
