import streamlit as st
import pickle
import os
import re
import random
import time
import sys

# =====================================================
# PATH SETUP
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))

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
model = pickle.load(open(os.path.join(BASE_DIR, "..", "model.pkl"), "rb"))

# =====================================================
# FEATURE ENGINEERING (MATCH DATASET)
# =====================================================
def extract_features(url):
    url = str(url)

    features = []
    features.append(len(url))
    features.append(url.count("."))
    features.append(url.count("-"))
    features.append(url.count("/"))
    features.append(int("https" in url))
    features.append(int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url))))
    features.append(int("@" in url))
    features.append(int("//" in url[7:]))

    domain = url.split("//")[-1].split("/")[0]
    features.append(len(domain))
    features.append(url.count(".") - 1)

    # ✅ ONLY THIS (NO brands feature)
    suspicious_words = ["login", "verify", "secure", "update", "account", "bank"]
    features.append(int(any(w in url.lower() for w in suspicious_words)))

    return features

# =====================================================
# RULE-BASED BOOST
# =====================================================
def rule_check(text):
    text = text.lower()

    if any(w in text for w in ["login", "verify", "update", "password"]):
        if any(b in text for b in ["amazon", "paypal", "google", "bank"]):
            return True

    return False

# =====================================================
# FINAL PREDICTION
# =====================================================
def final_predict(text):

    if rule_check(text):
        return "PHISHING (RULE)", 0.95

    features = extract_features(text)
    prob = model.predict_proba([features])[0][1]

    if prob > 0.5:
        return "PHISHING (ML)", prob
    else:
        return "SAFE", prob

# =====================================================
# EXPLAINABILITY
# =====================================================
def explain(text):
    words = ["urgent","verify","password","login","bank","click","update","security"]
    return [w for w in words if w in text.lower()]

# =====================================================
# UI STYLE
# =====================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(-45deg, #05070f, #0b1220, #0a0f1c, #020617);
    color: #e5e7eb;
    font-family: monospace;
}
.title {
    text-align: center;
    font-size: 34px;
    color: #3b82f6;
    text-shadow: 0 0 10px #3b82f6;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🛡️ BlueSec AI SOC Dashboard</div>", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================
mode = st.sidebar.radio("Mode", ["📊 Dashboard", "💻 Terminal"])

# =====================================================
# DASHBOARD
# =====================================================
if mode == "📊 Dashboard":

    st.subheader("🔍 Threat Analyzer")
    input_text = st.text_area("Paste URL or Email")

    if st.button("Scan"):

        label, prob = final_predict(input_text)
        reasons = explain(input_text)

        if "PHISHING" in label:
            st.error(f"🔴 {label}")
        else:
            st.success("🟢 SAFE")

        st.metric("Confidence", f"{round(prob*100,2)}%")

        if reasons:
            st.warning("⚠ Indicators: " + ", ".join(reasons))

    # ===============================
    # GMAIL SCANNER
    # ===============================
    st.subheader("📧 Gmail Scanner")

    if "user_email" not in st.session_state:
        st.session_state.user_email = None

    if st.button("Login Gmail"):
        service, user_email = get_service()
        st.session_state.user_email = user_email
        st.success(f"Logged in: {user_email}")

    if st.session_state.user_email:

        service, _ = get_service(st.session_state.user_email)

        if st.button("Scan Inbox"):

            emails = fetch_emails(service)

            for e in emails[:5]:

                msg = service.users().messages().get(
                    userId="me", id=e["id"]
                ).execute()

                snippet = msg.get("snippet", "")

                label, prob = final_predict(snippet)

                if "PHISHING" in label:
                    st.error(f"🔴 {label} ({round(prob*100,2)}%)")
                else:
                    st.success(f"🟢 SAFE ({round(prob*100,2)}%)")

                st.write(snippet)
                st.markdown("---")

# =====================================================
# TERMINAL MODE
# =====================================================
else:

    st.subheader("💻 SOC Terminal")

    text = st.text_area("Enter payload")

    if st.button("Run"):

        terminal = st.empty()

        steps = [
            "Initializing...",
            "Extracting features...",
            "Running model...",
            "Checking rules..."
        ]

        for s in steps:
            terminal.write(f"[+] {s}")
            time.sleep(0.5)

        label, prob = final_predict(text)

        terminal.write(f"[+] RESULT: {label}")
        terminal.write(f"[+] CONFIDENCE: {round(prob*100,2)}%")