import pickle
from features.url_features import extract_url_features

model = pickle.load(open('models/url_model.pkl', 'rb'))

url = input("Enter URL: ")

features = extract_url_features(url)

prediction = model.predict([list(features.values())])[0]
prob = model.predict_proba([list(features.values())])[0][prediction]

if prediction == 1:
    print(f"⚠️ Phishing ({prob*100:.2f}% confidence)")
else:
    print(f"✅ Legit ({prob*100:.2f}% confidence)")