import datetime as dt
from functools import wraps

import jwt
from flask import current_app, g, request

from db.init_db import get_db
from utils.response import error_response


def create_token(user):
    now = dt.datetime.utcnow()
    payload = {
        "user_id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "status": user["status"],
        "iat": int(now.timestamp()),
        "exp": int((now + dt.timedelta(seconds=current_app.config["JWT_EXPIRE_SECONDS"])).timestamp()),
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")


def decode_token(token):
    return jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return error_response("missing bearer token", code=401, http_status=401)
        token = auth.split(" ", 1)[1].strip()
        try:
            payload = decode_token(token)
        except Exception:
            return error_response("invalid or expired token", code=401, http_status=401)
        db = get_db()
        user = db.execute("SELECT id, username, role, status FROM user WHERE id = ?", (payload.get("user_id"),)).fetchone()
        if not user or int(user["status"]) != 1:
            return error_response("user disabled or not found", code=401, http_status=401)
        g.current_user = user
        return fn(*args, **kwargs)
    return wrapper
