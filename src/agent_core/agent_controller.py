from typing import List, Dict, Any
from groq import Groq
import json


# =========================================================
#   ESCOLHA AUTOMÁTICA DO MODELO GROQ (COMPATÍVEL 2025)
# =========================================================

def choose_model(task: str) -> str:
    """
    Seleciona o modelo Groq correto baseado na tarefa.
    """

    text = (task or "").lower()

    # Palavras que indicam raciocínio mais profundo
    reasoning_keywords = ["planejar", "analisar", "explicar", "estratégia", "motivo"]

    # Usa modelo maior quando precisar raciocinar
    if any(x in text for x in reasoning_keywords):
        return "llama-3.3-70b-versatile"   # modelo grande e suportado

    # Modelo rápido padrão
    return "llama-3.3-8b-instant"          # modelo rápido e suportado



# =========================================================
#   PLANNER
# =========================================================

class Planner:
    """ Gera um plano com 3 etapas claras. """

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

        content = (response.choices[0].message.content or "").strip()

        # Tenta JSON direto
        try:
            data = json.loads(content)
            if isinstance(data, list):
                return data
        except:
            pass

        # Extrai apenas o trecho JSON, se necessário
        try:
            start = content.find("[")
            end = content.rfind("]") + 1
            if start >= 0 and end > start:
                data = json.loads(content[start:end])
                if isinstance(data, list):
                    return data
        except:
            pass

        return []



# =========================================================
#   WORKER
# =========================================================

class Worker:
    """ Executa cada etapa do plano. """

    def __init__(self, client: Groq):
        self.client = client

    def execute(self, stage: Dict[str, Any]) -> str:
        description = stage.get("description", "")
        model = choose_model(description)

        prompt = f"""
Você é um worker. Execute o estágio abaixo:

NOME: {stage.get('name')}
DESCRIÇÃO: {description}

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
    """ Analisa o resultado e sugere melhorias. """

    def __init__(self, client: Groq):
        self.client = client

    def review(self, goal: str, plan: List[Dict[str, Any]], results: List[Dict[str, str]]) -> List[str]:

        model = "llama-3.3-70b-versatile"  # crítico sempre usa modelo maior

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

        # Tenta JSON direto
        try:
            data = json.loads(content)
            return data.get("melhorias", [])
        except:
            pass

        # Fallback: extrair linhas
        lines = [
            line.strip("-• ").strip()
            for line in content.split("\n")
            if line.strip()
        ]

        return lines[:3]



# =========================================================
#   ORCHESTRATOR — SISTEMA MULTI-AGENTE
# =========================================================

def run_multi_agent(goal: str, groq_client: Groq) -> str:
    log: List[str] = []

    log.append("🧠 Sistema Multi-Agente (GROQ 2025 — Estável)")
    log.append(f"🎯 Objetivo: {goal}")
    log.append("")

    # PLANO
    planner = Planner(groq_client)
    plan = planner.plan(goal)

    if not plan:
        return "❌ O planner não conseguiu gerar um plano."

    log.append("📌 PLANO GERADO:")
    for step in plan:
        log.append(f"- {step['id']} — {step['name']}: {step['description']}")
    log.append("")

    # EXECUÇÃO
    worker = Worker(groq_client)
    results = []

    for stage in plan:
        output = worker.execute(stage)
        results.append({"name": stage["name"], "output": output})

        log.append("⚙️ EXECUTADO:")
        log.append(output)
        log.append("")

    # CRÍTICO
    critic = Critic(groq_client)
    log.append("🔍 CRÍTICO:")

    feedback = critic.review(goal, plan, results)

    for item in feedback:
        log.append(f"- {item}")

    log.append("")
    log.append("✅ Execução Finalizada.")

    return "\n".join(log)
