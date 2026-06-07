# AI-Based Risk Factor Authentication System 🛡️

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)

An adaptive authentication system that intelligently evaluates every login attempt using a trained **Random Forest** Machine Learning model. Safe logins get direct access via JWT. Suspicious logins trigger OTP verification via email.

---

## 📝 Problem Statement

Conventional login systems rely solely on passwords, making them vulnerable to brute force attacks, credential stuffing, and account takeovers. Once a password is compromised, an attacker gains unrestricted access. This project implements an intelligent system that assesses the risk level of each login attempt dynamically before granting access.

---

## ⚙️ How It Works

1. **Credentials** — Flask verifies the password against a bcrypt-hashed version in MongoDB Atlas.
2. **Feature Extraction** — The risk engine extracts 6 contextual features from the login attempt.
3. **ML Prediction** — The Random Forest Classifier predicts a risk score: `0` = Safe, `1` = Risky.
4. **Adaptive Response** — Safe logins issue a JWT token directly. Risky logins trigger a 6-digit OTP sent via email.

---

## 🔍 6 Risk Factors

| # | Feature | Description |
|---|---|---|
| 1 | IP Match | Is the login IP same as registered IP? |
| 2 | Device Fingerprint | Is it the same browser and device? |
| 3 | Hour Deviation | Is the login time within usual hours? |
| 4 | Failed Attempts | How many wrong passwords before this? |
| 5 | Geo Risk | Is the IP from the same region? |
| 6 | Browser Change | Is it the same browser as usual? |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript (Fetch API) |
| Backend | Flask (Python) REST API |
| Database | MongoDB Atlas (Cloud) |
| ML | scikit-learn (Random Forest), pandas, numpy |
| Security | bcrypt, PyJWT, Flask-Limiter, Flask-CORS |
| Email (OTP) | Brevo Transactional Email API |
| Deployment | Render (Backend) + Netlify (Frontend) |
| Version Control | GitHub |

---

## 🛡️ Security Features

- **bcrypt** password hashing with salt — never stores plain text passwords
- **JWT** tokens with 1 hour expiry for stateless authentication
- **Flask-Limiter** rate limiting — max 10 requests per minute per IP
- **Account lockout** after 5 consecutive failed login attempts
- **OTP expiry** — 6-digit code expires in 5 minutes, single use only
- **CORS** protection via Flask-CORS
- **Environment variables** for all secrets via `.env`

---

## 🚀 Live Demo

- **Frontend:** https://ai-based-risk-auth-system.netlify.app
- **Backend API:** https://ai-based-risk-auth-system.onrender.com

---

## 💻 Local Setup

### Prerequisites
- Python 3.11
- Git
- MongoDB Atlas account (free)
- Brevo account (free) for OTP emails

### Step 1 — Clone the repository
```bash
git clone https://github.com/sofiya132/AI-Based-Risk-Auth-System.git
cd AI-Based-Risk-Auth-System
```

### Step 2 — Create virtual environment
```bash
cd backend
py -3.11 -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set up environment variables
```bash
# Copy the example file
copy .env.example .env
```

Edit `.env` with your actual values:
```env
MONGO_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/riskauth
SECRET_KEY=your_long_random_secret_key
MAIL_USERNAME=yourgmail@gmail.com
MAIL_PASSWORD=your_gmail_app_password
MAIL_DEFAULT_SENDER=yourgmail@gmail.com
BREVO_API_KEY=your_brevo_api_key
```

### Step 5 — Get MongoDB URI
1. Go to [mongodb.com/atlas](https://mongodb.com/atlas) → free account
2. Create cluster → Connect → Drivers → Copy URI
3. Replace `<password>` with your database user password
4. Paste in `.env` as `MONGO_URI`

### Step 6 — Get Brevo API Key
1. Go to [brevo.com](https://brevo.com) → free account
2. Settings → API Keys → Create API Key
3. Paste in `.env` as `BREVO_API_KEY`

### Step 7 — Train the ML model
```bash
# Generate synthetic training data
python ml/generate_csv.py

# Train Random Forest model
python ml/train_model.py
```

You should see:
```
login_data.csv created with 1200 rows
Model Accuracy: 100.00%
Model saved to .../rf_model.pkl
```

### Step 8 — Run the Flask server
```bash
python app.py
```

You should see:
```
MongoDB: Connected! ✅
Risk Engine: Random Forest model loaded successfully.
* Running on http://127.0.0.1:5000
```

### Step 9 — Open the frontend
Open `frontend/register.html` with Live Server in VS Code

Or update `API_BASE` in `frontend/script.js`:
```javascript
const API_BASE = "http://127.0.0.1:5000/api";
```

---

## 📁 Project Structure

```
AI-Based-Risk-Auth-System/
│
├── backend/
│   ├── app.py                  ← Main Flask app + CORS
│   ├── config.py               ← All configuration + env vars
│   ├── db.py                   ← MongoDB Atlas connection
│   ├── models/
│   │   └── user_model.py       ← User CRUD operations
│   ├── routes/
│   │   ├── auth_routes.py      ← /register /login /verify-otp
│   │   └── dashboard_routes.py ← /dashboard (JWT protected)
│   ├── ml/
│   │   ├── risk_engine.py      ← Feature extraction + ML prediction
│   │   ├── train_model.py      ← Random Forest training
│   │   ├── generate_csv.py     ← Synthetic dataset generation
│   │   └── login_data.csv      ← 1200 training records
│   ├── utils/
│   │   ├── jwt_utils.py        ← JWT create/verify
│   │   ├── otp_utils.py        ← OTP generate/save/verify
│   │   └── email_utils.py      ← Brevo email sender
│   ├── requirements.txt
│   ├── render.yaml
│   └── .env.example
│
└── frontend/
    ├── index.html              ← Register page
    ├── login.html              ← Login page
    ├── otp.html                ← OTP verification page
    ├── dashboard.html          ← Protected dashboard
    ├── styles.css              ← Shared styles
    └── script.js               ← Shared JS utilities
```

---

## 🔄 Authentication Flow

```
User submits email + password
        ↓
Flask verifies bcrypt password
        ↓
Extract 6 risk features
        ↓
Random Forest predicts risk score
        ↓
    ┌───┴───┐
  Safe(0)  Risky(1)
    ↓         ↓
Issue JWT   Send OTP email
    ↓         ↓
Dashboard  Verify OTP
           ↓
        Issue JWT
           ↓
        Dashboard
```

---

## 👥 Contributors

- [Sofiya Sindgi](https://github.com/sofiya132)
- [Sowmya N Kumar](https://github.com/Sowmya11082006)
- [Zaid Nisar Banday](https://github.com/zaidnisarbanday06)

---
