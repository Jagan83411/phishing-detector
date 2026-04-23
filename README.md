# 🛡️ BlueSec AI SOC Dashboard

### AI-Powered Phishing Detection System (URL + Email + SOC Monitoring)

---

## 🚀 Overview

**BlueSec SOC** is an intelligent cybersecurity system designed to detect phishing attacks in real-time using a **hybrid approach (Machine Learning + Rule-Based Detection)**.

It analyzes:

* 🌐 URLs
* 📧 Emails (via Gmail API)
* 🧠 Behavioral patterns

and presents results through a **SOC-style dashboard interface**.

---

## 🎯 Key Features

### 🔍 1. URL Phishing Detection

* Detects malicious URLs using ML model
* Feature-based analysis (length, symbols, patterns)
* Real-time prediction with confidence score

---

### 📧 2. Gmail Phishing Scanner

* Secure Gmail API integration
* Scans inbox messages
* Detects phishing emails automatically

---

### 🧠 3. Hybrid Detection Engine

* Machine Learning (Random Forest)
* Rule-based intelligence (keywords, brand misuse)
* Improves accuracy and reduces false positives

---

### 📊 4. SOC Dashboard UI

* Cybersecurity-themed interface
* Real-time threat analysis
* Visual feedback (Safe / Phishing)

---

### 💻 5. Hacker Terminal Mode

* Simulated SOC terminal
* Step-by-step scan execution
* Live logs + results

---

## 🧠 How It Works

```
Input (URL / Email)
        ↓
Feature Extraction
        ↓
Rule-Based Check
        ↓
ML Model Prediction
        ↓
Final Decision (SAFE / PHISHING)
        ↓
SOC Dashboard Output
```

---

## ⚙️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **ML Model:** Scikit-learn (Random Forest)
* **Email Integration:** Gmail API
* **Data Processing:** Pandas, NumPy

---

## 📂 Project Structure

```
phishing-detector/
│
├── app/
│   └── app.py
│
├── models/
│   └── train_model.py
│
├── gmail_scanner/
│   └── gmail_reader.py
│
├── threat_db/
│   └── db.py
│
├── data/
│   └── url_dataset.csv
│
├── backend/
│   └── main.py
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```
git clone https://github.com/Jagan83411/phishing-detector.git
cd phishing-detector
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Run the Application

```
streamlit run app/app.py
```

---

## 🔐 Gmail Setup (Optional)

* Enable Gmail API in Google Cloud Console
* Download `credentials.json`
* Place it inside `/app` folder
* Authenticate on first run

---
## Architecture Diagram and Workflow image
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/d5cbfcb9-1185-486c-b8d1-2daf90669616" />
---
## 📸 Screenshots

<img width="917" height="536" alt="image" src="https://github.com/user-attachments/assets/d8c92a21-197f-4768-acd5-686c6b12e049" />

<img width="914" height="529" alt="image" src="https://github.com/user-attachments/assets/a26107a5-e938-4eb1-8d97-e3de240ca918" />

<img width="908" height="529" alt="image" src="https://github.com/user-attachments/assets/e91411e0-dc3d-4211-bdc2-510de89455a4" />



---

## 📊 Model Performance

* Accuracy: ~85–95% (depending on dataset quality)
* Hybrid detection improves real-world reliability
* Handles both URL-based and email-based attacks

---

## ⚠️ Limitations

* Depends on dataset quality
* Cannot detect zero-day phishing perfectly
* Gmail scanning limited to user-authorized accounts

---

## 🔮 Future Improvements

* 🌍 VirusTotal API integration
* 🧩 Chrome Extension for real-time browsing protection
* 👥 Multi-user authentication system
* 📈 Threat analytics dashboard
* 🤖 Deep learning-based detection

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork this repo and submit a PR.

---

## 📜 License

This project is for educational and research purposes.

---

## 👨‍💻 Author

**Jagan**
Cybersecurity & AI Enthusiast

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
