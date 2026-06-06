import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/riskauth")
    
    # JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_change_this")
    JWT_EXPIRY_SECONDS = 3600
    
    # OTP
    OTP_EXPIRY_SECONDS = 300

    # Flask-Mail (kept for local testing)
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_TIMEOUT = 10

    # Brevo API Key (used on Render)
    BREVO_API_KEY = os.getenv("BREVO_API_KEY")

    # Rate limiting
    RATELIMIT_DEFAULT = "10 per minute"
    
    # Account lockout
    MAX_FAILED_ATTEMPTS = 5