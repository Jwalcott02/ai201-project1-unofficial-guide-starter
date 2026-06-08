import chromadb
from sentence_transformers import SentenceTransformer

# Load model and connect to existing ChromaDB
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="fau_cs_guide")

def retrieve(query, k=5):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )
    return results

def test_queries():
    test_questions = [
        "What are Professor Taebi's exams like?",
        "What should I know before taking Professor Petrie?",
        "Who should I take for Data Mining at FAU?",
        "What are the prerequisites for COT4400 Algorithms?",
        "What courses are required for the FAU CS degree?"
    ]

    for question in test_questions:
        print(f"\n{'='*60}")
        print(f"QUERY: {question}")
        print('='*60)
        results = retrieve(question)
        for i, (doc, meta, dist) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )):
            print(f"\nResult {i+1} | Source: {meta['source']} | Distance: {dist:.3f}")
            print(doc[:300])
            print("...")

if __name__ == "__main__":
    test_queries()