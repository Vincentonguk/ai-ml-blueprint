import io
import sys
from typing import Callable, Dict, List

from src.stage1_core_ml.pipeline_example import run_stage1_demo
from src.stage2_deep_learning.cnn_example import run_stage2_demo
from src.stage3_nlp_llm.nlp_demo import run_stage3_demo
from src.stage4_agents.agent_demo import run_stage4_demo
from src.stage5_rag_generative.rag_demo import run_stage5_demo
from src.stage6_leadership.leadership_demo import run_stage6_demo


def capture_output(func: Callable[[], None]) -> str:
    """Captura tudo que a função imprimir no console"""
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer
    try:
        func()
    finally:
        sys.stdout = old_stdout
    return buffer.getvalue()


STAGES: Dict[str, Dict] = {
    "stage1": {
        "name": "Stage 1 – Core ML & Python Engineering",
        "keywords": ["ml", "machine learning", "modelo", "produção", "deploy"],
        "runner": run_stage1_demo,
    },
    "stage2": {
        "name": "Stage 2 – Deep Learning Mastery",
        "keywords": ["deep", "deep learning", "cnn", "imagem", "visão"],
        "runner": run_stage2_demo,
    },
    "stage3": {
        "name": "Stage 3 – NLP & LLM Engineering",
        "keywords": ["nlp", "texto", "sentimento", "resumo", "llm"],
        "runner": run_stage3_demo,
    },
    "stage4": {
        "name": "Stage 4 – Agentic & Multi-Agent Systems",
        "keywords": [
            "agente", "agentes", "agent",
            "planner", "worker", "critic",
            "multi-agente", "autônomo",
            "decisão", "validar"
        ],
        "runner": run_stage4_demo,
    },
    "stage5": {
        "name": "Stage 5 – Generative AI & RAG",
        "keywords": ["rag", "busca", "documento", "contexto"],
        "runner": run_stage5_demo,
    },
    "stage6": {
        "name": "Stage 6 – Leadership & Strategy",
        "keywords": ["liderança", "estratégia", "governança", "gestão"],
        "runner": run_stage6_demo,
    },
}


def _detect_stages(goal: str) -> List[str]:
    goal_lower = goal.lower()
    selected = []

    for sid, info in STAGES.items():
        for kw in info["keywords"]:
            if kw in goal_lower:
                selected.append(sid)
                break

    return selected


def run_agent(goal: str) -> str:
    log_lines: List[str] = []

    log_lines.append("🤖 AGENT ORCHESTRATOR – MODO INTENCIONAL")
    log_lines.append(f"Objetivo recebido: {goal}")
    log_lines.append("")

    selected = _detect_stages(goal)

    if not selected:
        return (
            "❌ Objetivo não reconhecido pelo agente.\n"
            "Use termos como: ML, Deep, NLP, Agente, RAG ou Liderança."
        )

    for stage_id in selected:
        info = STAGES[stage_id]
        log_lines.append(f"===== EXECUTANDO: {info['name']} =====")

        try:
            result = capture_output(info["runner"])
            log_lines.append(result)
        except Exception as e:
            log_lines.append(f"[ERRO]: {e}")

        log_lines.append("")

    log_lines.append("🏁 Execução finalizada.")
    return "\n".join(log_lines)
