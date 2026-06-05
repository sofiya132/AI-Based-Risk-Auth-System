# dashboard_routes.py — Protected routes that require a valid JWT

from flask import Blueprint, request, jsonify
from utils.jwt_utils import verify_token
from models.user_model import find_user_by_email
from db import login_logs_collection

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api")


def require_auth(f):
    """
    Decorator function — wraps protected routes to verify JWT.
    Usage: @require_auth above any route function.
    """
    from functools import wraps

    @wraps(f)  # Preserves the original function's name and docstring
    def decorated(*args, **kwargs):
        # JWT is sent in the Authorization header as: "Bearer <token>"
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing or malformed"}), 401

        # Extract the token (remove "Bearer " prefix)
        token = auth_header.split(" ")[1]

        # Verify the token
        payload = verify_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401

        # Attach the decoded payload to the request context
        request.current_user = payload["email"]

        # Call the original route function
        return f(*args, **kwargs)

    return decorated


@dashboard_bp.route("/dashboard", methods=["GET"])
@require_auth  # This route requires a valid JWT
def dashboard():
    """
    Protected dashboard endpoint.
    Returns user info and recent login history.
    """
    email = request.current_user  # Set by the require_auth decorator

    # Fetch user from MongoDB
    user = find_user_by_email(email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Fetch last 5 login logs for this user
    recent_logs = list(
        login_logs_collection.find(
            {"email": email},
            {"_id": 0}  # Exclude MongoDB _id field from results
        ).sort("timestamp", -1).limit(5)  # Sort by newest first, limit 5
    )

    # Convert datetime objects to strings for JSON serialisation
    for log in recent_logs:
        if "timestamp" in log:
            log["timestamp"] = log["timestamp"].isoformat()

    return jsonify({
        "message": "Welcome to your dashboard",
        "user": {
            "email": user["email"],
            "is_locked": user.get("is_locked", False),
            "created_at": user["created_at"].isoformat()
        },
        "recent_logins": recent_logs
    }), 200