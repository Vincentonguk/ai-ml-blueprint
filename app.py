import os
import streamlit as st
from dotenv import load_dotenv

# ===============================
# ✅ CARREGAR A CHAVE DO .env
# ===============================
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_KEY:
    st.error("❌ OPENAI_API_KEY não encontrada no .env")
    st.stop()

# ===============================
# ✅ IMPORTAR SISTEMAS
# ===============================
from src.agent_core.multi_agent_system import run_multi_agent
from src.rag_engine.rag_real import run_rag_real

# ===============================
# ✅ INTERFACE
# ===============================
st.set_page_config(page_title="ALIENGBUK", layout="wide")

st.title("🤖 ALIENGBUK — Sistema Multi-Agente Autônomo")
st.markdown("Planner • Worker • Critic • RAG • OpenAI")

mode = st.sidebar.radio(
    "Escolha o modo:",
    ["🎯 Multi-Agente", "📄 RAG com Documentos"]
)

# ===============================
# 🎯 MODO MULTI-AGENTE
# ===============================
if mode == "🎯 Multi-Agente":
    st.subheader("🎯 Sistema Multi-Agente")

    goal = st.text_area(
        "Descreva o objetivo:",
        placeholder="Ex: Criar um sistema de atendimento automático...",
        height=150
    )

    if st.button("🚀 Executar Agente"):
        if not goal.strip():
            st.warning("Digite um objetivo.")
        else:
            with st.spinner("Executando agentes..."):
                try:
                    output = run_multi_agent(goal)
                    st.success("✅ Finalizado")
                    st.text_area("📜 Resultado", output, height=500)
                except Exception as e:
                    st.error("Erro na execução")
                    st.exception(e)

# ===============================
# 📄 MODO RAG REAL
# ===============================
else:
    st.subheader("📄 RAG Real")

    uploaded = st.file_uploader("Envie um PDF ou TXT", type=["pdf", "txt"])
    question = st.text_input("Digite sua pergunta:")

    if st.button("🔎 Rodar RAG"):
        if not uploaded:
            st.warning("Envie um arquivo.")
        elif not question.strip():
            st.warning("Digite uma pergunta.")
        else:
            temp_path = "temp_file." + uploaded.name.split(".")[-1]

            with open(temp_path, "wb") as f:
                f.write(uploaded.read())

            with st.spinner("Processando documento..."):
                try:
                    result = run_rag_real(temp_path, question)
                    st.success("✅ Pronto")
                    st.text_area("📜 Resultado", result, height=500)
                except Exception as e:
                    st.error("Erro no RAG")
                    st.exception(e)
