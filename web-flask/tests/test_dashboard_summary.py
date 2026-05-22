import json
import sqlite3
from pathlib import Path


def _login_headers(client, username="admin", password="admin123"):
    token = __import__("conftest").login(client, username=username, password=password)
    return {"Authorization": f"Bearer {token}"}


def _insert_record(
    client,
    *,
    record_id,
    user_id,
    detection_result=None,
    create_time="2026-05-22 10:00:00",
    object_key=None,
    result_object_key=None,
):
    db_path = Path(client.application.config["DATABASE"])
    payload = None if detection_result is None else json.dumps(detection_result, ensure_ascii=False)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO detection_records(
              id, user_id, model_id, original_image_bucket, original_image_object_key,
              result_image_bucket, result_image_object_key, detection_result,
              confidence_threshold, create_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record_id,
                user_id,
                "m_yolo26n_dev",
                "uploads",
                object_key or f"images/{record_id}.png",
                "results" if result_object_key else None,
                result_object_key,
                payload,
                0.5,
                create_time,
            ),
        )
        conn.commit()
    finally:
        conn.close()


def _summary(client, headers):
    rv = client.get("/api/detection/dashboard/summary", headers=headers)
    assert rv.status_code == 200, rv.get_json()
    return rv.get_json()["data"]


def _detected_result(*detections, summary=None):
    result = {
        "schema_version": "detection_result.v1",
        "detections": list(detections),
    }
    if summary is not None:
        result["summary"] = summary
    return result


def test_dashboard_summary_requires_jwt(client):
    rv = client.get("/api/detection/dashboard/summary")

    assert rv.status_code == 401


def test_dashboard_summary_normal_user_only_counts_own_records_and_handles_edge_cases(client):
    headers = _login_headers(client, username="test", password="123456")
    _insert_record(
        client,
        record_id="dr_user_detected",
        user_id=2,
        create_time="2026-05-22 10:00:00",
        result_object_key="images/dr_user_detected_result.png",
        detection_result=_detected_result(
            {"class_name": "floating_object", "confidence": 0.9},
            {"class_name": "floating_object"},
            summary={"total_detections": 2, "has_detections": True, "detection_status": "detected"},
        ),
    )
    _insert_record(
        client,
        record_id="dr_user_empty",
        user_id=2,
        create_time="2026-05-22 10:05:00",
        detection_result=_detected_result(
            summary={"total_detections": 0, "has_detections": False, "detection_status": "no_detection"},
        ),
    )
    _insert_record(
        client,
        record_id="dr_user_missing_result",
        user_id=2,
        create_time="2026-05-22 10:10:00",
        detection_result=None,
    )
    _insert_record(
        client,
        record_id="dr_admin_other",
        user_id=1,
        create_time="2026-05-22 10:20:00",
        detection_result=_detected_result({"class_name": "floating_object", "confidence": 0.5}),
    )

    data = _summary(client, headers)

    assert data["total_records"] == 3
    assert data["total_targets"] == 2
    assert data["average_confidence"] == 0.9
    assert data["detected_records"] == 1
    assert data["no_detection_records"] == 1
    assert data["unknown_records"] == 1
    assert data["latest_detection_time"] == "2026-05-22 10:10:00"
    assert len(data["recent_records"]) == 3
    assert data["recent_records"][0]["record_id"] == "dr_user_missing_result"
    assert data["recent_records"][0]["target_count"] == 0
    assert data["recent_records"][0]["detection_status"] == "unknown"
    assert data["recent_records"][0]["original_filename"] == "dr_user_missing_result.png"
    assert "original_image" in data["recent_records"][0]


def test_dashboard_summary_admin_counts_all_records(client):
    headers = _login_headers(client)
    _insert_record(
        client,
        record_id="dr_admin_detected",
        user_id=1,
        create_time="2026-05-22 11:00:00",
        detection_result=_detected_result(
            {"class_name": "floating_object", "confidence": 0.5},
            summary={"total_detections": 1, "detection_status": "detected"},
        ),
    )
    _insert_record(
        client,
        record_id="dr_user_detected",
        user_id=2,
        create_time="2026-05-22 11:05:00",
        detection_result=_detected_result(
            {"class_name": "floating_object", "confidence": 0.9},
            summary={"total_detections": 1, "detection_status": "detected"},
        ),
    )

    data = _summary(client, headers)

    assert data["total_records"] == 2
    assert data["total_targets"] == 2
    assert data["average_confidence"] == 0.7
    assert data["detected_records"] == 2
    assert data["latest_detection_time"] == "2026-05-22 11:05:00"
    assert [item["record_id"] for item in data["recent_records"]] == ["dr_user_detected", "dr_admin_detected"]


def test_dashboard_summary_old_record_missing_summary_falls_back_to_detections_length(client):
    headers = _login_headers(client)
    _insert_record(
        client,
        record_id="dr_legacy_no_summary",
        user_id=1,
        detection_result=_detected_result(
            {"class_name": "floating_object", "confidence": 0.8},
            {"class_name": "floating_object", "confidence": 0.6},
        ),
    )

    data = _summary(client, headers)

    assert data["total_records"] == 1
    assert data["total_targets"] == 2
    assert data["detected_records"] == 1
    assert data["average_confidence"] == 0.7
    assert data["recent_records"][0]["target_count"] == 2
    assert data["recent_records"][0]["detection_status"] == "detected"


def test_dashboard_summary_malformed_detection_result_uses_safe_unknown_fallback(client):
    headers = _login_headers(client)
    _insert_record(client, record_id="dr_malformed", user_id=1)
    db_path = Path(client.application.config["DATABASE"])
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("UPDATE detection_records SET detection_result=? WHERE id=?", ("{not-json", "dr_malformed"))
        conn.commit()
    finally:
        conn.close()

    data = _summary(client, headers)

    assert data["total_records"] == 1
    assert data["total_targets"] == 0
    assert data["average_confidence"] is None
    assert data["unknown_records"] == 1
    assert data["recent_records"][0]["detection_status"] == "unknown"
