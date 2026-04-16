# risk_engine.py — Extract login features and predict risk score using ML

import pickle
import os
import math
from datetime import datetime

# ── Load the trained model once at module import ──────────────────────────
# This runs when Flask first imports risk_engine — not on every request
model_path = os.path.join(os.path.dirname(__file__), "rf_model.pkl")

try:
    with open(model_path, "rb") as f:   # "rb" = read binary
        rf_model = pickle.load(f)
    print("Risk Engine: Random Forest model loaded successfully.")
except FileNotFoundError:
    rf_model = None
    print("WARNING: rf_model.pkl not found. Run train_model.py first!")

# ──────────────────────────────────────────────────────────────────────────

def extract_features(login_data, user_profile):
    """
    Convert raw login event data into the 6 numeric features
    that the Random Forest model expects.

    Parameters:
    - login_data: dict with current login attempt info
    - user_profile: dict from MongoDB (user's usual login patterns)

    Returns: list of 6 features
    """

    # Feature 1: IP Match
    # 1 if current IP matches the user's usual IP, else 0
    ip_match = 1 if login_data["ip"] == user_profile.get("usual_ip") else 0

    # Feature 2: Device Fingerprint Match
    # 1 if device matches the stored fingerprint, else 0
    device_match = 1 if login_data["device"] == user_profile.get("usual_device") else 0

    # Feature 3: Login Hour Deviation
    # How many hours away from the user's usual login window?
    current_hour = datetime.utcnow().hour
    usual_start = user_profile.get("usual_hour_start", 8)   # default 8am
    usual_end = user_profile.get("usual_hour_end", 22)      # default 10pm

    if usual_start <= current_hour <= usual_end:
        hour_deviation = 0   # Within normal window
    else:
        # Calculate minimum distance to the usual window
        dist_to_start = abs(current_hour - usual_start)
        dist_to_end = abs(current_hour - usual_end)
        hour_deviation = min(dist_to_start, dist_to_end)

    # Feature 4: Failed Attempts
    # Number of consecutive failed logins before this attempt
    failed_attempts = user_profile.get("failed_attempts", 0)

    # Feature 5: Geo Distance Risk
    # 1 if login is from a different country/region based on IP prefix
    # In production: use a geo-IP API. Here we use IP prefix as a proxy.
    usual_ip = user_profile.get("usual_ip", "")
    current_ip = login_data["ip"]
    # Compare first two octets (e.g., "192.168" from "192.168.1.1")
    usual_prefix = ".".join(usual_ip.split(".")[:2]) if usual_ip else ""
    current_prefix = ".".join(current_ip.split(".")[:2]) if current_ip else ""
    geo_risk = 0 if usual_prefix == current_prefix else 1

    # Feature 6: Browser Change Risk
    # 1 if the User-Agent string is different from usual device
    # device_match already covers this, but we add it as a separate signal
    browser_change = 0 if device_match == 1 else 1

    return [ip_match, device_match, hour_deviation, failed_attempts, geo_risk, browser_change]


def predict_risk(login_data, user_profile):
    """
    Use the trained Random Forest to predict if a login is risky.

    Returns:
    - risk_score: 0 (safe) or 1 (risky)
    - features: the 6 features used for prediction
    """
    if rf_model is None:
        # Fallback: rule-based risk check if model not trained yet
        print("Using fallback rule-based risk check")
        features = extract_features(login_data, user_profile)
        # Simple rule: if IP doesn't match AND device doesn't match → risky
        risk_score = 1 if (features[0] == 0 and features[1] == 0) else 0
        return risk_score, features

    # Extract the 6 features
    features = extract_features(login_data, user_profile)

    # reshape to [[f1, f2, f3, f4, f5, f6]] — sklearn expects 2D array
    prediction = rf_model.predict([features])

    # prediction is an array like [0] or [1] — take first element
    risk_score = int(prediction[0])

    return risk_score, features