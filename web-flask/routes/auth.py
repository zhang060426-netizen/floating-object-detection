from flask import Blueprint, g, request

from db.init_db import get_db
from services.auth_service import authenticate, login_payload
from utils.jwt_utils import require_auth
from utils.response import error_response, success_response

bp = Blueprint("auth", __name__)


@bp.route("/auth/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True) or {}
    username = payload.get("username")
    password = payload.get("password")
    if not username or not password:
        return error_response("username and password are required", code=400)
    user = authenticate(get_db(), username, password)
    if not user:
        return error_response("invalid username or password", code=401, http_status=401)
    return success_response(login_payload(user))


@bp.route("/auth/me", methods=["GET"])
@require_auth
def me():
    user = g.current_user
    return success_response({"id": user["id"], "username": user["username"], "role": "admin" if int(user["role"]) == 1 else "user"})
