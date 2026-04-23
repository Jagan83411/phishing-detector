# backend/main.py
from fastapi import FastAPI
import pickle
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(BASE_DIR, "vectorizer.pkl"), "rb"))

@app.get("/")
def home():
    return {"status": "Backend running"}

@app.post("/predict")
def predict(data: dict):
    text = data["text"]

    X = vectorizer.transform([text])
    prob = model.predict_proba(X)[0][1]

    if prob > 0.5:
        label = "PHISHING"
    else:
        label = "SAFE"

    return {
        "label": label,
        "confidence": round(prob * 100, 2)
    }