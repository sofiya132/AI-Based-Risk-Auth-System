# config.py — Centralises all configuration settings for the Flask app

import os
from dotenv import load_dotenv

# Load all variables from the .env file into the environment
load_dotenv()

class Config:
    # MongoDB connection string (from Atlas)
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/riskauth")

    # Secret key for signing JWT tokens — must be kept private
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_change_this")

    # JWT token expiry: 1 hour (in seconds)
    JWT_EXPIRY_SECONDS = 3600

    # OTP expiry: 5 minutes (in seconds)
    OTP_EXPIRY_SECONDS = 300

    # Flask-Mail settings for Gmail SMTP
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    # Rate limiting: max 10 logins per minute per IP
    RATELIMIT_DEFAULT = "10 per minute"

    # Max failed login attempts before account lock
    MAX_FAILED_ATTEMPTS = 5