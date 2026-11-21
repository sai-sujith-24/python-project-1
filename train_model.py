"""Train a demonstration model on user-supplied labeled URLs.

Input CSV must have 'url' and 'label' columns; label: 1=phishing, 0=benign.
The Flask app intentionally uses transparent heuristics until a model is validated.
"""
import argparse
from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from feature_extraction import extract_features


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=Path, help="CSV containing url,label")
    parser.add_argument("--output", default="phishing_model.pkl")
    args = parser.parse_args()
    df = pd.read_csv(args.dataset)
    if not {"url", "label"}.issubset(df.columns):
        parser.error("CSV must contain url and label columns")
    df = df.dropna(subset=["url", "label"]).copy()
    if len(df) < 20 or df["label"].nunique() != 2:
        parser.error("Provide at least 20 labeled URLs from both classes")
    x = [extract_features(str(url)) for url in df["url"]]
    y = df["label"].astype(int)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, stratify=y, random_state=42
    )
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(x_train, y_train)
    print(classification_report(y_test, model.predict(x_test), zero_division=0))
    joblib.dump(model, args.output)
    print("Saved experimental model to", args.output)


if __name__ == "__main__":
    main()
