# The Shakespearean Scholar — A Containerized RAG System

---

## 📖 Project Overview

This project implements a full-stack, containerized Retrieval-Augmented Generation (RAG) system that acts as an "Expert Shakespearean Scholar" on *The Tragedy of Julius Caesar* (Folger Edition). It’s designed as an AI tutor for ICSE Class 10 students—answers are academically rigorous, cite sources, and give deep insight.

---

## 📂 Repository Structure

<pre> 
├── A2_Data_ETL.py # ETL, chunking, embeddings
├── processed_chunks.jsonl # Preprocessed, metadata-rich chunks (for ChromaDB)
├── julius-caesar.pdf # Play text (Folger Edition)
├── A2_RAG_API.py # FastAPI backend (RAG orchestrator)
├── A2_Vector_Index.py # Vector database logic
├── evaluation.json # Evaluation testbed (25 factual + 10 analytical Qs)
├── output.json # System answers to evaluation set
├── output_scored.csv/json # Manual (faithfulness/relevancy) scoring
├── A2_evaluation.py # Evaluation automation script
├── A2_raga_eval_convert.py # RAGAs converter 
├── A2_raga_eval_run.py # RAGAs metrics script
├── raga_input.json # RAGAs-ready input
├── A2_frontend.py # Streamlit UI
├── Dockerfile # Backend/ETL build
├── Dockerfile.frontend # Frontend build
├── docker-compose.yml # Service orchestration (API, ollama, frontend)
├── requirements.txt # Python dependencies
├── julius_chroma_db/ # ChromaDB persistent store (mounted volume)
</pre>
---

## 🛠️ Components

- **Backend**: FastAPI (REST API for RAG pipeline orchestrating embedding, retrieval, LLM, citation)
- **LLM**: Open-source Ollama (e.g. Llama-3-8B or Mistral-7B), or Gemini API ready (optional)
- **Vector Store**: ChromaDB with semantic, logical chunks and rich metadata
- **Embeddings**: bge-base-en-v1.5
- **Frontend**: Streamlit UI for interactive querying
- **Dockerized**: All components launch in one command via Docker Compose

---

## 🚀 How to Run (Quickstart)

**Requirements:**  
- Docker & Docker Compose installed (any OS)

**Steps:**
- Clone and launch **all services (API, LLM, frontend)** in one go:
<pre>git clone https://github.com/Amanve77/The-Shakespearean-Scholar-RAG-System.git
cd The-Shakespearean-Scholar-RAG-System
docker-compose up --build</pre>

- **API Documentation:** Visit [http://localhost:8000/docs](http://localhost:8000/docs)
- **Frontend UI:** Visit [http://localhost:8501](http://localhost:8501)
    - Ask questions, see answers & source chunks

---

## 🛠️ How It Works

- **Backend RAG pipeline:** FastAPI (`A2_RAG_API.py`) executes: vector retrieval → LLM with prompt → grounded answer + citation.
- **ChromaDB:** Holds vector chunks (`processed_chunks.jsonl`) for semantic search.
- **Ollama:** Runs open LLM (Llama-3).
- **Frontend:** Streamlit (`A2_frontend.py`) gives simple academic Q&A interface with citations and full context display.
- **Evaluation:** All system answers to the question testbed in `output.json`/`output_scored.csv`. RAGAs scripts and manual rubric included for grading.
- **Fully reproducible:** All setup/ETL, build, and question answering is scripted and versioned.

---

## 📙 Usage & Evaluation

- **Test the API** in Swagger at `/docs` or POST directly to `/query`:
<pre>
{
"query": "Why does Brutus kill Caesar?"
}
</pre>
- **Try the UI:** Enter your custom question, see sources and answers.
- **Evaluation files provided:** See `evaluation.json`, `output.json`, and `output_scored.csv` for all rubric scores and rationales.
- **RAGAs auto scoring:** Run `A2_raga_eval_convert.py` and `A2_raga_eval_run.py` if you wish to benchmark using external LLMs (manual scores will suffice for grading).

---

## 🛠️ Build & Dev Notes

- All Dockerfiles present—backend and frontend build separately for fast, idempotent launches.
- Backend and frontend work together out-of-the-box (Docker networking).
- Requirements.txt includes only minimal, reproducible dependencies.

---

## 🌀 Troubleshooting

- **Frontend UI not starting:** Use only `docker-compose up --build` — do not run scripts locally unless you have all dependencies!
- **API timeout:** Backend may take time on first load. Increase timeout in the Streamlit code if needed.
- **Model loading:** Make sure Ollama has access to enough RAM/compute for your chosen LLM.
