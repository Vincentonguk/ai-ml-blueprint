import os
from dotenv import load_dotenv
from groq import Groq
from src.agent_core.agent_controller import run_multi_agent

# ==========================================
#   CARREGAR VARIÁVEIS DE AMBIENTE (.env)
# ==========================================
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("❌ ERRO: A variável GROQ_API_KEY não existe. Crie o arquivo .env na raiz do projeto contendo:\nGROQ_API_KEY=SUACHAVEAQUI")

# Criar cliente GROQ
client = Groq(api_key=API_KEY)

# ==========================================
#   INTERFACE DO TERMINAL ALIENGBUK
# ==========================================
print("🧠 ALIENGBUK — AGENTE AUTÔNOMO INICIADO")
print("Digite seu objetivo em linguagem natural.")
print("Digite 'sair' para encerrar.\n")

while True:
    goal = input("👉 Objetivo: ")

    if goal.lower() in ["sair", "exit", "quit"]:
        print("👋 Encerrando ALIENGBUK.")
        break

    # Executa o sistema multi-agente
    try:
        response = run_multi_agent(goal, client)
    except Exception as e:
        response = f"❌ ERRO DURANTE EXECUÇÃO DO AGENTE:\n{e}"

    print("\n" + "=" * 80)
    print(response)
    print("=" * 80 + "\n")
