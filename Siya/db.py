from pymongo import MongoClient
from datetime import datetime
import os

# ---------------- MongoDB Connection ---------------- #
MONGO_URL = os.getenv("MONGO_URL")  # MongoDB URI
client = MongoClient(MONGO_URL)
db = client["siya_chat_bot"]

# Collections
users_col = db["users"]       # Private users
groups_col = db["groups"]     # Group chats

# ---------------- User Functions ---------------- #
def add_private_user(user_id: int, username: str):
    """Add or update a private user"""
    users_col.update_one(
        {"user_id": user_id},
        {"$set": {"username": username, "joined_at": datetime.utcnow()}},
        upsert=True
    )

def is_private_user(user_id: int) -> bool:
    """Check if user exists"""
    return users_col.count_documents({"user_id": user_id}) > 0

# ---------------- Group Functions ---------------- #
def add_group_chat(chat_id: int, title: str):
    """Add or update a group chat"""
    groups_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"title": title, "joined_at": datetime.utcnow()}},
        upsert=True
    )

def is_group_chat(chat_id: int) -> bool:
    """Check if group exists"""
    return groups_col.count_documents({"chat_id": chat_id}) > 0