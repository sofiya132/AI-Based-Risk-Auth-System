# otp_utils.py — OTP generation, storage, and verification

import random
import string
from datetime import datetime, timezone, timedelta
from db import otp_collection
from config import Config

def generate_otp():
    """Generate a random 6-digit numeric OTP."""
    return "".join(random.choices(string.digits, k=6))


def save_otp(email, otp):
    """Save OTP to MongoDB with expiry time."""
    expiry_time = datetime.now(timezone.utc) + timedelta(seconds=Config.OTP_EXPIRY_SECONDS)
    otp_collection.update_one(
        {"email": email},
        {"$set": {
            "otp": otp,
            "expires_at": expiry_time,
            "used": False
        }},
        upsert=True
    )


def verify_otp(email, entered_otp):
    """Verify the OTP entered by the user."""
    record = otp_collection.find_one({"email": email})

    if not record:
        return False

    if record.get("used"):
        return False

    # Fix: handle both timezone-aware and naive datetimes from MongoDB
    expires_at = record["expires_at"]
    if expires_at.tzinfo is None:
        # Old record saved without timezone — make it UTC aware
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if datetime.now(timezone.utc) > expires_at:
        return False

    if record["otp"] != entered_otp:
        return False

    otp_collection.update_one({"email": email}, {"$set": {"used": True}})
    return True