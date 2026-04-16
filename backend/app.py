import os
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from config import Config

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)

# 1. Robust CORS Configuration
# This handles the handshake between your Netlify frontend and Render backend
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://ai-based-risk-auth-system.netlify.app",
            "https://ai-based-risk-auth-system.netlify.app/", # added trailing slash
            "http://localhost:3000" # helpful for local testing
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize Limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Initialize Mail
mail = Mail(app)

# Import and Register Blueprints
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

# 2. Manual Header Fallback
# Sometimes browsers need this extra layer to confirm the CORS policy
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://ai-based-risk-auth-system.netlify.app'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

@app.route("/", methods=["GET"])
def health_check():
    return {"status": "AI Risk Auth API is running"}, 200

# Handle Preflight (OPTIONS) requests
@app.route("/api/<path:path>", methods=["OPTIONS"])
def handle_options(path):
    return "", 200

# 3. The Port Fix for Render
if __name__ == "__main__":
    # Render provides the port via environment variables
    port = int(os.environ.get("PORT", 5000))
    # '0.0.0.0' allows the app to be accessible externally
    app.run(host="0.0.0.0", port=port)