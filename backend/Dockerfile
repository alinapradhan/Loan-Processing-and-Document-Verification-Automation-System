FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y tesseract-ocr libgl1 && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

COPY backend /app/backend
COPY ocr /app/ocr
COPY utils /app/utils

WORKDIR /app/backend
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
