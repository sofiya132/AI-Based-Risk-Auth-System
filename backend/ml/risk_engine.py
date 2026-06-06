import pickle
import os
import pandas as pd
from datetime import datetime, timezone, timedelta

model_path = os.path.join(os.path.dirname(__file__), "rf_model.pkl")

try:
    with open(model_path, "rb") as f:
        rf_model = pickle.load(f)
    print("Risk Engine: Random Forest model loaded successfully.")
except FileNotFoundError:
    rf_model = None
    print("WARNING: rf_model.pkl not found. Run train_model.py first!")


def get_ist_hour():
    """Get current hour in IST (UTC+5:30)."""
    ist_time = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    return ist_time.hour


def extract_features(login_data, user_profile):

    # Feature 1: IP Match
    ip_match = 1 if login_data["ip"] == user_profile.get("usual_ip") else 0

    # Feature 2: Device Match
    device_match = 1 if login_data["device"] == user_profile.get("usual_device") else 0

    # Feature 3: Hour Deviation (using IST)
    current_hour = get_ist_hour()
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

    # Feature 5: Geo Risk
    usual_ip   = user_profile.get("usual_ip", "")
    current_ip = login_data["ip"]
    usual_prefix   = ".".join(usual_ip.split(".")[:2]) if usual_ip   else ""
    current_prefix = ".".join(current_ip.split(".")[:2]) if current_ip else ""
    geo_risk = 0 if usual_prefix == current_prefix else 1

    # Feature 6: Browser Change
    browser_change = 0 if device_match == 1 else 1

    return [ip_match, device_match, hour_deviation,
            failed_attempts, geo_risk, browser_change]


def predict_risk(login_data, user_profile):
    features = extract_features(login_data, user_profile)

    ip_match     = features[0]
    device_match = features[1]
    failed_att   = features[3]

    print(f"Risk Engine: features={features} | ip={login_data['ip']} | usual_ip={user_profile.get('usual_ip')}")

    # Rule 1: Too many failed attempts → always risky
    if failed_att >= 3:
        print(f"Risk Engine: RISKY — Failed attempts={failed_att}")
        return 1, features

    # Rule 2: Different device AND different geo → risky
    # (not just different device alone — IP changes on cloud servers)
    if device_match == 0 and features[4] == 1:
        print(f"Risk Engine: RISKY — Unknown device + geo | features={features}")
        return 1, features

    # Rule 3: Same device but completely different IP prefix → risky
    if device_match == 1 and ip_match == 0 and features[4] == 1:
        print(f"Risk Engine: RISKY — Same device different geo | features={features}")
        return 1, features

    # ML model for all other cases
    if rf_model is not None:
        try:
            feature_names = [
                "ip_match", "device_match", "hour_deviation",
                "failed_attempts", "geo_risk", "browser_change"
            ]
            df = pd.DataFrame([features], columns=feature_names)
            prediction = rf_model.predict(df)
            risk_score = int(prediction[0])
            print(f"Risk Engine: ML={risk_score} | features={features}")
            return risk_score, features
        except Exception as e:
            print(f"Risk Engine ML error: {e}")

    # Fallback — only risky if device AND geo both different
    risk_score = 1 if (device_match == 0 and features[4] == 1) else 0
    return risk_score, features