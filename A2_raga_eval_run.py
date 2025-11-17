from datasets import Dataset
from ragas.evaluation import evaluate
from ragas.metrics import faithfulness, answer_relevancy

import json

import os
os.environ["OPENAI_API_KEY"] = "sk-xxxxx" # Replace with your actual API key

with open("raga_input.json", "r", encoding="utf-8") as f:
    data = json.load(f)

ds = Dataset.from_list(data)

result = evaluate(ds, metrics=[faithfulness, answer_relevancy])
print("----- RAGAs Evaluation Results -----")
print(result)