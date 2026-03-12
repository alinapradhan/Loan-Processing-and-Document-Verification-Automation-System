# API Documentation

Base URL: `http://localhost:8000/api/v1`

## Endpoints

### `GET /health`
Health check endpoint.

**Response**
```json
{"status": "ok"}
```

### `POST /process-loan-application`
Upload one or many documents as multipart form data.

**Form Data**
- `files`: multiple files (`.png`, `.jpg`, `.jpeg`, `.pdf`)

**Sample cURL**
```bash
curl -X POST "http://localhost:8000/api/v1/process-loan-application" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@sample_test_documents/aadhaar_sample.txt" \
  -F "files=@sample_test_documents/pan_sample.txt"
```

**Response (Example)**
```json
{
  "application_id": 1,
  "extraction_results": [],
  "consolidated_fields": {
    "name": "Ravi Kumar",
    "aadhaar_number": "123412341234",
    "pan_number": "ABCDE1234F",
    "monthly_income": 75000,
    "employer": "ABC Technologies",
    "account_balance": 185000,
    "employment_status": "Salaried"
  },
  "validation": {
    "is_valid": true,
    "issues": []
  },
  "score": {
    "score": 72,
    "approval_status": "REVIEW",
    "factors": {
      "income_points": 30,
      "balance_points": 20,
      "employment_points": 20,
      "risk_penalty": 0
    }
  }
}
```
