from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

vectorizer = pickle.load(open("../vectorizer.pkl", "rb"))
model = pickle.load(open("../model.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    url = request.json["url"]

    X = vectorizer.transform([url])
    prob = model.predict_proba(X)[0][1]

    return jsonify({
        "result": "phishing" if prob > 0.5 else "safe",
        "confidence": float(prob)
    })

app.run(port=5000)