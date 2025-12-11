from src.stage1_core_ml.pipeline_example import run_stage1_demo
from src.stage2_deep_learning.cnn_example import run_stage2_demo
from src.stage3_nlp_llm.nlp_demo import run_stage3_demo
from src.stage4_agents.agent_demo import run_stage4_demo
from src.stage5_rag_generative.rag_demo import run_stage5_demo
from src.stage6_leadership.leadership_demo import run_stage6_demo

MENU = '''
==================== AI & ML BLUEPRINT ====================
1) Stage 1 – Core ML & Python Engineering
2) Stage 2 – Deep Learning Mastery
3) Stage 3 – NLP & LLM Engineering
4) Stage 4 – Agentic & Multi-Agent Systems
5) Stage 5 – Generative AI & RAG
6) Stage 6 – Leadership & Strategy
0) Exit
==========================================================
Your choice: '''

def main():
    while True:
        choice = input(MENU).strip()
        if choice == "1":
            run_stage1_demo()
        elif choice == "2":
            run_stage2_demo()
        elif choice == "3":
            run_stage3_demo()
        elif choice == "4":
            run_stage4_demo()
        elif choice == "5":
            run_stage5_demo()
        elif choice == "6":
            run_stage6_demo()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
