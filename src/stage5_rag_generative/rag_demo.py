from transformers import pipeline
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from tools.web_search import web_search


def run_stage5_demo():
    print("\n[Stage 5] RAG + Generative AI + Internet\n")

    question = "How should customer data be handled?"

    print(f"🔎 Buscando na internet: {question}\n")
    web_results = web_search(question)

    web_docs = []
    for r in web_results:
        text = f"{r['title']} - {r['snippet']}"
        web_docs.append(text)
        print("🌐", r["title"])

    print("\n📚 Criando base vetorial a partir da Web...\n")

    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedder.encode(web_docs)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    q_embed = embedder.encode([question])
    _, idx = index.search(np.array(q_embed), 1)

    context = web_docs[idx[0][0]]

    print("\n🧠 CONTEXTO USADO PELO MODELO:\n")
    print(context)

    generator = pipeline("text-generation", model="gpt2")
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"

    result = generator(prompt, max_new_tokens=120)[0]["generated_text"]

    print("\n✅ RESPOSTA GERADA PELO AGENTE:\n")
    print(result)

    print("\n✅ Stage 5 Complete — RAG com Internet Ativado.\n")
