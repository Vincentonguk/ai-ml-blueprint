import streamlit as st

# ======================================================
# Page Config
# ======================================================
st.set_page_config(
    page_title="ALIENGBUK",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ======================================================
# Internal Semantic Layer (SAFE – UI ONLY)
# ======================================================
TEXTS = {
    "pt": {
        "APP_TITLE": "🧠 ALIENGBUK",
        "APP_TAGLINE": "Infraestrutura validada • Evolução consciente • Spiral-Up",
        "INTRO": """
Este aplicativo é construído como um **sistema vivo**.

Nada é executado por impulso.
Nada é descartado sem consciência.

Cada ideia passa por **validação estrutural, semântica e temporal**.
""",
        "ARCH_TITLE": "🧩 Construção do App & Observações Arquiteturais",
        "SPIRAL": """
### 🌀 Evolução em Espiral (Spiral-Up)

O sistema **não evolui em ciclos fechados** nem por tentativa e erro.

Ele evolui em **espiral ascendente**:
- Nada é forçado onde não pertence
- Nada é apagado só por não servir agora
- O aprendizado é acumulado

O que não encaixa **sobe de nível** e aguarda.
""",
        "FIT": """
### 🔍 Critérios de Encaixe

Antes de qualquer mudança, avaliamos:
- Objetivo atual
- Estrutura existente
- Dependências
- Segurança
- Momento correto

Sem encaixe completo, **não executa**.
""",
        "WAIT": """
### ⛔ Quando não é o momento

Se algo não encaixa:
- Não executa
- Não quebra
- Não descarta

As variáveis ficam **em espera consciente**.
""",
        "STATUS": "📌 Status atual: base validada • pronto para evolução",
        "MEM_TITLE": "🧠 Memória Aspiral — Conceitos em Espera",
        "MEM_DESC": """
Aqui ficam ideias, códigos e decisões que **não entraram agora**,
mas **não foram esquecidos**.
""",
        "LANG": "🌐 Idioma / Language"
    },
    "en": {
        "APP_TITLE": "🧠 ALIENGBUK",
        "APP_TAGLINE": "Validated infrastructure • Conscious evolution • Spiral-Up",
        "INTRO": """
This app is built as a **living system**.

Nothing runs by impulse.
Nothing is discarded without awareness.
""",
        "ARCH_TITLE": "🧩 App Construction & Architectural Notes",
        "SPIRAL": """
### 🌀 Spiral-Up Evolution

The system does not loop blindly.

It evolves upward:
- No forced integration
- No premature deletion
- Knowledge is preserved
""",
        "FIT": """
### 🔍 Fit Criteria

Changes require:
- Semantic fit
- Structural fit
- Timing fit
""",
        "WAIT": """
### ⛔ Not the right moment

If it doesn’t fit:
- Do not execute
- Preserve structure
- Store context
""",
        "STATUS": "📌 Current status: validated base • ready to evolve",
        "MEM_TITLE": "🧠 Spiral Memory — Pending Concepts",
        "MEM_DESC": "Ideas preserved for future re-evaluation.",
        "LANG": "🌐 Language / Idioma"
    }
}

# ======================================================
# Language Selector (SAFE)
# ======================================================
LANG_MAP = {
    "Português 🇧🇷": "pt",
    "English 🇺🇸": "en",
    "Français 🇫🇷 (beta)": "pt",
    "Deutsch 🇩🇪 (beta)": "pt",
}

lang_label = st.selectbox(TEXTS["pt"]["LANG"], list(LANG_MAP.keys()))
lang = LANG_MAP[lang_label]
T = TEXTS.get(lang, TEXTS["pt"])

# ======================================================
# Header
# ======================================================
st.title(T["APP_TITLE"])
st.caption(T["APP_TAGLINE"])
st.success("Streamlit está funcionando corretamente 🚀")
st.divider()

# ======================================================
# Intro
# ======================================================
st.write(T["INTRO"])
st.divider()

# ======================================================
# Architecture Section
# ======================================================
with st.expander(T["ARCH_TITLE"], expanded=True):
    st.markdown(T["SPIRAL"])
    st.markdown(T["FIT"])
    st.markdown(T["WAIT"])

# ======================================================
# Spiral Memory (UI Only)
# ======================================================
st.divider()

with st.expander(T["MEM_TITLE"], expanded=False):
    st.markdown(T["MEM_DESC"])

    st.text_area(
        "📥 Registrar observação",
        placeholder="Ideia, código ou decisão analisada mas não executada..."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox(
            "Motivo do não-encaixe",
            [
                "Contexto imaturo",
                "Dependências ausentes",
                "Risco estrutural",
                "Fora do objetivo atual",
                "Outro"
            ]
        )

    with col2:
        st.selectbox(
            "Tipo",
            ["Ideia", "Código", "Parâmetro", "Decisão", "Hipótese"]
        )

    st.info(
        "Nada aqui é perdido. Nada é executado automaticamente. "
        "Tudo aguarda o contexto correto."
    )

# ======================================================
# Status
# ======================================================
st.divider()
st.info(T["STATUS"])

# ======================================================
# Footer
# ======================================================
st.caption("ALIENGBUK • Spiral-Up Architecture • Consciência antes da execução")
