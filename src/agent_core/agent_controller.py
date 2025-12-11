from typing import List, Dict, Any
from groq import Groq
import json


# =========================================================
#   ESCOLHA AUTOMÁTICA DO MODELO GROQ (ATUALIZADO 2025)
# =========================================================

def choose_model(task: str) -> str:
    """
    Escolhe automaticamente o melhor modelo Groq
    com base na descrição da tarefa.
    """

    text = (task or "").lower()

    # Palavras que indicam raciocínio profundo
    reasoning_keywords = ["planejar", "analisar", "explicar", "estratégia", "motivo"]

    # Se precisar de raciocínio → usa o modelo mais inteligente atual
    if any(x in text for x in reasoning_keywords):
        return "llama-3.1-405b-reasoning"

    # Caso contrário → modelo rápido
    return "llama-3.1-8b-instant"



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

        # JSON direto
        try:
            data = json.loads(content)
            if isinstance(data, list):
                return data
        except:
            pass

        # Extrair trecho JSON
        try:
            start = content.find("[")
            end = content.rfind("]") + 1
            if start != -1 and end > start:
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
    """ Avalia o trabalho e sugere melhorias. """

    def __init__(self, client: Groq):
        self.client = client

    def review(
        self,
        goal: str,
        plan: List[Dict[str, Any]],
        results: List[Dict[str, str]],
    ) -> List[str]:

        # Sempre usa modelo mais inteligente
        model = "llama-3.1-405b-reasoning"

        prompt = f"""
Você é um crítico. Avalie a execução.

OBJETIVO:
{goal}

PLANO:
{json.dumps(plan, ensure_ascii=False, indent=2)}

RESULTADOS:
{json.dumps(results, ensure_ascii=False, indent=2)}

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

        content = (response.choices[0].message.content or "").strip()

        # JSON direto
        try:
            data = json.loads(content)
            return [m.strip() for m in data.get("melhorias", [])]
        except:
            pass

        # Fallback
        lines = [line.strip("-• ").strip() for line in content.split("\n") if line.strip()]
        return lines[:3]



# =========================================================
#   ORCHESTRATOR — SISTEMA MULTI-AGENTE
# =========================================================

def run_multi_agent(goal: str, groq_client: Groq) -> str:
    log: List[str] = []

    log.append("🧠 Sistema Multi-Agente (GROQ 2025 — Versão Estável)")
    log.append(f"🎯 Objetivo: {goal}")
    log.append("")

    # PLANNER
    planner = Planner(groq_client)
    plan = planner.plan(goal)

    if not plan:
        return "❌ O planner não conseguiu gerar um plano."

    log.append("📌 PLANO GERADO:")
    for step in plan:
        log.append(f"- {step.get('id')} — {step.get('name')}: {step.get('description')}")
    log.append("")

    # WORKER + CRITIC
    worker = Worker(groq_client)
    critic = Critic(groq_client)

    results: List[Dict[str, Any]] = []

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

    log.append("")
    log.append("✅ Execução Finalizada.")

    return "\n".join(log)
