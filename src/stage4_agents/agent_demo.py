class Planner:
    def plan(self, goal):
        return [
            f"Analyze goal: {goal}",
            "Collect relevant data",
            "Train baseline model",
            "Evaluate results",
            "Deploy system"
        ]

class Worker:
    def execute(self, steps):
        results = []
        for step in steps:
            results.append(f"Executed: {step}")
        return results

class Critic:
    def review(self, results):
        feedback = []
        for r in results:
            if "Deploy" in r:
                feedback.append("⚠️ Add monitoring, logging, and rollback strategy")
        if not feedback:
            feedback.append("✅ Execution looks safe, but continuous validation required")
        return feedback

def run_stage4_demo():
    print("\n[Stage 4] Agentic & Multi-Agent System Demo")

    goal = "Build a production-ready churn prediction system"

    planner = Planner()
    worker = Worker()
    critic = Critic()

    plan = planner.plan(goal)
    results = worker.execute(plan)
    feedback = critic.review(results)

    print("\nGOAL:", goal)
    print("\n--- PLAN ---")
    for step in plan:
        print("-", step)

    print("\n--- EXECUTION ---")
    for r in results:
        print("-", r)

    print("\n--- CRITIC FEEDBACK (SAFETY LAYER) ---")
    for f in feedback:
        print("-", f)

    print("\n✅ Stage 4 Complete — Agents Orchestrated with Validation.\n")
