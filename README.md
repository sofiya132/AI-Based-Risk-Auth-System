# AI-Based Risk Factor Authentication System 🛡️

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)

An adaptive authentication system that intelligently evaluates every login attempt using a trained **Random Forest** Machine Learning model.

## 📝 Problem Statement
Conventional login systems rely solely on passwords, making them highly vulnerable to brute force attacks and account takeovers. This project implements a system that assesses the risk level of each login attempt dynamically before granting access.

## ⚙️ How it Works
1. **Credentials:** Flask verifies the password against a **bcrypt-hashed** version in **MongoDB Atlas**.
2. **Features:** The risk engine extracts the IP address, device fingerprint, and login time.
3. **Prediction:** The **Random Forest Classifier** predicts a risk score: 0 (Safe) or 1 (Risky).
4. **Action:** Safe logins issue a **JWT token**; risky logins trigger a 6-digit **Flask-Mail OTP**.

## 🛠️ Tech Stack
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API).
- **Backend:** Flask (Python) REST API.
- **Database:** MongoDB Atlas (Cloud).
- **ML:** scikit-learn, pandas, numpy.
- **Security:** bcrypt, PyJWT, Flask-Limiter, Flask-CORS.

## 🛡️ Ethical Hacking & Defense
- **Brute Force:** Blocked via **Flask-Limiter** rate limiting.
- **Account Lockout:** Triggers after **5 consecutive failed attempts**.
- **Anomaly Detection:** The AI model serves as the primary defense by detecting unusual patterns.

## 👥 Team Contributions
- **[Sowmya N Kumar](https://github.com/Sowmya11082006)**: Register Module (Full Stack), bcrypt hashing, and MongoDB storage. 
- **[Sofiya Sindgi](https://github.com/sofiya132)**: Login Module (Full Stack), JWT generation, and ML model training. 
- **[Zaid Nisar Banday](https://github.com/)**: Risk + OTP Module (Full Stack), Flask-Mail, and model integration.
