import os
import faiss
import numpy as np
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from PyPDF2 import PdfReader

# =============================
# 🔹 CARREGAR VARIÁVEIS DE AMBIENTE
# =============================
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =============================
# 🔹 1) CARREGAR DOCUMENTOS
# =============================
def load_text_from_file(path: str) -> str:
    if path.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    if path.endswith(".pdf"):
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text

    raise ValueError("Formato não suportado. Use PDF ou TXT.")


# =============================
# 🔹 2) EMBEDDINGS OPENAI
# =============================
def embed(texts: List[str]) -> np.ndarray:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    vectors = [item.embedding for item in response.data]
    return np.array(vectors).astype("float32")


# =============================
# 🔹 3) VECTOR STORE COM FAISS
# =============================
class RAGStore:
    def __init__(self):
        self.index = None
        self.docs = []

    def build(self, documents: List[str]):
        self.docs = documents
        vectors = embed(documents)

        dim = vectors.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(vectors)

    def search(self, query: str, k: int = 3):
        q_vec = embed([query])
        distances, indices = self.index.search(q_vec, k)

        return [self.docs[i] for i in indices[0]]


# =============================
# 🔹 4) GERAR RESPOSTA COM CONTEXTO
# =============================
def generate_answer(context: str, question: str) -> str:
    prompt = f"""
Você é um assistente especialista.
Use APENAS o conteúdo abaixo para responder.

CONTEXTO:
{context}

PERGUNTA:
{question}

RESPOSTA:
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250,
        temperature=0.2,
    )

    return response.choices[0].message.content


# =============================
# 🔹 5) PIPELINE RAG COMPLETO
# =============================
def run_rag_real(file_path: str, question: str) -> str:
    text = load_text_from_file(file_path)

    # Quebrar em partes
    chunks = [text[i:i+800] for i in range(0, len(text), 800)]

    store = RAGStore()
    store.build(chunks)

    results = store.search(question)
    context = "\n---\n".join(results)

    answer = generate_answer(context, question)

    return (
        f"📄 Documento: {file_path}\n\n"
        f"🔍 Contexto recuperado:\n{context}\n\n"
        f"🤖 Resposta gerada:\n{answer}"
    )
