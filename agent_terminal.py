from src.agent_core.agent_controller import run_agent

print("🧠 ALIENGBUK — AGENTE AUTÔNOMO INICIADO")
print("Digite seu objetivo em linguagem natural.")
print("Digite 'sair' para encerrar.\n")

while True:
    goal = input("👉 Objetivo: ")

    if goal.lower() in ["sair", "exit", "quit"]:
        print("👋 Encerrando ALIENGBUK.")
        break

    response = run_agent(goal)
    print("\n" + "=" * 80)
    print(response)
    print("=" * 80 + "\n")
