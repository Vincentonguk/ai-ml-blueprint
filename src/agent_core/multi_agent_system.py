from typing import Any, Dict, List


# ================================
# 🧩 STAGES (simulação de estágios)
# ================================
STAGES = {
    "nlp": {
        "name": "NLP & LLM Engineering",
        "description": "Processamento de linguagem natural, classificação e análise de sentimentos.",
        "runner": lambda: "[NLP] Modelo de sentimentos carregado e analisando textos...",
    },
    "rag": {
        "name": "Generative AI & RAG",
        "description": "Busca vetorial em documentos com embeddings.",
        "runner": lambda: "[RAG] Base vetorial criada e pronta para consultas.",
    },
    "agents": {
        "name": "Agentic Systems",
        "description": "Sistema de agentes colaborativos.",
        "runner": lambda: "[AGENTS] Planner, Worker e Critic ativos.",
    },
}


# ================================
# 🔍 DETECTAR ESTÁGIOS POR OBJETIVO
# ================================
def _detect_stages(goal: str) -> List[str]:
    goal_lower = goal.lower()
    stages = []

    if "texto" in goal_lower or "sentimento" in goal_lower or "nlp" in goal_lower:
        stages.append("nlp")

    if "rag" in goal_lower or "documento" in goal_lower or "pdf" in goal_lower:
        stages.append("rag")

    if "agente" in goal_lower or "multi" in goal_lower:
        stages.append("agents")

    return stages


# ================================
# 📋 PLANNER
# ================================
class PlannerAgent:
    def plan(self, goal: str) -> Dict[str, Any]:
        stage_ids = _detect_stages(goal)

        steps = []
        for sid in stage_ids:
            steps.append(
                f"Rodar {STAGES[sid]['name']} para: {STAGES[sid]['description']}"
            )

        return {
            "goal": goal,
            "stage_ids": stage_ids,
            "steps": steps,
        }


# ================================
# ⚙️ WORKER
# ================================
class WorkerAgent:
    def execute(self, plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []

        for sid in plan["stage_ids"]:
            info = STAGES[sid]
            try:
                output = info["runner"]()
                results.append(
                    {
                        "stage_id": sid,
                        "name": info["name"],
                        "output": output,
                        "error": None,
                    }
                )
            except Exception as e:
                results.append(
                    {
                        "stage_id": sid,
                        "name": info["name"],
                        "output": "",
                        "error": str(e),
                    }
                )

        return results


# ================================
# 🧠 CRITIC
# ================================
class CriticAgent:
    def review(
        self, goal: str, plan: Dict[str, Any], results: List[Dict[str, Any]]
    ) -> List[str]:
        feedback = []

        if not plan["stage_ids"]:
            feedback.append("⚠️ Nenhum estágio técnico identificado para este objetivo.")
            return feedback

        feedback.append("✅ Pipeline executado com sucesso.")

        if "produção" in goal.lower():
            feedback.append("🚀 Considere adicionar pipeline de deploy e monitoramento.")

        return feedback


# ================================
# ✅ FUNÇÃO PRINCIPAL QUE ESTAVA FALTANDO
# ================================
def run_multi_agent(goal: str) -> str:
    log_lines: List[str] = []

    log_lines.append("🤖 ALIENGBUK — SISTEMA MULTI-AGENTE")
    log_lines.append(f"🎯 Objetivo recebido: {goal}")
    log_lines.append("")

    planner = PlannerAgent()
    worker = WorkerAgent()
    critic = CriticAgent()

    # 1️⃣ PLANEJAMENTO
    plan = planner.plan(goal)

    if not plan["stage_ids"]:
        log_lines.append("❌ Nenhum estágio compatível encontrado.")
        return "\n".join(log_lines)

    log_lines.append("📋 Plano de Execução:")
    for step in plan["steps"]:
        log_lines.append(f" - {step}")

    log_lines.append("")

    # 2️⃣ EXECUÇÃO
    log_lines.append("⚙️ Execução dos Estágios:")
    results = worker.execute(plan)

    for r in results:
        log_lines.append(f"\n===== {r['name']} =====")
        if r["error"]:
            log_lines.append(f"[ERRO] {r['error']}")
        else:
            log_lines.append(r["output"])

    # 3️⃣ CRÍTICA
    log_lines.append("\n🧠 Avaliação do Critic:")
    feedback = critic.review(goal, plan, results)
    for fb in feedback:
        log_lines.append(f" - {fb}")

    log_lines.append("\n🏁 Execução finalizada.")

    return "\n".join(log_lines)
