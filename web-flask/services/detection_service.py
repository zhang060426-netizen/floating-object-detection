import json
import time
import uuid

from ai.yolo_infer import InferenceUnavailable, build_detection_result, draw_result_image, image_metadata, run_yolo_image
from services.file_storage_service import copy_result_image, file_info, resolve_object_path, save_upload
from services.model_service import get_model


def _record_to_dict(row):
    original = file_info(row["original_image_bucket"], row["original_image_object_key"])
    result = None
    if row["result_image_bucket"] and row["result_image_object_key"]:
        result = file_info(row["result_image_bucket"], row["result_image_object_key"])
    try:
        detection_result = json.loads(row["detection_result"]) if row["detection_result"] else None
    except json.JSONDecodeError:
        detection_result = row["detection_result"]
    return {
        "id": row["id"],
        "record_id": row["id"],
        "user_id": row["user_id"],
        "model_id": row["model_id"],
        "original_image": original,
        "result_image": result,
        "detection_result": detection_result,
        "confidence_threshold": row["confidence_threshold"],
        "title": row["title"],
        "description": row["description"],
        "create_time": row["create_time"],
    }


def save_record(db, user_id, model_id, original_image, result_image, detection_result, confidence_threshold=0.5, title=None, description=None):
    record_id = "dr_" + uuid.uuid4().hex
    db.execute(
        """
        INSERT INTO detection_records(
          id, user_id, model_id, original_image_bucket, original_image_object_key,
          result_image_bucket, result_image_object_key, detection_result,
          confidence_threshold, title, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record_id,
            user_id,
            model_id,
            original_image["bucket"],
            original_image["object_key"],
            result_image.get("bucket") if result_image else None,
            result_image.get("object_key") if result_image else None,
            json.dumps(detection_result, ensure_ascii=False),
            confidence_threshold,
            title,
            description,
        ),
    )
    db.commit()
    return record_id


def _normalize_inference_result(result):
    detections, timing = result
    if isinstance(timing, dict):
        return detections, timing.copy()
    return detections, {"inference_ms": timing}


def _elapsed_ms(start):
    return (time.perf_counter() - start) * 1000


def _round_timing(timing):
    return {
        key: round(value, 3) if isinstance(value, (int, float)) and not isinstance(value, bool) else value
        for key, value in timing.items()
    }


def _update_record_detection_result(db, record_id, detection_result):
    db.execute(
        "UPDATE detection_records SET detection_result=? WHERE id=?",
        (json.dumps(detection_result, ensure_ascii=False), record_id),
    )
    db.commit()


def detect_image(db, user, image_file, model_id, confidence_threshold=0.5, save_record_flag=True):
    api_start = time.perf_counter()
    model = get_model(db, model_id)
    if not model:
        raise ValueError("model not found or unpublished")
    preprocess_start = time.perf_counter()
    try:
        upload_bucket, upload_key, upload_path = save_upload(image_file, "uploads", "images")
    except ValueError as exc:
        raise InferenceUnavailable(
            str(exc),
            reason="unsupported_image_type",
            details={"filename": image_file.filename or "upload"},
        ) from exc
    try:
        image_info = image_metadata(upload_path, image_file.filename or upload_path.name)
    except ValueError as exc:
        raise InferenceUnavailable(
            "invalid image file",
            reason="invalid_image",
            details={"filename": image_file.filename or upload_path.name},
        ) from exc
    preprocess_ms = _elapsed_ms(preprocess_start)

    detections, inference_timing = _normalize_inference_result(run_yolo_image(upload_path, model, confidence_threshold))
    result_image_start = time.perf_counter()
    result_bucket, result_key, result_path = copy_result_image(upload_path, image_file.filename or upload_path.name)
    draw_result_image(upload_path, result_path, detections)
    result_image_save_ms = _elapsed_ms(result_image_start)

    original_info = file_info(upload_bucket, upload_key)
    result_info = file_info(result_bucket, result_key)
    artifacts = {
        "original_image_key": upload_key,
        "annotated_image_key": result_key,
        "crop_keys": [],
    }
    detection_result = build_detection_result(
        model,
        image_info,
        detections,
        artifacts,
        confidence_threshold,
        timings=_round_timing({
            **inference_timing,
            "preprocess_ms": preprocess_ms,
            "result_image_save_ms": result_image_save_ms,
            "device": None,
            "model_cached": False,
        }),
    )
    record_id = None
    if save_record_flag:
        record_save_start = time.perf_counter()
        record_id = save_record(db, user["id"], model_id, original_info, result_info, detection_result, confidence_threshold)
        detection_result["timing"]["record_save_ms"] = round(_elapsed_ms(record_save_start), 3)
    detection_result["timing"]["total_api_ms"] = round(_elapsed_ms(api_start), 3)
    if record_id:
        _update_record_detection_result(db, record_id, detection_result)
    detection_status = detection_result["summary"]["detection_status"]
    return {
        "record_id": record_id,
        "detection_status": detection_status,
        "original_image": original_info,
        "result_image": result_info,
        "detection_result": detection_result,
    }


def list_records(db, user, page=1, page_size=20):
    offset = (page - 1) * page_size
    if int(user["role"]) == 1:
        total = db.execute("SELECT COUNT(*) AS n FROM detection_records").fetchone()["n"]
        rows = db.execute("SELECT * FROM detection_records ORDER BY create_time DESC LIMIT ? OFFSET ?", (page_size, offset)).fetchall()
    else:
        total = db.execute("SELECT COUNT(*) AS n FROM detection_records WHERE user_id=?", (user["id"],)).fetchone()["n"]
        rows = db.execute("SELECT * FROM detection_records WHERE user_id=? ORDER BY create_time DESC LIMIT ? OFFSET ?", (user["id"], page_size, offset)).fetchall()
    return {"items": [_record_to_dict(r) for r in rows], "total": total, "page": page, "page_size": page_size}


def get_record(db, user, record_id):
    if int(user["role"]) == 1:
        row = db.execute("SELECT * FROM detection_records WHERE id=?", (record_id,)).fetchone()
    else:
        row = db.execute("SELECT * FROM detection_records WHERE id=? AND user_id=?", (record_id, user["id"])).fetchone()
    return _record_to_dict(row) if row else None
