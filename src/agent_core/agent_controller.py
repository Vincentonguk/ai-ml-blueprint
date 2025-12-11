from typing import List, Dict, Any
from groq import Groq
import json


# =========================================================
#   ESCOLHA AUTOMÁTICA DO MODELO GROQ (CORRETO 2025)
# =========================================================

def choose_model(task: str) -> str:
    """
    Escolhe automaticamente o melhor modelo Groq
    com base na descrição da tarefa.
    """
    text = (task or "").lower()

    reasoning_keywords = ["planejar", "analisar", "explicar", "estratégia", "motivo"]

    # Raciocínio → modelo avançado real
    if any(x in text for x in reasoning_keywords):
        return "llama-3.1-70b-versatile"

    # Geral → modelo rápido
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
  {{"id": 1, "name": "Stage 1", "description": "..." }},
  {{"id": 2, "name": "Stage 2", "description": "..." }},
  {{"id": 3, "name": "Stage 3", "description": "..." }}
]
"""

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)
        except:
            pass

        # fallback
        try:
            start = content.find("[")
            end = content.rfind("]") + 1
            return json.loads(content[start:end])
        except:
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

        return response.choices[0].message.content.strip()



# =========================================================
#   CRITIC
# =========================================================

class Critic:
    def __init__(self, client: Groq):
        self.client = client

    def review(self, goal, plan, results) -> List[str]:

        model = "llama-3.1-70b-versatile"

        prompt = f"""
Você é um crítico. Avalie a execução.

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

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)["melhorias"]
        except:
            lines = [l.strip("-• ") for l in content.split("\n") if l.strip()]
            return lines[:3]



# =========================================================
#   ORCHESTRATOR
# =========================================================

def run_multi_agent(goal: str, groq_client: Groq) -> str:
    log = []

    log.append("🧠 Sistema Multi-Agente (Modelos Groq Atuais)")
    log.append(f"🎯 Objetivo: {goal}")
    log.append("")

    planner = Planner(groq_client)
    plan = planner.plan(goal)

    if not plan:
        return "❌ O planner não conseguiu gerar um plano."

    log.append("📌 PLANO GERADO:")
    for s in plan:
        log.append(f"- {s['id']} — {s['name']}: {s['description']}")
    log.append("")

    worker = Worker(groq_client)
    critic = Critic(groq_client)

    results = []

    for stage in plan:
        output = worker.execute(stage)
        results.append({"name": stage["name"], "output": output})

        log.append("⚙️ EXECUTADO:")
        log.append(output)
        log.append("")

    feedback = critic.review(goal, plan, results)

    log.append("🔍 CRÍTICO:")
    for f in feedback:
        log.append(f"- {f}")

    log.append("")
    log.append("✅ Execução Finalizada.")

    return "\n".join(log)
