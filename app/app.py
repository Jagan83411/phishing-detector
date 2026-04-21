import streamlit as st
import pickle
import os
import re
import numpy as np
import pandas as pd
import random
import time
import sys   # ✅ IMPORTANT

# =====================================================
# FIX PYTHON PATH (MUST BE FIRST)
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))
cred_path = os.path.join(BASE_DIR, "credentials.json")

#flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
# =====================================================
# IMPORT MODULES (AFTER PATH FIX)
# =====================================================
from threat_db.db import check_url
from gmail_scanner.gmail_reader import get_service, fetch_emails

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="BlueSec SOC Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# LOAD MODEL
# =====================================================
vectorizer = pickle.load(open(os.path.join(BASE_DIR, "..", "vectorizer.pkl"), "rb"))
model = pickle.load(open(os.path.join(BASE_DIR, "..", "model.pkl"), "rb"))

# =====================================================
# CYBER UI
# =====================================================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(-45deg, #05070f, #0b1220, #0a0f1c, #020617);
    background-size: 400% 400%;
    animation: bg 10s ease infinite;
    color: #e5e7eb;
    font-family: monospace;
}

@keyframes bg {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.title {
    text-align: center;
    font-size: 34px;
    color: #3b82f6;
    font-weight: bold;
    text-shadow: 0 0 15px #3b82f6;
}

.card {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(59,130,246,0.3);
    padding: 20px;
    border-radius: 15px;
}

.stButton > button {
    background: linear-gradient(90deg, #2563eb, #1e40af);
    color: white;
    border-radius: 10px;
    padding: 10px 15px;
    font-weight: bold;
}

.terminal {
    background: black;
    color: #00ff88;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #00ff88;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================
st.markdown("<div class='title'>🛡️ BlueSec AI SOC Dashboard</div>", unsafe_allow_html=True)

st.write("Real-time phishing detection system (URL + Email + SOC)")

# =====================================================
# SIDEBAR
# =====================================================
mode = st.sidebar.radio("Select Mode", ["📊 SOC Dashboard", "💻 Hacker Terminal"])

# =====================================================
# ML + DB LOGIC
# =====================================================
def predict_ml(text):
    X = vectorizer.transform([text])
    prob = model.predict_proba(X)[0][1]
    return prob

def final_predict(text):
    if check_url(text):
        return "PHISHING (DB MATCH)", 1.0

    prob = predict_ml(text)

    if prob > 0.5:
        return "PHISHING (ML)", prob
    else:
        return "SAFE", prob

# =====================================================
# EXPLAINABILITY
# =====================================================
suspicious_words = ["urgent","verify","password","login","bank","click","update","security"]

def explain(text):
    text = text.lower()
    return [w for w in suspicious_words if w in text]

# =====================================================
# SOC DASHBOARD
# =====================================================
if mode == "📊 SOC Dashboard":

    st.subheader("🔍 Threat Analyzer")
    input_text = st.text_area("Paste URL or Email")

    if st.button("Scan Threat"):

        label, prob = final_predict(input_text)
        reasons = explain(input_text)

        st.markdown("### 🧠 Result")

        if "PHISHING" in label:
            st.error(f"🔴 {label}")
        else:
            st.success("🟢 SAFE")

        st.write("Confidence:", round(prob * 100, 2), "%")

        if reasons:
            st.warning("⚠ Suspicious keywords: " + ", ".join(reasons))

    # =================================================
    # GMAIL SCANNER
    # =================================================
   # =================================================
# GMAIL SCANNER
# =================================================
st.subheader("📧 Gmail Inbox Scanner")

if st.button("Scan Gmail Inbox"):

    service = get_service()
    emails = fetch_emails(service)

    st.success(f"Emails fetched: {len(emails)}")
    st.subheader("📧 SOC Email Threat Panel")

    for e in emails[:5]:

        msg = service.users().messages().get(
            userId="me",
            id=e["id"]
        ).execute()

        snippet = msg.get("snippet", "")

        # 🧠 Prediction
        label, prob = final_predict(snippet)
        confidence = round(prob * 100, 2)

        # 🧠 Explainability
        reasons = explain(snippet)

        # 🔴 / 🟢 Color based on threat
        if "PHISHING" in label:
            border = "#ef4444"
            status = "🔴 HIGH RISK"
        else:
            border = "#10b981"
            status = "🟢 SAFE"

        # 🟦 SOC CARD
        st.markdown(f"""
        <div style="
            background: rgba(15,23,42,0.8);
            border-left: 5px solid {border};
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 0 10px {border};
        ">
            <b>{status}</b><br><br>
            📩 <b>Email Preview:</b><br>
            {snippet}<br><br>
            📊 <b>Confidence:</b> {confidence}%<br>
        </div>
        """, unsafe_allow_html=True)

        # 🧠 Indicators
        if reasons:
            st.warning("⚠ Indicators: " + ", ".join(reasons))

# =====================================================
# TERMINAL MODE
# =====================================================
elif mode == "💻 Hacker Terminal":

    st.subheader("💻 SOC Terminal Scanner")

    text = st.text_area("Enter Payload")

    if st.button("Run Scan"):

        terminal = st.empty()

        logs = [
            "[+] Initializing SOC engine...",
            "[+] Extracting features...",
            "[+] Running ML model...",
            "[+] Checking threat DB...",
        ]

        for log in logs:
            terminal.markdown(f"<div class='terminal'>{log}</div>", unsafe_allow_html=True)
            time.sleep(0.5)

        label, prob = final_predict(text)

        terminal.markdown(f"""
        <div class='terminal'>
        [+] RESULT: {label}<br>
        [+] CONFIDENCE: {round(prob*100,2)}%<br>
        [+] SESSION CLOSED
        </div>
        """, unsafe_allow_html=True)