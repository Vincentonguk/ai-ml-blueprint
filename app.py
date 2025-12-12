import streamlit as st
from src.agent_core.agent_controller import AgentController

st.set_page_config(page_title="ALIENGBUK", layout="centered")
st.title("🧠 ALIENGBUK — Autonomous AI Agent")

objective = st.text_input("Digite seu objetivo em linguagem natural:")

if st.button("Executar") and objective:
    agent = AgentController()
    try:
        result = agent.run(objective)
        st.success("Execução finalizada")
        st.write(result)
    except Exception as e:
        st.error(str(e))
