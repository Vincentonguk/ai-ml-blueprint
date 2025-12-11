from typing import List, Dict, Any
from groq import Groq
import json

# ==========================================
#   CONFIG GROQ – MODELO HÍBRIDO
# ==========================================

def choose_model(task: str) -> str:
    text = task.lower()

    reasoning_keywords = ["planejar", "analisar", "explicar", "estratégia", "motivo"]
    long_keywords = ["documento", "texto", "resumo", "rag"]

    if any(x in text for x in reasoning_keywords):
        return "llama3-70b-8192"

    if any(x in text for x in long_keywords):
        return "mixtral-8x7b-32768"

    return "mixtral-8x7b-32768"


# ==========================================
#   PLANNER
# ==========================================

class Planner:
    def __init__(self, client: Groq):
        self.client = client

    def plan(self, goal: str):
        model = choose_model(goal)

        prompt = f"""
Você é um planner especialista. Transforme o objetivo abaixo em 3 etapas claras.

OBJETIVO:
{goal}

Responda SOMENTE em JSON:
[
  {{"id": 1, "name": "Stage 1", "description": "..."}},
  {{"id": 2, "name": "Stage 2", "description": "..."}},
  {{"id": 3, "name": "Stage 3", "description": "..."}}
]
"""

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)
        except:
            try:
                start = content.find("[")
                end = content.rfind("]") + 1
                return json.loads(content[start:end])
            except:
                return []


# ==========================================
#   WORKER
# ==========================================

class Worker:
    def __init__(self, client: Groq):
        self.client = client

    def execute(self, stage):
        model = choose_model(stage["description"])

        prompt = f"""
Você é um worker. Execute o estágio abaixo:

NOME: {stage['name']}
DESCRIÇÃO: {stage['description']}

Explique passo a passo o que foi feito.
"""

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip()


# ==========================================
#   CRITIC
# ==========================================

class Critic:
    def __init__(self, client: Groq):
        self.client = client

    def review(self, goal, plan, results):
        model = "llama3-70b-8192"

        prompt = f"""
Você é um crítico. Avalie a execução:

OBJETIVO:
{goal}

PLANO:
{json.dumps(plan, indent=2, ensure_ascii=False)}

RESULTADOS:
{json.dumps(results, indent=2, ensure_ascii=False)}

Responda em JSON com este formato:

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
            data = json.loads(content)
            return data.get("melhorias", [])
        except:
            return ["Melhoria sugerida pelo modelo."]


# ==========================================
#   ORCHESTRATOR
# ==========================================

def run_multi_agent(goal: str, client: Groq) -> str:
    log = []
    log.append("🧠 Sistema Multi-Agente (GROQ)")
    log.append(f"🎯 Objetivo: {goal}\n")

    planner = Planner(client)
    plan = planner.plan(goal)

    if not plan:
        return "❌ O planner não conseguiu gerar um plano."

    log.append("📌 PLANO GERADO:")
    for step in plan:
        log.append(f"- {step['id']} — {step['name']}: {step['description']}")
    log.append("")

    worker = Worker(client)
    critic = Critic(client)

    results = []

    for stage in plan:
        output = worker.execute(stage)
        results.append({"stage": stage["name"], "output": output})

        log.append("⚙️ EXECUTADO:")
        log.append(output)
        log.append("")

    improvements = critic.review(goal, plan, results)

    log.append("🔍 CRÍTICO:")
    for item in improvements:
        log.append(f"- {item}")

    log.append("\n✅ Execução Finalizada.")

    return "\n".join(log)
