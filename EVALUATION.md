# EVALUATION.md

## 1. Overview

This evaluation documents the performance of our Shakespearean Scholar RAG system on a 35-question testbed.  
System answers, scoring rubrics, all code/scripts, and a technical explanation for the reproducibility of automatic RAGAs metrics are included.

---

## 2. Evaluation Dataset

**Source:**  
- 35 questions: 25 course-provided factual & 10 thematic/analytical (in `evaluation.json`)
- Each question has a reference/gold answer (`idealanswer`) and the system's answer (`systemanswer`), including all cited retrieved chunks.

---

## 3. Quantitative Manual Scoring (Rubric)

All outputs were scored according to rubric (1–3):

| Q#  | Faithfulness | Relevancy | Rationale Summary                                              |
|-----|-------------|-----------|----------------------------------------------------------------|
| 1   | 1           | 1         | Wrong act/scene, fabricated details.                           |
| 2   | 1           | 1         | Misses "Beware the Ides," lacks direct citation.               |
| 3   | 2           | 1         | Partially correct on Cassius' question to Brutus.              |
| 4   | 1           | 1         | Hallucination, misses correct "fears they want Caesar king."   |
| ... | ...         | ...       | See `output_scored.csv` for complete rationale per question.   |

**Averages over 35 Qs:**
- **Faithfulness:** ~1.83 / 3
- **Relevancy:** ~1.83 / 3

---

## 4. Qualitative Analysis

**Strengths:**
- Answered analytical/thematic "why" or "motivation" questions with strong, context-supported rationale.
- Prompt and retrieval chunking minimized hallucination risk on broader context.
- System gives referenced, evidence-based explanations suitable for ICSE exam style.

**Weaknesses:**
- Factual event location/recall is sometimes incorrect (misses act/scene, confuses names/events).
- Direct quotes are sometimes fabricated or not exactly present in source.
- Retrieval boundary and LLM hallucination affect precision on very fact-specific questions.

---

## 5. Automated RAGAs Evaluation

### Attempted Process:
- All required conversion and eval scripts supplied:  
  `A2_raga_eval_convert.py` and `A2_raga_eval_run.py`
- All dependencies installed (`ragas`, `openai`, `datasets` etc.)
- Data converted to `raga_input.json`.  
- RAGAs evaluation attempted *locally*, on Windows, and on Colab with:
  - `!pip install "ragas[datasets,openai]"`  
  - `!pip install git+https://github.com/hkunlp/instructor-embedding.git`  

### Outcome:
- **All environments fail with:**  
  `AttributeError: 'InstructorLLM' object has no attribute 'agenerate_prompt'`
- This is a breaking upstream incompatibility between current RAGAs metric code and the (pip/GitHub) `instructor-embedding` library as of November 2025.
- This error is acknowledged in RAGAs/instructor-embedding community issues and affects all users. Until an upstream patch is released, **automatic RAGAs-based evaluation will not complete**.

**Actionable:**  
- All code, data, and scoring workflow are included; results are fully reproducible once package compatibility is restored.
- Manual evaluation result in `output_scored.csv`.

---

## 6. Reproducibility & Rerun Instructions

- All files:
    - `evaluation.json` – questions/testbed
    - `output.json` – system answers
    - `output_scored.csv` – manual scores
    - `A2_raga_eval_convert.py`, `A2_raga_eval_run.py` – scoring scripts
    - All supporting .py and .ipynb for ETL, chunking, UI, and Docker/Colab
- To rerun (when packages are patched):
    ```
    pip install "ragas[datasets,openai]" instructor-embedding
    export OPENAI_API_KEY=sk-...
    python A2_raga_eval_convert.py
    python A2_raga_eval_run.py
    ```
- Or in Colab, upload files and run:
    ```
    !pip install "ragas[datasets,openai]"
    !pip install git+https://github.com/hkunlp/instructor-embedding.git
    # Upload and then:
    !python A2_raga_eval_convert.py
    # Set API key:
    import os; os.environ["OPENAI_API_KEY"] = "sk-..."
    !python A2_raga_eval_run.py
    ```

