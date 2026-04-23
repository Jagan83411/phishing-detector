import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# -----------------------------
# PATH
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "../data/processed/url_dataset.csv")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(dataset_path)

print("Columns:", df.columns)
print(df.head())

# -----------------------------
# FEATURES & LABEL
# -----------------------------
X = df.drop("label", axis=1)   # ✅ USE EXISTING FEATURES
y = df["label"]

# -----------------------------
# SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# MODEL
# -----------------------------
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# -----------------------------
# EVALUATE
# -----------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Accuracy: {accuracy * 100:.2f}%")

# -----------------------------
# SAVE
# -----------------------------
model_path = os.path.join(BASE_DIR, "../model.pkl")

with open(model_path, "wb") as f:
    pickle.dump(model, f)

print("✅ model.pkl saved!")