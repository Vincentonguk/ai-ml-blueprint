import streamlit as st
from datetime import datetime, timezone
import re
import json

# =========================================================
# Page Config
# =========================================================
st.set_page_config(
    page_title="ALIENGBUK",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =========================================================
# Semantic Layer (Internal) + Fallback
# =========================================================
SEMANTIC = {
    "pt": {
        "TITLE": "🧠 ALIENGBUK",
        "TAGLINE": "Shadow Pipeline • Arquitetura em Espiral • Modo Seguro (A)",
        "INTRO": (
            "Este sistema opera em **modo Shadow (simulação consciente)**.\n\n"
            "- Nada é executado\n"
            "- Nada é modificado\n"
            "- Tudo é analisado\n\n"
            "Objetivo agora: **Decision Trace Engine (READY/REVIEW/BLOCK) + Memória Aspiral**, sem execução real."
        ),
        "LANG_LABEL": "🌐 Idioma / Language",
        "INTENT_LABEL": "Descreva sua intenção (nada será executado):",
        "BTN_SIMULATE": "🔍 Simular decisão (Shadow)",
        "ARCH_TITLE": "🌀 Construção do Sistema (Spiral-Up)",
        "ARCH_BODY": (
            "### Modelo Aspiral (Spiral-Up)\n"
            "O sistema evolui em **espiral ascendente**, não em ciclos fechados.\n\n"
            "- O que não encaixa **não é executado**\n"
            "- O que não serve agora **não é apagado**\n"
            "- Tudo vira **memória contextual**\n\n"
            "### Critérios de Encaixe\n"
            "Uma ação só ocorre quando há:\n"
            "- Encaixe semântico\n"
            "- Encaixe estrutural\n"
            "- Encaixe temporal\n\n"
            "### Memória Aspiral\n"
            "Ideias rejeitadas **não são descartadas**: ficam como candidatas latentes e podem retornar quando o contexto mudar."
        ),
        "DECISION_TITLE": "🧭 Decision Trace Engine",
        "PLANNER_TITLE": "🧩 Shadow Planner (Estrutural)",
        "LLM_TITLE": "🧠 Shadow Insight (heurístico)",
        "EXEC_TITLE": "🪶 Shadow Executor (bloqueado)",
        "MEM_TITLE": "🌀 Memória Aspiral",
        "MEM_EMPTY": "Nenhuma memória registrada ainda.",
        "STATUS": "📌 Status: Shadow Pipeline ativo • Execução real bloqueada (Opção A)",
        "TOOLS_TITLE": "🧰 Ferramentas (Read-only)",
        "TOOLS_BODY": (
            "- Git → **Somente leitura**\n"
            "- Planner → **Simulado**\n"
            "- Executor → **Bloqueado**\n"
            "- RAG/ARG → **Ainda não conectado**\n"
            "- LLM → **Opcional (depois via Secrets)**\n\n"
            "> Nenhuma execução real ocorre neste estágio."
        ),
        "ADV_TITLE": "⚙️ Advanced (Memória / Exportar)",
        "BTN_CLEAR": "🧼 Limpar memória desta sessão",
        "BTN_EXPORT": "⬇️ Exportar memória (JSON)",
        "EXPORT_HINT": "Baixe o JSON e guarde como histórico local.",
        "BAD_INTENT": "Escreva uma intenção antes de simular.",
    },
    "en": {
        "TITLE": "🧠 ALIENGBUK",
        "TAGLINE": "Shadow Pipeline • Spiral-Up Architecture • Safe Mode (A)",
        "INTRO": (
            "This system runs in **Shadow mode (conscious simulation)**.\n\n"
            "- Nothing is executed\n"
            "- Nothing is modified\n"
            "- Everything is analyzed\n\n"
            "Goal now: **Decision Trace Engine (READY/REVIEW/BLOCK) + Aspiral Memory**, with zero real execution."
        ),
        "LANG_LABEL": "🌐 Language / Idioma",
        "INTENT_LABEL": "Describe your intention (nothing will be executed):",
        "BTN_SIMULATE": "🔍 Simulate decision (Shadow)",
        "ARCH_TITLE": "🌀 System Construction (Spiral-Up)",
        "ARCH_BODY": (
            "### Spiral-Up Model\n"
            "The system evolves in an **ascending spiral**, not closed loops.\n\n"
            "- What doesn't fit is **not executed**\n"
            "- What doesn't serve now is **not deleted**\n"
            "- Everything becomes **contextual memory**\n\n"
            "### Fit Criteria\n"
            "An action only happens when there is:\n"
            "- Semantic fit\n"
            "- Structural fit\n"
            "- Temporal fit\n\n"
            "### Aspiral Memory\n"
            "Rejected ideas are **stored, not erased** — they can return when the context becomes right."
        ),
        "DECISION_TITLE": "🧭 Decision Trace Engine",
        "PLANNER_TITLE": "🧩 Shadow Planner (Structural)",
        "LLM_TITLE": "🧠 Shadow Insight (heuristic)",
        "EXEC_TITLE": "🪶 Shadow Executor (blocked)",
        "MEM_TITLE": "🌀 Aspiral Memory",
        "MEM_EMPTY": "No memory entries yet.",
        "STATUS": "📌 Status: Shadow Pipeline active • Real execution blocked (Option A)",
        "TOOLS_TITLE": "🧰 Tools (Read-only)",
        "TOOLS_BODY": (
            "- Git → **Read-only**\n"
            "- Planner → **Simulated**\n"
            "- Executor → **Blocked**\n"
            "- RAG/ARG → **Not connected yet**\n"
            "- LLM → **Optional later (via Secrets)**\n\n"
            "> No real execution happens at this stage."
        ),
        "ADV_TITLE": "⚙️ Advanced (Memory / Export)",
        "BTN_CLEAR": "🧼 Clear session memory",
        "BTN_EXPORT": "⬇️ Export memory (JSON)",
        "EXPORT_HINT": "Download the JSON and keep it as local history.",
        "BAD_INTENT": "Write an intention before simulating.",
    },
}

LANG_MAP = {
    "Português 🇧🇷": "pt",
    "English 🇺🇸": "en",
    "Français 🇫🇷 (beta)": "en",   # fallback to EN
    "Deutsch 🇩🇪 (beta)": "en",    # fallback to EN
}

def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def t(key: str, lang: str) -> str:
    if lang in SEMANTIC and key in SEMANTIC[lang]:
        return SEMANTIC[lang][key]
    if "en" in SEMANTIC and key in SEMANTIC["en"]:
        return SEMANTIC["en"][key]
    return key

# =========================================================
# Decision Trace Engine (v1 - Heuristic, Safe)
# =========================================================
KEYWORDS_BLOCK = [
    r"\bpush\b", r"\bcommit\b", r"\bmerge\b", r"\brebase\b", r"\bdelete\b", r"\brm\b",
    r"\bformat\b", r"\bchmod\b", r"\bchown\b", r"\bdeploy\b", r"\brun\b", r"\bexecute\b",
    r"\bopenai\b", r"\bapi\s*key\b", r"\bsecret\b", r"\btoken\b", r"\bpassword\b",
    r"\bprod\b", r"\bproduction\b",
]
KEYWORDS_REVIEW = [
    r"\bstatus\b", r"\bdiff\b", r"\blog\b", r"\bbranch\b", r"\bshow\b", r"\binspect\b",
    r"\bdiagnos(e|tic)\b", r"\bexplain\b", r"\bplan\b", r"\bdesign\b", r"\brefactor\b",
    r"\bnotes?\b", r"\bmemory\b", r"\baspiral\b", r"\bspiral\b",
]
KEYWORDS_READY = [
    r"\bwrite\b", r"\bdraft\b", r"\bsummar(y|ize)\b", r"\btranslate\b", r"\bchecklist\b",
    r"\bcreate\s+text\b", r"\bui\b", r"\bcopy\b",
]

def _match_any(patterns, text: str) -> bool:
    for p in patterns:
        if re.search(p, text, flags=re.IGNORECASE):
            return True
    return False

def classify_intent(intent: str) -> dict:
    """
    Returns: {
      "state": "READY"|"REVIEW"|"BLOCK",
      "signals": {...},
      "reasons": [...],
      "suggestions": [...]
    }
    """
    txt = intent.strip()
    reasons = []
    suggestions = []
    signals = {
        "semantic_fit": True,
        "structural_fit": True,
        "temporal_fit": True,
        "risk": "low",
    }

    # Base guardrails (Option A): real execution is ALWAYS blocked
    # but we still classify readiness for "analysis-only" outputs.
    is_block = _match_any(KEYWORDS_BLOCK, txt)
    is_review = _match_any(KEYWORDS_REVIEW, txt)
    is_ready = _match_any(KEYWORDS_READY, txt)

    # Detect potentially "action-oriented" intents
    if is_block:
        state = "BLOCK"
        signals["risk"] = "high"
        reasons.append("Intent contains execution/credentials/modification signals.")
        suggestions.append("Convert to analysis-only: ask for a plan/checklist instead of executing.")
    else:
        # In Shadow mode, the best we can do is: READY (safe outputs) vs REVIEW (needs scrutiny)
        if is_review and not is_ready:
            state = "REVIEW"
            signals["risk"] = "medium"
            reasons.append("Intent suggests system/infra inspection or sensitive operations (read-only).")
            suggestions.append("Proceed as read-only plan/diagnostic. No commands will run here.")
        else:
            state = "READY"
            signals["risk"] = "low"
            reasons.append("Intent appears safe for analysis-only output.")
            suggestions.append("Proceed with a structured plan and keep execution blocked.")

    # Temporal fit (we're in Shadow stage)
    signals["temporal_fit"] = False
    reasons.append("Temporal gate: system is in Shadow/Safe Mode (Option A). Real execution is not allowed.")
    suggestions.append("If you want execution later: enable Secrets + switch to controlled executor phase (future).")

    return {
        "state": state,
        "signals": signals,
        "reasons": reasons,
        "suggestions": suggestions,
    }

def build_shadow_plan(intent: str, lang: str) -> dict:
    trace = classify_intent(intent)
    eval_list = [
        "Semantic fit (meaning/context)" if lang == "en" else "Encaixe semântico (significado/contexto)",
        "Structural fit (where it belongs)" if lang == "en" else "Encaixe estrutural (onde pertence)",
        "Temporal fit (is this the right stage?)" if lang == "en" else "Encaixe temporal (é o estágio certo?)",
    ]
    return {
        "intent": intent,
        "evaluation": eval_list,
        "decision_trace": trace,
        "timestamp_utc": now_utc_iso(),
        "mode": "SHADOW_SAFE_A",
    }

def build_shadow_executor(trace_state: str, lang: str) -> dict:
    return {
        "would_execute": False,
        "blocked": True,
        "blocked_reason": (
            "Safe Mode (Option A): executor is disabled. Analysis-only."
            if lang == "en"
            else "Modo Seguro (Opção A): executor desabilitado. Apenas análise."
        ),
        "recommended_next_state": trace_state,
    }

def memory_entry(intent: str, trace: dict) -> dict:
    return {
        "intent": intent,
        "state": trace.get("state"),
        "risk": trace.get("signals", {}).get("risk"),
        "reasons": trace.get("reasons", [])[:3],
        "timestamp_utc": now_utc_iso(),
        "tags": infer_tags(intent),
    }

def infer_tags(intent: str):
    s = intent.lower()
    tags = []
    if re.search(r"\bgit\b", s): tags.append("git")
    if re.search(r"\bstatus\b|\bdiff\b|\blog\b|\bbranch\b", s): tags.append("inspect")
    if re.search(r"\bdeploy\b|\bstreamlit\b", s): tags.append("deploy")
    if re.search(r"\barg\b|\brag\b|\bllm\b|\bagent\b", s): tags.append("ai")
    if re.search(r"\bsecret\b|\btoken\b|\bkey\b", s): tags.append("secrets")
    if not tags:
        tags.append("general")
    return tags

# =========================================================
# Session State
# =========================================================
if "aspiral_memory" not in st.session_state:
    st.session_state.aspiral_memory = []
if "last_trace" not in st.session_state:
    st.session_state.last_trace = None

# =========================================================
# UI: Language
# =========================================================
lang_label = st.selectbox(t("LANG_LABEL", "pt"), list(LANG_MAP.keys()), index=0)
lang = LANG_MAP[lang_label]
T = lambda k: t(k, lang)

# =========================================================
# UI: Header
# =========================================================
st.title(T("TITLE"))
st.caption(T("TAGLINE"))
st.divider()
st.write(T("INTRO"))

# =========================================================
# UI: Architecture Notes
# =========================================================
with st.expander(T("ARCH_TITLE"), expanded=False):
    st.markdown(T("ARCH_BODY"))

st.divider()

# =========================================================
# UI: Shadow Input
# =========================================================
intent = st.text_area(T("INTENT_LABEL"), placeholder="Ex: verificar status do git e mostrar alterações")

col_a, col_b, col_c = st.columns([1, 1, 2])
with col_a:
    run_btn = st.button(T("BTN_SIMULATE"), use_container_width=True)
with col_b:
    clear_btn = st.button(T("BTN_CLEAR"), use_container_width=True)
with col_c:
    st.caption("A = Shadow/Safe Mode • READY/REVIEW/BLOCK = decisão rastreável (sem executar)")

if clear_btn:
    st.session_state.aspiral_memory = []
    st.session_state.last_trace = None
    st.rerun()

# =========================================================
# Run Shadow Trace
# =========================================================
if run_btn:
    if not intent.strip():
        st.warning(T("BAD_INTENT"))
    else:
        plan = build_shadow_plan(intent.strip(), lang)
        trace = plan["decision_trace"]
        st.session_state.last_trace = plan

        # Append to aspiral memory
        st.session_state.aspiral_memory.append(memory_entry(intent.strip(), trace))

        # Planner
        with st.expander(T("PLANNER_TITLE"), expanded=True):
            st.json(plan)

        # Insight (heuristic explanation)
        with st.expander(T("LLM_TITLE"), expanded=True):
            state = trace["state"]
            risk = trace["signals"]["risk"]
            reasons = trace["reasons"]
            suggestions = trace["suggestions"]

            if lang == "en":
                st.markdown(f"**State:** `{state}`  •  **Risk:** `{risk}`")
                st.markdown("**Why:**")
            else:
                st.markdown(f"**Estado:** `{state}`  •  **Risco:** `{risk}`")
                st.markdown("**Por quê:**")

            for r in reasons:
                st.markdown(f"- {r}")

            if lang == "en":
                st.markdown("**Suggested next step (still no execution):**")
            else:
                st.markdown("**Próximo passo sugerido (ainda sem execução):**")

            for s in suggestions:
                st.markdown(f"- {s}")

        # Executor (always blocked)
        with st.expander(T("EXEC_TITLE"), expanded=True):
            st.json(build_shadow_executor(trace["state"], lang))

st.divider()

# =========================================================
# UI: Memory Viewer (Aspiral)
# =========================================================
with st.expander(T("MEM_TITLE"), expanded=True):
    mem = st.session_state.aspiral_memory
    if not mem:
        st.caption(T("MEM_EMPTY"))
    else:
        # Filter + search
        q = st.text_input("🔎 Buscar (intent/tags/state)", "")
        state_filter = st.multiselect(
            "Filtrar estado",
            options=["READY", "REVIEW", "BLOCK"],
            default=[],
        )

        def match(entry):
            blob = f"{entry.get('intent','')} {entry.get('state','')} {' '.join(entry.get('tags',[]))}".lower()
            if q and q.lower() not in blob:
                return False
            if state_filter and entry.get("state") not in state_filter:
                return False
            return True

        filtered = [e for e in mem if match(e)]
        st.caption(f"{len(filtered)} / {len(mem)} entradas")

        # Show newest first
        for i, e in enumerate(reversed(filtered), 1):
            st.markdown(f"**{i}.** `{e['intent']}`")
            st.caption(f"{e['state']} • risk={e['risk']} • {e['timestamp_utc']} • tags={', '.join(e['tags'])}")
            if e.get("reasons"):
                for r in e["reasons"]:
                    st.markdown(f"- {r}")
            st.divider()

        # Export
        export = json.dumps(mem, ensure_ascii=False, indent=2)
        st.download_button(
            label=T("BTN_EXPORT"),
            data=export.encode("utf-8"),
            file_name="aspiral_memory.json",
            mime="application/json",
        )
        st.caption(T("EXPORT_HINT"))

st.divider()

# =========================================================
# UI: Tools (Read-only) + Status
# =========================================================
with st.expander(T("TOOLS_TITLE"), expanded=False):
    st.markdown(T("TOOLS_BODY"))

st.info(T("STATUS"))
st.caption("ALIENGBUK • Shadow Pipeline + Decision Trace Engine • Spiral-Up Evolution • SAFE MODE (A)")
