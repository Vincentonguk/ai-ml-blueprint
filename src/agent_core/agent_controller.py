from typing import List, Dict, Any
from groq import Groq
import json


# ==========================================
#   CONFIG GROQ – MODELO HÍBRIDO
# ==========================================

def choose_model(task: str) -> str:
    """
    Escolhe automaticamente o melhor modelo Groq
    com base na descrição da tarefa.
    """
    text = (task or "").lower()

    # Tarefas que precisam de raciocínio complexo
    reasoning_keywords = ["planejar", "analisar", "explicar", "estratégia", "motivo"]

    # Tarefas longas (RAG, documentos, resumos)
    long_keywords = ["documento", "texto", "resumo", "rag"]

    if any(x in text for x in reasoning_keywords):
        return "llama3-70b-8192"

    if any(x in text for x in long_keywords):
        return "mixtral-8x7b-32768"

    # Padrão (rápido)
    return "mixtral-8x7b-32768"


# ==========================================
#   PLANNER
# ==========================================

class Planner:
    """
    Responsável por transformar um objetivo em um plano
    com múltiplos estágios.
    """

    def __init__(self, client: Groq):
        self.client = client

    def plan(self, goal: str) -> List[Dict[str, Any]]:
        """
        Gera 3 etapas claras para atingir o objetivo.
        Retorna uma lista de estágios no formato:
        [{ "id": int, "name": str, "description": str }, ...]
        """
        model = choose_model(goal)

        prompt = f"""
Você é um planner especialista. Transforme o objetivo abaixo em 3 etapas claras.

OBJETIVO:
{goal}

Responda SOMENTE em JSON exatamente neste formato:
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

        # 1) Tenta decodificar o JSON diretamente
        try:
            data = json.loads(content)
            if isinstance(data, list):
                return data
        except Exception:
            pass

        # 2) Fallback: tenta extrair apenas o trecho entre [ ... ]
        try:
            start = content.find("[")
            end = content.rfind("]") + 1
            if start != -1 and end != -1:
                data = json.loads(content[start:end])
                if isinstance(data, list):
                    return data
        except Exception:
            pass

        # 3) Se nada der certo, retorna lista vazia
        return []


# ==========================================
#   WORKER
# ==========================================

class Worker:
    """
    Executa cada estágio do plano.
    """

    def __init__(self, client: Groq):
        self.client = client

    def execute(self, stage: Dict[str, Any]) -> str:
        """
        Recebe um estágio e retorna a explicação passo a passo da execução.
        """
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


# ==========================================
#   CRITIC
# ==========================================

class Critic:
    """
    Avalia o plano e a execução, sugerindo melhorias.
    """

    def __init__(self, client: Groq):
        self.client = client

    def review(
        self,
        goal: str,
        plan: List[Dict[str, Any]],
        results: List[Dict[str, str]],
    ) -> List[str]:
        """
        Retorna uma lista com 3 melhorias possíveis.
        """
        model = "llama3-70b-8192"  # crítico sempre usa modelo mais inteligente

        prompt = f"""
Você é um crítico. Avalie a execução.

OBJETIVO:
{goal}

PLANO:
{json.dumps(plan, ensure_ascii=False, indent=2)}

RESULTADOS:
{json.dumps(results, ensure_ascii=False, indent=2)}

Responda em JSON com EXATAMENTE este formato:

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

        # 1) Tenta decodificar o JSON
        try:
            data = json.loads(content)
            improvements = data.get("melhorias", [])
            return [str(m).strip() for m in improvements if str(m).strip()]
        except Exception:
            pass

        # 2) Fallback: quebra por linhas e limpa bullets
        lines = [
            line.strip("-• ").strip()
            for line in content.split("\n")
            if line.strip()
        ]
        return lines[:3]  # garante no máximo 3 itens


# ==========================================
#   ORCHESTRATOR
# ==========================================

def run_multi_agent(goal: str, groq_client: Groq) -> str:
    """
    Orquestra o fluxo completo:
    - Planner gera o plano
    - Worker executa cada estágio
    - Critic avalia tudo
    - Retorna um log de execução em texto
    """
    log: List[str] = []

    log.append("🧠 Sistema Multi-Agente (GROQ Modo Híbrido)")
    log.append(f"🎯 Objetivo: {goal}")
    log.append("")

    # ----- Planner -----
    planner = Planner(groq_client)
    plan = planner.plan(goal)

    if not plan:
        return "❌ O planner não conseguiu gerar um plano."

    log.append("📌 PLANO GERADO:")
    for step in plan:
        step_id = step.get("id")
        name = step.get("name")
        description = step.get("description")
        log.append(f"- {step_id} — {name}: {description}")
    log.append("")

    # ----- Execução -----
    worker = Worker(groq_client)
    critic = Critic(groq_client)

    results: List[Dict[str, Any]] = []

    for stage in plan:
        output = worker.execute(stage)
        results.append({"name": stage.get("name"), "output": output})

        log.append("⚙️ EXECUTADO:")
        log.append(output)
        log.append("")

    # ----- Crítico -----
    log.append("🔍 CRÍTICO:")
    feedback = critic.review(goal, plan, results)

    for item in feedback:
        log.append(f"- {item}")

    log.append("")
    log.append("✅ Execução Finalizada.")

    return "\n".join(log)
