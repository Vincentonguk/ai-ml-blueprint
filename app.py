import json
import time
import hashlib
from dataclasses import dataclass, asdict
import streamlit as st

# =========================================================
# Page Config
# =========================================================
st.set_page_config(
    page_title="ALIENGBUK",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =========================================================
# Internal Semantic Layer (v2) — single-file, safe fallback
# =========================================================
TEXT = {
    "pt": {
        "APP_TITLE": "🧠 ALIENGBUK",
        "TAGLINE": "Spiral-Up • Validação antes da ação • Memória Aspiral",
        "HOME_OK": "Streamlit está funcionando corretamente 🚀",
        "HOME_DESC": (
            "Este app é um **sistema em construção consciente**. "
            "Nesta fase, tudo é **read-only**: sem execução real, sem risco."
        ),
        "LANG_LABEL": "🌐 Idioma / Language",
        "TAB_HOME": "🏠 Home",
        "TAB_ARCH": "🌀 Arquitetura",
        "TAB_PIPE": "🧭 Shadow Pipeline",
        "TAB_TRACE": "🧾 Decision Trace",
        "TAB_MEMORY": "🗂️ Memória Aspiral",
        "ARCH_TITLE": "🧩 Construção do Sistema (Spiral-Up)",
        "ARCH_BODY": """
### 🌀 Evolução em Espiral (Spiral-Up)
O sistema evolui em **espiral ascendente** (não em loops de tentativa e erro):

- O que **não encaixa** → **não executa**
- O que **não serve agora** → **não apaga**
- O aprendizado vira **memória contextual**

### 🔍 Critérios de Encaixe
Uma alteração só é liberada quando existe:
- **Encaixe semântico**
- **Encaixe estrutural**
- **Encaixe temporal** (“é o momento certo?”)

Sem os 3, o sistema **bloqueia** e registra o motivo.

### 🧠 Memória Aspiral
Ideias rejeitadas viram **candidatas latentes**.
Quando o contexto muda e “parece” com um cenário anterior, a candidata pode ser **reativada**.
""",
        "PIPE_DESC": (
            "Aqui você vê a **pipeline em modo sombra**. "
            "Ela simula planejamento e decisões, mas **não executa comandos**."
        ),
        "GOAL_LABEL": "🎯 Objetivo (ex.: “verificar status do git e mostrar alterações”)",
        "OBS_LABEL": "👁️ Observações (contexto atual, logs, ambiente, etc.)",
        "RUN_SHADOW": "Rodar Shadow Plan (simulação)",
        "RESULTS": "Resultados",
        "TRACE_DESC": "Registro das decisões do sistema (por que liberou/bloqueou).",
        "MEM_DESC": "Candidatas latentes (idéias guardadas) + reativação por similaridade.",
        "ADD_CAND": "Adicionar candidata à memória",
        "CAND_TITLE": "Título curto da candidata",
        "CAND_BODY": "Descrição / snippet / ideia",
        "CAND_TAGS": "Tags (separadas por vírgula) — ex: rag, pipeline, executor",
        "SAVE_CAND": "Salvar candidata",
        "SIMILARITY": "Similaridade com contexto atual",
        "REACTIVATE": "Reativar candidata",
        "EXPORT": "Exportar JSON (memória + trace)",
        "IMPORT": "Importar JSON",
        "UPLOAD": "Envie um JSON exportado anteriormente",
        "DANGER_NOTE": "🔒 **Nenhuma execução real ocorre nesta fase.**",
        "PIPE_SLOTS": """
### 🧩 Slots de Pipeline (somente leitura)
- Planner → **Conectado (simulado)**
- Executor → **Bloqueado (sem comandos)**
- Feedback Loop → **Ativo (trace e memória)**
- Git → **Somente leitura (conceitual)**
- ARG/RAG → **Preparação**
""",
        "STATUS": "📌 Status: Base validada • Shadow Pipeline ativo • Execução real ainda bloqueada",
    },
    "en": {
        "APP_TITLE": "🧠 ALIENGBUK",
        "TAGLINE": "Spiral-Up • Validate before action • Aspiral Memory",
        "HOME_OK": "Streamlit is working correctly 🚀",
        "HOME_DESC": (
            "This app is a **consciously built system**. "
            "In this phase everything is **read-only**: no real execution, no risk."
        ),
        "LANG_LABEL": "🌐 Language / Idioma",
        "TAB_HOME": "🏠 Home",
        "TAB_ARCH": "🌀 Architecture",
        "TAB_PIPE": "🧭 Shadow Pipeline",
        "TAB_TRACE": "🧾 Decision Trace",
        "TAB_MEMORY": "🗂️ Aspiral Memory",
        "ARCH_TITLE": "🧩 System Construction (Spiral-Up)",
        "ARCH_BODY": """
### 🌀 Spiral-Up Evolution
The system evolves in an **ascending spiral** (not closed trial-and-error loops):

- If it **doesn't fit** → **do not execute**
- If it **doesn't serve now** → **do not delete**
- Learning becomes **contextual memory**

### 🔍 Fit Criteria
A change is allowed only when we have:
- **Semantic fit**
- **Structural fit**
- **Temporal fit** (“is it the right moment?”)

Without all 3, the system **blocks** and records the reason.

### 🧠 Aspiral Memory
Rejected ideas become **latent candidates**.
When context becomes similar, they can be **reactivated**.
""",
        "PIPE_DESC": (
            "This is the **shadow-mode pipeline**. "
            "It simulates planning and decisions, but **does not run commands**."
        ),
        "GOAL_LABEL": "🎯 Goal (e.g., “check git status and show changes”)",
        "OBS_LABEL": "👁️ Observations (current context, logs, environment, etc.)",
        "RUN_SHADOW": "Run Shadow Plan (simulation)",
        "RESULTS": "Results",
        "TRACE_DESC": "Decision log (why it allowed/blocked).",
        "MEM_DESC": "Latent candidates + reactivation by similarity.",
        "ADD_CAND": "Add candidate to memory",
        "CAND_TITLE": "Short title",
        "CAND_BODY": "Description / snippet / idea",
        "CAND_TAGS": "Tags (comma-separated) — e.g., rag, pipeline, executor",
        "SAVE_CAND": "Save candidate",
        "SIMILARITY": "Similarity to current context",
        "REACTIVATE": "Reactivate candidate",
        "EXPORT": "Export JSON (memory + trace)",
        "IMPORT": "Import JSON",
        "UPLOAD": "Upload a previously exported JSON",
        "DANGER_NOTE": "🔒 **No real execution happens in this phase.**",
        "PIPE_SLOTS": """
### 🧩 Pipeline Slots (read-only)
- Planner → **Connected (simulated)**
- Executor → **Blocked (no commands)**
- Feedback Loop → **On (trace + memory)**
- Git → **Read-only (conceptual)**
- ARG/RAG → **Preparation**
""",
        "STATUS": "📌 Status: Base validated • Shadow Pipeline active • Real execution still blocked",
    },
    # FR/DE “beta”: fallback to EN automatically
    "fr": {},
    "de": {},
}


def t(key: str, lang: str) -> str:
    # fallback chain: chosen -> en -> pt -> key
    if lang in TEXT and key in TEXT[lang]:
        return TEXT[lang][key]
    if key in TEXT.get("en", {}):
        return TEXT["en"][key]
    if key in TEXT.get("pt", {}):
        return TEXT["pt"][key]
    return key


LANG_MAP = {
    "Português 🇧🇷": "pt",
    "English 🇺🇸": "en",
    "Français 🇫🇷 (soon)": "fr",
    "Deutsch 🇩🇪 (soon)": "de",
}

# =========================================================
# Data models
# =========================================================
@dataclass
class TraceItem:
    ts: float
    goal: str
    decision: str          # ALLOW / BLOCK / STORE / REACTIVATE
    reason: str
    stage: str             # planner / executor / feedback
    vars: dict


@dataclass
class Candidate:
    id: str
    ts: float
    title: str
    body: str
    tags: list
    last_score: float = 0.0
    status: str = "latent"  # latent / active / archived


# =========================================================
# Session state init
# =========================================================
if "trace" not in st.session_state:
    st.session_state.trace = []
if "memory" not in st.session_state:
    st.session_state.memory = []
if "last_goal" not in st.session_state:
    st.session_state.last_goal = ""
if "last_obs" not in st.session_state:
    st.session_state.last_obs = ""


def now_ts() -> float:
    return time.time()


def make_id(*parts: str) -> str:
    h = hashlib.sha256(("|".join(parts) + str(now_ts())).encode("utf-8")).hexdigest()
    return h[:12]


def add_trace(goal: str, decision: str, reason: str, stage: str, vars_: dict):
    st.session_state.trace.insert(
        0,
        TraceItem(ts=now_ts(), goal=goal, decision=decision, reason=reason, stage=stage, vars=vars_),
    )


def normalize(text: str) -> list:
    # super simple tokenization (no extra deps)
    text = (text or "").lower()
    for ch in ".,;:!?()[]{}<>/\\|\"'`~@#$%^&*-_=+—–\n\t":
        text = text.replace(ch, " ")
    tokens = [w for w in text.split(" ") if w.strip()]
    return tokens


def jaccard(a: str, b: str) -> float:
    A, B = set(normalize(a)), set(normalize(b))
    if not A and not B:
        return 0.0
    return len(A & B) / max(1, len(A | B))


def shadow_planner(goal: str, obs: str) -> dict:
    """
    Planner simulado:
    - gera steps conceituais
    - decide se deve BLOQUEAR (falta contexto) ou ARMAZENAR (candidato)
    - nunca executa nada
    """
    goal_l = (goal or "").lower()
    obs_l = (obs or "").lower()

    steps = []
    vars_ = {"goal_tokens": len(normalize(goal)), "obs_tokens": len(normalize(obs))}

    # Heurísticas simples (sem LLM, sem API)
    needs_git = "git" in goal_l or "commit" in goal_l or "push" in goal_l
    needs_files = "arquivo" in goal_l or "file" in goal_l or "pasta" in goal_l or "folder" in goal_l
    needs_api = "api" in goal_l or "openai" in goal_l or "key" in goal_l

    steps.append("Interpretar objetivo e classificar intenção (git / arquivos / api / ui).")
    steps.append("Checar se há contexto suficiente (observações).")
    steps.append("Gerar plano conceitual em passos.")
    steps.append("Registrar decisão no Decision Trace (ALLOW/BLOCK/STORE).")

    # Regras de bloqueio (temporais/estruturais)
    if needs_api:
        add_trace(goal, "BLOCK", "Pedido envolve API/key. Nesta fase a execução real está bloqueada.", "planner", vars_)
        return {
            "status": "BLOCK",
            "reason": "API/key solicitado — fase atual é read-only.",
            "steps": steps,
            "proposed_actions": ["Adicionar Secrets no Streamlit (futuro)", "Conectar LLM Planner (futuro)"],
        }

    if needs_git or needs_files:
        # Permitimos “simular plano”, mas bloqueamos execução
        add_trace(goal, "ALLOW", "Planejamento permitido. Execução real permanece bloqueada.", "planner", vars_)
        proposed = []
        if needs_git:
            proposed += ["Simular: git status", "Simular: git diff", "Simular: criar branch/commit (apenas roteiro)"]
        if needs_files:
            proposed += ["Simular: mkdir / criar arquivos (apenas roteiro)"]
        return {"status": "ALLOW", "reason": "Shadow plan ok.", "steps": steps, "proposed_actions": proposed}

    # Se objetivo é muito vago, vira candidato latente
    if len(normalize(goal)) < 4 and len(normalize(obs)) < 6:
        add_trace(goal, "STORE", "Objetivo/observações vagos. Armazenado como candidata latente.", "planner", vars_)
        return {
            "status": "STORE",
            "reason": "Pouco contexto — armazenar como candidata.",
            "steps": steps,
            "proposed_actions": ["Refinar objetivo", "Adicionar observações (logs/estado)"],
        }

    add_trace(goal, "ALLOW", "Planejamento permitido (genérico). Execução real bloqueada.", "planner", vars_)
    return {
        "status": "ALLOW",
        "reason": "Shadow plan ok (genérico).",
        "steps": steps,
        "proposed_actions": ["Organizar próximos passos", "Mapear dependências"],
    }


def store_candidate(title: str, body: str, tags_csv: str):
    tags = [x.strip() for x in (tags_csv or "").split(",") if x.strip()]
    cid = make_id(title, body)
    cand = Candidate(id=cid, ts=now_ts(), title=title.strip(), body=body.strip(), tags=tags)
    st.session_state.memory.insert(0, cand)
    add_trace(title, "STORE", "Candidata armazenada na memória aspiral.", "feedback", {"cid": cid, "tags": tags})


def reactivate_candidate(cid: str):
    for c in st.session_state.memory:
        if c.id == cid:
            c.status = "active"
            add_trace(c.title, "REACTIVATE", "Candidata reativada (contexto similar).", "feedback", {"cid": cid})
            return


def export_state() -> str:
    payload = {
        "version": 2,
        "trace": [asdict(x) for x in st.session_state.trace],
        "memory": [asdict(x) for x in st.session_state.memory],
        "last_goal": st.session_state.last_goal,
        "last_obs": st.session_state.last_obs,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def import_state(raw: str):
    data = json.loads(raw)
    trace = data.get("trace", [])
    memory = data.get("memory", [])
    st.session_state.trace = [TraceItem(**x) for x in trace]
    st.session_state.memory = [Candidate(**x) for x in memory]
    st.session_state.last_goal = data.get("last_goal", "")
    st.session_state.last_obs = data.get("last_obs", "")
    add_trace("IMPORT", "ALLOW", "Estado importado com sucesso.", "feedback", {"version": data.get("version")})


# =========================================================
# Top bar: Language selector
# =========================================================
lang_label = st.selectbox(t("LANG_LABEL", "pt"), list(LANG_MAP.keys()), index=0)
lang = LANG_MAP[lang_label]
if lang in ("fr", "de"):
    # fallback visible, never breaks
    st.caption("ℹ️ FR/DE estão em modo preview. Fallback automático para EN/PT quando faltar texto.")

# =========================================================
# Header
# =========================================================
st.title(t("APP_TITLE", lang))
st.caption(t("TAGLINE", lang))
st.success(t("HOME_OK", lang))
st.info(t("DANGER_NOTE", lang))
st.divider()

# =========================================================
# Tabs
# =========================================================
tabs = st.tabs([t("TAB_HOME", lang), t("TAB_ARCH", lang), t("TAB_PIPE", lang), t("TAB_TRACE", lang), t("TAB_MEMORY", lang)])

# -------------------------
# HOME
# -------------------------
with tabs[0]:
    st.write(t("HOME_DESC", lang))
    st.markdown(t("PIPE_SLOTS", lang))
    st.info(t("STATUS", lang))

# -------------------------
# ARCH
# -------------------------
with tabs[1]:
    st.subheader(t("ARCH_TITLE", lang))
    st.markdown(t("ARCH_BODY", lang))

# -------------------------
# SHADOW PIPELINE
# -------------------------
with tabs[2]:
    st.subheader("🧭 Shadow Pipeline")
    st.write(t("PIPE_DESC", lang))

    goal = st.text_input(t("GOAL_LABEL", lang), value=st.session_state.last_goal)
    obs = st.text_area(t("OBS_LABEL", lang), value=st.session_state.last_obs, height=140)

    cols = st.columns([1, 1, 2])
    with cols[0]:
        run = st.button(t("RUN_SHADOW", lang), use_container_width=True)
    with cols[1]:
        quick_store = st.button("🌀 Store as Candidate", use_container_width=True)

    if run:
        st.session_state.last_goal = goal
        st.session_state.last_obs = obs
        out = shadow_planner(goal, obs)

        st.markdown("### " + t("RESULTS", lang))
        st.write(f"**Status:** `{out['status']}`")
        st.write(f"**Reason:** {out['reason']}")

        st.markdown("#### Steps")
        for i, s in enumerate(out["steps"], 1):
            st.write(f"{i}. {s}")

        st.markdown("#### Proposed Actions (conceptual)")
        for a in out["proposed_actions"]:
            st.write(f"- {a}")

        # Similarity scan
        if st.session_state.memory:
            st.markdown("#### Candidate Recall (similarity scan)")
            ctx = f"{goal}\n{obs}"
            top = []
            for c in st.session_state.memory:
                score = jaccard(ctx, c.title + " " + c.body + " " + " ".join(c.tags))
                c.last_score = float(score)
                top.append((score, c))
            top.sort(key=lambda x: x[0], reverse=True)
            for score, c in top[:5]:
                st.write(f"- `{c.id}` • **{c.title}** • score={score:.2f} • status={c.status}")

    if quick_store:
        # store current goal/obs as a latent candidate
        if (goal or "").strip():
            store_candidate(
                title=(goal.strip()[:80] + ("..." if len(goal.strip()) > 80 else "")),
                body=(obs or "").strip() or "Sem observações.",
                tags_csv="shadow, candidate, spiral-up",
            )
            st.success("Candidata criada a partir do objetivo atual ✅")
        else:
            st.warning("Digite um objetivo antes de armazenar.")

# -------------------------
# TRACE
# -------------------------
with tabs[3]:
    st.subheader("🧾 Decision Trace")
    st.write(t("TRACE_DESC", lang))

    if not st.session_state.trace:
        st.info("Sem decisões registradas ainda.")
    else:
        # Filters
        fcols = st.columns([1, 1, 2])
        with fcols[0]:
            decision_filter = st.selectbox("Filtro (decision)", ["ALL", "ALLOW", "BLOCK", "STORE", "REACTIVATE"], index=0)
        with fcols[1]:
            stage_filter = st.selectbox("Filtro (stage)", ["ALL", "planner", "executor", "feedback"], index=0)

        items = st.session_state.trace
        if decision_filter != "ALL":
            items = [x for x in items if x.decision == decision_filter]
        if stage_filter != "ALL":
            items = [x for x in items if x.stage == stage_filter]

        for x in items[:50]:
            ts_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x.ts))
            with st.expander(f"{ts_str} • {x.decision} • {x.stage} • {x.goal[:60]}"):
                st.write("**Reason:**", x.reason)
                st.code(json.dumps(x.vars, ensure_ascii=False, indent=2), language="json")

    st.divider()
    st.subheader("📦 Import / Export")
    export_json = export_state()
    st.download_button(
        label=t("EXPORT", lang),
        data=export_json.encode("utf-8"),
        file_name="aliengbuk_state.json",
        mime="application/json",
        use_container_width=True,
    )

    up = st.file_uploader(t("UPLOAD", lang), type=["json"])
    if up is not None:
        try:
            raw = up.read().decode("utf-8")
            import_state(raw)
            st.success("Import OK ✅")
        except Exception as e:
            st.error(f"Falha ao importar: {e}")

# -------------------------
# MEMORY
# -------------------------
with tabs[4]:
    st.subheader("🗂️ Memória Aspiral")
    st.write(t("MEM_DESC", lang))

    st.markdown("### ➕ " + t("ADD_CAND", lang))
    c1, c2 = st.columns([1, 1])
    with c1:
        title = st.text_input(t("CAND_TITLE", lang))
    with c2:
        tags = st.text_input(t("CAND_TAGS", lang))

    body = st.text_area(t("CAND_BODY", lang), height=140)
    if st.button(t("SAVE_CAND", lang), use_container_width=True):
        if title.strip() and body.strip():
            store_candidate(title, body, tags)
            st.success("Salvo ✅")
        else:
            st.warning("Preencha título e descrição.")

    st.divider()

    if not st.session_state.memory:
        st.info("Sem candidatas ainda.")
    else:
        ctx = (st.session_state.last_goal or "") + "\n" + (st.session_state.last_obs or "")
        st.markdown("### 🔁 Recall (com base no contexto atual)")
        st.caption("Contexto atual = último Goal/Observations usados no Shadow Pipeline.")

        # Rank by similarity
        ranked = []
        for c in st.session_state.memory:
            score = jaccard(ctx, c.title + " " + c.body + " " + " ".join(c.tags))
            c.last_score = float(score)
            ranked.append((score, c))
        ranked.sort(key=lambda x: x[0], reverse=True)

        for score, c in ranked[:30]:
            header = f"{c.title}  •  score={score:.2f}  •  status={c.status}  •  id={c.id}"
            with st.expander(header):
                st.write(c.body)
                if c.tags:
                    st.caption("tags: " + ", ".join(c.tags))
                bcols = st.columns([1, 2, 2])
                with bcols[0]:
                    if st.button(f"✅ {t('REACTIVATE', lang)}", key=f"react_{c.id}"):
                        reactivate_candidate(c.id)
                        st.success("Reativada ✅")
                with bcols[1]:
                    if st.button("📦 Archive", key=f"arch_{c.id}"):
                        c.status = "archived"
                        add_trace(c.title, "ALLOW", "Candidata arquivada manualmente.", "feedback", {"cid": c.id})
                        st.success("Arquivada ✅")
                with bcols[2]:
                    if st.button("🧊 Set Latent", key=f"lat_{c.id}"):
                        c.status = "latent"
                        add_trace(c.title, "ALLOW", "Candidata marcada como latente.", "feedback", {"cid": c.id})
                        st.success("Latente ✅")

# =========================================================
# Footer
# =========================================================
st.caption("ALIENGBUK • Spiral-Up + Shadow Pipeline + Decision Trace + Aspiral Memory (safe mode)")
