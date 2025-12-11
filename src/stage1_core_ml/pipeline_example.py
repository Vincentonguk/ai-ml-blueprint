import time
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

def monitor(metric, value):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[MONITOR] {timestamp} | {metric}: {value:.4f}")

def run_stage1_demo():
    print("\n[Stage 1] Core ML & Python Engineering")

    data = load_breast_cancer()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = data.target

    print("Optimizing memory usage...")
    X = X.astype("float32")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000, n_jobs=-1))
    ])

    start = time.time()
    pipeline.fit(X_train, y_train)
    duration = time.time() - start

    train_acc = pipeline.score(X_train, y_train)
    test_acc = pipeline.score(X_test, y_test)

    monitor("Train Accuracy", train_acc)
    monitor("Test Accuracy", test_acc)
    monitor("Training Time (s)", duration)

    preds = pipeline.predict(X_test)
    print("\nClassification Report:\n")
    print(classification_report(y_test, preds))

    print("\n✅ Stage 1 Complete — Production ML Pipeline Built.\n")
