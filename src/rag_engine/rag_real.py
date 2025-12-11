import os
import PyPDF2
from groq import Groq
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


# ================================
# 🔹 EMBEDDING MODEL (OPEN-SOURCE)
# ================================
embedder = SentenceTransformer("all-MiniLM-L6-v2")


# ================================
# 🔹 Carregar texto do documento
# ================================
def load_document(path: str) -> str:
    ext = path.split(".")[-1].lower()

    if ext == "txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    elif ext == "pdf":
        reader = PyPDF2.PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    else:
        raise ValueError("Formato não suportado. Use PDF ou TXT.")


# ================================
# 🔹 Chunking (quebra em pedaços)
# ================================
def chunk_text(text: str, size: int = 400) -> list[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), size):
        chunk = " ".join(words[i:i + size])
        chunks.append(chunk)
    return chunks


# ================================
# 🔹 Vetorização (FAISS)
# ================================
class VectorStore:
    def __init__(self):
        self.index = None
        self.chunks = []

    def build(self, chunks: list[str]):
        self.chunks = chunks
        vectors = embedder.encode(chunks)
        self.index = faiss.IndexFlatL2(vectors.shape[1])
        self.index.add(np.array(vectors))

    def search(self, query: str, top_k: int = 3):
        q_vec = embedder.encode([query])
        distances, ids = self.index.search(np.array(q_vec), top_k)
        return [self.chunks[i] for i in ids[0]]


# ================================
# 🔹 Geração com GROQ
# ================================
def generate_answer(context: str, question: str, groq_client: Groq) -> str:
    prompt = f"""
You are a RAG assistant. Use ONLY the provided context to answer.

Context:
{context}

Question:
{question}

Answer:
"""

    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content


# ================================
# 🔹 FUNÇÃO PRINCIPAL DO RAG REAL
# ================================
def run_rag_real(path: str, question: str, groq_client: Groq):
    text = load_document(path)
    chunks = chunk_text(text)

    store = VectorStore()
    store.build(chunks)

    top_chunks = store.search(question, top_k=3)
    context = "\n\n".join(top_chunks)

    answer = generate_answer(context, question, groq_client)

    return answer
