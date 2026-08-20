import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Sample dataset
data = {
    'url_length': [20, 75, 50, 90],
    'https': [1, 0, 1, 0],
    'dots': [2, 5, 3, 7],
    'hyphens': [0, 4, 1, 5],
    'ats': [0, 1, 0, 2],
    'digits': [1, 8, 2, 10],
    'suspicious': [0, 4, 1, 5],
    'label': [0, 1, 0, 1]
}

df = pd.DataFrame(data)

X = df.drop('label', axis=1)
y = df['label']

model = RandomForestClassifier()

model.fit(X, y)

joblib.dump(model, 'phishing_model.pkl')

print("Model trained successfully")