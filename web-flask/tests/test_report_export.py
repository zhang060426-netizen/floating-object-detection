import io
import sqlite3
from pathlib import Path

from PIL import Image


def _login_headers(client, username="admin", password="admin123"):
    token = __import__("conftest").login(client, username=username, password=password)
    return {"Authorization": f"Bearer {token}"}


def _write_png(storage_root, bucket="uploads", object_key="images/report-original.png", color="white"):
    path = Path(storage_root) / bucket / object_key
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (24, 24), color=color)
    image.save(path, format="PNG")
    return {"bucket": bucket, "object_key": object_key}


def _create_record(client, headers, *, original=None, result=None, detection_result=None, confidence_threshold=0.5):
    if original is None:
        original = _write_png(client.application.config["STORAGE_ROOT"])
    payload = {
        "model_id": "m_yolo26n_dev",
        "original_image": original,
        "confidence_threshold": confidence_threshold,
    }
    if result is not None:
        payload["result_image"] = result
    if detection_result is not None:
        payload["detection_result"] = detection_result
    rv = client.post("/api/detection/records", headers=headers, json=payload)
    assert rv.status_code == 200, rv.get_json()
    return rv.get_json()["data"]["record_id"]


def _sample_detection_result():
    return {
        "schema_version": "detection_result.v1",
        "model": {
            "model_id": "m_yolo26n_dev",
            "model_name": "YOLO26n Dev Baseline",
            "base_model": "yolo26n",
            "confidence_threshold": 0.5,
        },
        "detections": [
            {
                "object_index": 0,
                "class_id": 0,
                "class_name": "floating_object",
                "class_display_name": "floating_object",
                "confidence": 0.91,
                "bbox_xyxy": [1, 2, 10, 12],
                "area_px": 90,
            }
        ],
        "summary": {
            "total_detections": 1,
            "object_count": 1,
            "has_detections": True,
            "detection_status": "detected",
            "max_confidence": 0.91,
            "avg_confidence": 0.91,
            "class_counts": {"floating_object": 1},
        },
        "timing": {"inference_ms": 12.5, "total_api_ms": 30.0},
    }


def _assert_docx_response(rv, record_id):
    assert rv.status_code == 200
    assert rv.headers["Content-Type"].startswith(
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    assert f'attachment; filename="detection-report-{record_id}.docx"' in rv.headers["Content-Disposition"]
    assert rv.data.startswith(b"PK")


def test_report_export_requires_jwt(client):
    headers = _login_headers(client)
    record_id = _create_record(client, headers, detection_result=_sample_detection_result())

    rv = client.get(f"/api/detection/records/{record_id}/report.docx")

    assert rv.status_code == 401


def test_login_user_exports_own_record_success(client):
    headers = _login_headers(client, username="test", password="123456")
    result = _write_png(client.application.config["STORAGE_ROOT"], "results", "images/report-result.png", color="red")
    record_id = _create_record(client, headers, result=result, detection_result=_sample_detection_result())

    rv = client.get(f"/api/detection/records/{record_id}/report.docx", headers=headers)

    _assert_docx_response(rv, record_id)


def test_report_export_content_type_is_docx_and_body_is_zip(client):
    headers = _login_headers(client)
    record_id = _create_record(client, headers, detection_result=_sample_detection_result())

    rv = client.get(f"/api/detection/records/{record_id}/report.docx", headers=headers)

    _assert_docx_response(rv, record_id)


def test_report_export_succeeds_when_result_image_empty(client):
    headers = _login_headers(client)
    record_id = _create_record(client, headers, result=None, detection_result=_sample_detection_result())

    rv = client.get(f"/api/detection/records/{record_id}/report.docx", headers=headers)

    _assert_docx_response(rv, record_id)


def test_report_export_detection_result_missing_does_not_500(client):
    headers = _login_headers(client)
    record_id = _create_record(client, headers, detection_result={})
    db_path = Path(client.application.config["DATABASE"])
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("UPDATE detection_records SET detection_result=NULL WHERE id=?", (record_id,))
        conn.commit()
    finally:
        conn.close()

    rv = client.get(f"/api/detection/records/{record_id}/report.docx", headers=headers)

    _assert_docx_response(rv, record_id)


def test_normal_user_cannot_export_other_users_record_returns_404(client):
    admin_headers = _login_headers(client)
    user_headers = _login_headers(client, username="test", password="123456")
    record_id = _create_record(client, admin_headers, detection_result=_sample_detection_result())

    rv = client.get(f"/api/detection/records/{record_id}/report.docx", headers=user_headers)

    assert rv.status_code == 404


def test_report_export_missing_record_returns_404(client):
    headers = _login_headers(client)

    rv = client.get("/api/detection/records/dr_missing/report.docx", headers=headers)

    assert rv.status_code == 404
