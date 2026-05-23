import json
import time
import uuid
from pathlib import Path

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


def _keyword_like_pattern(keyword):
    escaped = str(keyword).lower().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{escaped}%"


def list_records(db, user, page=1, page_size=20, keyword=None, model_id=None, detection_status=None, date_start=None, date_end=None):
    conditions = []
    params = []
    if int(user["role"]) != 1:
        conditions.append("user_id=?")
        params.append(user["id"])
    if keyword:
        conditions.append("LOWER(original_image_object_key) LIKE ? ESCAPE '\\'")
        params.append(_keyword_like_pattern(keyword))
    if model_id:
        conditions.append("model_id=?")
        params.append(model_id)
    if date_start:
        conditions.append("create_time>=?")
        params.append(date_start)
    if date_end:
        conditions.append("create_time<=?")
        params.append(date_end)

    where_clause = ""
    if conditions:
        where_clause = " WHERE " + " AND ".join(conditions)
    query = "SELECT * FROM detection_records" + where_clause + " ORDER BY create_time DESC"

    offset = (page - 1) * page_size
    if detection_status:
        rows = db.execute(query, tuple(params)).fetchall()
        rows = [row for row in rows if _canonical_detection_status(row) == detection_status]
        total = len(rows)
        page_rows = rows[offset:offset + page_size]
    else:
        total = db.execute("SELECT COUNT(*) AS n FROM detection_records" + where_clause, tuple(params)).fetchone()["n"]
        page_rows = db.execute(query + " LIMIT ? OFFSET ?", tuple(params) + (page_size, offset)).fetchall()
    return {"items": [_record_to_dict(r) for r in page_rows], "total": total, "page": page, "page_size": page_size}


def get_record(db, user, record_id):
    if int(user["role"]) == 1:
        row = db.execute("SELECT * FROM detection_records WHERE id=?", (record_id,)).fetchone()
    else:
        row = db.execute("SELECT * FROM detection_records WHERE id=? AND user_id=?", (record_id, user["id"])).fetchone()
    return _record_to_dict(row) if row else None


_DASHBOARD_SUMMARY_TARGET_KEYS = ("total_detections", "object_count", "target_count")
_DETECTED_STATUSES = {"detected", "has_detection", "success"}
_NO_DETECTION_STATUSES = {"no_detection", "none", "empty"}


def _safe_json_dict(value):
    if isinstance(value, dict):
        return value
    if not value:
        return None
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return None
        return parsed if isinstance(parsed, dict) else None
    return None


def _safe_list(value):
    return value if isinstance(value, list) else []


def _safe_int(value):
    if isinstance(value, bool) or value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _safe_float(value):
    if isinstance(value, bool) or value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _record_filename(row):
    object_key = row["original_image_object_key"]
    if not object_key:
        return None
    return Path(str(object_key).replace("\\", "/")).name


def _dashboard_record_stats(row):
    detection_result = _safe_json_dict(row["detection_result"])
    if not detection_result:
        return {
            "target_count": 0,
            "detection_status": "unknown",
            "confidences": [],
        }

    summary = detection_result.get("summary") if isinstance(detection_result.get("summary"), dict) else {}
    detections = _safe_list(detection_result.get("detections"))

    target_count = None
    for key in _DASHBOARD_SUMMARY_TARGET_KEYS:
        target_count = _safe_int(summary.get(key))
        if target_count is not None:
            break
    if target_count is None:
        target_count = len(detections)

    status = summary.get("detection_status")
    if isinstance(status, str) and status:
        normalized_status = status
    elif summary.get("has_detections") is True or summary.get("has_detection") is True:
        normalized_status = "detected"
    elif summary.get("has_detections") is False or summary.get("has_detection") is False:
        normalized_status = "no_detection"
    else:
        normalized_status = "detected" if target_count > 0 else "no_detection"

    confidences = []
    for detection in detections:
        if not isinstance(detection, dict):
            continue
        confidence = _safe_float(detection.get("confidence"))
        if confidence is not None:
            confidences.append(confidence)

    return {
        "target_count": target_count,
        "detection_status": normalized_status,
        "confidences": confidences,
    }


def _canonical_detection_status(row):
    stats = _dashboard_record_stats(row)
    status = str(stats["detection_status"] or "").lower()
    if status == "unknown":
        return "unknown"
    if status in _DETECTED_STATUSES or (status not in _NO_DETECTION_STATUSES and stats["target_count"] > 0):
        return "detected"
    if status in _NO_DETECTION_STATUSES or stats["target_count"] == 0:
        return "no_detection"
    return "unknown"


def _dashboard_record_item(row, stats):
    original_image = file_info(row["original_image_bucket"], row["original_image_object_key"])
    filename = _record_filename(row)
    item = {
        "id": row["id"],
        "record_id": row["id"],
        "create_time": row["create_time"],
        "model_id": row["model_id"],
        "target_count": stats["target_count"],
        "detection_status": stats["detection_status"],
        "original_image": original_image,
    }
    if filename:
        item["original_filename"] = filename
    return item


def dashboard_summary(db, user, recent_limit=5):
    limit = max(1, min(10, int(recent_limit or 5)))
    if int(user["role"]) == 1:
        rows = db.execute("SELECT * FROM detection_records ORDER BY create_time DESC, id DESC").fetchall()
    else:
        rows = db.execute(
            "SELECT * FROM detection_records WHERE user_id=? ORDER BY create_time DESC, id DESC",
            (user["id"],),
        ).fetchall()

    total_targets = 0
    detected_records = 0
    no_detection_records = 0
    unknown_records = 0
    confidences = []
    recent_records = []

    for row in rows:
        stats = _dashboard_record_stats(row)
        total_targets += stats["target_count"]
        confidences.extend(stats["confidences"])

        status = str(stats["detection_status"] or "").lower()
        if status in _DETECTED_STATUSES or (status not in _NO_DETECTION_STATUSES and stats["target_count"] > 0):
            detected_records += 1
        elif status in _NO_DETECTION_STATUSES or stats["target_count"] == 0:
            no_detection_records += 1
        else:
            unknown_records += 1

        if stats["detection_status"] == "unknown":
            # Malformed or missing detection_result is a separate unknown bucket, not no-detection.
            if no_detection_records > 0:
                no_detection_records -= 1
            unknown_records += 1

        if len(recent_records) < limit:
            recent_records.append(_dashboard_record_item(row, stats))

    average_confidence = None
    if confidences:
        average_confidence = round(sum(confidences) / len(confidences), 6)

    return {
        "total_records": len(rows),
        "total_targets": total_targets,
        "average_confidence": average_confidence,
        "detected_records": detected_records,
        "no_detection_records": no_detection_records,
        "unknown_records": unknown_records,
        "latest_detection_time": rows[0]["create_time"] if rows else None,
        "recent_records": recent_records,
    }
