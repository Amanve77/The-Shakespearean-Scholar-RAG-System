from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import chromadb
import requests
import os

CHROMA_DB_DIR = "./julius_chroma_db"
EMBED_MODEL_NAME = "BAAI/bge-base-en-v1.5"
TOP_K = 5
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = "llama3"  

app = FastAPI(title="Shakespearean Scholar RAG API")

class QueryRequest(BaseModel):
    query: str
    top_k: int = TOP_K 

class SourceChunk(BaseModel):
    chunk: str
    metadata: dict

class QueryResponse(BaseModel):
    answer: str
    sources: list

model = SentenceTransformer(EMBED_MODEL_NAME)
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
collection = chroma_client.get_or_create_collection("julius_chunks")

SYSTEM_PROMPT = (
    "You are a world-class Shakespearean scholar, writing for advanced high school and undergraduate literature students.\n"
    "- Only use the play excerpts provided (sources).\n"
    "- Cite each answer with inline [SOURCE N] references.\n"
    "- Do NOT add facts, interpretations or lines outside context.\n"
    "- Response tone is academic, clear, and insightful.\n"
)

def format_context_for_prompt(chunks):
    context = ""
    for i, doc in enumerate(chunks):
        context += f"SOURCE[{i+1}]:\n{doc.strip()}\n\n"
    return context

def generate_llm_answer(query: str, top_chunks: list, model_name: str = OLLAMA_MODEL):
    context = format_context_for_prompt(top_chunks)
    user_prompt = (
        f"{SYSTEM_PROMPT}\n"
        f"User question: {query}\n"
        f"Sources:\n{context}\n"
        f"Write an answer."
    )
    payload = {
        "model": model_name,
        "prompt": user_prompt,
        "stream": False
    }
    resp = requests.post(OLLAMA_API_URL, json=payload)
    answer = resp.json()["response"]
    return answer

@app.post("/query", response_model=QueryResponse)
async def rag_query(request: QueryRequest):
    query_emb = model.encode([request.query])
    results = collection.query(
        query_embeddings=query_emb,
        n_results=request.top_k,
        include=['documents', 'metadatas', 'distances']
    )
    docs = results['documents'][0]
    metas = results['metadatas'][0]
    sources = [
        {"chunk": doc, "metadata": meta}
        for doc, meta in zip(docs, metas)
    ]
    answer = generate_llm_answer(request.query, docs)
    return {"answer": answer, "sources": sources}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
