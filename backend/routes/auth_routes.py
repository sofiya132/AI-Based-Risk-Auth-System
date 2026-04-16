# auth_routes.py — /register, /login, /verify-otp endpoints

from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from db import login_logs_collection
from models.user_model import (
    create_user, find_user_by_email,
    verify_password, increment_failed_attempts, reset_failed_attempts
)
from utils.jwt_utils import create_token
from utils.otp_utils import generate_otp, save_otp, verify_otp
from ml.risk_engine import predict_risk

auth_bp = Blueprint("auth", __name__, url_prefix="/api")


# ─── REGISTER ────────────────────────────────────────────────────────────────

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    email = data["email"].lower().strip()
    password = data["password"]
    device_fingerprint = data.get("device_fingerprint", "unknown")

    if find_user_by_email(email):
        return jsonify({"error": "Email already registered"}), 409

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_id = create_user(email, password, ip, device_fingerprint)

    return jsonify({
        "message": "Registration successful",
        "user_id": user_id
    }), 201


# ─── LOGIN ───────────────────────────────────────────────────────────────────

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    email = data["email"].lower().strip()
    password = data["password"]
    device_fingerprint = data.get("device_fingerprint", "unknown")  # ← this line MUST be here
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    # Step 1: Find user
    user = find_user_by_email(email)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # Step 2: Check account lock
    if user.get("is_locked"):
        return jsonify({"error": "Account locked due to too many failed attempts."}), 403

    # Step 3: Verify password
    if not verify_password(password, user["password"]):
        increment_failed_attempts(email)
        remaining = max(0, 5 - user["failed_attempts"] - 1)
        return jsonify({"error": f"Invalid credentials. {remaining} attempts remaining."}), 401

    # Step 4: Reset failed attempts on success
    reset_failed_attempts(email)

    # Step 5: Build login data for risk engine
    login_data = {
        "ip": ip,
        "device": device_fingerprint,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    # Step 6: Run ML risk prediction
    risk_score, features = predict_risk(login_data, user)

    # Step 7: Log the attempt
    log_entry = {
        "email": email,
        "ip": ip,
        "device": device_fingerprint,
        "risk_score": risk_score,
        "features": features,
        "timestamp": datetime.now(timezone.utc),
        "otp_triggered": False
    }

    # Step 8: Safe or risky?
    if risk_score == 0:
        token = create_token(email)
        log_entry["action"] = "token_issued"
        login_logs_collection.insert_one(log_entry)
        return jsonify({
            "message": "Login successful",
            "token": token,
            "risk_score": risk_score
        }), 200

    else:
        otp = generate_otp()
        save_otp(email, otp)

        from app import mail
        from flask_mail import Message
        msg = Message(
            subject="Your Security Verification Code",
            recipients=[email],
            body=f"Your one-time code is: {otp}\n\nExpires in 5 minutes."
        )
        mail.send(msg)

        log_entry["otp_triggered"] = True
        log_entry["action"] = "otp_sent"
        login_logs_collection.insert_one(log_entry)

        return jsonify({
            "message": "Risky login detected. OTP sent to your email.",
            "risk_score": risk_score,
            "require_otp": True
        }), 200


# ─── VERIFY OTP ──────────────────────────────────────────────────────────────

@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp_route():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("otp"):
        return jsonify({"error": "Email and OTP are required"}), 400

    email = data["email"].lower().strip()
    entered_otp = data["otp"].strip()

    if verify_otp(email, entered_otp):
        token = create_token(email)
        return jsonify({
            "message": "OTP verified successfully",
            "token": token
        }), 200
    else:
        return jsonify({"error": "Invalid or expired OTP"}), 401