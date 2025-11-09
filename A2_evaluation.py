import requests
import json

with open("evaluation.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

results = []
for q in questions:
    resp = requests.post("http://localhost:8000/query", json={"query": q["question"]})
    print(f"Question: {q['question']}, Status: {resp.status_code}")
    try:
        ans = resp.json().get("answer", "")
    except Exception:
        print("Non-JSON response:", resp.text) 
        ans = "" 
    results.append({
        "question": q["question"],
        "ideal_answer": q["ideal_answer"],
        "systemanswer": ans
    })

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
