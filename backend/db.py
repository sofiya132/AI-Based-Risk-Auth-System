# db.py — Creates and returns the MongoDB database connection

from pymongo import MongoClient
from config import Config

# Create a single MongoClient instance (reused across the app)
client = MongoClient(Config.MONGO_URI)

# Connect to the 'riskauth' database
db = client.get_database("riskauth")

# Define collection references (like SQL tables)
users_collection = db["users"]         # Stores registered users
login_logs_collection = db["login_logs"]  # Stores login attempt history
otp_collection = db["otp_store"]       # Stores active OTPs