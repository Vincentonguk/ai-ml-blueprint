def run_stage6_demo():
    print("\n[Stage 6] AI Leadership & Strategy")

    team = {
        "ML Engineer": [
            "Build training pipelines",
            "Optimize models for performance"
        ],
        "Data Scientist": [
            "Experiment with models",
            "Define evaluation metrics"
        ],
        "MLOps Engineer": [
            "Deploy models",
            "Monitor drift and performance"
        ],
        "AI Lead": [
            "Define AI strategy",
            "Ensure ethics and governance",
            "Control budget and compute costs"
        ]
    }

    for role, duties in team.items():
        print(f"\n{role}:")
        for duty in duties:
            print(" -", duty)

    print("\n✅ Stage 6 Complete — Technical Leadership Mode Enabled.\n")
