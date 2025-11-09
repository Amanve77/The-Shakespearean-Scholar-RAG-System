import json

with open("output.json", "r", encoding="utf-8") as f:
    original = json.load(f)

raga_inputs = []
for row in original:
    contexts = []
    for s in row.get("sources", []):
        if isinstance(s, dict) and "chunk" in s:
            contexts.append(s["chunk"])
        elif isinstance(s, str):
            contexts.append(s)
    raga_inputs.append({
        "question": row["question"],
        "answer": row.get("systemanswer", ""),
        "contexts": contexts,
        "ground_truth": row.get("idealanswer", "")
    })

with open("raga_input.json", "w", encoding="utf-8") as f:
    json.dump(raga_inputs, f, indent=2, ensure_ascii=False)

print("Conversion complete. RAGAs input saved as raga_input.json.")
