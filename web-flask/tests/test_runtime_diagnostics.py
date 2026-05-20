import hashlib
import io
import sqlite3
from pathlib import Path

from PIL import Image

from ai.yolo_infer import InferenceUnavailable


def _login_headers(client):
    token = __import__("conftest").login(client)
    return {"Authorization": f"Bearer {token}"}


def _png_upload(filename="sample.png"):
    buf = io.BytesIO()
    Image.new("RGB", (32, 32), color="white").save(buf, format="PNG")
    buf.seek(0)
    return buf, filename


def _set_model_weight(client, weight_path):
    db_path = Path(client.application.config["DATABASE"])
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("UPDATE models SET weight_path=? WHERE id=?", (str(weight_path), "m_yolo26n_dev"))
        conn.commit()
    finally:
        conn.close()


def test_published_models_include_runtime_diagnostic(client, tmp_path):
    weight = tmp_path / "yolo26n.pt"
    weight.write_bytes(b"phase2b-runtime-diagnostic")
    _set_model_weight(client, weight)

    rv = client.get("/api/models/published", headers=_login_headers(client))

    assert rv.status_code == 200
    model = rv.get_json()["data"][0]
    diagnostic = model["runtime_diagnostic"]
    assert model["weight_exists"] is True
    assert model["is_dev_placeholder"] is True
    assert diagnostic["active_weight_path"] == str(weight)
    assert diagnostic["weight_exists"] is True
    assert diagnostic["weight_sha256"] == hashlib.sha256(weight.read_bytes()).hexdigest()
    assert diagnostic["is_dev_placeholder"] is True
    assert diagnostic["ultralytics_import_status"] in {"available", "missing"}
    assert "ultralytics_importable" in diagnostic
    assert "ultralytics_version" in diagnostic


def test_detection_image_dependency_unavailable_error(client, monkeypatch):
    import services.detection_service as detection_service

    def unavailable(*_args, **_kwargs):
        raise InferenceUnavailable(
            "ultralytics dependency is unavailable; real YOLO inference was not executed",
            reason="dependency_unavailable",
            details={"dependency": "ultralytics"},
        )

    monkeypatch.setattr(detection_service, "run_yolo_image", unavailable)
    image, filename = _png_upload()

    rv = client.post(
        "/api/detection/image",
        headers=_login_headers(client),
        data={"image": (image, filename), "model_id": "m_yolo26n_dev"},
        content_type="multipart/form-data",
    )

    assert rv.status_code == 500
    payload = rv.get_json()
    assert payload["data"]["reason"] == "dependency_unavailable"
    assert payload["data"]["dependency"] == "ultralytics"


def test_detection_image_weight_missing_error(client, monkeypatch):
    import services.detection_service as detection_service

    def missing(*_args, **_kwargs):
        raise InferenceUnavailable(
            "model weight not found: missing.pt",
            reason="weight_missing",
            details={"weight_path": "missing.pt"},
        )

    monkeypatch.setattr(detection_service, "run_yolo_image", missing)
    image, filename = _png_upload()

    rv = client.post(
        "/api/detection/image",
        headers=_login_headers(client),
        data={"image": (image, filename), "model_id": "m_yolo26n_dev"},
        content_type="multipart/form-data",
    )

    assert rv.status_code == 500
    payload = rv.get_json()
    assert payload["data"]["reason"] == "weight_missing"
    assert payload["data"]["weight_path"] == "missing.pt"


def test_detection_image_invalid_image_error(client):
    rv = client.post(
        "/api/detection/image",
        headers=_login_headers(client),
        data={"image": (io.BytesIO(b"not an image"), "bad.png"), "model_id": "m_yolo26n_dev"},
        content_type="multipart/form-data",
    )

    assert rv.status_code == 400
    payload = rv.get_json()
    assert payload["data"]["reason"] == "invalid_image"


def test_detection_image_no_detection_branch(client, monkeypatch):
    import services.detection_service as detection_service

    monkeypatch.setattr(
        detection_service,
        "run_yolo_image",
        lambda *_args, **_kwargs: (
            [],
            {"inference_ms": 12.5, "model_load_ms": 3.0, "postprocess_ms": 1.0},
        ),
    )
    image, filename = _png_upload()

    rv = client.post(
        "/api/detection/image",
        headers=_login_headers(client),
        data={"image": (image, filename), "model_id": "m_yolo26n_dev", "save_record": "true"},
        content_type="multipart/form-data",
    )

    assert rv.status_code == 200, rv.get_json()
    payload = rv.get_json()["data"]
    assert payload["record_id"].startswith("dr_")
    assert payload["detection_status"] == "no_detection"
    assert payload["detection_result"]["summary"]["total_detections"] == 0
    assert payload["detection_result"]["summary"]["detection_status"] == "no_detection"
    assert payload["detection_result"]["schema_version"] == "detection_result.v1"
    timing = payload["detection_result"]["timing"]
    assert timing["inference_ms"] == 12.5
    assert timing["model_load_ms"] == 3.0
    assert timing["postprocess_ms"] == 1.0
    assert timing["preprocess_ms"] >= 0
    assert timing["result_image_save_ms"] >= 0
    assert timing["record_save_ms"] >= 0
    assert timing["total_api_ms"] >= 0

    detail = client.get(f"/api/detection/records/{payload['record_id']}", headers=_login_headers(client))
    assert detail.status_code == 200
    saved_result = detail.get_json()["data"]["detection_result"]
    assert saved_result["schema_version"] == "detection_result.v1"
    assert saved_result["timing"]["total_api_ms"] == timing["total_api_ms"]
    assert saved_result["timing"]["record_save_ms"] == timing["record_save_ms"]


def test_detection_image_successful_detection_branch(client, monkeypatch):
    import services.detection_service as detection_service

    detection = {
        "detection_id": None,
        "object_index": 0,
        "class_id": 0,
        "class_name": "floating_object",
        "class_display_name": "floating_object",
        "confidence": 0.9,
        "bbox_xyxy": [1.0, 1.0, 20.0, 20.0],
        "bbox_xywhn": [0.5, 0.5, 0.5, 0.5],
        "bbox_format": "xyxy_pixel",
        "area_px": 361.0,
        "track_id": None,
        "crop_key": None,
    }
    monkeypatch.setattr(
        detection_service,
        "run_yolo_image",
        lambda *_args, **_kwargs: (
            [detection],
            {"inference_ms": 10.0, "model_load_ms": 2.0, "postprocess_ms": 0.5},
        ),
    )
    image, filename = _png_upload()

    rv = client.post(
        "/api/detection/image",
        headers=_login_headers(client),
        data={"image": (image, filename), "model_id": "m_yolo26n_dev", "save_record": "true"},
        content_type="multipart/form-data",
    )

    assert rv.status_code == 200, rv.get_json()
    payload = rv.get_json()["data"]
    assert payload["record_id"].startswith("dr_")
    assert payload["detection_status"] == "detected"
    assert payload["result_image"]["url"].startswith("/api/files/results/")
    assert payload["detection_result"]["summary"]["total_detections"] == 1
    assert payload["detection_result"]["summary"]["detection_status"] == "detected"
    assert payload["detection_result"]["schema_version"] == "detection_result.v1"
    timing = payload["detection_result"]["timing"]
    assert timing["inference_ms"] == 10.0
    assert timing["model_load_ms"] == 2.0
    assert timing["postprocess_ms"] == 0.5
    assert timing["preprocess_ms"] >= 0
    assert timing["result_image_save_ms"] >= 0
    assert timing["record_save_ms"] >= 0
    assert timing["total_api_ms"] >= 0
