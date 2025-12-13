import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st


# ======================================================
# Page Config
# ======================================================
st.set_page_config(
    page_title="ALIENGBUK",
    layout="centered",
    initial_sidebar_state="collapsed"
)

DATA_PATH = Path("data") / "memoria_aspiral.json"


# ======================================================
# Internal Semantic Layer (SAFE – UI ONLY)
# ======================================================
TEXTS = {
    "pt": {
        "APP_TITLE": "🧠 ALIENGBUK",
        "APP_TAGLINE": "Infraestrutura validada • Evolução consciente • Spiral-Up",
        "LANG": "🌐 Idioma / Language",
        "INTRO": (
            "Este aplicativo é construído como um **sistema vivo**.\n\n"
            "Nada é executado por impulso.\n"
            "Nada é descartado sem consciência.\n\n"
            "Cada ideia passa por **validação estrutural, semântica e temporal**."
        ),
        "ARCH_TITLE": "🧩 Construção do App & Observações Arquiteturais",
        "SPIRAL": (
            "### 🌀 Evolução em Espiral (Spiral-Up)\n\n"
            "O sistema **não evolui em ciclos fechados** nem por tentativa e erro.\n\n"
            "Ele evolui em **espiral ascendente**:\n"
            "- Nada é forçado onde não pertence\n"
            "- Nada é apagado só por não servir agora\n"
            "- O aprendizado é acumulado\n\n"
            "O que não encaixa **não some** — vira candidato latente."
        ),
        "FIT": (
            "### 🔍 Critérios de Encaixe\n\n"
            "Antes de qualquer mudança, avaliamos:\n"
            "- Objetivo atual\n"
            "- Estrutura existente\n"
            "- Dependências\n"
            "- Segurança e impacto\n"
            "- Momento correto\n\n"
            "**Sem encaixe completo, não executa.**"
        ),
        "WAIT": (
            "### ⛔ Quando não é o momento\n\n"
            "Se algo não encaixa:\n"
            "- Não executa\n"
            "- Não quebra\n"
            "- Não descarta\n\n"
            "As variáveis ficam **em espera consciente**."
        ),
        "MEM_TITLE": "🧠 Memória Aspiral — Estrutura Viva",
        "MEM_DESC": (
            "Aqui você registra ideias/códigos/decisões que **não entraram agora**, "
            "mas **não devem ser esquecidos**.\n\n"
            "O sistema preserva candidatos para reavaliação quando o contexto ficar compatível."
        ),
        "STATUS": "📌 Status atual: base validada • pronto para evolução",
        "BTN_SAVE": "💾 Salvar na Memória",
        "BTN_EXPORT": "⬇️ Exportar JSON",
        "BTN_IMPORT": "⬆️ Importar JSON",
        "BTN_REFRESH": "🔄 Recarregar",
        "FILTERS": "Filtros",
        "LIST": "📚 Itens registrados",
        "EMPTY": "Nenhum item ainda. Registre o primeiro candidato latente."
    },
    "en": {
        "APP_TITLE": "🧠 ALIENGBUK",
        "APP_TAGLINE": "Validated infrastructure • Conscious evolution • Spiral-Up",
        "LANG": "🌐 Language / Idioma",
        "INTRO": (
            "This app is built as a **living system**.\n\n"
            "Nothing runs by impulse.\n"
            "Nothing is discarded without awareness.\n\n"
            "Every idea goes through **structural, semantic, and temporal validation**."
        ),
        "ARCH_TITLE": "🧩 App Construction & Architectural Notes",
        "SPIRAL": (
            "### 🌀 Spiral-Up Evolution\n\n"
            "The system does not evolve in blind loops.\n\n"
            "It evolves upward:\n"
            "- Nothing is forced where it doesn't belong\n"
            "- Nothing is deleted just because it doesn't fit yet\n"
            "- Learning is accumulated\n\n"
            "What doesn't fit becomes a latent candidate."
        ),
        "FIT": (
            "### 🔍 Fit Criteria\n\n"
            "Before any change:\n"
            "- Current objective\n"
            "- Existing structure\n"
            "- Dependencies\n"
            "- Safety and impact\n"
            "- Right timing\n\n"
            "**Without full fit, do not execute.**"
        ),
        "WAIT": (
            "### ⛔ Not the right moment\n\n"
            "If it doesn't fit:\n"
            "- Don't execute\n"
            "- Preserve structure\n"
            "- Don't discard\n\n"
            "Variables remain in **conscious waiting**."
        ),
        "MEM_TITLE": "🧠 Spiral Memory — Living Structure",
        "MEM_DESC": (
            "Register ideas/code/decisions that **didn't fit now**, "
            "but **must not be forgotten**.\n\n"
            "Candidates are preserved for re-evaluation when context matches."
        ),
        "STATUS": "📌 Current status: validated base • ready to evolve",
        "BTN_SAVE": "💾 Save to Memory",
        "BTN_EXPORT": "⬇️ Export JSON",
        "BTN_IMPORT": "⬆️ Import JSON",
        "BTN_REFRESH": "🔄 Reload",
        "FILTERS": "Filters",
        "LIST": "📚 Registered items",
        "EMPTY": "No items yet. Register the first latent candidate."
    }
}

LANG_MAP = {
    "Português 🇧🇷": "pt",
    "English 🇺🇸": "en",
    "Français 🇫🇷 (beta)": "pt",
    "Deutsch 🇩🇪 (beta)": "pt",
}


# ======================================================
# Memory IO
# ======================================================
def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def load_memory() -> list[dict]:
    try:
        if not DATA_PATH.exists():
            DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
            DATA_PATH.write_text("[]", encoding="utf-8")
        raw = DATA_PATH.read_text(encoding="utf-8").strip()
        if not raw:
            return []
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except Exception:
        # não derruba o app — apenas trabalha em memória
        return []

def save_memory(items: list[dict]) -> bool:
    try:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except Exception:
        return False

def merge_import(current: list[dict], imported: list[dict]) -> list[dict]:
    # dedup por id
    seen = {it.get("id") for it in current if isinstance(it, dict)}
    merged = list(current)
    for it in imported:
        if isinstance(it, dict) and it.get("id") and it.get("id") not in seen:
            merged.append(it)
            seen.add(it.get("id"))
    return merged


# ======================================================
# Language Selector
# ======================================================
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
# Intro + Architecture
# ======================================================
st.write(T["INTRO"])
st.divider()

with st.expander(T["ARCH_TITLE"], expanded=True):
    st.markdown(T["SPIRAL"])
    st.markdown(T["FIT"])
    st.markdown(T["WAIT"])

st.divider()


# ======================================================
# Spiral Memory (Persistent + Export/Import)
# ======================================================
st.subheader(T["MEM_TITLE"])
st.write(T["MEM_DESC"])

# carregar memória uma vez por sessão
if "aspiral_items" not in st.session_state:
    st.session_state.aspiral_items = load_memory()

colA, colB, colC = st.columns([1, 1, 1])

with colA:
    if st.button(T["BTN_REFRESH"], use_container_width=True):
        st.session_state.aspiral_items = load_memory()
        st.rerun()

with colB:
    export_bytes = json.dumps(st.session_state.aspiral_items, ensure_ascii=False, indent=2).encode("utf-8")
    st.download_button(
        label=T["BTN_EXPORT"],
        data=export_bytes,
        file_name="memoria_aspiral_export.json",
        mime="application/json",
        use_container_width=True
    )

with colC:
    uploaded = st.file_uploader(T["BTN_IMPORT"], type=["json"])
    if uploaded is not None:
        try:
            imported = json.loads(uploaded.read().decode("utf-8"))
            if isinstance(imported, list):
                st.session_state.aspiral_items = merge_import(st.session_state.aspiral_items, imported)
                ok = save_memory(st.session_state.aspiral_items)
                st.success("Importado e salvo ✅" if ok else "Importado (salvar no disco falhou, mas ficou na sessão) ⚠️")
            else:
                st.error("JSON inválido: esperado uma lista []")
        except Exception as e:
            st.error(f"Falha ao importar: {e}")

st.divider()

# formulário para inserir item
with st.form("aspiral_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        kind = st.selectbox("Tipo", ["Ideia", "Código", "Parâmetro", "Decisão", "Hipótese"])
    with c2:
        reason = st.selectbox("Motivo do não-encaixe", ["Contexto imaturo", "Dependências ausentes", "Risco estrutural", "Fora do objetivo atual", "Outro"])

    title = st.text_input("Título curto (identificação)")
    content = st.text_area("Conteúdo / Observação", placeholder="Escreva aqui o que foi analisado e por que deve ser lembrado depois…")
    vars_line = st.text_input("Variáveis mínimas (separe por vírgula)", placeholder="ex: streamlit, import, encoding, deploy, planner")

    status = st.selectbox("Status", ["Latente", "Reavaliar depois", "Aguardando dependência", "Bloqueado por risco"])
    submitted = st.form_submit_button(T["BTN_SAVE"], use_container_width=True)

    if submitted:
        item = {
            "id": str(uuid.uuid4()),
            "created_at": _utc_now_iso(),
            "kind": kind,
            "reason": reason,
            "status": status,
            "title": title.strip() or f"{kind} sem título",
            "content": content.strip(),
            "vars": [v.strip() for v in vars_line.split(",") if v.strip()],
        }
        st.session_state.aspiral_items.insert(0, item)
        ok = save_memory(st.session_state.aspiral_items)
        st.success("Salvo ✅" if ok else "Salvo na sessão (disco indisponível) ⚠️")

st.divider()

# filtros + listagem
with st.expander(T["FILTERS"], expanded=False):
    f1, f2, f3 = st.columns(3)
    with f1:
        f_kind = st.multiselect("Tipo", ["Ideia", "Código", "Parâmetro", "Decisão", "Hipótese"], default=[])
    with f2:
        f_status = st.multiselect("Status", ["Latente", "Reavaliar depois", "Aguardando dependência", "Bloqueado por risco"], default=[])
    with f3:
        query = st.text_input("Buscar", placeholder="ex: deploy, import, streamlit, planner")

items = st.session_state.aspiral_items

def match(it: dict) -> bool:
    if f_kind and it.get("kind") not in f_kind:
        return False
    if f_status and it.get("status") not in f_status:
        return False
    if query:
        q = query.lower()
        blob = " ".join([
            str(it.get("title","")),
            str(it.get("content","")),
            " ".join(it.get("vars", []))
        ]).lower()
        return q in blob
    return True

filtered = [it for it in items if isinstance(it, dict) and match(it)]

st.subheader(T["LIST"])

if not filtered:
    st.info(T["EMPTY"])
else:
    for it in filtered[:200]:
        with st.container():
            st.markdown(f"**{it.get('title','(sem título)')}**")
            meta = f"• {it.get('kind','')} • {it.get('status','')} • {it.get('reason','')} • {it.get('created_at','')}"
            st.caption(meta)
            if it.get("vars"):
                st.code(", ".join(it["vars"]))
            if it.get("content"):
                st.write(it["content"])
            st.divider()

# ======================================================
# Status + Footer
# ======================================================
st.info(T["STATUS"])
st.caption("ALIENGBUK • Spiral-Up Architecture • Memória Aspiral v1 (persistência simples + export/import)")
