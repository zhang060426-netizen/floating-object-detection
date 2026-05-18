import io

from PIL import Image


def _login_headers(client):
    token = __import__("conftest").login(client)
    return {"Authorization": f"Bearer {token}"}


def _png_upload(filename="sample.png"):
    buf = io.BytesIO()
    Image.new("RGB", (16, 16), color="white").save(buf, format="PNG")
    buf.seek(0)
    return buf, filename


def test_health_db_reports_sqlite_ready(client):
    rv = client.get("/api/health/db")

    assert rv.status_code == 200
    assert rv.get_json()["data"] == {"status": "ok", "database": "sqlite"}


def test_detection_image_rejects_out_of_range_confidence(client):
    image, filename = _png_upload()

    rv = client.post(
        "/api/detection/image",
        headers=_login_headers(client),
        data={"image": (image, filename), "model_id": "m_yolo26n_dev", "confidence_threshold": "1.5"},
        content_type="multipart/form-data",
    )

    assert rv.status_code == 400
    payload = rv.get_json()
    assert payload["data"]["reason"] == "bad_request"
    assert payload["data"]["field"] == "confidence_threshold"


def test_detection_image_rejects_unsupported_extension_as_client_error(client):
    rv = client.post(
        "/api/detection/image",
        headers=_login_headers(client),
        data={"image": (io.BytesIO(b"plain text"), "sample.txt"), "model_id": "m_yolo26n_dev"},
        content_type="multipart/form-data",
    )

    assert rv.status_code == 400
    payload = rv.get_json()
    assert payload["data"]["reason"] == "unsupported_image_type"


def test_create_record_rejects_bad_confidence_without_500(client):
    rv = client.post(
        "/api/detection/records",
        headers=_login_headers(client),
        json={
            "model_id": "m_yolo26n_dev",
            "original_image": {"bucket": "uploads", "object_key": "images/test.png"},
            "detection_result": {"schema_version": "detection_result.v1"},
            "confidence_threshold": "bad",
        },
    )

    assert rv.status_code == 400
    payload = rv.get_json()
    assert payload["data"]["field"] == "confidence_threshold"
