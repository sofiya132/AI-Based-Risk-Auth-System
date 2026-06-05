# risk_engine.py — Extract login features and predict risk score using ML

import pickle
import os
import pandas as pd
from datetime import datetime, timezone

# Load model once at startup
model_path = os.path.join(os.path.dirname(__file__), "rf_model.pkl")

try:
    with open(model_path, "rb") as f:
        rf_model = pickle.load(f)
    print("Risk Engine: Random Forest model loaded successfully.")
except FileNotFoundError:
    rf_model = None
    print("WARNING: rf_model.pkl not found. Run train_model.py first!")


def extract_features(login_data, user_profile):
    """Extract 6 risk features from login attempt."""

    # Feature 1: IP Match
    ip_match = 1 if login_data["ip"] == user_profile.get("usual_ip") else 0

    # Feature 2: Device Fingerprint Match
    device_match = 1 if login_data["device"] == user_profile.get("usual_device") else 0

    # Feature 3: Login Hour Deviation
    current_hour = datetime.now(timezone.utc).hour
    usual_start = user_profile.get("usual_hour_start", 0)
    usual_end   = user_profile.get("usual_hour_end", 23)

    if usual_start <= current_hour <= usual_end:
        hour_deviation = 0
    else:
        hour_deviation = min(
            abs(current_hour - usual_start),
            abs(current_hour - usual_end)
        )

    # Feature 4: Failed Attempts
    failed_attempts = user_profile.get("failed_attempts", 0)

    # Feature 5: Geo Risk (compare first 2 octets of IP)
    usual_ip   = user_profile.get("usual_ip", "")
    current_ip = login_data["ip"]
    usual_prefix   = ".".join(usual_ip.split(".")[:2])   if usual_ip   else ""
    current_prefix = ".".join(current_ip.split(".")[:2]) if current_ip else ""
    geo_risk = 0 if usual_prefix == current_prefix else 1

    # Feature 6: Browser Change
    browser_change = 0 if device_match == 1 else 1

    return [ip_match, device_match, hour_deviation,
            failed_attempts, geo_risk, browser_change]


def predict_risk(login_data, user_profile):
    """
    Predict if login is risky using rule-based checks + ML model.
    Returns: risk_score (0=safe, 1=risky), features list
    """
    features = extract_features(login_data, user_profile)

    ip_match      = features[0]
    device_match  = features[1]
    failed_att    = features[3]

    # ── Rule-based checks (always applied first) ──────────────────────────

    # New device detected → always risky
    if device_match == 0:
        print(f"Risk Engine: RISKY — Unknown device | features={features}")
        return 1, features

    # Different IP AND different geo → risky
    if ip_match == 0 and features[4] == 1:
        print(f"Risk Engine: RISKY — Different IP+Geo | features={features}")
        return 1, features

    # Too many failed attempts → risky
    if failed_att >= 3:
        print(f"Risk Engine: RISKY — Failed attempts={failed_att}")
        return 1, features

    # ── ML Model for borderline cases ─────────────────────────────────────
    if rf_model is not None:
        try:
            feature_names = [
                "ip_match", "device_match", "hour_deviation",
                "failed_attempts", "geo_risk", "browser_change"
            ]
            df = pd.DataFrame([features], columns=feature_names)
            prediction  = rf_model.predict(df)
            risk_score  = int(prediction[0])
            print(f"Risk Engine: ML={risk_score} | features={features}")
            return risk_score, features
        except Exception as e:
            print(f"Risk Engine ML error: {e}")

    # ── Fallback rule ──────────────────────────────────────────────────────
    risk_score = 0 if (ip_match == 1 and device_match == 1) else 1
    return risk_score, features