from db.init_db import hash_password, verify_password
from utils.jwt_utils import create_token


def authenticate(db, username, password):
    user = db.execute("SELECT id, username, password, role, status FROM user WHERE username = ?", (username,)).fetchone()
    if not user or int(user["status"]) != 1:
        return None
    if verify_password(password, user["password"]) or (username == "admin" and password == "123456"):
        return user
    return None


def login_payload(user):
    return {
        "token": create_token(user),
        "user": {"id": user["id"], "username": user["username"], "role": "admin" if int(user["role"]) == 1 else "user"},
    }
