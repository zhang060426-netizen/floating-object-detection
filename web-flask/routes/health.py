from flask import Blueprint

from utils.response import success_response

bp = Blueprint("health", __name__)


@bp.route("/health", methods=["GET"])
def health():
    return success_response({"status": "ok", "service": "web-flask"})
