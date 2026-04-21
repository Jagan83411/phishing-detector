def scan_text(text):
    X = vectorizer.transform([text])
    prob = model.predict_proba(X)[0][1]
    return "PHISHING" if prob > 0.5 else "SAFE"