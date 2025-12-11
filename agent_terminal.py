import os
from dotenv import load_dotenv
from groq import Groq
from src.agent_core.agent_controller import run_multi_agent

# Carrega variáveis do arquivo .env
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("❌ ERRO: A variável GROQ_API_KEY não existe. Crie seu arquivo .env!")

client = Groq(api_key=API_KEY)

print("🧠 ALIENGBUK — AGENTE AUTÔNOMO INICIADO")
print("Digite seu objetivo em linguagem natural.")
print("Digite 'sair' para encerrar.\n")

while True:
    goal = input("👉 Objetivo: ")

    if goal.lower() in ["sair", "exit", "quit"]:
        print("👋 Encerrando ALIENGBUK.")
        break

    response = run_multi_agent(goal, client)
    print("\n" + "=" * 80)
    print(response)
    print("=" * 80 + "\n")
