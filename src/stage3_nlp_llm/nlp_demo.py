from transformers import pipeline

def run_stage3_demo():
    print("\n[Stage 3] NLP & Transformers Demo")

    summarizer = pipeline("summarization", model="facebook/bart-base")
    sentiment = pipeline("text-classification")

    text = '''
    Machine learning engineers build scalable training systems,
    deploy models into production, and monitor real-world predictions.
    '''

    summary = summarizer(text, max_length=40, min_length=15, do_sample=False)[0]["summary_text"]
    print("Summary:", summary)

    result = sentiment("I love building AI systems!")
    print("Sentiment:", result)

    print("\n✅ Stage 3 Complete — Context-Aware NLP Running.\n")
