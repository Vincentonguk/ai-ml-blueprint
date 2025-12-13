import streamlit as st
from src.semantic.concepts import t

st.set_page_config(
    page_title="ALIENGBUK",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# Language Selector (skin)
# -------------------------------
LANG_OPTIONS = {
    "Português 🇧🇷": "pt",
    "English 🇺🇸": "en",
    "Français 🇫🇷 (beta)": "fr",
    "Deutsch 🇩🇪 (beta)": "de",
}
lang_label = st.selectbox("🌐 Language / Idioma", list(LANG_OPTIONS.keys()), index=0)
lang = LANG_OPTIONS[lang_label]

# -------------------------------
# Header
# -------------------------------
st.title(t("APP_TITLE", lang))
st.caption(t("APP_TAGLINE", lang))
st.success("Streamlit está funcionando corretamente 🚀" if lang == "pt" else "Streamlit is working correctly 🚀")

st.divider()

# -------------------------------
# Intro
# -------------------------------
st.write(t("INTRO", lang))

st.divider()

# -------------------------------
# Architectural Observations
# -------------------------------
with st.expander(t("SECTION_ARCH_TITLE", lang), expanded=True):
    st.markdown(t("SPIRAL_MODEL", lang))
    st.markdown(t("FIT_CRITERIA", lang))
    st.markdown(t("NOT_RIGHT_MOMENT", lang))
    st.markdown(t("PARAM_DRIFT", lang))

st.divider()
st.info(
    "📌 Status atual: base validada. Próximo passo: backend inteligente."
    if lang == "pt"
    else "📌 Current status: validated base. Next step: intelligent backend."
)

st.caption("ALIENGBUK • Spiral-Up Architecture")
