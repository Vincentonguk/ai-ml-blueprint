import json
import time
import urllib.request
import urllib.error
from datetime import datetime

import streamlit as st

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="ALIENGBUK",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===============================
# Semantic Layer (PT/EN)
# ===============================
SEMANTIC = {
    "pt": {
        "TITLE": "🧠 ALIENGBUK",
        "TAGLINE": "Shadow Pipeline + Shadow LLM • Arquitetura em Espiral • Modo Seguro",
        "INTRO": """
Este sistema opera em **modo seguro**:

✅ Shadow Planner + Memória Aspiral  
✅ Shadow LLM (somente leitura / análise)  
❌ Executor REAL continua BLOQUEADO (nada é executado)

Modelo: **Spiral-Up / Aspiral Memory**
""",
        "LANG_LABEL": "🌐 Idioma / Language",
        "INPUT_LABEL": "Descreva sua intenção (nada será executado):",
        "BTN": "🧠 Gerar Análise (Shadow LLM)",
        "PLANNER_TITLE": "🧭 Shadow Planner (Estrutural)",
        "LLM_TITLE": "🧠 Shadow LLM Insight (Read-only)",
        "EXEC_TITLE": "🪶 Shadow Executor (BLOQUEADO)",
        "MEM_TITLE": "🌀 Memória Aspiral",
        "STATUS": "📌 Status: Shadow LLM ativo (texto) • Execução real bloqueada",
        "NO_KEY": "⚠️ Sem API Key nos Secrets. Shadow LLM ficará em modo simulado.",
        "KEY_OK": "🔐 Secrets OK. Shadow LLM habilitado (somente texto).",
        "MODEL": "Modelo do LLM (somente leitura)",
        "SIMULATED": "Modo simulado: adicione OPENAI_API_KEY em Settings → Secrets.",
        "CLEAR": "🧹 Limpar memória da sessão"
    },
    "en": {
        "TITLE": "🧠 ALIENGBUK",
        "TAGLINE": "Shadow Pipeline + Shadow LLM • Spiral-Up Architecture • Safe Mode",
        "INTRO": """
This system runs in **safe mode**:

✅ Shadow Planner + Aspiral Memory  
✅ Shadow LLM (read-only analysis)  
❌ REAL Executor remains BLOCKED (no actions executed)

Model: **Spiral-Up / Aspiral Memory**
""",
        "LANG_LABEL": "🌐 Language / Idioma",
        "INPUT_LABEL": "Describe your intention (nothing will be executed):",
        "BTN": "🧠 Generate Analysis (Shadow LLM)",
        "PLANNER_TITLE": "🧭 Shadow Planner (Structural)",
        "LLM_TITLE": "🧠 Shadow LLM Insight (Read-only)",
        "EXEC_TITLE": "🪶 Shadow Executor (BLOCKED)",
        "MEM_TITLE": "🌀 Aspiral Memory",
        "STATUS": "📌 Status: Shadow LLM active (text) • Real execution blocked",
        "NO_KEY": "⚠️ No API Key in Secrets. Shadow LLM will run in simulated mode.",
        "KEY_OK": "🔐 Secrets OK. Shadow LLM enabled (text only).",
        "MODEL": "LLM model (read-only)",
        "SIMULATED": "Simulated mode: add OPENAI_API_KEY in Settings → Secrets.",
        "CLEAR": "🧹 Clear session memory"
    }
}

LANG_MAP = {"Português 🇧🇷": "pt", "English 🇺🇸": "en"}
lang_label = st.selectbox(SEMANTIC["pt"]["LANG_LABEL"], list(LANG_MAP.keys()), index=0)
lang = LANG_MAP[lang_label]
T = SEMANTIC[lang]

# ===============================
# Header
# ===============================
st.title(T["TITLE"])
st.caption(T["TAGLINE"])
st.divider()
st.write(T["INTRO"])

# ===============================
# Secrets / Model
# ===============================
api_key = None
model_default = "gpt-4.1-mini"
try:
    api_key = st.secrets.get("OPENAI_API_KEY", None)
    model_default = st.secrets.get("OPENAI_MODEL", model_default)
except Exception:
    api_key = None

model = st.text_input(T["MODEL"], value=model_default)

if api_key:
    st.success(T["KEY_OK"])
else:
    st.warning(T["NO_KEY"])

# ===============================
# Session Memory
# ===============================
if "aspiral_memory" not in st.session_state:
    st.session_state.aspiral_memory = []
if "decision_trace" not in st.session_state:
    st.session_state.decision_trace = []

colA, colB = st.columns([1, 3])
with colA:
    if st.button(T["CLEAR"]):
        st.session_state.aspiral_memory = []
        st.session_state.decision_trace = []
        st.rerun()

st.divider()

# ===============================
# Helpers: OpenAI Responses API (read-only)
# ===============================
def _extract_text_from_responses(payload: dict) -> str:
    """
    Extract text from OpenAI Responses API structure.
    Falls back to pretty JSON if unexpected structure.
    """
    try:
        out = payload.get("output", [])
        texts = []
        for item in out:
            for c in item.get("content", []):
                if c.get("type") in ("output_text", "text") and "text" in c:
                    texts.append(c["text"])
        if texts:
            return "\n\n".join(texts).strip()
    except Exception:
        pass
    return json.dumps(payload, ensure_ascii=False, indent=2)

def shadow_llm_insight(intent: str, language: str, model_id: str) -> dict:
    """
    Read-only analysis: NO tool use, NO execution.
    Returns structured JSON when possible.
    """
    if not api_key:
        return {
            "mode": "simulated",
            "insight": T["SIMULATED"],
            "fit": {"semantic": "unknown", "structural": "unknown", "temporal": "unknown"},
            "risks": [],
            "prerequisites": [],
            "suggested_next_steps": ["Add Secrets and retry."]
        }

    instructions = (
        "You are ALIENGBUK Shadow LLM. READ-ONLY ANALYSIS ONLY. "
        "You must NOT propose executing real commands. You must NOT use tools. "
        "Return STRICT JSON with keys: "
        "insight, fit {semantic, structural, temporal}, risks, prerequisites, suggested_next_steps. "
        "Keep it concise and practical."
    )

    body = {
        "model": model_id,
        "instructions": instructions,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            f"LANG={language}\n"
                            f"INTENT={intent}\n\n"
                            "System state: SAFE MODE, real executor is BLOCKED. "
                            "We are planning/analysis only."
                        ),
                    }
                ],
            }
        ],
        "max_output_tokens": 650,
    }

    url = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    last_err = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                url=url,
                data=json.dumps(body).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                payload = json.loads(resp.read().decode("utf-8"))

            text = _extract_text_from_responses(payload)

            # Try to parse as JSON (we requested STRICT JSON)
            try:
                data = json.loads(text)
                data["mode"] = "llm"
                return data
            except Exception:
                return {"mode": "llm_raw", "raw_text": text}

        except urllib.error.HTTPError as e:
            last_err = f"HTTPError {e.code}: {e.reason}"
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(2 ** attempt)
                continue
            return {"mode": "error", "error": last_err}
        except Exception as e:
            last_err = str(e)
            time.sleep(2 ** attempt)

    return {"mode": "error", "error": last_err or "Unknown error"}

# ===============================
# User Input
# ===============================
intent = st.text_area(T["INPUT_LABEL"], height=120)

# ===============================
# Trigger
# ===============================
if st.button(T["BTN"]) and intent.strip():
    ts = datetime.utcnow().isoformat()

    # -------- Shadow Planner (structural, deterministic) --------
    planner = {
        "intent": intent,
        "evaluation": [
            "Semantic fit (meaning/context)",
            "Structural fit (where it belongs)",
            "Temporal fit (is this the right stage?)",
        ],
        "decision": "DO_NOT_EXECUTE",
        "reason": "SAFE MODE: executor is blocked. Planning/analysis only.",
        "timestamp": ts,
    }

    # -------- Shadow LLM Insight (read-only) --------
    insight = shadow_llm_insight(intent=intent, language=lang, model_id=model)

    # -------- Shadow Executor (always blocked) --------
    executor = {
        "would_execute": False,
        "blocked": True,
        "why": "SAFE MODE: Real execution is not authorized in this era.",
        "timestamp": ts,
    }

    # -------- Aspiral Memory Entry --------
    mem = {
        "timestamp": ts,
        "intent": intent,
        "status": "Em espera" if lang == "pt" else "Pending",
        "note": (
            "Candidata armazenada. Reavaliar quando contexto e permissão evoluírem."
            if lang == "pt"
            else "Stored candidate. Re-evaluate when context and permission evolve."
        ),
        "planner_decision": planner["decision"],
        "llm_mode": insight.get("mode", "unknown"),
        "llm_fit": insight.get("fit", {}),
    }

    st.session_state.decision_trace.append(
        {"timestamp": ts, "planner": planner, "llm": insight, "executor": executor}
    )
    st.session_state.aspiral_memory.append(mem)

    # -------- UI Output --------
    with st.expander(T["PLANNER_TITLE"], expanded=True):
        st.json(planner)

    with st.expander(T["LLM_TITLE"], expanded=True):
        st.json(insight)

    with st.expander(T["EXEC_TITLE"], expanded=True):
        st.json(executor)

st.divider()

# ===============================
# Memory Viewer
# ===============================
with st.expander(T["MEM_TITLE"], expanded=False):
    if st.session_state.aspiral_memory:
        # Show last 20, newest first
        for i, mem in enumerate(reversed(st.session_state.aspiral_memory[-20:]), 1):
            st.markdown(f"**{i}.** `{mem['intent']}`")
            st.caption(
                f"{mem['status']} • {mem['timestamp']} • decision={mem.get('planner_decision','?')} • llm={mem.get('llm_mode','?')}"
            )
            if mem.get("llm_fit"):
                st.code(f"fit: {json.dumps(mem['llm_fit'], ensure_ascii=False)}", language="json")
            st.markdown(f"> {mem['note']}")
            st.divider()
    else:
        st.caption("Nenhuma memória registrada ainda." if lang == "pt" else "No memory recorded yet.")

# ===============================
# Status
# ===============================
st.info(T["STATUS"])
st.caption("ALIENGBUK • Shadow Pipeline + Shadow LLM • Spiral-Up Evolution • SAFE MODE")
