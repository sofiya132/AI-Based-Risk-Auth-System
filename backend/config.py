import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/riskauth")
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_change_this")
    JWT_EXPIRY_SECONDS = 3600
    OTP_EXPIRY_SECONDS = 300

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_TIMEOUT = 10

    RATELIMIT_DEFAULT = "10 per minute"
    MAX_FAILED_ATTEMPTS = 5