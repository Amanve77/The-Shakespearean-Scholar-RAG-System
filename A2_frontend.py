import streamlit as st
import requests

st.title("Julius Caesar RAG Scholar 🌟")

query = st.text_area("Enter your Shakespeare question:", height=80)

if st.button("Ask"):
    with st.spinner("Thinking..."):
        response = requests.post(
            "http://assignment2-api:8000/query",
            json={"query": query},
            timeout=900
        )
        if response.ok:
            data = response.json()
            st.markdown("**Answer:**")
            st.write(data.get("answer", ""))
            st.markdown("**Source Chunks:**")
            for src in data.get("sources", []):
                text = src.get("chunk") if isinstance(src, dict) else str(src)
                st.code(text)
        else:
            st.error("Error: Could not get an answer from the API backend.")
