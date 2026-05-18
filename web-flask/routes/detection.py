from flask import Blueprint, g, request

from ai.yolo_infer import InferenceUnavailable
from db.init_db import get_db
from services.detection_service import detect_image, get_record, list_records, save_record
from services.file_storage_service import file_info
from services.model_service import get_model
from utils.jwt_utils import require_auth
from utils.response import error_response, success_response

bp = Blueprint("detection", __name__)


def parse_bool(value, default=True):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).lower() not in {"0", "false", "no", "off"}


def parse_confidence(value, default=0.5):
    if value is None:
        return default
    try:
        confidence = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("confidence_threshold must be a number") from exc
    if confidence < 0 or confidence > 1:
        raise ValueError("confidence_threshold must be between 0 and 1")
    return confidence


@bp.route("/detection/image", methods=["POST"])
@require_auth
def image_detection():
    image = request.files.get("image")
    if image is None or not image.filename:
        return error_response("image file is required", code=400)
    model_id = request.form.get("model_id")
    if not model_id:
        return error_response("model_id is required", code=400)
    try:
        confidence = parse_confidence(request.form.get("confidence_threshold"), 0.5)
    except ValueError:
        return error_response("confidence_threshold must be between 0 and 1", code=400, data={"reason": "bad_request", "field": "confidence_threshold"})
    save_flag = parse_bool(request.form.get("save_record"), True)
    try:
        return success_response(detect_image(get_db(), g.current_user, image, model_id, confidence, save_flag))
    except InferenceUnavailable as exc:
        http_status = 400 if exc.reason in {"invalid_image", "unsupported_image_type"} else 500
        return error_response(
            str(exc),
            code=http_status,
            data={"reason": exc.reason, "model_id": model_id, **exc.details},
            http_status=http_status,
        )
    except ValueError as exc:
        return error_response(str(exc), code=400, data={"reason": "bad_request", "model_id": model_id}, http_status=400)


@bp.route("/detection/records", methods=["POST"])
@require_auth
def create_record():
    payload = request.get_json(silent=True) or {}
    model_id = payload.get("model_id")
    original = payload.get("original_image") or {}
    result = payload.get("result_image") or None
    detection_result = payload.get("detection_result") or {}
    try:
        confidence = parse_confidence(payload.get("confidence_threshold"), 0.5)
    except ValueError as exc:
        return error_response(str(exc), code=400, data={"reason": "bad_request", "field": "confidence_threshold"}, http_status=400)
    if not model_id or not get_model(get_db(), model_id):
        return error_response("model not found or unpublished", code=400)
    if not original.get("bucket") or not original.get("object_key"):
        return error_response("original_image bucket and object_key are required", code=400)
    record_id = save_record(
        get_db(),
        g.current_user["id"],
        model_id,
        original,
        result,
        detection_result,
        confidence,
        payload.get("title"),
        payload.get("description"),
    )
    return success_response({"record_id": record_id, "id": record_id})


@bp.route("/detection/records", methods=["GET"])
@require_auth
def records():
    try:
        page = max(1, int(request.args.get("page", 1)))
        page_size = min(100, max(1, int(request.args.get("page_size", 20))))
    except ValueError:
        return error_response("page and page_size must be integers", code=400)
    return success_response(list_records(get_db(), g.current_user, page, page_size))


@bp.route("/detection/records/<record_id>", methods=["GET"])
@require_auth
def record_detail(record_id):
    record = get_record(get_db(), g.current_user, record_id)
    if not record:
        return error_response("record not found", code=404, http_status=404)
    return success_response(record)
