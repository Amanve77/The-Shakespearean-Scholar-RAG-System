FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY A2_RAG_API.py .
COPY julius_chroma_db/ ./julius_chroma_db/

EXPOSE 8000

CMD ["uvicorn", "A2_RAG_API:app", "--host", "0.0.0.0", "--port", "8000"]
