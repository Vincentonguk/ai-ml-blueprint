from groq import Groq

# ==========================================
#   CONFIG GROQ – MODELO HÍBRIDO
# ==========================================

def choose_model(task: str) -> str:
    task = task.lower()

    # Tarefas que precisam de raciocínio complexo
    if any(x in task for x in ["planejar", "analisar", "explicar", "estratégia", "motivo"]):
        return "llama3-70b-8192"

    # Tarefas longas (RAG, documentos, resumos)
    if any(x in task for x in ["documento", "texto", "resumo", "rag"]):
        return "mixtral-8x7b-32768"

    # Padrão (rápido)
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
  {{"id": 1, "name": "Stage 1", "description": "..." }},
  {{"id": 2, "name": "Stage 2", "description": "..." }},
  {{"id": 3, "name": "Stage 3", "description": "..." }}
]
"""

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        try:
            return json.loads(response.choices[0].message.content)
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

        return response.choices[0].message.content


# ==========================================
#   CRITIC
# ==========================================

class Critic:
    def __init__(self, client: Groq):
        self.client = client

    def review(self, goal, plan, results):
        model = "llama3-70b-8192"  # crítico sempre usa mais inteligência

        prompt = f"""
Você é um crítico. Avalie a execução.

OBJETIVO:
{goal}

PLANO:
{plan}

RESULTADOS:
{results}

Liste 3 melhorias possíveis.
"""

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.split("\n")


# ==========================================
#   ORCHESTRATOR
# ==========================================

def run_multi_agent(goal: str, groq_client: Groq):
    log = []
    log.append("🧠 Sistema Multi-Agente (Modo Híbrido GROQ Ativado)")
    log.append(f"🎯 Objetivo: {goal}")
    log.append("")

    planner = Planner(groq_client)
    plan = planner.plan(goal)

    if not plan:
        return "❌ O planner não conseguiu gerar um plano."

    log.append("📌 PLANO GERADO:")
    for step in plan:
        log.append(f"- {step['id']}: {step['name']} → {step['description']}")

    worker = Worker(groq_client)
    critic = Critic(groq_client)

    results = []

    for stage in plan:
        out = worker.execute(stage)
        results.append({"name": stage["name"], "output": out})
        log.append("\⚙️ EXECUTADO:")
        log.append(out)

    log.append("\n🔍 CRÍTICO:")
    feedback = critic.review(goal, plan, results)
    for line in feedback:
        log.append(f"- {line}")

    log.append("\n✅ Execução Finalizada.")

    return "\n".join(log)
