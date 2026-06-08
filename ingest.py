import os
import pdfplumber
import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="fau_cs_guide")

DOCS_DIR = "./documents"
CHUNK_SIZE = 500
OVERLAP = 50

def load_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def load_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n\n"
    return text

def clean_text(text):
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if len(chunk.strip()) > 0:
            chunks.append(chunk)
        start = end - overlap
    return chunks

def process_documents():
    all_chunks = []
    all_ids = []
    all_metadata = []

    for filename in os.listdir(DOCS_DIR):
        filepath = os.path.join(DOCS_DIR, filename)

        if filename.endswith(".txt"):
            raw = load_txt(filepath)
        elif filename.endswith(".pdf"):
            raw = load_pdf(filepath)
        else:
            continue

        cleaned = clean_text(raw)
        chunks = chunk_text(cleaned)

        print(f"{filename}: {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            chunk_id = f"{filename}_chunk_{i}"
            all_chunks.append(chunk)
            all_ids.append(chunk_id)
            all_metadata.append({"source": filename})

    print(f"\nEmbedding {len(all_chunks)} total chunks...")
    embeddings = model.encode(all_chunks).tolist()

    collection.add(
        documents=all_chunks,
        embeddings=embeddings,
        ids=all_ids,
        metadatas=all_metadata
    )

    print(f"\nDone! {len(all_chunks)} chunks stored in ChromaDB.")

    print("\n--- 5 SAMPLE CHUNKS ---")
    for chunk in all_chunks[:5]:
        print("\n" + chunk)
        print("-" * 40)

if __name__ == "__main__":
    process_documents()