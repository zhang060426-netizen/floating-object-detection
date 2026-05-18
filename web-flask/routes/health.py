from flask import Blueprint

from db.init_db import get_db
from utils.response import success_response

bp = Blueprint("health", __name__)


@bp.route("/health", methods=["GET"])
def health():
    return success_response({"status": "ok", "service": "web-flask"})


@bp.route("/health/db", methods=["GET"])
def health_db():
    get_db().execute("SELECT 1").fetchone()
    return success_response({"status": "ok", "database": "sqlite"})
