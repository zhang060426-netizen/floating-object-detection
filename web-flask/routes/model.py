from flask import Blueprint

from db.init_db import get_db
from services.model_service import list_published_models
from utils.jwt_utils import require_auth
from utils.response import success_response

bp = Blueprint("model", __name__)


@bp.route("/models/published", methods=["GET"])
@require_auth
def published_models():
    return success_response(list_published_models(get_db()))


@bp.route("/detection/models/published", methods=["GET"])
@require_auth
def detection_published_models_alias():
    return success_response(list_published_models(get_db()))
