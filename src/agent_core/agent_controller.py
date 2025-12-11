from typing import List, Dict, Any
from groq import Groq
import json

# =========================================================
#   ESCOLHA AUTOMÁTICA DO MODELO (MODELOS SUPORTADOS 2025)
# =========================================================

def choose_model(task: str) -> str:
    text = (task or "").lower()

    # Palavras que indicam necessidade de raciocínio profundo
    reasoning_keywords = ["planejar", "analisar", "explicar", "estratégia", "motivo"]

    # Modelo forte atual da Groq
    if any(x in text for x in reasoning_keywords):
        return "llama-3.1-70b-versatile"

    # Modelo rápido / padrão
    return "llama-3.1-8b-instant"


# =========================================================
#   PLANNER
# =========================================================

class Planner:
    def __init__(self, client: Groq):
        self.client = client

    def plan(self, goal: str) -> List[Dict[str, Any]]:
        model = choose_model(goal)

        prompt = f"""
Você é um planner especialista. Transforme o objetivo abaixo em 3 etapas claras.

OBJETIVO:
{goal}

Responda SOMENTE em JSON:
[
  {{"id": 1, "name": "Etapa 1", "description": "..." }},
  {{"id": 2, "name": "Etapa 2", "description": "..." }},
  {{"id": 3, "name": "Etapa 3", "description": "..." }}
]
"""

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )

        content = (response.choices[0].message.content or "").strip()

        try:
            data = json.loads(content)
            if isinstance(data, list):
                return data
        except:
            pass

        try:
            start = content.find("[")
            end = content.rfind("]") + 1
            if start != -1 and end > start:
                data = json.loads(content[start:end])
                return data
        except:
            pass

        return []


# =========================================================
#   WORKER
# =========================================================

class Worker:
    def __init__(self, client: Groq):
        self.client = client

    def execute(self, stage: Dict[str, Any]) -> str:
        model = choose_model(stage.get("description", ""))

        prompt = f"""
Você é um worker. Execute o estágio abaixo:

NOME: {stage.get('name')}
DESCRIÇÃO: {stage.get('description')}

Explique passo a passo o que foi feito.
"""

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )

        return (response.choices[0].message.content or "").strip()


# =========================================================
#   CRITIC
# =========================================================

class Critic:
    def __init__(self, client: Groq):
        self.client = client

    def review(self, goal: str, plan: List[Dict[str, Any]], results: List[Dict[str, str]]):
        model = "llama-3.1-70b-versatile"

        prompt = f"""
Você é um crítico. Avalie o planejamento e execução.

OBJETIVO:
{goal}

PLANO:
{json.dumps(plan, ensure_ascii=False, indent=2)}

RESULTADOS:
{json.dumps(results, ensure_ascii=False, indent=2)}

Responda em JSON:
{{
  "melhorias": [
    "Melhoria 1...",
    "Melhoria 2...",
    "Melhoria 3..."
  ]
}}
"""

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )

        content = (response.choices[0].message.content or "").strip()

        try:
            parsed = json.loads(content)
            return parsed.get("melhorias", [])
        except:
            pass

        lines = [l.strip("-• ").strip() for l in content.split("\n") if l.strip()]
        return lines[:3]


# =========================================================
#   ORCHESTRATOR
# =========================================================

def run_multi_agent(goal: str, groq_client: Groq) -> str:
    log = []

    log.append("🧠 Sistema Multi-Agente (GROQ 2025)")
    log.append(f"🎯 Objetivo: {goal}")
    log.append("")

    planner = Planner(groq_client)
    plan = planner.plan(goal)

    if not plan:
        return "❌ O planner não conseguiu gerar um plano."

    log.append("📌 PLANO GERADO:")
    for step in plan:
        log.append(f"- {step.get('id')} — {step.get('name')}: {step.get('description')}")
    log.append("")

    worker = Worker(groq_client)
    critic = Critic(groq_client)

    results = []

    for stage in plan:
        output = worker.execute(stage)
        results.append({"name": stage.get("name"), "output": output})

        log.append("⚙️ EXECUTADO:")
        log.append(output)
        log.append("")

    log.append("🔍 CRÍTICO:")
    feedback = critic.review(goal, plan, results)

    for item in feedback:
        log.append(f"- {item}")

    log.append("\n✅ Execução finalizada.")

    return "\n".join(log)
