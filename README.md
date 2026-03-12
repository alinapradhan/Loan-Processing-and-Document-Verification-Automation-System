# Loan Processing and Document Verification Automation System

Production-style reference implementation for automating loan document intake, OCR-based data extraction, KYC validation, and loan eligibility scoring in a banking/fintech workflow.

## Features

- Upload and classify loan documents:
  - Aadhaar card
  - PAN card
  - Salary slip
  - Bank statement
  - Loan application form
- OCR pipeline using **Tesseract**, **PaddleOCR**, and **OpenCV** preprocessing.
- FastAPI backend for upload, extraction, validation, and scoring.
- Validation rules for Aadhaar/PAN and cross-document consistency checks.
- Loan eligibility score based on income, bank balance, and employment status.
- PostgreSQL persistence using SQLAlchemy.
- React dashboard for document upload and approval status display.
- Dockerized deployment with Docker Compose.
- Architecture/workflow diagram and API docs.

---

## Repository Structure
  
```
.
├── backend/
│   ├── api/
│   ├── services/
│   ├── db/
│   ├── schemas/
│   └── main.py
├── frontend/
│   ├── src/
│   └── public/
├── models/
├── ocr/
├── utils/
├── docs/
│   ├── API.md
│   └── workflow.md
├── sample_test_documents/
├── docker-compose.yml
└── README.md
```

---

## Quick Start

### 1) Local (without Docker)

#### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev -- --host
```

Frontend runs on `http://localhost:5173`, backend on `http://localhost:8000`.

### 2) Docker Compose

```bash
docker compose up --build
```

Services:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- PostgreSQL: `localhost:5432`

---

## OCR Engine Selection

By default, Tesseract is used. You can switch with environment variable:

- `OCR_ENGINE=tesseract`
- `OCR_ENGINE=paddle`

Also configure:
- `TESSERACT_CMD` (optional custom path)

---

## API Usage

Interactive docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Detailed API reference: `docs/API.md`

---

## Workflow Diagram

Pipeline and process flow: `docs/workflow.md`

---

## Sample Test Documents

Placeholders and test instructions are under `sample_test_documents/`.

---

## Production Notes

- Add secure object storage (S3/Azure Blob) for uploaded docs.
- Integrate a queue (Celery/RQ) for asynchronous OCR processing.
- Add audit trail and role-based access controls.
- Encrypt sensitive data and implement data retention policies.
