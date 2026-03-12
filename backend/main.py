import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(str(Path(__file__).resolve().parents[1]))

from api.routes import router
from db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Loan Processing and Document Verification API",
    description="OCR-based loan document processing and eligibility scoring API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Loan Processing API is running"}
