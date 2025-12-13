import streamlit as st
from datetime import datetime

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="ALIENGBUK",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===============================
# Internal Semantic Layer (v1)
# ===============================
SEMANTIC = {
    "pt": {
        "APP_TITLE": "🧠 ALIENGBUK",
        "TAGLINE": "Arquitetura em Espiral • Evolução Consciente • Safe Mode",
        "INTRO": """
Este aplicativo representa um **sistema em construção consciente**.

Nada executa por impulso.  
Nada evolui sem encaixe.  
Nada é descartado sem memória.

Este é o **estágio preparatório** para Agentic AI.
""",
        "ARCH_TITLE": "🌀 Construção do Sistema (Spiral-Up)",
        "SPIRAL": """
### Modelo Aspiral (Spiral-Up)

O sistema evolui em **espiral ascendente**, não em ciclos fechados.

- O que não encaixa → **não executa**
- O que não serve agora → **não é apagado**
- Tudo vira **memória contextual**

Nada é forçado. Tudo é validado.
""",
        "FIT": """
### Critérios de Encaixe

Uma ação só ocorre quando há:
- Encaixe semântico  
- Encaixe estrutural  
- Encaixe temporal  

Sem os três, a ação é bloqueada.
""",
        "MEMORY": """
### Memória Aspiral

Ideias rejeitadas **não são descartadas**.  
Elas ficam armazenadas como **candidatas latentes**.

Quando o contexto muda, elas podem retornar.
""",
        "STATUS": "📌 Status atual: Base validada. Nenhuma execução real permitida."
    },
    "en": {
        "APP_TITLE": "🧠 ALIENGBUK",
        "TAGLINE": "Spiral-Up Architecture • Conscious Evolution • Safe Mode",
        "INTRO": """
This application represents a **consciously built system**.

Nothing executes impulsively.  
Nothing evolves without fit.  
Nothing is deleted without memory.

This is the **pre-Agentic AI stage**.
""",
        "ARCH_TITLE": "🌀 System Construction (Spiral-Up)",
        "SPIRAL": """
### Spiral-Up Model

The system evolves in an **ascending spiral**, not closed loops.

- What doesn't fit → **not executed**
- What doesn't serve now → **not deleted**
- Everything becomes **contextual memory**
""",
        "FIT": """
### Fit Criteria

An action only happens when there is:
- Semantic fit  
- Structural fit  
- Temporal fit  
""",
        "MEMORY": """
### Aspiral Memory

Rejected ideas are **stored, not erased**.

They may return when the context is right.
""",
        "STATUS": "📌 Current status: Base validated. No real execution allowed."
    }
}

# ===============================
# Language Selector
# ===============================
LANG_MAP = {
    "Português 🇧🇷": "pt",
    "English 🇺🇸": "en",
    "Français 🇫🇷 (soon)": "pt",
    "Deutsch 🇩🇪 (soon)": "pt"
}

lang_label = st.selectbox("🌐 Language / Idioma", list(LANG_MAP.keys()), index=0)
lang = LANG_MAP[lang_label]
T = SEMANTIC[lang]

# ===============================
# Session Memory (Aspiral)
# ===============================
if "aspiral_memory" not in st.session_state:
    st.session_state.aspiral_memory = []

# ===============================
# Header
# ===============================
st.title(T["APP_TITLE"])
st.caption(T["TAGLINE"])
st.success(
    "Streamlit está funcionando corretamente 🚀"
    if lang == "pt"
    else "Streamlit is running correctly 🚀"
)

st.divider()

# ===============================
# Intro
# ===============================
st.write(T["INTRO"])
st.divider()

# ===============================
# Architecture Section
# ===============================
with st.expander(T["ARCH_TITLE"], expanded=True):
    st.markdown(T["SPIRAL"])
    st.markdown(T["FIT"])
    st.markdown(T["MEMORY"])

st.divider()

# ===============================
# Decision Registration (Safe)
# ===============================
with st.expander("📝 Registro de Decisão (Memória Aspiral)", expanded=True):
    decision = st.text_area(
        "Descreva uma ideia, decisão ou tentativa (não executa nada):",
        placeholder="Ex: integrar planner → executor quando houver validação semântica..."
    )

    if st.button("Salvar na Memória Aspiral"):
        if decision.strip():
            st.session_state.aspiral_memory.append({
                "timestamp": datetime.utcnow().isoformat(),
                "content": decision.strip()
            })
            st.success("Decisão registrada com sucesso.")
        else:
            st.warning("Nada foi registrado. Campo vazio.")

# ===============================
# Memory Viewer (Read-Only)
# ===============================
with st.expander("🧠 Memória Aspiral (Somente Leitura)", expanded=False):
    if not st.session_state.aspiral_memory:
        st.caption("Nenhuma memória registrada ainda.")
    else:
        for i, item in enumerate(reversed(st.session_state.aspiral_memory), 1):
            st.markdown(f"**#{i} — {item['timestamp']}**")
            st.write(item["content"])
            st.divider()

# ===============================
# Shadow Pipeline (Read-Only)
# ===============================
with st.expander("🧩 Shadow Pipeline (Preparação)", expanded=False):
    st.markdown("""
- Planner → **Desconectado**
- Executor → **Bloqueado**
- ARG / RAG → **Observação apenas**
- LLM → **Não autorizado**
- Git Executor → **Somente leitura**

> Nenhuma execução real ocorre neste estágio.
""")

# ===============================
# Status
# ===============================
st.info(T["STATUS"])

# ===============================
# Footer
# ===============================
st.caption("ALIENGBUK • Spiral-Up Architecture • Safe Preparatory Stage")
