import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. Dataset path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "../data/processed/url_dataset.csv")

# 2. Load dataset
data = pd.read_csv(dataset_path)

# 3. Debug prints (NOW it's correct)
print(data.columns)
print(data.head())

# 4. Features & labels
# Features & label
X = data.drop("label", axis=1)
y = data["label"]

# 5. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 6. Vectorization
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 7. Model training
# 1. Model definition (MUST come first)
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

# 2. Train model
model.fit(X_train, y_train)

# 3. Predict
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(urls)

pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))
# 9. Save vectorizer
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

# 10. Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ model.pkl and vectorizer.pkl created successfully!")