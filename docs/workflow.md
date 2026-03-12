# Loan Automation Workflow

```mermaid
flowchart TD
    A[User Uploads Documents via React Dashboard] --> B[FastAPI Upload Endpoint]
    B --> C[OCR Preprocessing with OpenCV]
    C --> D[OCR Extraction Tesseract / PaddleOCR]
    D --> E[Field Extraction Rules]
    E --> F[Validation Aadhaar / PAN / Consistency]
    F --> G[Loan Eligibility Scoring]
    G --> H[Persist to PostgreSQL]
    H --> I[Structured JSON Response]
    I --> J[Dashboard Shows Approval Status]
```

## Steps
1. User uploads loan application document set.
2. Backend applies OCR and extracts raw text.
3. Rule-based parser maps key entities (name, ID, income, balance).
4. Validator checks document quality and consistency.
5. Scoring module computes eligibility and decision state.
6. Data is stored for audit and analytics.
7. UI displays final output and validation alerts.
