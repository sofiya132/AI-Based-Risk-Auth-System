import os
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": "*"}})

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

mail = Mail(app)

from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

@app.route("/", methods=["GET"])
def health_check():
    return {"status": "AI Risk Auth API is running"}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)