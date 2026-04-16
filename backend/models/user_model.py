# user_model.py — Functions for all user-related database operations

from db import users_collection
from config import Config
import bcrypt
from datetime import datetime, timezone

def create_user(email, password, ip, device_fingerprint):
    """Register a new user with hashed password and default login pattern."""
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12))
    current_hour = datetime.now(timezone.utc).hour

    user_doc = {
        "email": email,
        "password": hashed_password,
        "is_locked": False,
        "failed_attempts": 0,
        "created_at": datetime.now(timezone.utc),
        "usual_ip": ip,
        "usual_device": device_fingerprint,
        "usual_hour_start": current_hour - 2,
        "usual_hour_end": current_hour + 2,
    }

    result = users_collection.insert_one(user_doc)
    return str(result.inserted_id)


def find_user_by_email(email):
    """Fetch a user document from MongoDB by email address."""
    return users_collection.find_one({"email": email})


def increment_failed_attempts(email):
    """Increase failed login counter by 1. Lock account if limit reached."""
    user = find_user_by_email(email)
    if not user:
        return

    new_count = user["failed_attempts"] + 1
    update_data = {"failed_attempts": new_count}

    if new_count >= Config.MAX_FAILED_ATTEMPTS:
        update_data["is_locked"] = True

    users_collection.update_one({"email": email}, {"$set": update_data})


def reset_failed_attempts(email):
    """Reset failed attempt counter after a successful login."""
    users_collection.update_one(
        {"email": email},
        {"$set": {"failed_attempts": 0, "is_locked": False}}
    )


def verify_password(plain_password, hashed_password):
    """Check if entered password matches the stored hash."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)