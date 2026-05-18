from flask import Blueprint, send_file

from services.file_storage_service import resolve_object_path
from utils.jwt_utils import require_auth
from utils.response import error_response

bp = Blueprint("file", __name__)


@bp.route("/files/<bucket>/<path:object_key>", methods=["GET"])
@require_auth
def get_file(bucket, object_key):
    try:
        path = resolve_object_path(bucket, object_key)
    except ValueError:
        return error_response("invalid file path", code=400, http_status=400)
    if not path.exists() or not path.is_file():
        return error_response("file not found", code=404, http_status=404)
    return send_file(path)


@bp.route("/file/<bucket>/<path:object_key>", methods=["GET"])
@require_auth
def get_file_alias(bucket, object_key):
    return get_file(bucket, object_key)
