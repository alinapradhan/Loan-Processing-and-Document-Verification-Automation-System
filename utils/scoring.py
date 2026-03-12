from typing import Dict, Optional


def _income_points(monthly_income: Optional[float]) -> float:
    if not monthly_income:
        return 0
    if monthly_income >= 120000:
        return 40
    if monthly_income >= 70000:
        return 30
    if monthly_income >= 40000:
        return 20
    return 10


def _balance_points(account_balance: Optional[float]) -> float:
    if account_balance is None:
        return 0
    if account_balance >= 500000:
        return 30
    if account_balance >= 200000:
        return 20
    if account_balance >= 50000:
        return 10
    return 5


def _employment_points(employment_status: Optional[str]) -> float:
    if not employment_status:
        return 5
    normalized = employment_status.strip().lower()
    if normalized in {"permanent", "full time", "salaried"}:
        return 20
    if normalized in {"contract", "self employed"}:
        return 12
    return 5


def calculate_loan_score(fields: Dict[str, object]) -> Dict[str, object]:
    income = _income_points(fields.get("monthly_income"))
    balance = _balance_points(fields.get("account_balance"))
    employment = _employment_points(fields.get("employment_status"))

    risk_penalty = 0
    if not fields.get("pan_number") or not fields.get("aadhaar_number"):
        risk_penalty = 10

    score = max(0, min(100, income + balance + employment - risk_penalty))

    if score >= 75:
        status = "APPROVED"
    elif score >= 55:
        status = "REVIEW"
    else:
        status = "REJECTED"

    return {
        "score": score,
        "approval_status": status,
        "factors": {
            "income_points": income,
            "balance_points": balance,
            "employment_points": employment,
            "risk_penalty": risk_penalty,
        },
    }
