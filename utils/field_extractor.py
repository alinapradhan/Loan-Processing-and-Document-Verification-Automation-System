import re
from typing import Dict, Optional


def _extract_first(pattern: str, text: str) -> Optional[str]:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return match.group(1).strip() if match else None


def _extract_amount(pattern: str, text: str) -> Optional[float]:
    value = _extract_first(pattern, text)
    if not value:
        return None
    value = value.replace(",", "")
    try:
        return float(value)
    except ValueError:
        return None


def extract_fields(text: str) -> Dict[str, Optional[object]]:
    aadhaar_match = re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", text)
    pan_match = re.search(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", text)

    return {
        "name": _extract_first(r"Name\s*[:\-]\s*([A-Za-z ]+)", text),
        "aadhaar_number": aadhaar_match.group(0).replace(" ", "") if aadhaar_match else None,
        "pan_number": pan_match.group(0) if pan_match else None,
        "monthly_income": _extract_amount(r"(?:Net Salary|Monthly Income)\s*[:\-]?\s*([0-9,]+(?:\.[0-9]+)?)", text),
        "employer": _extract_first(r"Employer\s*[:\-]\s*([A-Za-z0-9 &,.]+)", text),
        "account_balance": _extract_amount(r"(?:Balance|Closing Balance)\s*[:\-]?\s*([0-9,]+(?:\.[0-9]+)?)", text),
        "employment_status": _extract_first(r"Employment Status\s*[:\-]\s*([A-Za-z ]+)", text),
    }
