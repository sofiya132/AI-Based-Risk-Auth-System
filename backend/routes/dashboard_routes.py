from flask import Blueprint, request, jsonify
from utils.jwt_utils import verify_token
from models.user_model import find_user_by_email
from db import login_logs_collection

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api")


def require_auth(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing"}), 401
        token = auth_header.split(" ")[1]
        payload = verify_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        request.current_user = payload["email"]
        return f(*args, **kwargs)
    return decorated


@dashboard_bp.route("/dashboard", methods=["GET"])
@require_auth
def dashboard():
    email = request.current_user

    user = find_user_by_email(email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Safe datetime conversion
    try:
        created_at = user["created_at"].isoformat()
    except Exception:
        created_at = str(user.get("created_at", ""))

    # Fetch recent login logs
    try:
        recent_logs = list(
            login_logs_collection.find(
                {"email": email},
                {"_id": 0}
            ).sort("timestamp", -1).limit(5)
        )

        # Safe conversion of each log
        safe_logs = []
        for log in recent_logs:
            safe_log = {
                "ip": log.get("ip", "unknown"),
                "risk_score": log.get("risk_score", 0),
                "action": log.get("action", ""),
                "otp_triggered": log.get("otp_triggered", False),
            }
            # Safe timestamp conversion
            try:
                safe_log["timestamp"] = log["timestamp"].isoformat()
            except Exception:
                safe_log["timestamp"] = str(log.get("timestamp", ""))
            safe_logs.append(safe_log)

    except Exception as e:
        print(f"Log fetch error: {e}")
        safe_logs = []

    return jsonify({
        "message": "Welcome to your dashboard",
        "user": {
            "email": user["email"],
            "is_locked": user.get("is_locked", False),
            "created_at": created_at
        },
        "recent_logins": safe_logs
    }), 200