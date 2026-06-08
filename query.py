import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize models and clients
model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="fau_cs_guide")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def retrieve(query, k=5):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )
    return results

def ask(question):
    # Retrieve relevant chunks
    results = retrieve(question)
    chunks = results["documents"][0]
    sources = list(set([meta["source"] for meta in results["metadatas"][0]]))

    # Build context from chunks
    context = "\n\n---\n\n".join(chunks)

    # Grounded prompt
    system_prompt = """You are a helpful guide for FAU Computer Science students.
Answer the question using ONLY the information provided in the documents below.
Do not use any outside knowledge or general information.
If the documents do not contain enough information to answer the question, say exactly:
'I don't have enough information in my documents to answer that.'
Always be specific and cite details from the documents."""

    user_prompt = f"""Documents:
{context}

Question: {question}

Answer based only on the documents above:"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1000
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources
    }