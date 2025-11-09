import json
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

CHUNKS_PATH = "processed_chunks.jsonl"
CHROMA_DB_DIR = "./julius_chroma_db"
EMBED_MODEL_NAME = "BAAI/bge-base-en-v1.5"

def load_chunks(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def get_embeddings(texts, model_name):
    model = SentenceTransformer(model_name)
    return model.encode(texts, show_progress_bar=True, batch_size=32)

def create_chroma_collection(embeddings, chunks, db_dir):
    chroma_client = chromadb.PersistentClient(path=db_dir)
    collection = chroma_client.get_or_create_collection("julius_chunks")
    ids = [chunk["chunk_id"] for chunk in chunks]
    docs = [chunk["text"] for chunk in chunks]
    metadatas = [{k: v for k, v in chunk.items() if k not in ("chunk_id", "text")} for chunk in chunks]
    collection.add(
        embeddings=embeddings,
        documents=docs,
        metadatas=metadatas,
        ids=ids
    )
    return collection

def demo_query(collection, model, query_text, top_k=3):
    query_emb = model.encode([query_text])
    results = collection.query(
        query_embeddings=query_emb,
        n_results=top_k,
        include=['metadatas', 'documents', 'distances']
    )
    for i, (doc, meta, dist) in enumerate(zip(results['documents'][0], results['metadatas'][0], results['distances'][0])):
        print(f"\n[{i+1}] Score: {dist:.4f}\nText: {doc}\nMetadata: {meta}")

def main():
    print("\n--- Phase 2: Embedding and Indexing ---")
    chunks = load_chunks(CHUNKS_PATH)
    print(f"Loaded {len(chunks)} chunks.")

    print(f"Loading embedding model: {EMBED_MODEL_NAME}")
    model = SentenceTransformer(EMBED_MODEL_NAME)

    print("Embedding chunk texts...")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = get_embeddings(texts, EMBED_MODEL_NAME)

    print("Indexing into ChromaDB...")
    collection = create_chroma_collection(embeddings, chunks, CHROMA_DB_DIR)
    print(f"\n✓ Indexed {len(chunks)} chunks into ChromaDB at '{CHROMA_DB_DIR}'.")

    print("\nDemo retrieval (top 3 for query):")
    demo_query(collection, model, "Where does Brutus join the conspiracy?", top_k=3)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        traceback.print_exc()
